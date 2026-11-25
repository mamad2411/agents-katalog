---
name: mavericks-mvi
description: Use when creating or modifying Mavericks 3.x State, MavericksState, MavericksViewModel, AssistedViewModelFactory, hiltMavericksViewModelFactory, ViewModelModule binding, initial args, Compose mavericksViewModel, collectAsStateWithLifecycle, Fragment MavericksView subscriptions, Async execute, setState, withState, DeliveryMode, uniqueOnly, or one-shot effects
---

# Mavericks MVI Guide

Mavericks screens are rendered from immutable state. Keep state data-only, reducers pure, and side effects in ViewModel methods or UI consumers.

## Quick Reference

| Task | Use |
|---|---|
| Define screen state | `data class XxxState(...) : MavericksState` |
| Create Hilt VM | `@AssistedInject` + `@Assisted initialState` + `Factory` + `hiltMavericksViewModelFactory()` |
| Register VM | `@Binds @IntoMap @ViewModelKey` in the owning `ViewModelModule` |
| One-shot request | `suspend { repo.call() }.execute { copy(request = it) }` |
| Long-lived Flow to normal state | `flow.setOnEach { value -> copy(value = value) }` |
| Refresh without UI flicker | `.execute(retainValue = State::request) { ... }` |
| Compose VM | `mavericksViewModel()` or `mavericksViewModel(argsFactory = { args })` |
| Compose state | `vm.collectAsStateWithLifecycle(State::prop)` |
| Fragment VM | `by fragmentViewModel()` / `activityViewModel()` / `parentFragmentViewModel()` |
| Fragment state | `vm.onEach(State::prop) { ... }` |
| Fragment one-shot | `vm.onEach(State::effect, deliveryMode = uniqueOnly()) { ... }` |
| Read current state in VM | `withState { state -> ... }` or suspend `awaitState()` |

## Core Rules

- State must be immutable, public, data-only, and reducer-safe.
- Hilt Mavericks VMs must use `@AssistedInject`, `@Assisted initialState`, `@AssistedFactory`, and `hiltMavericksViewModelFactory()`.
- Every Hilt Mavericks VM must be bound with `@Binds @IntoMap @ViewModelKey`.
- Use `execute` for finite async work represented by `Async<T>`.
- Use `setOnEach` for long-lived Flows that map directly to ordinary State fields.
- Use Mavericks lifecycle-aware Compose collection: `com.airbnb.mvrx.compose.collectAsStateWithLifecycle`.
- `DeliveryMode` is only for `MavericksView` subscriptions, not ViewModel `onEach` and not Compose.
- Effects are a project pattern on top of State; nullable single effects are not queues.

## Read Only What You Need

- State fields, immutability, args, and `@PersistState`: [references/state.md](references/state.md)
- ViewModel template, `execute`, `setOnEach`, `setState`, `withState`: [references/viewmodel-execute.md](references/viewmodel-execute.md)
- Hilt component and map binding: [references/hilt.md](references/hilt.md)
- Compose, Fragment, `MavericksView`, `DeliveryMode`, scopes: [references/observing-ui.md](references/observing-ui.md)
- Nullable effects, effect queues, consumption rules: [references/effects.md](references/effects.md)
- `Async<T>` states and rendering patterns: [references/async.md](references/async.md)
- Mavericks ViewModel testing: [references/testing.md](references/testing.md)

## Common Pitfalls

| Pitfall | Fix |
|---|---|
| Missing State defaults with no args path | Add defaults or initialize through args/`initialState()` |
| Mutable State field | Use immutable/read-only types and copy on update |
| Storing derived values | Use computed properties |
| Reading immediately after `setState` | Use reducer state, `withState`, or `awaitState()` |
| Heavy work inside reducer | Move work before `setState` or into `execute(dispatcher)` |
| Long action inside VM `onEach` gets cancelled | `onEach` uses `collectLatest`; move long work elsewhere |
| Flow wrapped in `execute` when no `Async` is needed | Use `setOnEach` |
| UI flickers during refresh | Use `retainValue` |
| Rendering state with `uniqueOnly()` | Use default delivery mode |
| Compose using legacy `collectAsState` | Use Mavericks `collectAsStateWithLifecycle` |
| Required Compose args omitted | Use `mavericksViewModel(argsFactory = { args })` |
| Effect fires twice after Fragment restart | Use `uniqueOnly()` and clear after handling |
| Multiple effects lost | Use a list/queue or redesign event semantics |
| Hilt VM creation crashes | Check `@AssistedFactory`, companion factory, and ViewModelModule binding |
