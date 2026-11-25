---
name: flutter-development
description: "Flutter pattern library: state management choices, const usage, a performance checklist, common failures, and full Riverpod, BLoC, CustomPainter, isolate, and rebuild-avoidance examples. Use when writing or reviewing Flutter code, picking state management, or chasing jank."
---

# Flutter development pattern library

## State management 2026 reference

| Library | Verdict |
|---|---|
| Riverpod 2.x | Default for new projects |
| BLoC | Solid if team prefers events/streams |
| Provider | Still fine; Riverpod's predecessor |
| GetX | Avoid; too magical |
| Redux | Overkill |
| `setState` | Widget-local only |

## Const cookbook

```dart
const SizedBox(height: 16),
const Divider(),
const Text('Static label'),

// Lints to enable:
// - prefer_const_constructors
// - prefer_const_literals_to_create_immutables
// - prefer_const_declarations
```

## Performance checklist

- `flutter run --profile` for real measurements
- ListView.builder over ListView(children:[...])
- AnimatedOpacity not Opacity
- compute() / isolates for parse/math
- const widgets aggressively
- Image.network with proper cacheWidth/cacheHeight
- Avoid saveLayer (Opacity, ShaderMask, ColorFilter cause it)

## Common failures

### "App is janky"
- Profile in profile mode (not debug)
- Check raster thread vs UI thread in DevTools
- Look for saveLayer triggers
- Move heavy parsing to compute() / isolate

### "Memory grows over time"
- Listeners not disposed (StreamSubscription, AnimationController)
- Images not evicted from cache
- Static references to BuildContext

### "Tests are flaky"
- Use `pumpAndSettle` for animations
- Mock time-dependent state
- WidgetTester.pump(duration) is more controllable than pumpAndSettle

## Platform integration

Pigeon for everything. Hand-coded MethodChannel for trivial calls only.

## Riverpod: StateNotifierProvider

```dart
import 'package:flutter_riverpod/flutter_riverpod.dart';

// State
@immutable
class CartState {
  final List<CartItem> items;
  final bool isLoading;

  const CartState({this.items = const [], this.isLoading = false});

  CartState copyWith({List<CartItem>? items, bool? isLoading}) => CartState(
    items: items ?? this.items,
    isLoading: isLoading ?? this.isLoading,
  );

  double get total => items.fold(0, (sum, item) => sum + item.price);
}

// Notifier
class CartNotifier extends StateNotifier<CartState> {
  CartNotifier(this._cartRepository) : super(const CartState());

  final CartRepository _cartRepository;

  Future<void> addItem(Product product) async {
    state = state.copyWith(isLoading: true);
    try {
      await _cartRepository.addToCart(product);
      state = state.copyWith(
        items: [...state.items, CartItem.fromProduct(product)],
        isLoading: false,
      );
    } catch (e) {
      state = state.copyWith(isLoading: false);
      rethrow;
    }
  }

  void removeItem(String itemId) {
    state = state.copyWith(
      items: state.items.where((item) => item.id != itemId).toList(),
    );
  }
}

// Provider
final cartProvider = StateNotifierProvider<CartNotifier, CartState>((ref) {
  return CartNotifier(ref.watch(cartRepositoryProvider));
});

// FutureProvider with family
final productProvider = FutureProvider.family<Product, String>((ref, id) {
  return ref.watch(productRepositoryProvider).getProduct(id);
});
```

### Using Riverpod in Widgets
```dart
class CartScreen extends ConsumerWidget {
  const CartScreen({super.key});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final cartState = ref.watch(cartProvider);

    // Listen for errors without rebuilding
    ref.listen(cartProvider, (prev, next) {
      if (next.isLoading == false && prev?.isLoading == true) {
        // Loading finished, show snackbar if needed
      }
    });

    return Stack(
      children: [
        ListView.builder(
          itemCount: cartState.items.length,
          itemBuilder: (context, index) {
            final item = cartState.items[index];
            return CartItemTile(
              item: item,
              onRemove: () => ref.read(cartProvider.notifier).removeItem(item.id),
            );
          },
        ),
        if (cartState.isLoading) const CircularProgressIndicator(),
      ],
    );
  }
}
```

---

## BLoC Pattern

```dart
// Events
abstract class AuthEvent {}
class LoginRequested extends AuthEvent {
  final String email;
  final String password;
  LoginRequested({required this.email, required this.password});
}
class LogoutRequested extends AuthEvent {}

// States
abstract class AuthState {}
class AuthInitial extends AuthState {}
class AuthLoading extends AuthState {}
class AuthAuthenticated extends AuthState { final User user; AuthAuthenticated(this.user); }
class AuthError extends AuthState { final String message; AuthError(this.message); }

// BLoC
class AuthBloc extends Bloc<AuthEvent, AuthState> {
  AuthBloc(this._authRepository) : super(AuthInitial()) {
    on<LoginRequested>(_onLoginRequested);
    on<LogoutRequested>(_onLogoutRequested);
  }

  final AuthRepository _authRepository;

  Future<void> _onLoginRequested(
    LoginRequested event, Emitter<AuthState> emit) async {
    emit(AuthLoading());
    try {
      final user = await _authRepository.login(event.email, event.password);
      emit(AuthAuthenticated(user));
    } on AuthException catch (e) {
      emit(AuthError(e.message));
    }
  }

  Future<void> _onLogoutRequested(
    LogoutRequested event, Emitter<AuthState> emit) async {
    await _authRepository.logout();
    emit(AuthInitial());
  }
}
```

### BLoC in Widget
```dart
class LoginScreen extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return BlocConsumer<AuthBloc, AuthState>(
      listener: (context, state) {
        if (state is AuthAuthenticated) {
          Navigator.of(context).pushReplacementNamed('/home');
        } else if (state is AuthError) {
          ScaffoldMessenger.of(context).showSnackBar(
            SnackBar(content: Text(state.message)),
          );
        }
      },
      builder: (context, state) {
        return Column(
          children: [
            if (state is AuthLoading) const LinearProgressIndicator(),
            LoginForm(
              onSubmit: (email, password) {
                context.read<AuthBloc>().add(
                  LoginRequested(email: email, password: password),
                );
              },
            ),
          ],
        );
      },
    );
  }
}
```

---

## CustomPainter

```dart
class WaveformPainter extends CustomPainter {
  final List<double> amplitudes;
  final Color color;

  WaveformPainter({required this.amplitudes, required this.color});

  @override
  void paint(Canvas canvas, Size size) {
    final paint = Paint()
      ..color = color
      ..strokeWidth = 2.0
      ..style = PaintingStyle.stroke
      ..strokeCap = StrokeCap.round;

    final path = Path();
    final stepX = size.width / (amplitudes.length - 1);

    for (int i = 0; i < amplitudes.length; i++) {
      final x = i * stepX;
      final y = size.height / 2 - amplitudes[i] * size.height / 2;

      if (i == 0) {
        path.moveTo(x, y);
      } else {
        final prevX = (i - 1) * stepX;
        final prevY = size.height / 2 - amplitudes[i - 1] * size.height / 2;
        final controlX = (prevX + x) / 2;
        path.cubicTo(controlX, prevY, controlX, y, x, y);
      }
    }

    canvas.drawPath(path, paint);
  }

  @override
  bool shouldRepaint(WaveformPainter old) =>
      old.amplitudes != amplitudes || old.color != color;
}

// Usage
CustomPaint(
  painter: WaveformPainter(amplitudes: samples, color: Colors.blue),
  size: const Size(double.infinity, 80),
)
```

---

## Isolate for Heavy Work

```dart
import 'dart:isolate';
import 'package:flutter/foundation.dart';

// Simple case: use compute()
Future<List<ProcessedItem>> processItems(List<RawItem> rawItems) async {
  return compute(_processInBackground, rawItems);
}

List<ProcessedItem> _processInBackground(List<RawItem> rawItems) {
  // Runs in separate isolate — no UI thread blocking
  return rawItems.map((item) => ProcessedItem.from(item)).toList();
}

// Complex case: long-lived isolate with bidirectional communication
Future<void> startBackgroundWorker() async {
  final receivePort = ReceivePort();
  await Isolate.spawn(_workerIsolate, receivePort.sendPort);

  receivePort.listen((message) {
    if (message is SendPort) {
      // Store sendPort to communicate back to isolate
    } else if (message is WorkResult) {
      // Handle result
    }
  });
}
```

---

## Performance: Avoiding Unnecessary Rebuilds

```dart
// Bad: rebuilds entire widget tree
Consumer(
  builder: (context, ref, child) {
    final entireState = ref.watch(bigStateProvider);
    return ExpensiveWidget(value: entireState.oneField);
  },
)

// Good: watch only the specific value needed
Consumer(
  builder: (context, ref, child) {
    final oneField = ref.watch(bigStateProvider.select((s) => s.oneField));
    return ExpensiveWidget(value: oneField);
  },
)

// Good: const widgets skip rebuild entirely
const Padding(
  padding: EdgeInsets.all(16),
  child: Text('Static label'),
)

// Good: RepaintBoundary isolates expensive CustomPaint
RepaintBoundary(
  child: CustomPaint(painter: ComplexChartPainter(data: data)),
)
```

---

## Cross-references
- `mobile-architecture` for MVVM/BLoC/clean
- `mobile-performance` for profiling
- `mobile-testing` for test strategy
- `mobile-ci-cd` for build automation
