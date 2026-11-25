---
name: websockets
description: "Apply when building real-time features with WebSockets: chat, live updates, notifications, collaborative tools, dashboards. Covers: FastAPI WebSocket, connection management, broadcast, reconnection. Trigger for: WebSocket, real-time, live, chat, push, SSE."
---

# WEBSOCKETS — Real-Time Production Patterns

## Connection Manager
```python
from fastapi import WebSocket
from typing import dict

class ConnectionManager:
    def __init__(self):
        # room_id → set of connected clients
        self.rooms: dict[str, set[WebSocket]] = {}

    async def connect(self, ws: WebSocket, room_id: str):
        await ws.accept()
        self.rooms.setdefault(room_id, set()).add(ws)

    async def disconnect(self, ws: WebSocket, room_id: str):
        self.rooms.get(room_id, set()).discard(ws)

    async def broadcast(self, room_id: str, message: dict):
        dead = set()
        for ws in self.rooms.get(room_id, set()):
            try:
                await ws.send_json(message)
            except Exception:
                dead.add(ws)
        self.rooms[room_id] -= dead  # clean disconnected clients

manager = ConnectionManager()
```

## FastAPI Endpoint
```python
@app.websocket("/ws/{room_id}")
async def websocket_endpoint(ws: WebSocket, room_id: str,
                             token: str = Query(...)):
    # Auth before accepting
    try:
        user = verify_token(token)
    except HTTPException:
        await ws.close(code=1008)  # Policy violation
        return

    await manager.connect(ws, room_id)
    try:
        while True:
            data = await asyncio.wait_for(ws.receive_json(), timeout=60)
            # Validate message
            message = ChatMessage.model_validate(data)
            await manager.broadcast(room_id, {
                "user": user.id,
                "content": message.content,
                "ts": datetime.utcnow().isoformat()
            })
    except asyncio.TimeoutError:
        await ws.send_json({"type": "ping"})
    except WebSocketDisconnect:
        manager.disconnect(ws, room_id)
```

## Client Reconnection (JavaScript)
```javascript
class ReconnectingWebSocket {
    constructor(url) {
        this.url = url;
        this.attempts = 0;
        this.connect();
    }
    connect() {
        this.ws = new WebSocket(this.url);
        this.ws.onclose = () => {
            const delay = Math.min(1000 * 2 ** this.attempts, 30000);
            setTimeout(() => { this.attempts++; this.connect(); }, delay);
        };
        this.ws.onopen = () => { this.attempts = 0; };
    }
}
```

## Forbidden
❌ No authentication on WebSocket endpoint
❌ No timeout/ping — zombie connections accumulate
❌ Storing connection objects in a database
❌ Sending large payloads (> 64KB) — use chunking
❌ No error handling on `send()` — crashes on disconnected client
