---
name: admob-integration
description: AdSpaceSDK (AdMob Next-Gen wrapper) integration for Android. Covers all ad types (Banner, Native, Interstitial, Rewarded, Rewarded Interstitial, Open App), CMP consent (UMP/GDPR), Firebase Remote Config, resume ads. Both View API (XML/Kotlin) and Jetpack Compose. Min SDK 26, Java 21.
---

# AdSpaceSDK Integration

Complete integration guide for AdSpaceSDK - an Ad Orchestration Layer wrapping Google AdMob Next-Gen SDK with CMP integration.

## Package Information

**CRITICAL**: Always use the correct package name to avoid confusion:

- **Maven Dependency**: `io.github.maichanchinh:adspace-admob:2.0.+`
- **Package Name**: `com.admob.adspace`
- **Min SDK**: Android 26 (API 26+)
- **Java/Kotlin**: Java 21, JVM target 21

All code examples use imports from `com.admob.adspace.*` package.

## Quick Start

Get AdSpaceSDK up and running in 5 minutes with this step-by-step checklist.

### Step 1: Add Dependency

Add to app module's `build.gradle.kts`:

```kotlin
dependencies {
    implementation("io.github.maichanchinh:adspace-admob:2.0.+")
}
```

Sync your Gradle project.

### Step 2: Configure AndroidManifest.xml

Add AdMob App ID in `<application>` tag:

```xml
<manifest>
    <application>
        <meta-data
            android:name="com.google.android.gms.ads.APPLICATION_ID"
            android:value="ca-app-pub-XXXXXXXXXXXXXXXX~YYYYYYYYYY"/>
    </application>
</manifest>
```

**Replace with your actual AdMob App ID** from [AdMob Console](https://apps.admob.com).

### Step 3: Create Local Config File

Create `assets/ads_config.json` in your app module:

```json
{
  "ads": {
    "global": {
      "enable": true,
      "cmp_auto": true,
      "min_interval": 30000
    },
    "spaces": [
      {
        "space": "ADMOB_Banner_Home",
        "adsType": "banner",
        "ids": ["ca-app-pub-3940256099942544/6300978111"],
        "enable": true,
        "minInterval": 30000
      },
      {
        "space": "ADMOB_Interstitial_General",
        "adsType": "interstitial",
        "ids": ["ca-app-pub-3940256099942544/1033173712"],
        "enable": true,
        "minInterval": 30000
      }
    ]
  }
}
```

**Note**: The example uses test ad unit IDs. Replace with your actual IDs before production.

### Step 4: Initialize SDK in Application

Create or update your `Application` class:

```kotlin
import android.app.Application
import com.admob.adspace.AdSpaceSDK
import com.admob.adspace.AdSpaceSDKConfig

class MyApplication : Application() {
    override fun onCreate() {
        super.onCreate()

        val config = AdSpaceSDKConfig(
            debug = BuildConfig.DEBUG,
            testDevices = emptyList(), // Optional: Add test device IDs
            minInterval = 30L, // Minimum interval between ads (seconds)
            appId = "ca-app-pub-XXXXXXXXXXXXXXXX~YYYYYYYYYY"
        )

        AdSpaceSDK.initialize(this, config)
    }
}
```

**Important**: Always use `Application Context`, never `Activity Context`.

### Step 5: Register Application in Manifest

Add to `AndroidManifest.xml`:

```xml
<application
    android:name=".MyApplication"
    ...>
```

### Step 6: Implement Your First Ad

**For Banner Ad** (XML layout):

```kotlin
import com.admob.adspace.banner.SpaceBanner

class MainActivity : AppCompatActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_main)

        // Load banner ad
        SpaceBanner.load(
            context = this,
            spaceName = "ADMOB_Banner_Home",
            adView = findViewById(R.id.adView)
        )
    }

    override fun onDestroy() {
        super.onDestroy()
        // Clean up to prevent memory leaks
        SpaceBanner.clearCache("ADMOB_Banner_Home")
    }
}
```

**For Interstitial Ad**:

```kotlin
import com.admob.adspace.interstitial.SpaceInterstitial
import com.admob.adspace.interstitial.InterstitialCallback

class MainActivity : AppCompatActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)

        // Preload interstitial
        SpaceInterstitial.preload(
            spaceName = "ADMOB_Interstitial_General",
            callback = object : InterstitialCallback {
                override fun onAdLoaded() {
                    // Ad ready to show
                }

                override fun onAdFailed(error: InterstitialError) {
                    // Handle error
                }
            }
        )
    }

    private fun showInterstitial() {
        SpaceInterstitial.show(
            activity = this,
            spaceName = "ADMOB_Interstitial_General",
            callback = object : InterstitialCallback {
                override fun onAdDismissed() {
                    // User closed ad, continue flow
                }

                override fun onAdFailed(error: InterstitialError) {
                    // Ad failed, continue flow
                }
            }
        )
    }
}
```

### Step 7: Test Your Integration

1. Run your app on a device or emulator
2. Check Logcat for AdSpaceSDK logs (tag: `AdSpaceSDK`)
3. Verify test ads are showing
4. Test CMP consent flow (if `cmp_auto: true`)

### Step 8: Prepare for Production

Before releasing, complete the [Production Readiness Checklist](#production-readiness-checklist) below.

### Quick Start Verification

After completing steps 1-7, verify:

- [ ] Gradle sync succeeds
- [ ] App launches without crashes
- [ ] Test ads display correctly
- [ ] Logcat shows "AdSpaceSDK initialized"
- [ ] CMP consent form appears (if enabled)
- [ ] No package import errors

If all checks pass, you're ready for detailed implementation!

## Quick Reference

### Common Imports

```kotlin
// Core SDK
import com.admob.adspace.AdSpaceSDK
import com.admob.adspace.AdSpaceSDKConfig

// Banner Ads
import com.admob.adspace.banner.SpaceBanner
import com.admob.adspace.banner.BannerCallback
import com.admob.adspace.banner.BannerError
import com.admob.adspace.banner.AdRevenue
import com.google.android.libraries.ads.mobile.sdk.banner.AdView

// Native Ads
import com.admob.adspace.native.SpaceNative
import com.admob.adspace.native.NativeCallback
import com.admob.adspace.native.NativeError
import com.google.android.libraries.ads.mobile.sdk.nativead.NativeAd
import com.google.android.libraries.ads.mobile.sdk.nativead.NativeAdView

// Interstitial Ads
import com.admob.adspace.interstitial.SpaceInterstitial
import com.admob.adspace.interstitial.InterstitialCallback
import com.admob.adspace.interstitial.InterstitialError

// Rewarded Ads
import com.admob.adspace.rewarded.SpaceRewarded
import com.admob.adspace.rewarded.RewardedCallback
import com.admob.adspace.rewarded.RewardedError

// Rewarded Interstitial Ads
import com.admob.adspace.rewardedinterstitial.SpaceRewardedInterstitial
import com.admob.adspace.rewardedinterstitial.RewardedInterstitialCallback
import com.admob.adspace.rewardedinterstitial.RewardedInterstitialError

// Open App Ads
import com.admob.adspace.open.SpaceOpenApp
import com.admob.adspace.open.OpenAppCallback
import com.admob.adspace.open.OpenAppError
```

## Initial Setup

### 1. Add Dependency

Add to app module's `build.gradle.kts`:

```kotlin
dependencies {
    implementation("io.github.maichanchinh:adspace-admob:2.0.+")
}
```

### 2. Configure AndroidManifest.xml

Add AdMob App ID:

```xml
<manifest>
    <application>
        <meta-data
            android:name="com.google.android.gms.ads.APPLICATION_ID"
            android:value="ca-app-pub-XXXXXXXXXXXXXXXX~YYYYYYYYYY"/>
    </application>
</manifest>
```

Replace with your actual AdMob App ID from AdMob console.

### 3. Initialize SDK

In `Application.onCreate()`:

```kotlin
import android.app.Application
import com.admob.adspace.AdSpaceSDK
import com.admob.adspace.AdSpaceSDKConfig

class MyApplication : Application() {
    override fun onCreate() {
        super.onCreate()

        val config = AdSpaceSDKConfig(
            debug = BuildConfig.DEBUG,
            testDevices = emptyList(), // Add test device IDs for testing
            minInterval = 30L, // Minimum interval between ads (seconds)
            appId = "ca-app-pub-XXXXXXXXXXXXXXXX~YYYYYYYYYY"
        )

        AdSpaceSDK.initialize(this, config)
    }
}
```

**Important**: Always use `Application Context`, never `Activity Context`.

### 4. Create Local Config File

Create `assets/ads_config.json` in your app module:

```json
{
  "ads": {
    "global": {
      "enable": true,
      "cmp_auto": true,
      "min_interval": 30000
    },
    "spaces": [
      {
        "space": "ADMOB_Banner_Home",
        "adsType": "banner",
        "ids": ["ca-app-pub-3940256099942544/6300978111"],
        "enable": true,
        "minInterval": 30000
      },
      {
        "space": "ADMOB_Native_List",
        "adsType": "native",
        "ids": ["ca-app-pub-3940256099942544/2247696110"],
        "enable": true,
        "minInterval": 30000
      },
      {
        "space": "ADMOB_Interstitial_General",
        "adsType": "interstitial",
        "ids": ["ca-app-pub-3940256099942544/1033173712"],
        "enable": true,
        "minInterval": 30000
      },
      {
        "space": "ADMOB_Rewarded_Video",
        "adsType": "reward",
        "ids": ["ca-app-pub-3940256099942544/5224354917"],
        "enable": true,
        "minInterval": 30000
      }
    ]
  }
}
```

**Config Fields**:
- `space`: Unique identifier for ad placement
- `adsType`: Ad type (`banner`, `native`, `interstitial`, `reward`, `reward_inter`, `open_app`)
- `ids`: Waterfall ad unit IDs (tries in order until success)
- `enable`: Enable/disable this space
- `minInterval`: Minimum milliseconds between shows

## Ad Integration by Type

For detailed implementation of each ad type, see:

- **Banner Ads**: See [references/banner.md](references/banner.md) - XML layout, Collapsible banners, Adaptive banners
- **Native Ads**: See [references/native.md](references/native.md) - Custom layouts, Unified Native, Media content
- **Interstitial Ads**: See [references/interstitial.md](references/interstitial.md) - Full-screen ads, Preload patterns
- **Rewarded Ads**: See [references/rewarded.md](references/rewarded.md) - User rewards, Rewarded video
- **Rewarded Interstitial Ads**: See [references/rewarded-interstitial.md](references/rewarded-interstitial.md) - Full-screen rewarded
- **Open App Ads**: See [references/open-app.md](references/open-app.md) - App launch ads, Cold start

## Advanced Configuration

For advanced features, see:

- **CMP Consent Management**: See [references/cmp.md](references/cmp.md) - GDPR/UMP consent flow, Loading dialog, Privacy options
- **Firebase Remote Config**: See [references/remote-config.md](references/remote-config.md) - Remote configuration override, A/B testing
- **App Resume Ads**: See [references/resume-ads.md](references/resume-ads.md) - Open app ads on resume, Interstitial resume
- **Event Handling**: See [references/events.md](references/events.md) - Global event bus subscription, Ad revenue tracking

## Additional Guides

- **Testing Guide**: See [references/testing.md](references/testing.md) - Unit tests, Instrumented tests, Test devices
- **Troubleshooting**: See [references/troubleshooting.md](references/troubleshooting.md) - Common issues, Debug techniques, Error codes
- **Analytics**: See [references/analytics.md](references/analytics.md) - Ad revenue tracking, Event analytics, Third-party analytics
- **Performance**: See [references/performance.md](references/performance.md) - Ad loading optimization, Memory management, Caching strategies
- **Production Checklist**: See [references/production-checklist.md](references/production-checklist.md) - Pre-release checklist, Policy compliance, Monitoring

## Migration Guide

Upgrading from AdSpaceSDK v1.x to v2.0? See [references/migration.md](references/migration.md) for:

- Breaking changes
- API modifications
- Configuration updates
- Code migration examples
- Testing your migration

## Critical Rules

1. **Package Name**: Always import from `com.admob.adspace.*`, not `io.github.maichanchinh.*`
2. **Thread Safety**: All Space classes are thread-safe
3. **Memory Management**: Clear cache on Activity destroy
4. **Premium Check**: Check user premium status before showing ads
5. **Min Interval**: SDK enforces minimum interval between shows
6. **CMP Gate**: Ads blocked until consent obtained (if required)
7. **Waterfall Strategy**: SDK tries ad unit IDs in order automatically
8. **Application Context**: Always use Application context for SDK initialization
9. **Test Devices**: Use test device IDs during development to avoid policy violations
10. **Consent Flow**: Never request ads before CMP consent flow completes (if required)

## Common Patterns

### Ad Readiness Check

```kotlin
// Check if ad is ready to show
if (SpaceInterstitial.isLoaded("ADMOB_Interstitial_General")) {
    SpaceInterstitial.show(activity, "ADMOB_Interstitial_General", callback)
} else {
    // Preload for next time
    SpaceInterstitial.preload("ADMOB_Interstitial_General", preloadCallback)
}
```

### Preload Strategy

```kotlin
// Preload multiple ads at app startup
class MyApplication : Application() {
    override fun onCreate() {
        super.onCreate()

        // After SDK initialization
        AdSpaceSDK.initialize(this, config)

        // Preload interstitials and rewarded ads
        SpaceInterstitial.preload("ADMOB_Interstitial_General", null)
        SpaceRewarded.preload("ADMOB_Rewarded_Video", null)
    }
}
```

### Cache Management

```kotlin
class MainActivity : AppCompatActivity() {
    override fun onDestroy() {
        super.onDestroy()

        // Clear cache for specific space
        SpaceBanner.clearCache("ADMOB_Banner_Home")

        // Or clear all banner cache
        SpaceBanner.clearAllCache()

        // Also available for other ad types
        SpaceNative.clearCache("ADMOB_Native_List")
        SpaceInterstitial.clearCache("ADMOB_Interstitial_General")
    }
}
```

### Global Ad Type Control

```kotlin
// Disable all banner ads globally
AdSpaceSDK.setAdTypeEnabled(AdsType.BANNER, false)

// Enable all interstitial ads globally
AdSpaceSDK.setAdTypeEnabled(AdsType.INTERSTITIAL, true)

// Check if ad type is enabled
if (AdSpaceSDK.isAdTypeEnabled(AdsType.REWARDED)) {
    // Rewarded ads are enabled
}
```

### Premium User Handling

```kotlin
class UserManager {
    fun isUserPremium(): Boolean {
        // Your premium check logic
        return UserRepository.isUserPremium()
    }
}

// Before showing any ad
if (!UserManager().isUserPremium()) {
    SpaceInterstitial.show(activity, "ADMOB_Interstitial_General", callback)
} else {
    // Skip ads for premium users
    continueFlow()
}
```

### Retry Pattern with Backoff

```kotlin
class AdManager {
    private var retryCount = 0
    private val maxRetries = 3

    fun showInterstitialWithRetry(activity: Activity) {
        SpaceInterstitial.show(
            activity = activity,
            spaceName = "ADMOB_Interstitial_General",
            callback = object : InterstitialCallback {
                override fun onAdFailed(error: InterstitialError) {
                    if (retryCount < maxRetries) {
                        retryCount++
                        // Exponential backoff: 1s, 2s, 4s
                        Handler(Looper.getMainLooper()).postDelayed({
                            preloadAndShow()
                        }, (2.0.pow(retryCount) * 1000).toLong())
                    } else {
                        // Give up and continue
                        retryCount = 0
                        continueFlow()
                    }
                }

                override fun onAdDismissed() {
                    retryCount = 0
                    continueFlow()
                }
            }
        )
    }

    private fun preloadAndShow() {
        SpaceInterstitial.preload(
            spaceName = "ADMOB_Interstitial_General",
            callback = object : InterstitialCallback {
                override fun onAdLoaded() {
                    // Try showing again
                    showInterstitialWithRetry(activity)
                }

                override fun onAdFailed(error: InterstitialError) {
                    // Preload failed, don't retry
                    continueFlow()
                }
            }
        )
    }
}
```

### Sequential Ad Shows

```kotlin
class GameFlowManager {
    fun onLevelComplete(activity: Activity) {
        // Show interstitial, then rewarded
        SpaceInterstitial.show(
            activity = activity,
            spaceName = "ADMOB_Interstitial_General",
            callback = object : InterstitialCallback {
                override fun onAdDismissed() {
                    // Interstitial closed, now offer rewarded
                    showRewardedAd(activity)
                }

                override fun onAdFailed(error: InterstitialError) {
                    // No interstitial, skip to rewarded
                    showRewardedAd(activity)
                }
            }
        )
    }

    private fun showRewardedAd(activity: Activity) {
        SpaceRewarded.show(
            activity = activity,
            spaceName = "ADMOB_Rewarded_Video",
            callback = object : RewardedCallback {
                override fun onUserEarnedReward() {
                    // User watched full ad, give reward
                    grantBonusReward()
                }

                override fun onAdDismissed() {
                    // Continue game flow
                    continueToNextLevel()
                }
            }
        )
    }
}
```

## Additional Public Methods

Besides the core initialization and ad-related methods, AdSpaceSDK provides these utility methods:

### Consent Management

```kotlin
// Manually request consent (for manual consent mode)
AdSpaceSDK.requestConsent(activity)

// Set callback when consent flow completes (auto or manual)
AdSpaceSDK.setConsentFlowCompletedCallback { canRequestAds ->
    if (canRequestAds) {
        // User consented - safe to request ads
        startLoadingAds()
    } else {
        // User denied consent - ads blocked
        handleNoConsent()
    }
}

// IMPORTANT: Always remove callback to prevent memory leaks
AdSpaceSDK.setConsentFlowCompletedCallback(null)
```

### Resume Ads Control

```kotlin
// Skip next resume ad show (both Open Resume and Interstitial Resume)
AdSpaceSDK.skipNextShow()

// Check if activity should ignore resume ads
val shouldIgnore = AdSpaceSDK.shouldIgnoreAdResume(activity)

// Set activity to ignore resume ads
AdSpaceSDK.setIgnoreAdResume(MainActivity::class.java)

// Set resume mode (NONE, OPEN_ADS, INTERSTITIAL)
AdSpaceSDK.setResumeMode(ResumeMode.OPEN_ADS, "ADMOB_OpenApp_Launch")
```

### Testing & Debugging

```kotlin
// Get list of test device IDs
val testDevices = AdSpaceSDK.getTestDevices()

// Get current activity reference (for lifecycle management)
val currentActivity = AdSpaceSDK.getCurrentActivity()

// Get current activity class name
val activityName = AdSpaceSDK.getCurrentActivityClassName()
```

## Quick Troubleshooting Checklist

When ads aren't working, follow these 5 steps to debug quickly:

### 1. Verify SDK Initialization

```kotlin
// Check if SDK is initialized
Log.d("AdCheck", "SDK initialized: ${AdSpaceSDK.isInitialized()}")
```

**What to check:**
- [ ] `AdSpaceSDK.initialize()` called in `Application.onCreate()`
- [ ] Application class registered in `AndroidManifest.xml`
- [ ] AdMob App ID correct in manifest
- [ ] Logcat shows "AdSpaceSDK initialized successfully"

### 2. Validate Configuration

```kotlin
// Check config is loaded
val config = AdSpaceSDK.getConfig()
Log.d("AdCheck", "Global enabled: ${config?.global?.enable}")
Log.d("AdCheck", "CMP auto: ${config?.global?.cmp_auto}")
```

**What to check:**
- [ ] `ads_config.json` exists in `assets/` folder
- [ ] JSON is valid (no syntax errors)
- [ ] Space name matches exactly (case-sensitive)
- [ ] Ad type is correct (`banner`, `interstitial`, etc.)
- [ ] Ad unit IDs are correct (test vs production)

### 3. Check Consent Status

```kotlin
// Check if consent obtained
AdSpaceSDK.setConsentFlowCompletedCallback { canRequestAds ->
    Log.d("AdCheck", "Can request ads: $canRequestAds")
}
```

**What to check:**
- [ ] CMP consent flow completed
- [ ] User didn't deny all consent
- [ ] `ads.global.cmp_auto` is `true` for auto consent
- [ ] Logcat shows "CMP consent obtained" or similar

### 4. Verify Ad Readiness

```kotlin
// Check if ad is loaded
val isLoaded = SpaceInterstitial.isLoaded("ADMOB_Interstitial_General")
Log.d("AdCheck", "Ad loaded: $isLoaded")
```

**What to check:**
- [ ] Ad preloading completed successfully
- [ ] `isLoaded()` returns `true`
- [ ] Min interval has elapsed (check `min_interval` config)
- [ ] Space is enabled in config (`enable: true`)
- [ ] No errors in callback (check `onAdFailed`)

### 5. Check Environment & Policies

```bash
# Check test device ID in Logcat
adb logcat | grep "AdSpaceSDK"
```

**What to check:**
- [ ] Using test ad units during development
- [ ] Test device ID configured (if needed)
- [ ] Debug mode enabled (`debug: true` in config)
- [ ] No ad blocking VPN enabled
- [ ] Google Play Services installed and updated
- [ ] Network connection available
- [ ] Device not rooted (for testing)

### Common Error Messages

| Error | Cause | Solution |
|-------|-------|----------|
| "Internal error" | Invalid ad unit ID | Check ad unit ID in config |
| "No fill" | No ad available | Try again later, check mediation settings |
| "Timeout" | Network too slow | Increase timeout, check connection |
| "Not ready" | Ad not loaded | Call `preload()` before `show()` |
| "Consent not obtained" | CMP not completed | Wait for consent flow |

## Production Readiness Checklist

Before releasing your app to production, complete this checklist:

### Configuration

- [ ] **Replace Test Ad Units**: All test ad unit IDs replaced with production IDs
- [ ] **AdMob App ID**: Production App ID in `AndroidManifest.xml`
- [ ] **Config File**: `ads_config.json` has production ad unit IDs
- [ ] **Debug Mode**: `debug = false` in `AdSpaceSDKConfig` for release builds
- [ ] **Test Devices**: Empty or removed from production config
- [ ] **Min Interval**: Appropriate min interval set (recommend 30-60 seconds)

### Consent & Privacy

- [ ] **CMP Config**: `cmp_auto: true` for GDPR compliance
- [ ] **Privacy Policy**: App privacy policy URL configured in AdMob console
- [ ] **Consent Flow**: Tested consent flow on EU devices
- [ ] **Child-Directed**: Set appropriate treatment for child-directed apps
- [ ] **Privacy Options**: Privacy options button accessible (if required)

### Testing

- [ ] **Device Testing**: Tested on multiple Android versions (26+)
- [ ] **Ad Types**: All ad types tested (Banner, Native, Interstitial, etc.)
- [ ] **CMP Flow**: Consent flow tested with different user choices
- [ ] **Premium Users**: Verified ads don't show for premium users
- [ ] **Network Conditions**: Tested on slow networks (3G, 4G, WiFi)
- [ ] **Orientation**: Tested both portrait and landscape
- [ ] **Tablet**: Tested on tablet screen sizes

### Code Quality

- [ ] **Memory Leaks**: Cache cleared in `onDestroy()` for all Activities
- [ ] **Callbacks Removed**: All callbacks removed in `onDestroy()`
- [ ] **Weak References**: Used WeakReference for Activity contexts
- [ ] **Error Handling**: All callbacks implement error handling
- [ ] **Thread Safety**: Ad operations on main thread where required

### AdMob Console

- [ ] **App Created**: App created in AdMob console
- [ ] **Ad Units Created**: All ad units created (Banner, Interstitial, etc.)
- [ ] **Mediation**: Mediation partners configured (if using)
- [ ] **Blocking Controls**: Ad categories blocked appropriately
- [ ] **Ad Review**: Ad creatives reviewed and allowed
- [ ] **Payments**: Payment information complete

### Policy Compliance

- [ ] **Ad Placement**: Ads don't interfere with app functionality
- [ ] **Content Policy**: App content complies with AdMob policies
- [ ] **Ad Density**: Ad density follows platform guidelines
- [ ] **Native Ads**: Native ads clearly labeled as "Advertisement"
- [ ] **Interstitial Timing**: Interstitials not shown too frequently

### Release Preparation

- [ ] **Build Variants**: Release build tested (`./gradlew assembleRelease`)
- [ ] **Proguard/R8**: Proguard rules configured (if using code obfuscation)
- [ ] **Version Bump**: App version incremented
- [ ] **Release Notes**: Release notes prepared
- [ ] **Screenshots**: App screenshots prepared for store listing

### Post-Launch

- [ ] **Monitoring**: Ad revenue and fill rate monitored for first week
- [ ] **Alerts**: Alerts set up for low fill rate or high error rate
- [ ] **Remote Config**: Remote Config ready for emergency kill switch
- [ ] **Rollback Plan**: Plan ready if critical issues discovered
- [ ] **User Feedback**: Mechanism to report ad issues

### Final Checks

- [ ] **Documentation**: Team documentation updated
- [ ] **Code Review**: Code reviewed by another developer
- [ ] **QA Approval**: QA team approved the release
- [ ] **Stakeholder Sign-off**: Product/business stakeholders notified

## Troubleshooting

**Ads not showing?**

Quick checklist:
1. Check `ads.global.enable` is `true` in config
2. Check space-specific `enable` is `true`
3. Verify AdMob App ID in manifest
4. Check min interval hasn't blocked the ad
5. Verify CMP consent obtained (if required)
6. Check user premium status

**Memory leaks?**
1. Always clear cache in `onDestroy()`
2. Use `WeakReference` for Activity contexts
3. Don't hold references to AdView/NativeAdView
4. Remove all callbacks in `onDestroy()`
5. Check for leaks using LeakCanary

**Wrong package imports?**
1. Use `com.admob.adspace.*` not `io.github.maichanchinh.*`
2. Check import statements match examples above
3. Verify dependency version is correct

**Low fill rate?**
1. Check ad unit IDs are correct
2. Verify mediation settings in AdMob console
3. Increase eCPM floor settings
4. Add more ad networks to mediation
5. Check geographic targeting

**CMP consent issues?**
1. Test on EU device or VPN to EU
2. Check `ads.global.cmp_auto` is `true`
3. Verify UMP SDK integrated correctly
4. Check consent form configuration in AdMob console
5. See [references/cmp.md](references/cmp.md) for details
