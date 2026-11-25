---
name: sse-throttled-progress-manager
description: Stream download / generation progress over Server-Sent Events with per-model throttling and thread-safe updates from background workers.
category: fastapi
version: 1.0.0
version_origin: extracted
tags: [fastapi, sse, progress, asyncio, threading]
source_type: extracted-from-git
source_url: https://github.com/jamiepine/voicebox.git
source_ref: main
source_commit: 476abe07fc2c1587f4b3e3916134018ebacd143d
source_project: voicebox
confidence: high
imported_at: 2026-04-18T00:00:00Z
---

# SSE throttled progress manager

## When to use
A FastAPI service runs long-running jobs on background threads (`asyncio.to_thread`, subprocess, thread pool) and needs to stream progress to potentially-multiple browser clients without flooding them.

## Steps
1. Build a `ProgressManager` holding a `dict[job_id, progress_dict]`, a `dict[job_id, list[asyncio.Queue]]` of subscribers, plus a `threading.Lock` for the shared state. Remember the main event loop at startup (`loop = asyncio.get_running_loop()`).
2. Progress producers call `update_progress(job_id, current, total, ...)`. Compute `pct = min(100, max(0, current/total*100))` — clamp hard because aggregate byte counts can temporarily go over during batch updates.
3. Throttle notifications per job. Remember `last_notify_time[job]` and `last_notify_progress[job]`. Skip the SSE push unless (status is terminal) OR (time since last push ≥ 0.5 s) OR (progress delta ≥ 1 pct). Internal state always updates; only the fan-out is throttled.
4. Thread-safe fan-out. Inside `_notify_listeners_threadsafe`, try `asyncio.get_running_loop()` — if it works you're on the event loop and can call `queue.put_nowait` directly. If it raises RuntimeError you're on a worker thread; use `main_loop.call_soon_threadsafe` with a closure that puts on the queue.
5. Bound each listener queue (`maxsize=10`) and gracefully drop updates on `QueueFull` — a slow client should not back-pressure the producer.
6. The SSE endpoint subscribes, emits initial state (only if status is `downloading`/`extracting` — don't replay a stale `complete`), streams updates with `yield f"data: {json.dumps(...)}\n\n"`, and sends `": heartbeat\n\n"` on a 1 s timeout so reverse proxies don't drop the connection. Close on `complete` / `error` / `CancelledError`.

## Counter / Caveats
- Always record the main event loop at startup. Background threads can't find it with `get_running_loop()`; you need the stored reference for `call_soon_threadsafe`.
- Never call `await queue.put(...)` from the producer path — a slow subscriber becomes a global slowdown. Drop on `QueueFull` and let the client reconnect.
- The initial-state guard (only replay "in progress" statuses) matters: without it, a reconnect after the job finished replays an old `complete` and confuses the UI.
- Heartbeats also make fetch-based SSE clients time out less often on corporate proxies.

Source references: `backend/utils/progress.py` (the `ProgressManager` class).
