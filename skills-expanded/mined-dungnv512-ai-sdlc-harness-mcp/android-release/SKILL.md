---
name: android-release
description: Android Play Store release checklist for Flutter apps — AndroidManifest.xml, Gradle signing, R8/ProGuard keep rules, App Bundle (AAB), Play Integrity, Data Safety form, adaptive icons, splash screen, App Links, fastlane supply. MANDATORY TRIGGERS - "android release", "play store", "play console", "androidmanifest", "gradle signing", "r8", "proguard", "app bundle", "aab", "play app signing", "play integrity", "data safety", "adaptive icon", "splash screen api", "fastlane supply".
allowed-tools: Read, Glob, Edit, Write
---

# Skill: android-release

## When to use

Any task touching the Android distribution pipeline: manifest permissions,
signing configuration, App Bundle builds, Play Store track promotions, Data
Safety form updates, adaptive icons, or App Links setup.

> Signing config in `android/app/build.gradle` is release-engineer territory
> (CLAUDE.md §9). Claude documents what is needed; humans implement.

---

## Inputs

- Feature slug or release tag
- New Android permissions the feature requires
- Domain(s) for App Links (e.g. `example.com`)
- Target Play Console track (`internal` / `alpha` / `beta` / `production`)

---

## Steps

### 1. AndroidManifest.xml essentials

File: `android/app/src/main/AndroidManifest.xml`

**Permissions — declare only what is used:**

```xml
<!-- Always present -->
<uses-permission android:name="android.permission.INTERNET" />
<uses-permission android:name="android.permission.ACCESS_NETWORK_STATE" />

<!-- Camera: KYC, avatar capture -->
<uses-permission android:name="android.permission.CAMERA" />

<!-- Notifications: Android 13+ requires runtime permission -->
<uses-permission android:name="android.permission.POST_NOTIFICATIONS" />

<!-- Vibration: notification feedback -->
<uses-permission android:name="android.permission.VIBRATE" />

<!-- Read media — Android 13+ granular media permissions -->
<uses-permission android:name="android.permission.READ_MEDIA_IMAGES" />
<!-- Below API 33 fallback -->
<uses-permission android:name="android.permission.READ_EXTERNAL_STORAGE"
    android:maxSdkVersion="32" />
```

**Security flags (must be present):**

```xml
<application
    android:usesCleartextTraffic="false"
    android:networkSecurityConfig="@xml/network_security_config"
    android:allowBackup="false"
    android:fullBackupContent="@xml/backup_rules"
    android:dataExtractionRules="@xml/data_extraction_rules"
    ...>
```

`android:allowBackup="false"` prevents secure storage from leaking via
cloud backups. `network_security_config` enforces HTTPS and certificate
pinning in production.

**Activity `exported` flags (Android 12+):**

Every `<activity>` or `<receiver>` with an intent filter must declare
`android:exported="true|false"` explicitly. Only the main activity and the
deep-link handler should be `exported="true"`. All others: `false`.

**`<queries>` block (Android 11+):**

If the app calls `startActivity` on external apps (share sheet, browser):

```xml
<queries>
  <intent>
    <action android:name="android.intent.action.VIEW" />
    <category android:name="android.intent.category.BROWSABLE" />
    <data android:scheme="https" />
  </intent>
</queries>
```

### 2. Network Security Config

File: `android/app/src/main/res/xml/network_security_config.xml`

```xml
<?xml version="1.0" encoding="utf-8"?>
<network-security-config>
  <!-- Production: no cleartextTrafficPermitted; cert pinning enforced in Dio -->
  <base-config cleartextTrafficPermitted="false">
    <trust-anchors>
      <certificates src="system" />
    </trust-anchors>
  </base-config>

  <!-- Debug builds only: allow dev server without pinning -->
  <debug-overrides>
    <trust-anchors>
      <certificates src="system" />
      <certificates src="user" />
    </trust-anchors>
  </debug-overrides>
</network-security-config>
```

Certificate pinning for the API domain is handled by the Dio
`CertificatePinning` interceptor (`lib/core/network/`), not by this file.

### 3. Signing config (release-engineer territory)

Claude does **not** modify signing config. Document what is required:

- Keystore stored as GitHub Encrypted Secret: `KEYSTORE_JKS_BASE64`.
- `keyAlias`, `keyPassword`, `storePassword` as CI secrets.
- Production package ID: your app's applicationId (e.g. `com.example.app`).
- CI materializes the keystore at `android/keystore/prod.jks` before build.
- Build command:

```bash
flutter build appbundle \
  --flavor prod \
  -t lib/main_prod.dart \
  --release \
  --obfuscate \
  --split-debug-info=./build/symbols/prod/$BUILD_NUMBER \
  --tree-shake-icons \
  --dart-define-from-file=env/prod.json
```

**Play App Signing:** Enroll in Play App Signing so Google re-signs the
AAB before distribution. This means the upload keystore (stored in CI) and
the distribution keystore (managed by Google) are different. The upload
keystore can be rotated safely.

### 4. R8 / ProGuard keep rules

File: `android/app/proguard-rules.pro`

See `.claude/skills/android-release/templates/proguard-rules.pro` for a
baseline. Critical categories:

- **Freezed / json_serializable**: keep generated `fromJson`/`toJson` and
  the `$` factory constructors. R8 will shrink them away otherwise.
- **Retrofit / Gson**: keep all `@SerializedName` annotations and response
  model classes.
- **Drift**: keep all `@UseMoor` and `@DataClassName` annotated classes.
- **flutter_secure_storage**: keep `EncryptedSharedPreferences` backing.
- **Firebase Messaging / Crashlytics**: included via google-services.json;
  verify ProGuard rules are imported from `google-services` plugin.

Check for R8-introduced crashes in the release build by testing on an
Android device with `--release` before promoting to Play.

### 5. App Bundle (AAB) build + Play App Signing

Always build an AAB (`appbundle`), not an APK, for Play Store submission.
AAB enables dynamic delivery and per-device split APKs.

```bash
# Verify the output
ls -lh build/app/outputs/bundle/prodRelease/app-prod-release.aab
```

After upload, Play App Signing re-signs with the distribution key. Verify
in Play Console: Setup > App integrity > App signing.

### 6. Play Console Data Safety form

Update the Data Safety section for every release that changes data
collection. Typical mapping (adapt to your app):

| Data type | Collected? | Shared? | Purpose |
|-----------|-----------|---------|---------|
| Name | Yes | No | Account functionality |
| Email | Yes | No | Account, comms |
| Phone number | Yes | No | OTP verification |
| User content | Yes | No | App functionality |
| Crash logs | Yes (opt-in) | No | Analytics |
| App interactions | Yes (opt-in) | No | Analytics |
| Device or other IDs | Yes | No | Security/fraud prevention |

Reference: [Android Developer — Data Safety](https://developer.android.com/google/play/data-safety)

### 7. Play Integrity API

Used for high-security actions (KYC submission, password change). The
Flutter layer calls the native Play Integrity plugin, sends the resulting
token to the backend, and the backend verifies with Google's API.

Minimum verdict required: `MEETS_DEVICE_INTEGRITY`.

```dart
// lib/core/security/attestation.dart
// Android path — Play Integrity
Future<String> requestPlayIntegrityToken(String nonce) async {
  // Platform channel to native PlayIntegrityManager
  final token = await _channel.invokeMethod<String>(
    'getPlayIntegrityToken',
    {'nonce': nonce},
  );
  return token!;
}
```

The nonce must be server-generated to prevent replay. Backend verifies
`appIntegrity.appRecognitionVerdict`, `deviceIntegrity.deviceRecognitionVerdict`,
and `requestDetails.nonce` against the original.

Reference: [Play Integrity API](https://developer.android.com/google/play/integrity)

### 8. Adaptive Icons

Required for all target SDK >= 26 (our minimum is API 26).

File structure:
```
android/app/src/main/res/
  mipmap-anydpi-v26/
    ic_launcher.xml          # adaptive icon definition
    ic_launcher_round.xml
  mipmap-*/
    ic_launcher_background.{png,xml}   # brand background
    ic_launcher_foreground.{png,xml}   # logo foreground
  mipmap-anydpi-v33/
    ic_launcher_monochrome.xml         # Android 13+ monochrome
```

The foreground must be contained within the 66dp safe zone (108dp total
icon size). Use a vector `ic_launcher_foreground.xml` for crispness.

### 9. Splash Screen API (Android 12+)

The system splash screen (Android 12+) is controlled via
`android:windowSplashScreenBackground` and
`android:windowSplashScreenAnimatedIcon` in the app theme.

```xml
<!-- android/app/src/main/res/values-v31/styles.xml -->
<resources>
  <style name="LaunchTheme" parent="Theme.SplashScreen">
    <item name="windowSplashScreenBackground">@color/splashBackground</item>
    <item name="windowSplashScreenAnimatedIcon">@drawable/splash_icon</item>
    <item name="windowSplashScreenIconBackgroundColor">@color/splashIconBg</item>
    <item name="postSplashScreenTheme">@style/NormalTheme</item>
  </style>
</resources>
```

In `MainActivity.kt`, call `installSplashScreen()` before `super.onCreate()`.
Flutter's `flutter_native_splash` package handles this automatically when
configured in `pubspec.yaml`.

Reference: [Splash Screen API](https://developer.android.com/develop/ui/views/launch/splash-screen)

### 10. POST_NOTIFICATIONS runtime permission (Android 13+)

Request just-in-time when the user first enables notifications in Settings,
not at launch:

```dart
// lib/features/settings/presentation/bloc/notification_settings_bloc.dart
Future<void> _onNotificationsToggled(event, emit) async {
  final status = await Permission.notification.request();
  if (status.isGranted) {
    await _pushService.subscribeToChannel(NotificationChannel.all);
    emit(state.copyWith(notificationsEnabled: true));
  }
}
```

Add `// PERM: POST_NOTIFICATIONS — user-initiated in notification settings`
comment wherever the permission is first requested.

Reference: [Android 13 notification permission](https://developer.android.com/develop/ui/views/notifications/notification-permission)

### 11. App Links (Android verification)

Intent filter for App Links in AndroidManifest.xml:

```xml
<intent-filter android:autoVerify="true">
  <action android:name="android.intent.action.VIEW" />
  <category android:name="android.intent.category.DEFAULT" />
  <category android:name="android.intent.category.BROWSABLE" />
  <data android:scheme="https" android:host="example.com" />
</intent-filter>
```

`assetlinks.json` must be served at
`https://<your-domain>/.well-known/assetlinks.json`.

Template: `.claude/skills/android-release/templates/assetlinks.json.example`

Verify:
```bash
adb shell pm get-app-links <your-application-id>
# Expected: "verified" for <your-domain>
```

Reference: [Android App Links verification](https://developer.android.com/training/app-links/verify-android-applinks)

### 12. Play release tracks

| Track | Audience | Command |
|-------|---------|---------|
| Internal testing | Engineers + QA (~20) | `fastlane play_internal` |
| Closed testing (alpha) | Beta cohort (~200) | `fastlane play_alpha` |
| Open testing (beta) | Self-selecting public | `fastlane play_beta` |
| Production | All users | `fastlane play_prod` (with phased rollout) |

Use phased rollout (1% → 10% → 50% → 100%) for production. Monitor
crash rate in Play Console's Android Vitals before advancing.

### 13. Play Console policy hot-spots (common)

| Policy | Concern |
|--------|---------|
| Financial services | If the app touches financial data, add a disclaimer clarifying informational vs. licensed-advice scope |
| User-generated content | Moderation policy must be reachable from within the app |
| Sensitive permissions (CAMERA, READ_MEDIA) | Justify in Play Console permission declaration form |
| Target SDK | Must be within one year of the current API level per Google's requirements |

Reference: [fastlane supply](https://docs.fastlane.tools/actions/supply/)

---

## Output

- `android/app/src/main/AndroidManifest.xml` updated
- `android/app/src/main/res/xml/network_security_config.xml` verified
- `android/app/proguard-rules.pro` updated if new libraries added
- Adaptive icon assets confirmed present
- PR note confirming Play Data Safety form updated

---

## Anti-patterns

- `android:usesCleartextTraffic="true"` — CI Semgrep blocks this.
- Signing config hardcoded in `build.gradle` — keystore and passwords must
  come from CI env vars, never from the repo.
- Building APK for Play Store — always build AAB.
- Missing `android:exported` on activities/receivers with intent filters —
  causes install failure on Android 12+.
- Requesting `POST_NOTIFICATIONS` at app launch — must be just-in-time.
- Adding ProGuard `-dontwarn` wildcards — fix the actual warning instead.

---

## See also

- `.claude/skills/deep-linking/SKILL.md` — App Links + assetlinks.json
- `.claude/skills/mobile-security/SKILL.md` — Play Integrity, root detection
- `.claude/skills/push-notifications/SKILL.md` — FCM, notification channels
