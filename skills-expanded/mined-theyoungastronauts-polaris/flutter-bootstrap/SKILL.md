---
name: flutter-bootstrap
description: "Scaffold a Flutter app (Riverpod, go_router, Dio, Freezed) paired with a Django backend."
disable-model-invocation: true
---

# Flutter Bootstrap

On-demand command for scaffolding a new Flutter app with Riverpod, Freezed, GoRouter, Dio, and a reference auth feature. Paired with a Django backend.

## Before You Start

Ask the user for these values (provide defaults where shown):

| Placeholder | Description | Example |
|-------------|-------------|---------|
| `{app_name}` | Flutter project name (snake_case) | `my_app` |
| `{app_title}` | Display name | `My App` |
| `{org}` | Organization identifier (reverse domain) | `com.example` |
| `{api_base_url}` | Backend API URL (default: `http://10.0.2.2:8000`) | `http://10.0.2.2:8000` |
| `{platforms}` | Target platforms (default: `ios,android`) | `ios,android,web` |

Note: `10.0.2.2` is the Android emulator alias for the host machine's localhost. For iOS simulator, use `http://localhost:8000`.

## Bootstrapping Steps

1. Check if puro is installed (`which puro`). If not, install it:
   ```bash
   curl -o- https://puro.dev/install.sh | bash
   ```
2. Create a puro environment for this project: `puro create {app_name} stable`
3. Run `puro -e {app_name} flutter create --org {org} --platforms {platforms} {app_name}`
4. `cd {app_name}` and pin the environment: `puro use {app_name}`
5. Replace the generated `lib/`, `pubspec.yaml`, `analysis_options.yaml`
6. Create `build.yaml` for Freezed/Riverpod codegen
7. Generate all files from templates below
8. Run `flutter pub get`
9. Run `dart run build_runner build --delete-conflicting-outputs`
10. Run `flutter run`

> **Note:** [puro](https://puro.dev/) manages per-project Flutter versions. The `puro use` command writes a `.purorc` file that pins this project to its environment. All `flutter` and `dart` commands automatically use the correct version when run from the project directory.

---

## Directory Structure

```
lib/
├── main.dart
├── config/
│   ├── env.dart
│   └── constants.dart
├── core/
│   ├── api/
│   │   └── dio_client.dart
│   ├── error/
│   │   └── failures.dart
│   ├── models/
│   │   └── paginated_response.dart
│   ├── router/
│   │   └── app_router.dart
│   ├── theme/
│   │   └── app_theme.dart
│   ├── providers/
│   │   └── session_provider.dart
│   ├── utils/
│   │   └── validation_utils.dart
│   └── widgets/
│       └── base_screen.dart
├── features/
│   └── auth/
│       ├── models/
│       │   ├── user.dart
│       │   └── session_token.dart
│       ├── services/
│       │   ├── auth_service.dart
│       │   └── auth_service_django.dart
│       ├── providers/
│       │   ├── auth_service_provider.dart
│       │   └── auth_provider.dart
│       ├── screens/
│       │   ├── login_screen.dart
│       │   └── register_screen.dart
│       └── widgets/
│           ├── login_form.dart
│           └── register_form.dart
test/
└── features/
    └── auth/
        └── auth_service_test.dart
```

---

## Project Config

### pubspec.yaml

```yaml
name: {app_name}
description: {app_title}
publish_to: 'none'
version: 1.0.0+1

environment:
  sdk: ^3.6.0

dependencies:
  flutter:
    sdk: flutter

  # State management (Riverpod: runtime pkgs are 3.x, codegen pkgs are 4.x)
  flutter_riverpod: ^3.3.2
  riverpod_annotation: ^4.0.3

  # Routing
  go_router: ^17.3.0

  # Networking
  dio: ^5.10.0

  # Models
  freezed_annotation: ^3.1.0
  json_annotation: ^4.9.0

  # Pagination
  infinite_scroll_pagination: ^5.1.1

  # Auth
  flutter_secure_storage: ^10.3.1
  jwt_decoder: ^2.0.0

  # UI
  cupertino_icons: ^1.0.0

dev_dependencies:
  flutter_test:
    sdk: flutter
  flutter_lints: ^5.0.0

  # Code generation
  build_runner: ^2.4.0
  freezed: ^3.2.5
  json_serializable: ^6.14.0
  riverpod_generator: ^4.0.4

  # Testing
  mocktail: ^1.0.0
```

### analysis_options.yaml

```yaml
include: package:flutter_lints/flutter.yaml

linter:
  rules:
    prefer_const_constructors: true
    prefer_const_declarations: true
    prefer_final_fields: true
    prefer_final_locals: true
    avoid_print: true
    require_trailing_commas: true
```

### build.yaml

```yaml
targets:
  $default:
    builders:
      freezed:
        options:
          format: true
      json_serializable:
        options:
          explicit_to_json: true
```

---

## File Templates

### lib/main.dart

```dart
import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';

import 'core/router/app_router.dart';
import 'core/theme/app_theme.dart';

void main() {
  WidgetsFlutterBinding.ensureInitialized();
  runApp(const ProviderScope(child: App()));
}

class App extends ConsumerWidget {
  const App({super.key});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final router = ref.watch(routerProvider);

    return MaterialApp.router(
      title: '{app_title}',
      theme: AppTheme.light(),
      darkTheme: AppTheme.dark(),
      debugShowCheckedModeBanner: false,
      routerConfig: router,
    );
  }
}
```

### lib/config/env.dart

```dart
class Env {
  // Host root only (scheme + host), e.g. https://api.example.com — request
  // paths carry the canonical `/api/v1/...` prefix, so don't include it here.
  static const String apiBaseUrl = String.fromEnvironment(
    'API_BASE_URL',
    defaultValue: '{api_base_url}',
  );

  static const bool debug = String.fromEnvironment(
    'DEBUG',
    defaultValue: 'true',
  ) == 'true';
}
```

### lib/config/constants.dart

```dart
class Constants {
  static const int defaultPaginationLimit = 20;
  static const Duration connectTimeout = Duration(seconds: 10);
  static const Duration receiveTimeout = Duration(seconds: 10);
}
```

---

## Core

### lib/core/error/failures.dart

```dart
sealed class Failure implements Exception {
  final String message;
  const Failure(this.message);

  @override
  String toString() => message;
}

class ServerFailure extends Failure {
  final int? statusCode;
  const ServerFailure(super.message, {this.statusCode});
}

class NetworkFailure extends Failure {
  const NetworkFailure([super.message = 'No internet connection']);
}

class AuthFailure extends Failure {
  const AuthFailure([super.message = 'Authentication failed']);
}

class ValidationFailure extends Failure {
  final Map<String, List<String>> fieldErrors;
  const ValidationFailure(
    super.message, {
    this.fieldErrors = const {},
  });
}
```

### lib/core/models/paginated_response.dart

```dart
class PaginatedResponse<T> {
  final int page;
  final int count;
  final int numPages;
  final List<T> results;

  const PaginatedResponse({
    required this.page,
    required this.count,
    required this.numPages,
    required this.results,
  });

  bool get canLoadMore => page < numPages;
}
```

### lib/core/api/dio_client.dart

```dart
import 'package:dio/dio.dart';
import 'package:flutter/foundation.dart';

import '../../config/constants.dart';
import '../../config/env.dart';
import '../../features/auth/models/session_token.dart';
import '../error/failures.dart';
import '../providers/session_provider.dart';

class DioClient {
  final Dio _dio;
  final Session _session;

  DioClient({required Session session})
      : _session = session,
        _dio = Dio(
          BaseOptions(
            baseUrl: Env.apiBaseUrl,
            connectTimeout: Constants.connectTimeout,
            receiveTimeout: Constants.receiveTimeout,
            headers: {
              'Content-Type': 'application/json',
              'Accept': 'application/json',
            },
          ),
        ) {
    _dio.interceptors.addAll([
      _authInterceptor(),
      if (kDebugMode) LogInterceptor(requestBody: true, responseBody: true),
    ]);
  }

  Interceptor _authInterceptor() {
    return InterceptorsWrapper(
      onRequest: (options, handler) async {
        final token = _session.token;
        if (token != null) {
          if (token.accessIsExpired && !token.refreshIsExpired) {
            try {
              final newToken = await _refreshToken(token.refresh);
              _session.setToken(newToken);
              options.headers['Authorization'] = 'Bearer ${newToken.access}';
            } on DioException {
              _session.clearToken();
              return handler.reject(
                DioException(requestOptions: options, type: DioExceptionType.cancel),
              );
            }
          } else if (!token.accessIsExpired) {
            options.headers['Authorization'] = 'Bearer ${token.access}';
          }
        }
        handler.next(options);
      },
      onError: (error, handler) {
        if (error.response?.statusCode == 401) {
          _session.clearToken();
        }
        handler.next(error);
      },
    );
  }

  Future<SessionToken> _refreshToken(String refreshToken) async {
    final response = await Dio(BaseOptions(baseUrl: _dio.options.baseUrl))
        .post('/api/v1/auth/refresh/', data: {'refresh': refreshToken});
    // Contract: refresh returns {access} only (rotation is off) — keep reusing
    // the current refresh token rather than expecting a new one back.
    return SessionToken(
      access: response.data['access'] as String,
      refresh: refreshToken,
    );
  }

  Future<Map<String, dynamic>> get(
    String path, {
    Map<String, dynamic>? queryParameters,
  }) async {
    try {
      final response = await _dio.get(path, queryParameters: queryParameters);
      return response.data;
    } on DioException catch (e) {
      throw _mapException(e);
    }
  }

  Future<Map<String, dynamic>> post(
    String path, {
    Map<String, dynamic>? data,
  }) async {
    try {
      final response = await _dio.post(path, data: data);
      return response.data;
    } on DioException catch (e) {
      throw _mapException(e);
    }
  }

  Future<Map<String, dynamic>> patch(
    String path, {
    Map<String, dynamic>? data,
  }) async {
    try {
      final response = await _dio.patch(path, data: data);
      return response.data;
    } on DioException catch (e) {
      throw _mapException(e);
    }
  }

  Future<void> delete(String path) async {
    try {
      await _dio.delete(path);
    } on DioException catch (e) {
      throw _mapException(e);
    }
  }

  Failure _mapException(DioException e) {
    if (e.type == DioExceptionType.connectionError ||
        e.type == DioExceptionType.connectionTimeout) {
      return const NetworkFailure();
    }
    final statusCode = e.response?.statusCode;
    final data = e.response?.data;
    if (statusCode == 401 || statusCode == 403) {
      return AuthFailure(data?['detail'] ?? 'Authentication failed');
    }
    if (statusCode == 400) {
      return ValidationFailure(
        data?['detail'] ?? 'Validation error',
        fieldErrors: _parseFieldErrors(data),
      );
    }
    return ServerFailure(
      data?['detail'] ?? 'Server error',
      statusCode: statusCode,
    );
  }

  Map<String, List<String>> _parseFieldErrors(dynamic data) {
    if (data is! Map<String, dynamic>) return {};
    final errors = <String, List<String>>{};
    for (final entry in data.entries) {
      if (entry.value is List) {
        errors[entry.key] = (entry.value as List).map((e) => e.toString()).toList();
      }
    }
    return errors;
  }
}
```

### lib/core/router/app_router.dart

```dart
import 'package:flutter/material.dart';
import 'package:go_router/go_router.dart';
import 'package:riverpod_annotation/riverpod_annotation.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';

import '../../features/auth/providers/auth_provider.dart';
import '../../features/auth/screens/login_screen.dart';
import '../../features/auth/screens/register_screen.dart';

part 'app_router.g.dart';

@riverpod
GoRouter router(Ref ref) {
  final auth = ref.watch(authProvider);

  return GoRouter(
    initialLocation: '/auth/login',
    redirect: (context, state) {
      final isLoggedIn = auth.valueOrNull != null;
      final isAuthRoute = state.matchedLocation.startsWith('/auth');

      if (!isLoggedIn && !isAuthRoute) return '/auth/login';
      if (isLoggedIn && isAuthRoute) return '/';
      return null;
    },
    routes: [
      GoRoute(
        path: '/auth/login',
        builder: (context, state) => const LoginScreen(),
      ),
      GoRoute(
        path: '/auth/register',
        builder: (context, state) => const RegisterScreen(),
      ),
      GoRoute(
        path: '/',
        builder: (context, state) => const Scaffold(
          body: Center(child: Text('Home — replace with your first feature')),
        ),
      ),
    ],
    errorPageBuilder: (context, state) => MaterialPage(
      child: Scaffold(
        body: Center(child: Text('404: ${state.error}')),
      ),
    ),
  );
}
```

### lib/core/theme/app_theme.dart

```dart
import 'package:flutter/material.dart';

class AppTheme {
  static ThemeData light() {
    return ThemeData(
      useMaterial3: true,
      colorScheme: ColorScheme.fromSeed(
        seedColor: Colors.blue,
        brightness: Brightness.light,
      ),
    );
  }

  static ThemeData dark() {
    return ThemeData(
      useMaterial3: true,
      colorScheme: ColorScheme.fromSeed(
        seedColor: Colors.blue,
        brightness: Brightness.dark,
      ),
    );
  }
}
```

### lib/core/providers/session_provider.dart

```dart
import 'package:flutter_secure_storage/flutter_secure_storage.dart';
import 'package:riverpod_annotation/riverpod_annotation.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';

import '../../features/auth/models/session_token.dart';

part 'session_provider.g.dart';

@riverpod
FlutterSecureStorage secureStorage(Ref ref) {
  return const FlutterSecureStorage();
}

@Riverpod(keepAlive: true)
class Session extends _$Session {
  @override
  SessionToken? build() => null;

  Future<void> initialize() async {
    final storage = ref.read(secureStorageProvider);
    final access = await storage.read(key: 'access_token');
    final refresh = await storage.read(key: 'refresh_token');
    if (access != null && refresh != null) {
      state = SessionToken(access: access, refresh: refresh);
    }
  }

  void setToken(SessionToken token) {
    state = token;
    final storage = ref.read(secureStorageProvider);
    storage.write(key: 'access_token', value: token.access);
    storage.write(key: 'refresh_token', value: token.refresh);
  }

  void clearToken() {
    state = null;
    final storage = ref.read(secureStorageProvider);
    storage.delete(key: 'access_token');
    storage.delete(key: 'refresh_token');
  }

  SessionToken? get token => state;
}
```

### lib/core/utils/validation_utils.dart

```dart
class ValidationUtils {
  static String? email(String? value) {
    if (value == null || value.isEmpty) return 'Email required';
    if (!RegExp(r'^.+@[a-zA-Z]+\.[a-zA-Z]+').hasMatch(value)) {
      return 'Invalid email';
    }
    return null;
  }

  static String? password(String? value) {
    if (value == null || value.isEmpty) return 'Password required';
    if (value.length < 8) return 'Password must be at least 8 characters';
    return null;
  }

  static String? required(String? value, String label) {
    if (value == null || value.isEmpty) return '$label required';
    return null;
  }
}
```

### lib/core/widgets/base_screen.dart

```dart
import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';

abstract class BaseScreen extends ConsumerWidget {
  final double horizontalPadding;
  final double verticalPadding;

  const BaseScreen({
    super.key,
    this.horizontalPadding = 16,
    this.verticalPadding = 8,
  });

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    return Scaffold(
      appBar: appBar(context, ref),
      floatingActionButton: floatingActionButton(context, ref),
      body: Padding(
        padding: EdgeInsets.symmetric(
          horizontal: horizontalPadding,
          vertical: verticalPadding,
        ),
        child: body(context, ref),
      ),
    );
  }

  AppBar? appBar(BuildContext context, WidgetRef ref) => null;

  FloatingActionButton? floatingActionButton(
    BuildContext context,
    WidgetRef ref,
  ) => null;

  Widget body(BuildContext context, WidgetRef ref) => const SizedBox.shrink();
}
```

---

## Auth Feature

### lib/features/auth/models/session_token.dart

```dart
import 'package:jwt_decoder/jwt_decoder.dart';

class SessionToken {
  final String access;
  final String refresh;

  const SessionToken({required this.access, required this.refresh});

  factory SessionToken.fromJson(Map<String, dynamic> json) {
    return SessionToken(access: json['access'], refresh: json['refresh']);
  }

  Map<String, dynamic> toJson() => {'access': access, 'refresh': refresh};

  bool get accessIsExpired => JwtDecoder.isExpired(access);
  bool get refreshIsExpired => JwtDecoder.isExpired(refresh);
}
```

### lib/features/auth/models/user.dart

```dart
import 'package:freezed_annotation/freezed_annotation.dart';

part 'user.freezed.dart';
part 'user.g.dart';

@freezed
abstract class User with _$User {
  const User._();

  factory User({
    required String uuid,
    required String email,
    String? username,
    @JsonKey(name: 'first_name') String? firstName,
    @JsonKey(name: 'last_name') String? lastName,
  }) = _User;

  factory User.fromJson(Map<String, dynamic> json) => _$UserFromJson(json);

  String get displayName {
    if (firstName != null && lastName != null) return '$firstName $lastName';
    if (firstName != null) return firstName!;
    return email;
  }
}
```

### lib/features/auth/services/auth_service.dart

```dart
import '../models/user.dart';

abstract class AuthService {
  Future<User> login({required String email, required String password});
  Future<User> register({
    required String email,
    required String username,
    required String password,
    required String firstName,
    required String lastName,
  });
  Future<User?> currentUser();
  Future<void> logout();
}
```

### lib/features/auth/services/auth_service_django.dart

```dart
import '../../../core/api/dio_client.dart';
import '../../../core/providers/session_provider.dart';
import '../models/session_token.dart';
import '../models/user.dart';
import 'auth_service.dart';

class AuthServiceDjango implements AuthService {
  final DioClient client;
  final Session session;

  AuthServiceDjango({required this.client, required this.session});

  @override
  Future<User> login({
    required String email,
    required String password,
  }) async {
    final result = await client.post(
      '/api/v1/auth/login/',
      data: {'email': email, 'password': password},
    );
    final token = SessionToken.fromJson(result);
    session.setToken(token);

    return currentUser().then((user) {
      if (user == null) throw Exception('Failed to fetch user after login');
      return user;
    });
  }

  @override
  Future<User> register({
    required String email,
    required String username,
    required String password,
    required String firstName,
    required String lastName,
  }) async {
    await client.post('/api/v1/auth/register/', data: {
      'username': username,
      'email': email,
      'password': password,
      'first_name': firstName,
      'last_name': lastName,
    });
    return login(email: email, password: password);
  }

  @override
  Future<User?> currentUser() async {
    if (session.token == null) return null;
    final result = await client.get('/api/v1/auth/me/');
    return User.fromJson(result);
  }

  @override
  Future<void> logout() async {
    session.clearToken();
  }
}
```

### lib/features/auth/providers/auth_service_provider.dart

```dart
import 'package:riverpod_annotation/riverpod_annotation.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';

import '../../../core/api/dio_client.dart';
import '../../../core/providers/session_provider.dart';
import '../services/auth_service.dart';
import '../services/auth_service_django.dart';

part 'auth_service_provider.g.dart';

@riverpod
DioClient dioClient(Ref ref) {
  final session = ref.watch(sessionProvider.notifier);
  return DioClient(session: session);
}

@riverpod
AuthService authService(Ref ref) {
  return AuthServiceDjango(
    client: ref.watch(dioClientProvider),
    session: ref.watch(sessionProvider.notifier),
  );
}
```

### lib/features/auth/providers/auth_provider.dart

```dart
import 'dart:async';

import 'package:riverpod_annotation/riverpod_annotation.dart';

import '../../../core/providers/session_provider.dart';
import '../models/user.dart';
import 'auth_service_provider.dart';

part 'auth_provider.g.dart';

@Riverpod(keepAlive: true)
class Auth extends _$Auth {
  @override
  FutureOr<User?> build() async {
    await ref.read(sessionProvider.notifier).initialize();
    if (ref.read(sessionProvider) == null) return null;
    return ref.read(authServiceProvider).currentUser();
  }

  Future<void> login({
    required String email,
    required String password,
  }) async {
    state = const AsyncLoading();
    state = await AsyncValue.guard(() async {
      return ref.read(authServiceProvider).login(
            email: email,
            password: password,
          );
    });
  }

  Future<void> register({
    required String email,
    required String username,
    required String password,
    required String firstName,
    required String lastName,
  }) async {
    state = const AsyncLoading();
    state = await AsyncValue.guard(() async {
      return ref.read(authServiceProvider).register(
            email: email,
            username: username,
            password: password,
            firstName: firstName,
            lastName: lastName,
          );
    });
  }

  Future<void> logout() async {
    await ref.read(authServiceProvider).logout();
    ref.read(sessionProvider.notifier).clearToken();
    state = const AsyncData(null);
  }
}
```

### lib/features/auth/screens/login_screen.dart

```dart
import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:go_router/go_router.dart';

import '../../../core/widgets/base_screen.dart';
import '../widgets/login_form.dart';

class LoginScreen extends BaseScreen {
  const LoginScreen({super.key});

  @override
  Widget body(BuildContext context, WidgetRef ref) {
    return Center(
      child: SingleChildScrollView(
        padding: const EdgeInsets.all(24),
        child: ConstrainedBox(
          constraints: const BoxConstraints(maxWidth: 400),
          child: Column(
            mainAxisAlignment: MainAxisAlignment.center,
            children: [
              Text(
                'Sign In',
                style: Theme.of(context).textTheme.headlineMedium?.copyWith(
                      fontWeight: FontWeight.bold,
                    ),
              ),
              const SizedBox(height: 32),
              const LoginForm(),
              const SizedBox(height: 16),
              TextButton(
                onPressed: () => context.go('/auth/register'),
                child: const Text("Don't have an account? Sign up"),
              ),
            ],
          ),
        ),
      ),
    );
  }
}
```

### lib/features/auth/screens/register_screen.dart

```dart
import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:go_router/go_router.dart';

import '../../../core/widgets/base_screen.dart';
import '../widgets/register_form.dart';

class RegisterScreen extends BaseScreen {
  const RegisterScreen({super.key});

  @override
  Widget body(BuildContext context, WidgetRef ref) {
    return Center(
      child: SingleChildScrollView(
        padding: const EdgeInsets.all(24),
        child: ConstrainedBox(
          constraints: const BoxConstraints(maxWidth: 400),
          child: Column(
            mainAxisAlignment: MainAxisAlignment.center,
            children: [
              Text(
                'Create Account',
                style: Theme.of(context).textTheme.headlineMedium?.copyWith(
                      fontWeight: FontWeight.bold,
                    ),
              ),
              const SizedBox(height: 32),
              const RegisterForm(),
              const SizedBox(height: 16),
              TextButton(
                onPressed: () => context.go('/auth/login'),
                child: const Text('Already have an account? Sign in'),
              ),
            ],
          ),
        ),
      ),
    );
  }
}
```

### lib/features/auth/widgets/login_form.dart

```dart
import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';

import '../../../core/error/failures.dart';
import '../../../core/utils/validation_utils.dart';
import '../providers/auth_provider.dart';

class LoginForm extends ConsumerStatefulWidget {
  const LoginForm({super.key});

  @override
  ConsumerState<LoginForm> createState() => _LoginFormState();
}

class _LoginFormState extends ConsumerState<LoginForm> {
  final _formKey = GlobalKey<FormState>();
  final _emailController = TextEditingController();
  final _passwordController = TextEditingController();
  bool _loading = false;
  String? _error;

  @override
  void dispose() {
    _emailController.dispose();
    _passwordController.dispose();
    super.dispose();
  }

  Future<void> _submit() async {
    if (!_formKey.currentState!.validate()) return;

    setState(() {
      _loading = true;
      _error = null;
    });

    try {
      await ref.read(authProvider.notifier).login(
            email: _emailController.text.trim(),
            password: _passwordController.text,
          );
    } on Failure catch (e) {
      setState(() => _error = e.message);
    } finally {
      if (mounted) setState(() => _loading = false);
    }
  }

  @override
  Widget build(BuildContext context) {
    return Form(
      key: _formKey,
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.stretch,
        children: [
          if (_error != null)
            Padding(
              padding: const EdgeInsets.only(bottom: 16),
              child: Text(
                _error!,
                style: TextStyle(color: Theme.of(context).colorScheme.error),
              ),
            ),
          TextFormField(
            controller: _emailController,
            validator: ValidationUtils.email,
            keyboardType: TextInputType.emailAddress,
            decoration: const InputDecoration(
              labelText: 'Email',
              border: OutlineInputBorder(),
            ),
          ),
          const SizedBox(height: 16),
          TextFormField(
            controller: _passwordController,
            validator: (v) => ValidationUtils.required(v, 'Password'),
            obscureText: true,
            decoration: const InputDecoration(
              labelText: 'Password',
              border: OutlineInputBorder(),
            ),
          ),
          const SizedBox(height: 24),
          FilledButton(
            onPressed: _loading ? null : _submit,
            child: _loading
                ? const SizedBox(
                    height: 20,
                    width: 20,
                    child: CircularProgressIndicator(strokeWidth: 2),
                  )
                : const Text('Sign In'),
          ),
        ],
      ),
    );
  }
}
```

### lib/features/auth/widgets/register_form.dart

```dart
import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';

import '../../../core/error/failures.dart';
import '../../../core/utils/validation_utils.dart';
import '../providers/auth_provider.dart';

class RegisterForm extends ConsumerStatefulWidget {
  const RegisterForm({super.key});

  @override
  ConsumerState<RegisterForm> createState() => _RegisterFormState();
}

class _RegisterFormState extends ConsumerState<RegisterForm> {
  final _formKey = GlobalKey<FormState>();
  final _emailController = TextEditingController();
  final _passwordController = TextEditingController();
  final _firstNameController = TextEditingController();
  final _lastNameController = TextEditingController();
  final _usernameController = TextEditingController();
  bool _loading = false;
  String? _error;

  @override
  void dispose() {
    _emailController.dispose();
    _passwordController.dispose();
    _firstNameController.dispose();
    _lastNameController.dispose();
    _usernameController.dispose();
    super.dispose();
  }

  Future<void> _submit() async {
    if (!_formKey.currentState!.validate()) return;

    setState(() {
      _loading = true;
      _error = null;
    });

    try {
      await ref.read(authProvider.notifier).register(
            email: _emailController.text.trim(),
            username: _usernameController.text.trim(),
            password: _passwordController.text,
            firstName: _firstNameController.text.trim(),
            lastName: _lastNameController.text.trim(),
          );
    } on Failure catch (e) {
      setState(() => _error = e.message);
    } finally {
      if (mounted) setState(() => _loading = false);
    }
  }

  @override
  Widget build(BuildContext context) {
    return Form(
      key: _formKey,
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.stretch,
        children: [
          if (_error != null)
            Padding(
              padding: const EdgeInsets.only(bottom: 16),
              child: Text(
                _error!,
                style: TextStyle(color: Theme.of(context).colorScheme.error),
              ),
            ),
          TextFormField(
            controller: _firstNameController,
            validator: (v) => ValidationUtils.required(v, 'First name'),
            decoration: const InputDecoration(
              labelText: 'First Name',
              border: OutlineInputBorder(),
            ),
          ),
          const SizedBox(height: 16),
          TextFormField(
            controller: _lastNameController,
            validator: (v) => ValidationUtils.required(v, 'Last name'),
            decoration: const InputDecoration(
              labelText: 'Last Name',
              border: OutlineInputBorder(),
            ),
          ),
          const SizedBox(height: 16),
          TextFormField(
            controller: _usernameController,
            validator: (v) => ValidationUtils.required(v, 'Username'),
            decoration: const InputDecoration(
              labelText: 'Username',
              border: OutlineInputBorder(),
            ),
          ),
          const SizedBox(height: 16),
          TextFormField(
            controller: _emailController,
            validator: ValidationUtils.email,
            keyboardType: TextInputType.emailAddress,
            decoration: const InputDecoration(
              labelText: 'Email',
              border: OutlineInputBorder(),
            ),
          ),
          const SizedBox(height: 16),
          TextFormField(
            controller: _passwordController,
            validator: ValidationUtils.password,
            obscureText: true,
            decoration: const InputDecoration(
              labelText: 'Password',
              border: OutlineInputBorder(),
            ),
          ),
          const SizedBox(height: 24),
          FilledButton(
            onPressed: _loading ? null : _submit,
            child: _loading
                ? const SizedBox(
                    height: 20,
                    width: 20,
                    child: CircularProgressIndicator(strokeWidth: 2),
                  )
                : const Text('Create Account'),
          ),
        ],
      ),
    );
  }
}
```

---

## Reference Test

### test/features/auth/auth_service_test.dart

```dart
import 'package:flutter_test/flutter_test.dart';
import 'package:mocktail/mocktail.dart';

import 'package:{app_name}/core/api/dio_client.dart';
import 'package:{app_name}/core/providers/session_provider.dart';
import 'package:{app_name}/features/auth/models/user.dart';
import 'package:{app_name}/features/auth/services/auth_service_django.dart';

class MockDioClient extends Mock implements DioClient {}

class MockSession extends Mock implements Session {}

void main() {
  late MockDioClient mockClient;
  late MockSession mockSession;
  late AuthServiceDjango authService;

  setUp(() {
    mockClient = MockDioClient();
    mockSession = MockSession();
    authService = AuthServiceDjango(client: mockClient, session: mockSession);
  });

  group('currentUser', () {
    test('returns null when no token', () async {
      when(() => mockSession.token).thenReturn(null);

      final user = await authService.currentUser();
      expect(user, isNull);
    });
  });
}
```

---

## .gitignore additions

Add these to the generated `.gitignore`:

```
# Freezed / Riverpod codegen
*.freezed.dart
*.g.dart
```

Note: Whether to commit generated files is a project-level choice. Excluding them keeps diffs clean but requires running `build_runner` after clone.

---

## Post-Bootstrap Checklist

1. `flutter create --org {org} --platforms {platforms} {app_name}`
2. Replace `lib/`, `pubspec.yaml`, `analysis_options.yaml` with templates above
3. Create `build.yaml`
4. `flutter pub get`
5. `dart run build_runner build --delete-conflicting-outputs`
6. `flutter run` — verify app launches with login screen
7. Connect to Django backend — verify login flow works
8. Commit initial scaffold

## After Bootstrap

For new features beyond auth, follow the patterns in `flutter-patterns.md`:
1. Create `features/{name}/` with `models/`, `services/`, `providers/`, `screens/`, `widgets/`
2. Add service interface + Django implementation
3. Wire up providers (service binding, list, detail, form)
4. Add routes to `app_router.dart`
5. Run `build_runner` after adding Freezed models or Riverpod providers
