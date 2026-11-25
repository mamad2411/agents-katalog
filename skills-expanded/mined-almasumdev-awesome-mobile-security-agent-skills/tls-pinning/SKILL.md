---
name: tls-pinning
description: TLS certificate pinning on mobile — pin sets, backup pins, kill switch, and library-specific wiring for OkHttp, URLSession, Dio, and TrustKit. Use when hardening the network layer.
---

# TLS Certificate Pinning

## Instructions

Certificate pinning raises the cost of an active MITM with a user-trusted CA. Done wrong, it bricks your app. Done right, it's a small, durable control.

### 1. Pin Subject Public Key Info (SPKI), Not Certificates

Pinning a full certificate breaks every time the cert is rotated (typically yearly). Pin the **SPKI SHA-256** of the leaf **or** of an intermediate / root you control. SPKI survives cert renewal as long as the key does.

Generate a pin:

```bash
openssl s_client -servername api.example.com -connect api.example.com:443 \
  </dev/null 2>/dev/null | openssl x509 -pubkey -noout \
  | openssl pkey -pubin -outform DER \
  | openssl dgst -sha256 -binary \
  | base64
```

### 2. Always Ship Backup Pins

Ship at least **two** pins per hostname:

- The current live pin.
- One or more pins that are not currently live (next-gen key, or a well-controlled intermediate).

If you ship only the current pin and the key rotates unexpectedly, every installed app is dead until users update.

### 3. Kill Switch

Your server must be able to tell the app "stop enforcing pinning". Options:

- A signed remote config (`/config/v1/pinning`) fetched on launch before any sensitive call.
- Enforcement disabled if config is missing / expired (fail-open for pinning) — this is the intentional trade-off, because fail-closed is worse than no pinning at all in an incident.

Audit this: a kill switch that can be flipped by an attacker with auth to your backend is fine; one that ships by default disabled is useless.

### 4. Android — OkHttp

```kotlin
val pinner = CertificatePinner.Builder()
    .add("api.example.com",
         "sha256/AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA=")
    .add("api.example.com",
         "sha256/BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB=") // backup
    .build()

val client = OkHttpClient.Builder()
    .certificatePinner(if (killSwitch.enabled) pinner else CertificatePinner.DEFAULT)
    .build()
```

You can also use `network_security_config.xml`:

```xml
<domain-config>
  <domain includeSubdomains="true">api.example.com</domain>
  <pin-set expiration="2027-01-01">
    <pin digest="SHA-256">AAAA...=</pin>
    <pin digest="SHA-256">BBBB...=</pin>
  </pin-set>
</domain-config>
```

`expiration` makes the pin set self-disarm on a known date — a backstop to misconfiguration.

### 5. iOS — URLSession + TrustKit

```swift
let config: [String: Any] = [
  kTSKSwizzleNetworkDelegates as String: false,
  kTSKPinnedDomains as String: [
    "api.example.com": [
      kTSKEnforcePinning as String: true,
      kTSKIncludeSubdomains as String: true,
      kTSKPublicKeyHashes as String: [
        "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA=",
        "BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB=",
      ],
      kTSKExpirationDate as String: "2027-01-01",
    ]
  ]
]
TrustKit.initSharedInstance(withConfiguration: config)
```

Rolling your own with `URLSessionDelegate` / `SecTrustEvaluateWithError` is viable but error-prone — prefer TrustKit.

### 6. Flutter — Dio

```dart
final dio = Dio();
(dio.httpClientAdapter as IOHttpClientAdapter).createHttpClient = () {
  final client = HttpClient();
  client.badCertificateCallback = (cert, host, port) {
    final spki = sha256.convert(cert.der).bytes; // pseudo
    return pinned.contains(base64.encode(spki));
  };
  return client;
};
```

Prefer `dio_certificate_pinning` or move the enforcement to the platform side (OkHttp / TrustKit) via a native channel — it's harder to bypass than pure-Dart.

### 7. React Native

- iOS: wire TrustKit into the native module.
- Android: use `network_security_config.xml` or a custom OkHttp client exposed to JS.
- `react-native-ssl-pinning` is a common package but review its CVE history before adopting.

### 8. Do Not Pin in Debug

Pinning breaks Charles / mitmproxy, which you need for debugging. Disable or replace pins in debug builds, but ensure that path cannot ship (check `BuildConfig.DEBUG`, `#if DEBUG`, `kDebugMode`).

## Checklist

- [ ] Pins are SPKI SHA-256, not full certificates.
- [ ] At least one backup pin is shipped.
- [ ] A remote kill switch exists and is tested.
- [ ] Pin set has an `expiration` date (where the framework supports it).
- [ ] Pinning is disabled in debug builds, but cannot ship disabled.
- [ ] Only production hostnames are pinned (no staging / analytics unless intentional).
- [ ] Pin rotation runbook is documented before the first release.
