import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from fastapi import FastAPI, WebSocket
from fastapi.middleware.cors import CORSMiddleware
import asyncio
from backend.simulation import run_simulation_tick


app = FastAPI()


# Connecting frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Keeping track of connected clients
clients = []

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    clients.append(websocket)
    
    try:
        while True:
            data = run_simulation_tick()
            # Sending new data to frontend
            await websocket.send_json(data)
            await asyncio.sleep(1) # 1 tick per second
            
    except Exception:
        clients.remove(websocket)