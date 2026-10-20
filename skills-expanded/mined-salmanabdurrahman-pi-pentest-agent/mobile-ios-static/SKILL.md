---
name: mobile-ios-static
description: iOS static security assessment for authorized IPA/app bundles — Info.plist analysis, entitlements review, ATS configuration audit, hardcoded-secret discovery, binary and framework inspection, URL scheme enumeration, MASVS-aligned finding classification with strict offline-only and no-backend-contact boundaries.
disable-model-invocation: true
risk: passive
allowed-modes: [mobile-pentest, reverse-engineering, forensic, ctf]
authorization-required: conditional
evidence-outputs: [evidence-hash, manifest-analysis, secret-finding-draft, entitlement-map, masvs-checklist]
---

# iOS static assessment — IPA artifact review

Use this skill to perform static security review of iOS IPA/app bundle artifacts you are authorized to analyze. Extract and audit the Info.plist for ATS exceptions and permission declarations, review code-signing entitlements, discover hardcoded secrets (API keys, tokens, cryptographic material), enumerate embedded frameworks and custom URL schemes, audit transport security configuration, and classify findings against the OWASP Mobile Application Security Verification Standard (MASVS). All analysis is offline and artifact-based. Never contact the application backend, reuse discovered credentials, or extract user data from the artifact — backend contact requires separate scope authorization and dynamic testing approval.

## Required inputs

- IPA file or `.app` bundle with verified SHA-256 hash, bundle identifier (`CFBundleIdentifier`), version (`CFBundleShortVersionString`), and build number (`CFBundleVersion`).
- Explicit authorization to decompile, extract, reverse-engineer, and statically analyze the application artifact.
- Written scope defining the app bundle, backend domains (for reference only — no contact), allowed analysis methods, and prohibited actions.
- Optional: App Store listing, app description, privacy label, and privacy policy for context on expected data handling.
- Valid authorization cache required only if backend API endpoints discovered in the artifact will be validated in later dynamic testing — static-only review does not require active authorization cache.

## Required gates

1. `pentest_agent_load_config` → `pentest_agent_validate_policy`.
2. `pentest_agent_parse_scope` for app bundle, backend, tenant, and test-account boundaries.
3. `pentest_agent_validate_target` for local app artifact and any backend endpoint before contact (deferred to dynamic phase).
4. `pentest_agent_check_authorization` before any backend contact (deferred to dynamic phase).
5. `pentest_agent_build_command` → `pentest_agent_execute_tool` for extraction and static analysis tools.
6. `pentest_agent_append_evidence` → `pentest_agent_record_finding` → report.

## Workflow

### Phase 1 — artifact intake and extraction

1. Hash the IPA file immediately: SHA-256, MD5, and SHA-1. Record the hash alongside the bundle identifier (from `Info.plist`), version string, build number, and file size.
2. Unzip the IPA (IPA is a ZIP archive containing `Payload/<AppName>.app/`). Verify the `.app` bundle structure: presence of the executable binary (Mach-O), `Info.plist`, `Frameworks/`, `PlugIns/`, `_CodeSignature/CodeResources`, and `embedded.mobileprovision`.
3. Verify the code signature: use `codesign -dvvv Payload/<AppName>.app` to inspect the signing identity, team identifier, and entitlements. A valid App Store distribution signature indicates the IPA matches the store version. An ad-hoc or development signature indicates a debug or enterprise build.
4. Inspect the provisioning profile: `embedded.mobileprovision` is a signed plist containing the allowed devices (for ad-hoc), team identifier, provisioning profile UUID, expiration date, and entitlements. Extract with `security cms -D -i embedded.mobileprovision`. Flag expired provisioning profiles or wildcard entitlements.
5. Extract the app binary's load commands with `otool -l` or `jtool -l`: identify the minimum iOS deployment target (`LC_VERSION_MIN_IPHONEOS`), supported architectures (arm64, arm64e), and whether the binary is encrypted (FairPlay `LC_ENCRYPTION_INFO`). An encrypted App Store binary requires decryption before further binary analysis — decryption requires a jailbroken device and is deferred to dynamic testing.
6. If the binary is unencrypted (enterprise or decrypted build), extract class information with `class-dump` to generate Objective-C header files. This reveals class names, method signatures, properties, and protocol conformances without full decompilation.

### Phase 2 — Info.plist security review

1. Extract `Info.plist` from the `.app` bundle and convert to XML with `plutil -convert xml1`. Review key security attributes:
   - `NSAppTransportSecurity` (ATS): dictionary defining exceptions to App Transport Security. Audit every exception domain — each one allows specific TLS downgrade behavior. Flag `NSExceptionAllowsInsecureHTTPLoads` (allows HTTP), `NSExceptionMinimumTLSVersion` below TLS 1.2, `NSExceptionRequiresForwardSecrecy` set to `false`, and `NSIncludesSubdomains` expanding exceptions to all subdomains.
   - `CFBundleURLTypes`: array of custom URL schemes the app registers to handle. For each scheme, record the scheme name and role (Viewer, Editor). Custom URL schemes are a known attack vector — any app can invoke them with arbitrary input.
   - `UIBackgroundModes`: background execution modes (audio, location, fetch, remote-notification, voip). Flag unexpected background modes that could enable persistent tracking or data exfiltration.
   - `LSApplicationQueriesSchemes`: URL schemes the app can query via `canOpenURL`. Reveals which third-party apps the app attempts to interact with.
   - Privacy usage descriptions: `NSPhotoLibraryUsageDescription`, `NSCameraUsageDescription`, `NSLocationWhenInUseUsageDescription`, `NSMicrophoneUsageDescription`, `NSContactsUsageDescription`, `NSHealthShareUsageDescription`, and others. Flag any permission declaration that lacks a corresponding purpose string (`UsageDescription` key missing or empty).
2. Check for `UIRequiredDeviceCapabilities`: hardware requirements (camera, microphone, gps, bluetooth). Validate that declared capabilities match the permissions requested — a flashlight app should not require microphone access.
3. Check `ITSAppUsesNonExemptEncryption` and `ITSEncryptionExportComplianceCode`: indicate whether the app uses encryption subject to export regulations. Presence of `ITSAppUsesNonExemptEncryption` without a compliance code is a compliance gap, not a security finding.
4. Check `FirebaseAutoInitEnabled`: if set to `false`, Firebase services require explicit initialization. If absent or `true`, Firebase initializes automatically with the bundled `GoogleService-Info.plist`.

### Phase 3 — entitlements and sandbox review

1. Extract entitlements from the code signature: `codesign -d --entitlements :- Payload/<AppName>.app`. Key entitlements to audit:
   - `com.apple.security.application-groups`: shared container group identifiers. Multiple apps from the same team can share data through app groups — validate the data shared across group members.
   - `keychain-access-groups`: keychain groups the app can access. List the groups and note whether any group prefix (`<TeamID>.*`) grants access to other apps' keychain items.
   - `com.apple.developer.associated-domains`: Universal Link domains the app handles. Each domain in the format `applinks:<domain>` must serve a valid `apple-app-site-association` file over HTTPS. Flag domains without HTTPS enforcement.
   - `aps-environment`: push notification environment (`development` or `production`). Development environment push tokens can be used to send push notifications outside the production APNs flow.
   - `com.apple.developer.networking.multipath`, `com.apple.developer.networking.networkextension`: VPN and network extension entitlements. Flag if the app can configure VPN tunnels — these entitlements should be rare outside VPN and MDM applications.
   - `get-task-allow`: if `true`, the app allows debugging with Xcode or `debugserver`. Must be `false` in App Store builds — production builds with this entitlement allow process debugging and injection.
   - `com.apple.developer.healthkit`, `com.apple.developer.healthkit.access`: HealthKit read/write access. Flag if the app requests HealthKit access without an obvious health-data use case.
   - `com.apple.developer.siri`: SiriKit integration. Flag if the app processes Siri intents containing sensitive data.
2. Check the sandbox by attempting to identify `com.apple.security.app-sandbox` entitlement. iOS apps distributed through the App Store are always sandboxed, but enterprise-signed apps may not be. A missing sandbox entitlement in an App Store build is anomalous but rare.
3. Check for iCloud entitlements: `com.apple.developer.ubiquity-kvstore-identifier` and `com.apple.developer.icloud-container-identifiers`. iCloud sync can unintentionally transfer sensitive data across devices. Flag if sensitive keychain items are synchronized to iCloud (identified by `kSecAttrSynchronizable` in dynamic analysis — static review can only flag the iCloud capability presence).

### Phase 4 — hardcoded secrets and sensitive data discovery

1. Extract all strings from the Mach-O binary: use `strings` on the executable file. Search for common secret patterns with grep: `api_key`, `apikey`, `api_secret`, `client_secret`, `access_token`, `password`, `secret`, `private_key`, `token`, `auth`, `bearer`, `credential`, `ssh-rsa`, `BEGIN RSA PRIVATE KEY`, `BEGIN CERTIFICATE`.
2. Search for secrets in `Info.plist` values: API endpoints, client IDs, and configuration strings may be stored as plist values. Flag any plist value matching a secret pattern.
3. Search for secrets in asset catalogs, JSON configuration files, and embedded property lists within the bundle: iterate all `.plist`, `.json`, `.xml`, and `.strings` files in the bundle and search for secret patterns.
4. Search for backend API endpoints: extract all URL-like strings from the binary and bundle resources. Categorize as: production API (`api.example.com`), development/staging (`dev-api.example.com`, `staging.example.com`, `test.example.com`), third-party (Firebase, analytics, ads, crash reporting), and IP addresses. Backend endpoints discovered during static analysis are out of scope for active testing until dynamic phase authorization is obtained.
5. Search for third-party SDK identifiers: Firebase project IDs, Google Cloud project IDs, AWS resource ARNs, Azure resource URIs, and other cloud service identifiers. These may be disclosed in configuration files or binary strings.
6. Search for hardcoded cryptographic keys and initialization vectors: AES keys (look for 16/24/32-byte Base64 or hex strings assigned to `key`, `secret`, `symmetricKey` variable names), RSA public keys (PEM headers), HMAC secrets, and hardcoded salts. Hardcoded symmetric keys are critical — anyone with the IPA can extract them.
7. Do not store raw secret values in evidence. Record the secret type, file path or binary offset, and category (API key, AES key, OAuth client secret, Firebase URL). Recommend immediate rotation.

### Phase 5 — transport security and ATS deep dive

1. Enumerate all `NSAppTransportSecurity` (ATS) exception domains from `Info.plist`. For each exception, document:
   - `NSExceptionAllowsInsecureHTTPLoads`: if `true`, the app allows HTTP to this domain. Flag for any domain handling authentication, payment, or personal data.
   - `NSExceptionMinimumTLSVersion`: the minimum TLS version. Flag if below `TLSv1.2` — earlier TLS versions have known vulnerabilities (POODLE for SSL 3.0, BEAST/Lucky13 for TLS 1.0, RC4 weaknesses).
   - `NSExceptionRequiresForwardSecrecy`: if `false`, the app allows non-forward-secret ciphers. Forward secrecy ensures session keys cannot be retroactively decrypted if the server private key is compromised.
   - `NSIncludesSubdomains`: if `true`, the exception applies to all subdomains. Flag if the parent domain hosts sensitive endpoints and subdomains include third-party services.
   - `NSThirdPartyExceptionAllowsInsecureHTTPLoads`, `NSThirdPartyExceptionMinimumTLSVersion`, `NSThirdPartyExceptionRequiresForwardSecrecy`: exceptions for third-party domains (ad networks, analytics). Flag if third-party domains receive sensitive data over reduced security.
   - `NSPinnedDomains`: certificate pinning configuration. Map pinned domains to SPKI hashes. Pinning is defense-in-depth — its absence is not a vulnerability, but its presence with incorrect hashes can break connectivity.
2. Calculate the ATS security posture: an app with no ATS exceptions is secure by default (all connections require HTTPS, TLS 1.2+, forward secrecy). Each exception weakens the posture. Flag if the total number of exceptions exceeds 10 or if any exception allows HTTP to a production API.
3. Verify that `NSAllowsArbitraryLoads` is not `true`. This key disables ATS entirely and allows all connections to use HTTP or weak TLS. It is incompatible with App Store submission unless justified — flag as critical if present.

### Phase 6 — frameworks, libraries, and binary analysis

1. Enumerate all embedded frameworks in `Frameworks/` and dynamic libraries linked by the binary (`otool -L`). Identify third-party frameworks: Firebase, Realm, Alamofire, AFNetworking, SDWebImage, Stripe, Mapbox, and others. For each framework, record the version (from `Info.plist` within the framework or from the framework binary's version load command).
2. Check framework versions against known vulnerabilities: use the framework name and version to search CVE databases. Flag frameworks with known exploitable CVEs, especially for networking, authentication, or cryptography frameworks.
3. Check for use of deprecated or insecure iOS APIs: search for `UIWebView` (deprecated in iOS 12, removed in iOS 18 — replaced by `WKWebView`), `NSURLConnection` (deprecated in iOS 9, replaced by `NSURLSession`), `SecTrustEvaluate` without pinning validation, and `kSecRandomDefault` misuse.
4. Check for `WKWebView` configuration issues in static binary analysis: search for `setJavaScriptEnabled` with no accompanying input validation, `addScriptMessageHandler` exposing native interfaces to JavaScript, or `setAllowsInlineMediaPlayback` without content security policy.
5. Identify PIE (Position-Independent Executable) and ARC (Automatic Reference Counting): `otool -hv` shows whether the binary has the `MH_PIE` flag. PIE is required for App Store since iOS 7 — its absence indicates a very old or non-standard build.

## Decision points

- **Escalate on ATS exception allowing HTTP to authentication or PII endpoint**: `NSExceptionAllowsInsecureHTTPLoads` for login, payment, or personal data endpoint → high; for analytics endpoint with no PII → low.
- **Escalate on `NSAllowsArbitraryLoads` enabled**: disables all ATS protections → critical.
- **Escalate on `get-task-allow` in App Store build**: allows process debugging → high; indicates the IPA is not a genuine App Store distribution.
- **Escalate on hardcoded symmetric encryption key**: AES/DES/ChaCha20 key in binary or plist → critical; all data encrypted with that key is recoverable by anyone with the IPA.
- **Escalate on hardcoded cloud service credentials**: AWS access key, Firebase service account key, Google Cloud API key with broad permissions → critical if permissions allow data access.
- **Escalate on unvalidated custom URL scheme**: URL handler processing input without host/path validation → high; can enable token theft via redirect.
- **Escalate on keychain access group with wildcard prefix**: `<TeamID>.*` access group → medium; app can access other team apps' keychain items.
- **Escalate on expired or wildcard provisioning profile**: expired profile → low (app won't launch); wildcard entitlements may grant unintended capabilities → medium.
- **Escalate on embedded framework with known critical CVE**: exploitable remote vulnerability in networking or auth framework → high; requires context on whether the vulnerable code path is reachable.
- **Escalate on HealthKit read access without health-data use case**: app reads health data without obvious health feature → high; potential privacy concern.
- **Downgrade on certificate pinning present**: defense-in-depth positive, document as good practice.
- **Downgrade on no ATS exceptions**: correct default posture, document as compliant.

## Prohibited behavior

- Contacting backend API endpoints discovered during static analysis — deferred to dynamic phase with separate authorization.
- Reusing, testing, or validating discovered API keys, tokens, or credentials against any service.
- Extracting and storing user data, PII, or proprietary information from the artifact.
- Uploading the IPA to online analysis services (VirusTotal, MobSF cloud) without owner approval.
- Modifying, repackaging, or resigning the IPA for dynamic testing without explicit authorization.
- Attempting to brute-force or decrypt FairPlay-encrypted binaries without a jailbroken device and explicit authorization.
- Sharing decrypted binaries, extracted class information, or decompiled code beyond the authorized assessment team.

## Stop conditions

- `NSAllowsArbitraryLoads` is `true` → stop, critical finding, document all ATS exceptions bypassed.
- `get-task-allow` is `true` in App Store IPA → stop, high finding, indicates non-production build.
- Hardcoded cloud credentials with data-access permissions → stop, critical finding, recommend immediate key rotation.
- Hardcoded symmetric encryption key protecting user data → stop, critical finding, recommend key migration.
- Evidence contains raw API key or token values → redact immediately, store only type and path.
- Backend endpoint discovered but scope does not cover active testing → document for dynamic phase, do not contact.

## Evidence — iOS static security matrix

For each IPA, record:

```text
IPA: <SHA-256> | Bundle: <CFBundleIdentifier> | Version: <CFBundleShortVersionString> (<CFBundleVersion>)
Signed by: <TeamIdentifier> — <SigningIdentity> | Profile UUID: <UUID> | Expiry: <date>

Info.plist:
  ATS exceptions: <count — domain list with flags>
  NSAllowsArbitraryLoads: <true | false>
  Custom URL schemes: <count — scheme list>
  Background modes: <count — mode list>
  Privacy descriptions: <total — missing description count>
  Firebase init: <auto | disabled>

Entitlements:
  get-task-allow: <true | false>
  App groups: <count — group list>
  Keychain access groups: <count — group list>
  Associated domains: <count — domain list>
  Push environment: <development | production | none>
  HealthKit: <read | write | none>
  iCloud: <kvstore | container | none>

Secrets:
  Hardcoded API keys: <count — sources>
  Hardcoded symmetric keys: <count — algorithms>
  Cloud credentials: <type — AWS/GCP/Firebase>
  Hardcoded backend URLs: <count — prod/staging/third-party>

Frameworks:
  Embedded frameworks: <count — names and versions>
  Deprecated APIs: <UIWebView | NSURLConnection | none>
  PIE enabled: <yes | no>

Transport Security posture:
  ATS fully enforced: <yes | no>
  HTTP allowed to any domain: <yes — domains | no>
  TLS < 1.2 allowed: <yes — domains | no>
  Forward secrecy disabled: <yes — domains | no>
  Certificate pinning: <yes — domains | no>

MASVS classification:
  MASVS-STORAGE-1 (sensitive data storage): <pass | fail>
  MASVS-CRYPTO-1 (cryptography): <pass | fail>
  MASVS-NETWORK-1 (network communication): <pass | fail>
  MASVS-PLATFORM-1 (platform interaction): <pass | fail>
  MASVS-CODE-1 (code quality): <pass | fail>

Overall risk: <critical | high | medium | low>
```

Never store: raw API key values, AES key bytes, OAuth client secrets embedded in the binary, full AWS/Firebase credential strings, provisioning profile UDID lists, binary decryption keys, or full `CodeResources` hashes.

## Report handoff

1. `pentest_agent_record_finding` for: ATS exceptions allowing HTTP to sensitive endpoints, `NSAllowsArbitraryLoads` enabled, `get-task-allow` in App Store build, hardcoded symmetric encryption keys, hardcoded cloud credentials, unvalidated custom URL schemes, wildcard keychain access groups, embedded frameworks with known critical CVEs, and HealthKit read access without health-data use case.
2. Reference the iOS static security matrix with MASVS classification.
3. Recommend: remove or narrow ATS exceptions — target zero exceptions for App Store builds; remove `NSAllowsArbitraryLoads` and use domain-specific exceptions only when absolutely necessary; never hardcode cryptographic keys — generate at runtime and store in the keychain; rotate hardcoded API keys and migrate to OAuth 2.0 or backend-proxy pattern; set `get-task-allow` to `false` in App Store builds; validate custom URL scheme input before processing; restrict keychain access groups to the app's own bundle identifier prefix; update embedded frameworks to latest versions to patch known CVEs; replace `UIWebView` with `WKWebView`; implement certificate pinning for high-risk domains; and verify the release IPA with `codesign` and `xcrun altool` before App Store submission.
