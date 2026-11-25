---
name: websocket-security
description: Test WebSocket channels for CSWSH, smuggling, injection, and auth flaws (wsrepl, ws-harness, Burp). Use when an app uses real-time channels, chat, notifications, or WS-backed APIs.
---

# WebSocket Security

Offensive testing of WebSocket and Socket.IO endpoints. Apply only on **authorized** targets; treat tokens and message content as sensitive. WebSocket auth/authz usually mirrors the same backend's REST models — align your session and resource-boundary assumptions with how the HTTP API behaves. (To *build* secure real-time systems rather than attack them, see the sibling `websocket-patterns` skill.)

## Quick Start — Spot the Channel

In a proxy or raw traffic review, filter for `101` and `Upgrade: websocket`:

```http
GET /ws HTTP/1.1
Upgrade: websocket
Connection: Upgrade
Sec-WebSocket-Key: dGhlIHNhbXBsZSBub25jZQ==
Sec-WebSocket-Version: 13
```
```http
HTTP/1.1 101 Switching Protocols
Sec-WebSocket-Accept: s3pPLMBiTxaQ9kYGzzhZRbK+xOo=
```

## Testing Decision Tree

1. **Identify endpoint** — from JS bundles, Swagger, or `101` responses; note `wss` vs `ws`.
2. **Handshake review** — are `Origin`, `Host`, and `Cookie` policies correct? Any token in the query string?
3. **Session binding** — reconnect with another user's cookie jar; compare subscription topics and data leakage.
4. **CSWSH** — load a local page that connects with the victim session active; verify the server rejects a wrong `Origin` or uses a non-cookie secret.
5. **Message semantics** — fuzz JSON/text/binary payloads for injection; mirror the same logic as HTTP API testing.
6. **Transport** — flag `ws://` in production; verify TLS and HSTS alignment.

## References

Each file is loaded on demand — read one only when the task needs that depth (progressive disclosure).

- `references/handshake-cswsh.md` — handshake protocol details and the full CSWSH playbook (condition, PoC, step-by-step exploitation, cookie/SameSite behavior) · read when reviewing the upgrade or testing cross-site hijacking.
- `references/vuln-classes.md` — the common-flaw table, message injection (MITM, app-level, stored XSS), Socket.IO-specifics (namespace/event/ack/polling-CSRF), and binary-payload manipulation · read when fuzzing messages or auditing Socket.IO.
- `references/smuggling.md` — WebSocket smuggling: proxy-bypass and H2-over-WS tunneling, with per-proxy behavior · read when a reverse proxy sits in front of the endpoint.
- `references/tooling.md` — wsrepl, ws-harness (HTTP bridge), Burp (SocketSleuth, Turbo Intruder), and binary frame analysis tools · read when setting up the testing toolchain.
