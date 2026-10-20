---
name: riverpod-patterns
description: "When to activate: Riverpod, Provider, StateNotifier, AsyncNotifier, ref.watch, ref.listen, ref.read, family, keepAlive, flutter_riverpod"
origin: zakr
metadata:
  namespace: zakr/devtools-pack
  version: 1.0.0
  category: engineering
  language: dart
  platforms: [claude-code, codex, gemini-cli, cursor, aider, windsurf]
---
# Riverpod Patterns

## Provider Types

```dart
// Simple sync value
final greetingProvider = Provider<String>((ref) => 'Hello');

// Mutable state (sync)
final counterProvider = StateProvider<int>((ref) => 0);

// Async data
final userProvider = FutureProvider.family<User, String>((ref, userId) async {
  final repo = ref.watch(userRepositoryProvider);
  return repo.fetchUser(userId);
});

// Stream-based
final messagesProvider = StreamProvider<List<Message>>((ref) {
  return ref.watch(chatServiceProvider).messageStream();
});
```

## StateNotifier (pre-Notifier API)

```dart
class CounterNotifier extends StateNotifier<int> {
  CounterNotifier() : super(0);

  void increment() => state++;
  void decrement() => state--;
  void reset() => state = 0;
}

final counterNotifierProvider = StateNotifierProvider<CounterNotifier, int>(
  (ref) => CounterNotifier(),
);
```

## Notifier API (Riverpod 2+)

```dart
// Sync Notifier
@riverpod
class Counter extends _$Counter {
  @override
  int build() => 0;
  void increment() => state++;
}

// Async Notifier
@riverpod
class UserList extends _$UserList {
  @override
  Future<List<User>> build() => ref.watch(userRepoProvider).fetchAll();

  Future<void> addUser(User user) async {
    state = const AsyncLoading();
    state = await AsyncValue.guard(() async {
      await ref.read(userRepoProvider).addUser(user);
      return ref.read(userRepoProvider).fetchAll();
    });
  }
}
```

## ref.watch vs ref.read vs ref.listen

```dart
class MyWidget extends ConsumerWidget {
  @override
  Widget build(BuildContext context, WidgetRef ref) {
    // watch: subscribe to changes, rebuild on update
    final count = ref.watch(counterProvider);

    // read: one-time access, no subscription (use in callbacks)
    return ElevatedButton(
      onPressed: () => ref.read(counterProvider.notifier).increment(),
      child: Text('$count'),
    );
  }
}

// listen: side effects on state change (navigation, snackbars)
class AuthWidget extends ConsumerStatefulWidget {
  @override
  ConsumerState<AuthWidget> createState() => _AuthWidgetState();
}

class _AuthWidgetState extends ConsumerState<AuthWidget> {
  @override
  void initState() {
    super.initState();
    ref.listenManual(authProvider, (prev, next) {
      if (next == AuthState.loggedOut) {
        Navigator.of(context).pushReplacementNamed('/login');
      }
    });
  }
}
```

## Family Modifier

```dart
// Parameterized providers
final userProvider = FutureProvider.family<User, String>((ref, id) async {
  return ref.watch(repoProvider).getUser(id);
});

// Usage in widget
final user = ref.watch(userProvider('user-123'));

// With custom param type (must implement ==  and hashCode)
@freezed
class UserFilter with _$UserFilter {
  const factory UserFilter({required String role, required bool active}) = _UserFilter;
}

final filteredUsersProvider = FutureProvider.family<List<User>, UserFilter>(
  (ref, filter) => ref.watch(repoProvider).getUsers(filter),
);
```

## keepAlive and autoDispose

```dart
// autoDispose: provider disposes when no longer watched (default with @riverpod)
@riverpod
Future<User> currentUser(CurrentUserRef ref) async {
  // Keeps alive for 5 min after last subscriber leaves
  final link = ref.keepAlive();
  Timer(const Duration(minutes: 5), link.close);
  return fetchCurrentUser();
}

// Manual keepAlive
final cacheProvider = FutureProvider.autoDispose<Data>((ref) async {
  ref.keepAlive(); // never auto-disposes after first load
  return fetchData();
});
```

## AsyncValue Handling

```dart
// In build method
final asyncUser = ref.watch(userProvider('123'));
return asyncUser.when(
  data: (user) => Text(user.name),
  loading: () => const CircularProgressIndicator(),
  error: (e, st) => Text('Error: $e'),
);

// withPrevious: show stale data while refreshing
return asyncUser.when(
  skipLoadingOnRefresh: true,
  data: (user) => Text(user.name),
  loading: () => const CircularProgressIndicator(),
  error: (e, st) => Text('Error: $e'),
);
```

## Provider Overrides for Testing

```dart
void main() {
  testWidgets('shows user name', (tester) async {
    await tester.pumpWidget(
      ProviderScope(
        overrides: [
          userProvider.overrideWith((ref) => Future.value(User(name: 'Test'))),
        ],
        child: const MyApp(),
      ),
    );
    expect(find.text('Test'), findsOneWidget);
  });
}
```

## Combining Providers

```dart
final searchResultsProvider = FutureProvider<List<Product>>((ref) async {
  final query = ref.watch(searchQueryProvider);
  final filters = ref.watch(activeFiltersProvider);
  if (query.isEmpty) return [];
  return ref.watch(productRepoProvider).search(query, filters);
});
```
