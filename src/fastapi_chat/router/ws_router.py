from fastapi import APIRouter, WebSocket, WebSocketDisconnect
import json

from fastapi_chat.connection_manager import ConnectionManager


class WsRouter:
    def __init__(self, manager: ConnectionManager):
        self.manager = manager
        self._router = APIRouter(
            prefix="",
            tags=['web socket'],
        )
        self._router.add_api_websocket_route(
            "/ws/{client_id}",
            self.websocket_endpoint,
        )

    async def websocket_endpoint(self, websocket: WebSocket, client_id: str):
        await self.manager.connect(client_id, websocket)

        # join notification
        await self.manager.broadcast(
            {"type": "system", "content": f"User {client_id} joined the chat"},
            exclude_client=client_id
        )

        try:
            while True:
                # Wait for messages from the client
                data = await websocket.receive_text()
                message_data = json.loads(data)

                # Route the message based on type
                if message_data["type"] == "chat":
                    # Broadcast actual message
                    await self.manager.broadcast({
                        "type": "chat",
                        "user": client_id,
                        "content": message_data["content"]
                    }, exclude_client=client_id)

                elif message_data["type"] == "typing":
                    # Broadcast typing status (true/false)
                    await self.manager.broadcast({
                        "type": "typing",
                        "user": client_id,
                        "is_typing": message_data["is_typing"]
                    }, exclude_client=client_id)

        except WebSocketDisconnect:
            self.manager.disconnect(client_id)
            await self.manager.broadcast(
                {"type": "system",
                 "content": f"User {client_id} left the chat"}
            )

    def get_router(self):
        return self._router
