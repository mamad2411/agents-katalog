---
name: realtime-websocket
description: |
  Real-time features with WebSockets and Server-Sent Events. Apply when building live
  notifications, chat, live dashboards, collaborative features, or real-time order tracking.
  Covers Django Channels, FastAPI WebSockets, Redis pub/sub, and React client hooks.
---

# Real-Time & WebSocket Patterns

## FastAPI WebSocket
```python
# Connection manager for multiple clients
from fastapi import WebSocket
from typing import DefaultDict
from collections import defaultdict

class ConnectionManager:
    def __init__(self):
        self.connections: DefaultDict[str, list[WebSocket]] = defaultdict(list)

    async def connect(self, room: str, websocket: WebSocket):
        await websocket.accept()
        self.connections[room].append(websocket)

    def disconnect(self, room: str, websocket: WebSocket):
        self.connections[room].remove(websocket)
        if not self.connections[room]:
            del self.connections[room]

    async def broadcast(self, room: str, message: dict):
        dead = []
        for ws in self.connections.get(room, []):
            try:
                await ws.send_json(message)
            except WebSocketDisconnect:
                dead.append(ws)
        for ws in dead:
            self.disconnect(room, ws)

manager = ConnectionManager()

@router.websocket("/ws/{room_id}")
async def websocket_endpoint(
    websocket: WebSocket,
    room_id: str,
    token: str = Query(...),
):
    user = await verify_ws_token(token)
    if not user:
        await websocket.close(code=4001)
        return

    await manager.connect(room_id, websocket)
    try:
        while True:
            data = await websocket.receive_json()
            await handle_ws_message(room_id, user, data, manager)
    except WebSocketDisconnect:
        manager.disconnect(room_id, websocket)
```

## Redis Pub/Sub for Multi-Server Broadcasting
```python
# When running multiple backend instances
import aioredis

async def redis_subscriber(channel: str):
    redis = await aioredis.create_redis_pool(settings.REDIS_URL)
    receiver = await redis.subscribe(channel)
    async for message in receiver[0].iter():
        data = json.loads(message)
        await manager.broadcast(data['room'], data['payload'])

# Publish from anywhere (even Celery tasks)
async def publish_to_room(room: str, event_type: str, payload: dict):
    redis = await get_redis()
    await redis.publish(f"room:{room}", json.dumps({
        "room": room,
        "payload": {"type": event_type, "data": payload, "timestamp": datetime.utcnow().isoformat()}
    }))
```

## React WebSocket Hook
```typescript
function useWebSocket(url: string, options: WSOptions = {}) {
  const [status, setStatus] = useState<'connecting' | 'open' | 'closed'>('connecting');
  const [lastMessage, setLastMessage] = useState<WSMessage | null>(null);
  const wsRef = useRef<WebSocket | null>(null);
  const reconnectTimer = useRef<ReturnType<typeof setTimeout>>();

  const connect = useCallback(() => {
    const ws = new WebSocket(url);
    wsRef.current = ws;

    ws.onopen = () => setStatus('open');
    ws.onmessage = (e) => setLastMessage(JSON.parse(e.data));
    ws.onclose = (e) => {
      setStatus('closed');
      if (!e.wasClean && options.reconnect !== false) {
        reconnectTimer.current = setTimeout(connect, 3000);
      }
    };
  }, [url]);

  useEffect(() => {
    connect();
    return () => {
      clearTimeout(reconnectTimer.current);
      wsRef.current?.close(1000, 'Component unmounted');
    };
  }, [connect]);

  const send = useCallback((data: object) => {
    if (wsRef.current?.readyState === WebSocket.OPEN) {
      wsRef.current.send(JSON.stringify(data));
    }
  }, []);

  return { status, lastMessage, send };
}

// Usage
function OrderTracker({ orderId }: { orderId: string }) {
  const { status, lastMessage } = useWebSocket(
    `${WS_BASE}/ws/orders/${orderId}?token=${token}`
  );

  useEffect(() => {
    if (lastMessage?.type === 'order.status_changed') {
      queryClient.invalidateQueries({ queryKey: queryKeys.orders.detail(orderId) });
      toast.info(`Order status: ${lastMessage.data.status}`);
    }
  }, [lastMessage]);

  return <OrderStatusBadge status={order?.status} isLive={status === 'open'} />;
}
```
