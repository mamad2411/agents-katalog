# App Distribution & Store Optimization Standards

**Version**: 2.7.0  
**Applies to**: iOS, Android, PWAs, cross-platform apps  
**Last Updated**: 2026-04-09

---

## 🎯 Core Principle

App distribution spans: building releases, signing, app store submission, versioning, beta testing, and user acquisition. This standard covers the entire lifecycle from development build to production release.

---

## 📦 Release Build Process

### iOS Release Build

**Prerequisites**
- Apple Developer account ($99/year)
- Paid Developer certificate (not free)
- Distribution provisioning profile
- App ID with all required capabilities

**Build Process**

```bash
# 1. Increment version in Xcode
# Project → General → Version 1.0.0 → Build 1

# 2. Create release archive
# Xcode → Product → Scheme: Release → Build For → Running
# Product → Archive

# 3. Validate archive
# Window → Organizer → Archives → Validate App

# 4. Export for distribution
# Window → Organizer → Archives → Export
# Select "Apple ID" as distribution method
# (Xcode auto-signs with distribution certificate)

# 5. Upload to App Store
# Xcode handles submission to TestFlight first
# Then review and submit for App Store review
```

**Signing Configuration**
```
Xcode Project → Build Settings → Signing:
- Signing Certificate: "Apple Distribution" (not development)
- Provisioning Profile: "App Store" profile
- Development Team: Your Team ID
- Code Signing Identity: Apple Distribution
```

**Version Format**
- **Version**: 1.0.0 (marketing version, shows to users)
- **Build**: 1 (internal, increments every build)
- Both must increment before submission

**Info.plist Requirements**
```xml
<key>CFBundleVersion</key>
<string>1</string>
<key>CFBundleShortVersionString</key>
<string>1.0.0</string>

<!-- Required for submission -->
<key>NSAppTransportSecurity</key>
<dict>
    <key>NSAllowsArbitraryLoads</key>
    <false/>
</dict>
<key>NSLocalNetworkUsageDescription</key>
<string>Your app needs to access local network...</string>
<key>NSBonjourServices</key>
<array>
    <string>_myservice._tcp</string>
</array>
```

### Android Release Build

**Prerequisites**
- Google Play account ($25 one-time fee)
- Upload key (keystore file, sign once)
- App signing key (Google manages in Play Console)

**Build Process**

```bash
# 1. Create upload keystore (one-time)
keytool -genkey -v -keystore upload-keystore.jks \
  -keyalg RSA -keysize 2048 -validity 10000 \
  -alias upload-key

# 2. Configure signing in app/build.gradle
signingConfigs {
    release {
        keyStore file("upload-keystore.jks")
        keyStorePassword "password"
        keyAlias "upload-key"
        keyPassword "password"
    }
}

buildTypes {
    release {
        signingConfig signingConfigs.release
        minifyEnabled true
        shrinkResources true
        proguardFiles getDefaultProguardFile('proguard-android-optimize.txt'), 'proguard-rules.pro'
    }
}

# 3. Build release APK / AAB
./gradlew bundleRelease  # Creates app-release.aab (recommended)
./gradlew assembleRelease  # Creates app-release.apk (legacy)

# 4. Upload to Play Console
# Google Play Console → Your App → Release → Internal Testing → Upload
```

**Version Format**
- **versionCode**: 1 (must increment every release, used internally)
- **versionName**: "1.0.0" (marketing version)

**AndroidManifest.xml Requirements**
```xml
<manifest ...>
    <uses-permission android:name="android.permission.INTERNET" />
    <uses-permission android:name="android.permission.ACCESS_NETWORK_STATE" />
    
    <application ...>
        <activity android:name=".MainActivity" />
    </application>
</manifest>
```

---

## 🏪 App Store Submission

### iOS App Store Review

**Common Rejection Reasons**

| Issue | Solution |
|-------|----------|
| Crashes on review device | Test on real device (not simulator) |
| Uses private APIs | Audit code for non-public frameworks |
| Incomplete app | Ensure all screens functional, no "Coming Soon" |
| No privacy policy | Add privacy URL in App Store Connect |
| Deceptive marketing | Match app description to actual features |
| External payment bypass | Use in-app purchases, not external links |
| Excessive permissions | Only request necessary permissions |

**App Store Connect Setup**
1. Create App ID (com.company.appname)
2. Create App record
3. Fill: Name, Description, Keywords, Category, Rating
4. Add Screenshots (2-5 per language)
5. Add Privacy Policy URL
6. Set Age Rating (Parental Controls questionnaire)
7. Configure In-App Purchases if needed
8. Upload build from Xcode
9. Add Release Notes
10. Submit for Review (typically 24-48 hours)

**Metadata Best Practices**
- **Name**: 30 chars max, include keyword (e.g., "Task Pro - To-Do Manager")
- **Subtitle**: 30 chars max, differentiator
- **Keywords**: 100 chars total, comma-separated, high-volume + long-tail
- **Description**: 4000 chars, benefits + features + screenshots callouts
- **Screenshots**: First 2 are most critical (show main feature)

### Google Play Store Review

**Common Rejection Reasons**

| Issue | Solution |
|-------|----------|
| Non-functional | Launch app successfully, all buttons work |
| Privacy violations | Never share data without consent |
| Inappropriate content | Correctly rate app (4+ if no mature content) |
| Misleading description | Match description to actual app |
| Malware detected | Run Play Protect scan, submit for re-review |
| External payment | Use Google Play Billing Library |

**Play Console Setup**
1. Create App (name + category)
2. Fill: Title (50 chars), Short Description (80 chars), Full Description (4000 chars)
3. Add Screenshots (2-8 recommended, landscape + portrait)
4. Manage Ratings (answer parental controls questions)
5. Configure Pricing & Distribution
6. Upload AAB to Internal Testing
7. Move to Staging / Production
8. Review and publish

**Metadata Best Practices**
- **Title**: 50 chars, include keyword
- **Short Description**: 80 chars, summary
- **Full Description**: User benefits + key features + links
- **Screenshots**: Show core features, test before uploading

---

## 🧪 Beta Testing

### iOS TestFlight

```
App Store Connect → Your App → TestFlight:

1. Add Internal Testers (Apple ID)
2. Add External Testers (email addresses)
3. Upload build
4. Review metadata (app preview, test notes)
5. Send invite link to testers
6. Testers install via TestFlight app
7. Feedback collected in TestFlight
```

**Best Practices**
- Release to internal testers first (employees)
- Fix critical issues before external
- External testing: min 48hrs before App Store submission
- Collect feedback: crashes, UI issues, features

### Android Internal Testing

```
Play Console → Your App → Testing → Internal Testing:

1. Create release with build
2. Add internal testers (Google group or email list)
3. Send invite link
4. Testers access app via Play Store (limited beta)
5. Monitor crash reports + ANR (Application Not Responding)
```

**Staged Rollout**
- Start with 1% of users
- Monitor crash rate, ratings
- Increase to 5%, then 10%, then 100%
- Pause if crash rate > 0.5%

---

## 📊 Versioning Strategy

### Semantic Versioning: MAJOR.MINOR.PATCH

**MAJOR** (1.0.0 → 2.0.0)
- Breaking changes (major UI overhaul, removed features, API incompatibility)
- User expects significant feature set change
- Frequency: ~1 per year

**MINOR** (1.0.0 → 1.1.0)
- New features (backward compatible)
- Frequency: ~1-2 per month

**PATCH** (1.0.0 → 1.0.1)
- Bug fixes, security patches
- Frequency: ~1 per week

**Examples:**
- 1.0.0: Initial launch
- 1.0.1: Bug fixes
- 1.1.0: Add dark mode
- 1.1.1: Fix dark mode crash
- 1.2.0: Add offline support
- 2.0.0: Complete UI redesign

### Build Numbers

**iOS**: Build numbers separate from version
- Version 1.0.0, Build 1
- Version 1.0.0, Build 2 (if rejecting and resubmitting)
- Version 1.0.1, Build 3

**Android**: versionCode must increment every release
```gradle
android {
    defaultConfig {
        versionCode 1  // Must increment for every release
        versionName "1.0.0"
    }
}
```

---

## 📱 App Size Optimization

### iOS

**Target**: < 150 MB on-device (App Store limit was 200 MB OTA, now app clips/bundling)

**Optimization Techniques**
- Asset optimization: compress PNG, use WebP where possible
- Code splitting: lazy load frameworks
- Remove unused code: -ObjC flag can bloat binary
- Swift optimizations: whole module optimization in release builds

**Build Settings for Release**
```
Xcode → Build Settings → Release:
- Optimization Level: Fastest, Smallest [-Osize]
- Link-Time Optimization (LTO): Yes
- Dead Code Stripping: Yes
- Symbols Hidden by Default: Yes
```

### Android

**Target**: < 150 MB APK (App Bundle handles this)

**Optimization Techniques**
```gradle
android {
    buildTypes {
        release {
            minifyEnabled true  // Remove unused code
            shrinkResources true  // Remove unused resources
            proguardFiles getDefaultProguardFile('proguard-android-optimize.txt'), 'proguard-rules.pro'
        }
    }
}
```

**ProGuard Rules Example**
```
# Keep API classes (example)
-keep class com.example.api.** { *; }

# Remove logging in production
-assumenosideeffects class android.util.Log {
    public static *** d(...);
    public static *** v(...);
    public static *** i(...);
}

# Optimize aggressively
-optimizations code/simplification/arithmetic,code/simplification/cast,field/*,class/merging/*
-optimizationpasses 5
```

---

## 🔄 Update Strategy

### Over-The-Air Updates (OTA)

**Options:**
1. **App Store / Play Store**: Standard, user controls updates
2. **Code push (CodePush, EAS Updates)**: Instant, for React Native / Expo
3. **Web**: JavaScript bundle via CDN (instant)

**CodePush Example (React Native)**
```typescript
import CodePush from 'react-native-code-push';

const App = () => {
  CodePush.sync({
    updateDialog: {
      optionalUpdateMessage: 'Update available',
      optionalInstallButtonLabel: 'Install',
    },
  });
  
  return <AppContent />;
};

export default CodePush(App);
```

### Forced Updates

Only force updates for **critical security fixes**:
```typescript
const MIN_VERSION = '1.0.1'; // Security fix

const checkUpdateRequired = async () => {
  const serverMinVersion = await api.get('/min-version');
  
  if (compareVersions(appVersion, serverMinVersion) < 0) {
    // Show modal: "Please update"
    showForcedUpdateDialog();
  }
};
```

---

## 📈 User Acquisition & Marketing

### App Store Optimization (ASO)

**Keywords**
- Research with App Annie, Mobile Action, Sensor Tower
- Include in: Title, Subtitle, Keywords field
- Long-tail keywords (e.g., "offline to-do" not just "to-do")

**Screenshots**
- Highlight top 2 features in first 2 screenshots
- Use text overlays: "Add tasks offline" + "Sync when online"
- Test A/B: submit with different screenshots, compare conversion

**Ratings & Reviews**
- Prompt for review after successful action (e.g., created task)
- Never block access if user declines review
- Respond to negative reviews (Play Console / App Store)
- Fix issues mentioned in reviews (shows responsiveness)

### Acquisition Channels

| Channel | Cost | Audience |
|---------|------|----------|
| Organic (ASO) | $0 | High intent (searching for app) |
| Apple Search Ads | $0.25-$5 CPM | Targeted keywords |
| Facebook / Instagram | $0.50-$2 CPI | Broad demographic |
| TikTok Ads | $0.50-$1 CPI | Younger users |
| Influencer | $500-$5K | Niche audiences |

---

## 📋 Release Checklist

- [ ] Version incremented (major/minor/patch)
- [ ] Build number incremented
- [ ] All crashes fixed (no TODOs in code)
- [ ] Security audit complete (no hardcoded secrets)
- [ ] Performance: app launches in < 3 seconds
- [ ] Offline mode tested (if applicable)
- [ ] Screenshots updated + A/B tested
- [ ] Release notes written (user-facing)
- [ ] Privacy policy updated if needed
- [ ] Tested on real device (iOS: iPhone + iPad, Android: phone + tablet)
- [ ] Code obfuscation enabled (Android ProGuard/R8, iOS link-time opt)
- [ ] Analytics event tracking verified
- [ ] Crash reporting configured (Sentry, Firebase Crashlytics)
- [ ] Beta tested for 48+ hours
- [ ] All critical paths E2E tested
- [ ] Deep links verified
- [ ] Notifications working (iOS + Android)
- [ ] Push certificate / key uploaded
- [ ] Ready for submission

---

## 🚀 Post-Launch Monitoring

### Metrics to Track

```typescript
// Firebase Analytics
firebase.analytics().logEvent('app_launched');
firebase.analytics().logEvent('feature_used', { feature_name: 'offline_mode' });
firebase.analytics().logEvent('crash_detected', { error: err.message });

// Crash Reporting
firebase.crashlytics().recordError(error);

// Performance Monitoring
firebase.performance().trace('app_startup').stop();
```

### Key Metrics

| Metric | Target | Tool |
|--------|--------|------|
| Crash-Free Users | 99%+ | Crashlytics |
| App Launch Time | < 3s | Performance Monitor |
| Frame Rate | 60 FPS | Android Profiler |
| Battery Impact | < 5% drain/hour | Xcode Energy Impact |
| Rating | 4.5+ | App Store / Play Store |

---

**Version**: 2.7.0  
**Last Updated**: 2026-04-09  
**Author**: SmartWorkz Dev
