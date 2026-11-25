---
name: bloc-pattern
description: Canonical BLoC pattern for Flutter apps - events past-tense, single Freezed state with status enum, side-effects via Stream<Effect>, optimistic updates. MANDATORY TRIGGERS - "bloc", "flutter_bloc", "state management", "event", "state", "BlocListener", "optimistic update", "side effect".
allowed-tools: Read, Glob, Write, Edit
---

# Skill: bloc-pattern

## When to use

Writing or refactoring a Bloc for any feature.

## Inputs

- feature slug
- list of user intents (e.g. `refresh`, `like post`, `submit comment`)
- failure modes the spec lists

## Steps

1. Create `<slug>_event.dart` — sealed class, past-tense subclasses.
2. Create `<slug>_state.dart` — single `@freezed` class with a
   `Status` enum field (`initial`, `loading`, `success`, `failure`)
   and a `Failure? failure` slot.
3. Create `<slug>_effect.dart` — sealed class of one-shot effects
   (`ShowSnack`, `NavigateTo`, `OpenSheet`).
4. Create `<slug>_bloc.dart`:
   - constructor injects usecases via `injectable`;
   - one `on<Event>` per event;
   - `emit` only state changes;
   - emit effects to a `_effects` `StreamController.broadcast()`.
5. Expose `Stream<Effect> get effects => _effects.stream;`.
6. Always `await close()` and `_effects.close()`.
7. Optimistic updates: emit success with optimistic payload first,
   reconcile with server reply, roll back on failure with effect
   `ShowSnack(localizedError)`.

## Output template (pseudo)

```dart
sealed class FeedEvent {}
final class FeedRefreshed extends FeedEvent {}
final class FeedPostLiked extends FeedEvent {
  FeedPostLiked(this.postId);
  final String postId;
}

@freezed
class FeedState with _$FeedState {
  const factory FeedState({
    @Default(FeedStatus.initial) FeedStatus status,
    @Default([]) List<Post> posts,
    Failure? failure,
  }) = _FeedState;
}

enum FeedStatus { initial, loading, success, failure }

sealed class FeedEffect {}
final class FeedShowSnack extends FeedEffect {
  FeedShowSnack(this.message);
  final String message;
}
```

## Anti-patterns to refuse

- Emitting from inside `setState` of a widget.
- Side-effects from `emit` (navigation, snackbars).
- Subclassing per state (`FeedLoading`, `FeedSuccess`, ...) — use
  the single Freezed class with a status enum instead.

## See also

- `clean-architecture`, `golden-tests`
