---
name: sse-event-buffer-reconnect
description: Buffer SSE events per conversation with a TTL that resets on every new event and a max-per-conversation cap, so reconnects during EventSource auto-retry replay cleanly without losing `tool_result` chunks.
category: api
version: 1.0.0
version_origin: extracted
tags: [sse, server-sent-events, reconnect, buffer, streaming, react]
confidence: high
source_type: extracted-from-git
source_url: https://github.com/coleam00/Archon.git
source_ref: dev
source_commit: d89bc767d291f52687beea91c9fcf155459be0d9
source_project: Archon
imported_at: 2026-04-18T00:00:00Z
---

# SSE Event Buffer with TTL-Reset + Reconnect Grace

## When to use

- Your backend pushes SSE events to a browser whose `EventSource` may auto-reconnect (laptop sleep, VPN flap, mobile network, React StrictMode double-mounts).
- Events arriving **during the reconnect window** must be replayed, not dropped. In practice, dropping a `tool_result` event leaves the UI showing a spinning tool card forever.
- You want bounded memory: one runaway loop producing 10 000 events/s should not OOM the server.

## Steps

1. **Separate two concerns**: (a) stream registry (active `conversationId → SSEWriter`) and (b) event buffer (`conversationId → BufferedEvent[]` for events emitted while no stream is attached).

2. **Pick three constants** with a fail-fast invariant at module load:

   ```ts
   const RECONNECT_GRACE_MS = 5_000;       // cleanup delay after stream removal
   const EVENT_BUFFER_TTL_MS = 60_000;     // how long to hold unconnected events
   const EVENT_BUFFER_MAX = 500;           // per-conversation cap
   if (EVENT_BUFFER_TTL_MS < RECONNECT_GRACE_MS) throw new Error(...);
   ```

   The invariant `TTL_MS >= GRACE_MS` is load-bearing — otherwise events emitted during a reconnect can expire before the client has had a chance to return.

3. **On `emit(conversationId, event)`:**
   - If an active stream exists and isn't closed, write the event. On write failure, delete the stream reference and close it (the browser's EventSource will auto-reconnect).
   - If no active stream, **buffer** the event with `Date.now()` timestamp.

4. **On `registerStream(conversationId, newStream)`:**
   - If an existing stream is attached, close it (new tab / reload replaces old).
   - Cancel any pending cleanup timer (the client came back).
   - Replay buffered events: filter out any whose age > TTL, replay the valid ones via `stream.writeSSE`, then clear the buffer. Log `transport.buffer_ttl_expired` with count if any were dropped — that's the "stuck tool card" alarm.

5. **On `removeStream(conversationId, expectedStream?)`:** if the caller passes `expectedStream`, only remove it if it **matches the currently registered stream**. This prevents a race where a stale `onAbort` callback from a replaced stream removes a newer stream. Critical in React StrictMode. Then schedule `onCleanup` after `RECONNECT_GRACE_MS` so a fast reconnect cancels it.

6. **Cap the per-conversation buffer** at `EVENT_BUFFER_MAX` by shift-dropping the oldest when exceeded. Log a **throttled** warning (`transport.buffer_evicted_oldest`, max once per 5 s per conversation) so runaway producers don't flood logs.

7. **Auto-clear the buffer** after `TTL_MS + 500ms` via a `setTimeout` that resets on every new event (held for TTL past the *most recent* event, not the first). This prevents buffers leaking for conversations whose client never reconnects.

8. **Run a zombie-reaper** every 5 minutes: iterate `streams`, remove any whose underlying writer is already `closed`. Covers cases where the transport layer silently half-closed.

9. **On `stop()`**, close every active stream, clear all Maps, clear all timers.

## Counter / Caveats

- **Don't compress** the buffer (e.g. keep only last N message-chunks) — partial messages break the UI. Use size-bounded cap + TTL, not content-aware trimming.
- **60 s TTL** is a defense against mobile / VPN reconnects. If you run in a LAN-only environment, you can drop it to 15-20 s. Never below `RECONNECT_GRACE_MS`.
- The React StrictMode double-mount race (step 5) is specifically why `removeStream` takes an `expectedStream`. Without it, rapid connect→disconnect→reconnect cycles lose the new stream's registration.
- If your SSE transport doesn't support `id:` / `Last-Event-ID` properly, this buffer is the only mechanism you have for recovery. Consider adding `Last-Event-ID` handling as a separate concern — the buffer pattern stands on its own.

## Evidence

- `packages/server/src/adapters/web/transport.ts` (303 lines): full implementation.
  - Constants + invariant at lines 17-45.
  - `registerStream` + buffered replay at lines 70-112 with the "stuck tool cards" comment explaining TTL expiration risk (lines 95-97).
  - `removeStream` with `expectedStream` race-guard comment at lines 114-127.
  - Eviction warning throttle at lines 240-251.
  - Zombie reaper at lines 134-142 (5-minute interval).
  - Auto-cleanup timer reset at lines 253-261.
- Commit SHA: d89bc767d291f52687beea91c9fcf155459be0d9.
