---
name: android-bug-hunting-anr-trace-analyzer
description: >
  Analyze an Android ANR (Application Not Responding) trace and identify what is blocking
  the main thread. Reads the "main" thread stack to determine the cause class — I/O blocking
  (disk/network), lock contention with another thread, deadlock, infinite loop, JNI block,
  Binder transaction stuck, IPC waiting on system_server — and points to the suspect frame.
  Also detects classic ANR patterns: SharedPreferences.commit on main, synchronous Room
  on main, MessageQueue starved, foreground service not called in time, slow startup
  initialization. Use this skill whenever the user pastes an ANR trace, shares an
  /data/anr/traces.txt excerpt, asks "why is my app frozen", "what's blocking the main
  thread", "ANR analysis", or includes a multi-thread Java stack dump (with "main" thread
  prominent). Trigger even on partial ANR traces.
---

# ANR Trace Analyzer

## Purpose

ANRs differ from crashes: there is no exception, no `Caused by`, no obvious failure point.
The trace is a snapshot of every thread, and the analyst's job is to read the *main*
thread to figure out why it isn't progressing, then read other threads to find who's
holding the resource it's waiting on.

**Output format.** A focused analysis report (described below). One trace, one analysis.

---

## Step 1 — Identify the trace

A typical ANR trace from `logcat` or `/data/anr/traces.txt` looks like:

```
----- pid 12345 at 2024-01-01 12:00:00 -----
Cmd line: com.example.app
Build fingerprint: 'google/...'
ABI: 'arm64'
Build type: optimized

"main" prio=5 tid=1 Native
  | group="main" sCount=1 dsCount=0 flags=1 obj=0x...
  | sysTid=12345 nice=-10 cgrp=top-app sched=0/0 handle=0x...
  | state=S schedstat=( ... ) utm=... stm=... core=...
  | stack=0x... stackSize=...
  | held mutexes=
  native: #00 pc 0000000000056ddc  /apex/com.android.runtime/lib64/bionic/libc.so (read+8)
  native: #01 pc ...
  at java.io.FileInputStream.read(FileInputStream.java:...)
  at android.app.SharedPreferencesImpl.loadFromDisk(SharedPreferencesImpl.java:...)
  - locked <0x...> (a android.app.SharedPreferencesImpl)
  at com.example.app.MainActivity.onResume(MainActivity.kt:42)
  ...

"DefaultDispatcher-worker-1" daemon prio=5 tid=15 Waiting
  | group="main" ...
  at jdk.internal.misc.Unsafe.park(Native method)
  - parking to wait for <0x...> (a kotlinx.coroutines.JobImpl)
  ...
```

Key elements per thread:
- **Thread name** — `main` is the one to read first.
- **State** — `Native`, `Sleeping`, `Waiting`, `Runnable`, `Blocked`, `Suspended`, `TimedWaiting`.
- **Stack** — what the thread is doing.
- **`held mutexes`** — locks this thread holds.
- **`- locked <0x...>`** / **`- waiting on <0x...>`** / **`- parking to wait for <0x...>`** — synchronization edges.

---

## Step 2 — Read the main thread

The main thread's state and top frames classify the cause.

### Cause class A — Blocked on I/O

**Signals.**
- State: `Native` or `Sleeping`.
- Stack contains `FileInputStream.read`, `FileOutputStream.write`, `Os.read`,
  `Posix.read`, `socket.read`, `connect`, `Socket.connect`.
- App frame above the I/O call sits in `onResume`, `onCreate`, `onClick`, etc.

**Hypothesis.** Synchronous I/O on the main thread.

**Specific patterns:**

- **A1 — `SharedPreferencesImpl.loadFromDisk` / `awaitLoadedLocked`.** The first
  `getXxx` call after `getSharedPreferences` blocks while the prefs file is read.
  Hot on cold start.
- **A2 — `Room`/`SQLiteDatabase.executeSql` / `acquireReference`.** Synchronous
  database call. Either `allowMainThreadQueries` is on or a non-suspend DAO is being
  called from Main.
- **A3 — Network `connect` / `read`.** Retrofit `.execute()`, `OkHttpClient` sync,
  raw `HttpURLConnection`. ANR on slow network.
- **A4 — `Bitmap`/`AssetManager` decode.** Large image decode on Main.
- **A5 — `dlopen` / native library load.** `System.loadLibrary` from `onCreate` of a
  large native library.

---

### Cause class B — Blocked on a lock held by another thread

**Signals.**
- State: `Blocked`.
- Stack has `- waiting to lock <0x…>`.
- Another thread in the dump has `- locked <0x…>` for the same address.

**Hypothesis.** Lock contention. Find the holder thread; that's the *real* culprit.

**Method.**

1. Note the address from the main thread's `waiting to lock`.
2. `grep` (or scan) the trace for that address with `locked` — the other thread
   holding it.
3. Read that thread's stack: it's doing the work that is, transitively, blocking Main.

**Common patterns:**
- **B1 — `synchronized` on a singleton's monitor** — `getInstance` or initialization
  contention.
- **B2 — Database write transaction** held by a worker thread; Main blocks on a read
  that needs the same lock.
- **B3 — `WorkManager` internal locks** during enqueue at startup.

---

### Cause class C — Deadlock

**Signals.** Two threads, each waiting for a lock held by the other. The lock graph
forms a cycle.

**Method.**

1. From Main's `waiting to lock <X>`, find the holder of X (say, thread T2).
2. T2 has `waiting to lock <Y>`.
3. Find the holder of Y. If it's Main (or a thread that ultimately points back to
   Main), it's a deadlock.

**Severity.** Always Critical.

**Recommended fix.** Lock ordering, or eliminate one of the locks (often by reducing
shared state).

---

### Cause class D — Waiting on a lifecycle/IPC condition

**Signals.**
- State: `Waiting` or `TimedWaiting`.
- Stack has `Object.wait`, `Unsafe.park`, or `LockSupport.parkNanos`.
- A `parking to wait for <0x…>` line points to a Job, Future, or Condition.

**Hypothesis.** Main thread is blocked waiting for another thread's result. Common
sub-cases:

- **D1 — `Future.get()`** — synchronous wait on a background task.
- **D2 — `runBlocking`** — explicit block bridging to suspend code.
- **D3 — `CountDownLatch.await`** — explicit synchronization.
- **D4 — Binder transaction** — `BinderProxy.transact` waiting for `system_server`
  or another app's process. If `system_server` is busy or the called provider is
  slow, Main stalls.

---

### Cause class E — JNI / native blocking

**Signals.**
- Top of the stack is `native:` frames in a non-bionic library (the app's own .so or
  a third-party library).
- State: `Runnable` or `Native`.

**Hypothesis.** Native code on Main blocking — e.g. video frame processing, crypto,
heavy serialization done in C++.

**Recommended fix.** Move native call sites off Main.

---

### Cause class F — Infinite or runaway loop

**Signals.**
- State: `Runnable`.
- Stack frames in app code, no I/O or wait.
- The same trace captured a moment later (if the user has multiple) shows the same
  thread still in app code, just at a different line.

**Hypothesis.** Tight loop on Main. Common causes:
- Compose recomposition loop (state mutated during composition).
- Layout thrash (calling `requestLayout` from a layout pass).
- Misused `Choreographer.postFrameCallback` ping-ponging.

**Recommended fix.** Identify the loop boundary and break it.

---

### Cause class G — MessageQueue starvation

**Signals.**
- Main is `Runnable` in `MessageQueue.next` or `Looper.loopOnce`.
- One specific message is taking too long to process — a downstream Handler dispatch
  with heavy work.

**Hypothesis.** A previous message handler did too much work; the next event (input,
draw) starves and the system raises ANR.

**Method.** Check the most recent app frames *below* the Looper frames.

---

### Cause class H — Foreground service not started in time

**Signals.** ANR reason is `Context.startForegroundService() did not then call Service.startForeground()`.

**Hypothesis.** A Service started via `startForegroundService` did not call
`startForeground` within the OS timeout (~5s).

**Recommended fix.** Hoist `startForeground` to the very top of `onStartCommand` /
`onCreate`. Defer all other init.

---

## Step 3 — Cross-reference with other threads

Once a cause class is identified, scan all other threads to:

1. **Find the holder** of any lock Main is waiting on.
2. **Find the contention partner** (which thread is doing the I/O / lock-holding work).
3. **Note unusual patterns.** Many app threads in `Sleeping` is normal; many in `Runnable`
   suggests CPU thrash. Many threads named the same ("OkHttp Dispatcher", "pool-N-thread-M")
   in unusual numbers may indicate thread leaks.

---

## Step 4 — Produce the analysis

Format:

```markdown
## ANR Analysis

### Trace summary
- **Process:** {package}
- **Reason:** {ANR reason from the report header, if present}
- **Main thread state:** {Native/Sleeping/Waiting/Runnable/Blocked/…}
- **Top app frame on main:** `{file:line}` — `{Class.method}`

### Cause class
**{A/B/C/D/E/F/G/H — name}** — confidence {High/Medium/Low}.

### Hypothesis
{1–3 sentences in the codebase's own terms. E.g.: "Main thread is blocked in
`SharedPreferencesImpl.loadFromDisk` while reading the prefs file. This is the first
read of `user_prefs` and the file is 200KB+, so the cold-cache load on a slow device
exceeds the ANR threshold."}

### Contention map (if applicable)
- Main thread `waiting to lock <0xABC>` at frame `{file:line}`.
- Lock `<0xABC>` held by thread `"{name}"` at frame `{file:line}`.
- That thread is doing: {summary — I/O, computation, waiting on something else}.

### Where to look in source
- `{file:line}` — {what to inspect}
- `{file:line}` — {what to verify}

### Suggested fix
{Concrete remediation. E.g.: "Move the first prefs read off Main: in
`Application.onCreate`, launch a coroutine on `Dispatchers.IO` that reads the prefs
file once. Or migrate to DataStore."}

### What would invalidate this hypothesis
{Conditions: "If the trace is from a debuggable build with the debugger attached,
the trace can be misleading"; "If `traces.txt` was captured after the ANR resolved,
the snapshot may show a different state".}
```

---

## Notes

- Always read the *main* thread first, then crawl the lock graph from there.
- Modern Android (12+) writes ANRs to `/data/anr/anr_*` as separate files; older
  Android writes to `/data/anr/traces.txt`. The format inside is essentially the same.
- Crashlytics ANR reports include a "main thread" stack but truncate other threads —
  a contention-class diagnosis may not be possible without the full `traces.txt`. Note
  this in the analysis.
- Some ANRs are environmental (e.g. low memory causing the system to swap). Look for
  hints in the dump header (memory stats, GC info). Note these as confounding factors.
- The Android Vitals dashboard (Play Console) groups ANRs by signature; multiple ANRs
  with the same top-frame are the same root cause.
