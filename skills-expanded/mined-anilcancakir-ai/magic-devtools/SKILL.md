---
name: magic-devtools
description: "Wire tapir and crumbs into a Magic app with magic_devtools, and keep the wiring out of release builds."
version: 1.1.0
when_to_use: "Use when code imports package:magic_devtools or touches MagicDevtools, the tapir or crumbs integrations, MagicPerfIntegration or the /preview catalog."
---

# magic_devtools

`magic_devtools` is the seam between a Magic app and two dev tools: tapir, the E2E driver an agent uses to snapshot and drive the app, and crumbs, the runtime inspector that records HTTP, logs, exceptions and app activity. It adds Magic-aware enrichers to tapir's snapshots, feeds Magic's HTTP, model, cache, event, gate, query and log activity into crumbs, assembles the data path behind tapir's perf sessions, and hosts a dev-only component catalog at `/preview`. `magic` itself depends on neither tool; this package is where they meet.

This skill covers wiring and testing `magic_devtools` only. Driving the app (`tapir:snap`, `tapir:tap`, perf sessions) is the `tapir` skill, reading records is the `crumbs` skill, Magic's container, router, forms and providers are the `magic-framework` skill, and styling a preview with Wind classes is the `wind-ui` skill.

## Install

```bash
flutter pub add magic_devtools tapir crumbs
```

Requires Dart >=3.13, Flutter >=3.47 and `magic` ^1.0.0. All three packages go under `dependencies`, because `lib/main.dart` imports them and a `dev_dependencies` entry trips the `depend_on_referenced_packages` lint. There is no service provider, config file or `plugin:install` step. `dart run magic:dowel magic:install --with-devtools` writes the wiring as per-tool blocks while it installs Magic; by hand it is the two calls below.

| Barrel | Exports |
|---|---|
| `package:magic_devtools/magic_devtools.dart` | `MagicDevtools`, `MagicPerfIntegration`, `PerfInsightRules`, `PerfRuleInputs` |
| `package:magic_devtools/tapir.dart` | `MagicTapirIntegration` and its 14 enricher functions |
| `package:magic_devtools/crumbs.dart` | `MagicCrumbsIntegration`, `MagicHttpFacadeAdapter` and the six watchers |
| `package:magic_devtools/preview.dart` | `MagicPreview`, `PreviewEntry`, `MagicPreviewCatalog`, `kPreviewEnabled` |

## Rules for every install call

1. Guard each call with `if (!kReleaseMode)` at the call site, in the app's `main.dart`. Nothing in this package checks the build mode, and `kReleaseMode` is a compile-time constant, so the guard is what drops tapir, crumbs and this package from a release build. Never move the guard into a helper that is itself called unguarded.
2. Use `!kReleaseMode`, not `kDebugMode`. Debug and profile builds both carry the tools, and a performance measurement belongs on a profile build, where `kDebugMode` is false.
3. Every `install()` is idempotent within an isolate, so a second call registers nothing twice. That does not make a late call safe: see the perf rules.

## MagicDevtools rules

1. Call `MagicDevtools.installPre()` before `await Magic.init(...)` and `MagicDevtools.installPost()` after it. The pre half installs `TapirPlugin`, `CrumbsPlugin`, one `ExceptionWatcher`, one `DumpWatcher` and `MagicPerfIntegration`, so boot errors land in crumbs; the post half installs `MagicCrumbsIntegration` then `MagicTapirIntegration`, which resolve Magic's container.
2. Pick one style per app: the umbrella, or the per-tool blocks. `installPre()` keeps the watcher pair it registered, but it cannot see a pair the app registered by hand, and two `ExceptionWatcher`s record every exception twice.
3. Register an extra crumbs watcher with `CrumbsPlugin.registerWatcher(...)` after `installPre()`, not instead of it.

## MagicTapirIntegration rules

1. Install it after `Magic.init()`. Its Echo subscription is made only when the `broadcasting` binding exists at `install()`; installed earlier, `magicEchoConnection` can answer only `connected` or `disconnected`.
2. Expect the `magic*` lines only from `tapir:snap --includeEnrichers`: enrichers are off by default.
3. Keep custom enricher keys distinct from the 14 `magic*` keys. tapir prints every line every enricher returns and removes no duplicates.
4. An enricher has tapir's signature `String? Function(Element, RefRegistry)`, runs synchronously, and never keeps the `Element` between calls.
5. `tapir:navigate --route` takes a URL path: the adapter calls `MagicRouter.instance.to(route)`, not `toNamed`. On a `StateError` it answers `false` and tapir falls back to its own navigation.
6. `magicAuthUser` reads only the `id` and `display_name` attributes; a user model without `display_name` prints the id alone. A `MagicMiddleware` object prints through its `toString()`.
7. Expect no `magicAuthUser` line in an app without `AuthServiceProvider`: the enricher checks `Magic.bound('auth')` first, as the Echo enricher does for `broadcasting`, and the other enrichers keep their lines.

## MagicCrumbsIntegration rules

1. Install it after `Magic.init()`. Before it, the HTTP adapter finds no `network` binding and attaches nothing, and the install guard stops a later call from retrying.
2. Bodies are masked by key before they are stringified and cut at 8192 characters, and the header named by `auth.token.header` (default `Authorization`) is hidden. Add your own names with `CrumbsRedaction.hideRequestHeaders`, `hideRequestParameters` and `hideResponseParameters`; they merge with crumbs' defaults.
3. Keep secrets out of model attributes in a debug session: a `ModelRecord` copies every attribute unmasked.
4. Read `EventRecord.payload` as always empty: `MagicEventWatcher` records which event fired and when, not its fields.
5. `Http.fake()` installs no interceptors, so faked requests never reach crumbs. Assert on the fake.
6. The event watchers' `uninstall()` removes nothing, because magic's `EventDispatcher` has no per-listener removal; tests clear the dispatcher themselves.
7. `MagicLogWatcher` wraps the container's `log` manager, so `Log.*` calls land in `crumbs:tail` and `tapir:console`; a call made during `Magic.init()`, before the post half, is not recorded. `Log.fake()` still works: called before the install it is wrapped and keeps its entries, called after it replaces the wrapper. `Log.unfake()` drops the wrapper too, so call `MagicLogWatcher().install()` after it to bridge again. A `Map` or `List` context is masked by key before it is stored; the message text is not.

## MagicPerfIntegration rules

1. Install it before `Magic.init()`, which `installPre()` does. `Magic.init()` builds the router after the providers boot, and `MagicRouter.addObserver` throws a `StateError` from then on. The throw is deliberate: a missing observer would leave the report without route transitions and nothing to say why.
2. `tapir:install` and `crumbs:install` never write `MagicPerfIntegration` or `MagicDevtools`. An app wired only by them gets a structurally complete perf report with every counter at zero, because tapir's unassigned pointers fail silently.
3. Run an `attribution` session (the `tapir:perf_begin` default) for counters and insights, a `timing` one for comparable milliseconds; a timing session counts nothing and evaluates no insight.
4. `routeTransitions` holds named pushes only, at most 200. A dialog or bottom sheet pushes an unnamed route and is skipped.

## MagicPreview rules

1. Call `MagicPreview.register(previewEntries())` and then `MagicPreview.registerRoutes()` from a provider's `boot()`. `boot()` runs inside `Magic.init()` before the router is built; a later `registerRoutes()` throws the router's `StateError`, and `register()` after `registerRoutes()` leaves the catalog empty because the routes captured the entries when they were added.
2. Generate the index with `dart run magic:dowel previews:refresh` (scans `--path`, default `lib`, and writes `<path>/_previews.g.dart`). Each `*.preview.dart` file holds exactly one public class whose name ends in `Preview`, with a `const` constructor; the generated builder is `(_) => const XxxPreview()`.
3. Keep entries in a function, never a top-level const list, so a release build can drop them.
4. `registerRoutes()` returns at once in release, and when `kPreviewEnabled` (`PREVIEW_ENABLED`, default `kDebugMode`) is false. A profile build needs `--dart-define=PREVIEW_ENABLED=true` and a call site guarded by `!kReleaseMode`, since a `kDebugMode` check is false there.

## Recipes

Wire both tools with the umbrella:

```dart
import 'package:flutter/foundation.dart' show kReleaseMode;
import 'package:flutter/widgets.dart';
import 'package:magic/magic.dart';
import 'package:magic_devtools/magic_devtools.dart';

Future<void> main() async {
  WidgetsFlutterBinding.ensureInitialized();

  if (!kReleaseMode) MagicDevtools.installPre();

  await Magic.init(); // the app's configFactories and providers go here

  if (!kReleaseMode) MagicDevtools.installPost();

  runApp(MagicApplication());
}
```

Wire tapir with the perf path and no crumbs:

```dart
import 'package:flutter/foundation.dart' show kReleaseMode;
import 'package:flutter/widgets.dart';
import 'package:magic/magic.dart';
import 'package:magic_devtools/magic_devtools.dart';
import 'package:magic_devtools/tapir.dart';
import 'package:tapir/tapir.dart';

Future<void> main() async {
  WidgetsFlutterBinding.ensureInitialized();

  if (!kReleaseMode) {
    TapirPlugin.install();
    MagicPerfIntegration.install();
  }

  await Magic.init();

  if (!kReleaseMode) MagicTapirIntegration.install();

  runApp(MagicApplication());
}
```

Mask an app-specific header and request body key next to the auth header the integration hides, inside the same guard:

```dart
import 'package:crumbs/crumbs.dart';
import 'package:flutter/foundation.dart' show kReleaseMode;
import 'package:flutter/widgets.dart';
import 'package:magic/magic.dart';
import 'package:magic_devtools/magic_devtools.dart';

Future<void> main() async {
  WidgetsFlutterBinding.ensureInitialized();

  if (!kReleaseMode) MagicDevtools.installPre();

  await Magic.init();

  if (!kReleaseMode) {
    MagicDevtools.installPost();
    CrumbsRedaction.hideRequestHeaders(<String>['X-Device-Secret']);
    CrumbsRedaction.hideRequestParameters(<String>['pin']);
  }

  runApp(MagicApplication());
}
```

Register the preview catalog from the route provider. `_previews.g.dart` is the file `previews:refresh` writes:

```dart
import 'package:flutter/foundation.dart' show kReleaseMode;
import 'package:magic/magic.dart';
import 'package:magic_devtools/preview.dart';

import '_previews.g.dart';

class RouteServiceProvider extends ServiceProvider {
  RouteServiceProvider(super.app);

  @override
  void register() {}

  @override
  Future<void> boot() async {
    // The app's own routes are registered here first.
    if (!kReleaseMode) {
      MagicPreview.register(previewEntries());
      MagicPreview.registerRoutes();
    }
  }
}
```

## Testing

Every integration keeps static state. Reset each one you installed, and the packages underneath, so a test cannot leak enrichers, watchers or tapir pointers into the next:

```dart
import 'package:crumbs/crumbs.dart';
// flutter_test exports its own EventDispatcher; Magic's is the one to clear.
import 'package:flutter_test/flutter_test.dart' hide EventDispatcher;
import 'package:magic/magic.dart';
import 'package:magic_devtools/crumbs.dart';
import 'package:magic_devtools/tapir.dart';
import 'package:tapir/tapir.dart';

void main() {
  setUpAll(TestWidgetsFlutterBinding.ensureInitialized);

  setUp(() {
    MagicApp.reset();
    Magic.flush();
    MagicRouter.reset();
    CrumbsStore.resetForTesting();
    EventDispatcher.instance.clear();
  });

  tearDown(() {
    MagicTapirIntegration.resetForTesting();
    MagicCrumbsIntegration.resetForTesting();
  });

  test('installs the Magic enrichers once', () {
    MagicTapirIntegration.install();
    MagicTapirIntegration.install();

    expect(TapirPlugin.enrichers, hasLength(14));
  });
}
```

| Reset | Clears |
|---|---|
| `MagicDevtools.resetForTesting()` | The `ExceptionWatcher` and `DumpWatcher` `installPre()` registered, restoring `FlutterError.onError`, the platform error callback and `debugPrint` |
| `MagicTapirIntegration.resetForTesting()` | The 14 enrichers, the navigate adapter, the Echo subscription, the install guard |
| `MagicCrumbsIntegration.resetForTesting()` | The install guard, the `log` manager wrapper and tapir's three crumbs readers; not the adapter or the watchers' listeners, so also call `EventDispatcher.instance.clear()` |
| `MagicPerfIntegration.resetForTesting()` | The guard, the session counters, the sink, the insight contributor, the frame watcher, every tapir perf pointer; not the navigator observer, so also call `MagicRouter.reset()` |
| `MagicPreview.resetForTesting()` | The registered entries; `MagicRouter.reset()` drops the routes |

Inside `testWidgets`, call `MagicDevtools.resetForTesting()` at the end of the test body rather than in `tearDown`: flutter_test checks `debugPrint` right after the body, before `tearDown` runs. A host test cannot open a real tapir interaction (`PerfInteraction` has a private constructor), so replace `MagicPerfIntegration.zoneInteraction`, `interactionIdAt` or `activeInteractionId` instead; `MagicPerfIntegration.resetForTesting()` puts them back.
