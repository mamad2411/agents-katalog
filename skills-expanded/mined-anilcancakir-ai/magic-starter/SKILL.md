---
name: magic-starter
description: "Build with magic_starter: opt-in Magic screens for sign-in, settings, teams, billing and support, plus the view registry."
version: 1.7.0
when_to_use: "Use when code imports package:magic_starter or touches MagicStarter, a starter view key, an MS component or a starter:* command."
---

# magic_starter

Ready-made screens for a Magic app: login, registration, password reset, email verification, two-factor, social and phone sign-in, guest sessions and handoff; a settings hub with profile, security and preference pages; teams; the `magic_notifications` screens in the app shell; billing over `magic_payments`; a support desk. Each feature is a toggle in `lib/config/magic_starter.dart` that defaults to `false`. `MagicStarterServiceProvider` wires it, `MagicStarter` is the facade (`bootstrap`, `view`, theme setters), `MagicStarterConfig` reads the toggles and routes, and every screen, layout and modal resolves through a string-keyed registry the host can override. The controllers call `magic-starter-laravel`'s `api/v1` routes one to one.

This skill covers `magic_starter` only. The Magic framework itself (container, facades, routing, `Auth`, `Http`, controllers) is the `magic-framework` skill; the className syntax and the W-widgets are `wind-ui`; the notification API (`Notify`) is `magic-notifications`, the billing contract is `magic-payments`, the social login bridge is `magic-social-auth`.

## Install

```bash
flutter pub add magic_starter
dart run magic:dowel plugin:install magic_starter --no-bootstrap
dart run magic:dowel starter:install --features=registration,teams,notifications
dart run magic:dowel starter:doctor
```

Requires Dart >=3.13, Flutter >=3.47 and `magic` ^1.0.0, in an app already scaffolded with `dart run magic:dowel magic:install`. `plugin:install` registers `MagicStarterDowelProvider` and injects `MagicStarterServiceProvider` into `lib/config/app.dart`; pass `--no-bootstrap`, because the chained `starter:install` always gets `--non-interactive`, writes every feature `false`, and a later `starter:install --features=...` finds the config that exists by then, leaves it alone and exits 1 naming the features it would have changed (recover with `starter:configure`, a hand edit, or `--force`). Run `starter:install` yourself: without `--features` it asks one question per feature, every answer defaulting to no; with it, an unlisted key is written `false`. It writes `lib/config/magic_starter.dart`, the middleware, `User` (and `Team`), a dashboard, `lib/routes/app.dart`, the `MagicStarter.bootstrap(...)` call in `AppServiceProvider`, the `auth` and `guest` aliases in `lib/app/kernel.dart`, the route registrations and the English strings in `assets/lang/en.json`. The package has no executable: every command is `dart run magic:dowel starter:<command>`. Import only `package:magic_starter/magic_starter.dart` (or `package:magic_starter/cli.dart` from a pure Dart dispatcher).

## Boot rules

1. Register `MagicStarterServiceProvider` in `providers`, after `AuthServiceProvider` (and after `NotificationServiceProvider` when `notifications` is on): its `boot()` reads the session the auth provider restored and the push driver the notification provider attached. It is not auto-registered; without it `MagicStarter.manager` falls back to a default manager, prints one debug warning, and no auth listener, push identity or `starter.*` Gate ability exists.
2. Call `MagicStarter.bootstrap(userFactory:, onLogout:, locales:)` from `AppServiceProvider.boot()`. Pass the host's own `userFactory`: without one every screen reads `MagicStarterAuthUser`, and nothing fails to say so.
3. The team callbacks `currentTeam`, `allTeams`, `onSwitch` come as all three or none. A partial set throws `ArgumentError` before any setter runs; `teams` on without them throws `StateError`. Route `onSwitch` through `MagicStarter.switchTeam('$teamId')`: it switches on the backend, applies the answer's user and re-identifies the store billing rail, which a direct `MagicStarterTeamController.instance.switchTeam` call skips.
4. `onLogin` runs after a fresh sign-in (not a restore); `onGuestClaimed` gets the `GuestClaimOutcome` of a guest claim. Both are optional and also have setters (`useLogin`, `useGuestClaimed`). `MagicStarter.manager.onAnalyticsPreferenceChanged` gets the new value after the user changes the `analytics` switch (never on the boot or sign-in apply); re-apply `magic_analytics` identity there. The starter imports no analytics package: with `analytics` on, `applyAnalyticsOptOut` is how the account's choice reaches the host's own (boot, sign-in, the switch, sign-out), and `boot()` throws a `StateError` while it is unset. Pass it to `bootstrap()` (`applyAnalyticsOptOut: (optedOut) => Analytics.setOptOut(optedOut)`, with `magic_analytics` installed in the host through `flutter pub add` and `plugin:install`) and combine a host-level consent there. The starter calls the hook one change at a time, in order, so a hook that awaits is safe; it must not call `MagicStarterAnalyticsPreferenceController.updateAnalyticsPreference` or `applyOnDevice`, `applyCachedOnDevice` or `forgetOnDevice`, which would wait on the call it runs inside (a sign-out is fine).
5. Register work that needs the token at sign-out with `MagicStarter.beforeLogout(hook)`, before this provider boots: its own hooks release the push device and revoke the token with `POST /auth/logout`, and a hook registered after them runs on a dead token. Each hook is bounded to five seconds and a throw is logged. Sign a user out with `MagicStarter.signOut()`: it runs the hooks once, then the `onLogout` callback, which replaces the built-in sign-out, or the built-in one when none is set. A custom `onLogout` must await `Auth.logout()` itself and must not call `MagicStarterAuthController.instance.logout()` (that runs the hooks a second time). Read the guest flag with `MagicStarter.isGuest()`, never `Auth.user()?.get<bool>('is_guest')` inline.

## Feature rules

1. A toggle is read when the manager is first resolved: a feature that is off registers no route and no view key, so `MagicStarter.view.make(key)` throws `StateError`. Guard links and builds with `MagicStarterConfig.has<Feature>Features()`, never an inline `Config.get`.
2. `social_login` needs a bridge: `MagicStarter.useSocialAuth(MagicStarterSocialAuth)`. Without it the provider buttons and the Connected accounts hub row never render. `magic_social_auth` publishes the bridge; the starter never calls its `signOut()`, so the bridge signs its SDK out itself.
3. `billing` needs `billing.web_origin`, an absolute URL with no trailing slash. Unset or empty, the billing screen hides the web checkout button; a relative value makes Stripe refuse the return URL and the error is only logged, so the button does nothing. `billing.billable` is `'user'` or `'team'`, must equal the backend's, and any other value throws `StateError`.
4. `billing` registers the `teams.billing` view key and no route. The host registers a page at `MagicStarterConfig.billingRoute()` (`routes.billing`, default `/teams/billing`) and puts a `MagicStarterBillingController` in the container first (Recipes), since the view resolves its controller and cannot construct one.
5. `notifications` makes the provider declare `<notifications.external_id_prefix><user id>` as the push identity on every `Auth.stateNotifier` change and release it on any sign-out, account deletion included. The prefix defaults to `user_` and must equal the backend's `MAGIC_STARTER_EXTERNAL_ID_PREFIX`: a mismatch is accepted by OneSignal and delivered to nobody. A blank value resolves to `user_`.
6. `support` needs `registerMagicStarterSupportRoutes()` in the route provider; `starter:install` adds it only when `support` was chosen at install. Every `support_*` option needs `support`.
7. `guest_auth` adds no route: it shows "Continue as guest" on login, records the guest token and claims the guest's data at the next sign-in. `RedirectIfAuthenticated` lets a guest session through to the auth pages.
8. Stored and unread: `MagicStarterConfig.requestTimeoutSeconds()` and `maxRetries()`, and `useGuestAuthEntry()`. Do not build on them. `useNewsletterLabel()` is read by the register view alone (the checkbox label when `newsletter` is on), not by the profile newsletter page.

## Route and middleware rules

1. The route groups name the middleware `auth` and `guest`. Register them with `Kernel.registerAll({'auth': () => EnsureAuthenticated(), 'guest': () => RedirectIfAuthenticated()})`; `starter:install` writes this into `lib/app/kernel.dart`.
2. Call `registerMagicStarterAuthRoutes()` and `registerMagicStarterProfileRoutes()` always, and the team, notification and support functions freely: each returns early while its toggle is off. None takes an argument.
3. Paths come from config: `routes.auth_prefix` (`/auth`), `routes.profile_prefix` (`/settings`), `routes.teams_prefix` (`/teams`), `routes.notifications_prefix`, `routes.login`, `routes.home`. Build links with `MagicStarterConfig.*Route()`, never a literal path.
4. `EnsureAuthenticated` sends a signed-out visitor to `routes.login` and records the location with `MagicRouter.setIntendedUrl`; every sign-in lands there, or on `routes.home`. The login and register screens also honour `?next=<in-app path>`. `starter:install` registers its own `lib/app/middleware/` copies instead, which record no intended URL and do not let a guest through; register the package classes for this behaviour.
5. Put a host page inside the starter's shell with `layout: (child) => MagicStarter.view.makeLayout('layout.app', child: child)` and `layoutId: MagicStarterLayoutIds.app`. A different `layoutId` is a separate shell, which rebuilds the layout on every move between them.

## View registry rules

1. Override with `MagicStarter.view.register(key, builder)`, `registerLayout('layout.app' | 'layout.guest', builder)` or `registerModal('modal.confirm' | 'modal.password_confirm' | 'modal.two_factor', builder)`, from any provider's `boot()`. Defaults register only when a key is free, so provider order does not matter.
2. The settings surface is `settings.hub` plus drill-down keys: `profile.profile`, `settings.appearance`, `settings.security.password` (always), `settings.language`, `settings.timezone`, `settings.newsletter`, `settings.changelog`, `settings.security.two_factor`, `settings.security.sessions`, `settings.security.connected_accounts` (behind their toggles). `profile.settings` is not a registered default key.
3. `notifications.list` and `notifications.preferences` live on `magic_notifications`' `Notify.view`. Registering them on `MagicStarter.view` mounts nothing.
4. A slot adds a widget inside a shipped view: `MagicStarter.view.slot(viewKey, slotName, builder)`, registered before the view builds. Only the names a view reads work (`header` and `footer` on the auth views, the hub, `profile.profile` and the team views; `formFooter` on login and register; `afterSection:members` on `teams.settings`); any other name is inert.
5. `makeLayout` hands your layout the child unchanged; under a route group it is go_router's shell navigator. Render it once inside the layout and never key it on the route path: under go_router 18 a path key freezes a page that reads `GoRouterState.of` in `build` when it is left.
6. `dart run magic:dowel starter:publish --tag=views:<key>` copies a view into `lib/resources/views/starter/`, rewrites its relative imports to `package:magic_starter/magic_starter.dart`, and registers it in `AppServiceProvider` under an `as published` import (the barrel exports the original under the same class name). The copy does not follow later releases; `starter:doctor` flags a published view nothing registers.

Every key with its condition and widget: `references/views-and-layouts.md`.

## Theming rules

1. `MagicStarter.useWindTheme(windTheme)` keeps, field by field, what a single setter called before it set. A setter called after it assigns its whole struct, so build that struct from the active theme (`MagicStarter.useLayoutTheme(MagicStarter.layoutTheme.copyWith(...))`) or every field it omits, the Wind-derived colours included, goes back to its stock default. A field set to exactly its stock default, or to exactly what the previous `useWindTheme()` derived for it, reads as unset, and the next `useWindTheme()` replaces it; to keep such a value, set a different one, or set it again after `useWindTheme()` with `copyWith`. `useTheme(MagicStarterTheme)` replaces every sub-theme, so `useButtonTheme()` and `useFieldTheme()` come after it or the host's standard is lost without an error.
2. Every `use*Theme()` assigns the whole struct: a field you leave out goes back to its default. Change one string with `MagicStarter.formTheme.copyWith(...)`, `MagicStarter.modalTheme.copyWith(...)` or the `copyWith` of any other sub-theme.
3. Page geometry is the host's: set `MagicStarter.manager.pageContainerClassName` once from the string your own pages use (default `'max-w-7xl px-4 lg:px-8 pt-6 sm:pt-8 pb-16'`), and never put a `max-w-*` or page `px-*` on a starter page or component.
4. Style with the semantic aliases (`bg-surface`, `text-fg`, `bg-primary`, `border-color-border`, ...) from `MagicStarterTokens.defaultAliases`, passed as `WindThemeData(aliases: ...)`. Wind drops an alias the theme lacks silently, so the class paints nothing.
5. A `className` passed to an `MS` component is appended after the theme and wins on every family it names.

Sub-themes, the button and field arithmetic and the modal presentation: `references/theming.md`.

## Sign-in and identity rules

1. Every shipped sign-in (password, social, two-factor challenge, OTP, guest, handoff) concludes in one internal step that reads a two-factor answer at the top level or under `data`, shows a cancelled deletion, logs in and lands on the intended URL. Drive a sign-in through the controllers (`doLogin`, `doSocialSignIn`, `doTwoFactorChallenge`, ...) rather than calling `Auth.login` with a token yourself, or those steps are skipped.
2. Gated profile calls take `proof:` (`Map<String, String>`): `doEnableTwoFactor`, `doDisableTwoFactor`, `getRecoveryCodes`, `doRegenerateRecoveryCodes`, `doRevokeSession`, `doRevokeOtherSessions`, `doDeleteAccount`, `doSetPassword`. A password account gives `{'password': ...}`, a password-less one `{'code': ...}` or `{'confirmation_token': ...}`, a guest `{}`. Get it with `confirmIdentity(context)` or run the action inside `confirmAndRun(context, controller, action: ...)`.
3. Read a refusal by its `code`, never its message (`step_up_required`, `password_already_set`, `last_login_method`, `owns_shared_teams`, ...).
4. `doDeleteAccount(proof:)` schedules the deletion by default (a sign-in within the grace period cancels it); `immediately: true` skips the grace period. Either way the user is signed out without the before-logout hooks.
5. Call `MagicStarterAuthController.instance.doSocialSignIn(provider)` straight from the tap, with no `await` before it, or a web popup is blocked.
6. A controller of yours that caches one user's or one team's data implements magic's `SessionScoped`; the provider declares the session identity as user plus team, and the host calls `SessionScope.attach()` last in its own provider.

## Recipes

Bootstrap a team app. `User` and `Team` are the host's models. With `teams` on, `starter:install` writes a `Team` that ships `toMagicStarterTeam()` and a `User` with the `currentTeam` and `allTeams` getters. Write the conversion yourself (an extension returning `MagicStarterTeam(id:, name:, photoUrl:, isPersonalTeam:)`) only when a `team.dart` or `user.dart` already existed and `starter:install` skipped it because `--force` was not passed:

```dart
import 'package:magic/magic.dart';
import 'package:magic_starter/magic_starter.dart';

class AppServiceProvider extends ServiceProvider {
  AppServiceProvider(super.app);

  @override
  void register() {}

  @override
  Future<void> boot() async {
    MagicStarter.bootstrap(
      userFactory: (data) => User.fromMap(data),
      onLogout: () async {
        await Auth.logout();
        MagicRoute.to(MagicStarterConfig.loginRoute());
      },
      locales: {
        'en': 'English',
        'tr': 'Türkçe',
      },
      currentTeam: () => User.current.currentTeam?.toMagicStarterTeam(),
      allTeams: () => User.current.allTeams
          .map((team) => team.toMagicStarterTeam())
          .toList(),
      onSwitch: (teamId) => MagicStarter.switchTeam('$teamId'),
    );
  }
}
```

Register the routes and the middleware aliases:

```dart
import 'package:magic/magic.dart';
import 'package:magic_starter/magic_starter.dart';

void registerStarterRoutes() {
  Kernel.registerAll({
    'auth': () => EnsureAuthenticated(),
    'guest': () => RedirectIfAuthenticated(),
  });

  registerMagicStarterAuthRoutes();
  registerMagicStarterProfileRoutes();
  registerMagicStarterTeamRoutes();
  registerMagicStarterNotificationRoutes();
  registerMagicStarterSupportRoutes();
}
```

Mount the billing view (`UsageStat` comes from `magic_payments`, a direct dependency once you name it):

```dart
import 'package:magic/magic.dart';
import 'package:magic_payments/magic_payments.dart';
import 'package:magic_starter/magic_starter.dart';

void registerBilling() {
  Magic.put(
    MagicStarterBillingController(
      usageCopy: (stats) => [
        for (final stat in stats)
          UsageStat(
            key: stat.key,
            used: stat.used,
            limit: stat.limit,
            label: trans('usage.${stat.key}'),
          ),
      ],
      formatNumber: (value) => '$value',
    ),
  );

  if (!MagicStarterConfig.hasBillingFeatures()) return;

  MagicRoute.group(
    middleware: ['auth'],
    layoutId: MagicStarterLayoutIds.app,
    layout: (child) => MagicStarter.view.makeLayout('layout.app', child: child),
    routes: () {
      MagicRoute.page(
        MagicStarterConfig.billingRoute(),
        () => MagicStarter.view.make('teams.billing'),
      );
    },
  );
}
```

Replace a screen and add a slot:

```dart
import 'package:flutter/widgets.dart';
import 'package:magic/magic.dart';
import 'package:magic_starter/magic_starter.dart';

class BrandedLoginView extends StatelessWidget {
  const BrandedLoginView({super.key});

  @override
  Widget build(BuildContext context) => WText('Sign in', className: 'text-fg');
}

void customiseStarter() {
  MagicStarter.view.register('auth.login', () => const BrandedLoginView());

  MagicStarter.view.slot('settings.hub', 'footer', (context) {
    return WText('v1', className: 'text-sm text-fg-muted');
  });
}
```

Theme from the host palette, then the button and field standards:

```dart
import 'package:magic/magic.dart';
import 'package:magic_starter/magic_starter.dart';

void themeStarter(WindThemeData windTheme) {
  const String standard = 'px-5 py-[11px] text-[17px] leading-[22px]';

  MagicStarter.useWindTheme(windTheme);
  MagicStarter.useButtonTheme(
    const MagicStarterButtonTheme(
      shapeClassName: 'rounded-full',
      smClassName: standard,
      mdClassName: standard,
      lgClassName: standard,
    ),
  );
  MagicStarter.useFormTheme(
    MagicStarter.formTheme.copyWith(
      inputClassName: 'w-full py-[10px] min-h-11 text-[17px] leading-[22px]',
    ),
  );
}
```

Run a gated action with step-up proof from a view of your own:

```dart
import 'package:flutter/widgets.dart';
import 'package:magic/magic.dart';
import 'package:magic_starter/magic_starter.dart';

Future<void> deleteAccount(BuildContext context) async {
  final MagicStarterProfileController controller =
      MagicStarterProfileController.instance;

  await confirmAndRun(
    context,
    controller,
    variant: ConfirmDialogVariant.danger,
    action: (proof) => controller.doDeleteAccount(proof: proof),
  );
}
```

Turn a plan-gated `403` into the upgrade prompt:

```dart
import 'package:magic/magic.dart';
import 'package:magic_starter/magic_starter.dart';

Future<void> analyse(String id) async {
  final MagicResponse response = await Http.post('/monitors/$id/analyze');
  if (response.successful) return;

  final PlanUpgradeRequirement? requirement =
      PlanUpgradeRequirement.fromResponse(response);
  if (requirement != null) {
    UpgradePrompt.show(requirement);
  }
}
```

## Testing

No mocking library. In `setUp()` call `MagicApp.reset()` and `Magic.flush()`, then `setUpMagicStarterForTests()` (or pass a configured `MagicStarterManager`), bind a contract fake for the network (`Magic.singleton('network', () => FakeDriver())`, a class that `implements NetworkDriver` and records the method, URL and payload) and set toggles with `Config.set('magic_starter.features.<key>', true)` before the manager is first resolved. Assert the request a controller sends and its state (`controller.isSuccess`, `hasErrors`), never a faked sign-in. `MagicStarter.resetFallbackManagerForTests()` clears the unbound fallback between tests. Dispose a controller's `ValueNotifier`s in `tearDown()`.

## References

- `references/views-and-layouts.md`: every view, layout and modal key with its condition, the slots, the shell hooks (navigation, header, sidebar footer, page chrome, bottom nav), publishing.
- `references/controllers-and-routes.md`: the controllers and what each owns, every route with its path and middleware, sign-in completion and session scope.
- `references/theming.md`: the sub-themes, `useWindTheme`, the button and field standards, modal presentation.
- `references/backend-contract.md`: the `api/v1` endpoints each controller calls, the backend keys that must match, the refusal codes.
