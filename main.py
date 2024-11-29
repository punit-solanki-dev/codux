import fastapi, asyncio, subprocess, json
from fastapi import WebSocketDisconnect
from utils.formatters import convert_to_raw_string
from config.socket import WebSocketHandler
from wrappers.python_wrappers import PythonCodeWrapper
from code_analyzer.python_analyzer import is_code_not_safe
from text_console.text_execution import text_executor
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

app = fastapi.FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(text_executor)


@app.websocket("/execute")
async def execute_websocket(websocket: fastapi.WebSocket):
    await websocket.accept()
    handler = WebSocketHandler().initialize(websocket)

    try:
        data = await websocket.receive_text()
        code = json.loads(data).get("code", "")
        if not code:
            await websocket.send_text("Error: No code provided.")
            return
        restricted_code, message = is_code_not_safe("PYTHON", code)
        if restricted_code:
            await websocket.send_text(str(message))
            return
        await execute_code(code, websocket)
    except WebSocketDisconnect:
        print("Client disconnected.")
        handler.connection_closed_event.set()  # Signal that the connection is closed
    except Exception as e:
        print(e)
        await websocket.send_text("Unexpected error occurred.")
    finally:
        # Attempt to close the WebSocket connection
        try:
            await websocket.close()
        except RuntimeError:
            print("WebSocket already closed.")


async def execute_code(code: str, websocket: fastapi.WebSocket):
    """Execute provided Python code and send output."""
    socket_handler = WebSocketHandler()
    wrapped_code = PythonCodeWrapper(code)
    process = subprocess.Popen(
        ["python3", "-u", "-c", wrapped_code.wrap_all()],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        stdin=subprocess.PIPE,
        text=True,
        bufsize=1,
    )

    async def read_stdout():
        while (
            not socket_handler.connection_closed_event.is_set()
            and not socket_handler.execution_complete_event.is_set()
        ):
            output = await asyncio.get_event_loop().run_in_executor(
                None, process.stdout.readline  # type: ignore
            )
            if output == "" and process.poll() is not None:
                socket_handler.execution_complete_event.set()  # Signal that execution is complete
                break
            if output:
                await websocket.send_text(
                    json.dumps({"message": output[:-1], "type": "output"})
                )

    async def read_stderr():
        while (
            not socket_handler.connection_closed_event.is_set()
            and not socket_handler.execution_complete_event.is_set()
        ):
            error_output = await asyncio.get_event_loop().run_in_executor(
                None, process.stderr.readline  # type: ignore
            )
            if error_output == "" and process.poll() is not None:
                socket_handler.execution_complete_event.set()  # Signal that execution is complete
                break
            if error_output:
                await websocket.send_text(
                    json.dumps({"message": error_output.strip(), "type": "error"})
                )

    try:
        await asyncio.gather(
            read_stdout(),
            read_stderr(),
            handle_input(websocket, process),
        )
    finally:
        await websocket.send_text(
            json.dumps({"message": "\n\n====Code execution completed====\n\n", "type": "terminate"})
        )
        print("Closing process")
        if process.poll() is None:  # Check if process is still running
            process.terminate()  # Safely terminate the process
            await asyncio.get_event_loop().run_in_executor(
                None, process.wait
            )  # Wait for the process to terminate


async def handle_input(websocket: fastapi.WebSocket, process):
    """Handle input from the WebSocket client."""
    socket_handler = WebSocketHandler()
    while (
        not socket_handler.connection_closed_event.is_set()
        and not socket_handler.execution_complete_event.is_set()
    ):
        try:
            # Wait for user input from WebSocket client with a timeout
            user_input = await asyncio.wait_for(websocket.receive_text(), timeout=1)
            parsed_user_input = json.loads(user_input)
            if process.stdin:
                process.stdin.write(parsed_user_input['data'] + "\n")
                process.stdin.flush()
        except asyncio.TimeoutError:
            continue  # No input, continue the loop
        except WebSocketDisconnect:
            print("Client disconnected during input handling.")
            socket_handler.connection_closed_event.set()  # Signal that the connection is closed
            break  # Exit the loop if the WebSocket disconnects
        except Exception as e:
            print(e)
            await websocket.send_text("Error while handling input.")
            socket_handler.connection_closed_event.set()  # Signal that the connection is closed
            break
