---
name: mobile-android-static
description: Android static security assessment for authorized APK/AAB artifacts — manifest analysis, component-export review, permission mapping, hardcoded-secret discovery, WebView hardening, network-security-config review, crypto audit, and MASVS-aligned finding classification with strict no-backend-contact and no-token-reuse boundaries.
disable-model-invocation: true
risk: passive
allowed-modes: [mobile-pentest, reverse-engineering, forensic, ctf]
authorization-required: conditional
evidence-outputs: [evidence-hash, manifest-analysis, secret-finding-draft, component-map, masvs-checklist]
---

# Android static assessment — APK artifact review

Use this skill to perform static security review of Android APK/AAB artifacts you are authorized to analyze. Decompile the application, audit the manifest for exported components and permissions, discover hardcoded secrets (API keys, tokens, cryptographic material), review WebView and network-security configurations, audit cryptographic implementations, and classify findings against the OWASP Mobile Application Security Verification Standard (MASVS). All analysis is offline and artifact-based. Never contact the application backend, reuse discovered credentials, or extract user data from the artifact — backend contact requires separate scope authorization and dynamic testing approval.

## Required inputs

- APK/AAB artifact with verified SHA-256 hash, package name, and version code/name.
- Explicit authorization to decompile, reverse-engineer, and statically analyze the application artifact.
- Written scope defining the app package, backend domains (for reference only — no contact), and allowed analysis methods.
- Optional: Play Store listing, app description, and privacy policy for context on expected behavior.
- Valid authorization cache required only if backend API endpoints discovered in the artifact will be validated in later dynamic testing — static-only review does not require active authorization cache.

## Required gates

1. `pentest_agent_load_config` → `pentest_agent_validate_policy`.
2. `pentest_agent_parse_scope` for app package, backend, tenant, and test-account boundaries.
3. `pentest_agent_validate_target` for local app artifact and any backend endpoint before contact (deferred to dynamic phase).
4. `pentest_agent_check_authorization` before any backend contact (deferred to dynamic phase).
5. `pentest_agent_build_command` → `pentest_agent_execute_tool` for decompilation and static analysis tools.
6. `pentest_agent_append_evidence` → `pentest_agent_record_finding` → report.

## Workflow

### Phase 1 — artifact intake and decompilation

1. Hash the APK/AAB immediately: SHA-256, MD5, and SHA-1. Record the hash alongside the package name, version code (`versionCode`), version name (`versionName`), and file size.
2. Verify the artifact signature: use `apksigner verify --print-certs` to inspect the signing certificate. Record the certificate fingerprint (SHA-256), issuer, subject, and validity period. Check whether the application is signed with a debug certificate (`CN=Android Debug`, `O=Android`) — debug certificates in production builds indicate the APK was not prepared for release.
3. Decompile the APK with `apktool d` to extract: `AndroidManifest.xml` (decoded), `res/` (resources — strings, layouts, drawables, raw files), `assets/` (bundled assets), `lib/` (native libraries per architecture), and `smali/` (disassembled DEX bytecode).
4. Decompile to Java source with `jadx` for readable code analysis. The Java output is not byte-perfect but is sufficient for logic review, string analysis, and vulnerability discovery. Record the jadx version used.
5. If the APK uses obfuscation (ProGuard, R8, DexGuard), note the obfuscation type. ProGuard/R8 renames classes/methods but preserves control flow; DexGuard applies additional string encryption and control-flow obfuscation.

### Phase 2 — AndroidManifest analysis

1. Extract the `AndroidManifest.xml` from apktool output and audit key attributes:
   - `android:debuggable`: should be `false` in production. `true` allows ADB debugging and application data access.
   - `android:allowBackup`: should be `false` or explicitly restricted. `true` allows ADB backup of app data, including shared preferences, databases, and internal storage.
   - `android:networkSecurityConfig`: references an XML file defining trust anchors, cleartext traffic policy, and certificate pinning. Record the reference path for further review.
   - `android:usesCleartextTraffic`: should be `false` if the app handles sensitive data. `true` allows HTTP traffic that can be intercepted.
   - `android:taskAffinity` and `android:launchMode`: review for task-hijacking susceptibility.
2. Enumerate all `<activity>`, `<service>`, `<provider>`, and `<receiver>` components. For each exported component (`android:exported="true"` or implicit export via intent filters), record:
   - Component name and type.
   - Intent filters: which actions, categories, and data schemes trigger the component.
   - Permissions protecting the component (`android:permission` or `android:protectionLevel`).
   - Whether the component handles sensitive data or privileged actions.
3. Flag any exported component without permission protection — any app on the device can invoke it. If the component passes data to other components or performs privileged operations, this is a high finding.
4. Enumerate all `<permission>` declarations: custom permissions, `protectionLevel` (normal, dangerous, signature, signatureOrSystem). Permissions defined with `protectionLevel="normal"` or `dangerous"` may be weaker than intended.

### Phase 3 — permission and capability mapping

1. Extract all requested permissions from `<uses-permission>` tags. Categorize:
   - **Normal**: `INTERNET`, `ACCESS_NETWORK_STATE`, `VIBRATE` — low sensitivity.
   - **Dangerous**: `CAMERA`, `RECORD_AUDIO`, `READ_CONTACTS`, `ACCESS_FINE_LOCATION`, `READ_SMS`, `READ_EXTERNAL_STORAGE` — requires runtime permission on Android 6+.
   - **Signature/privileged**: `BIND_DEVICE_ADMIN`, `MANAGE_EXTERNAL_STORAGE`, `SYSTEM_ALERT_WINDOW` — elevated privileges.
   - **Custom**: defined by the app itself.
2. For each dangerous permission, verify there is a legitimate use case in the app's functionality. A flashlight app requesting `READ_CONTACTS` is suspicious. Document permissions that appear excessive.
3. Check for `<uses-feature>` declarations: these declare hardware requirements (`android.hardware.camera`, `android.hardware.bluetooth`, `android.hardware.location.gps`). Validate that hardware-requiring permissions match the declared features.
4. Identify whether the app uses fingerprint/biometric authentication (`USE_BIOMETRIC`, `USE_FINGERPRINT`) and whether the biometric result is used only for local authentication (correct) or transmitted over the network (incorrect — biometric data should never leave the device).

### Phase 4 — hardcoded secrets and sensitive data discovery

1. Search for hardcoded secrets in strings resources (`res/values/strings.xml` and locale variants): grep for `api_key`, `apikey`, `api_secret`, `client_secret`, `access_token`, `password`, `secret`, `private_key`, `token`, `auth`, `bearer`.
2. Search for secrets in decompiled Java source (jadx output): grep for hardcoded string literals matching API key formats (alphanumeric strings of 20+ characters assigned to `key`, `secret`, `token` variables), Base64-encoded strings near `Authorization` header construction, and cryptographic key material.
3. Search for cloud-service credentials: AWS access keys (`AKIA*` pattern), Google Cloud service account keys, Firebase database URLs and secrets, Azure connection strings, and other platform-specific credential formats.
4. Search for backend API endpoints: extract all URL strings from strings.xml, decompiled Java, and native libraries (`lib/*.so` via `strings`). Categorize as: production API (`api.example.com`), development/staging (`dev-api.example.com`, `staging.example.com`), and third-party (Firebase, analytics, ads). Backend endpoints discovered during static analysis are out-of-scope for active testing until dynamic phase authorization is obtained.
5. Search for hardcoded cryptographic keys and IVs: AES keys (16/24/32 bytes in hex or Base64), RSA public/private keys, HMAC secrets, and hardcoded initialization vectors. Hardcoded symmetric keys are critical — they can be extracted from the APK and used to decrypt traffic or forge authentication tokens.
6. Do not store raw secret values in evidence. Record the secret type, file path, and category (API key, AES key, client secret). Recommend immediate rotation.

### Phase 5 — network security and WebView review

1. Review the network security configuration XML (referenced from `android:networkSecurityConfig` in the manifest):
   - `<base-config cleartextTrafficPermitted="true">`: should be `false` for production. `true` allows HTTP traffic.
   - `<trust-anchors>`: check whether user-installed CAs are trusted (`<certificates src="user">`). Trusting user CAs enables man-in-the-middle interception of all app traffic.
   - `<domain-config>`: per-domain cleartext and certificate pinning configuration. Check whether pinning is implemented for critical domains.
   - `<debug-overrides>`: should not be present in production builds.
2. If no `networkSecurityConfig` is declared, evaluate the defaults: Android 9+ (API 28+) blocks cleartext traffic by default; Android 8 and below allows it.
3. Audit WebView usage in decompiled Java:
   - `setJavaScriptEnabled(true)`: enables JavaScript in WebView. Should be disabled unless essential and combined with input sanitization.
   - `addJavascriptInterface(obj, name)`: exposes a Java object to JavaScript running in the WebView. If the WebView loads untrusted content, this is a critical finding — JavaScript can invoke arbitrary Java methods on the exposed object (CVE-2012-6636 and related).
   - `setAllowFileAccess(true)` and `setAllowFileAccessFromFileURLs(true)`: allows WebView to access local files. Should be `false`.
   - `setAllowUniversalAccessFromFileURLs(true)`: allows file-origin scripts to access any origin. Critical if enabled — should always be `false`.
   - `shouldOverrideUrlLoading`: check whether the app validates URLs before loading them. If the app loads any URL without scheme/host validation, WebView can be redirected to `file://` or `javascript:` URLs.
4. Check for SSL/TLS certificate validation overrides: custom `TrustManager` that accepts all certificates (empty `checkServerTrusted`), custom `HostnameVerifier` that always returns `true`, or `SSLSocketFactory` that trusts all certificates. Any of these disables TLS validation entirely — a critical finding.

### Phase 6 — cryptographic implementation review

1. Identify cryptographic operations in decompiled Java: search for `Cipher`, `Mac`, `Signature`, `KeyGenerator`, `SecretKey`, `MessageDigest`, and `SecureRandom`.
2. Audit for weak algorithms:
   - **Symmetric**: DES, 3DES, RC4, Blowfish — weak. AES-128 minimum, AES-256 preferred. ECB mode is insecure for block ciphers (identical plaintext blocks produce identical ciphertext).
   - **Hash**: MD5, SHA-1 — weak for security. SHA-256 minimum.
   - **PRNG**: `java.util.Random` — not cryptographically secure. Should use `SecureRandom`.
   - **Key derivation**: PBKDF2 with low iteration count, single SHA-1/MD5 hash without salt — weak.
3. Audit for hardcoded cryptographic material (already covered in Phase 4 — cross-reference).
4. Check whether the app implements certificate pinning: OkHttp `CertificatePinner`, TrustKit, or custom `TrustManager`. If cert pinning is present, note the pinned domains and hash algorithm. Pinning is a defense-in-depth measure — its absence is not a vulnerability by itself.
5. Check whether the Android Keystore is used for key storage. The Keystore provides hardware-backed key storage on devices with a secure element or TEE. Keys stored outside the Keystore (in SharedPreferences, files, or hardcoded) are at higher risk of extraction.

## Decision points

- **Escalate on debug certificate in production**: APK signed with `CN=Android Debug` → high; indicates the APK was not built for release.
- **Escalate on exported component without permission**: sensitive activity/service/provider accessible to any app → high; critical if the component handles authentication, payment, or personal data.
- **Escalate on JavaScript interface in WebView loading untrusted content**: `addJavascriptInterface` with `setJavaScriptEnabled` → critical if the WebView loads any URL from user input or external sources.
- **Escalate on custom TrustManager that bypasses TLS**: empty `checkServerTrusted` → critical; all HTTPS traffic can be intercepted.
- **Escalate on hardcoded symmetric encryption key**: AES/DES key in source or resources → critical; all data encrypted with that key is recoverable.
- **Escalate on hardcoded cloud service credentials**: AWS/Google/Firebase keys → critical if the keys have broad permissions.
- **Escalate on cleartext traffic permitted with sensitive data**: HTTP for login, payment, or PII endpoints → high.
- **Escalate on WebView file access enabled**: `setAllowFileAccess` + `setAllowUniversalAccessFromFileURLs` → critical.
- **Escalate on debug mode enabled**: `android:debuggable="true"` → high; `debug-overrides` in network config → high.
- **Downgrade on app-obfuscation absence**: informative — defense-in-depth gap, not a vulnerability.

## Prohibited behavior

- Contacting backend API endpoints discovered during static analysis — deferred to dynamic phase with separate authorization.
- Reusing, testing, or validating discovered API keys, tokens, or credentials against any service.
- Extracting and storing user data, PII, or proprietary information from the artifact.
- Uploading the APK to online analysis services (VirusTotal, MobSF cloud) without owner approval.
- Modifying, repackaging, or resigning the APK for dynamic testing without explicit authorization.
- Attempting to brute-force or decrypt encrypted configuration values beyond identifying the algorithm and key source.

## Stop conditions

- JavaScript interface in WebView with untrusted content → stop, critical finding, recommend immediate removal or input origin validation.
- Custom TrustManager bypassing all TLS validation → stop, critical finding.
- Hardcoded cloud service credentials with broad permissions → stop, critical finding, recommend immediate key rotation.
- Debug certificate or debug flags in production build → stop, high finding.
- Evidence contains raw API keys, token values, or credential material → redact immediately, store only type and path.

## Evidence — Android static security matrix

For each APK, record:

```text
APK: <SHA-256> | Package: <name> | Version: <code/name>
Signed with: <certificate SHA-256 subject> | Debug cert: <yes | no>

Manifest:
  debuggable: <true | false>
  allowBackup: <true | false>
  usesCleartextTraffic: <true | false | not set>
  networkSecurityConfig: <path | not declared>
  Exported activities: <count — unprotected count>
  Exported services: <count — unprotected count>
  Exported providers: <count — unprotected count>
  Exported receivers: <count — unprotected count>

Permissions:
  Dangerous permissions: <list>
  Excessive permissions: <list — permission vs likely use case>
  Custom permissions: <count>

Secrets:
  Hardcoded API keys: <count — sources>
  Hardcoded symmetric keys: <count — algorithms>
  Cloud credentials: <type — AWS/GCP/Firebase>
  Hardcoded backend URLs: <count — production/staging/third-party>

Network and WebView:
  Cleartext permitted: <yes — domain | no>
  User CAs trusted: <yes | no>
  Cert pinning: <yes — domains | no>
  JavaScript enabled in WebView: <yes — context | no>
  JavaScript interface exposed: <yes — class name | no>
  File access in WebView: <yes — flags | no>
  TLS validation overridden: <yes — method | no>

Crypto:
  Weak symmetric algorithms: <DES | 3DES | RC4 | none>
  Weak hash algorithms: <MD5 | SHA-1 | none>
  Insecure PRNG: <java.util.Random | SecureRandom>
  Keystore used: <yes | no>

MASVS classification:
  MASVS-STORAGE-1 (sensitive data storage): <pass | fail>
  MASVS-CRYPTO-1 (cryptography): <pass | fail>
  MASVS-NETWORK-1 (network communication): <pass | fail>
  MASVS-PLATFORM-1 (platform interaction): <pass | fail>
  MASVS-CODE-1 (code quality): <pass | fail>

Overall risk: <critical | high | medium | low>
```

Never store: raw API key values, symmetric key bytes, full AWS/Firebase credential strings, WebView JavaScript interface introspection output, certificate private keys, or base64-decoded token values.

## Report handoff

1. `pentest_agent_record_finding` for: debug certificate, exported components without permission, JavaScript interface in untrusted WebView, TLS validation disabled, hardcoded symmetric keys, hardcoded cloud credentials, cleartext traffic for sensitive endpoints, WebView file access, weak cryptographic algorithms, and excessive permissions.
2. Reference the Android static security matrix with MASVS classification.
3. Recommend: sign production APKs with a release certificate (not debug); set `android:exported="false"` on all components that are not intended for external access; protect exported components with `android:permission` set to a custom signature-level permission; disable `addJavascriptInterface` or ensure the WebView loads only trusted, app-bundled content; remove custom TrustManagers that bypass TLS; never hardcode cryptographic keys — generate them at runtime or use the Android Keystore; remove hardcoded API keys and use OAuth 2.0 or backend-proxy pattern; set `android:usesCleartextTraffic="false"` and configure `networkSecurityConfig` with strict domain rules; replace MD5/SHA-1 with SHA-256, DES/3DES with AES-256, and `java.util.Random` with `SecureRandom`; and run `apkanalyzer` and `bundletool` to verify the release build before publishing.
