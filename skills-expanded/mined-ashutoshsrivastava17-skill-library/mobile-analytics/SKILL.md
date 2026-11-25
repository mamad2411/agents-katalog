---
name: mobile-analytics
description: >
  Implement mobile analytics and crash reporting — event tracking strategy,
  Firebase Analytics, Mixpanel, Amplitude, Crashlytics, Sentry, user properties,
  funnel tracking, privacy-compliant tracking (ATT, consent), and A/B testing
  across Flutter, Android (Kotlin/Java), and iOS (Swift/ObjC).
  TRIGGER when: user says /mobile-analytics, asks about tracking events in a mobile app,
  needs to set up crash reporting, or wants to design an analytics strategy.
argument-hint: "[analytics need or tracking strategy]"
user-invocable: true
---

# Mobile Analytics & Crash Reporting

You are a senior mobile engineer. Help the user design, implement, or review analytics and crash reporting with platform-specific guidance and privacy best practices.

## Process

### Step 1: Define Analytics Goals

| Question | Why It Matters |
|----------|---------------|
| What decisions will analytics inform? (product, growth, engineering) | Determines what to track |
| What are the key user journeys? | Funnel definition |
| What KPIs matter? (DAU, retention, conversion, revenue) | Metric selection |
| What is the privacy posture? (GDPR, CCPA, COPPA) | Consent and data minimization |
| What platforms? (Flutter, Android, iOS) | SDK selection |
| What is the budget? | Free tier vs. paid tools |

### Step 2: Choose Analytics Stack

| Tool | Best For | Free Tier | Platforms |
|------|----------|-----------|-----------|
| **Firebase Analytics** | General event tracking, integrates with FCM/Crashlytics | Unlimited events | All |
| **Mixpanel** | User behavior, funnels, retention, A/B testing | 20M events/month | All |
| **Amplitude** | Product analytics, behavioral cohorts | 10M events/month | All |
| **PostHog** | Open source, self-hostable, feature flags + analytics | 1M events/month | All |
| **Segment** | Analytics router (sends to multiple destinations) | 1K users/month | All |

| Crash Reporting | Best For | Free Tier |
|----------------|----------|-----------|
| **Firebase Crashlytics** | Crash reports, ANRs, integrated with Firebase | Free |
| **Sentry** | Crashes + performance + breadcrumbs, multi-platform | 5K errors/month |
| **Bugsnag** | Crash stability scoring, release tracking | 7.5K events/month |
| **Datadog RUM** | Real user monitoring + crashes + APM | Trial |

**Recommended default:** Firebase Analytics + Crashlytics (free, well-integrated, good for most apps). Add Mixpanel or Amplitude if product analytics depth is needed.

### Step 3: Design Event Taxonomy

**Naming convention:** `object_action` (noun_verb, snake_case)

| Category | Examples | Purpose |
|----------|---------|---------|
| **Screen views** | `screen_viewed` | Funnel, navigation patterns |
| **User actions** | `button_tapped`, `item_added_to_cart`, `search_performed` | Feature usage, conversion |
| **Lifecycle** | `app_opened`, `session_started`, `app_backgrounded` | Engagement, retention |
| **Commerce** | `product_viewed`, `purchase_completed`, `subscription_started` | Revenue, conversion |
| **Errors** | `api_error_occurred`, `form_validation_failed` | Reliability, UX issues |
| **Performance** | `screen_load_time`, `api_response_time` | Performance monitoring |

**Event schema template:**
```json
{
  "event": "product_added_to_cart",
  "properties": {
    "product_id": "abc123",
    "product_name": "Running Shoes",
    "product_category": "footwear",
    "price": 99.99,
    "currency": "USD",
    "source_screen": "product_detail",
    "quantity": 1
  }
}
```

**Rules:**
- Use consistent naming across platforms (same event name on Flutter, Android, iOS)
- Track properties, not separate events (`button_tapped` with `button_name` property, not `login_button_tapped`, `signup_button_tapped`)
- Keep event count manageable (50-100 events is typical, not 1000+)
- Document every event in a tracking plan spreadsheet

### Step 4: Implement Analytics

#### Flutter

```dart
// Firebase Analytics
final analytics = FirebaseAnalytics.instance;

// Screen view
await analytics.logScreenView(screenName: 'product_detail', screenClass: 'ProductDetailScreen');

// Custom event
await analytics.logEvent(
  name: 'product_added_to_cart',
  parameters: {
    'product_id': product.id,
    'product_name': product.name,
    'price': product.price,
    'currency': 'USD',
    'source_screen': 'product_detail',
  },
);

// User properties
await analytics.setUserProperty(name: 'subscription_tier', value: 'premium');
await analytics.setUserId(id: user.id);

// E-commerce events (built-in)
await analytics.logPurchase(
  currency: 'USD',
  value: 99.99,
  transactionId: 'txn_123',
  items: [AnalyticsEventItem(itemId: 'abc123', itemName: 'Running Shoes', price: 99.99)],
);

// Analytics wrapper for clean architecture
abstract class AnalyticsTracker {
  void trackEvent(String name, Map<String, dynamic> properties);
  void trackScreenView(String screenName);
  void setUserProperty(String key, String value);
  void setUserId(String id);
}

class FirebaseAnalyticsTracker implements AnalyticsTracker {
  final FirebaseAnalytics _analytics;
  @override
  void trackEvent(String name, Map<String, dynamic> properties) {
    _analytics.logEvent(name: name, parameters: properties);
  }
  // ... other methods
}

// Use via DI — easy to swap implementations or add multiple destinations
```

#### Android (Kotlin)

```kotlin
// Firebase Analytics
val analytics = Firebase.analytics

// Screen view
analytics.logEvent(FirebaseAnalytics.Event.SCREEN_VIEW) {
    param(FirebaseAnalytics.Param.SCREEN_NAME, "product_detail")
    param(FirebaseAnalytics.Param.SCREEN_CLASS, "ProductDetailFragment")
}

// Custom event
analytics.logEvent("product_added_to_cart") {
    param("product_id", product.id)
    param("product_name", product.name)
    param("price", product.price)
    param("currency", "USD")
    param("source_screen", "product_detail")
}

// User properties
analytics.setUserProperty("subscription_tier", "premium")
analytics.setUserId(user.id)

// Analytics interface for clean architecture
interface AnalyticsTracker {
    fun trackEvent(name: String, properties: Map<String, Any> = emptyMap())
    fun trackScreenView(screenName: String)
    fun setUserProperty(key: String, value: String)
    fun setUserId(id: String)
}

@Singleton
class FirebaseAnalyticsTracker @Inject constructor(
    private val analytics: FirebaseAnalytics
) : AnalyticsTracker {
    override fun trackEvent(name: String, properties: Map<String, Any>) {
        analytics.logEvent(name, Bundle().apply {
            properties.forEach { (key, value) ->
                when (value) {
                    is String -> putString(key, value)
                    is Long -> putLong(key, value)
                    is Double -> putDouble(key, value)
                    else -> putString(key, value.toString())
                }
            }
        })
    }
}
```

#### Android (Java)

```java
// Firebase Analytics
FirebaseAnalytics analytics = FirebaseAnalytics.getInstance(context);

Bundle params = new Bundle();
params.putString("product_id", product.getId());
params.putString("product_name", product.getName());
params.putDouble("price", product.getPrice());
analytics.logEvent("product_added_to_cart", params);

// User properties
analytics.setUserProperty("subscription_tier", "premium");
```

#### iOS (Swift)

```swift
import FirebaseAnalytics

// Screen view
Analytics.logEvent(AnalyticsEventScreenView, parameters: [
    AnalyticsParameterScreenName: "product_detail",
    AnalyticsParameterScreenClass: "ProductDetailViewController"
])

// Custom event
Analytics.logEvent("product_added_to_cart", parameters: [
    "product_id": product.id,
    "product_name": product.name,
    "price": product.price,
    "currency": "USD",
    "source_screen": "product_detail"
])

// User properties
Analytics.setUserProperty("premium", forName: "subscription_tier")
Analytics.setUserID(user.id)

// Analytics protocol for clean architecture
protocol AnalyticsTracker {
    func trackEvent(_ name: String, properties: [String: Any])
    func trackScreenView(_ screenName: String)
    func setUserProperty(_ value: String, forName name: String)
    func setUserId(_ id: String)
}

struct FirebaseAnalyticsTracker: AnalyticsTracker {
    func trackEvent(_ name: String, properties: [String: Any]) {
        Analytics.logEvent(name, parameters: properties)
    }
    // ... other methods
}
```

#### iOS (Objective-C)

```objc
@import FirebaseAnalytics;

[FIRAnalytics logEventWithName:@"product_added_to_cart" parameters:@{
    @"product_id": product.productId,
    @"product_name": product.name,
    @"price": @(product.price),
    @"currency": @"USD"
}];

[FIRAnalytics setUserPropertyString:@"premium" forName:@"subscription_tier"];
```

### Step 5: Implement Crash Reporting

#### Flutter — Crashlytics
```dart
// Initialize in main
void main() async {
  WidgetsFlutterBinding.ensureInitialized();
  await Firebase.initializeApp();

  // Catch Flutter framework errors
  FlutterError.onError = FirebaseCrashlytics.instance.recordFlutterFatalError;

  // Catch async errors
  PlatformDispatcher.instance.onError = (error, stack) {
    FirebaseCrashlytics.instance.recordError(error, stack, fatal: true);
    return true;
  };

  runApp(const MyApp());
}

// Add breadcrumbs for context
FirebaseCrashlytics.instance.log('User tapped checkout button');

// Set user ID for crash correlation
FirebaseCrashlytics.instance.setUserIdentifier(user.id);

// Custom keys for debugging
FirebaseCrashlytics.instance.setCustomKey('screen', 'checkout');
FirebaseCrashlytics.instance.setCustomKey('cart_items', cartCount);

// Non-fatal error reporting
try {
  await processPayment();
} catch (e, stackTrace) {
  FirebaseCrashlytics.instance.recordError(e, stackTrace, reason: 'Payment processing failed');
}
```

#### Android (Kotlin) — Crashlytics
```kotlin
// Set user for crash correlation
Firebase.crashlytics.setUserId(user.id)
Firebase.crashlytics.setCustomKey("screen", "checkout")

// Breadcrumbs
Firebase.crashlytics.log("User tapped checkout button")

// Non-fatal error
try {
    processPayment()
} catch (e: Exception) {
    Firebase.crashlytics.recordException(e)
}
```

#### iOS (Swift) — Crashlytics
```swift
// Set user
Crashlytics.crashlytics().setUserID(user.id)
Crashlytics.crashlytics().setCustomValue("checkout", forKey: "screen")

// Breadcrumbs
Crashlytics.crashlytics().log("User tapped checkout button")

// Non-fatal error
do {
    try processPayment()
} catch {
    Crashlytics.crashlytics().record(error: error)
}
```

#### Sentry (Cross-platform alternative)
```dart
// Flutter — Sentry
await SentryFlutter.init((options) {
  options.dsn = 'https://...@sentry.io/...';
  options.tracesSampleRate = 0.2; // 20% of transactions for performance
  options.profilesSampleRate = 0.1;
  options.environment = kReleaseMode ? 'production' : 'development';
});

// Breadcrumb
Sentry.addBreadcrumb(Breadcrumb(message: 'User tapped checkout', category: 'ui'));

// Capture exception with context
Sentry.captureException(error, stackTrace: stackTrace, withScope: (scope) {
  scope.setTag('screen', 'checkout');
  scope.setExtra('cart_items', cartCount);
});
```

### Step 6: Privacy-Compliant Tracking

#### App Tracking Transparency (iOS 14.5+)

Required before using IDFA or cross-app tracking.

```swift
import AppTrackingTransparency

func requestTrackingPermission() {
    ATTrackingManager.requestTrackingAuthorization { status in
        switch status {
        case .authorized:
            // Enable personalized ads, attribution SDKs
            Analytics.setAnalyticsCollectionEnabled(true)
        case .denied, .restricted:
            // Use privacy-safe analytics only
            Analytics.setAnalyticsCollectionEnabled(true) // Firebase doesn't use IDFA
        case .notDetermined:
            break
        @unknown default:
            break
        }
    }
}
```

```dart
// Flutter — app_tracking_transparency package
final status = await AppTrackingTransparency.requestTrackingAuthorization();
if (status == TrackingStatus.authorized) {
  // Enable full tracking
}
```

#### Consent Management

```dart
// Analytics wrapper with consent
class ConsentAwareAnalytics implements AnalyticsTracker {
  final AnalyticsTracker _tracker;
  bool _hasConsent = false;
  final List<_PendingEvent> _queue = [];

  void setConsent(bool granted) {
    _hasConsent = granted;
    if (granted) {
      for (final event in _queue) {
        _tracker.trackEvent(event.name, event.properties);
      }
      _queue.clear();
    } else {
      _queue.clear(); // discard queued events
    }
  }

  @override
  void trackEvent(String name, Map<String, dynamic> properties) {
    if (_hasConsent) {
      _tracker.trackEvent(name, properties);
    }
    // Don't queue if no consent — data minimization
  }
}
```

**Privacy rules:**
- Never track PII (email, phone, name) in event properties
- Use anonymized user IDs, not real identifiers
- Respect ATT on iOS — don't use IDFA without authorization
- Provide opt-out mechanism in app settings
- Document what you track in privacy policy and store declarations
- GDPR: get consent before tracking in EU
- COPPA: no analytics tracking for users under 13

### Step 7: Performance Monitoring

| Tool | Tracks | Platform |
|------|--------|----------|
| **Firebase Performance** | Screen rendering, network latency, custom traces | All |
| **Sentry Performance** | Transactions, slow/frozen frames, app start | All |

```dart
// Flutter — Firebase Performance custom trace
final trace = FirebasePerformance.instance.newTrace('checkout_flow');
await trace.start();
trace.putAttribute('payment_method', 'credit_card');
// ... do checkout work ...
trace.incrementMetric('items_purchased', cartCount);
await trace.stop();

// HTTP monitoring (automatic with firebase_performance)
// Or manual:
final metric = FirebasePerformance.instance.newHttpMetric(
  'https://api.example.com/orders',
  HttpMethod.Post,
);
await metric.start();
final response = await dio.post('/orders', data: orderData);
metric.httpResponseCode = response.statusCode;
metric.responsePayloadSize = response.data.toString().length;
await metric.stop();
```

## Output Format

```markdown
## Analytics Strategy
- **Platform:** [Flutter / Android / iOS]
- **Tools:** [Firebase + Crashlytics / Mixpanel + Sentry / etc.]
- **Privacy:** [ATT / GDPR consent / COPPA]

## Event Taxonomy
| Event | Properties | Funnel Stage |
|-------|-----------|-------------|
| ... | ... | ... |

## User Properties
| Property | Values | Purpose |
|----------|--------|---------|
| ... | ... | ... |

## Crash Reporting Setup
[SDK configuration, breadcrumbs, user identification]

## Privacy Implementation
[Consent flow, data minimization, ATT]
```

## Quality Checklist

- [ ] Event naming is consistent across platforms (same names on Flutter, Android, iOS)
- [ ] Events are documented in a tracking plan
- [ ] Crash reporting captures uncaught exceptions on all platforms
- [ ] Breadcrumbs provide context before crashes
- [ ] User ID is set for crash/analytics correlation
- [ ] No PII in event properties or crash logs
- [ ] ATT permission requested before IDFA usage (iOS)
- [ ] Consent mechanism implemented for GDPR regions
- [ ] Analytics collection can be disabled from app settings
- [ ] Debug/development events are filtered from production data
- [ ] Symbol files / dSYMs / ProGuard mappings uploaded for readable crash reports
- [ ] Performance monitoring covers key user journeys

## Edge Cases

- Firebase Analytics batches events and sends them approximately every hour (or on app background) — events are not real-time
- Crashlytics reports are processed async — crashes may take minutes to appear in dashboard
- On iOS, if the user declines ATT, Firebase Analytics still works (it doesn't use IDFA) but attribution SDKs won't have IDFA
- ProGuard/R8 obfuscation makes crash reports unreadable — always upload mapping files to Crashlytics/Sentry
- Flutter crashes in release mode need `--split-debug-info` symbols uploaded for readable stack traces
- Mixpanel/Amplitude have server-side event limits — monitor usage to avoid overages
- Don't log events in hot loops (scroll listeners, animation frames) — aggregate or debounce
