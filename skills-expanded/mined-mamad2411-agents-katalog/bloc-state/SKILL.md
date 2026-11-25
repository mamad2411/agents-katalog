---
name: bloc-state
description: How state is shaped with flutter_bloc in this project — Bloc vs Cubit, freezed unions for states/events, bloc_concurrency transformers instead of manual in-flight flags, one-shot effects, and testing with bloc_test.
---

# Bloc state

## Bloc vs Cubit

- **Cubit** — a set of methods that produce states. Best for: settings toggle, filter controls, simple screen state.
- **Bloc** — discrete events → states. Best for: auth, checkout, forms, anything with "submit" semantics where concurrency and ordering matter.

If you'd write the same method two different ways depending on "is it busy?", you want a Bloc with a transformer.

## Canonical Bloc shape

```dart
// search_bloc.dart
class SearchBloc extends Bloc<SearchEvent, SearchState> {
  SearchBloc({required this.repo}) : super(const SearchState.idle()) {
    on<SearchEvent>((event, emit) async {
      await event.map(
        queryChanged: (e) => _onQueryChanged(e, emit),
        cleared:      (_) async => emit(const SearchState.idle()),
      );
    }, transformer: restartable()); // cancel in-flight when a new event arrives
  }

  final SearchRepository repo;

  Future<void> _onQueryChanged(QueryChanged e, Emitter<SearchState> emit) async {
    final query = e.query.trim();
    if (query.length < 2) { emit(const SearchState.idle()); return; }
    emit(const SearchState.loading());
    final result = await repo.search(query);
    emit(result.fold(
      (failure) => SearchState.error(failure),
      (items)   => SearchState.success(items),
    ));
  }
}
```

```dart
// search_event.dart
@freezed
sealed class SearchEvent with _$SearchEvent {
  const factory SearchEvent.queryChanged(String query) = QueryChanged;
  const factory SearchEvent.cleared() = Cleared;
}

// search_state.dart
@freezed
sealed class SearchState with _$SearchState {
  const factory SearchState.idle() = _Idle;
  const factory SearchState.loading() = _Loading;
  const factory SearchState.success(List<SearchResult> items) = _Success;
  const factory SearchState.error(Failure failure) = _Error;
}
```

Rules:
- Events and states are **freezed sealed unions**. `.map` and `switch` are both exhaustive.
- The bloc's public surface is the `add(event)` method + `state` getter + `stream`. Don't add custom methods.
- All `emit`s happen in event handlers. No `emit` from outside `on<...>`.

## `bloc_concurrency` transformers

Use the right transformer instead of guarding with booleans:

- **`droppable()`** — ignore new events while one is in flight. **Form submissions, "Sign in", any non-idempotent action.**
- **`restartable()`** — cancel the in-flight one and run the new. **Search, filters, anything that supersedes the last.**
- **`sequential()`** — queue. **Uploads, analytics events, ordered writes.**
- **`concurrent()`** (default) — just don't rely on order.

If you see this in existing code, it's an anti-pattern to replace:

```dart
// bad
bool _isProcessing = false;
on<Submit>((e, emit) async {
  if (_isProcessing) return;
  _isProcessing = true;
  try { ... } finally { _isProcessing = false; }
});

// good
on<Submit>(_onSubmit, transformer: droppable());
```

## State shape — union vs single state

Use a **union** when states carry different data:

```dart
@freezed
sealed class ActivityState with _$ActivityState {
  const factory ActivityState.loading() = _Loading;
  const factory ActivityState.success(Activity activity) = _Success;
  const factory ActivityState.error(Failure failure) = _Error;
}
```

Use a **single state** when fields overlap and only a `status` changes:

```dart
@freezed
class CheckoutState with _$CheckoutState {
  const factory CheckoutState({
    @Default(FormzSubmissionStatus.initial) FormzSubmissionStatus status,
    @Default(Email.pure()) Email email,
    @Default(Password.pure()) Password password,
    String? errorMessage,
  }) = _CheckoutState;
}
```

Union when the UI looks fundamentally different per state. Single when the UI keeps its shape and only a button / banner changes.

## One-shot effects

Snackbars, navigation, toasts, vibration — **never** as states. Two patterns:

### Pattern A — effect field in state (easiest, good default)

```dart
@freezed
class LoginState with _$LoginState {
  const factory LoginState({
    @Default(FormzSubmissionStatus.initial) FormzSubmissionStatus status,
    LoginEffect? effect,                 // <-- transient
  }) = _LoginState;
}

@freezed
sealed class LoginEffect with _$LoginEffect {
  const factory LoginEffect.navigateHome() = _NavigateHome;
  const factory LoginEffect.showError(String message) = _ShowError;
}
```

The view uses `BlocListener` with `listenWhen` and the bloc **clears the effect** on the next state change:

```dart
// after consuming, the next emit rebuilds state with effect: null
emit(state.copyWith(effect: null));
```

### Pattern B — separate `Stream<Effect>` controller

When effects must fire independently of state changes. Add a `StreamController<Effect>` in the bloc, close it in `close()`, expose `Stream<Effect> get effects`.

Pick one per feature, don't mix.

## Error surface

- Blocs never know about `DioException`. They receive `Failure` via `Either`.
- Failures map to UI either as an error state or an effect (snackbar).
- For forms, surface `ValidationFailure.fields` into per-field `formz` inputs.

## Lifecycle

- `close()` overrides **must** call `super.close()`. Cancel subscriptions there.
- Never `await`-loop inside `close()`. The BLoC is being disposed; if you need a long shutdown, do it before the widget goes away.

## Testing

Keep a single concept per test. See `.claude/skills/flutter-testing/SKILL.md`. Rough template:

```dart
blocTest<SearchBloc, SearchState>(
  'loading → success on valid query',
  build: () => SearchBloc(repo: fakeRepo..nextResult = Right(coffeeList)),
  act: (b) => b.add(const SearchEvent.queryChanged('cof')),
  expect: () => const [SearchState.loading(), SearchState.success(coffeeList)],
);
```

## Hard nos

- No `Equatable` on new states/events. Freezed.
- No `_isProcessing` flags. `droppable()` / `restartable()` / `sequential()`.
- No effects encoded as states ("ShowSnackbarState"). Use an effect field or a separate stream.
- No direct dio/api calls in a bloc. Repository only.
- No `.then(...)` chains in handlers. Await.
