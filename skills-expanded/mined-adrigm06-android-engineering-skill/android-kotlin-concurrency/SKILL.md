---
name: android-kotlin-concurrency
description: Kotlin coroutines and Flow engineering skill for structured concurrency, scope lifecycle, dispatcher strategy, and reactive stream design. Use when coroutine leaks, cancellation failures, dispatcher misuse, Flow vs StateFlow selection, or thread-safety in suspend functions are in scope.
---

# Purpose

Design correct and leak-free Kotlin concurrency in Android using structured concurrency principles, evidence-driven dispatcher strategy, and safe reactive stream composition.

## Scope and authority

This skill is lead authority for:

- coroutine scope design and lifecycle binding
- Flow / StateFlow / SharedFlow selection and composition
- dispatcher strategy and thread-safety decisions
- cancellation safety and structured concurrency enforcement
- suspend function design and cold/hot stream selection

This skill must defer when applicable:

- architectural ownership of ViewModels and repositories to `android-architecture`
- UI state rendering and recomposition to `android-compose`
- performance profiling and ANR root-cause to `android-performance`

## When to use

- coroutine scope is leaking or outliving its lifecycle (e.g., `GlobalScope` misuse)
- cancellation is not propagating correctly across suspend calls
- `Flow` vs `StateFlow` vs `SharedFlow` selection is unclear or wrong
- dispatcher choice causes jank or blocks the main thread
- suspend function is not cancellable or has unsafe shared mutable state
- structured concurrency violations in production or test code

## When not to use

- when the primary question is ViewModel architecture or repository layering (`android-architecture`)
- when the primary question is jank or startup profiling without concurrency root cause (`android-performance`)
- when the question is Compose state management specifically (`android-compose`)

## Decision engine workflow

1. Identify the concurrency problem class (scope, dispatcher, cancellation, stream type, thread-safety).
2. Classify lifecycle binding context (ViewModel, Fragment, Service, WorkManager, standalone).
3. Select stream type and scope strategy branch.
4. Validate dispatcher choice and cancellation propagation.
5. Run cross-skill checks (architecture for ownership, performance for hot-path impact).
6. Resolve conflicts using authority model from `../../AGENTS.md`.
7. Return implementation guidance with fallback options.

## Branching decision tree

### Branch A: scope and lifecycle binding

- `ViewModel` (UI-triggered async work):
  - use `viewModelScope` — auto-cancelled on ViewModel cleared.
  - do not use `GlobalScope` or manually constructed scopes that outlive the ViewModel.
- `Fragment / Activity` (lifecycle-bound observation):
  - use `lifecycleScope` with `repeatOnLifecycle` for Flow collection.
  - avoid `launchWhenStarted` — it suspends but does not cancel on STOP.
- `Repository / data layer` (no lifecycle):
  - inject a `CoroutineScope` from DI with explicit ownership.
  - never create ad-hoc `CoroutineScope(Dispatchers.IO)` without a cancellation owner.
- `WorkManager / Service`:
  - use `CoroutineWorker` or bind to an injected scope with explicit job cancellation.

### Branch B: stream type selection

- `StateFlow`: current-value holder for UI state; always has a value; replays last to new collectors.
- `SharedFlow`: for events/effects that must not replay (navigation events, one-time signals).
- `Flow` (cold): on-demand data streams (Room queries, network, Paging); no independent lifecycle.
- `Channel`: only when one-to-one producer-consumer delivery with backpressure is required; prefer `Flow` otherwise.

### Branch C: dispatcher strategy

- `Dispatchers.Main`: UI updates, StateFlow emissions from ViewModel, navigation triggers.
- `Dispatchers.Main.immediate`: when already on main thread and dispatch overhead must be avoided.
- `Dispatchers.IO`: blocking I/O (network, disk, database). Not for CPU-intensive work.
- `Dispatchers.Default`: CPU-intensive computation (parsing, sorting, encoding).
- `Dispatchers.Unconfined`: avoid in production; use only in tests with `UnconfinedTestDispatcher`.

Do not apply `withContext(Dispatchers.IO)` as a blanket jank fix — profile before changing dispatcher.

### Branch D: cancellation safety

- Long-running suspend loops must call `ensureActive()` or check `isActive` at iteration boundaries.
- Use `withTimeout` / `withTimeoutOrNull` for deadline-bound operations.
- Avoid swallowing `CancellationException` in `try/catch (e: Exception)` blocks — always re-throw it.
- Prefer `supervisorScope` when child failure must not cancel siblings.

### Branch E: testing strategy

- Use `StandardTestDispatcher` with `advanceUntilIdle()` for deterministic coroutine control.
- Inject dispatchers via constructor — never hardcode `Dispatchers.IO` in production classes.
- Use `turbine` for Flow assertion in unit tests.
- Replace `delay()` with virtual time in tests via `TestCoroutineScheduler`.

## Conflict handling and composition

When used with other skills:

- With `android-architecture`:
  - scope ownership must align with layer ownership; a Repository must not own a ViewModel-scoped job.
- With `android-performance`:
  - measured jank may implicate wrong dispatcher; escalate with trace evidence before changing dispatch strategy.
- With `android-testing`:
  - flaky tests caused by real-time delays or shared coroutine state require deterministic dispatcher injection.
- With `android-compose`:
  - `StateFlow` consumed in Compose must be collected with `collectAsStateWithLifecycle`, not `collectAsState`.

## Quantitative gates

Use measurable gates and label each `pass | at-risk | fail`:

- scope-leak gate: no coroutines alive after owning lifecycle ends (verified by leak detection or test)
- cancellation propagation gate: `CancellationException` reaches structured root without suppression
- dispatcher correctness gate: no blocking calls on `Dispatchers.Main`; no UI updates from `Dispatchers.IO`
- test determinism gate: all coroutine tests use injected test dispatcher; no `Thread.sleep()` or real `delay()`

If no observable evidence exists, return a measurement and instrumentation plan before recommending dispatcher or scope changes.

## Tradeoff realism

Allow context-justified non-ideal decisions when explicit:

- `GlobalScope` may be acceptable for fire-and-forget analytics with no cancellation requirement — must be labeled.
- `runBlocking` is acceptable in tests and top-level entry points; never acceptable in production suspend chains.
- Mixing cold Flow and SharedFlow is acceptable during migration with an explicit cutover plan.

Do not present temporary concurrency shortcuts as final architecture.

## Uncertainty protocol

Always report confidence:

- `High` (>= 0.80)
- `Medium` (0.60-0.79)
- `Low` (< 0.60)

If confidence is medium/low:

- state missing context (scope ownership, lifecycle binding, whether caller is suspend or not)
- provide at least one conservative fallback
- escalate to `android-architecture` when scope ownership is structurally ambiguous
- escalate to `android-performance` when dispatcher change is proposed without profiling evidence

## Cross-skill handoff payload

Use the standard payload defined in `../../AGENTS.md` (section: Cross-skill handoff contract).
Set `requesting_skill` to `android-kotlin-concurrency`.

## Output contract

Follow global order from `../../AGENTS.md`:

1. `Context and constraints`
2. `Decision and rationale`
3. `Alternatives considered`
4. `Tradeoffs`
5. `Risks and mitigations`
6. `Confidence and unknowns`
7. `Cross-skill impacts`
8. `Next implementation steps`

Also include:

- `Scope and lifecycle binding strategy`
- `Stream type selection`
- `Dispatcher strategy`
- `Cancellation safety analysis`
- `Testing approach`

## Anti-pattern detection

- `GlobalScope` usage without explicit fire-and-forget justification
- `launchWhenStarted` for Flow collection (suspends but does not cancel)
- blocking calls (`Thread.sleep`, `runBlocking`) inside suspend functions or coroutines
- catching `CancellationException` without re-throwing
- hardcoded `Dispatchers.IO` in production classes without injection
- `SharedFlow` used for UI state that needs a current value (use `StateFlow` instead)
- missing `repeatOnLifecycle` for lifecycle-aware Flow collection in UI layer

## Related resources

- `references/kotlin-concurrency-patterns.md`
