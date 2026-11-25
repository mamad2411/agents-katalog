---
name: anr-deadlock-detective
description: Investigate Android ANRs (Application Not Responding) and main-thread deadlocks from traces, logs, and Perfetto/systrace data. Covers main-thread blocks, binder transactions, lock contention, Choreographer skips, and coroutine-induced ANRs. Use whenever the user mentions ANR, "not responding" dialogs, "the app hangs", "input dispatching timed out", `anr/traces.txt`, Crashlytics ANR reports, or asks why a screen freezes. Also use when the dev has a stack trace from `adb bugreport` and needs help reading it.
---

# ANR & Deadlock Detective

ANRs happen when the main thread can't process an input event within ~5 seconds (or a broadcast within 10–20s). The fix is rarely "make it faster" — it's "figure out what's blocking, then move it off the main thread or remove the wait." This skill is a structured read of the evidence.

## When to use

Triggers: "ANR", "input dispatching timed out", "main thread blocked", "the app hangs", "deadlock", "Choreographer skipped frames", attached `traces.txt` or `anr` log.

For "this screen feels slow" without a real hang, use `compose-recomposition-optimizer` or `startup-jank-profiler` instead.

## Process

### Phase 1: Get the right artifact

The most useful evidence, in order of preference:

1. **ANR trace** from `/data/anr/traces.txt` or pulled via `adb bugreport`. Contains the main thread stack at the moment of the ANR.
2. **Perfetto / systrace** capture during the hang. Shows what other threads were doing and where binder calls went.
3. **Crashlytics / Sentry ANR report** — has the main thread stack but usually not other threads.
4. Reproduction steps + a screen recording, as a fallback.

Ask the dev which they have. If only a description, push them to capture a trace before guessing.

### Phase 2: Read the main thread stack

Find the `"main"` thread in the trace. Look at the top frames. Pattern-match:

| Top of stack | Likely cause |
|---|---|
| `Object.wait`, `LockSupport.park` | Waiting on a lock or future — find what's holding it. |
| `nativePollOnce` | Main thread idle. The ANR is elsewhere; trace a recent binder call or look at input dispatcher. |
| `Binder.transact` | Blocking IPC. Check which system service — `AccountManager`, `ContentResolver`, custom AIDL. |
| `SharedPreferencesImpl$EditorImpl.commit` | `commit()` on main thread. Switch to `apply()`. |
| Database query (`SQLiteSession`) | Disk I/O on main. Move off (Room with suspend, or coroutine on `Dispatchers.IO`). |
| `BitmapFactory.decode*` | Image decode on main. Use an image loader (Coil/Glide) or move to background. |
| `runBlocking` | Coroutine being awaited synchronously on main. Almost always wrong. |
| Network (`Socket`, `OkHttp`) | Network on main. Should never happen — `StrictMode` should have caught it. |
| Compose / Choreographer frame | UI work too slow. Use the recomposition optimizer. |

### Phase 3: Trace the blocker

If the main thread is waiting on a lock or future, find who holds it.

- Look at other thread stacks for the same monitor/lock address.
- For coroutines: a `runBlocking` waiting on a job that's suspended on `Dispatchers.Main` is a classic deadlock — the job can't resume because the main thread is blocked waiting for it.
- For binder: identify the target process (`ActivityManager`, `WindowManager`, your own service). A slow system binder call usually means device pressure or the service itself is stuck.

### Phase 4: Categorize and fix

Group the root cause into one of these and apply the matching fix:

**Main-thread I/O**
- Disk reads, `SharedPreferences.commit`, eager database queries in `onCreate`. Move to background — `lifecycleScope.launch(Dispatchers.IO)`, Room suspend queries, or DataStore.

**Coroutine deadlock**
- `runBlocking` on main waiting for a `Dispatchers.Main` coroutine. Refactor the caller to be suspend-aware, or restructure so the awaited work uses `Dispatchers.Default`/`IO`.
- A `Mutex` held across a suspension point that re-enters. Restructure.

**Slow binder call**
- `getContentResolver().query()` against a slow provider. Move to background.
- IPC to your own service that's doing work synchronously. Make it async (`oneway` AIDL or a callback).

**Lock contention**
- Many threads contending on a single `synchronized` block. Reduce critical section size or replace with concurrent data structures (`ConcurrentHashMap`, `AtomicReference`).

**Frame-time overflow**
- The main thread is busy with legitimate UI work that's just too slow. Hand off to `compose-recomposition-optimizer` or RecyclerView optimization.

### Phase 5: Verify the fix

- Reproduce the hang on the same device class (cheap devices reveal more).
- Run with `StrictMode` enabled in debug to catch new violations.
- Add a Macrobenchmark that exercises the scenario and asserts no frames over 16ms.
- For ANRs that came from Crashlytics, watch the dashboard for a week — confirm the rate drops.

## Output

A short writeup with:

1. **What the trace shows** — one sentence on where the main thread was stuck.
2. **Root cause** — the category from Phase 4.
3. **Fix** — specific code change.
4. **Verification** — how to confirm it's gone.

## Common pitfalls

- **Assuming `nativePollOnce` is the problem.** It means the main thread is idle. The ANR cause is elsewhere — check input dispatcher, binder calls from other threads, or system pressure.
- **Adding `withContext(Dispatchers.IO)` around every call.** Doesn't fix structural issues like `runBlocking` deadlocks.
- **Reading only the main thread stack.** For deadlocks, the holder is on another thread — you need the full trace.
- **`Thread.sleep` "to test".** Catches nothing real; production hangs are always caused by waits on real work.
