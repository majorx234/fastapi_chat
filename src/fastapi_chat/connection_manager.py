from fastapi import WebSocket
from typing import Dict
import json


class ConnectionManager:
    def __init__(self):
        # Store active connections: {client_id: websocket}
        self.active_connections: Dict[str, WebSocket] = {}

    async def connect(self, client_id: str, websocket: WebSocket):
        await websocket.accept()
        self.active_connections[client_id] = websocket

    def disconnect(self, client_id: str):
        if client_id in self.active_connections:
            del self.active_connections[client_id]

    async def broadcast(self, message: dict, exclude_client: str = None):
        """Sends a message to all connected clients (not exclude_client)"""
        for client_id, connection in self.active_connections.items():
            if client_id != exclude_client:
                await connection.send_text(json.dumps(message))
