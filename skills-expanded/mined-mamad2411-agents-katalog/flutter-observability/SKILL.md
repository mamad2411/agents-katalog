---
name: flutter-observability
description: Flutter observability standards — one injected AppLogger facade with built-in redaction, the print/debugPrint ban, crash-reporter context and navigation breadcrumbs, the three global error channels, a sealed AnalyticsEvent catalogue with consent checked before collection, and typed feature flags with a fail-open minimum-version gate. Load when writing or reviewing logging, crash reporting, analytics events, remote config or feature flags.
user-invocable: false
stack: logging/flutter-observability
paths:
  - "**/core/observability/*.dart"
  - "**/core/logging/*.dart"
  - "**/*_logger.dart"
  - "**/*analytics*.dart"
  - "**/*remote_config*.dart"
  - "**/*feature_flag*.dart"
---

Full standards in [flutter-observability.md](flutter-observability.md). Always-on summary:

**Scope:** the logger, the crash reporter's context, the analytics catalogue, and feature flags. Error *types* and `isReportable` are `api-style/dio` — obey them, never redefine them. Crash triage as a practice is the `/flutter-monitoring` command.

**Logging:**
- One `AppLogger` facade, injected from a provider. Nothing calls a logging package, a crash reporter or the console directly. Message is a short constant; everything variable goes in `fields:`.
- Never `print` and never `debugPrint` — `avoid_print` misses the second, and it still writes to the system log in release. Also banned: `dart:developer`'s `log`, `stdout.writeln`. Console sink exists in debug/profile only; release is silent below `warn`.
- Redaction runs inside the facade (`redact(fields)` in `_emit`) so a call site cannot skip it. Never log a token, password, `Authorization` header, response body or full URI. Log method and path via `redactUri(uri)`, which replaces the query string — that is where emails and identifiers travel. Deny-list on keys *plus* a shape check for JWT-looking values.
- Crash context set once: `flavor`, `app_version`, `build_number`, the **pseudonymous** user id (never an email), the current `route`, plus navigation breadcrumbs from one `NavigatorObserver`.

**Error channels — install all three, each catches what the others miss:**
- `FlutterError.onError` (framework: build/layout/paint/gestures), `PlatformDispatcher.instance.onError` (uncaught async — `return true;`, because `false` falls through to the platform default), and `runZonedGuarded` around `runApp` with `WidgetsFlutterBinding.ensureInitialized()` inside the same zone (bootstrap errors before `runApp`).
- Uncaught is `fatal: true`; a handled error is `fatal: false` and only reported when its type says `isReportable`. Never `catch (_) {}`.

**Analytics:**
- A `sealed class AnalyticsEvent` catalogue; each event is a `final class … extends AnalyticsEvent` with `String get name` and typed `parameters`. Never a free-form name and a bag at a call site.
- One convention: `object_verb`, snake_case, past tense — `course_enrolled`, `checkout_completed`. ≤40 chars, no `firebase_`/`google_`/`ga_` prefix, ≤25 parameters.
- No personal data as a property — no email, phone, name, address, search text or precise location. Identity is the pseudonymous id via `setUser`.
- Screen views come from the `NavigatorObserver`, never from `initState`. Debug and non-prod builds use a `DebugAnalyticsService`, never the production property.
- Consent gates **collection**, not reporting: `setAnalyticsCollectionEnabled(status == ConsentStatus.granted)`, and `log()` **drops** events while consent is not `granted`. Never queue or buffer them — a queued event is data collected without permission. `unknown` behaves as `denied`; a switch to denied calls `resetAnalyticsData()`.

**Feature flags:**
- Typed `Flag<T>` in one catalogue, with `defaultValue` (the *safe* behaviour, so the app works with no network), `owner` and `removeBy` as required parameters. Read through `flags.value(Flags.x)` — never `FirebaseRemoteConfig.instance.getBool('…')`, where a typo silently returns `false` forever.
- The minimum-version gate **fails open**: `if (!flags.hasFetched) return UpdateRequirement.none;`, and an absent or unparseable value is also `none`. A blocking screen from a config blip is a self-inflicted total outage. `enum UpdateRequirement { none, recommended, blocking }`.
- Every risky feature ships a kill switch that has been verified off, read at the decision point rather than cached at boot. Flags never gate security — the server authorises, the flag only hides the button.

**Related:** `api-style/dio`, `state/riverpod`, `frontend/go-router`, `auth/flutter-session`, `ci/flutter-release`, `testing/flutter-test`.
