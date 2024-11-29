import fastapi, asyncio


class WebSocketHandler:
    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(WebSocketHandler, cls).__new__(cls)
        return cls.instance

    def initialize(self, websocket: fastapi.WebSocket):
        self.websocket = websocket
        self.connection_closed_event = asyncio.Event()
        self.execution_complete_event = asyncio.Event()
        return self
