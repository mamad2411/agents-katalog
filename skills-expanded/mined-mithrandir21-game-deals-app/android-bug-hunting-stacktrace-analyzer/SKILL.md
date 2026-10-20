---
name: android-bug-hunting-stacktrace-analyzer
description: >
  Analyze a Java/Kotlin/Android stacktrace or crash report and produce a high-confidence
  hypothesis about the root cause. Identifies the exception type, locates the first frame
  in user/app code (vs. framework/system frames), maps to source if available, recognizes
  common crash patterns (NPE on lateinit, ClassCastException from generics erasure,
  IllegalStateException from Fragment-not-attached, Foreground Service missing,
  ConcurrentModificationException, OutOfMemoryError, ANR-converted-to-stuck-trace, etc.),
  and points to the suspect file:line. Use this skill whenever the user pastes a stacktrace,
  shares a crash log, asks "what does this crash mean", "why is this exception happening",
  "help me debug this stack trace", or includes a "Caused by:" / "FATAL EXCEPTION:" / "at
  com.…" block in their message. Trigger even when only a partial trace is provided.
---

# Stacktrace Analyzer

## Purpose

A stacktrace is dense information; the goal is to extract the actionable parts quickly
and form a hypothesis with high signal-to-noise. This skill encodes the patterns a
senior Android engineer applies when reading a crash.

**Output format.** A focused analysis report (described below), not the shared Bug Report
Format. This skill produces a single hypothesis per trace, not a list of findings.

---

## Step 1 — Identify the trace shape

A typical Android stacktrace has these shapes:

### Shape A — Java/Kotlin exception

```
FATAL EXCEPTION: main
Process: com.example.app, PID: 12345
java.lang.IllegalStateException: Fragment X{abc} not attached to a context.
    at androidx.fragment.app.Fragment.requireContext(Fragment.java:1003)
    at com.example.app.HomeFragment.loadData(HomeFragment.kt:42)
    at com.example.app.HomeFragment$onViewCreated$1.invokeSuspend(HomeFragment.kt:30)
    ...
Caused by: java.lang.NullPointerException: …
    at com.example.app.repo.UserRepo.fetch(UserRepo.kt:55)
    ...
```

### Shape B — Native crash (tombstone)

```
*** *** *** *** *** *** *** *** *** *** *** *** *** *** *** ***
Build fingerprint: 'google/sdk_gphone64_arm64/…'
ABI: 'arm64'
signal 11 (SIGSEGV), code 1 (SEGV_MAPERR), fault addr 0x0
backtrace:
    #00 pc 0000000000056ddc  /apex/com.android.runtime/lib64/bionic/libc.so (memcpy+12)
    #01 pc …  /data/app/.../base.apk!libnative.so (Java_com_example_…)
```

### Shape C — ANR

```
ANR in com.example.app
Reason: Input dispatching timed out
…
"main" prio=5 tid=1 Sleeping
  | …
  at java.lang.Thread.sleep(Native method)
  at com.example.app.MainActivity.onResume(MainActivity.kt:23)
```

(For ANR traces specifically, prefer the `android-bug-hunting-anr-trace-analyzer` skill — it's deeper.)

---

## Step 2 — Extract the key signals

For Shape A:

1. **Exception type.** The first line after `FATAL EXCEPTION:` (or the user-pasted
   header). Examples: `NullPointerException`, `IllegalStateException`,
   `IllegalArgumentException`, `ClassCastException`, `OutOfMemoryError`,
   `RuntimeException`, `SecurityException`, `BadParcelableException`.

2. **Exception message.** Often diagnostic by itself. "Attempt to invoke virtual method
   'X' on a null object reference" tells you the receiver was null.

3. **First app frame.** Walk down the stack and find the first frame in the app's
   package (i.e. not `android.*`, `androidx.*`, `java.*`, `kotlin.*`,
   `kotlinx.coroutines.*`). That's where to start reading source.

4. **Caused by chain.** Walk every `Caused by:` — the *deepest* cause is the root.

5. **Thread name.** `main` means UI thread. `DefaultDispatcher-worker-N` means a
   coroutine on `Dispatchers.Default`. `OkHttp Dispatcher` means an OkHttp callback
   thread. The thread name often disambiguates the cause.

For Shape B:

1. The signal: `SIGSEGV` (memory violation), `SIGABRT` (abort, often from native
   `__assert`), `SIGBUS` (bus error, alignment).
2. The library on the crashing frame.
3. Fault address — `0x0` strongly suggests a null pointer in native code.

---

## Step 3 — Match against the pattern catalogue

Each pattern: signature → likely cause → where to look.

### P1 — `NullPointerException` on `lateinit` property

**Signature.** `kotlin.UninitializedPropertyAccessException: lateinit property X has not
been initialized` OR an NPE with stacktrace pointing to access of a `lateinit var` field.

**Likely cause.** Property accessed before its initialization point. Common in Fragments
where a `lateinit var binding` is read after `onDestroyView`, or in objects whose init
is deferred but not gated.

**Where to look.** The first app frame. Read the field declaration; check every entry
point that doesn't go through the initialization.

---

### P2 — `IllegalStateException: Fragment not attached to a context`

**Signature.** `Fragment X{…} not attached to a context` from `Fragment.requireContext`,
`requireActivity`, `getResources`, etc.

**Likely cause.** Coroutine launched on `lifecycleScope` (rather than
`viewLifecycleOwner.lifecycleScope`) is still running after the fragment detached. Or:
an event handler / callback fired post-detach.

**Where to look.** Search the fragment for `lifecycleScope.launch` (vs.
`viewLifecycleOwner.lifecycleScope.launch`). Also look for callbacks registered on
long-lived objects.

---

### P3 — `IllegalStateException: Can not perform this action after onSaveInstanceState`

**Signature.** That message, often from `FragmentTransaction.commit`.

**Likely cause.** Fragment transaction committed after the host activity has saved its
state (typically post-onPause on older versions).

**Where to look.** The transaction call site. Use `commitAllowingStateLoss()` only as
a last resort; preferably defer the transaction to `STARTED` lifecycle state.

---

### P4 — `RuntimeException: Unable to start activity ComponentInfo{…}: java.lang.NullPointerException`

**Signature.** ComponentInfo wrapping a deeper cause.

**Likely cause.** Crash in `onCreate` of the named activity. The Caused-by chain has
the real cause.

**Where to look.** Skip to the first `Caused by:` and apply the matching pattern.

---

### P5 — `SQLiteException` / Room "Cannot access database on the main thread"

**Signature.** `java.lang.IllegalStateException: Cannot access database on the main
thread since it may potentially lock the UI for a long period of time.`

**Likely cause.** A non-suspend, non-Flow Room DAO method called from Main.

**Where to look.** First app frame's class — find the DAO method invoked. See
`android-bug-hunting-main-thread-violations` D1 for the static-analysis equivalent.

---

### P6 — `ConcurrentModificationException`

**Signature.** That exception name, almost always with `ArrayList$Itr.next` or similar
in the trace.

**Likely cause.** Iterating a collection while another thread (or the same thread inside
the loop) mutates it. Common in coroutines that share a `MutableList` across launches.

**Where to look.** First app frame. Find the iteration site and the mutation site;
they're racing.

---

### P7 — `OutOfMemoryError`

**Signature.** `java.lang.OutOfMemoryError: …` often with "Failed to allocate a NN byte
allocation with M free bytes…"

**Likely cause.** Bitmap loading without subsampling; loading large lists into memory
at once; leaks accumulating across rotations (the heap fills with retained Activities).

**Where to look.** Top frame. If `BitmapFactory.decode*`, the immediate cause is image
size. If the fragment/activity itself, suspect leak.

---

### P8 — `BadParcelableException` / `ParcelFormatException`

**Signature.** Errors involving `Parcel.readException`, `Parcel.unmarshall`,
`BadParcelableException`.

**Likely cause.** A `Parcelable` whose `writeToParcel` doesn't match its
`createFromParcel` (or `@Parcelize` change without a correct migration).
Process-restoration bugs.

**Where to look.** The class named in the message. Diff with previous versions if
this surfaced after a release.

---

### P9 — `SecurityException`

**Signature.** Usually involves a permission name in the message.

**Likely cause.** Missing runtime permission; missing `<uses-permission>` in manifest;
attempting to access a feature the OS now restricts.

**Where to look.** The API on the top frame. Cross-reference with manifest and runtime
permission flow.

---

### P10 — `NetworkOnMainThreadException`

**Signature.** That exception name.

**Likely cause.** Networking on Main. See `android-bug-hunting-main-thread-violations` D4.

---

### P11 — `IllegalArgumentException: View not attached to window manager`

**Signature.** That message from `WindowManagerImpl.removeView` or `ViewRootImpl`.

**Likely cause.** Dismissing a dialog whose host activity is already finishing/destroyed.

**Where to look.** The dismiss call site. Guard with `isFinishing`/`isDestroyed`, or
move dialog management into a `DialogFragment`.

---

### P12 — `ClassCastException` from generics erasure

**Signature.** `java.lang.ClassCastException: java.util.LinkedHashMap cannot be cast to
com.example.MyType` (or similar).

**Likely cause.** Deserializing JSON into `Any` and casting, or generic type erasure
biting at runtime. Often: Gson's `fromJson(json, MyType.class)` with a generic
`MyType<T>` losing T.

**Where to look.** First app frame; inspect the deserialization or the cast.

---

### P13 — `Foreground service did not call startForeground in time`

**Signature.** `Context.startForegroundService() did not then call Service.startForeground()`.

**Likely cause.** Service startup delayed by initialization; coroutine doing setup before
calling `startForeground`.

**Where to look.** The Service's `onStartCommand` / `onCreate`. `startForeground` must
be called within ~5s of `startForegroundService`.

---

### P14 — `WindowManager.BadTokenException`

**Signature.** `Unable to add window — token … is not valid; is your activity running?`

**Likely cause.** Showing a dialog or popup after the activity is destroyed.

**Where to look.** The show call site.

---

### P15 — `RuntimeException: Canvas: trying to use a recycled bitmap`

**Signature.** That message during draw.

**Likely cause.** A bitmap was recycled while still in use by an ImageView/Canvas. Common
when manually calling `Bitmap.recycle()` (rarely needed on modern Android).

**Where to look.** Any explicit `recycle()` call in the touched flow.

---

### P16 — Coroutine swallowed exception (no stacktrace in app frames)

**Signature.** Exception printed with no app frames, or `JobCancellationException` with
no useful trace.

**Likely cause.** `async` whose result was never `await`'d, or a `try/catch` swallowing
`Throwable`. The real exception happened, but its stacktrace was discarded.

**Where to look.** Search the suspected code path for `async { }` without `await`, and
for `catch (e: Throwable)` blocks.

---

### P17 — `RuntimeException: Trying to load a CharSequence value from … but value is …`

(Or any other ResourceTypeException.)

**Likely cause.** Resource ID mismatch — resource of the wrong type passed to a getter.
Often a generated `R.id.foo` vs `R.string.foo` mistake, or a stale build with R conflict.

**Where to look.** The getter call. Clean rebuild often fixes stale R issues.

---

## Step 4 — Produce the analysis

Format:

```markdown
## Stacktrace Analysis

### Exception
- **Type:** {ExceptionType}
- **Message:** "{message}"
- **Thread:** {thread name}
- **Process:** {if known}

### First app frame
`{file:line}` — `{Class.method}`

### Cause chain
1. {primary exception, brief}
2. → caused by: {next cause}
3. → caused by: {root cause}

### Pattern match
**{Pattern ID and short name}** — confidence {High/Medium/Low}.

### Hypothesis
{1–3 sentences explaining what is most likely happening, in the codebase's own terms.}

### Where to look
- `{file:line}` — {what to read for}
- `{file:line}` — {what to verify}

### Suggested fix
{Concrete change. Code example if obvious. Otherwise, the investigation step.}

### What would invalidate this hypothesis
{Conditions under which the analysis would be wrong — e.g. "if the exception is thrown
from a worker thread the user didn't show, the cause is different".}
```

If the user provided source files alongside the trace, open the suspected files at the
referenced lines and verify the hypothesis before presenting it.

---

## Notes

- Many crashes have multiple `Caused by:` levels — always read to the bottom.
- ProGuard/R8 obfuscation produces traces with mangled names (`a.b.c`). If the user
  hasn't deobfuscated, ask for the mapping file or note that without it the analysis
  is approximate.
- For traces from production crash-reporting tools (Crashlytics, Sentry), the format
  varies but the same patterns apply.
- If the trace is truncated or the user pasted only the top, ask for the full text
  before committing to a hypothesis.
- Native crashes (Shape B) often need `addr2line` and the unstripped library to map
  to source. Note this in the analysis if relevant.
