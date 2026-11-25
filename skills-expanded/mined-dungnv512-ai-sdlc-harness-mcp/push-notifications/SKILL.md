---
name: push-notifications
description: Push notification setup for Flutter apps — Firebase Messaging, APNs auth key, iOS provisional permission, Android 13+ POST_NOTIFICATIONS, notification channels, notification categories/actions, foreground/background handlers, silent push, deep-link routing from tap, payload schema, badge updates, quiet-hours rules. MANDATORY TRIGGERS - "push", "fcm", "apns", "notification", "firebase_messaging", "notification channel", "post_notifications", "silent push", "notification category", "deep link from notification".
allowed-tools: Read, Glob, Edit, Write
---

# Skill: push-notifications

## When to use

Setting up push notifications for a new notification type, adding an
Android notification channel, wiring a notification tap to a deep-link
route, or debugging missing/silent notifications.

---

## Inputs

- Notification type slug (e.g. `comment_reply`, `vote_milestone`)
- Target platforms (iOS / Android / both)
- Deep-link route the notification should open

---

## Steps

### 1. Firebase setup

**Required files (never commit to repo — sourced from CI secrets):**
- Android: `android/app/google-services.json`
- iOS: `ios/Runner/GoogleService-Info.plist`

Both files are gitignored. CI materializes them from encrypted secrets
before each build.

**APNs configuration:** Use the `.p8` auth key (not the `.p12` cert) in
Firebase Console → Project Settings → Cloud Messaging → Apple app
configuration. The `.p8` key does not expire; the `.p12` cert does. Store
the `.p8` in the CI secrets vault, not the repo.

Reference: [FCM docs](https://firebase.google.com/docs/cloud-messaging)

### 2. firebase_messaging plugin wiring

```dart
// lib/core/push/push_service.dart
@lazySingleton
class PushService {
  PushService(this._messaging, this._deepLinkRouter, this._db);

  final FirebaseMessaging _messaging;
  final DeepLinkRouter _deepLinkRouter;
  final AppDatabase _db;

  Future<void> init() async {
    // iOS: request permission (use provisional for first launch)
    await _requestIOSPermission();

    // Get + persist FCM token
    final token = await _messaging.getToken();
    if (token != null) await _persistToken(token);
    _messaging.onTokenRefresh.listen(_persistToken);

    // Foreground message handler
    FirebaseMessaging.onMessage.listen(_onForegroundMessage);

    // Tapped from background
    FirebaseMessaging.onMessageOpenedApp.listen(_onNotificationTap);

    // Cold-start: check if app was opened from a terminated-state notification
    final initial = await _messaging.getInitialMessage();
    if (initial != null) _onNotificationTap(initial);
  }

  Future<void> _requestIOSPermission() async {
    await _messaging.requestPermission(
      alert: true,
      badge: true,
      sound: true,
      provisional: true,   // Deliver quietly to Notification Center without prompt
    );
  }
}
```

Reference: [firebase_messaging pub.dev](https://pub.dev/packages/firebase_messaging)

### 3. iOS provisional permission

Use `provisional: true` on first launch so notifications are delivered
silently to Notification Center without showing the system permission prompt.
This gives users a chance to see notifications before deciding whether
to grant full permission.

Show the full permission prompt only when the user explicitly navigates
to Settings → Notifications and toggles "Push notifications" on. At that
point, call `requestPermission` with `provisional: false`.

Reference: [Apple Push Notification Service](https://developer.apple.com/documentation/usernotifications)

### 4. Android 13+ POST_NOTIFICATIONS

Runtime permission required on Android 13+ (API 33+). Request just-in-time:

```dart
// lib/features/settings/presentation/bloc/notification_settings_bloc.dart
Future<void> _onEnableNotifications(event, emit) async {
  // PERM: POST_NOTIFICATIONS — user-initiated in notification settings screen
  final status = await Permission.notification.request();
  if (status.isGranted) {
    await _pushService.subscribeAll();
    emit(state.copyWith(notificationsEnabled: true));
  } else if (status.isPermanentlyDenied) {
    _effects.add(const ShowOpenAppSettings());
  }
}
```

Do not request `POST_NOTIFICATIONS` at app launch. Show a rationale screen
first explaining what kinds of notifications the user will receive (e.g.
replies, votes, alerts).

Reference: [Android 13 notification permission](https://developer.android.com/develop/ui/views/notifications/notification-permission)

### 5. Notification channels (Android 8+)

Create channels at app startup in `PushService.init()`:

```dart
// lib/core/push/notification_channels.dart
class NotificationChannels {
  static const messages = 'app_messages';
  static const comments = 'app_comments';
  static const votes = 'app_votes';
  static const system = 'app_system';

  static Future<void> create(FlutterLocalNotificationsPlugin plugin) async {
    const androidPlugin = AndroidFlutterLocalNotificationsPlugin;
    await plugin
        .resolvePlatformSpecificImplementation<androidPlugin>()
        ?.createNotificationChannel(
          const AndroidNotificationChannel(
            messages,
            'Messages',
            description: 'Direct message notifications',
            importance: Importance.high,
            playSound: true,
          ),
        );
    // Repeat for comments, votes, system...
  }
}
```

Reference: [Notification channels](https://developer.android.com/develop/ui/views/notifications/channels)

### 6. Notification categories and inline actions

**iOS notification categories:**

```dart
// Register categories at init time
await _messaging.setForegroundNotificationPresentationOptions(
  alert: true,
  badge: true,
  sound: true,
);
// iOS notification actions are configured via UNUserNotificationCenter
// in native code (AppDelegate.swift) — see ios/Runner/AppDelegate.swift
```

**Android reply action (inline reply for chat messages):**

```dart
final androidDetails = AndroidNotificationDetails(
  NotificationChannels.messages,
  'Messages',
  actions: [
    AndroidNotificationAction(
      'reply',
      'Reply',
      inputs: [
        AndroidNotificationActionInput(label: 'Type a message...'),
      ],
    ),
    AndroidNotificationAction('mark_read', 'Mark as read'),
  ],
);
```

### 7. Foreground vs background message handlers

| State | Handler | Behavior |
|-------|---------|---------|
| Foreground | `FirebaseMessaging.onMessage` | Show in-app banner via `OverlayEntry`; do NOT show OS notification |
| Background (tapped) | `FirebaseMessaging.onMessageOpenedApp` | Resolve `deepLink` → `GoRouter.go(path)` |
| Terminated (cold start) | `FirebaseMessaging.getInitialMessage()` | Delay route until session resolves; check in `bootstrap.dart` |
| Background (data-only) | `FirebaseMessaging.onBackgroundMessage` | Top-level isolate function; update local badge count |

Background handler must be a top-level function (not a class method):

```dart
// lib/core/push/push_background_handler.dart
@pragma('vm:entry-point')
Future<void> firebaseMessagingBackgroundHandler(RemoteMessage message) async {
  // Minimal work only — cannot access BuildContext
  await Firebase.initializeApp();
  final count = (await _readBadgeCount()) + 1;
  await _writeBadgeCount(count);
}
```

Register in `main_*.dart` before `runApp`:
```dart
FirebaseMessaging.onBackgroundMessage(firebaseMessagingBackgroundHandler);
```

### 8. Silent / data-only pushes

For background data sync (unread count refresh, feed update signals):

Push payload:
```json
{
  "data": {
    "type": "unread_count_update",
    "count": "5"
  },
  "content_available": 1
}
```

On iOS, `content-available: 1` is required. This wakes the app in the
background but does NOT show a notification. The background handler updates
the local `notifications` table and the app badge.

### 9. Tap → deep link → route

Example payload schema — adapt fields to your app's notification model,
but keep `type` + `deepLink` as the routing contract:

```json
{
  "type": "comment.reply",
  "subjectId": "post:01HXXXX",
  "deepLink": "app://post/01HXXXX?focus=comment:01HYYYY",
  "ts": "2026-05-29T07:00:00Z"
}
```

Resolution in `DeepLinkRouter`:
```dart
void handleNotificationTap(RemoteMessage message) {
  final deepLink = message.data['deepLink'];
  if (deepLink == null) return;
  // Validate scheme before routing — do not route arbitrary URLs
  final uri = Uri.tryParse(deepLink);
  if (uri == null || !_isAllowedScheme(uri)) return;
  router.go(_toInternalPath(uri));
}

bool _isAllowedScheme(Uri uri) =>
    uri.scheme == 'app' ||
    (uri.scheme == 'https' && uri.host == 'example.com');
```

### 10. Badge updates

**iOS badge count:** Set via `firebase_messaging`:
```dart
await FirebaseMessaging.instance.setForegroundNotificationPresentationOptions(
  badge: true,
);
// Server sends badge count in the APNs payload `aps.badge` field.
```

**Android badge count:** Managed automatically by the OS from the notification
channel's unread count. Use `FlutterLocalNotificationsPlugin` to set a
specific number if needed.

### 11. Push token refresh and persistence

```dart
void _persistToken(String token) async {
  // Store in local storage (non-sensitive device token, not an auth token)
  await _db.settingsDao.upsert(key: 'fcm_token', value: token);
  // Sync to backend
  await _notificationApi.registerToken(token, platform: _platform);
}
```

On sign-out: unregister the FCM token from the backend and delete it from
local storage:
```dart
await FirebaseMessaging.instance.deleteToken();
await _db.settingsDao.delete(key: 'fcm_token');
await _notificationApi.unregisterToken();
```

### 12. Quiet-hours / do-not-disturb windows

If your app has a natural "off hours" window for a notification category
(e.g. non-urgent alerts tied to business hours, trading hours, or a
user-configurable quiet period), silence or defer delivery client-side as
a belt-and-suspenders guard on top of server-side scheduling:

```dart
// lib/core/lifecycle/quiet_hours.dart
bool get isWithinActiveWindow {
  final now = DateTime.now().toUtc().add(appTimeZoneOffset);
  if (!activeWeekdays.contains(now.weekday)) return false;
  return now.hour >= activeWindowStartHour && now.hour < activeWindowEndHour;
}
```

The backend should also respect this — time-sensitive push notifications
should carry a `scheduledFor` field and the push worker should delay
delivery accordingly. The client-side check is a secondary guard, not the
source of truth.

---

## Output

- `PushService.init()` wired in `bootstrap.dart`
- New notification type has its own channel (Android) or category (iOS)
- Notification tap resolves to the correct deep-link route
- `POST_NOTIFICATIONS` requested just-in-time with a `// PERM:` comment
- Token refresh persisted and synced to backend

---

## Anti-patterns

- Showing an OS notification in the foreground handler — show an in-app
  banner instead.
- Routing arbitrary URLs from push payloads without scheme validation —
  open redirect vulnerability.
- Storing the APNs `.p12` cert in the repo — must be in CI secrets.
- Calling `FirebaseMessaging.requestPermission()` at cold start on Android 13+ —
  must be just-in-time.
- Processing push payloads that contain user PII (email, name, message body) —
  payload carries IDs only; content is fetched after navigation.

---

## See also

- `.claude/skills/deep-linking/SKILL.md` — route resolution from notification tap
- `.claude/skills/ios-release/SKILL.md` — APNs entitlement, background modes
- `.claude/skills/android-release/SKILL.md` — FCM setup, manifest permissions
- your project's frontend architecture doc — Push & deep links
