---
name: flutter-state-management
description: Chooses between Riverpod and Bloc for a Flutter feature, implements it cleanly and covers the logic and widgets with tests.
---

# Flutter state management

Follow the project's existing choice. Introduce a second state library only if the user asks.

## Steps

1. Read `pubspec.yaml` and two existing features. Note which of `flutter_riverpod`, `flutter_bloc`, `provider` is in use and how files are laid out.
2. If nothing is in use, choose by need. Riverpod fits derived and cached async data, dependency injection and many small independent states. Bloc fits event-driven flows with strict transitions, such as multi-step forms, auth and payments, where an event log is valuable. Say which you chose and why in two sentences.
3. Model state as an immutable type with explicit cases: initial, loading, data, failure. Use a sealed class or freezed. Never a bag of nullable fields plus a boolean `isLoading`.
4. Riverpod: use `AsyncNotifier` or `Notifier`, read with `ref.watch` in `build`, use `ref.read` only in callbacks, and use `select` to narrow rebuilds. Bloc: one event class per user intent, one `on<Event>` handler each, emit only from handlers, and close subscriptions in `close()`.
5. Keep widgets thin. They render state and send events or call notifier methods. No repository calls, no `BuildContext` inside logic.
6. Tests: unit test the notifier with a `ProviderContainer` and overrides, or the bloc with `bloc_test`. Add widget tests that pump each state and check the visible result.
7. Run `dart format`, `flutter analyze` and `flutter test`.

## Rules

- Dispose controllers and cancel streams.
- Never call `notifyListeners` or emit after dispose.
- No global mutable singletons for state.

## Report

The library chosen and the reason, files added or changed, and test results.
