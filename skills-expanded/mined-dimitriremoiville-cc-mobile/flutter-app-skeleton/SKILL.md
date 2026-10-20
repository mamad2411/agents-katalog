---
name: flutter-app-skeleton
description: Canonical blueprint for scaffolding a brand-new Flutter app in this project's style — full pubspec, folder layout, base classes (Failure, DioFactory, GetIt container, AppDatabase), analysis_options, flavor setup, and test helpers. Load when initializing a new Flutter app or when you need the authoritative starting files. The `/init-flutter-app` command drives this skill end to end.
---

# Flutter app skeleton

This skill is the source of truth for what a new Flutter app looks like on day 0. Every file below is meant to be written as-is (with the placeholders swapped). Nothing in here is stack-agnostic — it's opinionated for this project's conventions (`flutter_bloc` + `get_it` + `dio` + `drift` + `fpdart` + `freezed` + typed `go_router`).

Use via `/init-flutter-app`. The command handles the user interaction; this skill holds the templates.

## Companion files (load conditionally)

The core templates (pubspec, folder layout, `core/`, `routing/`, `shared/`, tests) live in this file. Flag-conditional extensions live in sibling files — load only the ones matching the user's flags to keep context focused:

- `INCLUDE_DRIFT` → [_drift.md](./_drift.md)
- `INCLUDE_FIREBASE` → [_firebase.md](./_firebase.md)
- `INCLUDE_NOTIFICATIONS` → [_notifications.md](./_notifications.md)
- `INCLUDE_WORKMANAGER` → [_workmanager.md](./_workmanager.md)

## Placeholders

Throughout the templates, replace:

- `{{APP_NAME}}` — the Dart package name, `snake_case` (e.g., `my_app`).
- `{{APP_CLASS}}` — `UpperCamelCase` version used in class names (e.g., `MyApp`).
- `{{ORG_DOMAIN}}` — reverse-domain organization identifier (e.g., `com.example.app`).
- `{{APP_DISPLAY_NAME}}` — human-readable app name (e.g., `My App`).
- Feature flags (`INCLUDE_DRIFT`, `INCLUDE_FIREBASE`, `INCLUDE_NOTIFICATIONS`, `INCLUDE_WORKMANAGER`) — include/exclude the corresponding blocks.

## Execution order

Do these in order. Skip the optional steps the user opted out of.

1. **Run `flutter create`** to get platform folders.
2. **Seed `pubspec.yaml`** with the non-dependency shell, then use `dart pub add` for every dependency. Do not hardcode versions from this skill — `pub add` picks the current compatible version at runtime. Verify against the floor-constraint table after.
3. **Overwrite `analysis_options.yaml`**.
4. **Write `build.yaml`** for codegen config.
5. **Delete `lib/main.dart`** and the default `test/widget_test.dart`.
6. **Write the `lib/` tree** (templates follow).
7. **Write `test/helpers/`**.
8. **Run `flutter pub get`**.
9. **Run `dart run build_runner build --delete-conflicting-outputs`**.
10. **Run `dart analyze --fatal-infos --fatal-warnings`** and fix anything the skeleton tripped.
11. **Report the manual Android / iOS flavor steps** — those require Xcode + Gradle edits the CLI shouldn't do automatically.

## Step 1 — `flutter create` (foundation)

The scaffold is **always layered on top of `flutter create`'s output**, never invented from scratch. Flutter's CLI owns the platform folder structure (`android/`, `ios/`, gradle wrapper, xcodeproj, asset registration, Info.plist defaults, podfile, manifest). Re-implementing that by hand is brittle: Flutter SDK updates routinely tweak these files, and any hand-rolled skeleton would fall out of sync within a release or two. Running `flutter create` first means the scaffold inherits the canonical project shape for whatever SDK the user has installed; the rest of this skill only overlays the `lib/`, `test/`, and config files we care about.

```bash
flutter create \
  --template=app \
  --org {{ORG_DOMAIN}} \
  --project-name {{APP_NAME}} \
  --platforms=android,ios \
  .
```

Flags that matter:

- `--template=app` — the default, but pinned explicitly so the intent is unambiguous (not `package`, not `plugin`, not `module`). If the user later wants a Flutter module embedded in a native host, they should run `/init-flutter-app` separately and pass `--template=module` themselves; this scaffold is app-shaped.
- `--platforms=android,ios` — restrict to mobile. Adding `web`, `windows`, `linux`, `macos` here would scaffold those platform folders too, all of which would need their own flavor configuration, signing, icon, splash, and CI plumbing this skill doesn't cover. Keeping the surface small at init time means the user can run `flutter create --platforms=web .` later to add a single platform deliberately, rather than maintaining six.
- `--org {{ORG_DOMAIN}}` — controls the reverse-DNS namespace used by Android (`applicationId`) and iOS (`PRODUCT_BUNDLE_IDENTIFIER`). This is the single hardest thing to change after the fact, so the user is asked for it in Phase 0.

(If the directory already has files, run in an empty subfolder or accept the overwrite warnings — but the `/init-flutter-app` command should have already bailed in that case during Phase 0's directory-state check.)

## Step 2 — `pubspec.yaml`

**Do not hardcode versions in this skill.** Versions drift; a skill pinned to "latest as of today" is a ticking clock. Instead:

1. Write the non-dependency scaffold of `pubspec.yaml` (name, description, environment, flutter assets block — shown below).
2. Add dependencies with `dart pub add` — the resolver picks the current compatible version, and pub writes a real caret constraint into the final `pubspec.yaml`. That pin lives in the generated project, not in this skill.
3. Verify the resolved versions respect the **floor constraints** listed below. If any resolves lower than the floor (e.g. the user has an older Flutter pinning them back), stop and surface it to the user.

### 2a — Seed `pubspec.yaml`

Overwrite the `flutter create` output with this shell (no dependencies yet):

```yaml
name: {{APP_NAME}}
description: "{{APP_DISPLAY_NAME}}"
publish_to: 'none'
version: 0.1.0+1

environment:
  sdk: ">=3.8.0 <4.0.0"
  flutter: ">=3.35.0"

dependencies:
  flutter:
    sdk: flutter
  flutter_localizations:
    sdk: flutter

dev_dependencies:
  flutter_test:
    sdk: flutter

flutter:
  uses-material-design: true
  generate: true
  assets:
    - assets/images/
    - assets/icons/
```

### 2b — Add dependencies

Run these `dart pub add` commands from the project root. Group them as shown so the final `pubspec.yaml` groups read well; pub preserves insertion order.

```bash
# Core Flutter extras
dart pub add cupertino_icons intl

# State management
dart pub add flutter_bloc bloc_concurrency formz

# DI
dart pub add get_it

# Routing (typed)
dart pub add go_router

# Functional / error model
dart pub add fpdart

# Immutability & codegen annotations
dart pub add freezed_annotation json_annotation

# Networking
dart pub add dio connectivity_plus

# Storage (secure + simple)
dart pub add flutter_secure_storage shared_preferences path_provider path

# Utilities
dart pub add logging package_info_plus device_info_plus uuid crypto url_launcher clock
```

Optional blocks — run only if the flag is on:

```bash
# INCLUDE_DRIFT — note: sqlcipher_flutter_libs provides BOTH SQLite + encryption.
#                 Do NOT also add sqlite3_flutter_libs; it will conflict.
dart pub add drift sqlite3 sqlcipher_flutter_libs

# INCLUDE_FIREBASE
dart pub add firebase_core firebase_analytics firebase_crashlytics firebase_remote_config

# INCLUDE_NOTIFICATIONS
dart pub add flutter_local_notifications timezone flutter_timezone app_settings

# INCLUDE_WORKMANAGER
dart pub add workmanager
```

Dev dependencies:

```bash
# Testing
dart pub add --dev bloc_test mocktail fake_async

# Goldens — pick one at init time
dart pub add --dev alchemist          # default
# or:
dart pub add --dev golden_toolkit

# Codegen
dart pub add --dev build_runner freezed json_serializable go_router_builder

# INCLUDE_DRIFT
dart pub add --dev drift_dev

# Lints
dart pub add --dev flutter_lints
```

### 2c — Compatibility traps (no fixed versions — describes the symptom + fix)

`dart pub add` already resolves to the latest stable that satisfies the Flutter SDK constraints, so the templates **never** pin numbers. The traps below are the failure modes you'll recognize when the resolved set isn't compatible — they describe the symptom and the fix without naming a specific version that would age.

| Trap | Symptom | Fix |
|---|---|---|
| **Pre-typed-routes go_router** | `Undefined name '$appRoutes'` / `Undefined class 'TypedGoRoute'`. | The typed-route generator (`@TypedGoRoute`) lives in modern `go_router`. If the resolver landed an older major, bump the SDK floor (the user's Flutter is too old) or upgrade `go_router` explicitly. |
| **freezed v2 vs v3 sealed-class output** | Generated files use `mixin _$Foo` instead of `sealed class _$Foo` and exhaustive switch fails. | freezed v3+ generates Dart-3 sealed unions. If the resolver lands v2, the rest of the templates won't pattern-match exhaustively. Bump `freezed` major. |
| **drift / drift_dev majors mismatched** | `incompatible drift_dev` resolver error or runtime "schema version mismatch". | The two must share a major. `dart pub add drift drift_dev` in one command keeps them aligned; if you add separately, verify with `dart pub deps`. |
| **mocktail still null-unsafe** | `Null check used on a null value` from `when()` setups. | Pre-1.0 mocktail has the old API. Bump major. |
| **intl resolver lock** | `dart pub add intl` refuses, or pulls a version below what Flutter ships. | Never `any` — pin the caret constraint of whatever `flutter pub deps` reports for `intl`. The Flutter SDK bundles a constraint; defer to it. |
| **sqlcipher + sqlite3_flutter_libs collision** | Native build fails with "duplicate symbol _sqlite3_*". | These two ship the same SQLite native binary. Pick one. The skill uses `sqlcipher_flutter_libs` (it provides BOTH SQLite + encryption); never add `sqlite3_flutter_libs` alongside it. |
| **fpdart pre-1.0 renames** | `Either.right(...)` works, then later `Right(...)` doesn't. | Pre-1.0 fpdart had different names. Bump major. |
| **get_it scope API missing** | `pushNewScope` / `popScope` undefined in tests. | Old get_it doesn't have scopes. Test helpers in this skill rely on them. Bump major. |

If `dart pub add` refuses a package because of SDK constraints, do **not** work around it by lowering a floor or pinning down. Surface the resolver output and stop — the user's Flutter SDK is the cap, and they should bump that, not retreat to older packages.

### 2d — Rule of thumb

**Do not edit `pubspec.yaml` by hand inside this skill.** `dart pub add` is the source of truth for versions. If you must hand-edit (e.g. to change a group comment), do it after `pub add` has written the entries.

Do remind the user: never use `intl: any`. If they later add `intl` themselves, use a caret constraint.

## Step 2.5 — Verify the Flutter SDK floor (online)

`dart pub add` resolves all pub.dev packages live, so the only thing the user's local environment can pin too low is the **Flutter SDK itself**. The compatibility traps above all assume Flutter ≥ 3.35 (Dart ≥ 3.8) — Dart 3 sealed classes, exhaustive switch, and modern `intl` all need it.

Two checks, in order:

1. **Local check.** Run `flutter --version` and parse the first line (`Flutter <X.Y.Z> ...`). If `<X.Y.Z>` is below the floor in `environment.flutter` from the seed `pubspec.yaml` above, stop and ask the user to upgrade. Don't lower the floor.
2. **Online sanity check (only if you can't read local — e.g. the user is on a sandbox).** `WebFetch` `https://storage.googleapis.com/flutter_infra_release/releases/releases_macos.json` (or `_linux.json` / `_windows.json`) and pull `current_release.stable` → look up that hash in `releases[]` to find the stable version string. Use that as a "known good" reference; report if the user's local Flutter is more than one minor version behind.

The goal is to surface "your Flutter is too old" *before* `dart pub add` tries 30 packages and fails on each one in confusing ways.

```yaml
include: package:flutter_lints/flutter.yaml

analyzer:
  exclude:
    - "**/*.g.dart"
    - "**/*.freezed.dart"
    - "lib/l10n/**"
    - "**/*.gr.dart"
  errors:
    # Promote a few patterns to errors — catch at CI time.
    unused_import: error
    dead_code: error
    missing_required_param: error
    missing_return: error

linter:
  rules:
    always_use_package_imports: true
    avoid_print: true
    cancel_subscriptions: true
    close_sinks: true
    prefer_const_constructors: true
    prefer_const_literals_to_create_immutables: true
    prefer_final_locals: true
    omit_local_variable_types: true
    unawaited_futures: true
    use_build_context_synchronously: true
    require_trailing_commas: true
    sort_pub_dependencies: false   # we group by purpose, not alphabetically
```

## Step 4 — `build.yaml`

```yaml
targets:
  $default:
    builders:
      freezed:
        options:
          copy_with: true
          equal: true
      json_serializable:
        options:
          explicit_to_json: true
          create_factory: true
          create_to_json: true
      go_router_builder:
        generate_for:
          - lib/routing/**.dart
```

## Step 5 — `lib/` tree

Create the folder skeleton first (empty folders get a `.gitkeep`), then write the seed files below.

```
lib/
├── main_dev.dart
├── main_prod.dart
├── app_initializer.dart
├── {{APP_NAME}}_app.dart
├── core/
│   ├── analytics/                         # always emitted (interface + Noop impl)
│   │   ├── i_analytics_tracker.dart
│   │   ├── analytics_event.dart
│   │   ├── noop_analytics_tracker.dart
│   │   └── firebase_analytics_tracker.dart    # only if INCLUDE_FIREBASE
│   ├── auth/
│   │   └── auth_token_provider.dart
│   ├── config/
│   │   ├── app_config.dart
│   │   └── flavor.dart
│   ├── database/                          # only if INCLUDE_DRIFT
│   │   ├── app_database.dart
│   │   └── executor.dart
│   ├── di/
│   │   └── container.dart
│   ├── errors/
│   │   └── failures.dart
│   ├── logging/
│   │   ├── i_logger.dart
│   │   └── app_logger.dart
│   ├── network/
│   │   ├── api_call_error_handling.dart
│   │   └── dio_factory.dart
│   └── notifications/                     # only if INCLUDE_NOTIFICATIONS
│       └── .gitkeep
├── feature/
│   └── home/                              # bottom-nav shell + Feed/Profile tabs
│       ├── di/
│       │   └── home_module.dart
│       └── presentation/
│           ├── pages/
│           │   ├── home_shell_page.dart
│           │   ├── feed_page.dart
│           │   └── profile_page.dart
│           └── bloc/
│               ├── feed_bloc.dart
│               ├── feed_event.dart
│               ├── feed_state.dart
│               ├── profile_bloc.dart
│               ├── profile_event.dart
│               └── profile_state.dart
├── l10n/
│   └── app_en.arb
├── routing/
│   └── app_router.dart
└── shared/
    ├── theme/
    │   ├── app_theme.dart
    │   └── app_spacing.dart
    └── widgets/
        └── .gitkeep
```

### `lib/main_dev.dart`

```dart
import 'package:flutter/material.dart';
import 'package:{{APP_NAME}}/app_initializer.dart';
import 'package:{{APP_NAME}}/core/config/flavor.dart';
import 'package:{{APP_NAME}}/{{APP_NAME}}_app.dart';

Future<void> main() async {
  WidgetsFlutterBinding.ensureInitialized();
  await AppInitializer.initialize(flavor: Flavor.dev);
  runApp(const {{APP_CLASS}}App());
}
```

### `lib/main_prod.dart`

```dart
import 'package:flutter/material.dart';
import 'package:{{APP_NAME}}/app_initializer.dart';
import 'package:{{APP_NAME}}/core/config/flavor.dart';
import 'package:{{APP_NAME}}/{{APP_NAME}}_app.dart';

Future<void> main() async {
  WidgetsFlutterBinding.ensureInitialized();
  await AppInitializer.initialize(flavor: Flavor.prod);
  runApp(const {{APP_CLASS}}App());
}
```

### `lib/app_initializer.dart`

```dart
import 'package:flutter/foundation.dart';
import 'package:{{APP_NAME}}/core/analytics/i_analytics_tracker.dart';
import 'package:{{APP_NAME}}/core/config/app_config.dart';
import 'package:{{APP_NAME}}/core/config/flavor.dart';
import 'package:{{APP_NAME}}/core/di/container.dart';

abstract final class AppInitializer {
  static Future<void> initialize({required Flavor flavor}) async {
    AppConfig.init(flavor: flavor);
    // INCLUDE_FIREBASE:
    //   await Firebase.initializeApp(options: DefaultFirebaseOptions.currentPlatform);
    //   FlutterError.onError = FirebaseCrashlytics.instance.recordFlutterFatalError;
    await initializeDependencies(flavor: flavor);

    // Toggle analytics collection. No-op without Firebase; with Firebase it
    // gates Crashlytics + Analytics so debug installs don't pollute prod
    // dashboards. The toggle goes through the IAnalyticsTracker interface so
    // this file never imports firebase_*.
    await sl<IAnalyticsTracker>().setCollectionEnabled(!kDebugMode);
  }
}
```

### `lib/{{APP_NAME}}_app.dart`

```dart
import 'package:flutter/material.dart';
import 'package:flutter_localizations/flutter_localizations.dart';
import 'package:{{APP_NAME}}/core/di/container.dart';
import 'package:{{APP_NAME}}/routing/app_router.dart';
import 'package:{{APP_NAME}}/shared/theme/app_theme.dart';

class {{APP_CLASS}}App extends StatelessWidget {
  const {{APP_CLASS}}App({super.key});

  @override
  Widget build(BuildContext context) => MaterialApp.router(
        title: '{{APP_DISPLAY_NAME}}',
        theme: AppTheme.light(),
        darkTheme: AppTheme.dark(),
        themeMode: ThemeMode.system,
        routerConfig: sl<AppRouter>().config,
        localizationsDelegates: const [
          GlobalMaterialLocalizations.delegate,
          GlobalWidgetsLocalizations.delegate,
          GlobalCupertinoLocalizations.delegate,
        ],
        supportedLocales: const [Locale('en')],
      );
}
```

### `lib/core/config/flavor.dart`

```dart
enum Flavor { dev, prod }

extension FlavorX on Flavor {
  bool get isDev => this == Flavor.dev;
  bool get isProd => this == Flavor.prod;
}
```

### `lib/core/config/app_config.dart`

```dart
import 'package:{{APP_NAME}}/core/config/flavor.dart';

class AppConfig {
  AppConfig._({required this.flavor, required this.apiBaseUrl, required this.isDebug});

  final Flavor flavor;
  final String apiBaseUrl;
  final bool isDebug;

  static AppConfig? _instance;
  static AppConfig get current {
    final value = _instance;
    if (value == null) throw StateError('AppConfig not initialized. Call AppConfig.init() first.');
    return value;
  }

  static void init({required Flavor flavor}) {
    _instance = AppConfig._(
      flavor: flavor,
      apiBaseUrl: switch (flavor) {
        Flavor.dev => const String.fromEnvironment('API_BASE_URL', defaultValue: 'https://dev.api.example.com'),
        Flavor.prod => const String.fromEnvironment('API_BASE_URL', defaultValue: 'https://api.example.com'),
      },
      isDebug: flavor.isDev,
    );
  }
}
```

### `lib/core/errors/failures.dart`

```dart
sealed class Failure {
  const Failure({required this.message, this.code, this.rootCause, this.stackTrace});
  final String message;
  final String? code;
  final Object? rootCause;
  final StackTrace? stackTrace;

  @override
  String toString() => '$runtimeType($message${code == null ? '' : ', code: $code'})';
}

final class NetworkFailure extends Failure {
  const NetworkFailure({super.message = 'Network error', super.rootCause, super.stackTrace});
}

final class ServerFailure extends Failure {
  const ServerFailure({required super.message, super.code, super.rootCause, super.stackTrace});
}

final class AuthFailure extends Failure {
  const AuthFailure({super.message = 'Unauthorized', super.code, super.rootCause, super.stackTrace});
}

final class NotFoundFailure extends Failure {
  const NotFoundFailure({required super.message, super.code});
}

final class ValidationFailure extends Failure {
  const ValidationFailure({required super.message, this.fields = const {}})
      : super(code: 'validation');
  final Map<String, String> fields;
}

final class CacheFailure extends Failure {
  const CacheFailure({required super.message, super.rootCause, super.stackTrace});
}

final class CancelledFailure extends Failure {
  const CancelledFailure() : super(message: 'Cancelled');
}

final class RateLimitFailure extends Failure {
  const RateLimitFailure({required this.retryAfter}) : super(message: 'Rate limited');
  final Duration retryAfter;
}

final class UnknownFailure extends Failure {
  const UnknownFailure({required super.message, super.rootCause, super.stackTrace});
}
```

### `lib/core/analytics/i_analytics_tracker.dart`

Cross-cutting interface. Cubits/Blocs depend on this, never on `firebase_analytics` directly. The taxonomy lives in a sealed `AnalyticsEvent` next door so every event lands in one grep-able place — magic strings sprinkled across screens are how analytics dashboards quietly drift.

```dart
import 'package:{{APP_NAME}}/core/analytics/analytics_event.dart';

abstract interface class IAnalyticsTracker {
  Future<void> track(AnalyticsEvent event);
  Future<void> setUserProperty(String key, String? value);
  /// Toggle collection at runtime (debug builds default off — see AppInitializer).
  Future<void> setCollectionEnabled(bool enabled);
}
```

### `lib/core/analytics/analytics_event.dart`

Sealed taxonomy. Add new events as `final class` entries here — never as raw strings at call sites. Names are snake_case (Firebase + most backends prefer it) and parameters are primitive-only (the intersection of what every backend can serialize without a custom mapper).

```dart
sealed class AnalyticsEvent {
  const AnalyticsEvent({required this.name, this.params = const {}});
  final String name;
  final Map<String, Object?> params;
}

final class HomeViewed extends AnalyticsEvent {
  const HomeViewed() : super(name: 'home_viewed');
}

final class FeedViewed extends AnalyticsEvent {
  const FeedViewed() : super(name: 'feed_viewed');
}

final class ProfileViewed extends AnalyticsEvent {
  const ProfileViewed() : super(name: 'profile_viewed');
}

final class ItemTapped extends AnalyticsEvent {
  ItemTapped({required String itemId})
      : super(name: 'item_tapped', params: {'item_id': itemId});
}

final class ScreenOpenedFromDeepLink extends AnalyticsEvent {
  ScreenOpenedFromDeepLink({required String route})
      : super(name: 'deep_link_open', params: {'route': route});
}
```

### `lib/core/analytics/noop_analytics_tracker.dart`

Always emitted. Null-Object implementation — used by default and when `INCLUDE_FIREBASE=false`. Lets every Cubit/Bloc inject `IAnalyticsTracker` unconditionally; no `if (analyticsEnabled)` branches at call sites.

```dart
import 'package:{{APP_NAME}}/core/analytics/analytics_event.dart';
import 'package:{{APP_NAME}}/core/analytics/i_analytics_tracker.dart';

class NoopAnalyticsTracker implements IAnalyticsTracker {
  const NoopAnalyticsTracker();

  @override
  Future<void> track(AnalyticsEvent event) async {}

  @override
  Future<void> setUserProperty(String key, String? value) async {}

  @override
  Future<void> setCollectionEnabled(bool enabled) async {}
}
```

> The `FirebaseAnalyticsTracker` impl lives in [`_firebase.md`](./_firebase.md). It uses the same interface and is bound in `container.dart` only under `INCLUDE_FIREBASE`. It is **defensive against an uninitialized FirebaseApp** — i.e. it silently no-ops until `flutterfire configure` produces a real `firebase_options.dart` and the user drops the per-flavor JSON/plist. That way the scaffold runs end-to-end immediately and starts emitting events automatically once Firebase is wired up.

### `lib/core/auth/auth_token_provider.dart`

```dart
abstract interface class AuthTokenProvider {
  Future<String?> currentToken();
  Future<String?> refresh();
  Future<void> clear();
  Stream<AuthFailureReason> get failureStream;
}

enum AuthFailureReason { refreshFailed, revokedToken, unknown }
```

### `lib/core/logging/i_logger.dart`

```dart
abstract interface class ILogger {
  void debug(String message, {Object? error, StackTrace? stackTrace});
  void info(String message, {Object? error, StackTrace? stackTrace});
  void warn(String message, {Object? error, StackTrace? stackTrace});
  void error(String message, {Object? error, StackTrace? stackTrace});
}
```

### `lib/core/logging/app_logger.dart`

```dart
import 'package:logging/logging.dart';
import 'package:{{APP_NAME}}/core/logging/i_logger.dart';

class AppLogger implements ILogger {
  AppLogger({String name = '{{APP_NAME}}'}) : _log = Logger(name) {
    Logger.root.level = Level.ALL;
    Logger.root.onRecord.listen((record) {
      // ignore: avoid_print
      print('${record.time.toIso8601String()} ${record.level.name} ${record.loggerName}: ${record.message}');
    });
  }

  final Logger _log;

  @override
  void debug(String message, {Object? error, StackTrace? stackTrace}) =>
      _log.fine(message, error, stackTrace);

  @override
  void info(String message, {Object? error, StackTrace? stackTrace}) =>
      _log.info(message, error, stackTrace);

  @override
  void warn(String message, {Object? error, StackTrace? stackTrace}) =>
      _log.warning(message, error, stackTrace);

  @override
  void error(String message, {Object? error, StackTrace? stackTrace}) =>
      _log.severe(message, error, stackTrace);
}
```

### `lib/core/network/api_call_error_handling.dart`

```dart
import 'package:dio/dio.dart';
import 'package:fpdart/fpdart.dart';
import 'package:{{APP_NAME}}/core/errors/failures.dart';

mixin ApiCallErrorHandling {
  Future<Either<Failure, T>> handleApiCall<R, T>(
    Future<R> Function() call, {
    required T Function(R dto) map,
  }) async {
    try {
      final response = await call();
      return Right(map(response));
    } on DioException catch (e, s) {
      return Left(_mapDioException(e, s));
    } catch (e, s) {
      return Left(UnknownFailure(message: e.toString(), rootCause: e, stackTrace: s));
    }
  }

  Failure _mapDioException(DioException e, StackTrace s) => switch (e.type) {
        DioExceptionType.cancel => const CancelledFailure(),
        DioExceptionType.connectionTimeout ||
        DioExceptionType.receiveTimeout ||
        DioExceptionType.sendTimeout ||
        DioExceptionType.connectionError =>
          NetworkFailure(rootCause: e, stackTrace: s),
        DioExceptionType.badCertificate =>
          NetworkFailure(message: 'SSL error', rootCause: e, stackTrace: s),
        DioExceptionType.badResponse => _mapStatus(e, s),
        DioExceptionType.unknown =>
          UnknownFailure(message: e.message ?? 'unknown', rootCause: e, stackTrace: s),
      };

  Failure _mapStatus(DioException e, StackTrace s) {
    final status = e.response?.statusCode ?? 0;
    final body = e.response?.data;
    return switch (status) {
      400 => ValidationFailure(message: _message(body) ?? 'Bad request'),
      401 || 403 => AuthFailure(code: '$status', rootCause: e, stackTrace: s),
      404 => NotFoundFailure(message: _message(body) ?? 'Not found', code: '404'),
      409 => ServerFailure(message: _message(body) ?? 'Conflict', code: '409', rootCause: e, stackTrace: s),
      429 => RateLimitFailure(retryAfter: _retryAfter(e.response?.headers)),
      _ when status >= 500 =>
        ServerFailure(message: _message(body) ?? 'Server error', code: '$status', rootCause: e, stackTrace: s),
      _ => UnknownFailure(message: _message(body) ?? 'Unknown error', rootCause: e, stackTrace: s),
    };
  }

  String? _message(Object? body) {
    if (body is Map<String, Object?>) {
      final msg = body['message'] ?? body['error'];
      return msg is String ? msg : null;
    }
    return null;
  }

  Duration _retryAfter(Headers? headers) {
    final raw = headers?.value('retry-after');
    final seconds = int.tryParse(raw ?? '');
    return Duration(seconds: seconds ?? 60);
  }
}
```

### `lib/core/network/dio_factory.dart`

```dart
import 'package:dio/dio.dart';
import 'package:{{APP_NAME}}/core/auth/auth_token_provider.dart';
import 'package:{{APP_NAME}}/core/config/app_config.dart';
import 'package:{{APP_NAME}}/core/logging/i_logger.dart';

class DioFactory {
  const DioFactory({
    required this.config,
    required this.authTokenProvider,
    required this.logger,
  });

  final AppConfig config;
  final AuthTokenProvider authTokenProvider;
  final ILogger logger;

  Dio create() {
    final dio = Dio(BaseOptions(
      baseUrl: config.apiBaseUrl,
      connectTimeout: const Duration(seconds: 10),
      receiveTimeout: const Duration(seconds: 30),
      sendTimeout: const Duration(seconds: 30),
      headers: const {'Accept': 'application/json'},
    ));

    dio.interceptors.add(InterceptorsWrapper(
      onRequest: (options, handler) async {
        final token = await authTokenProvider.currentToken();
        if (token != null) options.headers['Authorization'] = 'Bearer $token';
        handler.next(options);
      },
      onError: (err, handler) async {
        if (err.response?.statusCode == 401) {
          final refreshed = await authTokenProvider.refresh();
          if (refreshed != null) {
            final opts = err.requestOptions;
            opts.headers['Authorization'] = 'Bearer $refreshed';
            try {
              final retry = await dio.fetch<Object?>(opts);
              return handler.resolve(retry);
            } on DioException catch (e) {
              return handler.next(e);
            }
          }
        }
        handler.next(err);
      },
    ));

    if (config.isDebug) {
      dio.interceptors.add(LogInterceptor(requestBody: true, responseBody: true));
    }
    return dio;
  }
}
```

### `lib/core/di/container.dart`

```dart
import 'package:dio/dio.dart';
import 'package:get_it/get_it.dart';
import 'package:{{APP_NAME}}/core/analytics/i_analytics_tracker.dart';
import 'package:{{APP_NAME}}/core/analytics/noop_analytics_tracker.dart';
import 'package:{{APP_NAME}}/core/config/app_config.dart';
import 'package:{{APP_NAME}}/core/config/flavor.dart';
import 'package:{{APP_NAME}}/core/logging/app_logger.dart';
import 'package:{{APP_NAME}}/core/logging/i_logger.dart';
import 'package:{{APP_NAME}}/core/network/dio_factory.dart';
import 'package:{{APP_NAME}}/feature/home/di/home_module.dart';
import 'package:{{APP_NAME}}/routing/app_router.dart';

final GetIt sl = GetIt.instance;

Future<void> initializeDependencies({required Flavor flavor}) async {
  // Core
  sl.registerLazySingleton<ILogger>(AppLogger.new);
  sl.registerLazySingleton<AppConfig>(() => AppConfig.current);

  // Analytics — defaults to Noop. Under INCLUDE_FIREBASE, replace this line
  // with `FirebaseAnalyticsTracker.new` (see _firebase.md). The interface is
  // always available, so Cubits/Blocs inject IAnalyticsTracker unconditionally.
  sl.registerLazySingleton<IAnalyticsTracker>(NoopAnalyticsTracker.new);

  // sl.registerLazySingleton<AuthTokenProvider>(() => SecureStorageAuthTokenProvider(...));
  // sl.registerLazySingleton<Dio>(() => DioFactory(config: sl(), authTokenProvider: sl(), logger: sl()).create());

  // Routing
  sl.registerLazySingleton<AppRouter>(AppRouter.new);

  // Features — add each feature's register<Feature>Module(sl) here.
  registerHomeModule(sl);
}
```

### `lib/core/database/app_database.dart`  *(INCLUDE_DRIFT)*

```dart
import 'package:drift/drift.dart';
import 'package:{{APP_NAME}}/core/database/executor.dart';

part 'app_database.g.dart';

@DriftDatabase(tables: [])
class AppDatabase extends _$AppDatabase {
  AppDatabase(QueryExecutor super.executor);

  @override
  int get schemaVersion => 1;

  @override
  MigrationStrategy get migration => MigrationStrategy(
        onCreate: (m) => m.createAll(),
      );
}
```

### `lib/core/database/executor.dart`  *(INCLUDE_DRIFT)*

```dart
import 'dart:io';
import 'package:drift/drift.dart';
import 'package:drift/native.dart';
import 'package:path/path.dart' as p;
import 'package:path_provider/path_provider.dart';

QueryExecutor openConnection({required String passphrase}) => LazyDatabase(() async {
      final dir = await getApplicationDocumentsDirectory();
      final file = File(p.join(dir.path, '{{APP_NAME}}.db'));
      return NativeDatabase.createInBackground(
        file,
        setup: (raw) => raw.execute("PRAGMA key = '$passphrase';"),
      );
    });
```

### `lib/routing/app_router.dart`

Top-level router uses `StatefulShellRoute.indexedStack` so the bottom-nav shell preserves each tab's nav stack independently — that's the modern go_router pattern for tab-based navigation. The shell page (`HomeShellPage`) renders the `NavigationBar` and the active tab's `navigator`. Each tab's content lives in its own typed `GoRouteData` so deep links land on the right tab.

```dart
import 'package:flutter/material.dart';
import 'package:go_router/go_router.dart';
import 'package:{{APP_NAME}}/feature/home/presentation/pages/feed_page.dart';
import 'package:{{APP_NAME}}/feature/home/presentation/pages/home_shell_page.dart';
import 'package:{{APP_NAME}}/feature/home/presentation/pages/profile_page.dart';

part 'app_router.g.dart';

class AppRouter {
  GoRouter get config => _router;

  final _router = GoRouter(
    initialLocation: '/feed',
    routes: $appRoutes,
    debugLogDiagnostics: true,
  );
}

@TypedStatefulShellRoute<HomeShellRoute>(
  branches: <TypedStatefulShellBranch<StatefulShellBranchData>>[
    TypedStatefulShellBranch<FeedBranch>(routes: <TypedRoute<RouteData>>[
      TypedGoRoute<FeedRoute>(path: '/feed'),
    ]),
    TypedStatefulShellBranch<ProfileBranch>(routes: <TypedRoute<RouteData>>[
      TypedGoRoute<ProfileRoute>(path: '/profile'),
    ]),
  ],
)
class HomeShellRoute extends StatefulShellRouteData {
  const HomeShellRoute();

  @override
  Widget builder(BuildContext context, GoRouterState state, StatefulNavigationShell navigationShell) =>
      HomeShellPage(navigationShell: navigationShell);
}

class FeedBranch extends StatefulShellBranchData {
  const FeedBranch();
}

class ProfileBranch extends StatefulShellBranchData {
  const ProfileBranch();
}

class FeedRoute extends GoRouteData {
  const FeedRoute();
  @override
  Widget build(BuildContext context, GoRouterState state) => const FeedPage();
}

class ProfileRoute extends GoRouteData {
  const ProfileRoute();
  @override
  Widget build(BuildContext context, GoRouterState state) => const ProfilePage();
}
```

### `lib/feature/home/presentation/pages/home_shell_page.dart`

The shell hosts the `NavigationBar`. `StatefulNavigationShell.goBranch(...)` switches the active tab while preserving each branch's navigation history.

```dart
import 'package:flutter/material.dart';
import 'package:go_router/go_router.dart';

class HomeShellPage extends StatelessWidget {
  const HomeShellPage({super.key, required this.navigationShell});

  final StatefulNavigationShell navigationShell;

  @override
  Widget build(BuildContext context) => Scaffold(
        body: navigationShell,
        bottomNavigationBar: NavigationBar(
          selectedIndex: navigationShell.currentIndex,
          onDestinationSelected: (i) => navigationShell.goBranch(
            i,
            initialLocation: i == navigationShell.currentIndex,
          ),
          destinations: const [
            NavigationDestination(icon: Icon(Icons.home_outlined), selectedIcon: Icon(Icons.home), label: 'Feed'),
            NavigationDestination(icon: Icon(Icons.person_outline), selectedIcon: Icon(Icons.person), label: 'Profile'),
          ],
        ),
      );
}
```

### `lib/feature/home/presentation/bloc/feed_event.dart`

Plain Dart-3 sealed class — no freezed needed for event taxonomies in this project (events are values; equality is by identity for `const` data objects, and the exhaustive `switch` in the `on<E>` handler is enforced by the type system). Add new events as `final class` entries here.

```dart
sealed class FeedEvent {
  const FeedEvent();
}

/// Fired once when the page mounts. Triggers the screen-viewed analytics event
/// and any first-load side-effects (later: a paginated fetch from a repository).
final class FeedStarted extends FeedEvent {
  const FeedStarted();
}
```

### `lib/feature/home/presentation/bloc/feed_state.dart`

```dart
import 'package:freezed_annotation/freezed_annotation.dart';

part 'feed_state.freezed.dart';

@freezed
class FeedState with _$FeedState {
  const factory FeedState({
    @Default(<String>[]) List<String> items,
  }) = _FeedState;
}
```

### `lib/feature/home/presentation/bloc/feed_bloc.dart`

Canonical event-driven Bloc: takes `IAnalyticsTracker` as a dependency, registers one handler per event variant, and never reaches for Firebase directly. The analytics call lives inside the `_onStarted` handler — not in the constructor body — so the side-effect is reproducible, testable with `blocTest`, and easy to extend with additional work (e.g. dispatching a `FeedFetched` event once the analytics call resolves). `bloc_concurrency`'s `droppable()` transformer prevents `FeedStarted` from being processed twice if the page somehow re-emits it on a rebuild.

```dart
import 'package:bloc_concurrency/bloc_concurrency.dart';
import 'package:flutter_bloc/flutter_bloc.dart';
import 'package:{{APP_NAME}}/core/analytics/analytics_event.dart';
import 'package:{{APP_NAME}}/core/analytics/i_analytics_tracker.dart';
import 'package:{{APP_NAME}}/feature/home/presentation/bloc/feed_event.dart';
import 'package:{{APP_NAME}}/feature/home/presentation/bloc/feed_state.dart';

class FeedBloc extends Bloc<FeedEvent, FeedState> {
  FeedBloc({required IAnalyticsTracker analytics})
      : _analytics = analytics,
        super(const FeedState()) {
    on<FeedStarted>(_onStarted, transformer: droppable());
  }

  final IAnalyticsTracker _analytics;

  Future<void> _onStarted(FeedStarted event, Emitter<FeedState> emit) async {
    await _analytics.track(const FeedViewed());
  }
}
```

### `lib/feature/home/presentation/pages/feed_page.dart`

Stateless page that wires the Bloc via `BlocProvider` and fires the initial `FeedStarted` event with the `..add(...)` cascade. The Bloc is built off `sl<IAnalyticsTracker>()` so it picks up whichever impl is registered (Noop or Firebase).

```dart
import 'package:flutter/material.dart';
import 'package:flutter_bloc/flutter_bloc.dart';
import 'package:{{APP_NAME}}/core/analytics/i_analytics_tracker.dart';
import 'package:{{APP_NAME}}/core/di/container.dart';
import 'package:{{APP_NAME}}/feature/home/presentation/bloc/feed_bloc.dart';
import 'package:{{APP_NAME}}/feature/home/presentation/bloc/feed_event.dart';
import 'package:{{APP_NAME}}/feature/home/presentation/bloc/feed_state.dart';

class FeedPage extends StatelessWidget {
  const FeedPage({super.key});

  @override
  Widget build(BuildContext context) => BlocProvider(
        create: (_) => FeedBloc(analytics: sl<IAnalyticsTracker>())..add(const FeedStarted()),
        child: Scaffold(
          appBar: AppBar(title: const Text('Feed')),
          body: BlocBuilder<FeedBloc, FeedState>(
            builder: (context, state) => Center(
              child: Text('Feed (${state.items.length} items)'),
            ),
          ),
        ),
      );
}
```

### `lib/feature/home/presentation/bloc/profile_event.dart`

```dart
sealed class ProfileEvent {
  const ProfileEvent();
}

final class ProfileStarted extends ProfileEvent {
  const ProfileStarted();
}
```

### `lib/feature/home/presentation/bloc/profile_state.dart`

```dart
import 'package:freezed_annotation/freezed_annotation.dart';

part 'profile_state.freezed.dart';

@freezed
class ProfileState with _$ProfileState {
  const factory ProfileState({
    @Default('guest') String userName,
  }) = _ProfileState;
}
```

### `lib/feature/home/presentation/bloc/profile_bloc.dart`

```dart
import 'package:bloc_concurrency/bloc_concurrency.dart';
import 'package:flutter_bloc/flutter_bloc.dart';
import 'package:{{APP_NAME}}/core/analytics/analytics_event.dart';
import 'package:{{APP_NAME}}/core/analytics/i_analytics_tracker.dart';
import 'package:{{APP_NAME}}/feature/home/presentation/bloc/profile_event.dart';
import 'package:{{APP_NAME}}/feature/home/presentation/bloc/profile_state.dart';

class ProfileBloc extends Bloc<ProfileEvent, ProfileState> {
  ProfileBloc({required IAnalyticsTracker analytics})
      : _analytics = analytics,
        super(const ProfileState()) {
    on<ProfileStarted>(_onStarted, transformer: droppable());
  }

  final IAnalyticsTracker _analytics;

  Future<void> _onStarted(ProfileStarted event, Emitter<ProfileState> emit) async {
    await _analytics.track(const ProfileViewed());
  }
}
```

### `lib/feature/home/presentation/pages/profile_page.dart`

```dart
import 'package:flutter/material.dart';
import 'package:flutter_bloc/flutter_bloc.dart';
import 'package:{{APP_NAME}}/core/analytics/i_analytics_tracker.dart';
import 'package:{{APP_NAME}}/core/di/container.dart';
import 'package:{{APP_NAME}}/feature/home/presentation/bloc/profile_bloc.dart';
import 'package:{{APP_NAME}}/feature/home/presentation/bloc/profile_event.dart';
import 'package:{{APP_NAME}}/feature/home/presentation/bloc/profile_state.dart';

class ProfilePage extends StatelessWidget {
  const ProfilePage({super.key});

  @override
  Widget build(BuildContext context) => BlocProvider(
        create: (_) => ProfileBloc(analytics: sl<IAnalyticsTracker>())..add(const ProfileStarted()),
        child: Scaffold(
          appBar: AppBar(title: const Text('Profile')),
          body: BlocBuilder<ProfileBloc, ProfileState>(
            builder: (context, state) => Center(
              child: Text('Profile (${state.userName})'),
            ),
          ),
        ),
      );
}
```

### `lib/feature/home/di/home_module.dart`

Per-feature registration module — the convention used everywhere in this project. The home tabs themselves are stateless until you flesh them out, so the module is currently empty; it exists so adding the next dependency (a repository, a use case) doesn't churn `container.dart`.

```dart
import 'package:get_it/get_it.dart';

void registerHomeModule(GetIt sl) {
  // Add Home-feature factories here as real screens land:
  //   sl.registerFactory<HomeRepository>(() => HomeRepositoryImpl(...));
}
```

### `lib/shared/theme/app_theme.dart`

```dart
import 'package:flutter/material.dart';

abstract final class AppTheme {
  static ThemeData light() => ThemeData(
        useMaterial3: true,
        colorScheme: ColorScheme.fromSeed(seedColor: const Color(0xFF6750A4)),
      );

  static ThemeData dark() => ThemeData(
        useMaterial3: true,
        brightness: Brightness.dark,
        colorScheme: ColorScheme.fromSeed(
          seedColor: const Color(0xFF6750A4),
          brightness: Brightness.dark,
        ),
      );
}
```

### `lib/shared/theme/app_spacing.dart`

```dart
abstract final class AppSpacing {
  static const double xs = 4;
  static const double sm = 8;
  static const double md = 16;
  static const double lg = 24;
  static const double xl = 32;
  static const double xxl = 48;
}
```

### `lib/l10n/app_en.arb`

```json
{
  "@@locale": "en",
  "appTitle": "{{APP_DISPLAY_NAME}}"
}
```

Add `l10n.yaml` at the project root:

```yaml
arb-dir: lib/l10n
template-arb-file: app_en.arb
output-localization-file: app_localizations.dart
```

## Step 6 — `test/` scaffold

Delete `test/widget_test.dart` from `flutter create`.

### `test/helpers/pump_app.dart`

```dart
import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';

extension PumpAppExt on WidgetTester {
  Future<void> pumpApp({
    required Widget child,
    ThemeData? theme,
    Locale locale = const Locale('en'),
  }) async {
    await pumpWidget(
      MaterialApp(
        theme: theme ?? ThemeData.light(useMaterial3: true),
        locale: locale,
        home: child,
      ),
    );
  }
}
```

### `test/helpers/fakes.dart`

```dart
import 'package:{{APP_NAME}}/core/logging/i_logger.dart';

class NoopLogger implements ILogger {
  @override void debug(String message, {Object? error, StackTrace? stackTrace}) {}
  @override void info(String message, {Object? error, StackTrace? stackTrace}) {}
  @override void warn(String message, {Object? error, StackTrace? stackTrace}) {}
  @override void error(String message, {Object? error, StackTrace? stackTrace}) {}
}
```

### `test/smoke_test.dart`

```dart
import 'package:flutter_test/flutter_test.dart';

void main() {
  test('smoke', () {
    expect(1 + 1, 2);
  });
}
```

### `test/feature/home/feed_bloc_test.dart`

Anchors the convention: every Bloc that depends on `IAnalyticsTracker` should have a sibling test that asserts the right event fires. `mocktail` (not `mockito`) is the project default; the fake must `registerFallbackValue` for any `AnalyticsEvent` argument used with `any()`. `blocTest` from `bloc_test` is the canonical way to verify a Bloc — `build → act → verify`.

```dart
import 'package:bloc_test/bloc_test.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:mocktail/mocktail.dart';
import 'package:{{APP_NAME}}/core/analytics/analytics_event.dart';
import 'package:{{APP_NAME}}/core/analytics/i_analytics_tracker.dart';
import 'package:{{APP_NAME}}/feature/home/presentation/bloc/feed_bloc.dart';
import 'package:{{APP_NAME}}/feature/home/presentation/bloc/feed_event.dart';
import 'package:{{APP_NAME}}/feature/home/presentation/bloc/feed_state.dart';

class _MockAnalytics extends Mock implements IAnalyticsTracker {}

class _FakeAnalyticsEvent extends Fake implements AnalyticsEvent {}

void main() {
  setUpAll(() {
    registerFallbackValue(_FakeAnalyticsEvent());
  });

  group('FeedBloc', () {
    late _MockAnalytics analytics;

    setUp(() {
      analytics = _MockAnalytics();
      when(() => analytics.track(any())).thenAnswer((_) async {});
    });

    test('starts with empty FeedState', () {
      final bloc = FeedBloc(analytics: analytics);
      expect(bloc.state, const FeedState());
      bloc.close();
    });

    blocTest<FeedBloc, FeedState>(
      'tracks FeedViewed when FeedStarted is added',
      build: () => FeedBloc(analytics: analytics),
      act: (bloc) => bloc.add(const FeedStarted()),
      verify: (_) {
        verify(() => analytics.track(any(that: isA<FeedViewed>()))).called(1);
      },
    );
  });
}
```

(Other tests go under `test/core/`, `test/feature/<feature>/`, `test/shared/`.)

## Step 7 — Flavors (Android + iOS)

**These require editing project files the CLI shouldn't touch automatically.** Report the needed steps to the user — don't try to perform them.

### Android (`android/app/build.gradle.kts`)

```kotlin
android {
    flavorDimensions += "env"
    productFlavors {
        create("dev") {
            dimension = "env"
            applicationIdSuffix = ".dev"
            versionNameSuffix = "-dev"
            resValue("string", "app_name", "{{APP_DISPLAY_NAME}} Dev")
        }
        create("prod") {
            dimension = "env"
            resValue("string", "app_name", "{{APP_DISPLAY_NAME}}")
        }
    }
}
```

Move `google-services.json` (if Firebase) to `android/app/src/dev/` and `android/app/src/prod/`.

### iOS

1. In Xcode (`ios/Runner.xcworkspace`), duplicate the `Runner` scheme → `Runner-dev` and `Runner-prod`.
2. Under Build Settings, create `DEV` and `PROD` configurations (duplicate `Debug`/`Release`).
3. Set `PRODUCT_BUNDLE_IDENTIFIER` per config (`.dev` suffix on dev).
4. Drop `GoogleService-Info.plist` files per flavor into `ios/Flutter/dev/` and `ios/Flutter/prod/`, then select in the build phase.

Run with:

```bash
flutter run --flavor dev  --target lib/main_dev.dart
flutter run --flavor prod --target lib/main_prod.dart
```

## Step 8 — Codegen

```bash
flutter pub get
dart run build_runner build --delete-conflicting-outputs
dart analyze --fatal-infos --fatal-warnings
flutter test
```

## Post-init checklist (show the user)

- [ ] `flutter pub get` succeeded.
- [ ] `dart run build_runner build --delete-conflicting-outputs` generated `app_router.g.dart`, `feed_state.freezed.dart`, `profile_state.freezed.dart` (and `app_database.g.dart` if INCLUDE_DRIFT).
- [ ] `dart analyze` is clean.
- [ ] `flutter run --flavor dev --target lib/main_dev.dart` boots to the Home shell with Feed + Profile bottom-nav tabs.
- [ ] `flutter test` passes (`smoke_test`, `feed_bloc_test`).
- [ ] Android flavors set up in `android/app/build.gradle.kts`.
- [ ] iOS schemes + configurations set up in Xcode.
- [ ] (If INCLUDE_FIREBASE) `flutterfire configure` run for both flavors. The `FirebaseAnalyticsTracker` no-ops at runtime if Firebase isn't initialized yet, so the app launches regardless; events start flowing once configure has run + the JSON/plist drops are in place.
- [ ] Replace the Feed and Profile placeholders with your first real features (use `/new-feature <name>` or follow the conventions in `flutter-architecture/SKILL.md`).
- [ ] Add new analytics events as sealed entries in `lib/core/analytics/analytics_event.dart` — never magic strings.
- [ ] Git initialized: `git init && git add . && git commit -m 'initial scaffold'`.

## Hard rules for this skill

- **Never** include `sqlite3_flutter_libs` alongside `sqlcipher_flutter_libs`. They conflict.
- **Never** include `mockito`. `mocktail` only.
- **Never** include `dartz`. `fpdart` only.
- **Never** include `Equatable`. Use `freezed` for value types / unions.
- **Never** use string-based `go_router` route constants when `go_router_builder` + typed routes are available.
- **Never** set `GetIt.I.allowReassignment = true` in templates. Use scopes in tests.
- **Never** leave `intl: any` — pin a version.
