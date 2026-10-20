---
name: bloc-patterns
description: "When to activate: flutter_bloc, BLoC, Cubit, BlocBuilder, BlocListener, BlocConsumer, HydratedBloc, events, states, bloc pattern"
origin: zakr
metadata:
  namespace: zakr/devtools-pack
  version: 1.0.0
  category: engineering
  language: dart
  platforms: [claude-code, codex, gemini-cli, cursor, aider, windsurf]
---
# BLoC Patterns

## Cubit (simple state, no events)

```dart
class CounterCubit extends Cubit<int> {
  CounterCubit() : super(0);
  void increment() => emit(state + 1);
  void decrement() => emit(state - 1);
  void reset() => emit(0);
}

// Widget
BlocProvider(
  create: (_) => CounterCubit(),
  child: BlocBuilder<CounterCubit, int>(
    builder: (context, count) => Text('$count'),
  ),
);
context.read<CounterCubit>().increment();
```

## BLoC with Sealed Events and States

```dart
// events.dart
sealed class AuthEvent {}
class LoginRequested extends AuthEvent {
  final String email, password;
  LoginRequested(this.email, this.password);
}
class LogoutRequested extends AuthEvent {}
class TokenRefreshRequested extends AuthEvent {}

// states.dart
sealed class AuthState {}
class AuthInitial extends AuthState {}
class AuthLoading extends AuthState {}
class AuthAuthenticated extends AuthState {
  final User user;
  AuthAuthenticated(this.user);
}
class AuthFailure extends AuthState {
  final String message;
  AuthFailure(this.message);
}

// bloc.dart
class AuthBloc extends Bloc<AuthEvent, AuthState> {
  AuthBloc(this._authService) : super(AuthInitial()) {
    on<LoginRequested>(_onLogin);
    on<LogoutRequested>(_onLogout);
  }

  final AuthService _authService;

  Future<void> _onLogin(LoginRequested event, Emitter<AuthState> emit) async {
    emit(AuthLoading());
    try {
      final user = await _authService.login(event.email, event.password);
      emit(AuthAuthenticated(user));
    } catch (e) {
      emit(AuthFailure(e.toString()));
    }
  }

  Future<void> _onLogout(LogoutRequested event, Emitter<AuthState> emit) async {
    await _authService.logout();
    emit(AuthInitial());
  }
}
```

## BlocBuilder, BlocListener, BlocConsumer

```dart
// BlocBuilder: rebuild on state change
BlocBuilder<AuthBloc, AuthState>(
  buildWhen: (prev, curr) => prev.runtimeType != curr.runtimeType, // skip same-type rebuilds
  builder: (context, state) => switch (state) {
    AuthLoading() => const CircularProgressIndicator(),
    AuthAuthenticated(:final user) => HomeScreen(user: user),
    AuthFailure(:final message) => ErrorWidget(message),
    _ => const LoginScreen(),
  },
);

// BlocListener: side effects (navigation, snackbars) — no rebuild
BlocListener<AuthBloc, AuthState>(
  listener: (context, state) {
    if (state is AuthFailure) {
      ScaffoldMessenger.of(context).showSnackBar(SnackBar(content: Text(state.message)));
    }
    if (state is AuthAuthenticated) {
      context.go('/home');
    }
  },
  child: const LoginForm(),
);

// BlocConsumer: both rebuild and side effects
BlocConsumer<AuthBloc, AuthState>(
  listener: (context, state) { /* side effects */ },
  builder: (context, state) => /* UI */ const SizedBox(),
);
```

## MultiBlocProvider and MultiBlocListener

```dart
MultiBlocProvider(
  providers: [
    BlocProvider(create: (_) => AuthBloc(authService)),
    BlocProvider(create: (ctx) => CartBloc()),
    BlocProvider(create: (ctx) => NotificationBloc()),
  ],
  child: const AppShell(),
);

MultiBlocListener(
  listeners: [
    BlocListener<AuthBloc, AuthState>(listener: (ctx, s) { ... }),
    BlocListener<CartBloc, CartState>(listener: (ctx, s) { ... }),
  ],
  child: const Scaffold(),
);
```

## HydratedBloc (persisted state)

```dart
void main() async {
  WidgetsFlutterBinding.ensureInitialized();
  HydratedBloc.storage = await HydratedStorage.build(
    storageDirectory: await getApplicationDocumentsDirectory(),
  );
  runApp(const MyApp());
}

class ThemeCubit extends HydratedCubit<ThemeMode> {
  ThemeCubit() : super(ThemeMode.system);

  void setTheme(ThemeMode mode) => emit(mode);

  @override
  ThemeMode fromJson(Map<String, dynamic> json) =>
      ThemeMode.values.byName(json['mode'] as String);

  @override
  Map<String, dynamic>? toJson(ThemeMode state) => {'mode': state.name};
}
```

## Bloc-to-Bloc Communication

```dart
// Option 1: Using stream subscription
class CartBloc extends Bloc<CartEvent, CartState> {
  CartBloc(AuthBloc authBloc) : super(CartInitial()) {
    on<CartLoadRequested>(_onLoad);
    // React to auth changes
    _authSubscription = authBloc.stream.listen((authState) {
      if (authState is AuthInitial) add(CartClearRequested());
    });
  }
  late StreamSubscription _authSubscription;

  @override
  Future<void> close() {
    _authSubscription.cancel();
    return super.close();
  }
}

// Option 2: With Riverpod wrapping BLoC
```

## Testing BLoC

```dart
import 'package:bloc_test/bloc_test.dart';

void main() {
  group('AuthBloc', () {
    late AuthBloc bloc;
    late MockAuthService mockService;

    setUp(() {
      mockService = MockAuthService();
      bloc = AuthBloc(mockService);
    });

    tearDown(() => bloc.close());

    blocTest<AuthBloc, AuthState>(
      'emits [Loading, Authenticated] on successful login',
      build: () {
        when(() => mockService.login(any(), any()))
            .thenAnswer((_) async => fakeUser);
        return AuthBloc(mockService);
      },
      act: (bloc) => bloc.add(LoginRequested('test@test.com', 'pass')),
      expect: () => [isA<AuthLoading>(), isA<AuthAuthenticated>()],
    );

    blocTest<AuthBloc, AuthState>(
      'emits [Loading, Failure] on login error',
      build: () {
        when(() => mockService.login(any(), any())).thenThrow(Exception('Bad credentials'));
        return AuthBloc(mockService);
      },
      act: (bloc) => bloc.add(LoginRequested('x', 'y')),
      expect: () => [isA<AuthLoading>(), isA<AuthFailure>()],
    );
  });
}
```
