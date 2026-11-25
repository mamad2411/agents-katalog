---
name: mobile-security
description: Mobile security hardening for Flutter apps — OWASP MASVS L2, biometric step-up, flutter_secure_storage options, certificate pinning, App Attest, Play Integrity, jailbreak/root detection, screenshot protection, obfuscation. MANDATORY TRIGGERS - "mobile security", "biometric", "face id", "touch id", "fingerprint", "keychain", "keystore", "cert pinning", "app attest", "play integrity", "jailbreak", "root detection", "screenshot protection", "screen recording", "mobile threats", "owasp masvs", "mstg".
allowed-tools: Read, Glob, Edit, Write
---

# Skill: mobile-security

## When to use

Implementing a feature that touches biometrics, secure storage, certificate
pinning, device integrity, or privacy-sensitive screens. Also triggered by
a security-review pass when the diff includes auth, network, storage, or
deep links.

Target: **OWASP MASVS L2** for all production flows that handle auth
tokens, PII, or financial data. Keep a project-specific security coverage
matrix documenting which controls apply to which flows.

References: [OWASP MASVS](https://mas.owasp.org/MASVS/), [OWASP MSTG](https://mas.owasp.org/MASTG/)

---

## Inputs

- Feature slug
- Diff or description of what data is stored / transmitted / rendered

---

## Steps

### 1. flutter_secure_storage — correct options

Tokens and secrets go **only** into `flutter_secure_storage`. Never into
`shared_preferences`, Hive boxes, Drift tables without encryption, or logs.

```dart
// lib/core/di/core_module.dart
@lazySingleton
FlutterSecureStorage get secureStorage => const FlutterSecureStorage(
  aOptions: AndroidOptions(
    encryptedSharedPreferences: true,   // EncryptedSharedPreferences backing
  ),
  iOptions: IOSOptions(
    accessibility: KeychainAccessibility.first_unlock_this_device_only,
    // first_unlock_this_device_only: accessible after first unlock,
    // NOT synced to iCloud, NOT accessible on a different device.
  ),
);
```

Verify:
- `encryptedSharedPreferences: true` for Android — uses AES-256-GCM backed
  by Android Keystore.
- `first_unlock_this_device_only` for iOS — satisfies AES-256-at-rest
  storage requirements per MASVS MSTG-STORAGE-1.
- No token written to `SharedPreferences` anywhere — enforce with a CI
  static-analysis rule (e.g. a Semgrep rule) if you can.

### 2. Biometric step-up for sensitive operations

Require step-up authentication before irreversible or high-sensitivity
actions: identity/KYC submission, password change, destructive confirms,
account deletion.

```dart
// lib/core/security/biometric_guard.dart
import 'package:local_auth/local_auth.dart';

@lazySingleton
class BiometricGuard {
  final _auth = LocalAuthentication();

  Future<bool> authenticate(BuildContext context) async {
    final canCheck = await _auth.canCheckBiometrics;
    final isDeviceSupported = await _auth.isDeviceSupported();
    if (!canCheck || !isDeviceSupported) {
      // Fallback: require password re-entry — never silently bypass
      return _fallbackToPassword(context);
    }
    return _auth.authenticate(
      localizedReason: t.security.biometricPrompt,
      options: const AuthenticationOptions(
        stickyAuth: true,
        biometricOnly: false, // allow device PIN as fallback
      ),
    );
  }
}
```

iOS `Info.plist` must include `NSFaceIDUsageDescription`.

Failure modes: if biometrics not enrolled OR lockout → show password
challenge dialog. Never cancel the protected action silently.

### 3. Certificate pinning

Two SPKI pins at all times (current + rotation) via the Dio
`CertificatePinning` interceptor:

```dart
// lib/core/network/certificate_pinning.dart
const _prodPins = [
  'sha256/REPLACE_WITH_CURRENT_LEAF_SPKI_HASH=',  // current cert
  'sha256/REPLACE_WITH_BACKUP_SPKI_HASH=',         // rotation backup
];

HttpClient buildPinnedClient() {
  final context = SecurityContext.defaultContext;
  return HttpClient(context: context)
    ..badCertificateCallback = (cert, host, port) {
      // NEVER return true here — enforce with a CI static-analysis rule
      return false;
    };
}
```

Pin rotation procedure:
1. New pin added to `_prodPins` array 30 days before cert rotation.
2. App release ships both pins.
3. After cert rotation, old pin removed in next release.
4. Kill-switch via Remote Config allows bypassing in catastrophic
   mis-rotation (requires signed payload from server).

Reference: [Flutter --obfuscate](https://docs.flutter.dev/deployment/obfuscate)

### 4. App Attest (iOS 14+)

Used for sensitive server calls (identity verification, password change):

```dart
// lib/core/security/attestation.dart — iOS path
Future<String> getAppAttestAssertion(String challengeFromServer) async {
  // Platform channel to DeviceCheck/AppAttest framework
  final assertion = await _channel.invokeMethod<String>(
    'getAppAttestAssertion',
    {'challenge': challengeFromServer},
  );
  return assertion!;
}
```

Flow:
1. Client requests challenge nonce from server (`GET /auth/attest/challenge`).
2. Client calls `DCAppAttestService.generateAssertion(challenge)`.
3. Client sends assertion in `X-App-Attest-Assertion` header.
4. Server verifies with Apple's DeviceCheck API.

Reference: [Apple App Attest](https://developer.apple.com/documentation/devicecheck/preparing_to_use_the_app_attest_service)

### 5. Play Integrity (Android)

Used for same sensitive server calls:

```dart
// lib/core/security/attestation.dart — Android path
Future<String> requestPlayIntegrityToken(String nonce) async {
  final token = await _channel.invokeMethod<String>(
    'getPlayIntegrityToken',
    {'nonce': nonce},
  );
  return token!;
}
```

The backend verifies the token against Google's Play Integrity API and
checks:
- `appIntegrity.appRecognitionVerdict == PLAY_RECOGNIZED`
- `deviceIntegrity.deviceRecognitionVerdict` contains `MEETS_DEVICE_INTEGRITY`
- `requestDetails.nonce` matches the server-generated nonce

Reference: [Play Integrity API](https://developer.android.com/google/play/integrity)

### 6. Jailbreak / root detection

Use `flutter_jailbreak_detection` at app start:

```dart
// lib/core/security/jailbreak_guard.dart
@lazySingleton
class JailbreakGuard {
  Future<JailbreakStatus> check() async {
    final isJailbroken = await FlutterJailbreakDetection.jailbroken;
    final isDeveloperMode = await FlutterJailbreakDetection.developerMode;
    if (isJailbroken) return JailbreakStatus.compromised;
    if (isDeveloperMode) return JailbreakStatus.developerMode;
    return JailbreakStatus.clean;
  }
}
```

Soft-warn vs hard-block matrix — adapt the specific flows to your app,
but keep the shape:

| Feature | compromised | developerMode |
|---------|-------------|---------------|
| General browsing | soft banner | none |
| Low-risk interactions (posting, voting) | soft banner | none |
| Identity verification | hard block | soft warning |
| Password change | hard block | soft warning |
| Consent / privacy settings | hard block | none |

Hard block: navigate away from the screen with an error message, do not
allow the action. Log a `security.device.trust_low` event.

### 7. Screenshot and screen recording protection

Apply on sensitive screens: private messaging, identity verification,
profile-edit, any composer that handles unsent sensitive content.

**Android** — set `FLAG_SECURE` via `flutter_windowmanager`:
```dart
await FlutterWindowManager.addFlags(FlutterWindowManager.FLAG_SECURE);
// Remove when leaving the sensitive screen:
await FlutterWindowManager.clearFlags(FlutterWindowManager.FLAG_SECURE);
```

**iOS** — overlay a privacy screen when `UIScreen.isCaptured` is true:
```dart
// lib/core/security/screen_protection.dart
// Uses the secure_application package to add a blur overlay on backgrounding
// and when screen recording is detected.
SecureApplication(
  nativeRemoveDelay: 0.0,
  child: SecureGate(
    blurr: 20,
    opacity: 0.6,
    lockedBuilder: (ctx, state) => const Center(
      child: Icon(Icons.lock_outline, size: 64),
    ),
    child: _sensitiveContent,
  ),
)
```

### 8. Copy-paste protection on sensitive inputs

For identity-document fields and financial inputs, disable paste from the
system clipboard:

```dart
TextField(
  obscureText: true,
  enableInteractiveSelection: false,  // disables long-press clipboard menu
  inputFormatters: [
    FilteringTextInputFormatter.digitsOnly,
  ],
)
```

### 9. Build obfuscation and symbol upload

Every release build includes:

```bash
flutter build appbundle \
  --obfuscate \
  --split-debug-info=./build/symbols/prod/$BUILD_NUMBER \
  ...
```

After build, upload symbols to your crash reporter (CI step — do not
skip). Example for Sentry:

```bash
sentry-cli debug-files upload \
  --org your-org \
  --project mobile-prod \
  ./build/symbols/prod/$BUILD_NUMBER
```

Without symbol upload, crash reports will show obfuscated stack
traces that cannot be deobfuscated.

### 10. Hard rules (never violate)

- **Never log PII at `info` or above.** Auth tokens, emails, phone numbers,
  identity-document numbers, message bodies are forbidden from logs.
  Configure a logger redaction filter in your app's bootstrap code.
- **Never store tokens in `SharedPreferences`.** Enforce with a CI
  static-analysis rule if you can.
- **Never disable certificate pinning in release builds.** The kill-switch
  only operates via a server-signed payload — never a simple build flag.
- **Never return `true` from `badCertificateCallback`.** Enforce with a CI
  static-analysis rule.
- **Never use `http://` scheme in network calls.**
  `android:usesCleartextTraffic="false"` and ATS enforce this at the OS
  level.

---

## Per-PR security checklist (mobile-specific)

- [ ] New sensitive field uses `flutter_secure_storage` (not `SharedPreferences`).
- [ ] New screen with user secrets has screenshot protection applied.
- [ ] New biometric-gated action handles fallback to password, not silent bypass.
- [ ] New network endpoint uses shared `Dio` instance (not ad-hoc `http`).
- [ ] Certificate pinning interceptor is in the Dio chain.
- [ ] `// PERM: <permission-name>` comment added for any new runtime permission.
- [ ] No `print()` or `debugPrint()` containing token or PII value.

---

## Anti-patterns

- Storing JWT in `SharedPreferences` or `Hive` without encryption.
- Calling `local_auth.authenticate()` with `biometricOnly: true` — this
  locks out users without enrolled biometrics on sensitive screens.
- Using `FlutterSecureStorage` with default `IOSOptions` (which uses
  `unlocked_this_device` — weaker than the recommended setting above).
- Returning `true` from `badCertificateCallback` "for debugging" — use a
  separate dev cert that is pinned in the dev flavor.
- Adding jailbreak detection only on the UI layer without a matching
  server-side device-trust header validation (e.g. `X-Device-Trust`).

---

## See also

- `.claude/skills/ios-release/SKILL.md` — PrivacyInfo.xcprivacy, App Attest entitlement
- `.claude/skills/android-release/SKILL.md` — Play Integrity, network security config
- your project's security checklist doc, if one exists
- your project's security/architecture doc — Mobile hardening section
