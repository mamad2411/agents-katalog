---
name: firebase-services
description: Firebase integration patterns for this Flutter app — Crashlytics, Analytics, Remote Config, and App Check, each behind a thin interface that can be swapped or stubbed in tests. Load whenever wiring a new Firebase service or touching flavor configuration.
---

# Firebase services

## Philosophy

Firebase SDKs should never be imported above `data/`. Every service has:
- A domain-level interface in `domain/services/` (pure Dart, no Firebase).
- A concrete implementation in `data/firebase/` that wraps the SDK.
- A stub fake in `test/support/` for tests.

Swap at the composition root (`main.dart` / `injection.dart`).

## FlutterFire configuration

One `firebase_options.dart` per flavor. Generate via FlutterFire CLI **per flavor**:

```bash
flutterfire configure --project=my-app-dev --ios-bundle-id=com.example.app.dev --android-package-name=com.example.app.dev --out=lib/firebase_options_dev.dart
flutterfire configure --project=my-app-prod --ios-bundle-id=com.example.app --android-package-name=com.example.app --out=lib/firebase_options_prod.dart
```

`main_dev.dart` / `main_prod.dart` pass the right options into `Firebase.initializeApp(...)`.

## Crashlytics

`domain/services/crash_reporter.dart`:

```dart
abstract interface class CrashReporter {
  Future<void> recordError(Object error, StackTrace stack, {String? reason, Map<String, dynamic>? extras});
  void setUserId(String? userId);
  void setKey(String key, Object value);
}
```

`data/firebase/firebase_crash_reporter.dart`:

```dart
class FirebaseCrashReporter implements CrashReporter {
  FirebaseCrashReporter(this._crashlytics);

  final FirebaseCrashlytics _crashlytics;

  @override
  Future<void> recordError(
    Object error,
    StackTrace stack, {
    String? reason,
    Map<String, dynamic>? extras,
  }) {
    extras?.forEach((key, value) => _crashlytics.setCustomKey(key, value.toString()));
    return _crashlytics.recordError(error, stack, reason: reason);
  }

  @override
  void setUserId(String? userId) => _crashlytics.setUserIdentifier(userId ?? '');

  @override
  void setKey(String key, Object value) => _crashlytics.setCustomKey(key, value.toString());
}
```

Bootstrap in `main.dart`:

```dart
await Firebase.initializeApp(options: DefaultFirebaseOptions.currentPlatform);
FlutterError.onError = FirebaseCrashlytics.instance.recordFlutterFatalError;
PlatformDispatcher.instance.onError = (error, stack) {
  FirebaseCrashlytics.instance.recordError(error, stack, fatal: true);
  return true;
};
```

Wire the interface via GetIt: `sl.registerLazySingleton<CrashReporter>(() => FirebaseCrashReporter(FirebaseCrashlytics.instance))`.

## Analytics

Keep the wire format decoupled from Firebase-specific event shapes:

```dart
abstract interface class AnalyticsClient {
  Future<void> logEvent(String name, {Map<String, Object?>? parameters});
  Future<void> setUserProperty(String name, String? value);
}

class FirebaseAnalyticsClient implements AnalyticsClient {
  FirebaseAnalyticsClient(this._analytics);
  final FirebaseAnalytics _analytics;

  @override
  Future<void> logEvent(String name, {Map<String, Object?>? parameters}) =>
      _analytics.logEvent(name: name, parameters: parameters?.map((k, v) => MapEntry(k, v as Object)));

  @override
  Future<void> setUserProperty(String name, String? value) =>
      _analytics.setUserProperty(name: name, value: value);
}
```

Event names and parameters go in a `domain/analytics/events.dart` registry so you don't scatter magic strings.

## Remote Config

One fetch at startup, then read synchronously:

```dart
class FirebaseFeatureFlags implements FeatureFlags {
  FirebaseFeatureFlags(this._rc);
  final FirebaseRemoteConfig _rc;

  Future<void> initialize() async {
    await _rc.setConfigSettings(RemoteConfigSettings(
      fetchTimeout: const Duration(seconds: 10),
      minimumFetchInterval: const Duration(hours: 1),
    ));
    await _rc.setDefaults(const {
      'enable_new_checkout': false,
      'orders_per_page': 20,
    });
    await _rc.fetchAndActivate();
  }

  @override
  bool isEnabled(String flag) => _rc.getBool(flag);

  @override
  int getInt(String key) => _rc.getInt(key);
}
```

Gate with a `minimumFetchInterval` in release; during dev you want a short interval.

## App Check

Guards your Firebase backend from non-legit clients:

```dart
await FirebaseAppCheck.instance.activate(
  androidProvider: AndroidProvider.playIntegrity,
  appleProvider: AppleProvider.appAttestWithDeviceCheckFallback,
);
```

Debug builds enroll via `AndroidProvider.debug` / `AppleProvider.debug` with a device token registered in the Firebase console.

## Flavor config

`android/app/build.gradle.kts`:

```kotlin
android {
    flavorDimensions += "env"
    productFlavors {
        create("dev") { applicationIdSuffix = ".dev"; dimension = "env"; resValue("string", "app_name", "App Dev") }
        create("prod") { dimension = "env"; resValue("string", "app_name", "App") }
    }
}
```

Drop `google-services.json` for each flavor under `android/app/src/{flavor}/google-services.json`.

iOS: one `GoogleService-Info.plist` per scheme under `ios/Runner/Firebase/{Dev,Prod}/`, copied via a Run Script phase.

## Testing

Every interface has a `Fake*` counterpart:

```dart
class FakeCrashReporter implements CrashReporter {
  final List<(Object, StackTrace)> recorded = [];
  @override Future<void> recordError(Object error, StackTrace stack, {String? reason, Map<String, dynamic>? extras}) async {
    recorded.add((error, stack));
  }
  @override void setUserId(String? userId) {}
  @override void setKey(String key, Object value) {}
}
```

Never call `Firebase.initializeApp()` in unit tests. Integration tests that need live Firebase use the emulator suite.

## Hard nos

- No `import 'package:firebase_*/...` in `lib/domain/` or `lib/presentation/`.
- No unconditional `FirebaseAnalytics.instance.logEvent(...)` — go through the injected `AnalyticsClient`.
- No committing a dev `GoogleService-Info.plist` / `google-services.json` for prod, or vice versa.
- No `fetchAndActivate()` on every app launch without caching; respect the fetch interval.
- No enabling Crashlytics in debug without a fence — your stack traces drown theirs.
