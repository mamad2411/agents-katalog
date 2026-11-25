---
name: starlette
description: "Applies when building or reviewing Starlette applications. Covers middleware, lifespan events, streaming, WebSockets, and background tasks."
---

# Starlette

## Middleware and lifespan

1. **Middleware executes outermost-first for requests (onion model).** CORSMiddleware before auth. TrustedHostMiddleware early.
2. **Use lifespan context manager, not deprecated on_startup/on_shutdown.**
3. **Use `Request.state` to pass data between middleware and handlers.**

## Responses

4. **`BackgroundTask` for fire-and-forget after response.** Runs after response completes. For concurrent work, use a task queue.
5. **`StreamingResponse` for large payloads.** Async generator avoids loading everything into memory.
6. **WebSocket handlers must explicitly accept, receive, close.** Handle WebSocketDisconnect. Use try/finally.

## Routing and testing

7. **Register exception handlers on the app for HTTP errors.**
8. **Mount static files with explicit prefix.** Never from application root.
9. **TestClient (httpx) for testing.** `with TestClient(app) as client:` fires lifespan events.
10. **Handle ClientDisconnect in long-running endpoints.** Check `is_disconnected()` periodically.
11. **Never `allow_origins=["*"]` with `allow_credentials=True`.** Forbidden by CORS spec.
12. **Use explicit response types** (PlainTextResponse, HTMLResponse, JSONResponse) for correct Content-Type.
