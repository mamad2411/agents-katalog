---
name: mitm-prevention
description: Preventing man-in-the-middle attacks on mobile — user CA posture on newer Android and iOS, cleartext traffic policies, and platform configuration. Use when configuring the app's network security baseline.
---

# MITM Prevention Baseline

## Instructions

Before pinning, get the platform baseline right. Most real-world MITM on mobile comes from misconfigured cleartext or from accepting user-installed CAs.

### 1. Android: Network Security Config

Ship an explicit `res/xml/network_security_config.xml` even if you think defaults are fine:

```xml
<?xml version="1.0" encoding="utf-8"?>
<network-security-config>
  <base-config cleartextTrafficPermitted="false">
    <trust-anchors>
      <certificates src="system"/>
      <!-- user CAs are NOT trusted by default from Android 7+ -->
    </trust-anchors>
  </base-config>

  <domain-config cleartextTrafficPermitted="false">
    <domain includeSubdomains="true">api.example.com</domain>
  </domain-config>

  <debug-overrides>
    <trust-anchors>
      <certificates src="user"/>
    </trust-anchors>
  </debug-overrides>
</network-security-config>
```

Key points:
- `cleartextTrafficPermitted="false"` blocks `http://` at the platform layer.
- `<debug-overrides>` only applies to `android:debuggable="true"` builds — perfect for Charles / mitmproxy in dev, impossible to ship enabled.
- Do **not** add `<certificates src="user"/>` to `base-config`; that is the most common cause of pinned apps being MITMed.

Wire it in `AndroidManifest.xml`:

```xml
<application
    android:networkSecurityConfig="@xml/network_security_config"
    android:usesCleartextTraffic="false"
    ... >
```

### 2. iOS: App Transport Security (ATS)

Keep ATS on. The minimum acceptable `Info.plist`:

```xml
<key>NSAppTransportSecurity</key>
<dict>
  <key>NSAllowsArbitraryLoads</key>
  <false/>
  <!-- If you truly need a narrow exception, scope it: -->
  <key>NSExceptionDomains</key>
  <dict>
    <key>legacy.partner.example</key>
    <dict>
      <key>NSIncludesSubdomains</key><true/>
      <key>NSExceptionMinimumTLSVersion</key><string>TLSv1.2</string>
      <key>NSExceptionAllowsInsecureHTTPLoads</key><false/>
    </dict>
  </dict>
</dict>
```

Never set `NSAllowsArbitraryLoads=true` globally. App Review increasingly rejects it.

### 3. User-Installed CAs

- Android 7+ (API 24): apps do **not** trust user CAs unless the manifest opts in. Good default — leave it.
- iOS: user/profile-installed CAs **are** trusted by default. Pinning is the mitigation (see [tls-pinning](../../network/tls-pinning/SKILL.md)).
- Neither platform can fully block a rooted / jailbroken device from MITMing your traffic. Layer attestation ([api-abuse-protection](../api-abuse-protection/SKILL.md)).

### 4. Detecting MITM in Production

You usually do **not** want to proactively detect MITM in-app; it becomes a cat-and-mouse game. Instead:

- Pin.
- Log pin failures server-side as a high-severity anomaly metric.
- Require attestation on sensitive endpoints.

### 5. WebViews

WebViews inherit system trust — they will happily load a proxied MITM site. Controls:

- Never load user-controlled URLs in a WebView that has access to a JS bridge.
- Disable `setAllowFileAccessFromFileURLs` / `setAllowUniversalAccessFromFileURLs` on Android.
- On iOS, prefer `ASWebAuthenticationSession` or `SFSafariViewController` for any third-party auth — they inherit Safari's protections and can't be MITMed by an in-app JS bridge.

### 6. Deep Links / Universal Links

A malicious app on Android can claim the same custom scheme as yours. Mitigations:

- Prefer **App Links** (Android) and **Universal Links** (iOS), both of which are HTTPS URLs verified by the OS against `/.well-known/assetlinks.json` or `/.well-known/apple-app-site-association`.
- Validate any deep-link parameters server-side before acting on them — never trust an `amount` or `to` field just because it arrived via the registered scheme.

### 7. Flutter / RN Specific

- Flutter's `dart:io` `HttpClient` respects Android NSC but **not** iOS ATS in every version — verify on your target. Prefer `dart:io` on iOS going through `URLSession` via a native plugin for anything sensitive.
- React Native's JS `fetch` goes through OkHttp (Android) / NSURLSession (iOS), so platform config applies. `XMLHttpRequest` for legacy libraries takes the same path.

## Checklist

- [ ] `network_security_config.xml` ships with `cleartextTrafficPermitted="false"` and no user CAs in `base-config`.
- [ ] `android:usesCleartextTraffic="false"` in the manifest.
- [ ] `NSAllowsArbitraryLoads` is `false`; any `NSExceptionDomains` are narrowly scoped.
- [ ] Debug / MITM-proxy overrides are gated to debug builds only.
- [ ] No WebView exposes `file://` access or a JS bridge to arbitrary URLs.
- [ ] Third-party auth uses `SFSafariViewController` / `ASWebAuthenticationSession`, not an in-app WebView.
- [ ] App Links / Universal Links are used for any sensitive deep link; parameters are re-validated server-side.
