#!/bin/bash

echo "Starting FastAPI Server with Uvicorn"
uvicorn main:app --host 0.0.0.0 --port 8080 --workers 8 --timeout-keep-alive 120