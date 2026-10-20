---
name: one-websocket-port-for-ws-and-http
description: Run a web UI + WebSocket RPC on the same port by passing an httpHandler to the WsRpcServer — Node's http upgrade event lets one server serve both.
category: architecture
version: 1.0.0
version_origin: extracted
tags: [websocket, http, port-sharing, webui]
confidence: medium
source_type: extracted-from-git
source_url: https://github.com/lukilabs/craft-agents-oss.git
source_ref: main
source_commit: 61f7d48a5b4fd0a8094f002c9e3aea5f3824dcfb
source_project: craft-agents-oss
source_path: packages/server/src/index.ts
imported_at: 2026-04-18T00:00:00Z
---

# One port for both HTTP and WebSocket

## When to use
- Shipping a server that exposes BOTH a REST/HTML web UI and a WebSocket RPC endpoint.
- Firewalls allow one port; you can't ask users to open two.
- Simplifies TLS setup (one cert, one address, one port).

## How it works
1. Create a Node `http.createServer(requestHandler)` (or `https.createServer`).
2. Pass it to `new WebSocketServer({ server: httpServer })`. The WS library hooks the `upgrade` event on the shared HTTP server.
3. HTTP requests: the `requestHandler` handles `/api/auth`, `/api/oauth/callback`, static assets, etc.
4. WebSocket upgrades: the WS library sees `Upgrade: websocket` in the request headers, pulls the socket, runs the handshake.
5. Auth is shared: the HTTP handler sets a JWT cookie on login; the WS upgrade reads the same cookie to authorize the connection (see `jwt-cookie-auth-on-websocket-upgrade`).
6. Expose the HTTP handler via a thin fetch-style abstraction so your WsRpcServer can accept it from outside:
   ```ts
   bootstrapServer({ httpHandler: nodeHttpAdapter(webuiHandler.fetch), ... })
   ```

## Example
```ts
import { createServer } from 'node:http';
import { WebSocketServer } from 'ws';
import { fetch as webuiFetch } from './webui/http-server';

const http = createServer(nodeHttpAdapter(webuiFetch));
const wss = new WebSocketServer({ server: http });

wss.on('connection', (ws, req) => {
  if (!validateSessionCookie(req.headers.cookie)) { ws.close(4001, 'AUTH_FAILED'); return; }
  bindRpcHandlers(ws);
});
http.listen(port, host);
```

## Gotchas
- Under TLS, use `https.createServer({ cert, key })` - the WS library transparently upgrades to `wss://` on the same port.
- If you skip port-sharing and run them on different ports, CORS + cookie SameSite rules will bite you.
- The HTTP handler must NOT try to handle WebSocket upgrade requests - the WS library intercepts them. If your handler tries to read the body, you'll deadlock.
- Remember to set `server.close()` on both when shutting down (the WS library's `close` doesn't stop the HTTP accept loop).
- Expose `CRAFT_WEBUI_WS_URL` so a reverse proxy can override the browser's ws target (e.g. going through nginx on :443 that proxies to :9100 internally).
