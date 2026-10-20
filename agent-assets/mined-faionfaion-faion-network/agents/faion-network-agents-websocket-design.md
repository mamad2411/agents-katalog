# WebSocket Design

## Summary

**One-sentence:** WebSocket protocol spec: typed message envelope with version + id, heartbeat ping/pong with TTL, exponential reconnect with jitter, backpressure on send queue, auth via short-lived token, JSON-schema validation per message type.

**One-paragraph:** WebSocket connections rot when the message envelope is freeform JSON (clients break on field drift), when there is no heartbeat (NAT dies silently), when reconnect logic hammers the server on outage, when the send queue is unbounded (server OOMs), and when auth is via long-lived cookies (token theft is permanent). This methodology produces a spec: versioned envelope `{v, type, id, ts, payload}`, ping/pong every 30s with TTL, exponential reconnect with full jitter, bounded outgoing queue with shed policy, short-lived (5min) signed token at handshake, JSON schema per message type validated on both sides.

**Ефективно для:**

- Перший WebSocket сервіс - зафіксувати envelope + heartbeat + reconnect.
- Connections silently die після 30 хв - впровадити ping/pong.
- Reconnect storm після збою - exponential backoff + jitter.
- Server OOM від unbounded send queue - bounded + shed policy.
- Auth через cookie - short-lived signed token.

## Applies If (ALL must hold)

- Service uses WebSocket (RFC 6455) for bidirectional real-time messaging.
- Connections are long-lived (>30s) and pass through NAT / corporate firewalls.
- Server has finite memory and accepts many concurrent connections.
- Auth model permits short-lived tokens.

## Skip If (ANY kills it)

- Use case is one-shot SSE (Server-Sent Events) - use SSE methodology.
- Use case is pure REST polling - WebSocket overhead is not justified.
- Tiny demo with <10 concurrent connections.
- Protocol is gRPC bi-directional streaming - use gRPC methodology.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Message taxonomy | list of message types + JSON schema per type | engineering |
| Auth model | short-lived token signing | security |
| Reconnect policy | expected outage window | platform |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| [[rate-limiting]] | WS connections share rate-limit budget with REST API. |
| [[rust-tokio-async]] | common async runtime hosting the WS server. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 7 rules: versioned envelope, heartbeat 30s, reconnect with jitter, bounded send queue, short-lived token, schema per type, close codes | ~1100 |
| `content/02-output-contract.xml` | essential | JSON Schema draft-07 + valid/invalid examples + forbidden patterns | ~900 |
| `content/03-failure-modes.xml` | essential | 4 antipatterns (symptom/root-cause/fix) | ~800 |
| `content/04-procedure.xml` | essential | 5-step plan: envelope, heartbeat, reconnect, send queue, auth + schemas | ~900 |
| `content/05-examples.xml` | essential | Worked example for a multiplayer chat WS service | ~900 |
| `content/06-decision-tree.xml` | essential | Routing tree on observable signals → rule id | ~600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `design-envelope` | sonnet | Per-message-type judgement. |
| `wire-heartbeat` | haiku | Boilerplate setInterval. |
| `reconnect-client` | sonnet | Backoff math + edge cases (token expiry mid-reconnect). |
| `size-send-queue` | opus | Stakes high; wrong shed policy drops user data. |

## Templates

| File | Purpose |
|------|---------|
| `templates/envelope.schema.json` | JSON Schema for the WS envelope + 1 example message type. |
| `templates/client.ts` | Client reconnect + heartbeat skeleton with exponential backoff + full jitter. |
| `templates/connection-manager.py` | Python connection-manager: presence map + heartbeat + room broadcast. |
| `templates/ws-client.ts` | TS WebSocket client wrapper: backoff reconnect + heartbeat + envelope. |
| `templates/_smoke-test.json` | Minimum viable WS spec for validator smoke-test. |

Files the packer does not ship standalone have their bodies inlined under `## Template Contents` at the end of this file - read them there, do not fetch the path.

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-websocket-design.py` | Validate the artefact against `content/02-output-contract.xml` schema. | After draft, before merge; pre-commit. |

## Related

- [[rate-limiting]]
- [[rust-tokio-async]]
- [[api-error-handling]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable inputs - envelope shape, heartbeat presence, reconnect logic, queue boundedness - onto a rule from `content/01-core-rules.xml`. Use it before merging WS code: it catches no-heartbeat and reconnect-storm upstream.

## Template Contents

Bodies of the templates above that the packer does not ship as standalone files, inlined here so they are deliverable.

### `templates/envelope.schema.json`

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "envelope",
  "type": "object",
  "required": [
    "v",
    "type",
    "id",
    "ts",
    "payload"
  ],
  "properties": {
    "v": {
      "type": "integer",
      "enum": [
        1
      ]
    },
    "type": {
      "type": "string"
    },
    "id": {
      "type": "string"
    },
    "ts": {
      "type": "integer"
    },
    "payload": {
      "type": "object"
    }
  }
}
```

### `templates/client.ts`

```typescript
type State = 'closed' | 'connecting' | 'open';

export class WSClient {
  private state: State = 'closed';
  private socket: WebSocket | null = null;
  private attempt = 0;
  private pingTimer?: ReturnType<typeof setInterval>;
  constructor(private url: () => string) {}
  connect(): void {
    this.state = 'connecting';
    const socket = new WebSocket(this.url());
    this.socket = socket;
    socket.onopen = () => { this.state = 'open'; this.attempt = 0; this.startHeartbeat(); };
    socket.onclose = () => { this.state = 'closed'; this.stopHeartbeat(); this.scheduleReconnect(); };
    socket.onmessage = (e) => { /* dispatch */ };
  }
  private scheduleReconnect(): void {
    const base = Math.min(60000, 1000 * 2 ** this.attempt);
    const delay = Math.floor(Math.random() * base);
    this.attempt++;
    setTimeout(() => this.connect(), delay);
  }
  private startHeartbeat(): void {
    this.pingTimer = setInterval(() => this.socket?.send(JSON.stringify({ v: 1, type: 'ping', id: crypto.randomUUID(), ts: Date.now(), payload: {} })), 30000);
  }
  private stopHeartbeat(): void { if (this.pingTimer) clearInterval(this.pingTimer); }
}
```

### `templates/connection-manager.py`

```python
"""
FastAPI WebSocket ConnectionManager.
Manages user connections, channel subscriptions, and broadcast.
Input: user_id (str), channel (str), WSMessage
Output: sends JSON to connected WebSocket clients
"""
from fastapi import WebSocket
from fastapi.websockets import WebSocketState
from dataclasses import dataclass, asdict
from typing import Dict, Set, Optional
from enum import Enum
import asyncio
import json
import logging


class MessageType(str, Enum):
    PING = "ping"
    PONG = "pong"
    SUBSCRIBE = "subscribe"
    UNSUBSCRIBE = "unsubscribe"
    MESSAGE = "message"
    ERROR = "error"
    ACK = "ack"


@dataclass
class WSMessage:
    type: MessageType
    channel: Optional[str] = None
    data: Optional[dict] = None
    id: Optional[str] = None

    def to_json(self) -> str:
        return json.dumps({k: v for k, v in asdict(self).items() if v is not None})


class ConnectionManager:
    def __init__(self):
        self.active_connections: Dict[str, WebSocket] = {}
        self.channel_subscriptions: Dict[str, Set[str]] = {}
        self.user_channels: Dict[str, Set[str]] = {}

    async def connect(self, websocket: WebSocket, user_id: str):
        await websocket.accept()
        if user_id in self.active_connections:
            await self.disconnect(user_id)
        self.active_connections[user_id] = websocket
        self.user_channels[user_id] = set()
        logging.info(f"User {user_id} connected")

    async def disconnect(self, user_id: str):
        if user_id not in self.active_connections:
            return
        for channel in list(self.user_channels.get(user_id, [])):
            await self.unsubscribe(user_id, channel)
        ws = self.active_connections.pop(user_id, None)
        self.user_channels.pop(user_id, None)
        if ws and ws.client_state == WebSocketState.CONNECTED:
            await ws.close()
        logging.info(f"User {user_id} disconnected")

    async def subscribe(self, user_id: str, channel: str):
        if channel not in self.channel_subscriptions:
            self.channel_subscriptions[channel] = set()
        self.channel_subscriptions[channel].add(user_id)
        self.user_channels[user_id].add(channel)
        await self.send_to_user(user_id, WSMessage(
            type=MessageType.ACK, channel=channel, data={"action": "subscribed"}
        ))

    async def unsubscribe(self, user_id: str, channel: str):
        if channel in self.channel_subscriptions:
            self.channel_subscriptions[channel].discard(user_id)
            if not self.channel_subscriptions[channel]:
                del self.channel_subscriptions[channel]
        if user_id in self.user_channels:
            self.user_channels[user_id].discard(channel)

    async def send_to_user(self, user_id: str, message: WSMessage):
        ws = self.active_connections.get(user_id)
        if ws and ws.client_state == WebSocketState.CONNECTED:
            try:
                await ws.send_text(message.to_json())
            except Exception as e:
                logging.error(f"Error sending to {user_id}: {e}")
                await self.disconnect(user_id)

    async def broadcast_to_channel(self, channel: str, message: WSMessage):
        subscribers = self.channel_subscriptions.get(channel, set())
        tasks = [self.send_to_user(uid, message) for uid in subscribers]
        await asyncio.gather(*tasks, return_exceptions=True)
```

### `templates/ws-client.ts`

```typescript
/**
 * TypeScript WebSocket client with reconnect, message queue, and heartbeat.
 * Usage: const ws = new WebSocketClient('wss://api.example.com/ws/user123');
 *        await ws.connect();
 *        const unsubscribe = ws.subscribe('chat:room-1', handler);
 */
interface WSMessage {
  type: 'ping' | 'pong' | 'subscribe' | 'unsubscribe' | 'message' | 'error' | 'ack';
  channel?: string;
  data?: unknown;
  id?: string;
}

type MessageHandler = (message: WSMessage) => void;

class WebSocketClient {
  private ws: WebSocket | null = null;
  private reconnectAttempts = 0;
  private readonly maxReconnectAttempts = 5;
  private readonly reconnectDelay = 1000;
  private pingInterval: ReturnType<typeof setInterval> | null = null;
  private handlers = new Map<string, Set<MessageHandler>>();
  private messageQueue: WSMessage[] = [];
  private isConnected = false;

  constructor(private readonly url: string) {}

  connect(): Promise<void> {
    return new Promise((resolve, reject) => {
      this.ws = new WebSocket(this.url);

      this.ws.onopen = () => {
        this.isConnected = true;
        this.reconnectAttempts = 0;
        this.startPing();
        this.flushQueue();
        resolve();
      };

      this.ws.onclose = () => {
        this.isConnected = false;
        this.stopPing();
        this.handleReconnect();
      };

      this.ws.onerror = (err) => reject(err);

      this.ws.onmessage = (event) => {
        const msg: WSMessage = JSON.parse(event.data as string);
        if (msg.type === 'pong') return;
        if (msg.channel) this.handlers.get(msg.channel)?.forEach(h => h(msg));
        this.handlers.get('*')?.forEach(h => h(msg));
      };
    });
  }

  send(message: WSMessage) {
    if (this.isConnected && this.ws?.readyState === WebSocket.OPEN) {
      this.ws.send(JSON.stringify(message));
    } else {
      this.messageQueue.push(message);
    }
  }

  subscribe(channel: string, handler: MessageHandler): () => void {
    if (!this.handlers.has(channel)) this.handlers.set(channel, new Set());
    this.handlers.get(channel)!.add(handler);
    this.send({ type: 'subscribe', channel });
    return () => {
      this.handlers.get(channel)?.delete(handler);
      if (this.handlers.get(channel)?.size === 0) {
        this.send({ type: 'unsubscribe', channel });
        this.handlers.delete(channel);
      }
    };
  }

  disconnect() {
    this.stopPing();
    this.maxReconnectAttempts = 0 as never;
    this.ws?.close(1000, 'Client disconnect');
  }

  private startPing() {
    this.pingInterval = setInterval(() => this.send({ type: 'ping' }), 25000);
  }

  private stopPing() {
    if (this.pingInterval) { clearInterval(this.pingInterval); this.pingInterval = null; }
  }

  private handleReconnect() {
    if (this.reconnectAttempts >= this.maxReconnectAttempts) return;
    const delay = this.reconnectDelay * Math.pow(2, this.reconnectAttempts) + Math.random() * 1000;
    this.reconnectAttempts++;
    setTimeout(() => this.connect().catch(console.error), delay);
  }

  private flushQueue() {
    while (this.messageQueue.length > 0) {
      const msg = this.messageQueue.shift();
      if (msg) this.send(msg);
    }
  }
}

export { WebSocketClient, WSMessage, MessageHandler };
```

### `templates/_smoke-test.json`

```json
{
  "envelope": {
    "fields": [
      "v",
      "type",
      "id",
      "ts",
      "payload"
    ]
  },
  "heartbeat": {
    "interval_seconds": 30,
    "timeout_seconds": 90
  },
  "reconnect_policy": {
    "base_ms": 1000,
    "max_ms": 60000,
    "jitter": "full"
  },
  "send_queue": {
    "max_size": 1000,
    "shed_policy": "drop_oldest"
  },
  "auth": {
    "method": "signed_token_query",
    "ttl_seconds": 300
  }
}
```
