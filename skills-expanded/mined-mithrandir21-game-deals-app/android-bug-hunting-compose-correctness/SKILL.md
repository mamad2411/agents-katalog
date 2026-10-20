---
name: android-bug-hunting-compose-correctness
description: >
  Hunt for runtime defects in Jetpack Compose code: side effects launched outside
  LaunchedEffect/DisposableEffect, state read in non-composable scopes, remember/rememberSaveable
  used incorrectly (missing keys, non-Saveable types, recomputing on every recomposition),
  LaunchedEffect keyed on Unit when it should depend on state, unstable lambda captures
  causing recomposition storms, hot/cold Flow misuse in Compose (collectAsState vs
  collectAsStateWithLifecycle), state hoisting violations, mutating state during composition,
  and snapshot/derivedStateOf misuse. Use this skill whenever the user asks to find bugs in
  Compose UI, "find Compose problems", "audit my Composables", "why is my Compose code
  recomposing too much", or any phrasing implying defects in @Composable functions. Trigger
  whenever a bug hunt covers a project with @Composable functions.
---

# Compose Correctness Hunter

## Purpose

Compose has a small but distinctive set of correctness traps. Most of them produce bugs
that look like "weird UI behaviour" rather than crashes — duplicated effects, stale state,
missed updates, infinite recomposition, jank from over-recomposition. This skill encodes
the well-known antipatterns and looks for each one.

**Output format.** Use the shared Bug Report Format. Read `.claude/skills/android-bug-hunting-dispatcher/references/report-format.md` before writing findings.

---

## Step 1 — Scope

```bash
# All composable functions
grep -rEln "@Composable" --include="*.kt" .

# Effect APIs
grep -rEn "LaunchedEffect|DisposableEffect|SideEffect|rememberCoroutineScope|\
remember\s*\{|rememberSaveable|derivedStateOf|produceState|snapshotFlow|\
mutableStateOf|collectAsState|collectAsStateWithLifecycle" --include="*.kt" .
```

---

## Step 2 — Run each detector

---

### D1 — Side effect launched outside an effect handler

**Pattern.** A side-effecting call (network request, analytics event, navigation,
`viewModel.foo()`) made directly in the body of a `@Composable` function — not inside
`LaunchedEffect`, `DisposableEffect`, or `SideEffect`.

```bash
grep -rEnB2 -A2 "@Composable" --include="*.kt" . | head -400
```

For each composable, scan the body for direct calls like:
- `viewModel.fetchData()`
- `analytics.log("…")`
- `navController.navigate(…)`
- `coroutineScope.launch { … }` (where `coroutineScope` is local-scoped via `rememberCoroutineScope`)

These should be inside `LaunchedEffect(key) { … }`, an event callback (`onClick`), or
explicitly opt-in via `SideEffect`.

**Why it's a bug.** Composables can be invoked many times per second. A naked side
effect in the body fires on every recomposition — duplicate analytics, repeat network
calls, infinite navigation loops, double-shown dialogs.

**Severity.** Critical for navigation/network/persistent side effects. High for
analytics. Medium for log spam.

**Recommended fix.**

```kotlin
@Composable
fun Screen(viewModel: VM) {
    LaunchedEffect(Unit) {
        viewModel.fetchData()  // runs once per composition entering the tree
    }
}
```

For state-dependent triggers, key the LaunchedEffect on the trigger:

```kotlin
LaunchedEffect(userId) { viewModel.loadProfile(userId) }
```

---

### D2 — `LaunchedEffect(Unit)` (or `LaunchedEffect(true)`) when it should depend on state

**Pattern.**

```bash
grep -rEn "LaunchedEffect\s*\(\s*(Unit|true)\s*\)" --include="*.kt" .
```

For each hit, read the block. If it references parameters that can change (state,
arguments to the composable), the key is wrong.

**Why it's a bug.** Effect runs once and never re-fires when its inputs change. Stale
data, missed updates.

**Severity.** High.

**Recommended fix.** Key the effect on every input that should retrigger it:

```kotlin
// Before
LaunchedEffect(Unit) { vm.load(productId) }
// After
LaunchedEffect(productId) { vm.load(productId) }
```

---

### D3 — `rememberSaveable` with non-Saveable types

**Pattern.**

```bash
grep -rEn "rememberSaveable" --include="*.kt" .
```

For each hit, check the type held. Saveable types are: primitives, `String`, types
implementing `Parcelable`, types with a custom `Saver`. Common offenders:
- `LocalDate` / `LocalDateTime`
- `Uri` (sometimes — depends on version)
- Custom data classes without a `Saver`
- `Color` (works), `Brush` (does not)
- `MutableList`/`MutableMap` raw

**Why it's a bug.** On process death + restoration (or sometimes config change), the
value either fails to restore or throws.

**Severity.** Medium. Manifests as state lost on rotation only when Don't Keep Activities
is on, or after the OS reclaims the process.

**Recommended fix.** Provide a `Saver`:

```kotlin
val DateSaver = Saver<LocalDate, String>(
    save = { it.toString() },
    restore = { LocalDate.parse(it) }
)

val date = rememberSaveable(saver = DateSaver) { mutableStateOf(LocalDate.now()) }
```

Or use a `Parcelable`/`@Parcelize` data class.

---

### D4 — `remember` without correct keys

**Pattern A.** `remember { computeFromArgs(arg) }` — recomputes only on first composition,
but `arg` may change.

```bash
grep -rEn "remember\s*\{" --include="*.kt" .
```

For each, check the block: does it depend on parameters that can change? If yes, the
key form should be used: `remember(arg) { … }`.

**Pattern B.** `remember(state.value)` — keying on a state read inside the same
composition. Almost always wrong; use `derivedStateOf` instead.

**Why it's a bug.** Stale memoized values, or unnecessary recomputation, or both.

**Severity.** Medium.

**Recommended fix.** `remember(arg) { compute(arg) }`. For values derived from state,
use `derivedStateOf`:

```kotlin
val isAtTop by remember {
    derivedStateOf { listState.firstVisibleItemIndex == 0 }
}
```

---

### D5 — `collectAsState()` instead of `collectAsStateWithLifecycle()`

**Pattern.**

```bash
grep -rEn "\.collectAsState\(\)" --include="*.kt" .
```

For each hit, ask: is this in a screen-level composable that can be off-screen? In
modern Android (Compose 1.5+ and lifecycle-runtime-compose), `collectAsStateWithLifecycle()`
is the correct default for screen-bound state.

**Why it's a bug.** Plain `collectAsState` keeps the upstream Flow active even when the
host screen is not visible — wastes CPU, network, and battery; for hot upstreams (Room
invalidation, websocket) it can cause real damage.

**Severity.** Medium. High when upstream is expensive.

**Recommended fix.** Add the `lifecycle-runtime-compose` artifact and use
`collectAsStateWithLifecycle()` for any Flow representing screen-scoped state.

---

### D6 — Mutating state during composition

**Pattern.** Inside a composable body (not inside an effect or a callback), code that
calls `state.value = …` or invokes `mutableStateOf().value =` directly.

```bash
grep -rEn "\.value\s*=" --include="*.kt" .
```

For each hit, check whether it's inside a `@Composable` body and not inside a callback
or effect.

**Why it's a bug.** Causes Compose to invalidate state mid-composition, leading to
infinite recomposition loops or `IllegalStateException` ("Reading a state that was
created after the snapshot was taken").

**Severity.** Critical when it produces the loop or exception.

**Recommended fix.** Move the mutation into `LaunchedEffect`, `SideEffect` (if it must
run after every composition that occurred), or a callback.

---

### D7 — Reading state inside a remembered lambda without `rememberUpdatedState`

**Pattern.** `LaunchedEffect(Unit) { delay(5000); onTimeout() }` where `onTimeout` is a
parameter of the composable. The lambda captures the *initial* `onTimeout`; if the parent
recomposes with a new lambda, the captured one is stale.

**Why it's a bug.** Stale callbacks fire — the user sees the wrong action triggered.

**Severity.** High when the captured callback has user-visible effect.

**Recommended fix.**

```kotlin
@Composable
fun TimerScreen(onTimeout: () -> Unit) {
    val currentOnTimeout by rememberUpdatedState(onTimeout)
    LaunchedEffect(Unit) {
        delay(5000)
        currentOnTimeout()
    }
}
```

---

### D8 — `rememberCoroutineScope` used for work that doesn't need a scope

**Pattern.** `val scope = rememberCoroutineScope()` followed by `scope.launch { … }`
for work that is purely a side effect of state change (not an event response).

```bash
grep -rEn "rememberCoroutineScope" --include="*.kt" .
```

**Why it's a bug.** `rememberCoroutineScope` is for coroutines tied to user events
(e.g. `onClick { scope.launch { animate() } }`). Using it as a substitute for
`LaunchedEffect` invites the side-effect-on-recomposition problem (D1).

**Severity.** Medium.

**Recommended fix.** Use `LaunchedEffect(key) { … }` for state-driven work; reserve
`rememberCoroutineScope` for event handlers.

---

### D9 — Unstable parameters causing recomposition storms

**Pattern.** Composable parameters that are:
- `List<X>` (the interface is unstable)
- `Map<K, V>` (same)
- Functional types capturing mutable state (lambda capturing a `var`)
- Types declared in modules without `kotlinx-collections-immutable` or `@Stable`

```bash
grep -rEn "fun \w+\s*\([^)]*: List<|fun \w+\s*\([^)]*: Map<" --include="*.kt" . | grep -E "@Composable"
```

(Or: list all `@Composable` functions and inspect their parameters.)

**Why it's a bug.** Compose can't skip a composable if its inputs are unstable — every
parent recomposition forces this child to recompose, even with identical content. Cascades
into recomposition storms; can hit ANR territory in deep trees.

**Severity.** Medium to High depending on tree depth and frequency.

**Recommended fix.**
- Use `ImmutableList`/`PersistentList` from `kotlinx-collections-immutable`.
- Mark domain types `@Immutable` or `@Stable` if you can guarantee stability.
- For lambdas capturing state, hoist them into `remember`.

---

### D10 — `derivedStateOf` overuse / underuse

**Pattern A — overuse.** `derivedStateOf { someState.value }` (no actual derivation).

**Pattern B — underuse.** Heavy computation directly in composition body that depends
on state (e.g. filtering a large list on every recomposition).

**Why it's a bug (overuse).** Adds cost without benefit.
**Why it's a bug (underuse).** Recomputes expensive work on every recomposition even
when the *result* hasn't changed.

**Severity.** Medium.

**Recommended fix.**

```kotlin
val visibleItems by remember(items, query) {
    derivedStateOf { items.filter { it.matches(query) } }
}
```

---

### D11 — `MutableState` exposed from a ViewModel

**Pattern.**

```bash
grep -rEn "mutableStateOf" --include="*.kt" . | grep -v "/test/"
```

For each hit in a ViewModel, check if the resulting `MutableState` is exposed publicly.

**Why it's a bug.** Crosses the layering boundary — Compose runtime types in domain/VM
layer. Also tends to lack the back-pressure / replay semantics you'd want; rebinds
poorly across configuration changes.

**Severity.** Low to Medium (mostly a layering defect, occasionally a real bug when
the State is read from a non-Compose context).

**Recommended fix.** Use `StateFlow<UiState>` from the VM; convert to State at the UI
boundary with `collectAsStateWithLifecycle()`.

---

### D12 — `DisposableEffect` without a real `onDispose`

**Pattern.**

```bash
grep -rEnA10 "DisposableEffect" --include="*.kt" .
```

For each hit, verify the lambda ends with `onDispose { … }` and that the dispose block
actually undoes the setup (unregisters, cancels, closes).

**Why it's a bug.** A no-op `onDispose { }` for a `DisposableEffect` that registered
something means the registration leaks.

**Severity.** High when the registration is non-trivial (sensors, listeners, observers).

**Recommended fix.** Make `onDispose` symmetric with the setup.

---

### D13 — `produceState` returning before initial value is set

**Pattern.**

```bash
grep -rEnA15 "produceState" --include="*.kt" .
```

For each hit, check whether the producer block can suspend indefinitely before the first
assignment to `value`. If yes, consumers see the initial value forever.

**Severity.** Medium. Manifests as a loading state never resolving when the producer
hangs on a network call without timeout.

**Recommended fix.** Set `value` early (e.g. to a Loading sentinel), and use `withTimeout`
where applicable.

---

### D14 — `Modifier` parameter not flowed through, or `Modifier.composed` overuse

**Pattern.** `@Composable fun Foo() { Box(Modifier.padding(8.dp)) { … } }` with no
`modifier` parameter — caller can't customize layout.

**Severity.** Low. Usually a usability/maintainability issue, occasionally hides a bug
(e.g. caller can't apply `testTag`).

**Recommended fix.** Take `modifier: Modifier = Modifier` and apply it at the root.

---

### D15 — Reading `LocalConfiguration.current` / `LocalDensity.current` in inner composables

**Pattern.** Repeatedly reading composition locals deep in the tree, or reading them in
hot paths.

**Severity.** Low — performance issue rather than correctness, unless misused for state.

**Recommended fix.** Read once at the top of the composable into a local `val`.

---

## Step 3 — Write the report

Write findings to `<workspace>/findings-compose-correctness.md` in shared Bug Report
Format. Group by detector ID; the dispatcher will renumber and sort.

---

## Notes

- For Compose 1.6+ projects, the Compose Compiler can report stability for parameter
  types — if the team has the metrics enabled, inspect the report alongside the grep
  results for D9.
- Many of these bugs are best confirmed by running with the recomposition counter
  overlay (`Layout Inspector → Show Recomposition Counts`); flag patterns from this
  skill that match observed re-composition hot spots.
- Distinguish between Compose-Material and Compose-Material3 idioms; `collectAsStateWithLifecycle`
  is in `androidx.lifecycle:lifecycle-runtime-compose` regardless.
