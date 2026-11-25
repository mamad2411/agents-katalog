---
name: push-notification-patterns
description: "Push setup code for iOS registration and a rich notification service extension, Android FCM with notification channels and terminated-state taps, FCM HTTP v1 server payloads, and a state handling summary. Use when implementing or debugging push notifications."
---

# Push Notification Patterns

## iOS: Full Push Setup

```swift
import UserNotifications
import FirebaseMessaging

class AppDelegate: UIResponder, UIApplicationDelegate,
                   UNUserNotificationCenterDelegate,
                   MessagingDelegate {

    func application(_ application: UIApplication,
                     didFinishLaunchingWithOptions launchOptions: [UIApplication.LaunchOptionsKey: Any]?) -> Bool {
        FirebaseApp.configure()

        // Request notification permission
        UNUserNotificationCenter.current().delegate = self
        Messaging.messaging().delegate = self

        UNUserNotificationCenter.current().requestAuthorization(
            options: [.alert, .badge, .sound]
        ) { granted, error in
            guard granted else { return }
            DispatchQueue.main.async {
                UIApplication.shared.registerForRemoteNotifications()
            }
        }

        return true
    }

    // APNs token — FCM swizzles this; still useful for direct APNs
    func application(_ application: UIApplication,
                     didRegisterForRemoteNotificationsWithDeviceToken deviceToken: Data) {
        Messaging.messaging().apnsToken = deviceToken
    }

    // FCM token — send to your server
    func messaging(_ messaging: Messaging, didReceiveRegistrationToken fcmToken: String?) {
        guard let token = fcmToken else { return }
        // Send to server only if different from stored token
        if UserDefaults.standard.string(forKey: "fcmToken") != token {
            UserDefaults.standard.set(token, forKey: "fcmToken")
            Task { await PushTokenService.register(token: token) }
        }
    }

    // Foreground: show notification as banner
    func userNotificationCenter(_ center: UNUserNotificationCenter,
                                 willPresent notification: UNNotification,
                                 withCompletionHandler completionHandler: @escaping (UNNotificationPresentationOptions) -> Void) {
        completionHandler([.banner, .badge, .sound])
    }

    // Handle tap — route to correct screen
    func userNotificationCenter(_ center: UNUserNotificationCenter,
                                 didReceive response: UNNotificationResponse,
                                 withCompletionHandler completionHandler: @escaping () -> Void) {
        let userInfo = response.notification.request.content.userInfo
        DeepLinkRouter.handle(userInfo: userInfo)
        completionHandler()
    }
}
```

### iOS: Rich Notification Service Extension

```swift
// NotificationService.swift (in separate target)
class NotificationService: UNNotificationServiceExtension {
    var contentHandler: ((UNNotificationContent) -> Void)?
    var bestAttemptContent: UNMutableNotificationContent?

    override func didReceive(_ request: UNNotificationRequest,
                              withContentHandler contentHandler: @escaping (UNNotificationContent) -> Void) {
        self.contentHandler = contentHandler
        bestAttemptContent = (request.content.mutableCopy() as? UNMutableNotificationContent)

        guard let content = bestAttemptContent,
              let imageURLString = content.userInfo["image_url"] as? String,
              let imageURL = URL(string: imageURLString) else {
            contentHandler(request.content)
            return
        }

        // Download image attachment
        let task = URLSession.shared.downloadTask(with: imageURL) { tempURL, _, error in
            defer { contentHandler(content) }
            guard let tempURL else { return }

            let filename = imageURL.lastPathComponent
            let destination = URL(fileURLWithPath: NSTemporaryDirectory()).appendingPathComponent(filename)
            try? FileManager.default.moveItem(at: tempURL, to: destination)

            if let attachment = try? UNNotificationAttachment(identifier: "image", url: destination) {
                content.attachments = [attachment]
            }
        }
        task.resume()
    }

    override func serviceExtensionTimeWillExpire() {
        // Called if download didn't complete in time — deliver best attempt
        if let contentHandler, let bestAttemptContent {
            contentHandler(bestAttemptContent)
        }
    }
}
```

---

## Android: FCM Setup with Notification Channels

```kotlin
class MyApplication : Application() {
    override fun onCreate() {
        super.onCreate()
        FirebaseApp.initializeApp(this)
        createNotificationChannels()
    }

    private fun createNotificationChannels() {
        val channels = listOf(
            NotificationChannel(
                "orders",
                "Order Updates",
                NotificationManager.IMPORTANCE_HIGH
            ).apply {
                description = "Your order status updates"
                enableVibration(true)
            },
            NotificationChannel(
                "promotions",
                "Promotions",
                NotificationManager.IMPORTANCE_LOW
            ).apply {
                description = "Deals and promotions"
            }
        )

        val manager = getSystemService(NotificationManager::class.java)
        channels.forEach { manager.createNotificationChannel(it) }
    }
}

class MyFirebaseMessagingService : FirebaseMessagingService() {

    // Token refresh — send new token to server
    override fun onNewToken(token: String) {
        lifecycleScope.launch {
            PushTokenRepository.register(token)
        }
    }

    // Foreground push AND data-only push (background goes to system tray)
    override fun onMessageReceived(remoteMessage: RemoteMessage) {
        val data = remoteMessage.data
        val channelId = data["channel_id"] ?: "orders"

        val notification = NotificationCompat.Builder(this, channelId)
            .setContentTitle(remoteMessage.notification?.title ?: data["title"])
            .setContentText(remoteMessage.notification?.body ?: data["body"])
            .setSmallIcon(R.drawable.ic_notification)
            .setAutoCancel(true)
            .setContentIntent(buildDeepLinkIntent(data))
            .build()

        NotificationManagerCompat.from(this)
            .notify(data["notification_id"]?.toInt() ?: 0, notification)
    }

    private fun buildDeepLinkIntent(data: Map<String, String>): PendingIntent {
        val intent = Intent(this, MainActivity::class.java).apply {
            flags = Intent.FLAG_ACTIVITY_SINGLE_TOP
            data["order_id"]?.let { putExtra("order_id", it) }
        }
        return PendingIntent.getActivity(this, 0, intent,
            PendingIntent.FLAG_UPDATE_CURRENT or PendingIntent.FLAG_IMMUTABLE)
    }
}
```

### Handle Tap from Terminated State (Android)

```kotlin
class MainActivity : AppCompatActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        handlePushIntent(intent)
    }

    override fun onNewIntent(intent: Intent) {
        super.onNewIntent(intent)
        handlePushIntent(intent)
    }

    private fun handlePushIntent(intent: Intent) {
        val orderId = intent.getStringExtra("order_id") ?: return
        navController.navigate(OrderDetailDestination(orderId))
    }
}
```

---

## FCM HTTP v1 Payload (Server Side)

```json
{
  "message": {
    "token": "device_registration_token",
    "notification": {
      "title": "Your order shipped",
      "body": "Order #1234 is on its way"
    },
    "data": {
      "order_id": "1234",
      "channel_id": "orders",
      "deep_link": "myapp://orders/1234"
    },
    "android": {
      "priority": "high",
      "notification": {
        "channel_id": "orders",
        "notification_priority": "PRIORITY_HIGH"
      }
    },
    "apns": {
      "payload": {
        "aps": {
          "alert": {
            "title": "Your order shipped",
            "body": "Order #1234 is on its way"
          },
          "badge": 1,
          "sound": "default",
          "mutable-content": 1
        },
        "order_id": "1234"
      }
    }
  }
}
```

---

## Notification State Handling Summary

```
Foreground:
  iOS → UNUserNotificationCenterDelegate.willPresent → return [.banner, .sound]
  Android → FirebaseMessagingService.onMessageReceived → build + show NotificationCompat

Background / Tray tap:
  iOS → UNUserNotificationCenterDelegate.didReceive → route via DeepLinkRouter
  Android → MainActivity.onNewIntent or onCreate → read intent extras

Silent push (content-available: 1):
  iOS → AppDelegate.application(_:didReceiveRemoteNotification:fetchCompletionHandler:)
  Android → onMessageReceived (data-only message, no notification key)
```
