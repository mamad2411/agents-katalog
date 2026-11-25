---
name: analytics-patterns
description: "Analytics patterns: a vendor-neutral analytics service, Firebase event constraints and DebugView, Crashlytics error reporting, funnel event schemas, and AppsFlyer attribution. Use when instrumenting events or crash reporting in a mobile app."
---

# Analytics Patterns

## Analytics Service Abstraction

```swift
// iOS — centralize all analytics calls
import FirebaseAnalytics

enum AnalyticsEvent {
    case productViewed(productId: String, category: String, source: String)
    case addedToCart(productId: String, price: Double, quantity: Int)
    case purchaseCompleted(orderId: String, revenue: Double, itemCount: Int)
    case screenViewed(screenName: String)

    var name: String {
        switch self {
        case .productViewed: return "product_viewed"
        case .addedToCart: return "add_to_cart"
        case .purchaseCompleted: return "purchase"
        case .screenViewed: return "screen_view"
        }
    }

    var parameters: [String: Any] {
        switch self {
        case .productViewed(let id, let category, let source):
            return ["product_id": id, "category": category, "source": source]
        case .addedToCart(let id, let price, let quantity):
            return ["product_id": id, "price": price, "quantity": quantity]
        case .purchaseCompleted(let orderId, let revenue, let count):
            return ["transaction_id": orderId, "value": revenue, "item_count": count]
        case .screenViewed(let name):
            return [AnalyticsParameterScreenName: name]
        }
    }
}

class AnalyticsService {
    static let shared = AnalyticsService()
    private var userId: String?

    func identify(userId: String) {
        self.userId = userId
        Analytics.setUserID(userId)
        // Never set PII directly — use your own user ID
    }

    func track(_ event: AnalyticsEvent) {
        Analytics.logEvent(event.name, parameters: event.parameters)
    }

    func setUserProperty(_ value: String, name: String) {
        Analytics.setUserProperty(value, forName: name)
    }
}

// Usage
AnalyticsService.shared.track(.productViewed(
    productId: "SKU-123",
    category: "Electronics",
    source: "home_featured"
))
```

```kotlin
// Android Kotlin
class AnalyticsService @Inject constructor(
    private val firebaseAnalytics: FirebaseAnalytics
) {
    fun identify(userId: String) {
        firebaseAnalytics.setUserId(userId)
    }

    fun trackProductViewed(productId: String, category: String, source: String) {
        val bundle = bundleOf(
            "product_id" to productId,
            "category" to category,
            "source" to source
        )
        firebaseAnalytics.logEvent("product_viewed", bundle)
    }

    fun trackPurchase(orderId: String, revenue: Double, itemCount: Int) {
        val bundle = bundleOf(
            FirebaseAnalytics.Param.TRANSACTION_ID to orderId,
            FirebaseAnalytics.Param.VALUE to revenue,
            FirebaseAnalytics.Param.CURRENCY to "USD",
            "item_count" to itemCount
        )
        firebaseAnalytics.logEvent(FirebaseAnalytics.Event.PURCHASE, bundle)
    }
}
```

---

## Firebase Analytics: Event Constraints

```
Event names:    max 40 chars, snake_case, no spaces, no leading underscore
Parameters:     max 25 per event, names max 40 chars, string values max 100 chars
User properties: max 25 custom, names max 24 chars, values max 36 chars
Custom events:  logged to BigQuery daily; real-time in DebugView
Reserved names: first_open, in_app_purchase, session_start, app_update, etc.
```

### Enable DebugView (iOS)
```bash
# Add launch argument in Xcode scheme: -FIRAnalyticsDebugEnabled
# Or via terminal:
xcrun simctl launch booted com.yourapp -FIRAnalyticsDebugEnabled
```

### Enable DebugView (Android)
```bash
adb shell setprop debug.firebase.analytics.app com.yourpackage
# Disable:
adb shell setprop debug.firebase.analytics.app .none.
```

---

## Crashlytics: Error Reporting

```swift
// iOS — non-fatal error with context
import FirebaseCrashlytics

func handleApiError(_ error: Error, endpoint: String) {
    let crashlytics = Crashlytics.crashlytics()
    crashlytics.setCustomValue(endpoint, forKey: "api_endpoint")
    crashlytics.setCustomValue(userId ?? "anonymous", forKey: "user_id")
    crashlytics.log("API error on \(endpoint): \(error.localizedDescription)")
    crashlytics.record(error: error)
}
```

```kotlin
// Android Kotlin
fun handleApiError(error: Exception, endpoint: String) {
    Firebase.crashlytics.apply {
        setCustomKey("api_endpoint", endpoint)
        setCustomKey("user_id", currentUserId ?: "anonymous")
        log("API error on $endpoint: ${error.message}")
        recordException(error)
    }
}
```

---

## Funnel Event Schema

```
Acquisition funnel:
  app_open                    { source: "notification" | "organic" | "paid_social" }
  screen_view                 { screen_name: "home" }
  product_viewed              { product_id, category, source, price }
  add_to_cart                 { product_id, category, price, quantity }
  begin_checkout              { cart_value, item_count }
  payment_info_entered        { payment_method: "card" | "apple_pay" | "paypal" }
  purchase                    { transaction_id, value, currency, item_count }

Retention events:
  session_start               (automatic Firebase)
  notification_received       { notification_type, campaign_id }
  notification_tapped         { notification_type, campaign_id }
  feature_used                { feature_name, context }
```

---

## AppsFlyer Attribution

```swift
// iOS — start SDK in AppDelegate.didFinishLaunching
AppsFlyerLib.shared().appsFlyerDevKey = "YOUR_DEV_KEY"
AppsFlyerLib.shared().appleAppID = "YOUR_APP_STORE_ID"
AppsFlyerLib.shared().delegate = self

// Log in-app event mapped to AppsFlyer schema
AppsFlyerLib.shared().logEvent(
    AFEventPurchase,
    withValues: [
        AFEventParamRevenue: 29.99,
        AFEventParamCurrency: "USD",
        AFEventParamContentId: "SKU-123"
    ]
)

// Handle deep link attribution
extension AppDelegate: AppsFlyerDeepLinkDelegate {
    func didResolveDeepLink(_ result: DeepLinkResult) {
        switch result.status {
        case .found:
            let deepLink = result.deepLink!
            let productId = deepLink.clickHTTPReferrer
            // Navigate to product
        default: break
        }
    }
}
```
