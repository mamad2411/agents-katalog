---
name: mobile-push-notifications
description: >
  Implement push notifications in mobile apps — FCM, APNs, local notifications,
  rich media, notification channels, deep linking from notifications, silent push,
  token management, and notification strategies across Flutter, Android (Kotlin/Java),
  and iOS (Swift/ObjC).
  TRIGGER when: user says /mobile-push-notifications, asks about push notifications,
  needs to implement FCM/APNs, or wants to design a notification strategy.
argument-hint: "[notification feature or integration need]"
user-invocable: true
---

# Mobile Push Notifications

You are a senior mobile engineer. Help the user design, implement, or review push notification systems with platform-specific best practices.

## Process

### Step 1: Understand Requirements

| Question | Why It Matters |
|----------|---------------|
| What types of notifications? (transactional, marketing, real-time alerts) | Determines priority and channel strategy |
| Does the app need to deep link from notifications? | Payload design and navigation handling |
| Are there rich media needs? (images, action buttons, custom UI) | Notification extension / custom layout |
| Is the app cross-platform? | FCM covers both, but APNs-specific features may be needed |
| Are there notification preferences? (per-topic opt-in/out) | Topic subscription or server-side filtering |
| What is the expected volume? | Batching, throttling, server architecture |

### Step 2: Architecture Overview

```
Backend Server
  → Push Provider (FCM / APNs / both)
    → Device
      → OS Notification System
        → App (foreground: in-app handling / background: system tray)
          → User taps → Deep link → Specific screen
```

**Key components:**
| Component | Responsibility |
|-----------|---------------|
| **Backend** | Decides when/what to send, calls FCM/APNs API, manages device tokens |
| **FCM (Firebase Cloud Messaging)** | Cross-platform delivery (Android + iOS), topic subscriptions, analytics |
| **APNs (Apple Push Notification service)** | iOS delivery, required even when using FCM on iOS (FCM wraps APNs) |
| **Device token** | Unique identifier per device per app — must be refreshed and synced to backend |
| **Notification payload** | Title, body, data, image, actions, deep link |

### Step 3: Request Permission

#### Flutter
```dart
// Using firebase_messaging
final messaging = FirebaseMessaging.instance;

// Request permission (required on iOS, Android 13+)
final settings = await messaging.requestPermission(
  alert: true,
  badge: true,
  sound: true,
  provisional: false, // set true for quiet delivery on iOS
  announcement: false,
  carPlay: false,
  criticalAlert: false, // requires Apple entitlement
);

if (settings.authorizationStatus == AuthorizationStatus.authorized) {
  print('User granted permission');
} else if (settings.authorizationStatus == AuthorizationStatus.provisional) {
  print('User granted provisional permission');
} else {
  print('User declined permission');
}

// Get device token
final token = await messaging.getToken();
await sendTokenToServer(token);

// Listen for token refresh
messaging.onTokenRefresh.listen((newToken) {
  sendTokenToServer(newToken);
});
```

#### Android (Kotlin)
```kotlin
// Android 13+ (API 33) requires runtime permission
if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.TIRAMISU) {
    val permissionLauncher = registerForActivityResult(
        ActivityResultContracts.RequestPermission()
    ) { granted ->
        if (granted) {
            getAndSendToken()
        } else {
            // Explain why notifications are useful, offer settings link
        }
    }
    permissionLauncher.launch(Manifest.permission.POST_NOTIFICATIONS)
}

// Get FCM token
FirebaseMessaging.getInstance().token.addOnSuccessListener { token ->
    sendTokenToServer(token)
}

// AndroidManifest.xml
// <uses-permission android:name="android.permission.POST_NOTIFICATIONS" />
```

#### Android (Java)
```java
// Request permission (Android 13+)
if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.TIRAMISU) {
    ActivityCompat.requestPermissions(this,
        new String[]{Manifest.permission.POST_NOTIFICATIONS}, REQUEST_CODE);
}

// Get FCM token
FirebaseMessaging.getInstance().getToken().addOnSuccessListener(token -> {
    sendTokenToServer(token);
});
```

#### iOS (Swift)
```swift
import UserNotifications

// Request permission
UNUserNotificationCenter.current().requestAuthorization(
    options: [.alert, .badge, .sound]
) { granted, error in
    if granted {
        DispatchQueue.main.async {
            UIApplication.shared.registerForRemoteNotifications()
        }
    }
}

// AppDelegate — receive device token
func application(_ application: UIApplication,
                 didRegisterForRemoteNotificationsWithDeviceToken deviceToken: Data) {
    let token = deviceToken.map { String(format: "%02.2hhx", $0) }.joined()
    sendTokenToServer(token)
    // Also set FCM token if using Firebase
    Messaging.messaging().apnsToken = deviceToken
}

func application(_ application: UIApplication,
                 didFailToRegisterForRemoteNotificationsWithError error: Error) {
    print("Failed to register: \(error)")
}
```

#### iOS (Objective-C)
```objc
// Request permission
UNUserNotificationCenter *center = [UNUserNotificationCenter currentNotificationCenter];
[center requestAuthorizationWithOptions:(UNAuthorizationOptionAlert | UNAuthorizationOptionBadge | UNAuthorizationOptionSound)
    completionHandler:^(BOOL granted, NSError *error) {
        if (granted) {
            dispatch_async(dispatch_get_main_queue(), ^{
                [[UIApplication sharedApplication] registerForRemoteNotifications];
            });
        }
    }];

// Receive token
- (void)application:(UIApplication *)application didRegisterForRemoteNotificationsWithDeviceToken:(NSData *)deviceToken {
    // Convert to string and send to server
}
```

### Step 4: Handle Incoming Notifications

#### Flutter
```dart
// Foreground — app is open
FirebaseMessaging.onMessage.listen((RemoteMessage message) {
  // Show in-app notification (snackbar, overlay, local notification)
  if (message.notification != null) {
    showInAppNotification(message.notification!);
  }
  // Handle data payload
  handleDataPayload(message.data);
});

// Background — app is in background (but not terminated)
FirebaseMessaging.onBackgroundMessage(_backgroundHandler);

@pragma('vm:entry-point')
Future<void> _backgroundHandler(RemoteMessage message) async {
  await Firebase.initializeApp();
  // Process data silently (NO UI updates — different isolate)
  await processBackgroundData(message.data);
}

// Notification tap — app opened from notification
FirebaseMessaging.onMessageOpenedApp.listen((RemoteMessage message) {
  navigateToScreen(message.data['deepLink']);
});

// App launched from terminated state via notification
final initialMessage = await FirebaseMessaging.instance.getInitialMessage();
if (initialMessage != null) {
  navigateToScreen(initialMessage.data['deepLink']);
}
```

#### Android (Kotlin)
```kotlin
// FirebaseMessagingService — handles all incoming messages
class MyFirebaseMessagingService : FirebaseMessagingService() {

    override fun onNewToken(token: String) {
        // Token refreshed — send to server
        sendTokenToServer(token)
    }

    override fun onMessageReceived(message: RemoteMessage) {
        // Data message — always delivered here (foreground + background)
        message.data.let { data ->
            if (data.isNotEmpty()) {
                processData(data)
            }
        }

        // Notification message — only delivered here if app is in FOREGROUND
        // In background, system shows it automatically
        message.notification?.let { notification ->
            showNotification(notification.title, notification.body, message.data)
        }
    }

    private fun showNotification(title: String?, body: String?, data: Map<String, String>) {
        val intent = Intent(this, MainActivity::class.java).apply {
            flags = Intent.FLAG_ACTIVITY_NEW_TASK or Intent.FLAG_ACTIVITY_CLEAR_TOP
            putExtra("deepLink", data["deepLink"])
        }
        val pendingIntent = PendingIntent.getActivity(
            this, 0, intent, PendingIntent.FLAG_IMMUTABLE or PendingIntent.FLAG_UPDATE_CURRENT
        )

        val notification = NotificationCompat.Builder(this, CHANNEL_ID)
            .setSmallIcon(R.drawable.ic_notification)
            .setContentTitle(title)
            .setContentText(body)
            .setAutoCancel(true)
            .setContentIntent(pendingIntent)
            .build()

        NotificationManagerCompat.from(this).notify(notificationId, notification)
    }
}
```

#### iOS (Swift)
```swift
// UNUserNotificationCenterDelegate
class AppDelegate: UIResponder, UIApplicationDelegate, UNUserNotificationCenterDelegate {

    func application(_ application: UIApplication, didFinishLaunchingWithOptions ...) -> Bool {
        UNUserNotificationCenter.current().delegate = self
        return true
    }

    // Foreground — app is open
    func userNotificationCenter(_ center: UNUserNotificationCenter,
                                willPresent notification: UNNotification,
                                withCompletionHandler completionHandler: @escaping (UNNotificationPresentationOptions) -> Void) {
        let data = notification.request.content.userInfo
        // Show banner even in foreground
        completionHandler([.banner, .sound, .badge])
    }

    // User tapped notification
    func userNotificationCenter(_ center: UNUserNotificationCenter,
                                didReceive response: UNNotificationResponse,
                                withCompletionHandler completionHandler: @escaping () -> Void) {
        let data = response.notification.request.content.userInfo
        if let deepLink = data["deepLink"] as? String {
            navigateToScreen(deepLink)
        }
        completionHandler()
    }
}
```

### Step 5: Notification Channels (Android)

Android 8+ (API 26) requires notification channels. Users can control each channel independently.

```kotlin
// Create channels at app startup (idempotent — safe to call repeatedly)
fun createNotificationChannels(context: Context) {
    val manager = context.getSystemService(NotificationManager::class.java)

    val channels = listOf(
        NotificationChannel("orders", "Order Updates", NotificationManager.IMPORTANCE_HIGH).apply {
            description = "Updates about your orders"
            enableVibration(true)
        },
        NotificationChannel("promotions", "Promotions", NotificationManager.IMPORTANCE_LOW).apply {
            description = "Deals and special offers"
            enableVibration(false)
        },
        NotificationChannel("chat", "Messages", NotificationManager.IMPORTANCE_HIGH).apply {
            description = "Chat messages"
            enableVibration(true)
            setShowBadge(true)
        },
    )

    manager.createNotificationChannels(channels)
}

// Use channel when building notification
NotificationCompat.Builder(context, "orders") // channel ID
    .setSmallIcon(R.drawable.ic_notification)
    .setContentTitle("Order Shipped")
    .setContentText("Your order #1234 has been shipped")
    .build()
```

**Channel strategy:**
| Channel | Importance | Use Case |
|---------|-----------|----------|
| `orders` | HIGH | Transactional — order status, delivery |
| `chat` | HIGH | Real-time messages |
| `reminders` | DEFAULT | Scheduled reminders |
| `promotions` | LOW | Marketing, deals (easy for user to mute) |
| `system` | MIN | Background sync status, non-urgent updates |

### Step 6: Rich Notifications

#### Images & Media

**Flutter:**
```dart
// FCM payload with image
// Server sends: { "notification": { "title": "...", "body": "...", "image": "https://..." } }
// flutter_local_notifications for custom display
await flutterLocalNotificationsPlugin.show(
  id,
  title,
  body,
  NotificationDetails(
    android: AndroidNotificationDetails(
      'channel_id', 'Channel Name',
      styleInformation: BigPictureStyleInformation(
        DrawableResourceAndroidBitmap('large_image'),
      ),
    ),
    iOS: DarwinNotificationDetails(
      attachments: [DarwinNotificationAttachment(imagePath)],
    ),
  ),
);
```

**Android — Big Picture / Big Text:**
```kotlin
val style = NotificationCompat.BigPictureStyle()
    .bigPicture(downloadedBitmap)
    .bigLargeIcon(null as Bitmap?) // hide large icon when expanded

val notification = NotificationCompat.Builder(context, channelId)
    .setSmallIcon(R.drawable.ic_notification)
    .setContentTitle("New Product")
    .setContentText("Check out our latest arrival")
    .setStyle(style)
    .build()
```

**iOS — Notification Service Extension (for images):**
```swift
// NotificationService.swift (Notification Service Extension target)
class NotificationService: UNNotificationServiceExtension {
    override func didReceive(_ request: UNNotificationRequest,
                             withContentHandler contentHandler: @escaping (UNNotificationContent) -> Void) {
        guard let content = request.content.mutableCopy() as? UNMutableNotificationContent,
              let imageURLString = content.userInfo["image_url"] as? String,
              let imageURL = URL(string: imageURLString) else {
            contentHandler(request.content)
            return
        }

        // Download and attach image
        downloadImage(from: imageURL) { localURL in
            if let localURL = localURL,
               let attachment = try? UNNotificationAttachment(identifier: "image", url: localURL) {
                content.attachments = [attachment]
            }
            contentHandler(content)
        }
    }
}
```

#### Action Buttons

**Android:**
```kotlin
val approveIntent = PendingIntent.getBroadcast(context, 0,
    Intent(context, NotificationActionReceiver::class.java).putExtra("action", "approve"),
    PendingIntent.FLAG_IMMUTABLE)

val rejectIntent = PendingIntent.getBroadcast(context, 0,
    Intent(context, NotificationActionReceiver::class.java).putExtra("action", "reject"),
    PendingIntent.FLAG_IMMUTABLE)

NotificationCompat.Builder(context, channelId)
    .setContentTitle("Approval Request")
    .setContentText("John wants to join your team")
    .addAction(R.drawable.ic_check, "Approve", approveIntent)
    .addAction(R.drawable.ic_close, "Reject", rejectIntent)
    .build()
```

**iOS:**
```swift
// Register action category
let approveAction = UNNotificationAction(identifier: "APPROVE", title: "Approve",
                                         options: [.authenticationRequired])
let rejectAction = UNNotificationAction(identifier: "REJECT", title: "Reject",
                                        options: [.destructive])
let category = UNNotificationCategory(identifier: "APPROVAL",
                                      actions: [approveAction, rejectAction],
                                      intentIdentifiers: [])
UNUserNotificationCenter.current().setNotificationCategories([category])

// Handle action in delegate
func userNotificationCenter(_ center: UNUserNotificationCenter,
                            didReceive response: UNNotificationResponse, ...) {
    switch response.actionIdentifier {
    case "APPROVE": handleApprove(response.notification.request.content.userInfo)
    case "REJECT": handleReject(response.notification.request.content.userInfo)
    default: break
    }
}
```

### Step 7: Local Notifications

For scheduled reminders, timers, and offline triggers.

**Flutter — flutter_local_notifications:**
```dart
// Schedule a notification
await flutterLocalNotificationsPlugin.zonedSchedule(
  id,
  'Reminder',
  'Don\'t forget to check your order',
  tz.TZDateTime.now(tz.local).add(const Duration(hours: 1)),
  const NotificationDetails(
    android: AndroidNotificationDetails('reminders', 'Reminders'),
    iOS: DarwinNotificationDetails(),
  ),
  androidScheduleMode: AndroidScheduleMode.exactAllowWhileIdle,
  uiLocalNotificationDateInterpretation:
      UILocalNotificationDateInterpretation.absoluteTime,
);
```

**Android:**
```kotlin
// Using WorkManager for reliable scheduled notifications
val notificationWork = OneTimeWorkRequestBuilder<NotificationWorker>()
    .setInitialDelay(1, TimeUnit.HOURS)
    .setInputData(workDataOf("title" to "Reminder", "body" to "Check your order"))
    .build()
WorkManager.getInstance(context).enqueue(notificationWork)
```

**iOS:**
```swift
let content = UNMutableNotificationContent()
content.title = "Reminder"
content.body = "Don't forget to check your order"
content.sound = .default

let trigger = UNTimeIntervalNotificationTrigger(timeInterval: 3600, repeats: false)
let request = UNNotificationRequest(identifier: UUID().uuidString,
                                    content: content, trigger: trigger)
UNUserNotificationCenter.current().add(request)
```

### Step 8: Silent Push / Data-Only Messages

For background data sync without user-visible notification.

**FCM payload (data-only — no `notification` key):**
```json
{
  "to": "device_token",
  "data": {
    "type": "sync",
    "resource": "orders",
    "timestamp": "2024-01-15T10:00:00Z"
  }
}
```

**iOS — enable background modes:**
- Xcode > Capabilities > Background Modes > Remote notifications
- Set `content-available: 1` in APNs payload
- App gets ~30 seconds of background execution time

### Step 9: Topic Subscriptions

```dart
// Flutter — subscribe to topic
await FirebaseMessaging.instance.subscribeToTopic('order_updates');
await FirebaseMessaging.instance.unsubscribeFromTopic('promotions');
```

```kotlin
// Android
FirebaseMessaging.getInstance().subscribeToTopic("order_updates")
FirebaseMessaging.getInstance().unsubscribeFromTopic("promotions")
```

```swift
// iOS
Messaging.messaging().subscribe(toTopic: "order_updates")
Messaging.messaging().unsubscribe(fromTopic: "promotions")
```

**Topic vs. token targeting:**
| Approach | Use Case | Server Complexity |
|----------|----------|------------------|
| **Token-based** | Personalized notifications (user-specific) | Server stores tokens, targets individually |
| **Topic-based** | Broadcast to groups (all iOS users, all premium users) | Simple, FCM handles distribution |
| **Condition-based** | Combine topics (`'orders' in topics && 'premium' in topics`) | Medium |

## Notification Strategy Checklist

- [ ] Permission requested at the right time (not on first launch — explain value first)
- [ ] Device token is sent to server and refreshed on change
- [ ] Foreground, background, and terminated states all handled
- [ ] Notification tap navigates to the correct screen (deep link)
- [ ] Notification channels configured (Android 8+)
- [ ] Rich media (images, action buttons) implemented where needed
- [ ] Silent push used for background sync (not user-facing)
- [ ] Topic subscriptions match user preferences
- [ ] Badge count is managed (increment on receive, clear on read)
- [ ] Notification analytics tracked (delivered, opened, dismissed)
- [ ] Rate limiting — don't spam users (leads to permission revocation)
- [ ] Opt-out preferences respected (server-side filtering, not just client-side)

## Output Format

```markdown
## Notification Architecture
- **Platform:** [Flutter / Android / iOS]
- **Push Provider:** [FCM / APNs / both]
- **Types:** [Transactional / Marketing / Real-time / Local]

## Implementation Plan
[Which notification types, channels, and features to implement]

## Payload Design
[Sample payloads for each notification type]

## Deep Link Mapping
[Notification type → target screen]

## User Preferences
[How users control notification settings]
```

## Edge Cases

- FCM delivery on iOS requires APNs configuration — FCM wraps APNs, it doesn't bypass it
- On Android, data-only messages are delivered to `onMessageReceived` even in background; notification messages are NOT (system handles display)
- On iOS, background delivery is "best effort" — the system may throttle or delay silent push
- Device tokens change on app reinstall, OS update, or restoring from backup — always sync on app start
- Huawei devices without Google Play Services cannot use FCM — use Huawei Push Kit as fallback
- Android doze mode and app standby can delay notification delivery — use HIGH priority for time-sensitive messages
- iOS provisional authorization (quiet delivery) shows notifications in Notification Center but not on lock screen — good for low-priority first engagement
- Don't request notification permission on first app launch — explain the value first, then ask
