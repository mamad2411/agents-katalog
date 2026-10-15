---
name: reactor-sdk
description: Build real-time video AI applications with Reactor SDKs. Use when code imports `@reactor-team/js-sdk` or `reactor-sdk`; when connecting a web/mobile frontend to a GPU-powered Reactor model (Helios and others); when streaming video via WebRTC with command-based control; when publishing webcam input for video-to-video transformations; when handling JWT authentication for Reactor; or when debugging Reactor connection lifecycle (disconnected → connecting → waiting → ready). SKIP when project uses unrelated WebRTC (e.g., plain video calling), or video pipelines that don't touch Reactor.
---

# Reactor SDK

Reactor streams real-time video from GPU-hosted AI models to web and mobile frontends over WebRTC. Clients authenticate with JWTs, connect to a named model, send commands to control generation, and receive video tracks (JS/React) or NumPy frames (Python).

**SDKs:**
- JavaScript / TypeScript: `@reactor-team/js-sdk` (npm / pnpm)
- Python: `reactor-sdk` (pip)

**API key format:** `rk_...` — never commit or expose in client bundles.

## Pick the right reference

Load only the reference(s) matching the task. Each is self-contained.

| Task | Read |
|---|---|
| Vanilla JS / TS app, non-React framework | [references/javascript.md](references/javascript.md) |
| React app (hooks, `ReactorProvider`, `ReactorView`, `WebcamStream`) | [references/react.md](references/react.md) |
| Python script, server, data pipeline, frame processing | [references/python.md](references/python.md) |
| JWT fetching, dev vs. production auth, env vars | [references/authentication.md](references/authentication.md) |
| Model-specific command schemas (Helios, etc.) | [references/models.md](references/models.md) |

For tasks that span SDKs (e.g., a React frontend talking to a Python backend), read both references.

## Connection lifecycle

Every SDK exposes the same four-state lifecycle:

```
disconnected → connecting → waiting → ready
```

| State | Meaning | Can send commands? |
|---|---|---|
| `disconnected` | No active connection | No |
| `connecting` | Establishing coordinator connection | No |
| `waiting` | Queued for GPU assignment | No |
| `ready` | GPU assigned, session live | **Yes** |

**Always wait for `ready` before sending commands or publishing tracks.** Commands sent earlier fail silently or throw. Register event listeners *before* calling `connect()` so you don't miss the `ready` transition.

## Core workflow (SDK-agnostic)

1. Create an API key (`rk_...`) in the [Reactor Dashboard](https://reactor.inc/dashboard).
2. **JS**: mint a JWT server-side by POSTing to `https://api.reactor.inc/tokens` with the `Reactor-API-Key` header; ship only the JWT to the browser. **Python**: pass the API key directly to the `Reactor` constructor.
3. Create a Reactor instance with `modelName`. Tracks are advertised by the server — the client does not declare `send` / `receive`.
4. Register event/status listeners.
5. `connect()`.
6. On `ready`, send commands and/or publish tracks (names match the model's input attributes).
7. On teardown, `disconnect()` and stop any local media tracks.

SDK-specific API calls for each step are in the per-SDK references.

## Critical gotchas

These bite every integration. Keep them in mind regardless of SDK.

- **Never expose a raw API key in browser code.** Mint JWTs server-side via `POST https://api.reactor.inc/tokens` and ship only the JWT. There is no `fetchInsecureJwtToken` in the current SDK. See [references/authentication.md](references/authentication.md).
- **Track names are contracts.** The string passed to `publishTrack()` / `publish_track()` must match the server-side model's input attribute name. Mismatches fail silently — no error, no frames.
- **JWTs expire after 6 hours.** Long-lived sessions need refresh + reconnect logic.
- **Media cleanup is mandatory.** Forgetting `unpublishTrack()` + `stream.getTracks().forEach(t => t.stop())` leaks cameras and memory across route changes / unmounts.
- **Reconnects don't preserve session state by default.** For brief network blips, call `disconnect(recoverable=True)` (Python) / `disconnect(true)` (JS) and then `reconnect()`; otherwise expect a fresh session.
- **Python `@on_frame` is synchronous.** Slow handlers block frame delivery — offload to a queue or `asyncio.create_task()`.
- **Commands are model-specific.** Command names and argument shapes differ per model. Check [references/models.md](references/models.md) or the model's own docs before guessing.
- **React store renames two methods.** Hooks expose `publish` / `unpublish` (not `publishTrack` / `unpublishTrack`). The underlying `Reactor` class keeps the longer names.
- **Cross-SDK naming drifts between JS and Python.** Status values are lowercase strings in JS (`"ready"`) and enum members in Python (`ReactorStatus.READY`). Error fields are camelCase in JS (`retryAfter`, `lastError`) and snake_case in Python (`retry_after`). When porting code between SDKs, convert both.

## Verification checklist

Before shipping Reactor integration code:

- [ ] API key lives in env vars or a secret manager, never in source
- [ ] Browser code fetches the JWT from your server, not from a client-exposed key
- [ ] Listeners (`statusChanged` / `on_status` / `@on_frame`) are registered *before* `connect()`
- [ ] All command sends are gated on `status === "ready"` / `ReactorStatus.READY`
- [ ] Teardown path calls `disconnect()` and stops every local media track
- [ ] Error handling dispatches on `error.recoverable` / `retryAfter` (not specific code strings)
- [ ] Track names passed to `publishTrack()` / `publish_track()` match the model's input attribute
- [ ] Python frame handlers are non-blocking
- [ ] Full lifecycle exercised once end-to-end: connect → ready → command → disconnect

## Official docs

- Navigation index: https://docs.reactor.inc/llms.txt
- Auth guide: https://docs.reactor.inc/authentication
- JS SDK guide: https://docs.reactor.inc/javascript-guide
- Python SDK guide: https://docs.reactor.inc/python-guide

When in doubt, fetch the current model or SDK page — API surfaces drift and this skill may be stale. Verify method names and argument shapes against the live docs before writing non-trivial code.
