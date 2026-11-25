---
name: bloc-signals
description: Implement, review, test, and migrate Dart and Flutter code that uses BlocSignal (bloc_signals, bloc_signals_flutter, bloc_signals_test), the BLoC-style API built on signals. Use this when the code imports package:bloc_signals, extends BlocSignal or CubitSignal, uses BlocSignalProvider, BlocSignalBuilder, BlocSignalListener, or context.select, or when the user asks how BlocSignal differs from flutter_bloc or wants to move from BLoC to synchronous signal-based state.
metadata:
  last_modified: "2026-11-10"
  package_versions: "bloc_signals 1.7.0, bloc_signals_flutter 1.5.0, bloc_signals_test 1.0.3"
  source: "https://github.com/RandalSchwartz/BlocSignal (MIT). Upstream agent skill: plugins/bloc-signals/skills/bloc-signals/"
---

# BlocSignal

BlocSignal keeps the BLoC event model (events in, state out) on top of Rody Davis's signals v7 primitives. Its updates are synchronous: `emit` changes state immediately, with no stream and no microtask. It is young and its API can change, so verify against the installed package source before editing code.

## Start from the installed package
1. Read the consumer project's `pubspec.yaml` and `pubspec.lock` to find the `bloc_signals` version.
2. Check every type and member you plan to use against the installed source (`package:bloc_signals/...`). Do not assume parity with `package:bloc` or Riverpod.
3. Read the matching reference below, then make the smallest change that keeps behavior.

## Route the task
- [references/core.md](references/core.md): `BlocSignal`, `CubitSignal`, `on<E>`, `emit`, `createEffect`, equality, and `close`.
- [references/flutter.md](references/flutter.md): `BlocSignalProvider`, `BlocSignalBuilder`, `BlocSignalListener`, `BlocSignalConsumer`, `BlocSignalSelector`, and `context.value/state/select`.
- [references/testing.md](references/testing.md): `blocSignalTest`, synchronous assertions, and widget tests.
- [references/migration-from-bloc.md](references/migration-from-bloc.md): moving from `flutter_bloc` / `bloc` to BlocSignal, and the differences that break code.

## Contracts to preserve
- Constructors take named `initialState:`. Write `: super(initialState: 0)`, not `: super(0)`.
- `emit` is synchronous, and it skips a value equal to the current state.
- `add` returns `void`. Synchronous handlers finish before `add` returns.
- `close()` is idempotent, disposes effects created with `createEffect`, and drops events after closure.
- Read raw values with `stateValue` (or `value`) inside methods and handlers. `state` returns a `ReadonlySignal` for reactive bindings.
- `BlocSignalProvider(create:)` is lazy by default and owns its bloc. `BlocSignalProvider.value` does not own it.
- `context.watch<T>()` tracks provider replacement, not state changes. Use `BlocSignalBuilder` to rebuild on state.
- Never create an `effect` or `computed` inside `build`. Give it an explicit owner and a disposal path.
- A global `BlocSignalObserver` is a single slot. Compose observers instead of replacing them.

## Packages
- `bloc_signals`: core (pure Dart).
- `bloc_signals_flutter`: Flutter providers, builders, listeners, selectors.
- `bloc_signals_test`: `blocSignalTest` helpers.
- Optional: `bloc_signals_lint`, `bloc_signals_hydrate`, `bloc_signals_replay`, `bloc_signals_riverpod`, `bloc_signals_devtools`, `bloc_signals_jaspr`.

## Validation
Run `flutter analyze` and the nearest tests. The examples in these references were compiled and tested against `bloc_signals` 1.7.0, `bloc_signals_flutter` 1.5.0, and `bloc_signals_test` 1.0.3.
