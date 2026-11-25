---
name: android-notifications-push
description: |
  Push notification and local notification patterns for Android - FCM setup, FirebaseMessagingService, notification channels, NotificationCompat.Builder, deep-link on tap via PendingIntent and NavDeepLinkBuilder, foreground vs background delivery, POST_NOTIFICATIONS permission on Android 13+, data-only vs notification messages, grouping, and badges. Use this skill whenever adding push notifications, configuring Firebase Cloud Messaging, showing local notifications, handling notification taps, or creating notification channels. Trigger on phrases like "push notification", "FCM", "Firebase messaging", "notification channel", "local notification", "notification tap", "POST_NOTIFICATIONS", "data message", or "notification badge".
---

# Android Notifications and Push (FCM)

## Core Principles

- Create notification channels once at app startup, never lazily on first use.
- Every notification must belong to a channel — the system ignores notifications without one on API 26+.
- Request POST_NOTIFICATIONS permission before showing any notification on Android 13+ (API 33+).
- Keep FirebaseMessagingService thin: parse the message payload, delegate to a use case or repository.
- Data-only FCM messages always arrive in onMessageReceived; notification messages only arrive there when the app is in the foreground.
- Deep-link destinations on tap must be validated exactly as external deep links — they are untrusted input.

---

## Project Setup

### Gradle dependencies

```kotlin
// build.gradle.kts (app module)
dependencies {
    implementation(platform("com.google.firebase:firebase-bom:33.1.0"))
    implementation("com.google.firebase:firebase-messaging-ktx")
    implementation("androidx.core:core-ktx:1.13.1")          // NotificationCompat
    implementation("androidx.navigation:navigation-compose:2.7.7")
}
```

Add `google-services.json` to the `app/` directory and apply the plugin:

```kotlin
// app/build.gradle.kts
plugins {
    id("com.google.gms.google-services")
}
```

```kotlin
// root build.gradle.kts
plugins {
    id("com.google.gms.google-services") version "4.4.2" apply false
}
```

---

## Notification Channels

Create channels once in `Application.onCreate()` — creating an existing channel is a no-op after the first call.

```kotlin
// core/notifications/NotificationChannels.kt
object NotificationChannels {
    const val CHANNEL_ORDERS    = "orders"
    const val CHANNEL_PROMOTIONS = "promotions"
    const val CHANNEL_REMINDERS  = "reminders"
}

fun createNotificationChannels(context: Context) {
    if (Build.VERSION.SDK_INT < Build.VERSION_CODES.O) return
    val manager = context.getSystemService(NotificationManager::class.java)

    manager.createNotificationChannels(
        listOf(
            NotificationChannel(
                NotificationChannels.CHANNEL_ORDERS,
                context.getString(R.string.channel_orders_name),
                NotificationManager.IMPORTANCE_HIGH
            ).apply {
                description = context.getString(R.string.channel_orders_description)
                enableLights(true)
                lightColor = Color.BLUE
            },
            NotificationChannel(
                NotificationChannels.CHANNEL_PROMOTIONS,
                context.getString(R.string.channel_promotions_name),
                NotificationManager.IMPORTANCE_DEFAULT
            ),
            NotificationChannel(
                NotificationChannels.CHANNEL_REMINDERS,
                context.getString(R.string.channel_reminders_name),
                NotificationManager.IMPORTANCE_HIGH
            ).apply {
                description = context.getString(R.string.channel_reminders_description)
            }
        )
    )
}
```

Call from `Application`:

```kotlin
class App : Application() {
    override fun onCreate() {
        super.onCreate()
        createNotificationChannels(this)
        // other initialization...
    }
}
```

Anti-pattern: creating channels in a fragment, ViewModel, or lazy block — if the first notification arrives before lazy initialization, it silently fails.

---

## POST_NOTIFICATIONS Permission (Android 13+)

Declare in `AndroidManifest.xml`:

```xml
<uses-permission android:name="android.permission.POST_NOTIFICATIONS" />
```

Request it just before the user enables notifications in settings, following the same pattern as other runtime permissions. See **android-permissions-device-apis** for the full rationale/permanent-denial flow.

```kotlin
// In a Root composable
val notificationPermLauncher = rememberLauncherForActivityResult(
    ActivityResultContracts.RequestPermission()
) { granted ->
    viewModel.onAction(SettingsAction.OnNotificationPermissionResult(granted))
}

// Launched when user taps "Enable push notifications"
if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.TIRAMISU) {
    notificationPermLauncher.launch(Manifest.permission.POST_NOTIFICATIONS)
} else {
    viewModel.onAction(SettingsAction.OnNotificationPermissionResult(true))
}
```

Check before showing a local notification:

```kotlin
fun canPostNotifications(context: Context): Boolean {
    return if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.TIRAMISU) {
        ContextCompat.checkSelfPermission(
            context, Manifest.permission.POST_NOTIFICATIONS
        ) == PackageManager.PERMISSION_GRANTED
    } else {
        NotificationManagerCompat.from(context).areNotificationsEnabled()
    }
}
```

---

## FirebaseMessagingService

```kotlin
class AppMessagingService : FirebaseMessagingService() {

    // Injected via Koin (see android-di-koin for service injection)
    private val tokenRepository: FcmTokenRepository by inject()
    private val notificationHelper: NotificationHelper by inject()

    override fun onNewToken(token: String) {
        // Called when FCM assigns or rotates the device token.
        // Upload to your backend so you can send targeted pushes.
        CoroutineScope(Dispatchers.IO + SupervisorJob()).launch {
            tokenRepository.uploadToken(token)
        }
    }

    override fun onMessageReceived(message: RemoteMessage) {
        // Called for:
        //   - ALL data-only messages regardless of app state
        //   - Notification messages ONLY when app is in the foreground
        val title   = message.notification?.title
            ?: message.data["title"]
            ?: return
        val body    = message.notification?.body
            ?: message.data["body"]
            ?: return
        val channel = message.data["channel"]
            ?: NotificationChannels.CHANNEL_ORDERS
        val deepLink = message.data["deepLink"]

        notificationHelper.showPush(
            title    = title,
            body     = body,
            channel  = channel,
            deepLink = deepLink
        )
    }
}
```

Register in `AndroidManifest.xml`:

```xml
<service
    android:name=".AppMessagingService"
    android:exported="false">
    <intent-filter>
        <action android:name="com.google.firebase.MESSAGING_EVENT" />
    </intent-filter>
</service>
```

---

## Data-Only vs Notification Messages

| Message type          | App foreground     | App background / killed            |
|-----------------------|--------------------|------------------------------------|
| Notification message  | `onMessageReceived` | System tray — FCM shows it automatically, `onMessageReceived` NOT called |
| Data-only message     | `onMessageReceived` | `onMessageReceived` (high-priority) |

Prefer **data-only messages** for production apps so you control the notification appearance in all states and can apply deep-link logic uniformly.

Send data-only from the server:
```json
{
  "to": "<device_token>",
  "priority": "high",
  "data": {
    "title": "Your order shipped",
    "body": "Estimated delivery: tomorrow",
    "channel": "orders",
    "deepLink": "myapp://orders/order_123"
  }
}
```

---

## Local Notifications with NotificationCompat

```kotlin
// core/notifications/NotificationHelper.kt
class NotificationHelper(private val context: Context) {

    private val manager = NotificationManagerCompat.from(context)
    private var nextId  = AtomicInteger(1_000)

    fun showPush(
        title: String,
        body: String,
        channel: String,
        deepLink: String? = null,
        notificationId: Int = nextId.getAndIncrement()
    ) {
        if (!canPostNotifications(context)) return

        val pendingIntent = buildTapIntent(deepLink, notificationId)

        val notification = NotificationCompat.Builder(context, channel)
            .setSmallIcon(R.drawable.ic_notification)
            .setContentTitle(title)
            .setContentText(body)
            .setStyle(NotificationCompat.BigTextStyle().bigText(body))
            .setAutoCancel(true)
            .setContentIntent(pendingIntent)
            .setPriority(NotificationCompat.PRIORITY_HIGH)
            .build()

        manager.notify(notificationId, notification)
    }

    private fun buildTapIntent(deepLink: String?, notificationId: Int): PendingIntent {
        val flags = PendingIntent.FLAG_UPDATE_CURRENT or PendingIntent.FLAG_IMMUTABLE

        return if (deepLink != null) {
            // NavDeepLinkBuilder creates a back stack so Back works naturally
            NavDeepLinkBuilder(context)
                .setGraph(R.navigation.nav_graph)
                .setDestination(R.id.orderDetailFragment) // or typed route
                .setArguments(Bundle().apply {
                    putString("deepLink", deepLink)
                })
                .createPendingIntent()
        } else {
            val intent = Intent(context, MainActivity::class.java).apply {
                action = Intent.ACTION_MAIN
                addCategory(Intent.CATEGORY_LAUNCHER)
                addFlags(Intent.FLAG_ACTIVITY_NEW_TASK)
            }
            PendingIntent.getActivity(context, notificationId, intent, flags)
        }
    }
}
```

Anti-pattern: using `FLAG_MUTABLE` when the extra data is set at build time and will not be modified by external processes.

---

## Deep-Link on Notification Tap (Compose Navigation)

For Compose Navigation, build the tap intent from a validated URI:

```kotlin
fun buildDeepLinkPendingIntent(
    context: Context,
    uri: Uri,
    notificationId: Int
): PendingIntent {
    val intent = Intent(Intent.ACTION_VIEW, uri, context, MainActivity::class.java).apply {
        addFlags(Intent.FLAG_ACTIVITY_SINGLE_TOP)
    }
    return PendingIntent.getActivity(
        context,
        notificationId,
        intent,
        PendingIntent.FLAG_UPDATE_CURRENT or PendingIntent.FLAG_IMMUTABLE
    )
}
```

Declare the deep-link route in the Compose nav graph:

```kotlin
composable(
    route = "orders/{orderId}",
    deepLinks = listOf(navDeepLink { uriPattern = "myapp://orders/{orderId}" })
) { backStackEntry ->
    val orderId = backStackEntry.arguments?.getString("orderId") ?: return@composable
    OrderDetailRoute(orderId = orderId)
}
```

Always validate the URI components before acting on them — see **android-deep-links**.

---

## Foreground vs Background Delivery

When the app is in the foreground and a push arrives, `onMessageReceived` is called but no system notification appears for notification messages. You must call `NotificationHelper.showPush(...)` yourself.

Good pattern:

```kotlin
override fun onMessageReceived(message: RemoteMessage) {
    // Your code runs here regardless of app state for data-only messages.
    // For notification messages: only runs when app is foregrounded.
    notificationHelper.showPush(
        title    = message.data["title"] ?: message.notification?.title ?: return,
        body     = message.data["body"]  ?: message.notification?.body  ?: return,
        channel  = message.data["channel"] ?: NotificationChannels.CHANNEL_ORDERS,
        deepLink = message.data["deepLink"]
    )
}
```

Anti-pattern: relying solely on the FCM SDK to display notification messages — you lose control of appearance, channel assignment, and deep-link handling when the app is in the background.

---

## Notification Grouping

Group related notifications so the tray does not fill up for apps that post many updates:

```kotlin
private const val GROUP_KEY_ORDERS = "com.example.app.ORDERS"

fun showOrderNotification(orderId: String, title: String, body: String) {
    val notifId = orderId.hashCode()

    // Individual notification
    val notification = NotificationCompat.Builder(context, NotificationChannels.CHANNEL_ORDERS)
        .setSmallIcon(R.drawable.ic_notification)
        .setContentTitle(title)
        .setContentText(body)
        .setGroup(GROUP_KEY_ORDERS)
        .setAutoCancel(true)
        .build()
    manager.notify(notifId, notification)

    // Summary notification (required on API < 28 to trigger grouping; good practice on all)
    val summary = NotificationCompat.Builder(context, NotificationChannels.CHANNEL_ORDERS)
        .setSmallIcon(R.drawable.ic_notification)
        .setGroup(GROUP_KEY_ORDERS)
        .setGroupSummary(true)
        .setAutoCancel(true)
        .build()
    manager.notify(SUMMARY_ID_ORDERS, summary)
}
```

---

## Notification Badges

On API 26+ the launcher badge count is tied to the number of active notifications. To set it explicitly:

```kotlin
NotificationCompat.Builder(context, channel)
    .setBadgeIconType(NotificationCompat.BADGE_ICON_SMALL)
    .setNumber(unreadCount)   // shown in long-press badge on supported launchers
    // ...
    .build()
```

To clear the badge, cancel all associated notifications:

```kotlin
NotificationManagerCompat.from(context).cancelAll()
```

---

## FCM Token Management

```kotlin
// Fetch the current token (call once after sign-in)
FirebaseMessaging.getInstance().token.addOnCompleteListener { task ->
    if (task.isSuccessful) {
        val token = task.result
        // Upload to backend
    }
}
```

Token rotation rules:
- Rotates on app reinstall, factory reset, or FCM token refresh.
- `onNewToken` in `FirebaseMessagingService` is always the authoritative source.
- Invalidate the old token on the server when the user signs out.

---

## Checklist: Adding Push Notifications

- [ ] `google-services.json` placed in `app/`
- [ ] `FirebaseMessagingService` subclass registered in manifest
- [ ] Notification channels created in `Application.onCreate()`
- [ ] POST_NOTIFICATIONS permission requested at the right moment (Android 13+)
- [ ] Token uploaded to backend on `onNewToken` and after sign-in
- [ ] Using data-only FCM messages for full control over display
- [ ] Deep-link URIs validated before navigation
- [ ] Notification tap uses `FLAG_IMMUTABLE` PendingIntent
- [ ] Grouped notifications for high-volume channels
- [ ] Token cleared from backend on sign-out
