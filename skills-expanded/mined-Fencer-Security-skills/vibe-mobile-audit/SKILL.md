---
name: vibe-mobile-audit
description: Audit a vibe-coded mobile app (Expo, React Native, native iOS / Android, occasionally Flutter) and produce a severity-tagged markdown report. Use when the user wants to security-review a mobile app — "audit my Expo app," "review my React Native app," "is this iOS app safe," "check my Android app." Covers secret storage (Keychain/Keystore vs UserDefaults/SharedPreferences/AsyncStorage), network security (ATS, NetworkSecurityConfig, cert pinning), deep links / URL schemes / intent filters, WebView and JS bridges, permissions, and backup-included data, on top of the shared baseline. Runs safe live probes against the backend API and inspects built IPA/APK for embedded secrets.
allowed-tools: Read Grep Glob
---

# Vibe-coded mobile app security audit

Audits mobile apps — Expo, React Native, native iOS (Swift / Objective-C), native Android (Kotlin
/ Java), occasionally Flutter. The threat model differs meaningfully from a webapp:

- The app ships to user devices and runs there. Anything embedded in the bundle is recoverable
  by a determined attacker.
- The OS provides secure-storage APIs (iOS Keychain, Android Keystore). Most vibe-coded apps
  use the easy-but-wrong APIs (`UserDefaults`, `SharedPreferences`, `AsyncStorage`) and put
  tokens there.
- Deep links and URL schemes are an attack surface — another app can launch yours with crafted
  parameters.
- WebView with a JS bridge to native code is a category of remote code execution.
- The backend API the app talks to has the same threat model as a `vibe-service-audit` target —
  this skill probes it, but a full backend audit is `vibe-service-audit`'s job.

## When to use this skill

Use this when the user wants to security-review a mobile app: Expo, React Native, native iOS or
Android, Flutter. Phrases like "audit my Expo app," "review my React Native app," "is this iOS
app safe," "check my Android app," or "audit this mobile build" all qualify.

Don't use this for: web apps even if they're styled like an app (use `vibe-webapp-audit`), the
mobile app's backend on its own (use `vibe-service-audit`), or PWAs / Capacitor / Ionic apps
that are essentially webapps in a wrapper (use `vibe-webapp-audit`; flag the wrapper as a
caveat).

## Inputs the skill expects

- A path to a local repo (the working directory by default).
- Optionally, the **backend API base URL** — for live probes against the API the app calls.
- Optionally, a path to a **built IPA / APK** — for embedded-secret inspection.

Ask for these at the start. Missing → skip the relevant live tests and record the gap.

## Workflow

```bash
SKILL_DIR="${CLAUDE_SKILL_DIR:-${SKILL_DIR}}"
SHARED_DIR="$SKILL_DIR/../../shared"
# Always reads:
#   $SHARED_DIR/references/baseline.md
#   $SHARED_DIR/references/live-tests-baseline.md
#   $SHARED_DIR/references/report-template.md
# Conditionally (per platform):
#   $SKILL_DIR/references/ios.md
#   $SKILL_DIR/references/android.md
#   $SKILL_DIR/references/react-native-expo.md
#   $SKILL_DIR/references/live-tests.md  (if backend URL or IPA/APK provided)
```

1. **Detect the platform** (~30s — see below).
2. **Ask for the backend URL and any built artifact path.**
3. **Run the baseline** (`$SHARED_DIR/references/baseline.md`, checks A–D).
4. **Run the category-specific static checks** (sections 1–7 below). Read the platform-specific
   reference(s).
5. **Run live tests** if a target was provided. Read `$SHARED_DIR/references/live-tests-baseline.md`
   then `$SKILL_DIR/references/live-tests.md`.
6. **Render the report** using `$SHARED_DIR/references/report-template.md`.

### Detect the platform

```bash
# React Native / Expo
grep -hE '"(react-native|expo|@react-native|@expo)"' package.json 2>/dev/null
ls app.json app.config.js app.config.ts expo.json 2>/dev/null

# Native iOS
find . -maxdepth 4 -name "*.xcodeproj" -o -name "*.xcworkspace" -o -name "Info.plist" 2>/dev/null | head -10
find . -maxdepth 5 -name "Podfile" 2>/dev/null

# Native Android
find . -maxdepth 4 -name "AndroidManifest.xml" -o -name "build.gradle" -o -name "build.gradle.kts" 2>/dev/null | head -10

# Flutter
ls pubspec.yaml 2>/dev/null
```

**MANDATORY** — pick references based on detection and read each in full before proceeding.
Do NOT load references for platforms not detected.

- **Pure native iOS** (no `react-native` / `expo` in `package.json`) → **MANDATORY:
  `$SKILL_DIR/references/ios.md`**. Do NOT load `android.md` or `react-native-expo.md`.
- **Pure native Android** → **MANDATORY: `$SKILL_DIR/references/android.md`**. Do NOT load
  `ios.md` or `react-native-expo.md`.
- **React Native or Expo** → **MANDATORY: all three of
  `$SKILL_DIR/references/react-native-expo.md`, `$SKILL_DIR/references/ios.md`,
  `$SKILL_DIR/references/android.md`**. RN/Expo apps have both platform sub-projects.
- **Flutter** → no dedicated reference yet; apply general principles. Do NOT load any reference.
  Note Flutter-specific coverage as a gap in the report.

## 1 — Secret storage

**The headline failure mode**: tokens, API keys, and PII written to the wrong storage API.
The OS provides secure storage; the vibe-coded mistake is reaching for the easy API and putting
auth tokens there.

**Before flagging, ask yourself**: is what's being stored a _credential_ (auth token, refresh
token, API key, password), an _identifier_ (user ID, device ID), or a _preference_ (theme,
last-opened tab)? Only credentials and credential-equivalents warrant High; identifiers are Low;
preferences are not findings.

| Platform     | Wrong (easy)                                        | Right                                                    |
| ------------ | --------------------------------------------------- | -------------------------------------------------------- |
| iOS          | `UserDefaults`, plain files in Documents            | `Keychain` (`kSecAttrAccessibleWhenUnlockedThisDevice…`) |
| Android      | `SharedPreferences`, plain files in `getFilesDir()` | `EncryptedSharedPreferences`, `Keystore`                 |
| React Native | `AsyncStorage`                                      | `react-native-keychain`, `expo-secure-store`             |

```bash
# React Native
grep -rE "(AsyncStorage|@react-native-async-storage)" --include="*.{ts,tsx,js,jsx}" . | head -20
grep -rE "(react-native-keychain|expo-secure-store)" --include="*.{ts,tsx,js,jsx}" . | head -10

# iOS
grep -rE "UserDefaults\.(standard|init)" --include="*.{swift,m}" . | head -20
grep -rE "(KeychainAccess|SecItemAdd|kSec)" --include="*.{swift,m}" . | head -10

# Android
grep -rE "(SharedPreferences|getDefaultSharedPreferences|getSharedPreferences)" \
  --include="*.{kt,java}" . | head -20
grep -rE "(EncryptedSharedPreferences|KeyStore|MasterKey)" --include="*.{kt,java}" . | head -10
```

**Severity:**

- Auth token / refresh token / OAuth credential in `AsyncStorage` / `UserDefaults` /
  `SharedPreferences`: **High** — recoverable from device backups, jailbroken devices, and (on
  Android pre-EncryptedSharedPreferences) other apps with similar UID.
- API key embedded in the app bundle and accessible at runtime: **Medium** — the key is in the
  app regardless of where it's read; if it's a server-secret-ish key (e.g., Twilio auth token),
  upgrade to **High**.
- PII (email, phone, location history) in plain `UserDefaults` / `SharedPreferences` without
  encryption: **Medium**.

## 2 — Network security

**Before flagging a network-security finding, ask yourself**: is the platform's _default_ safe,
and has the developer opted _out_ of it? iOS (ATS, opt-out via `NSAllowsArbitraryLoads`) and
Android (API 28+ cleartext-off, opt-out via `network_security_config.xml`) both default to
"HTTPS only." Plain HTTP requires an explicit dial-down, which is a deliberate developer act
and warrants severity. No opt-out, no finding.

**Find the platform config:**

```bash
ls app.json app.config.js ios/<project>/Info.plist android/app/src/main/res/xml 2>/dev/null

grep -hE '"(react-native-ssl-pinning|@trust-pkg/.*pinning)"' package.json 2>/dev/null
grep -rE "(URLSessionPinningDelegate|TrustKit|CertificatePinner)" \
  --include="*.{swift,m,kt,java}" . | head -10
```

iOS: read the App Transport Security block in `Info.plist`. Android: read
`network_security_config.xml` if present (referenced by `<application>` in
`AndroidManifest.xml`).

**Severity:**

- iOS `NSAllowsArbitraryLoads: YES` in `Info.plist` for production: **High** (HTTPS bypass).
- Android `cleartextTrafficPermitted: true` in `network_security_config.xml` for production:
  **High**.
- Android missing `network_security_config.xml` on API 28+ AND the app uses HTTP anywhere:
  **Medium**.
- No certificate pinning AND the app handles sensitive transactions (banking, health,
  high-value PII): **Medium** — pinning is hardening, not a baseline requirement; severity
  rises with sensitivity.

## 3 — Deep links and URL schemes

Deep links let another app (or a browser, or a phishing email) launch yours with a URL. If the
handler trusts query parameters as authority, that's an authentication-bypass.

**Before flagging a deep link handler, ask yourself**: who is the implied trust source of the
URL parameters? If the handler treats `?userId=42` as proof of identity, the user has been
impersonated. If it treats it as a hint and re-verifies against the authenticated session, the
parameter is harmless.

```bash
# iOS — URL schemes registered in Info.plist
grep -A5 "CFBundleURLSchemes" ios/<project>/Info.plist app.json 2>/dev/null

# Universal Links — apple-app-site-association
find . -name "apple-app-site-association" -o -name "assetlinks.json" 2>/dev/null

# Android intent filters
grep -A20 "<intent-filter" android/app/src/main/AndroidManifest.xml 2>/dev/null

# Expo / React Native deep link handling
grep -rE "(Linking\.(addEventListener|getInitialURL)|useURL|expo-linking)" \
  --include="*.{ts,tsx,js,jsx}" . | head -20
```

Flag:

- Deep link handler that reads an auth token / session ID from query params and signs the user
  in. **Critical** — phishing vector.
- Deep link handler that performs a destructive action (delete, transfer, change-email) without
  user confirmation. **High**.
- Android `<intent-filter>` with `android:exported="true"` for an activity that mutates state and
  doesn't re-verify the caller. **High**.
- Missing app-link verification (no `apple-app-site-association` / `assetlinks.json` for an app
  that uses universal/app links). **Medium** — opens a hijack vector if a malicious app
  registers the same URL.

## 4 — WebView usage

**Before flagging a WebView, ask yourself**: what does it load, and what does its JS bridge
expose? A WebView loading only bundled HTML is roughly as safe as the rest of the app. A
WebView loading remote URLs is a potential XSS vector. A WebView loading remote URLs _with_ a
JS bridge that calls native methods is a remote-code-execution vector. The combination is the
finding, not the WebView alone.

A WebView with a JS-to-native bridge is a category of RCE if untrusted content can reach it.

**Patterns to flag:**

| Pattern                                                                                                      | Severity     |
| ------------------------------------------------------------------------------------------------------------ | ------------ |
| `addJavascriptInterface` / `WKScriptMessageHandler` exposing native I/O / shell, AND remote-loadable WebView | **Critical** |
| WebView loading user-supplied / attacker-influenceable URLs                                                  | **High**     |
| React Native `onMessage` handler that executes message data as code or routes by it                          | **High**     |
| `UIWebView` on iOS (deprecated, removed in iOS 12+)                                                          | **Medium**   |

**Find the surface:**

```bash
# React Native
grep -rE "(WebView|react-native-webview)" --include="*.{ts,tsx,js,jsx}" . | head -10
grep -rE "(onMessage|injectedJavaScript|postMessage)" --include="*.{ts,tsx,js,jsx}" . | head -10

# iOS
grep -rE "(WKWebView|UIWebView|addScriptMessageHandler|evaluateJavaScript)" \
  --include="*.{swift,m}" . | head -10

# Android
grep -rE "(WebView|addJavascriptInterface|setJavaScriptEnabled)" --include="*.{kt,java}" . | head -10
```

## 5 — Permissions

**Before flagging a permission, ask yourself**: does the app's code actually _use_ it? Many
vibe-coded apps request permissions a template suggested (camera, location, contacts) without
the corresponding code path. Unused permissions are still findings — they expand the user's
trust surface and are a Play/App Store policy concern — but they're cleanup-level, not exploit-
level. Used-but-over-broad (e.g., `ACCESS_FINE_LOCATION` when coarse would do) is the higher-
severity case.

**Patterns to flag:**

| Pattern                                                                            | Severity                           |
| ---------------------------------------------------------------------------------- | ---------------------------------- |
| Permission requested but no corresponding code-path usage                          | **Low–Medium** (cleanup)           |
| `android.permission.QUERY_ALL_PACKAGES` without justification                      | **Medium** (Play policy + privacy) |
| `SYSTEM_ALERT_WINDOW` (overlay) for non-overlay apps                               | **Medium**                         |
| `WRITE_EXTERNAL_STORAGE` on API 30+ (should use scoped storage)                    | **Low**                            |
| `READ_PHONE_STATE` / `READ_PHONE_NUMBERS` for apps that don't need them            | **Medium**                         |
| Fine-grained when coarse would do (`ACCESS_FINE_LOCATION` for city-level features) | **Low**                            |

**Find the surface:**

```bash
# iOS — Info.plist usage descriptions
grep -E "NS.*UsageDescription" ios/<project>/Info.plist app.json 2>/dev/null
# Android — manifest permissions
grep -A1 "<uses-permission" android/app/src/main/AndroidManifest.xml 2>/dev/null
# Expo — app.json permissions section
grep -A20 "permissions" app.json app.config.js 2>/dev/null
```

## 6 — Backup and on-device exposure

**Before flagging a backup finding, ask yourself**: is sensitive data being written _somewhere_
the backup picks up? `allowBackup=true` alone isn't a finding — it's a finding when combined
with auth tokens / PII in `SharedPreferences` / app-private files. The backup path inherits the
content; if the content was safe (everything in Keystore, nothing sensitive in SharedPrefs),
the backup flag is mostly moot.

Sensitive data included in device backups (iCloud, Google Drive) is exposed wherever the
backup goes.

**Patterns to flag:**

| Pattern                                                                         | Severity                            |
| ------------------------------------------------------------------------------- | ----------------------------------- |
| Android `allowBackup="true"` AND auth tokens / PII in `SharedPreferences`/files | **Medium**                          |
| iOS files written with `NSFileProtectionNone` AND containing sensitive content  | **Medium** (locked-device readable) |
| iOS sensitive files NOT excluded from backup (and not Keychain-stored)          | **Low**                             |

**Find the surface:**

```bash
grep "allowBackup" android/app/src/main/AndroidManifest.xml 2>/dev/null
grep -rE "NSFileProtectionNone|FileProtectionType\.none" --include="*.{swift,m}" . | head -10
grep -rE "(isExcludedFromBackup|NSURLIsExcludedFromBackupKey)" --include="*.{swift,m}" . | head -10
```

## 7 — Backend API trust boundary

**Before flagging a backend-trust finding, ask yourself**: is this a _client-side_ defect
(something the client does wrong with the API response) or a _server-side_ defect (something
the backend itself does wrong)? The mobile audit only flags the client-side half. Server-side
auth gaps, IDOR, missing input validation belong to `vibe-service-audit` — recommend running
it as a follow-up if no separate backend audit happened.

The backend API the app calls is a separate threat surface — full audit belongs to
`vibe-service-audit`. In this skill, flag only the client-side issues:

- API base URL hardcoded to a development/staging host in a production bundle. **Medium**.
- Client implementing authorization decisions (e.g., "show admin UI if `user.isAdmin`") and
  trusting the server to enforce. This isn't a finding on its own (it's how all client/server
  apps work), but if the server doesn't enforce too, it's **Critical** — note that the audit
  recommends running `vibe-service-audit` against the backend.
- App accepting plain-text responses where it expects JSON (no `Content-Type` check) — surface
  for MITM injection on a misconfigured network. **Low**.

In the report's "What's next" section, recommend running `vibe-service-audit` against the
backend if one wasn't audited separately.

## Producing the report

Read `$SHARED_DIR/references/report-template.md`. Save as
`vibe-mobile-audit-<YYYY-MM-DD>-<HHMM>.md`. Tell the user the exact path.

## What this skill is NOT

- Not a mobile pen test. The skill doesn't dynamically instrument a running app or jailbreak /
  root anything.
- Not a runtime / on-device analysis. The skill is static + (optionally) bundle introspection.
- Not a store-review audit. App Store and Play Store have their own policy reviews; this
  skill doesn't predict them.
- Not a Flutter-specific audit yet — Flutter coverage is general-principles only.
