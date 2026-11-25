---
name: deep-link-patterns
description: "Ready-to-adapt apple-app-site-association and assetlinks.json files, entitlements and intent filters, go_router deep links, Branch deferred links, and simulator and adb test commands. Use when configuring or testing Universal Links, App Links, or deferred deep links."
---

# Deep Link Patterns

## apple-app-site-association (AASA)

### Format (iOS 13+ with components)
```json
{
  "applinks": {
    "apps": [],
    "details": [
      {
        "appIDs": ["TEAMID1234.com.myapp.ios"],
        "components": [
          {
            "/": "/product/*",
            "comment": "Product detail pages"
          },
          {
            "/": "/user/*/settings",
            "comment": "User settings with wildcard"
          },
          {
            "/": "/checkout",
            "?": { "ref": "?" },
            "comment": "Checkout with optional ref param"
          },
          {
            "/": "/admin/*",
            "exclude": true,
            "comment": "Exclude admin paths"
          }
        ]
      }
    ]
  },
  "webcredentials": {
    "apps": ["TEAMID1234.com.myapp.ios"]
  }
}
```

Server requirements:
- Served at exactly `https://yourdomain.com/.well-known/apple-app-site-association`
- No redirect (Apple's crawler doesn't follow redirects)
- `Content-Type: application/json`
- No `.json` file extension

### iOS Entitlement (Xcode)
```xml
<!-- In MyApp.entitlements -->
<key>com.apple.developer.associated-domains</key>
<array>
  <string>applinks:yourdomain.com</string>
  <string>applinks:www.yourdomain.com</string>
</array>
```

### iOS Handling (SwiftUI)
```swift
@main
struct MyApp: App {
    var body: some Scene {
        WindowGroup {
            ContentView()
                .onOpenURL { url in
                    DeepLinkRouter.handle(url)
                }
        }
    }
}

class DeepLinkRouter {
    static func handle(_ url: URL) {
        let components = URLComponents(url: url, resolvingAgainstBaseURL: false)
        let pathComponents = url.pathComponents

        switch pathComponents.dropFirst().first {
        case "product":
            let productId = pathComponents.dropFirst(2).first
            // Navigate to product detail
        case "user":
            // Handle user profile
        default:
            // Fallback: open home screen
            break
        }
    }
}
```

---

## assetlinks.json (Android)

```json
[
  {
    "relation": ["delegate_permission/common.handle_all_urls"],
    "target": {
      "namespace": "android_app",
      "package_name": "com.myapp.android",
      "sha256_cert_fingerprints": [
        "AB:CD:EF:..."
      ]
    }
  }
]
```

Get SHA-256 fingerprint:
```bash
keytool -list -v -keystore release.keystore -alias mykey -storepass password \
  | grep SHA256

# Or from Play Console: Setup > App integrity > App signing certificate
```

### AndroidManifest.xml Intent Filter
```xml
<activity android:name=".MainActivity">
    <!-- Standard launcher intent -->
    <intent-filter>
        <action android:name="android.intent.action.MAIN"/>
        <category android:name="android.intent.category.LAUNCHER"/>
    </intent-filter>

    <!-- App Links (verified HTTPS) -->
    <intent-filter android:autoVerify="true">
        <action android:name="android.intent.action.VIEW"/>
        <category android:name="android.intent.category.DEFAULT"/>
        <category android:name="android.intent.category.BROWSABLE"/>
        <data
            android:scheme="https"
            android:host="yourdomain.com"
            android:pathPrefix="/product"/>
    </intent-filter>
</activity>
```

### Android Handling (Kotlin)
```kotlin
class MainActivity : AppCompatActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        handleDeepLink(intent)
    }

    override fun onNewIntent(intent: Intent?) {
        super.onNewIntent(intent)
        intent?.let { handleDeepLink(it) }
    }

    private fun handleDeepLink(intent: Intent) {
        val uri = intent.data ?: return
        if (intent.action != Intent.ACTION_VIEW) return

        val pathSegments = uri.pathSegments
        when (pathSegments.firstOrNull()) {
            "product" -> {
                val productId = pathSegments.getOrNull(1)
                navigateToProduct(productId)
            }
            "user" -> navigateToProfile(uri.lastPathSegment)
            else -> { /* Home screen */ }
        }
    }
}
```

---

## Flutter Deep Links with go_router

```dart
// pubspec.yaml
// dependencies:
//   go_router: ^13.0.0
//   app_links: ^6.0.0

final router = GoRouter(
  routes: [
    GoRoute(path: '/', builder: (_, __) => const HomeScreen()),
    GoRoute(
      path: '/product/:id',
      builder: (context, state) {
        final id = state.pathParameters['id']!;
        return ProductDetailScreen(productId: id);
      },
    ),
    GoRoute(
      path: '/user/:id/settings',
      builder: (context, state) => UserSettingsScreen(
        userId: state.pathParameters['id']!,
      ),
    ),
  ],
);

// In main widget
class MyApp extends StatefulWidget {
  @override
  State<MyApp> createState() => _MyAppState();
}

class _MyAppState extends State<MyApp> {
  final _appLinks = AppLinks();

  @override
  void initState() {
    super.initState();
    _initDeepLinks();
  }

  Future<void> _initDeepLinks() async {
    // Handle cold start (app opened from link)
    final uri = await _appLinks.getInitialAppLink();
    if (uri != null) router.go(uri.path);

    // Handle warm start (app already running)
    _appLinks.uriLinkStream.listen((uri) {
      router.go(uri.path);
    });
  }

  @override
  Widget build(BuildContext context) => MaterialApp.router(routerConfig: router);
}
```

---

## Branch.io Deferred Deep Linking

```swift
// iOS AppDelegate
func application(_ application: UIApplication,
                 didFinishLaunchingWithOptions launchOptions: [UIApplication.LaunchOptionsKey: Any]?) -> Bool {
    Branch.getInstance().initSession(launchOptions: launchOptions) { params, error in
        guard error == nil, let params = params as? [String: AnyObject] else { return }
        if let productId = params["+productId"] as? String {
            // User installed app via a product deep link — navigate to product
            AppRouter.shared.navigateToProduct(productId)
        }
    }
    return true
}
```

---

## Testing Commands

```bash
# iOS Universal Link test (Simulator)
xcrun simctl openurl booted "https://yourdomain.com/product/123"

# Android App Link test
adb shell am start -W -a android.intent.action.VIEW \
  -d "https://yourdomain.com/product/123" com.myapp.android

# Verify Android App Links status
adb shell pm get-app-links com.myapp.android

# Test AASA file is accessible
curl -I https://yourdomain.com/.well-known/apple-app-site-association

# Validate assetlinks
curl https://yourdomain.com/.well-known/assetlinks.json
```
