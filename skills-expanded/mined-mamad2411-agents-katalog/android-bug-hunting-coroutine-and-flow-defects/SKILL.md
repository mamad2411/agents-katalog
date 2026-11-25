---
name: android-bug-hunting-coroutine-and-flow-defects
description: >
  Hunt for runtime defects in Kotlin coroutine and Flow usage in Android/KMP code. Covers
  scope misuse (GlobalScope, runBlocking in production, wrong scope for the work),
  exception swallowing (launch vs async, missing SupervisorJob), lifecycle-aware collection
  (collect in onCreate vs repeatOnLifecycle), Flow vs StateFlow vs SharedFlow misuse
  (one-shot events on StateFlow, replay bugs on rotation, cold/hot confusion), missing
  flowOn, blocking calls inside coroutines, non-cooperative cancellation, and suspend
  function shape mistakes. Use this skill whenever the user asks to find bugs related to
  coroutines, Flow, StateFlow, SharedFlow, suspend functions, viewModelScope, lifecycleScope,
  GlobalScope, or async concurrency in Kotlin — including phrasings like "any concurrency
  bugs", "Flow problems", "coroutine leaks", or "is my StateFlow usage correct". Trigger
  whenever a bug hunt touches Kotlin code that uses coroutines or Flow, even if not asked
  by name.
---

# Coroutine and Flow Defect Hunter

## Purpose

Coroutines are where Android apps quietly bleed correctness. The bugs are subtle, the
patterns are well-cataloged, and almost all of them are detectable from source. This
skill encodes those patterns and hunts for them systematically.

**Output format.** Use the shared Bug Report Format. Read `.claude/skills/android-bug-hunting-dispatcher/references/report-format.md` before writing findings.

---

## Step 1 — Scope the search

Find every file that touches coroutines or Flow:

```bash
grep -rEn "kotlinx\.coroutines|GlobalScope|runBlocking|viewModelScope|lifecycleScope|\
\bFlow<|StateFlow|SharedFlow|MutableStateFlow|MutableSharedFlow|\
\bsuspend fun|\bawait\(|\.collect\b|repeatOnLifecycle|launchIn" \
  --include="*.kt" .
```

Skip generated code (`build/`, `.gradle/`, anything under `generated/`).

---

## Step 2 — Run each detector

Each detector below has: a name, a grep/ripgrep pattern, the rule, and the severity
defaults. Run them in order. For every hit, open the file, confirm the antipattern
in context, and write a finding.

---

### D1 — `GlobalScope` usage in app code

**Pattern.** `GlobalScope.launch` or `GlobalScope.async` anywhere outside `main()` of a
plain JVM tool, tests, or top-level utilities explicitly designed for app-lifetime work.

```bash
grep -rEn "GlobalScope\.(launch|async|produce|actor)" --include="*.kt" .
```

**Why it's a bug.** `GlobalScope` is not tied to any lifecycle. Coroutines launched there
outlive the screen, the user session, sometimes the process foreground state, holding
references to ViewModels, Activities, or repositories. Errors are not propagated to any
parent and crash policies are inconsistent across versions.

**Severity.** High by default. Critical if the launched block touches `Context`/`View`
references.

**Recommended fix.** Replace with the right scoped scope: `viewModelScope`, `lifecycleScope`,
an `Application`-scoped `CoroutineScope(SupervisorJob() + Dispatchers.Main.immediate)` for
truly process-lifetime work, or a Hilt/Koin-injected scope.

---

### D2 — `runBlocking` on the main thread / in production

**Pattern.** `runBlocking { … }` outside of `main()`, `@Test`, `init` of a CLI tool, or
explicit blocking-bridge utilities.

```bash
grep -rEn "runBlocking" --include="*.kt" . | grep -vE "/test/|Test\.kt|/main\.kt"
```

**Why it's a bug.** Blocks the calling thread, including the UI thread. ANRs follow.
Common offender: bridging suspend code to legacy Java callers without isolating the bridge.

**Severity.** Critical if reachable from the main thread. High otherwise.

**Recommended fix.** For Java interop, expose a callback/future variant via
`CoroutineScope.future { … }` (kotlinx-coroutines-jdk8) or use a deliberate background
dispatcher. Never `runBlocking` on `Dispatchers.Main`.

---

### D3 — Flow collection without `repeatOnLifecycle`

**Pattern.** `.collect { … }` on a Flow inside a Fragment/Activity that is NOT wrapped in
`repeatOnLifecycle(Lifecycle.State.STARTED)` (or `flowWithLifecycle`).

```bash
grep -rEn "\.collect\s*\{" --include="*.kt" . \
  | grep -vE "repeatOnLifecycle|flowWithLifecycle|/test/"
```

For each hit, open the file and check:
- Is it inside an Activity/Fragment?
- Is it inside `lifecycleScope.launch { … }` directly without `repeatOnLifecycle`?
- Is the collected Flow tied to UI state (Room, network, StateFlow, etc.)?

**Why it's a bug.** When the screen goes to the background, the coroutine continues
collecting. For hot upstreams (Room invalidation tracker, `callbackFlow` from system
services) this leaks the Fragment view and processes events that update destroyed UI.

**Severity.** High. Critical if the collected upstream holds references to expensive
resources.

**Recommended fix.**

```kotlin
// Before
viewLifecycleOwner.lifecycleScope.launch {
    viewModel.uiState.collect { render(it) }
}

// After
viewLifecycleOwner.lifecycleScope.launch {
    viewLifecycleOwner.repeatOnLifecycle(Lifecycle.State.STARTED) {
        viewModel.uiState.collect { render(it) }
    }
}
```

In Compose, prefer `collectAsStateWithLifecycle()` over `collectAsState()`.

---

### D4 — `StateFlow` used for one-shot events

**Pattern.** `MutableStateFlow<Event?>` or `MutableStateFlow<NavCommand>` where the value
represents a single event (navigation, snackbar, toast, dialog).

```bash
grep -rEn "MutableStateFlow<.*Event|MutableStateFlow<.*Effect|MutableStateFlow<.*Nav" \
  --include="*.kt" .
```

Also look for ViewModels that expose `StateFlow` of nullable types where the receiver
is expected to "consume" the event by setting it back to `null`.

**Why it's a bug.** `StateFlow` replays the latest value to every new collector. After
a configuration change the same event fires again — duplicate navigation, repeated
toasts, double-shown dialogs. The "set to null after consume" pattern races with new
emissions.

**Severity.** High. Often surfaces as user-facing duplicate-toast / double-navigation
bugs that are hard to reproduce in development.

**Recommended fix.** Use a `Channel<Event>(Channel.BUFFERED)` exposed as
`receiveAsFlow()`, or a `MutableSharedFlow<Event>(extraBufferCapacity = 1)`. Channels
deliver each event exactly once.

```kotlin
private val _effects = Channel<UiEffect>(Channel.BUFFERED)
val effects = _effects.receiveAsFlow()
```

---

### D5 — `SharedFlow` with `replay = 0` used as state

**Pattern.** `MutableSharedFlow<UiState>()` (default `replay = 0`) where collectors expect
to render the current state.

```bash
grep -rEn "MutableSharedFlow<" --include="*.kt" .
```

**Why it's a bug.** A new collector arriving after an emission gets nothing. Late
subscribers (e.g. a Fragment recreated on rotation) see a blank screen until the next
emission.

**Severity.** Medium to High depending on user impact.

**Recommended fix.** Use `MutableStateFlow` for state, or `MutableSharedFlow(replay = 1)`
if you specifically need SharedFlow's broadcast semantics.

---

### D6 — `launch` used where `async`/`await` is needed (or vice versa)

**Pattern A.** `async { … }` whose result is never `.await()`'d — fire-and-forget with
async loses the coroutine if the parent is cancelled and silently swallows exceptions
until `await()` is called.

```bash
grep -rEn "\.async\s*\{" --include="*.kt" .
```

For each hit, scan forward for `.await()`. If never awaited, it should have been `launch`.

**Pattern B.** `launch { … }` followed by reading a value mutated inside the block —
race condition; the caller may read before the block runs.

**Severity.** High for swallowed exceptions; Medium for the inverse.

**Recommended fix.** Use `launch` for fire-and-forget, `async` only when you need the
result. If you need to await, await it.

---

### D7 — Missing `flowOn` for upstream blocking work

**Pattern.** `flow { … emit(blockingCall()) … }` or operators doing CPU/IO work
without `.flowOn(Dispatchers.IO)` or `.flowOn(Dispatchers.Default)` upstream of the
collector.

```bash
grep -rEn "\bflow\s*\{|\.map\s*\{|\.transform\s*\{" --include="*.kt" . \
  | head -200
```

For each, inspect whether the block does I/O or heavy CPU and whether `flowOn` is
present anywhere upstream of `.collect`.

**Why it's a bug.** Without `flowOn`, the work runs on the collector's context — usually
`Dispatchers.Main` from a Fragment/ViewModel observer. Janks the UI; on slow operations
triggers ANR.

**Severity.** Medium to Critical depending on cost of the work.

**Recommended fix.** Add `.flowOn(Dispatchers.IO)` (or `Default`) immediately upstream
of the heavy operator, not at the bottom of the chain.

---

### D8 — Blocking calls inside coroutines

**Pattern.** Inside a `suspend fun` or coroutine block:

```bash
grep -rEn "Thread\.sleep|\.readBytes\(\)|\.readText\(\)|URL\(.+\)\.openStream|\
JdbcConnection|HttpURLConnection|ObjectInputStream|FileInputStream|FileOutputStream" \
  --include="*.kt" .
```

For each hit, check if it's inside a suspend context and on which dispatcher.

**Why it's a bug.** Blocks the underlying thread. On `Dispatchers.Main` → ANR. On
`Dispatchers.IO` → wastes a thread from the pool, can starve other I/O. Cancellation
also stops working — the coroutine cannot be cancelled while blocked.

**Severity.** Critical on Main, High on IO/Default.

**Recommended fix.** Use suspending alternatives (`okhttp3` `await`, `Retrofit` suspend
functions, `withContext(Dispatchers.IO) { … }` for unavoidable blocking I/O, Ktor
client). For `Thread.sleep`, use `delay`.

---

### D9 — Non-cooperative cancellation

**Pattern A.** Tight loops with no suspension points:

```kotlin
while (condition) {
    doCpuWork()  // never calls a suspending function
}
```

```bash
grep -rEnB1 -A3 "while\s*\(.*\)\s*\{" --include="*.kt" . | head -200
```

**Pattern B.** `try { … } catch (e: Exception) { … }` swallowing `CancellationException`.

```bash
grep -rEn "catch\s*\(\s*\w+\s*:\s*(Exception|Throwable)" --include="*.kt" . | head -100
```

For each, check if `CancellationException` is rethrown.

**Why it's a bug.** Coroutines cannot be cancelled at non-suspending points without
`yield()` or `ensureActive()`. Catching `CancellationException` and swallowing it breaks
structured concurrency — the coroutine appears alive after its scope is cancelled.

**Severity.** High. Manifests as work continuing after a screen leaves, potentially
mutating state that no longer exists.

**Recommended fix.**

```kotlin
// In tight loops:
while (isActive) { doCpuWork() }
// Or:
yield()  // periodically inside the loop

// In catch blocks:
catch (e: CancellationException) { throw e }
catch (e: Exception) { /* handle */ }
```

---

### D10 — Suspend function returns `Job`/`Deferred`

**Pattern.** `suspend fun foo(): Job` or `suspend fun foo(): Deferred<X>`.

```bash
grep -rEn "suspend fun.*: (Job|Deferred)" --include="*.kt" .
```

**Why it's a bug.** Almost always a category error. The suspend function should either
return the result directly, or it shouldn't be suspend. Returning a Job from a suspend
function tangles structured concurrency — callers don't know whether to await, join, or
cancel.

**Severity.** Medium. Mostly a correctness/maintainability defect, occasionally hides
real races.

**Recommended fix.** Decide: is the function a suspending operation that produces a
result (return the result), or a launcher (drop `suspend`, accept a `CoroutineScope`)?

---

### D11 — `viewModelScope` used for work that should outlive the ViewModel

**Pattern.** `viewModelScope.launch { saveAnalytics() }` or
`viewModelScope.launch { uploadCriticalData() }` where the user can navigate away
mid-operation.

**Why it's a bug.** `viewModelScope` is cancelled in `onCleared()`. Critical writes
get cancelled if the screen is closed before they complete.

**Severity.** High when data persistence is involved.

**Recommended fix.** Use an application-scoped scope or `WorkManager` for must-complete
work. ViewModelScope is for UI-bound work only.

---

### D12 — Missing `SupervisorJob` where children must fail independently

**Pattern.** Custom `CoroutineScope(...)` constructions without `SupervisorJob()`:

```bash
grep -rEn "CoroutineScope\(" --include="*.kt" .
```

**Why it's a bug.** With a regular `Job`, one child's failure cancels all siblings.
For top-level scopes (e.g. an `Application` scope launching independent jobs), this
means one error nukes everything.

**Severity.** Medium.

**Recommended fix.** `CoroutineScope(SupervisorJob() + Dispatchers.Default)` (or whatever
dispatcher fits). For class-internal scopes that are the *parent* of related work,
regular Job is fine — that's the whole "fail together" intent.

---

### D13 — `Dispatchers.Main` vs `Dispatchers.Main.immediate` mistakes

**Pattern.** `withContext(Dispatchers.Main) { … }` invoked from code already on the main
thread for trivial synchronous work — wastes a re-dispatch, defers the work to the next
loop tick (visible as a one-frame flicker for UI updates).

**Severity.** Low to Medium.

**Recommended fix.** Use `Dispatchers.Main.immediate` when the dispatch should be
synchronous if already on Main.

---

### D14 — `collect` + `launchIn` redundancy / shape mistakes

**Pattern A.** `flow.onEach { … }.launchIn(scope)` is correct and preferred.

**Pattern B.** `scope.launch { flow.collect { … } }` — also correct but verbose.

**Pattern C.** `flow.collect { … }` at top level (not inside a coroutine) — won't compile,
but `flow.onEach { … }` without `launchIn` *will* compile and silently does nothing.

```bash
grep -rEn "\.onEach\s*\{" --include="*.kt" .
```

For each, scan for `launchIn` or `collect` consuming the resulting Flow.

**Severity.** Medium. The "no-op Flow" case is a real bug — users wonder why their
listener never fires.

---

### D15 — `combine`/`zip` with `MutableStateFlow` initial-value surprise

**Pattern.** `combine(stateFlowA, stateFlowB) { … }` where one of the flows starts with
a default that the UI shouldn't render (e.g. `MutableStateFlow(emptyList())` combined
with a "loaded" flag).

**Severity.** Low. Mostly a visual flash; flag only when user-impacting.

**Recommended fix.** Use a sealed `UiState` (Loading / Success / Error) instead of
combining raw values.

---

## Step 3 — Write the report

For each detector that produced a hit, write a Bug Report Format finding to
`<workspace>/findings-coroutine-and-flow-defects.md`. Group by detector ID for traceability,
but use the shared format — the dispatcher will renumber and resort.

If a detector produced zero hits, note it briefly so the dispatcher can include it in
the "Specialists that found nothing" section.

---

## Notes

- Many of these patterns require eyeballing context — grep is a starting point, not a
  verdict. Always read the surrounding code before flagging.
- Tests are noisy — `runBlocking` and `GlobalScope` are often fine in test code. Filter
  out `/test/`, `/androidTest/`, and `*Test.kt`.
- For codebases using older RxJava patterns mid-migration, expect duplicates between
  Rx and coroutine paths — flag the coroutine ones and mention the migration context.
