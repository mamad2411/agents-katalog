---
name: "integrating-google-ads"
description: "Integrates Google Mobile Ads (AdMob) into Flutter using google_mobile_ads v7.x with Banner, Interstitial, Rewarded, and Native ad formats. Use this skill whenever implementing app monetization, adding AdMob ads to Flutter, fixing ad loading or display errors, managing ad lifecycle (preload/dispose), preventing memory leaks from undisposed ads, handling GDPR/ATT consent flows, troubleshooting AdMob dashboard integration, or any time the words 'AdMob', 'google_mobile_ads', 'banner ad', 'interstitial', 'rewarded ad', 'native ad', or 'ad monetization' appear in the request. Supports Android (GMA SDK 24.9+) and iOS (GMA SDK 12.14+)."
metadata:
  last_modified: "2026-04-01 14:35:00 (GMT+8)"
---

# Flutter Ads Implementation (`google_mobile_ads` v7.x)

## Goal
> Verified against `google_mobile_ads` 9.2.0 (requires Flutter 3.38.1+). The `InterstitialAd.load` and `RewardedAd.load` callback signatures below match this version.

Integrate Google Mobile Ads securely and efficiently. Prevent memory leaks by strictly managing `AdWidget` lifecycles and ensure high fill-rates by pre-loading full-screen ads before they are needed.

## Instructions

### 1. Core Native Initialization
Before calling any Dart code, the native manifests must be explicitly configured with the Google Mobile Ads application ID.

**Android (`android/app/src/main/AndroidManifest.xml`)**
Add the `<meta-data>` tag immediately inside the `<application>` tag.
```xml
<manifest>
    <application>
        <!-- Use TEST ID for development: ca-app-pub-3940256099942544~3347511713 -->
        <meta-data
            android:name="com.google.android.gms.ads.APPLICATION_ID"
            android:value="YOUR_ANDROID_APP_ID"/>
    </application>
</manifest>
```

**iOS (`ios/Runner/Info.plist`)**
Add `GADApplicationIdentifier`.
```xml
<key>GADApplicationIdentifier</key>
<!-- Use TEST ID for development: ca-app-pub-3940256099942544~1458002511 -->
<string>YOUR_IOS_APP_ID</string>
```

**Flutter (`main.dart`)**
Initialize the SDK eagerly before `runApp`.
```dart
void main() async {
  WidgetsFlutterBinding.ensureInitialized();
  await MobileAds.instance.initialize();
  runApp(const MyApp());
}
```

---

### 2. Test Ad Unit IDs (CRITICAL)
Always use Google's predefined test ad units during development and testing. Using your own live production IDs on test devices will lead to immediate AdSense account suspension.

**Android Test IDs:**
*   Banner: `ca-app-pub-3940256099942544/6300978111`
*   Interstitial: `ca-app-pub-3940256099942544/1033173712`
*   Rewarded: `ca-app-pub-3940256099942544/5224354917`
*   Native Advanced: `ca-app-pub-3940256099942544/2247696110`

**iOS Test IDs:**
*   Banner: `ca-app-pub-3940256099942544/2934735716`
*   Interstitial: `ca-app-pub-3940256099942544/4411468910`
*   Rewarded: `ca-app-pub-3940256099942544/1712485313`
*   Native Advanced: `ca-app-pub-3940256099942544/3986624511`

---

### 3. Banner Ads (Inline Constrained Widgets)
Banner ads are rendered organically within the Flutter widget tree using an `AdWidget`. 

**Implementation Pattern:**
1. Maintain the `BannerAd` instance in the `State`.
2. Load it during `initState`.
3. Track an `_isLoaded` flag to render the `AdWidget` only when ready.
4. **CRITICAL:** Call `.dispose()` in `dispose`.

```dart
class BannerAdWidget extends StatefulWidget {
  @override
  _BannerAdWidgetState createState() => _BannerAdWidgetState();
}

class _BannerAdWidgetState extends State<BannerAdWidget> {
  BannerAd? _bannerAd;
  bool _isLoaded = false;

  final String adUnitId = Platform.isAndroid
      ? 'ca-app-pub-3940256099942544/6300978111'
      : 'ca-app-pub-3940256099942544/2934735716';

  @override
  void initState() {
    super.initState();
    _loadAd();
  }

  void _loadAd() {
    _bannerAd = BannerAd(
      adUnitId: adUnitId,
      request: const AdRequest(),
      size: AdSize.banner, // e.g. 320x50
      listener: BannerAdListener(
        onAdLoaded: (ad) => setState(() => _isLoaded = true),
        onAdFailedToLoad: (ad, err) {
          ad.dispose(); // CRITICAL
        },
      ),
    )..load();
  }

  @override
  void dispose() {
    _bannerAd?.dispose(); // CRITICAL
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    if (_bannerAd != null && _isLoaded) {
      return SafeArea(
        child: SizedBox(
          width: _bannerAd!.size.width.toDouble(),
          height: _bannerAd!.size.height.toDouble(),
          child: AdWidget(ad: _bannerAd!),
        ),
      );
    }
    return const SizedBox.shrink();
  }
}
```

---

### 4. Interstitial Ads (Full-Screen Transitions)
Interstitials are full-screen overlays. They **MUST** be pre-loaded before the user triggers the logic that displays them. 

**Implementation Pattern:**
```dart
class InterstitialManager {
  InterstitialAd? _interstitialAd;

  // Utilize the test IDs defined above during development
  final String adUnitId = Platform.isAndroid
      ? 'ca-app-pub-3940256099942544/1033173712'
      : 'ca-app-pub-3940256099942544/4411468910';

  /// Call this when the user ENTERS the screen/level.
  void loadAd() {
    InterstitialAd.load(
      adUnitId: adUnitId,
      request: const AdRequest(),
      adLoadCallback: InterstitialAdLoadCallback(
        onAdLoaded: (ad) {
          ad.fullScreenContentCallback = FullScreenContentCallback(
            onAdDismissedFullScreenContent: (ad) {
              ad.dispose(); // CRITICAL
              loadAd(); // Pre-load the next one immediately
            },
            onAdFailedToShowFullScreenContent: (ad, error) {
              ad.dispose(); // CRITICAL
            },
          );
          _interstitialAd = ad;
        },
        onAdFailedToLoad: (err) => print('Failed to load: $err'),
      ),
    );
  }

  /// Call this when the user leaves the screen/finishes a level.
  void showAd(VoidCallback onDone) {
    if (_interstitialAd != null) {
      // Define a one-time wrapper if you need logic strictly after dismissal
      _interstitialAd!.fullScreenContentCallback?.onAdDismissedFullScreenContent = (ad) {
        ad.dispose();
        loadAd();
        onDone(); // Resume app logic
      };
      _interstitialAd!.show();
      _interstitialAd = null; // Prevent showing twice
    } else {
      onDone(); // Fallback if ad wasn't loaded
    }
  }
}
```

---

### 5. Rewarded Ads (Value-Exchange)
Used for giving users points/lives in exchange for watching a video. Similar lifecycle to Interstitials but requires secure reward handling.

**Implementation Pattern:**
```dart
RewardedAd? _rewardedAd;

void _loadRewardedAd() {
  RewardedAd.load(
    adUnitId: Platform.isAndroid 
        ? 'ca-app-pub-3940256099942544/5224354917' 
        : 'ca-app-pub-3940256099942544/1712485313',
    request: const AdRequest(),
    rewardedAdLoadCallback: RewardedAdLoadCallback(
      onAdLoaded: (ad) {
        ad.fullScreenContentCallback = FullScreenContentCallback(
          onAdDismissedFullScreenContent: (ad) {
            ad.dispose();
            _loadRewardedAd(); // Reload
          },
        );
        _rewardedAd = ad;
      },
      onAdFailedToLoad: (err) {},
    ),
  );
}

void _showRewardedAd() {
  if (_rewardedAd != null) {
    _rewardedAd!.show(
      // CRITICAL: Handle the reward logic here
      onUserEarnedReward: (AdWithoutView ad, RewardItem reward) {
        print('User earned: ${reward.amount} ${reward.type}');
        // Grant virtual currency
      },
    );
    _rewardedAd = null;
  }
}
```

---

### 6. Native Ads (Seamless Integration)
Native ads match the look and feel of your app. Google now provides `NativeTemplateStyle` to avoid writing complex custom Java/Swift factories unless absolutely necessary.

```dart
NativeAd? _nativeAd;
bool _nativeAdIsLoaded = false;

void _loadNativeAd() {
  _nativeAd = NativeAd(
    // Utilize the test IDs defined above during development
    adUnitId: Platform.isAndroid 
        ? 'ca-app-pub-3940256099942544/2247696110' 
        : 'ca-app-pub-3940256099942544/3986624511',
    request: const AdRequest(),
    // Use predefined templates for zero native code
    nativeTemplateStyle: NativeTemplateStyle(
      templateType: TemplateType.medium,
      mainBackgroundColor: Colors.white,
      cornerRadius: 10.0,
      callToActionTextStyle: NativeTemplateTextStyle(
        textColor: Colors.white,
        backgroundColor: Colors.blue,
        style: NativeTemplateFontStyle.bold,
        size: 16.0,
      ),
    ),
    listener: NativeAdListener(
      onAdLoaded: (ad) => setState(() => _nativeAdIsLoaded = true),
      onAdFailedToLoad: (ad, error) {
        ad.dispose();
      },
    ),
  )..load();
}

// In build method:
if (_nativeAdIsLoaded && _nativeAd != null)
  ConstrainedBox(
    constraints: const BoxConstraints(
      minWidth: 320, // minimum recommended width
      minHeight: 320, // minimum recommended height
      maxWidth: 400,
      maxHeight: 400,
    ),
    child: AdWidget(ad: _nativeAd!),
  )
```

## Constraints
*   **Memory Leaks:** Always call `.dispose()` on any ad instance inside `onAdFailedToLoad`, `onAdDismissedFullScreenContent`, or the parent StatefulWidget's `dispose()` method. Failure to do so degrades app performance significantly.
*   **Initialization Timing:** Never attempt to call `Ad.load()` prior to awaiting `MobileAds.instance.initialize()`.
*   **Test Ad Units:** Always use the predefined Google Test Ad Unit IDs while in development. Using live production IDs against test devices leads directly to AdSense account suspension.
