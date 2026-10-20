---
name: debug-lockorder-detection-system
description: Runtime lock-order deadlock detection via a DEBUG_LOCKORDER compile flag that tracks lock acquisition order and reports circular dependencies.
category: debug
version: 1.0.0
tags: [cpp, threading, deadlock, debugging, instrumentation]
source_type: extracted-from-git
source_url: https://github.com/bitcoin/bitcoin
source_ref: refs/remotes/origin/master
source_commit: edcf84c73abcad31346388a4b8712b38742801ce
source_project: bitcoin
version_origin: extracted
confidence: high
---

# Runtime Lock-Order Detection via DEBUG_LOCKORDER

## When to use

Multi-threaded C++ codebases with enough locks that a human reviewer cannot prove a consistent global lock order by inspection.

## Procedure

1. Wrap all lock acquire/release sites in project-defined macros (e.g. `LOCK(cs)` / `LOCK2(a, b)`) so the instrumentation lives in one place.
2. Gate the instrumentation behind a `DEBUG_LOCKORDER` compile flag, enabled in Debug and sanitizer CI builds, off in Release.
3. On each acquire, capture `{this_thread, lock_addr, call_site}` into a per-thread held-lock stack and into a global `(prev, next)` edge set.
4. Whenever a new edge inverts an existing edge, fail loudly (abort in Debug, log in relaxed modes) with both call sites so the user sees the offending pair.
5. Pair with a `DEBUG_LOCKCONTENTION` flag that times lock waits to surface hot contention without changing release perf.

## Notes

- Store the held-lock stack in a `thread_local` container so no shared state is on the hot path.
- Call-site capture via `__FILE__`/`__LINE__` macros is enough; no stack walking required.
- Run the instrumented build under the full functional test suite once per release — most real deadlocks surface in minutes.

## Evidence

- `doc/developer-notes.md` (sections "DEBUG_LOCKORDER" and "DEBUG_LOCKCONTENTION")
- `src/sync.h`
