---
name: mobile-state-restoration
description: Flutter state restoration and app lifecycle management — RestorationMixin, restorationId, WidgetsBindingObserver lifecycle events, iOS state preservation, Android process death, resume/background realtime handling, draft auto-save. MANDATORY TRIGGERS - "state restoration", "app lifecycle", "background fetch", "restoration id", "restorable", "foreground background", "ios state preservation", "android process death".
allowed-tools: Read, Glob, Edit, Write
---

# Skill: mobile-state-restoration

## When to use

Adding a new page with user-entered state (forms, scroll position, filters),
implementing a background/foreground transition handler, or debugging
"blank screen after resume" / "lost draft" reports.

---

## Inputs

- Page or feature slug
- List of user-entered fields or interactive state that must survive
  process death or backgrounding

---

## Steps

### 1. restorationScopeId on the app root

The root `MaterialApp` (or `MaterialApp.router`) must declare a
`restorationScopeId`. Set this once in your app's root widget:

```dart
// lib/my_app.dart
MaterialApp.router(
  restorationScopeId: 'app_root',
  ...
)
```

Every page that registers a `RestorationMixin` must have its own unique
`restorationId` on its route. `GoRouter` routes assign this via the
`pageBuilder`'s `key` — use the route path as the restoration ID.

### 2. RestorationMixin on stateful pages

Any page that holds more than one user-entered field must mix in
`RestorationMixin`:

```dart
// lib/features/post/presentation/pages/composer_page.dart
class _ComposerPageState extends State<ComposerPage>
    with RestorationMixin {

  final RestorableTextEditingController _bodyController =
      RestorableTextEditingController();
  final RestorableString _selectedTag = RestorableString('');
  final RestorableBool _isSubmitting = RestorableBool(false);

  @override
  String get restorationId => 'composer_page';

  @override
  void restoreState(RestorationBucket? oldBucket, bool initialRestore) {
    registerForRestoration(_bodyController, 'body_text');
    registerForRestoration(_selectedTag, 'selected_tag');
    registerForRestoration(_isSubmitting, 'is_submitting');
  }

  @override
  void dispose() {
    _bodyController.dispose();
    _selectedTag.dispose();
    _isSubmitting.dispose();
    super.dispose();
  }
}
```

Restoration IDs must be:
- Unique within the restoration scope (the page's bucket).
- Stable across app versions (never rename them).
- Lowercase with underscores.

Reference: [Flutter State Restoration](https://api.flutter.dev/flutter/widgets/RestorationMixin-mixin.html)

### 3. RestorableProperty types

Use the built-in `RestorableProperty` subclasses wherever possible:

| State type | Restorable type |
|-----------|-----------------|
| `String` | `RestorableString` |
| `int` | `RestorableInt` |
| `bool` | `RestorableBool` |
| `double` | `RestorableDouble` |
| `DateTime?` | `RestorableDateTime` |
| `TextEditingController` | `RestorableTextEditingController` |
| Custom (serializable) | `RestorableValue<T>` with custom `toPrimitives`/`fromPrimitives` |
| Enum | `RestorableEnumN<T>` (null-safe) via the `restorable_change_notifier` pattern |

For a custom type (e.g. `FeedFilter`):

```dart
class RestorableFeedFilter extends RestorableValue<FeedFilter> {
  @override
  FeedFilter createDefaultValue() => FeedFilter.forYou;

  @override
  void didUpdateValue(FeedFilter? oldValue) {
    notifyListeners();
  }

  @override
  FeedFilter fromPrimitives(Object? data) =>
      FeedFilter.values.firstWhere((e) => e.name == data);

  @override
  Object? toPrimitives() => value.name;
}
```

### 4. WidgetsBindingObserver for lifecycle events

Each feature Bloc that manages a live subscription or network resource
must respond to lifecycle events:

```dart
// lib/core/lifecycle/app_lifecycle_manager.dart
@lazySingleton
class AppLifecycleManager extends WidgetsBindingObserver {
  AppLifecycleManager(this._realtime, this._outbox, this._session) {
    WidgetsBinding.instance.addObserver(this);
  }

  @override
  void didChangeAppLifecycleState(AppLifecycleState state) {
    switch (state) {
      case AppLifecycleState.paused:
        _onPaused();
      case AppLifecycleState.resumed:
        _onResumed();
      case AppLifecycleState.detached:
        _onDetached();
      case AppLifecycleState.inactive:
        // Transitional — do not trigger heavy work here
        break;
      case AppLifecycleState.hidden:
        // iOS multitask switcher — treat like paused
        _onPaused();
    }
  }

  void _onPaused() {
    _realtime.pauseAll();           // pause realtime subscriptions
    // If biometric re-auth is enabled: clear in-memory access token
    if (_session.requiresReauthOnResume) _session.clearAccessToken();
  }

  void _onResumed() {
    _realtime.resumeAll();          // resubscribe to all channels
    _outbox.drain();                // flush any pending mutations
    _session.refreshIfNeeded();     // refresh access token if near expiry
  }

  void _onDetached() {
    _realtime.disconnect();         // full disconnect on process teardown
  }
}
```

If your app has channels that only make sense during a specific window
(e.g. business hours, market hours, or an event window), pause those
channels outside that window via a small helper — see §12 pattern in the
`push-notifications` skill for a "quiet hours" example.

### 5. iOS state preservation (UISceneStorage)

iOS uses `UIScene` lifecycle for state preservation. The Flutter engine
handles the bridge automatically when `restorationScopeId` is set.

For scenes: iOS saves the `RestorationBucket` tree and restores it when the
app returns from background. No additional iOS-native code is needed for the
Flutter layer — the engine bridges `UISceneStorage` automatically.

For push notifications arriving while backgrounded:
- The `firebase_messaging` background handler runs in a separate Dart
  isolate. Do not access `BuildContext` or Flutter state from it.
- Use a local cache (e.g. a Hive `inbox_cache` box) to persist the unread
  count, so the badge is accurate when the app resumes.

Reference: [Apple Scene-based state preservation](https://developer.apple.com/documentation/uikit/uiscene)

### 6. Android process death

Android can kill the process at any time while in the background. The
`RestorationMixin` state is persisted by the engine to a `Bundle` before
the process dies and restored on relaunch.

Additional Android-specific concerns:
- If you use Drift (or another local DB), re-open it in `bootstrap.dart`
  on every cold start. Ensure migrations are idempotent.
- In-memory state (access token in `SessionManager`) is lost on process
  death — `SessionManager` should re-read the refresh token from secure
  storage and issue a new access token on first API call.
- Any offline mutation queue persisted locally should survive process
  death and drain automatically on reconnect.

Reference: [Android Process Death](https://developer.android.com/topic/libraries/architecture/saving-states)

### 7. Deferring rebuilds until first frame

Avoid loading heavy data before the first frame is painted:

```dart
// lib/bootstrap.dart
void bootstrap(Flavor flavor) async {
  WidgetsFlutterBinding.ensureInitialized();

  // Defer first frame until DI and DB are ready
  WidgetsBinding.instance.deferFirstFrame();

  await _initDependencies(flavor);   // GetIt.allReady()

  WidgetsBinding.instance.allowFirstFrame();
  runApp(const MyApp());
}
```

### 8. Foreground / background workflow summary

| Event | Action |
|-------|--------|
| `paused` | Pause realtime subs; clear in-memory token if re-auth enabled |
| `inactive` | No action (transitional state) |
| `hidden` | Treat as `paused` (iOS task switcher) |
| `resumed` | Resume realtime subs; drain outbox; refresh token; emit a refresh event |
| `detached` | Full disconnect + flush |

### 9. Edge cases

**Multi-step flows (onboarding, verification):**
Persist each step's completion in local storage (e.g. a `verification_draft`
box) so the user can resume from the last step after backgrounding. The
current step index is a `RestorableInt` on the flow's page.

**Composer drafts auto-save:**
`ComposerBloc` debounces keystrokes (500 ms) and writes to a local
`composer_drafts` store. On cold start, if an unsubmitted draft exists,
surface a "Continue draft?" dialog. On explicit send or discard, delete
the draft entry.

**Message scroll position:**
`ChatPage`'s `ScrollController` offset is stored in `RestorationBucket`
via a `RestorableDouble`. On resume, scroll is restored before the first
frame via `WidgetsBinding.addPostFrameCallback`.

---

## Output

For each new page with user-entered state:
- `restorationScopeId` present on the route.
- `RestorationMixin` mixed into the `State`.
- All user-entered fields registered via `registerForRestoration`.
- `WidgetsBindingObserver` wired in `AppLifecycleManager` for any new
  Bloc that holds a live resource.
- Restoration ID documented in a `///` comment on the `restorationId`
  getter.

---

## Anti-patterns

- Omitting `RestorationMixin` on a form page — user loses data on process death.
- Using the widget's `runtimeType.toString()` as `restorationId` — class
  renames will silently break restoration.
- Calling `_realtime.resumeAll()` from `inactive` state — the app may
  immediately go back to `paused` (e.g. FaceID prompt).
- Writing the refresh token to a Hive box instead of `flutter_secure_storage`
  — the box is not encrypted by default.
- Starting realtime subscriptions before `GetIt.allReady()` — the channel
  registry may not be registered yet.

---

## See also

- `.claude/skills/mobile-security/SKILL.md` — token clearing on pause
- your project's frontend architecture doc — Realtime lifecycle
- your project's mobile standards doc — state restoration rule
