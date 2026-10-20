---
name: "flutter"
description: "Build cross-platform mobile apps with Flutter and Dart"
---

# Flutter 3+

## When to activate
- Building Flutter applications for iOS, Android, web, or desktop
- Architecting state management with Riverpod 2
- Configuring navigation with go_router
- Implementing platform channels for native code integration
- Optimizing widget rebuild performance
- Running `flutter build` for production artifacts

## When NOT to use
- React Native, Expo, or other non-Flutter mobile frameworks
- Dart-only CLI tools or server-side Dart with no Flutter widgets
- When the question is about Xcode/Android Studio configuration unrelated to Flutter build tooling

## Instructions

### Widget Rebuild Optimization

Every `setState`, provider change, or inherited widget notification rebuilds the widget subtree. Minimize the blast radius:

**Lift state down.** Keep stateful widgets as close as possible to the UI that depends on them. A single top-level `StatefulWidget` rebuilds the entire tree.

**Use `const` constructors.** Widgets constructed with `const` are skipped during rebuild if their configuration hasn't changed.

```dart
// Good — these don't rebuild when parent rebuilds
const Text('Static label'),
const SizedBox(height: 16),
const Icon(Icons.star),
```

**Extract heavy subtrees.** Pull stable subtrees into their own widget class. Flutter skips unchanged widgets when their `==` returns true (automatic for `const` instances).

**Use `RepaintBoundary` for animations.** Wrap animated subtrees to isolate their GPU layer from the rest of the tree.

```dart
RepaintBoundary(
  child: AnimatedContainer(
    duration: const Duration(milliseconds: 300),
    width: _expanded ? 200 : 100,
    color: Colors.blue,
  ),
)
```

**Avoid building widgets inside `build` methods.** Functions that return widgets prevent Flutter from identifying unchanged subtrees. Use proper `Widget` classes or `Builder` pattern instead.

### Riverpod 2 Provider Types

| Provider | Use case |
|---|---|
| `Provider<T>` | Synchronous, read-only computed value or service |
| `FutureProvider<T>` | One-shot async value (loaded once, no mutation) |
| `StreamProvider<T>` | Continuous stream of values (WebSocket, Firestore) |
| `NotifierProvider<N, T>` | Synchronous mutable state with logic methods |
| `AsyncNotifierProvider<N, T>` | Async mutable state with loading/error/data |
| `StateProvider<T>` | Simple mutable value with no logic (quick UI state) |

```dart
// Provider — read-only service
final httpClientProvider = Provider<Dio>((ref) => Dio());

// FutureProvider — async fetch, no mutation
final userProvider = FutureProvider.family<User, int>((ref, id) async {
  final dio = ref.watch(httpClientProvider);
  final resp = await dio.get('/users/$id');
  return User.fromJson(resp.data);
});

// NotifierProvider — mutable state with methods
class CartNotifier extends Notifier<List<CartItem>> {
  @override
  List<CartItem> build() => [];

  void add(CartItem item) => state = [...state, item];
  void remove(String id) => state = state.where((i) => i.id != id).toList();
  void clear() => state = [];
}

final cartProvider = NotifierProvider<CartNotifier, List<CartItem>>(CartNotifier.new);

// AsyncNotifierProvider — async state with loading/error
class OrdersNotifier extends AsyncNotifier<List<Order>> {
  @override
  Future<List<Order>> build() => ref.read(orderRepoProvider).fetchAll();

  Future<void> refresh() async {
    state = const AsyncValue.loading();
    state = await AsyncValue.guard(() => ref.read(orderRepoProvider).fetchAll());
  }
}

final ordersProvider = AsyncNotifierProvider<OrdersNotifier, List<Order>>(OrdersNotifier.new);
```

In widgets, use `ref.watch` to rebuild on change, `ref.read` for one-off access in callbacks, `ref.listen` for side effects.

### go_router Route Definition

```dart
// lib/router.dart
final routerProvider = Provider<GoRouter>((ref) {
  final authState = ref.watch(authStateProvider);

  return GoRouter(
    initialLocation: '/home',
    debugLogDiagnostics: true,
    redirect: (context, state) {
      final isLoggedIn = authState.valueOrNull != null;
      final isAuthRoute = state.matchedLocation.startsWith('/auth');

      if (!isLoggedIn && !isAuthRoute) return '/auth/login';
      if (isLoggedIn && isAuthRoute) return '/home';
      return null;
    },
    routes: [
      GoRoute(
        path: '/auth/login',
        builder: (ctx, state) => const LoginScreen(),
      ),
      ShellRoute(
        builder: (ctx, state, child) => AppShell(child: child),
        routes: [
          GoRoute(
            path: '/home',
            builder: (ctx, state) => const HomeScreen(),
          ),
          GoRoute(
            path: '/orders',
            builder: (ctx, state) => const OrdersScreen(),
            routes: [
              GoRoute(
                path: ':id',
                builder: (ctx, state) {
                  final id = state.pathParameters['id']!;
                  return OrderDetailScreen(orderId: id);
                },
              ),
            ],
          ),
        ],
      ),
    ],
  );
});
```

Navigate:
```dart
context.go('/orders');           // replace history
context.push('/orders/42');      // push onto stack
context.pop();                   // go back
context.goNamed('order-detail', pathParameters: {'id': '42'});
```

### Platform Channel — MethodChannel Pattern

```dart
// lib/services/battery_service.dart
import 'package:flutter/services.dart';

class BatteryService {
  static const _channel = MethodChannel('com.example.app/battery');

  Future<int> getBatteryLevel() async {
    try {
      final level = await _channel.invokeMethod<int>('getBatteryLevel');
      return level ?? -1;
    } on PlatformException catch (e) {
      throw Exception('Failed to get battery level: ${e.message}');
    }
  }
}
```

```kotlin
// android/app/src/main/kotlin/com/example/app/MainActivity.kt
class MainActivity : FlutterActivity() {
    private val channel = "com.example.app/battery"

    override fun configureFlutterEngine(flutterEngine: FlutterEngine) {
        super.configureFlutterEngine(flutterEngine)
        MethodChannel(flutterEngine.dartExecutor.binaryMessenger, channel)
            .setMethodCallHandler { call, result ->
                if (call.method == "getBatteryLevel") {
                    val level = getBatteryLevel()
                    if (level != -1) result.success(level)
                    else result.error("UNAVAILABLE", "Battery not available", null)
                } else {
                    result.notImplemented()
                }
            }
    }

    private fun getBatteryLevel(): Int {
        val manager = getSystemService(BATTERY_SERVICE) as BatteryManager
        return manager.getIntProperty(BatteryManager.BATTERY_PROPERTY_CAPACITY)
    }
}
```

Use `EventChannel` for continuous streams (sensor data, location). Use `BasicMessageCodec` for binary data. Use method channels only for request/response patterns.

### flutter build Flags

```bash
# iOS — requires Xcode and valid provisioning profile
flutter build ios --release
flutter build ipa --release                           # .ipa for App Store / TestFlight
flutter build ipa --release --export-method app-store

# Android APK (direct install)
flutter build apk --release
flutter build apk --release --split-per-abi          # one APK per CPU architecture

# Android App Bundle (Play Store)
flutter build appbundle --release
flutter build appbundle --release --obfuscate --split-debug-info=./debug_info/

# Web
flutter build web --release --base-href /app/

# Common flags
flutter build appbundle \
  --release \
  --dart-define=ENVIRONMENT=production \
  --dart-define=API_URL=https://api.example.com \
  --obfuscate \
  --split-debug-info=./debug_symbols/
```

Use `--dart-define` to inject compile-time environment variables. Never store secrets in `--dart-define` for client apps — they are extractable from the binary.

## Example

A product listing screen using `AsyncNotifierProvider` and go_router navigation:

```dart
// Notifier
class ProductsNotifier extends AsyncNotifier<List<Product>> {
  @override
  Future<List<Product>> build() {
    return ref.read(productRepoProvider).fetchAll();
  }
}

final productsProvider =
    AsyncNotifierProvider<ProductsNotifier, List<Product>>(ProductsNotifier.new);

// Widget
class ProductsScreen extends ConsumerWidget {
  const ProductsScreen({super.key});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final products = ref.watch(productsProvider);

    return Scaffold(
      appBar: const AppBar(title: Text('Products')),
      body: switch (products) {
        AsyncData(:final value) => ListView.builder(
            itemCount: value.length,
            itemBuilder: (ctx, i) => ListTile(
              title: Text(value[i].name),
              onTap: () => context.push('/products/${value[i].id}'),
            ),
          ),
        AsyncError(:final error) => Center(child: Text('Error: $error')),
        _ => const Center(child: CircularProgressIndicator()),
      },
    );
  }
}
```

Build for production:
```bash
flutter build appbundle --release --obfuscate --split-debug-info=./debug/
```

---
