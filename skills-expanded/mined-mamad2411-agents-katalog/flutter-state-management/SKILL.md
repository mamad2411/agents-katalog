---
name: flutter-state-management
category: architecture
description: Use when a Flutter screen needs app state or data - separate presentation from state, keep business logic out of widgets, and follow the app's existing state solution (Riverpod 3 Notifier/AsyncNotifier, or the official ChangeNotifier+ListenableBuilder MVVM pattern)
tech_stack: Flutter
---
# Flutter State Management

## Overview

Widgets render state; something else owns it. Keeping business logic and data out of the widget tree is what makes Flutter screens testable and rebuilds cheap.

**Core principle:** Follow the app's existing state solution (Riverpod, Bloc, Provider, etc.) — do not introduce a second one. The pattern matters more than the library.

## Rules (library-agnostic)

- **One source of truth per piece of state**, owned by a controller/notifier/bloc — never duplicated across widgets via `setState`.
- **Presentation ↔ state via a thin interface:** the widget watches state and sends events/intents; it never contains the business rule or the network call.
- **`StatefulWidget` is for ephemeral UI only** (animation controllers, focus, scroll) — anything that outlives a rebuild or comes from a service is app state.
- **Handle all async states explicitly:** loading, data, empty, error. A `FutureBuilder`/`AsyncValue` that only renders the happy path ships a spinner-forever bug.
- **Dispose** controllers/subscriptions to avoid leaks.
- **Immutable state objects** (copyWith) so rebuilds are diff-friendly and predictable.

## Worked Example — Riverpod 3 (`Notifier`/`AsyncNotifier`, not `StateNotifier`)

`StateNotifier`/`StateNotifierProvider`/`StateProvider`/`ChangeNotifierProvider` are legacy as of Riverpod 3 — use `Notifier`/`AsyncNotifier` in new code. If the repo still uses `StateNotifier`, follow it; don't migrate existing code on your own initiative.

```dart
// state owner: no widgets, pure logic — unit-testable without pumping a widget
class TaskListNotifier extends AsyncNotifier<List<Task>> {
  @override
  Future<List<Task>> build() => ref.read(taskRepositoryProvider).list();

  Future<void> reload() async {
    state = const AsyncLoading();
    state = await AsyncValue.guard(() => ref.read(taskRepositoryProvider).list());
  }
}

final taskListProvider = AsyncNotifierProvider<TaskListNotifier, List<Task>>(TaskListNotifier.new);

// widget: watches state, renders each case, sends intents — no logic
ref.watch(taskListProvider).when(
  loading: () => const AppSpinner(),
  error:   (e, _) => AppErrorView(message: e.toString(), onRetry: () => ref.read(taskListProvider.notifier).reload()),
  data:    (tasks) => tasks.isEmpty ? const EmptyView() : TaskList(tasks: tasks),
);
```

## Alternative — official Flutter MVVM (`ChangeNotifier` + `ListenableBuilder`)

Flutter's own architecture guide and the `flutter-apply-architecture-best-practices` skill teach this pattern when the app has no state-management package at all:

```dart
class TaskListViewModel extends ChangeNotifier {
  TaskListViewModel(this._repo);
  final TaskRepository _repo;
  List<Task>? _tasks;
  Object? _error;
  bool _loading = false;

  List<Task>? get tasks => _tasks;
  Object? get error => _error;
  bool get loading => _loading;

  Future<void> load() async {
    _loading = true; _error = null; notifyListeners();
    try { _tasks = await _repo.list(); }
    catch (e) { _error = e; }
    finally { _loading = false; notifyListeners(); }
  }
}

ListenableBuilder(
  listenable: viewModel,
  builder: (context, _) => switch (viewModel) {
    _ when viewModel.loading => const AppSpinner(),
    _ when viewModel.error != null => AppErrorView(message: '${viewModel.error}', onRetry: viewModel.load),
    _ => TaskList(tasks: viewModel.tasks ?? const []),
  },
)
```

Pick one pattern per app and stay consistent with what's already there — don't introduce a second state-management approach into a repo that already has one.

## Common Mistakes

- Business logic / http calls inside `build` or `initState`.
- `setState` juggling data that came from an API.
- Introducing a new state library alongside the app's existing one.
- Ignoring the error/empty branch of an async state.
- Leaked controllers (no `dispose`).

## Red Flags

- A widget imports an http client or repository directly.
- The same state mirrored in two widgets.
- An async view with no error handling.
