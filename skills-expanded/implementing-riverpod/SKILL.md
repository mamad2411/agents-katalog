---
name: "implementing-riverpod"
description: "Implements Riverpod (v3.3.x) compile-safe state management for Flutter apps. Use when implementing @riverpod code generation providers, handling AsyncValue loading/error/data states, using ref.watch/ref.read/ref.listen, setting up ProviderScope, writing Notifier/AsyncNotifier classes, using FutureProvider/StreamProvider, applying autoDispose and family modifiers, combining providers, testing providers in isolation, scoping rebuilds with Consumer instead of ConsumerWidget, using ref.watch with select() for field-level precision, migrating from StateNotifierProvider or Riverpod 2.x patterns, handling Notifier resource lifecycle with ref.onDispose, or using experimental Mutation and offline persistence APIs."
metadata:
  last_modified: "2026-04-27 17:41:00 (GMT+8)"
---

# Riverpod State Management (v3.3.x)

## Goal
Implement compile-time safe, context-free state management using Riverpod. Use `@riverpod` code generation for all new code — the generator handles auto-dispose, family, and type safety automatically.

## Process

### Phase 1: Install Dependencies

**Code Generation (Recommended)**:
```yaml
dependencies:
  flutter_riverpod: ^3.5.0
  riverpod_annotation: ^4.0.8

dev_dependencies:
  build_runner: ^2.17.1
  riverpod_generator: ^4.0.10
  # riverpod_lint is not compatible with riverpod_generator 4.0.8+ (analyzer conflict); see the lint variant below
```

**Manual only** (no code generation):
```yaml
dependencies:
  flutter_riverpod: ^3.5.0
```

> **Lint variant (verified with `dart pub get` on Flutter 3.47.9):** `riverpod_lint` and `custom_lint` cannot be combined with `riverpod_generator` 4.0.8+. `riverpod_generator` 4.0.0+1 still resolves with `riverpod_lint` 3.1.0 (verified). Use this set when you need lint rules:
> ```yaml
> flutter_riverpod: ^3.0.3
> riverpod_annotation: ^3.0.3
> riverpod_generator: ^3.0.3
> riverpod_lint: ^3.0.3
> custom_lint: ^0.8.1
> build_runner: ^2.15.1   # 2.16+ needs analyzer 14, which conflicts with custom_lint
> freezed: ^3.2.3
> json_serializable: ^6.11.2
> ```

### Phase 2: Setup ProviderScope

```dart
void main() {
  runApp(ProviderScope(child: MyApp()));
}
```

### Phase 3: Create Providers

**Notifier (synchronous mutable state)**:
```dart
part 'counter.g.dart';

@riverpod
class Counter extends _$Counter {
  @override
  int build() => 0;

  void increment() => state++;
  void decrement() => state--;
}
// Generated: counterProvider
```

**AsyncNotifier (async mutable state)**:
```dart
@riverpod
class TodoList extends _$TodoList {
  @override
  Future<List<Todo>> build() async => fetchTodos();

  Future<void> addTodo(String title) async {
    state = const AsyncValue.loading();
    state = await AsyncValue.guard(() async {
      final todo = await apiClient.createTodo(title);
      return [...await future, todo];
    });
  }
}
// Generated: todoListProvider
```

**FutureProvider with auto-retry**:
```dart
@Riverpod(retry: myRetryStrategy)
Future<User> userProfile(Ref ref, String userId) async {
  return fetchUser(userId);
}

Duration? myRetryStrategy(int retryCount, Object error) {
  if (retryCount >= 5) return null;
  return Duration(milliseconds: 200 * (1 << retryCount));
}
```

→ See [riverpod.md](./references/riverpod.md) for manual providers, testing, Mutations, and offline persistence.

### Phase 4: Consume Providers

**Prefer `Consumer` to scope rebuilds to the smallest subtree.** `ConsumerWidget` rebuilds the entire widget on every state change; `Consumer` rebuilds only its `builder`.

```dart
// Preferred: only Text rebuilds when count changes
class HomeScreen extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: Consumer(
        builder: (context, ref, _) {
          final count = ref.watch(counterProvider);
          return Text('Count: $count');
        },
      ),
      floatingActionButton: FloatingActionButton(
        // ref.read in callbacks — never ref.watch
        onPressed: () => ProviderScope.containerOf(context)
            .read(counterProvider.notifier)
            .increment(),
        child: const Icon(Icons.add),
      ),
    );
  }
}
```

Use `ConsumerWidget` only when the **entire** widget tree depends on provider state:

```dart
class CounterPage extends ConsumerWidget {
  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final count = ref.watch(counterProvider);
    return Scaffold(
      appBar: AppBar(title: Text('Count: $count')),
      body: CounterBody(count: count),
      floatingActionButton: FloatingActionButton(
        onPressed: () => ref.read(counterProvider.notifier).increment(),
        child: const Icon(Icons.add),
      ),
    );
  }
}
```

Use `ref.watch(provider.select((s) => s.field))` to rebuild only when a specific field changes:

```dart
Consumer(
  builder: (context, ref, _) {
    // Only rebuilds when isLoggedIn changes, ignoring other User fields
    final isLoggedIn = ref.watch(authProvider.select((u) => u.isLoggedIn));
    return isLoggedIn ? const HomeView() : const LoginView();
  },
)
```

Use `HookConsumerWidget` when combining with `flutter_hooks`. Use `ref.listen` for side-effects (snackbars, navigation) without triggering rebuilds.

→ See [riverpod.md](./references/riverpod.md#consumer-vs-consumerwidget) for detailed Consumer vs ConsumerWidget decision table and `select()` patterns.

### Phase 5: Handle Async States

```dart
Widget build(BuildContext context, WidgetRef ref) {
  final userAsync = ref.watch(userProfileProvider('u1'));

  return userAsync.when(
    data: (user) => Text('Hello, ${user.name}'),
    loading: () => const CircularProgressIndicator(),
    error: (e, st) => Text('Error: $e'),
  );
}
```

→ See [PITFALLS.md](./references/PITFALLS.md) for `AsyncValue` best practices and optimistic UI with `copyWithPrevious`.

### Phase 6: Provider Dependencies

```dart
@riverpod
Future<List<Post>> userPosts(Ref ref, String userId) async {
  final user = await ref.watch(userProfileProvider(userId).future);
  return fetchPostsForUser(user.id);
}
```

→ See [PITFALLS.md](./references/PITFALLS.md) for `ref.mounted` checks, memory leak prevention, and `ref.read` vs `ref.watch` rules.

---

## Reference Documentation

- [Riverpod Patterns (v3.x)](./references/riverpod.md) — Code generation, manual providers, testing, experimental Mutations and persistence
- [Common Pitfalls](./references/PITFALLS.md) — `ref.mounted`, memory leaks, `ref.read` vs `ref.watch`, AsyncValue patterns
- [State Management Overview](./references/state-management-overview.md) — ChangeNotifier/Provider decision guide

---

## Constraints

- **No BuildContext in providers**: Access state via `ref` only.
- **Compile-time safety**: Use `@riverpod` code generation; catches errors at build time.
- **Immutable state**: Keep state immutable; use Freezed for complex models. v3.0 uses `==` for all state comparisons — implement `operator ==` or use Freezed.
- **Auto-dispose by default**: Code-gen providers auto-dispose unless marked `keepAlive: true`.
- **Ref lifecycle**: Never store `ref` in a variable or pass it outside provider scope.
- **AsyncValue.guard**: Always wrap async state mutations in `AsyncValue.guard()`.
- **⚠️ ref.mounted**: Always check `ref.mounted` after `await` before updating state.
- **⚠️ ref.onDispose**: Cancel timers, streams, and HTTP requests in `ref.onDispose`.
- **⚠️ ref.read in callbacks**: Use `ref.read` in event handlers; `ref.watch` only in `build()`.
- **⚠️ Notifier resource leak (v3.0)**: Notifier creates fresh instances on every rebuild — never store timers or controllers directly inside a Notifier. Extract to a dedicated `Provider` with `ref.onDispose`.
- **Scoped rebuilds**: Prefer `Consumer` over `ConsumerWidget`; use `select()` for field-level precision.
