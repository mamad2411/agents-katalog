---
name: deep-linking
description: Deep linking setup for Flutter apps — app_links package, iOS Universal Links (AASA), Android App Links (assetlinks.json), URL scheme fallback, cold-start vs warm-start handlers, route table, unhandled link fallback, DI-friendly link handler, testing commands. MANDATORY TRIGGERS - "deep link", "universal link", "app link", "app_links", "apple-app-site-association", "assetlinks.json", "cold start link", "warm start", "url scheme".
allowed-tools: Read, Glob, Edit, Write
---

# Skill: deep-linking

## When to use

Adding a new deep-linkable route, updating the AASA or assetlinks.json,
debugging a cold-start link that routes to the wrong screen, or verifying
that social share links open the app correctly.

---

## Inputs

- New route path (e.g. `/post/{id}`, `/topic/{slug}/posts`)
- Whether the route requires authentication
- Platform(s): iOS, Android, or both
- Your app's custom URL scheme and universal-link domain (replace the
  `app://` scheme and `example.com` domain used below with your own)

---

## Steps

### 1. app_links wiring

`app_links` is the single source of truth for inbound link streams on
both platforms. It handles:
- iOS Universal Links
- Android App Links
- Custom URL scheme fallback (e.g. `app://`)

Reference: [app_links pub.dev](https://pub.dev/packages/app_links)

```dart
// lib/core/push/deep_link_router.dart
@lazySingleton
class DeepLinkRouter {
  DeepLinkRouter(this._router, this._session);

  final GoRouter _router;
  final SessionManager _session;
  late final _appLinks = AppLinks();
  StreamSubscription<Uri>? _sub;

  Future<void> init() async {
    // Cold start: app was terminated, opened via link
    final initial = await _appLinks.getInitialLink();
    if (initial != null) {
      // Defer routing until session state resolves
      await _session.readyCompleter.future;
      _route(initial);
    }

    // Warm start: app in background, link received
    _sub = _appLinks.uriLinkStream.listen(
      _route,
      onError: (e) => logger.e('DeepLinkRouter', error: e),
    );
  }

  void _route(Uri uri) {
    final path = _toInternalPath(uri);
    if (path == null) {
      // Unhandled link: navigate to the app's home route with a toast
      _router.go('/home');
      _showUnhandledLinkToast();
      return;
    }
    _router.go(path);
  }

  void dispose() => _sub?.cancel();
}
```

### 2. Route table

Example deep-linkable routes — replace with your app's actual entities
and paths, but keep the shape (custom scheme, HTTPS universal link,
internal path, auth requirement) as a single source of truth:

| Custom scheme | HTTPS universal | Internal path | Auth required |
|--------------|-----------------|---------------|---------------|
| `app://post/{id}` | `https://example.com/p/{id}` | `/post/:id` | No (view) |
| `app://item/{id}` | `https://example.com/i/{id}` | `/item/:id` | No (view) |
| `app://profile/{handle}` | `https://example.com/u/{handle}` | `/profile/:handle` | No |
| `app://topic/{slug}/posts` | `https://example.com/t/{slug}` | `/topic/:slug/posts` | No |
| `app://chat/{convId}` | — | `/chat/:convId` | Yes |
| `app://notification/{id}` | — | Resolves to underlying target | Yes |

If your route params need normalization (case-folding, decoding), do it
once in a shared helper:
```dart
String _normalizeSlug(String s) => s.toLowerCase().replaceAll('%24', '');
```

Reference: [Flutter deep linking](https://docs.flutter.dev/ui/navigation/deep-linking)

### 3. Internal path mapping

```dart
String? _toInternalPath(Uri uri) {
  // Validate scheme
  if (!_isAllowedUri(uri)) return null;

  // Custom scheme: app://post/01HXXXX
  if (uri.scheme == 'app') {
    return _mapCustomScheme(uri);
  }

  // Universal link: https://example.com/p/01HXXXX
  if (uri.host == 'example.com') {
    return _mapUniversalLink(uri);
  }

  return null;
}

bool _isAllowedUri(Uri uri) =>
    uri.scheme == 'app' ||
    (uri.scheme == 'https' && uri.host == 'example.com');

String? _mapCustomScheme(Uri uri) {
  final segments = uri.pathSegments;
  if (segments.isEmpty) return '/home';
  return switch (segments[0]) {
    'post'         => '/post/${segments.getOrNull(1)}',
    'item'         => '/item/${segments.getOrNull(1)}',
    'profile'      => '/profile/${segments.getOrNull(1)}',
    'topic'        => '/topic/${_normalizeSlug(segments.getOrNull(1) ?? '')}',
    'chat'         => '/chat/${segments.getOrNull(1)}',
    'notification' => _resolveNotification(segments.getOrNull(1)),
    _              => null,
  };
}
```

### 4. Cold-start vs warm-start handlers

**Cold start** (app terminated):
- `_appLinks.getInitialLink()` returns the Uri once.
- Session may not be ready yet — defer routing with a `Completer`.
- The `GoRouter` `redirect` function handles auth: if the route requires
  auth and session is `LoggedOut`, redirect to `/auth/sign-in` with the
  deep link stored in `extra` for post-login redirect.

**Warm start** (app backgrounded):
- `_appLinks.uriLinkStream` emits the Uri.
- Session is already available.
- Route immediately.

### 5. iOS Universal Links setup

**AASA file**: Must be served at exactly:
`https://example.com/.well-known/apple-app-site-association`

- No redirect.
- `Content-Type: application/json` (or `application/pkcs7-mime` for signed).
- Must be reachable by Apple's CDN validation servers.

Template: `.claude/skills/deep-linking/templates/apple-app-site-association.json.example`

**Entitlement** in `ios/Runner/Runner.entitlements`:
```xml
<key>com.apple.developer.associated-domains</key>
<array>
  <string>applinks:example.com</string>
</array>
```

**Verify cold start** on simulator:
```bash
xcrun simctl openurl booted "https://example.com/p/01HXXXX"
```

**Verify on device**:
```bash
# Open Safari, navigate to the URL — should prompt to open in app
```

Reference: [Apple Universal Links setup](https://developer.apple.com/ios/universal-links/)

### 6. Android App Links setup

**assetlinks.json**: Must be served at:
`https://example.com/.well-known/assetlinks.json`

Template: `.claude/skills/deep-linking/templates/assetlinks.json.example`

The SHA-256 fingerprint must be the Play App Signing certificate fingerprint
(not the upload keystore). Retrieve from Play Console → Setup → App integrity → App signing.

**AndroidManifest.xml** intent filter:
```xml
<intent-filter android:autoVerify="true">
  <action android:name="android.intent.action.VIEW" />
  <category android:name="android.intent.category.DEFAULT" />
  <category android:name="android.intent.category.BROWSABLE" />
  <data android:scheme="https" android:host="example.com" />
</intent-filter>

<!-- Custom scheme fallback -->
<intent-filter>
  <action android:name="android.intent.action.VIEW" />
  <category android:name="android.intent.category.DEFAULT" />
  <category android:name="android.intent.category.BROWSABLE" />
  <data android:scheme="app" />
</intent-filter>
```

**Verify**:
```bash
adb shell pm get-app-links com.example.app
# Expected: "verified" status for example.com

adb shell am start \
  -W -a android.intent.action.VIEW \
  -d "https://example.com/p/01HXXXX" com.example.app
```

Reference: [Android App Links verification](https://developer.android.com/training/app-links/verify-android-applinks)

### 7. Custom URL scheme fallback

The custom scheme (e.g. `app://`) is the fallback for contexts where
universal links cannot be used (email clients, some third-party apps).
Register in:

**iOS** `Info.plist`:
```xml
<key>CFBundleURLTypes</key>
<array>
  <dict>
    <key>CFBundleURLSchemes</key>
    <array>
      <string>app</string>
    </array>
    <key>CFBundleURLName</key>
    <string>com.example.app</string>
  </dict>
</array>
```

**Android** already covered by the custom scheme `<intent-filter>` above.

**Social share links must use universal links**, not the custom scheme.
iOS 9+ Safari will not open custom URL schemes from the web; universal
links work seamlessly from Safari and most social apps.

### 8. Unhandled deep-link fallback

When a URI cannot be resolved to an internal route:
1. Navigate to the app's home route (or stay on current page if already
   there).
2. Show a toast via `t.deepLink.linkNotFound` (localized "link not
   found" message).
3. Log `analytics.deep_link.unhandled` with the URI scheme (not the full
   URI — may contain sensitive path components).

Do not crash or navigate to a blank page.

### 9. Share-to-other-apps payload format

When sharing an entity externally, always generate a universal link:

```dart
String shareUrl(Post post) => 'https://example.com/p/${post.id}';
String shareUrl(Item item) => 'https://example.com/i/${item.id}';
```

Never share a custom-scheme URL (e.g. `app://...`) as the primary share
payload — it will not open in a browser for non-users.

---

## Output

- `DeepLinkRouter.init()` called in `bootstrap.dart`.
- New route added to `_toInternalPath` switch table.
- AASA / assetlinks.json updated for new path pattern.
- `GoRouter` redirect handles auth state for auth-required routes.
- `xcrun simctl` / `adb am start` test command documented in PR.

---

## Anti-patterns

- Routing arbitrary URIs from deep links without scheme validation — open
  redirect vulnerability.
- Using the custom scheme as the primary share URL — it will not open in
  browsers.
- Calling `GoRouter.go()` before session state is resolved on cold start —
  leads to redirect loops.
- Storing the full deep-link URI in analytics events — path segments may
  contain user IDs; log only the route template.
- Setting `autoVerify="false"` on the App Links intent filter — this
  downgrades App Links to standard deep links (browser disambiguation dialog).

---

## See also

- `.claude/skills/push-notifications/SKILL.md` — notification tap → deep link
- `.claude/skills/ios-release/SKILL.md` — associated domains entitlement
- `.claude/skills/android-release/SKILL.md` — assetlinks.json, intent filter
- your project's frontend architecture doc — deep link contract
