---
name: get-it-di
description: How get_it is wired in this Flutter project — feature-level registration modules, scopes, factory vs singleton, testing with pushNewScope rather than allowReassignment. Load when adding a new injectable, creating a DI module, writing DI-aware tests, or debugging a get_it error.
---

# get_it DI

Feature-level modules, one root composer, scopes in tests.

## Root entry point

```dart
// core/di/container.dart
final GetIt sl = GetIt.instance;

Future<void> initializeDependencies({required Flavor flavor}) async {
  _registerCore(sl, flavor: flavor);
  await _registerDatabase(sl);
  _registerFirebase(sl);

  // Features — each module is colocated with the feature code
  registerAuthModule(sl);
  registerActivityModule(sl);
  registerTodayModule(sl);
  registerSettingsModule(sl);
  // ...
}
```

- Called once from `app_initializer.dart` at app start.
- Order matters: register dependencies **before** their dependents.
- Async registrations (database open, secure storage init) use `registerSingletonAsync` and are awaited in `allReady()` if needed.

## Feature module

```dart
// feature/auth/di/auth_module.dart
void registerAuthModule(GetIt sl) {
  // data layer
  sl.registerLazySingleton<AuthRepository>(
    () => AuthRepositoryImpl(
      api: sl(),
      secureStorage: sl(),
      logger: sl(),
    ),
  );

  // presentation layer
  sl.registerFactory<AuthBloc>(
    () => AuthBloc(
      authRepository: sl(),
      logger: sl(),
    ),
  );
}
```

Rules:
- **Singletons** for repositories, services, DAOs, loggers, the logger, the API client wrapper — anything stateful and shared.
- **Factories** for blocs, cubits, use cases. Fresh instance per request.
- **Interface binding.** Always `registerLazySingleton<Interface>(...)`, not the impl type.
- Don't reach across feature modules. A module registers what it owns and consumes from `core/`.

## Scopes (for tests, overlays, sub-flows)

`GetIt` supports stacked scopes. This is the right tool for:
- Tests (push scope in `setUp`, pop in `tearDown`).
- Authenticated-session services that should only exist while logged in (push on login, pop on logout).
- Nested sub-flows with their own lifetimes.

```dart
// login
sl.pushNewScope(scopeName: 'authenticated');
sl.registerLazySingleton<UserProfileRepository>(() => UserProfileRepositoryImpl(...));

// logout
sl.popScopesTill('authenticated');   // removes that scope and above
```

## Resolving dependencies in code

- **Constructor injection** is the default. Classes take dependencies as parameters; GetIt wires them once at the composition root.
- **`context.read<T>()` / `context.watch<T>()`** for blocs/cubits provided by `BlocProvider`. This is how widgets see state.
- **`sl<T>()` is acceptable at the composition edge** — specifically, inside a `BlocProvider.create:` callback in a `<Feature>Page`.
- **Never** call `sl<T>()` inside `build()`, `initState()`, or a widget callback. That's a service locator anti-pattern.

```dart
// ok
BlocProvider<AuthBloc>(create: (_) => sl<AuthBloc>(), child: const LoginView());

// not ok
@override
Widget build(BuildContext context) {
  final bloc = sl<AuthBloc>(); // <-- no
  ...
}
```

## Tests — do this

```dart
setUp(() {
  GetIt.I.pushNewScope(scopeName: 'test');
  GetIt.I.registerLazySingleton<AuthRepository>(() => FakeAuthRepository());
  GetIt.I.registerLazySingleton<ILogger>(() => NoopLogger());
});

tearDown(() {
  GetIt.I.popScope();
});
```

Rules:
- **Never `allowReassignment = true`.** That's a leaky global that hides test interference.
- **Prefer not using GetIt in tests at all.** Construct the class under test with its fakes directly. Use scopes only when a component you can't reach depends on GetIt internally.

## Common errors

- **`Object of type X is not registered inside GetIt`** — the module isn't called, or you registered the concrete class but asked for the interface.
- **`Type X is already registered inside GetIt`** — you pushed a scope and forgot to pop, or you registered twice in the same scope.
- **Factory returning stale state** — you registered a bloc as `registerLazySingleton` instead of `registerFactory`. Blocs almost always want factory.
- **Async registration not ready** — awaited `sl.allReady()` missing after bootstrapping.

## Why not move to Riverpod?

Valid question, addressed elsewhere (see the project-level architecture notes). For this codebase, keep `get_it`. Riverpod would replace DI + state + caching in one stroke — it's a bigger change than it sounds.

## Hard nos

- `sl<T>()` inside `build`.
- `allowReassignment = true` in tests.
- Registering concrete classes and resolving them by concrete type — register the interface.
- Circular dependencies at registration time. If two things need each other, one of them is misdesigned.
