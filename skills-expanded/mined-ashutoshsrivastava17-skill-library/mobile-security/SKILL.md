---
name: mobile-security
description: >
  Harden mobile apps against attacks — certificate pinning, code obfuscation,
  root/jailbreak detection, biometric auth, secure storage, reverse engineering
  prevention, and app integrity checks across Flutter, Android (Kotlin/Java),
  and iOS (Swift/ObjC).
  TRIGGER when: user says /mobile-security, asks about securing a mobile app,
  needs certificate pinning, biometric auth, code obfuscation, or app hardening.
argument-hint: "[app or security concern to address]"
user-invocable: true
---

# Mobile Security Hardening

You are a senior mobile security engineer. Help the user design, implement, and audit mobile app security with platform-specific guidance and actionable checklists.

## Process

### Step 1: Assess the Threat Surface

| Question | Why It Matters |
|----------|---------------|
| What sensitive data does the app handle? (auth tokens, PII, financial, health) | Determines encryption and storage requirements |
| Does the app communicate with backend APIs? | Network security, cert pinning |
| Is the app in a regulated industry? (finance, health, government) | Compliance-driven security requirements |
| Is the app distributed publicly or enterprise-only? | Public apps face reverse engineering attacks |
| Does the app handle payments? | PCI-DSS, in-app purchase integrity |
| What is the minimum OS version? | Older OS versions have known vulnerabilities |

### Step 2: Secure Network Communication

#### Certificate Pinning

Prevents MITM attacks by validating the server's certificate against a known pin.

**Flutter:**
```dart
// Using Dio with certificate pinning
class CertPinningInterceptor extends Interceptor {
  @override
  void onRequest(RequestOptions options, RequestInterceptorHandler handler) {
    (options.extra['dio_http_client_adapter'] as IOHttpClientAdapter?)
        ?.onHttpClientCreate = (client) {
      client.badCertificateCallback = (cert, host, port) => false;
      final context = SecurityContext();
      context.setTrustedCertificatesBytes(trustedCertBytes);
      return HttpClient(context: context);
    };
    handler.next(options);
  }
}

// Using http_certificate_pinning package
final result = await HttpCertificatePinning.check(
  serverURL: 'https://api.example.com',
  headerHttp: {},
  sha: SHA.SHA256,
  allowedSHAFingerprints: ['AA:BB:CC:DD:...'],
  timeout: 50,
);
```

**Android (Kotlin) — OkHttp:**
```kotlin
// Network security config (preferred for Android 7+)
// res/xml/network_security_config.xml
/*
<network-security-config>
    <domain-config>
        <domain includeSubdomains="true">api.example.com</domain>
        <pin-set expiration="2025-12-31">
            <pin digest="SHA-256">AABB.../pin>
            <pin digest="SHA-256">CCDD...</pin> <!-- backup pin -->
        </pin-set>
    </domain-config>
</network-security-config>
*/

// OkHttp CertificatePinner (programmatic)
val client = OkHttpClient.Builder()
    .certificatePinner(
        CertificatePinner.Builder()
            .add("api.example.com", "sha256/AABB...")
            .add("api.example.com", "sha256/CCDD...") // backup
            .build()
    )
    .build()
```

**Android (Java):**
```java
CertificatePinner pinner = new CertificatePinner.Builder()
    .add("api.example.com", "sha256/AABB...")
    .build();
OkHttpClient client = new OkHttpClient.Builder()
    .certificatePinner(pinner)
    .build();
```

**iOS (Swift) — URLSession:**
```swift
// URLSessionDelegate for pinning
class PinningDelegate: NSObject, URLSessionDelegate {
    let pinnedHashes: Set<String> = ["AABB...", "CCDD..."]

    func urlSession(_ session: URLSession,
                    didReceive challenge: URLAuthenticationChallenge,
                    completionHandler: @escaping (URLSession.AuthChallengeDisposition, URLCredential?) -> Void) {
        guard let trust = challenge.protectionSpace.serverTrust,
              let cert = SecTrustGetCertificateAtIndex(trust, 0) else {
            completionHandler(.cancelAuthenticationChallenge, nil)
            return
        }
        let serverHash = sha256(SecCertificateCopyData(cert) as Data)
        if pinnedHashes.contains(serverHash) {
            completionHandler(.useCredential, URLCredential(trust: trust))
        } else {
            completionHandler(.cancelAuthenticationChallenge, nil)
        }
    }
}

// Using TrustKit (recommended library)
let config: [String: Any] = [
    kTSKSwizzleNetworkDelegates: false,
    kTSKPinnedDomains: [
        "api.example.com": [
            kTSKPublicKeyHashes: ["AABB...", "CCDD..."],
            kTSKEnforcePinning: true,
            kTSKIncludeSubdomains: true
        ]
    ]
]
TrustKit.initSharedInstance(withConfiguration: config)
```

**Best practices:**
- Always include a backup pin (in case primary certificate rotates)
- Set expiration dates and monitor for upcoming certificate renewals
- Pin the public key hash, not the certificate (survives certificate renewal if key stays same)
- Handle pinning failures gracefully — log and fail closed, don't fall back to unpinned

#### Secure API Communication

| Practice | Implementation |
|----------|---------------|
| HTTPS only | Enforce via network security config (Android) / ATS (iOS) |
| No cleartext traffic | `android:usesCleartextTraffic="false"`, ATS enabled by default on iOS |
| Token refresh | Interceptor that refreshes expired tokens before retrying request |
| Request signing | HMAC signature on request body to prevent tampering |
| Response validation | Validate response structure and types, don't trust server blindly |

### Step 3: Secure Local Data

| Data Type | Secure Storage | Platform |
|-----------|---------------|----------|
| **Auth tokens** | flutter_secure_storage / EncryptedSharedPreferences / Keychain | All |
| **API keys** | Build-time injection (not in source) | All |
| **User PII** | Encrypted database (SQLCipher, encrypted Room, encrypted Core Data) | All |
| **Biometric-gated secrets** | Keystore + BiometricPrompt / Keychain + LAContext / local_auth | All |
| **Session data** | In-memory only, clear on background if sensitive | All |
| **Cached images/files** | App-internal storage, not external/shared | All |

**Flutter — Secure Storage:**
```dart
final storage = const FlutterSecureStorage(
  aOptions: AndroidOptions(encryptedSharedPreferences: true),
  iOptions: IOSOptions(accessibility: KeychainAccessibility.first_unlock),
);
await storage.write(key: 'token', value: authToken);
// Automatically uses Keychain (iOS) and EncryptedSharedPreferences (Android)
```

**Android — EncryptedSharedPreferences + Keystore:**
```kotlin
// Master key backed by Android Keystore (hardware-backed on supported devices)
val masterKey = MasterKey.Builder(context)
    .setKeyScheme(MasterKey.KeyScheme.AES256_GCM)
    .build()

val securePrefs = EncryptedSharedPreferences.create(
    context, "secure_prefs", masterKey,
    EncryptedSharedPreferences.PrefKeyEncryptionScheme.AES256_SIV,
    EncryptedSharedPreferences.PrefValueEncryptionScheme.AES256_GCM
)

// Biometric-gated key
val masterKey = MasterKey.Builder(context)
    .setKeyScheme(MasterKey.KeyScheme.AES256_GCM)
    .setUserAuthenticationRequired(true)
    .setRequestStrongBoxBacked(true) // hardware security module
    .build()
```

**iOS — Keychain with access control:**
```swift
// Keychain with biometric protection
let accessControl = SecAccessControlCreateWithFlags(
    nil,
    kSecAttrAccessibleWhenPasscodeSetThisDeviceOnly,
    .biometryCurrentSet,
    nil
)

let query: [String: Any] = [
    kSecClass as String: kSecClassGenericPassword,
    kSecAttrAccount as String: "auth_token",
    kSecValueData as String: tokenData,
    kSecAttrAccessControl as String: accessControl!,
    kSecUseAuthenticationContext as String: LAContext()
]
SecItemAdd(query as CFDictionary, nil)
```

### Step 4: Implement Biometric Authentication

#### Flutter
```dart
final localAuth = LocalAuthentication();

// Check availability
final canAuth = await localAuth.canCheckBiometrics;
final biometrics = await localAuth.getAvailableBiometrics();

// Authenticate
final authenticated = await localAuth.authenticate(
  localizedReason: 'Authenticate to access your account',
  options: const AuthenticationOptions(
    stickyAuth: true,
    biometricOnly: false, // allow PIN/pattern as fallback
  ),
);
```

#### Android (Kotlin)
```kotlin
val biometricPrompt = BiometricPrompt(
    this,
    ContextCompat.getMainExecutor(this),
    object : BiometricPrompt.AuthenticationCallback() {
        override fun onAuthenticationSucceeded(result: BiometricPrompt.AuthenticationResult) {
            val cipher = result.cryptoObject?.cipher
            // Use cipher to decrypt protected data
        }
        override fun onAuthenticationError(errorCode: Int, errString: CharSequence) {
            // Handle error (user cancelled, lockout, etc.)
        }
    }
)

val promptInfo = BiometricPrompt.PromptInfo.Builder()
    .setTitle("Authentication required")
    .setSubtitle("Verify your identity")
    .setAllowedAuthenticators(BIOMETRIC_STRONG or DEVICE_CREDENTIAL)
    .build()

biometricPrompt.authenticate(promptInfo, BiometricPrompt.CryptoObject(cipher))
```

#### iOS (Swift)
```swift
let context = LAContext()
var error: NSError?

if context.canEvaluatePolicy(.deviceOwnerAuthenticationWithBiometrics, error: &error) {
    context.evaluatePolicy(
        .deviceOwnerAuthenticationWithBiometrics,
        localizedReason: "Authenticate to access your account"
    ) { success, error in
        if success {
            // Access Keychain items protected by biometric
        }
    }
}

// Check biometric type
switch context.biometryType {
case .faceID: print("Face ID")
case .touchID: print("Touch ID")
case .opticID: print("Optic ID") // Vision Pro
case .none: print("No biometrics")
}
```

**Best practices:**
- Always provide a non-biometric fallback (PIN/password)
- Use biometrics to gate access to a Keystore/Keychain key, not as a standalone check
- Handle biometric enrollment changes (new fingerprint added → invalidate keys)
- Don't store biometric data yourself — always use platform APIs

### Step 5: Code Obfuscation & Tamper Protection

#### Flutter
```bash
# Build with obfuscation
flutter build apk --obfuscate --split-debug-info=build/symbols
flutter build ipa --obfuscate --split-debug-info=build/symbols

# Keep symbol mapping for crash reporting (upload to Firebase/Sentry)
```

#### Android — R8/ProGuard
```proguard
# proguard-rules.pro
-keepattributes SourceFile,LineNumberTable  # readable crash reports
-renamesourcefileattribute SourceFile

# Obfuscate everything except what's needed
-keep class com.example.app.data.models.** { *; }  # API models (Gson/Moshi)
-keep class * implements android.os.Parcelable { *; }

# Enable aggressive optimization
-optimizationpasses 5
-allowaccessmodification
```

```kotlin
// build.gradle.kts
android {
    buildTypes {
        release {
            isMinifyEnabled = true    // enables R8
            isShrinkResources = true  // removes unused resources
            proguardFiles(
                getDefaultProguardFile("proguard-android-optimize.txt"),
                "proguard-rules.pro"
            )
        }
    }
}
```

#### iOS — Xcode Build Settings
```
// Xcode build settings for release
SWIFT_COMPILATION_MODE = wholemodule
SWIFT_OPTIMIZATION_LEVEL = -O         // or -Osize for smaller binary
STRIP_INSTALLED_PRODUCT = YES
STRIP_SWIFT_SYMBOLS = YES
DEPLOYMENT_POSTPROCESSING = YES
GCC_GENERATE_DEBUGGING_SYMBOLS = NO   // for release
```

**Additional obfuscation tools:**
- **iXGuard / DexGuard** — commercial, advanced obfuscation + tamper detection
- **SwiftShield** — string and class name obfuscation for Swift
- **ProGuard / R8** — built-in for Android (free)

### Step 6: Root / Jailbreak Detection

| Platform | Approach |
|----------|---------|
| **Flutter** | `flutter_jailbreak_detection`, `safe_device` packages |
| **Android** | Check for su binary, test-keys, known root apps, SafetyNet/Play Integrity API |
| **iOS** | Check for Cydia, writable system paths, sandbox integrity |

**Android — Play Integrity API (recommended):**
```kotlin
val integrityManager = IntegrityManagerFactory.create(applicationContext)
val integrityTokenRequest = IntegrityTokenRequest.builder()
    .setNonce(generateNonce())
    .build()

integrityManager.requestIntegrityToken(integrityTokenRequest)
    .addOnSuccessListener { response ->
        // Send token to your server for verification
        verifyOnServer(response.token())
    }
```

**iOS — Jailbreak detection checks:**
```swift
func isJailbroken() -> Bool {
    // Check for known jailbreak files
    let paths = [
        "/Applications/Cydia.app",
        "/Library/MobileSubstrate/MobileSubstrate.dylib",
        "/bin/bash", "/usr/sbin/sshd", "/etc/apt",
        "/private/var/lib/apt/"
    ]
    for path in paths {
        if FileManager.default.fileExists(atPath: path) { return true }
    }

    // Check if app can write outside sandbox
    let testPath = "/private/jailbreak_test.txt"
    do {
        try "test".write(toFile: testPath, atomically: true, encoding: .utf8)
        try FileManager.default.removeItem(atPath: testPath)
        return true
    } catch { return false }

    // Check if app can open cydia URL scheme
    if UIApplication.shared.canOpenURL(URL(string: "cydia://")!) { return true }

    return false
}
```

**Important caveats:**
- Root/jailbreak detection is a **speed bump**, not a wall — determined attackers can bypass it
- Always verify integrity server-side (Play Integrity / App Attest), not just client-side
- Decide policy: block app entirely, disable sensitive features, or log for monitoring
- Don't rely solely on client-side checks for security-critical decisions

### Step 7: Prevent Reverse Engineering

| Technique | Platform | Effect |
|-----------|----------|--------|
| Code obfuscation | All | Makes decompiled code harder to read |
| String encryption | Android (DexGuard), iOS (SwiftShield) | Hides hardcoded strings |
| Anti-debugging | All | Detect and block debugger attachment |
| Integrity checks | All | Detect binary modification |
| Play Integrity / App Attest | Android / iOS | Server-side device and app verification |
| SSL pinning | All | Prevents traffic interception |

**iOS — App Attest (server-verified integrity):**
```swift
import DeviceCheck

let attestService = DCAppAttestService.shared
if attestService.isSupported {
    attestService.generateKey { keyId, error in
        guard let keyId = keyId else { return }
        // Store keyId, use for attestation
        attestService.attestKey(keyId, clientDataHash: challengeHash) { attestation, error in
            // Send attestation to server for verification
        }
    }
}
```

### Step 8: Secure Data in Transit & At Rest

| Concern | Implementation |
|---------|---------------|
| **Screenshot prevention** | `FLAG_SECURE` (Android), `UIScreen` notification (iOS), not native in Flutter (use platform channels) |
| **Clipboard protection** | Clear clipboard after timeout, use `UIPasteboardDetectionPattern` (iOS 14+) |
| **Background snapshot** | Overlay blur/blank view in `onPause`/`applicationDidEnterBackground` |
| **Logging** | Strip all logs in release builds (`timber` with release tree, `os_log` with appropriate levels) |
| **Debug builds** | Disable debug features, assert `!BuildConfig.DEBUG` on sensitive paths |

**Android — Prevent screenshots:**
```kotlin
// In Activity
window.setFlags(
    WindowManager.LayoutParams.FLAG_SECURE,
    WindowManager.LayoutParams.FLAG_SECURE
)
```

**iOS — Hide content on app switch:**
```swift
// In SceneDelegate or AppDelegate
func sceneWillResignActive(_ scene: UIScene) {
    let blurEffect = UIBlurEffect(style: .light)
    let blurView = UIVisualEffectView(effect: blurEffect)
    blurView.frame = window?.bounds ?? .zero
    blurView.tag = 999
    window?.addSubview(blurView)
}

func sceneDidBecomeActive(_ scene: UIScene) {
    window?.viewWithTag(999)?.removeFromSuperview()
}
```

## App Hardening Checklist

### Pre-Release Security Audit

- [ ] **Network:** HTTPS enforced, no cleartext traffic, certificate pinning configured
- [ ] **Storage:** All sensitive data in secure storage (Keychain / EncryptedSharedPrefs / flutter_secure_storage)
- [ ] **Auth:** Biometric authentication uses platform Keystore/Keychain, not standalone check
- [ ] **Tokens:** Auth tokens have expiry, refresh logic handles token rotation
- [ ] **Obfuscation:** Code obfuscation enabled for release builds (R8, --obfuscate, Swift optimization)
- [ ] **Logging:** No sensitive data in logs, logging stripped or reduced in release builds
- [ ] **Debugging:** Debugger detection or anti-debug in release builds
- [ ] **Integrity:** Play Integrity API (Android) / App Attest (iOS) integrated for server verification
- [ ] **Root/Jailbreak:** Detection implemented with appropriate policy (block/warn/log)
- [ ] **Screenshots:** Prevented on sensitive screens (banking, auth)
- [ ] **Background:** Content hidden when app enters background (task switcher)
- [ ] **Clipboard:** Sensitive data cleared from clipboard after timeout
- [ ] **Deep links:** Input validated from deep link parameters (no injection)
- [ ] **WebViews:** JavaScript disabled unless required, no `file://` access, validate URLs
- [ ] **Secrets:** No API keys, tokens, or credentials in source code or assets
- [ ] **Dependencies:** Third-party SDKs audited for data collection and permissions
- [ ] **Permissions:** Only necessary permissions requested, justified in store listing
- [ ] **Backup:** Sensitive data excluded from auto-backup (`android:allowBackup`, excluded from iCloud)
- [ ] **Export compliance:** Encryption usage declared for App Store

## Output Format

```markdown
## Security Assessment
- **Platform:** [Flutter / Android / iOS]
- **Risk Level:** [Low / Medium / High / Critical]
- **Sensitive Data:** [What data the app handles]

## Findings
| # | Category | Finding | Severity | Recommendation |
|---|----------|---------|----------|----------------|
| 1 | ... | ... | ... | ... |

## Hardening Plan
[Prioritized list of security improvements]

## Compliance Notes
[Regulatory requirements if applicable]
```

## Edge Cases

- Certificate pinning can cause outages if certificates rotate without pin updates — implement pin expiry monitoring and emergency bypass mechanism (controlled by server, not hardcoded)
- Root/jailbreak detection false positives occur on some custom ROMs and enterprise MDM devices — provide a way to report false positives
- Biometric APIs behave differently across Android manufacturers — test on Samsung, Pixel, and Xiaomi at minimum
- On Android, `EncryptedSharedPreferences` requires API 23+ — provide fallback for older devices
- Flutter's `flutter_secure_storage` uses Keychain (iOS) and EncryptedSharedPreferences (Android) under the hood — but on older Android (<23), it falls back to AES encryption with key stored in SharedPreferences (less secure)
- Apple requires a privacy nutrition label declaration for any encryption, biometric, or tracking usage
- Apps using non-standard encryption may require US export compliance documentation (ERN/CCATS)
