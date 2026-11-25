---
name: python-websockets
description: "When to activate: WebSockets, real-time, FastAPI WebSocket, websockets library, broadcasting, connection management"
origin: zakr
metadata:
  namespace: zakr/devtools-pack
  version: 1.0.0
  category: engineering
  language: python
  platforms: [claude-code, codex, gemini-cli, cursor, aider, windsurf]
---

# Python WebSocket Patterns

## FastAPI WebSocket
```python
from fastapi import WebSocket, WebSocketDisconnect, Depends
from typing import Any
import json

class ConnectionManager:
    def __init__(self) -> None:
        self.active: dict[str, WebSocket] = {}
    
    async def connect(self, client_id: str, ws: WebSocket) -> None:
        await ws.accept()
        self.active[client_id] = ws
    
    def disconnect(self, client_id: str) -> None:
        self.active.pop(client_id, None)
    
    async def send(self, client_id: str, data: Any) -> None:
        ws = self.active.get(client_id)
        if ws:
            await ws.send_text(json.dumps(data))
    
    async def broadcast(self, data: Any, exclude: str | None = None) -> None:
        payload = json.dumps(data)
        for cid, ws in list(self.active.items()):
            if cid != exclude:
                try:
                    await ws.send_text(payload)
                except Exception:
                    self.disconnect(cid)

manager = ConnectionManager()

@app.websocket("/ws/{client_id}")
async def websocket_endpoint(ws: WebSocket, client_id: str, token: str = "") -> None:
    user = await authenticate_token(token)
    if not user:
        await ws.close(code=4001, reason="Unauthorized")
        return
    
    await manager.connect(client_id, ws)
    try:
        while True:
            data = await ws.receive_text()
            message = json.loads(data)
            await handle_message(client_id, message, manager)
    except WebSocketDisconnect:
        manager.disconnect(client_id)
        await manager.broadcast({"type": "user_left", "client_id": client_id})
```

## Redis Pub/Sub for Multi-Instance Broadcast
```python
import aioredis

async def websocket_redis_handler(ws: WebSocket, channel: str, redis: Redis) -> None:
    pubsub = redis.pubsub()
    await pubsub.subscribe(channel)
    
    try:
        async for message in pubsub.listen():
            if message["type"] == "message":
                await ws.send_text(message["data"])
    finally:
        await pubsub.unsubscribe(channel)

# Publisher (from API endpoint or worker)
async def publish_event(redis: Redis, channel: str, event: dict) -> None:
    await redis.publish(channel, json.dumps(event))
```

## Heartbeat Pattern
```python
@app.websocket("/ws/{client_id}")
async def ws_with_heartbeat(ws: WebSocket, client_id: str) -> None:
    await ws.accept()
    
    async def heartbeat() -> None:
        while True:
            await asyncio.sleep(30)
            try:
                await ws.send_text('{"type":"ping"}')
            except Exception:
                break
    
    heartbeat_task = asyncio.create_task(heartbeat())
    try:
        while True:
            data = await ws.receive_text()
            # handle data
    except WebSocketDisconnect:
        pass
    finally:
        heartbeat_task.cancel()
```
