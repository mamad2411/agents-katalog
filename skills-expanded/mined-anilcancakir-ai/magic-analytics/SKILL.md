---
name: magic-analytics
description: "Send GA4 analytics from a Magic app: GTM on web, Firebase on mobile, one Analytics facade, ad signals always denied."
version: 1.0.1
when_to_use: "Use when code imports package:magic_analytics or touches Analytics, AnalyticsServiceProvider or analyticsConfig in a Magic app."
---

# magic_analytics

GA4 for a Magic app through one `Analytics` facade. On web a Google Tag Manager container is loaded from a first-party gateway path; on iOS and Android events go through Firebase; with no IDs a null driver sends nothing. Every parameter value, page title and location is scrubbed of emails and tokens before it leaves (an identifying user id is refused instead), ads consent is always denied and the package is inert until the host sets its keys. It is generic on purpose: no user model, team or event of its own.

This skill covers `magic_analytics` only. The Magic framework (container, facades, routing, `Auth`) is the `magic-framework` skill, and GA4, GTM and Firebase themselves are Google's documentation.

## Install

```bash
flutter pub add magic_analytics
dart run magic:dowel plugin:install magic_analytics
```

Requires Dart >=3.13, Flutter >=3.47 and `magic` ^1.0.0, with `firebase_core` and `firebase_analytics` pulled in. The installer publishes `lib/config/analytics.dart`, registers `AnalyticsServiceProvider` in `lib/config/app.dart` and adds `analyticsConfig` to the config factories. It writes no native file and cannot set up a web server. Import only the barrel: `package:magic_analytics/magic_analytics.dart`. `package:magic_analytics/cli.dart` (`MagicAnalyticsDowelProvider`, no commands) is for dowel's `plugin:install`, never for app code.

## Config rules

1. `ANALYTICS_ENABLED` other than `true`, `1` or `yes` binds `NullDriver`. The web driver needs both `GTM_CONTAINER_ID` and `GTM_GATEWAY_PATH`, so a container is never requested from `googletagmanager.com`. The mobile driver needs `firebase_options` to be a `FirebaseOptions Function()`.
2. Read the keys through `Env.filled`, which treats `KEY=""` as nothing. `Env` reads the bundled `.env`, not `--dart-define`.
3. Web gateway: proxy a first-party path to `GTM-XXXXXXX.fps.goog` (Google tag gateway), never `googletagmanager.com`. The container's GA4 configuration sets `send_page_view` to `false`: the driver pushes each page view itself. The Google tag alone sends no custom event: the container also needs a GA4 Event tag (event name `{{Event}}`) on a Custom Event trigger, version 2 data layer variables for `page_location`, `page_referrer`, `page_title`, `user_id`, the default params and `user_properties.<name>`, a shared Event Settings Variable, and "Require additional consent: `analytics_storage`" on both tags so an opted-out user sends no cookieless pings (see `doc/basics/drivers.md`, Container Setup).
4. Mobile: run `flutterfire configure --platforms=ios,android`, set `'firebase_options': () => DefaultFirebaseOptions.currentPlatform`, and leave it `null` on web. Firebase is never initialised on web.
5. Native keys keep collection off until the driver enables it and ads denied. iOS `Info.plist`: `FIREBASE_ANALYTICS_COLLECTION_ENABLED` false, `FirebaseAutomaticScreenReportingEnabled` false, `GOOGLE_ANALYTICS_DEFAULT_ALLOW_ANALYTICS_STORAGE` true, and `GOOGLE_ANALYTICS_DEFAULT_ALLOW_AD_STORAGE`, `..._AD_USER_DATA`, `..._AD_PERSONALIZATION_SIGNALS` false. Android `<meta-data>`: `firebase_analytics_collection_enabled` false, `google_analytics_automatic_screen_reporting_enabled` false, `google_analytics_default_allow_analytics_storage` true, and `google_analytics_default_allow_ad_storage`, `..._ad_user_data`, `..._ad_personalization_signals` false.

## Provider rules

1. Register `AnalyticsServiceProvider` in the `providers` list of `lib/config/app.dart`, after the error reporting providers. `boot()` adds the page view observer to `MagicRouter`, which refuses one after it has built its `routerConfig`.
2. The provider resets analytics when the signed-in user signs out or changes, keyed on the user id, so a team switch keeps the identity. It never identifies anyone: call `Analytics.identify` yourself with the user's UUID, never an email.
3. `AnalyticsNavigatorObserver` reports the route name as the title (the pattern when the route has none) and the route pattern (`/monitors/:id`, never `/monitors/42`) as the location, so no id or token leaves. A page without a name is not a page view.

## Facade rules

1. `setDefaultParams` replaces the whole set; team facts (a plan, a size) go here, sent with every event. `setUserProperties` is user-level only. Pass every default you want kept.
2. `reset()` nulls the user id, every user property and every default parameter, and never rotates the client id. Run it on sign-out or a user change; the provider already does.
3. GA4 limits are asserted in debug and the call is dropped with a log in release: names 40 characters, letters, digits and underscores, no `ga_`, `google_` or `firebase_` prefix; 25 parameters with defaults; string values 100 characters; user property name 24 and value 36; user id 256. Values are strings or numbers.
4. Every call returns a future that never fails; a driver error is logged, never thrown into UI flow. The one exception is a GA4 limit violation, which throws an `AssertionError` in debug (dropped with a log in release). Calls run in order on a queue.
5. Never send an email, token or code as a parameter, title or user id. String values are scrubbed (`UrlScrubber`) and `identify` refuses an id the scrubber would change, but a secret in free text is not recognisable.

## Consent rules

1. `ad_storage`, `ad_user_data` and `ad_personalization` are denied on every start; nothing grants them.
2. The opt-out is in memory only. The host persists it and calls `Analytics.setOptOut` on every start, before the first page view.
3. While opted out every call except `setOptOut`, `reset` and `clientId` is a no-op that reaches no driver.
4. The web driver loads lazily on the first send, never on an opted-out device; opting out after load pushes a consent update. It pushes `user_properties` nested, default params flat, follows every `track` with a push that returns its parameter keys to the value it holds for them (user id, user properties, page fields, defaults) or `null` (the data layer merges, so they would otherwise leak into later events), and builds `page_location` and `page_referrer` from the origin plus the pattern (the first referrer is the origin root). Before `gtm.start` it pre-seeds both fields with the origin alone, so the Google tag never reads a tokenised address bar.
5. The Firebase driver turns collection on at first use unless opted out, and never calls `resetAnalyticsData`.

## Recipes

Wire the app:

```dart
import 'package:magic/magic.dart';
import 'package:material_ui/material_ui.dart';

import 'config/analytics.dart'; // published by plugin:install

Future<void> main() async {
  await Magic.init(
    configFactories: [
      () => analyticsConfig,
      // Keep every other config factory your main() already passes.
    ],
  );

  runApp(MagicApplication(title: 'My App'));
}
```

Identify, tag the team and send an event (the ids and plan are the app's own):

```dart
import 'package:magic_analytics/magic_analytics.dart';

Future<void> afterSignIn(String userUuid, String teamPlan) async {
  await Analytics.identify(userUuid);
  await Analytics.setDefaultParams({'team_plan': teamPlan});
  await Analytics.track('monitor_created', {'monitor_type': 'http'});
}
```

Restore the stored opt-out during boot:

```dart
import 'package:magic_analytics/magic_analytics.dart';

Future<void> restoreConsent(bool storedOptOut) async {
  await Analytics.setOptOut(storedOptOut);
}
```

## Testing

No mocking library is needed. `Analytics.fake()` binds the real manager over a recording `FakeAnalytics`; call it after the provider registers, and in a `testWidgets` test inside the body (not `setUp`) so the send queue is created in its zone. `Analytics.unfake()` and `MagicRouter.reset()` go in `tearDown`.

```dart
import 'package:flutter_test/flutter_test.dart';
import 'package:magic/magic.dart';
import 'package:magic_analytics/magic_analytics.dart';

void main() {
  setUp(() {
    MagicApp.reset();
    Magic.flush();
  });

  tearDown(() {
    Analytics.unfake();
    MagicRouter.reset();
  });

  test('creating a monitor sends one event', () async {
    final FakeAnalytics fake = Analytics.fake();

    await Analytics.track('monitor_created', {'monitor_type': 'http'});

    fake.assertTracked('monitor_created');
    expect(fake.events.single.defaultParams, isEmpty);
  });
}
```

`fake.events`, `fake.screens` and `fake.calls` hold `RecordedAnalyticsCall`s, each stamped with the user id, user properties and default parameters the transport held. A call made without `await` lands on a later microtask: `await Future<void>.delayed(Duration.zero)` before reading.
