---
name: desktop-ipc
description: Desktop IPC specialist. Owns protocol design between main/renderer/workers, message schemas, request/response patterns, security boundaries, and performance. Auto-invoked when designing or changing inter-process messages.
---

# Desktop IPC

IPC is the app's security boundary: the renderer runs web content, the main
process holds OS capabilities, and every channel between them is a potential
privilege-escalation path. Typed, allowlisted, validated — or it's an RCE vector.

## When to reach for this

- Adding or changing channels between main, renderer, and worker processes
- Reviewing the preload/`contextBridge` surface a renderer can reach
- Moving large payloads (streaming, backpressure, cancellation) across processes
- Investigating a suspected renderer-to-main privilege escalation

## Principles

1. **Typed channels only.** Every channel has a named contract in a schema module
   both processes import; no stringly-typed dispatch. Validate at runtime on the
   receiving side — compile-time types don't survive a compromised sender.
2. **The renderer is hostile.** Treat it as compromised. Electron baseline:
   `contextIsolation: true` (default since Electron 12), `sandbox: true` (default
   since Electron 20), `nodeIntegration: false`. Anything weaker is an ADR.
3. **Least privilege, verbs not capabilities.** The preload exposes specific
   actions (`exportReport()`), never `ipcRenderer` itself or a generic
   `invoke(channel, ...args)` passthrough — a passthrough deletes the allowlist.
4. **Validate the sender, not just the payload.** With multiple windows or
   webviews, check `event.senderFrame` origin per handler; a payload schema
   can't tell you *who* is calling.
5. **Request/response over fire-and-forget.** `invoke`/`handle` pairs are
   correlatable, cancellable, and debuggable; bare `send` events drop errors on
   the floor.
6. **Measure serialization cost.** Structured clone copies the payload; anything
   beyond a few MB goes over a `MessagePort`, stream, or file handle — not a
   JSON-blob event on the main channel.

## Channel design checklist

- [ ] Channel named and typed in the shared contract module
- [ ] Receiving side parses payload with a runtime validator (zod or equivalent)
- [ ] Handler checks `senderFrame` against the allowlist for that channel
- [ ] Renderer sends opaque IDs, never file paths or URLs main will act on directly
- [ ] `shell.openExternal` / process spawns gated on an explicit URL/command allowlist
- [ ] Long operations support cancellation and report progress over the same contract
- [ ] Payloads > ~1 MB routed via MessagePort/stream, not the event channel

A worked Electron skeleton (shared zod contract, minimal preload bridge, main
handler with sender validation and opaque-ID path resolution) is in
[`references/typed-channel.md`](references/typed-channel.md).

## Pitfalls

- Preload exposing `ipcRenderer` or a generic channel passthrough — the single most common Electron security bug
- Handlers acting on renderer-supplied file paths (arbitrary read/write via path traversal)
- Trusting an identity field inside the payload instead of `event.senderFrame`
- `shell.openExternal(url)` with an unvalidated renderer-supplied URL
- Fire-and-forget events with no correlation ID, making failures invisible
- One mega-channel multiplexing every message type, defeating per-channel allowlisting

---
*Related: `desktop-shell-integration` (deep-link payloads entering via IPC),
`desktop-autoupdate` (updater-triggered IPC), `security-checklist` (boundary
review) · domain agent: `desktop-architect` (process model the IPC sits on) ·
output/ADR format: `playbook-conventions`*
