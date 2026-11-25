---
name: posthog-analytics-with-opt-out-and-thread-queue
description: Background-thread CLI analytics that respects DO_NOT_TRACK + custom opt-out env, persists an anonymous UUID in ~/.config, queues events with bounded size, and flushes on atexit with a timeout.
category: cli
version: 1.0.0
version_origin: extracted
tags: [analytics, posthog, opt-out, background-thread, cli]
confidence: medium
source_type: extracted-from-git
source_url: https://github.com/Tracer-Cloud/opensre.git
source_ref: main
source_commit: fb5ba0a1b4ef511d16c56a80f1f126b1f581d724
source_project: opensre
source_path: app/analytics/provider.py
imported_at: 2026-04-18T00:00:00Z
---

# CLI Analytics with Opt-Out and Thread Queue

## When to use
You're shipping an open-source CLI and want anonymous telemetry to demonstrate adoption to sponsors, but with strict guarantees: never block CLI execution, respect industry-standard opt-out flags, never collect PII, always be ready for the user to disable it.

## How it works
- Honor both `DO_NOT_TRACK=1` and a custom `<APP>_ANALYTICS_DISABLED=1`.
- Anonymous ID = first-run UUID stored in `~/.config/<app>/anonymous_id`. Falls back to a per-process UUID if writing fails.
- Events queue into a bounded `queue.Queue(maxsize=128)`; full queue silently drops.
- A daemon thread drains the queue with httpx, posting to PostHog with a 2-second timeout.
- `atexit.register(self.shutdown)` ensures pending events flush within 1 second on CLI exit.
- A drained Event is signalled via `threading.Event` so shutdown can wait for in-flight sends.
- Base properties (cli_version, python_version, os_family) attached to every event automatically.

## Example
```python
class Analytics:
    def __init__(self):
        self._disabled = _is_opted_out()
        self._anonymous_id = _get_or_create_anonymous_id()
        self._queue: queue.Queue = queue.Queue(maxsize=128)
        self._pending = 0; self._drained = threading.Event(); self._drained.set()
        self._worker = None; self._shutdown = False
        if not self._disabled:
            atexit.register(self.shutdown)

    def capture(self, event, properties=None):
        if self._disabled or self._shutdown: return
        envelope = _Envelope(event=event.value,
                             properties=_BASE_PROPERTIES | (properties or {}))
        self._ensure_worker()
        try:
            with self._pending_lock:
                self._pending += 1; self._drained.clear()
            self._queue.put_nowait(envelope)
        except queue.Full:
            self._mark_done()

    def _worker_loop(self):
        with httpx.Client(timeout=2.0) as client:
            while True:
                item = self._queue.get()
                if item is None: self._queue.task_done(); break
                try: self._send(client, item)
                finally:
                    self._queue.task_done()
                    self._mark_done()
            # drain remainder on shutdown ...

def _is_opted_out():
    return os.getenv("MYAPP_ANALYTICS_DISABLED","0") == "1" or os.getenv("DO_NOT_TRACK","0") == "1"
```

## Gotchas
- Always honor `DO_NOT_TRACK` (consoledoc.org standard) — it's the universal opt-out.
- Bounded queue + dropped overflow keeps the CLI responsive even when the network is slow.
- `atexit` flush MUST have a timeout (1s here) so CLI exit isn't held hostage by a stuck network.
- Disable analytics inside CI runners and pytest by detecting `CI=1`/`PYTEST_CURRENT_TEST` env so adoption metrics aren't polluted.
- Never include hostnames, file contents, or alert payloads in event properties — only OS-level metadata.
