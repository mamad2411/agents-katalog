---
name: store-compliance-scan
description: Probe a mobile app's shipped config against the dated App Store and Google Play gates — privacy manifest, purpose strings, ATT, account deletion, login 4.8, target SDK, 16 KB pages, data declarations, IAP — as release blockers.
kind: skill
pack: mobile
allowed-tools: [Read, Grep, Glob, Bash]
---

# Skill: store-compliance-scan

## Premise

A store gate does not care what the source says. App Store Connect reads the built app's Info.plist, its privacy manifests and the SDK that built it; Play reads the merged manifest, the target API and the native libraries' alignment. Libraries inject permissions the source manifest never names, `flutter.targetSdkVersion` resolves only at build time, and an Expo app's native folders are generated. Every class here is a gap between a dated store requirement and what the **shipped** configuration declares.

**Store gates are a release-blocker axis, never a security severity.** Each row carries one value: **HARD-BLOCK** (the upload or update is refused by a machine), **REJECTION** (a human applies a cited guideline), **PENALTY** (visibility or publishing limits after release), **SCHEDULE** (dated, not in force yet: report the days remaining), **VERIFY** (judgement the guideline leaves open). These are `@app-store-reviewer`'s three buckets plus two. A store row never becomes "critical", and a security finding never borrows a store date.

**Every finding cites the config `<file:line>` (merged or built when available) + the gate row (§ The dated store gates) with its date and days remaining + the axis + the probe that settles it.** The probe tier is **A** (the shipped artifact) for declarations and **D** for flows (deletion, the ATT prompt, restore) — [`precedents/mobile.md`](../../../../snippets/precedents/mobile.md) § The claim, restated. **No artifact, no Xcode or no emulator means `SKIPPED`, never PASS**; a candidate below its tier is **Unconfirmed** with the probe written out ([`refute-before-report.md`](../../../../snippets/refute-before-report.md) § 2, gate 6). `@app-store-reviewer` (this pack) is the judge: it quotes the live policy and decides the bucket.

## The dated store gates

This table is the pack's single copy of the store dates. Other mobile files point here instead of repeating a date. Every row was read on its primary page on **2026-10-05**; quote it as "per the page as of 2026-10-05". **Re-read a row's page before reporting it once the run's date is 90 days past that.**

| # | Store | Gate | In force | Axis | § | Primary page (page date) |
|---|---|---|---|---|---|---|
| G1 | Play | New apps and updates target API 36 (Wear OS, Automotive 35; TV, XR 34); existing apps below 35 stop reaching new users on newer Android | 2026-08-31; extension on request to **2026-11-01** | HARD-BLOCK | 6 | developer.android.com/google/play/requirements/target-sdk (2026-10-01) |
| G2 | Apple | Uploads built with Xcode 26+ and an iOS / iPadOS 26 SDK | 2026-04-28 | HARD-BLOCK | 6 | developer.apple.com/news/upcoming-requirements |
| G3 | Apple | Uploads target iOS / iPadOS 13 or later | 2026-09-09 | HARD-BLOCK | 6 | same |
| G4 | Apple | Approved reasons for required-reason APIs used by the app or its SDKs, in a privacy manifest | 2024-05-01 | HARD-BLOCK | 1 | same; developer.apple.com/documentation/bundleresources/describing-use-of-required-reason-api |
| G5 | Apple | SDKs on Apple's commonly-used list ship their own privacy manifest, and a signature when binary | new apps, and updates that add the SDK | REJECTION | 1 | developer.apple.com/support/third-party-SDK-requirements |
| G6 | Apple | Updated age-rating answers (App Store Connect; not in the repo — ledger only) | 2026-01-31 | HARD-BLOCK | — | developer.apple.com/news/upcoming-requirements |
| G7 | Apple | In-app account deletion where accounts can be created (the whole record; Sign in with Apple tokens revoked through the REST API) | 2022-06-30 | REJECTION (5.1.1(v)) | 4 | developer.apple.com/support/offering-account-deletion-in-your-app |
| G8 | Play | In-app deletion path **and** a working web deletion link in Data safety | enforcement after 2024-05-31 | REJECTION | 4 | support.google.com/googleplay/android-developer/answer/13327111 |
| G9 | Apple | Purpose strings that clearly and completely describe the use (5.1.1); tracking only after ATT consent, never a condition for features (5.1.2(i)); an *equivalent* login beside a primary third-party login (4.8); IAP for digital unlocks, US storefront may link out (3.1.1) | in force | REJECTION · VERIFY for 4.8 and 3.1.1 | 2, 3, 5, 9 | developer.apple.com/app-store/review/guidelines (no page date shown) |
| G10 | Play | Data safety form for every app (also apps collecting nothing), a privacy policy, SDK practices included; misrepresentation → blocked updates or removal | in force | REJECTION | 8 | support.google.com/googleplay/android-developer/answer/10787469 |
| G11 | Play | `READ_MEDIA_IMAGES` / `READ_MEDIA_VIDEO` only for core broad access, with a declaration; otherwise the Photo Picker | full compliance 2025-05-28 | REJECTION | 2 | support.google.com/googleplay/android-developer/answer/14115180 |
| G12 | Play | `AD_ID` declared by apps targeting 13+ that use the advertising ID (SDKs may merge it in) | enforcement from 2022-04-01 (page) | VERIFY | 3 | support.google.com/googleplay/android-developer/answer/6048248 |
| G13 | Play | `QUERY_ALL_PACKAGES` only for core broad visibility (device search, antivirus, file managers, browsers), with the Permissions Declaration Form; otherwise removal | in force (no date on the page) | REJECTION | 2 | support.google.com/googleplay/android-developer/answer/10158779 |
| G14 | Play | Each foreground-service type an app targeting 14+ uses is declared in Play Console (App content): the feature, the impact of deferral, a video | in force since late 2023 | REJECTION | 2 | support.google.com/googleplay/android-developer/answer/13392821 |
| G15 | Play | Play Billing Library **8+** for new apps and updates (7 retired) | 2026-08-31; extension to **2026-11-01** | HARD-BLOCK | 9 | developer.android.com/google/play/billing/deprecation-faq (2026-09-09) |
| G16 | Play | 16 KB page support for apps targeting 35+ on 64-bit; updates without it cannot be released | **2027-02-01** | SCHEDULE → HARD-BLOCK | 7 | developer.android.com/guide/practices/page-sizes (2026-09-16) |
| G17 | Play | Bad-behaviour thresholds for memory (anonymous RSS + swap), bitmap memory and DEX optimization (≥ 25 % coverage, R8 or equivalent) | February 2027 | SCHEDULE → PENALTY | routed | Android Developers blog, 2026-08-26 |
| G18 | Play | Apps with sign-in restore it on a new device (Restore Credentials API) | April 2027 | SCHEDULE → PENALTY | 4 | same post |

The research catalog also records Android developer verification for sideloaded apps in BR / ID / SG / TH from 2026-09-30 (a distribution gate, not a Play one) — **not re-read today**: report it as VERIFY until a run re-reads its page. Every row here is a summary in our words; quote the live page, never this table, in a store finding.

## The rule

A candidate is a finding when all five hold:

1. **It ships to that store.** The root builds for the platform (an `ios/` folder, an Xcode project, an Expo app, an Android module) and the configuration is the release one — not a Debug entitlements file, a `src/debug` manifest, a test target.
2. **The effective config agrees.** The merged manifest, the Expo prebuild output, the built app's Info.plist, `INFOPLIST_KEY_*` build settings — not only the source. A library-injected permission is real; one removed with `tools:node="remove"` is not ([`precedents/mobile.md`](../../../../snippets/precedents/mobile.md) § 25).
3. **The gate applies on the run's date.** Read the row's date against today (the script prints it): in force is the row's axis; in force with an extension still open is that axis "unless the extension was granted" plus the days to it; not yet in force is SCHEDULE with the days remaining.
4. **Nothing exempts it.** A gate's own exceptions (Wear OS at 35, the 4.8 own-account exception, 3.1.5 physical goods, alarm-clock exact alarms — precedents § 18, § 49).
5. **The probe on the shipped artifact** (A) or the flow on a device (D) confirms it — or the row stays Unconfirmed with the probe written out.

## Boundaries

- A **missing** purpose string for an API in use crashes at first access → `mobile-lifecycle-scan` § 3 (this pack); here it is the store row. A foreground service without a type crashes → lifecycle § 2; § 2d here lists the types to declare in Play Console. Both runs dedupe by `<file:line>`.
- Token storage, cleartext, exported components, debuggable or debug-signed release builds → `mobile-security-scan` when the security pack is installed; without it, reported under [`precedents/mobile.md`](../../../../snippets/precedents/mobile.md) § 8.
- Purpose-string **wording**, metadata, screenshots, review notes → `@app-store-reviewer` (precedents § 6). This skill flags only blank, placeholder and unused strings.
- Vitals (crash, ANR, wake locks, memory, bitmap) are measured by `mobile-perf-scan` and `@device-performance-auditor`; the store consequence of G17 is `@app-store-reviewer`'s. App size is `app-size-scan`.
- OTA configuration → `mobile-lifecycle-scan` § 7; what an update may change (2.5.2) → `@app-store-reviewer`.
- Durability of an acknowledged write → `offline-sync-scan`. Account deletion is here; what logout leaves behind is there.

## Adapt to the codebase — lanes

| Lane | Declarations live in | Effective config to read | Lint lane (project config, keep only the rule) |
|---|---|---|---|
| **Expo (CNG)** | `app.json` / `app.config.*`: `ios.infoPlist`, `ios.privacyManifests`, `android.permissions` / `blockedPermissions`, the `expo-build-properties` plugin | the prebuild output, then the build artifact; Expo's privacy guide says Apple does not reliably read CocoaPods manifests, so declare in `ios.privacyManifests` (docs.expo.dev, read 2026-10-05) | — |
| **React Native (bare)** | `ios/<App>/Info.plist`, `PrivacyInfo.xcprivacy`, `android/app/src/main/AndroidManifest.xml`, `android/build.gradle` `ext` | `android/app/build/intermediates/merged_manifests/release/…`; the archive | Android lint below |
| **Flutter** | `ios/Runner/Info.plist`, `ios/Runner/PrivacyInfo.xcprivacy`, `android/app/build.gradle(.kts)` | `build/app/intermediates/merged_manifests/release/…` — the only place `flutter.targetSdkVersion` is a number | Android lint below |
| **Android** | `src/main/AndroidManifest.xml`, `build.gradle(.kts)`, `settings.gradle(.kts)`, `gradle/libs.versions.toml` | `build/intermediates/merged_manifests/<variant>/…`, `aapt2 dump badging` | `./gradlew lintRelease`: `ExpiredTargetSdkVersion`, `ExpiringTargetSdkVersion`, `Aligned16KB`, `QueryAllPackagesPermission`, `PhotoAndVideoPolicy`, `ForegroundServicesPolicy`, `BackgroundLocationPolicy`, `PlaySdkIndexNonCompliant` |
| **iOS** | `Info.plist` or `INFOPLIST_KEY_*` (generated plist), `PrivacyInfo.xcprivacy`, `Podfile` / `Package.swift`, CI and Fastlane files | the built app's `Info.plist` (`DTXcode`, `DTSDKName`, `MinimumOSVersion`) [K]; Xcode Organizer's privacy report [K] | — |

## Pre-flight greps

Run as **one** script from the repo root. Grep **N** feeds detector **§N**; grep 0 is context. The root and exclusion block is `mobile-lifecycle-scan`'s, unchanged. Every `rg` names its path; the git-ignored merged manifest is named explicitly with `--no-ignore`. A line tagged `1a`–`9b` is a set-difference result; the rest are grep hits to read against the gate table. Any `rg` error on stderr is a failed grep, never zero hits.

```bash
# Mobile roots: RN/Expo package.json dirs, Flutter pubspec dirs, Android modules, Xcode project dirs; nested roots folded.
ROOTS=()
while IFS= read -r d; do ROOTS+=("$d"); done < <(
  { rg -l --pcre2 '"(?:react-native|expo)"\s*:' -g 'package.json' -g '!**/node_modules/**' .
    rg -l --pcre2 '^\s+sdk:\s*flutter\b' -g 'pubspec.yaml' -g '!**/.dart_tool/**' .
    rg --files -g '**/src/main/AndroidManifest.xml' -g '!**/{build,node_modules,.gradle}/**' . | sed 's#/src/main/AndroidManifest\.xml$#/x#'
    rg --files -g '**/*.xcodeproj/project.pbxproj' -g '!**/{Pods,node_modules,DerivedData}/**' . | sed 's#/[^/]*\.xcodeproj/project\.pbxproj$#/x#'
  } | while IFS= read -r f; do dirname "$f"; done | sort -u | awk 'p != "" && index($0, p "/") == 1 { next } { print; p = $0 }')
[ ${#ROOTS[@]} -gt 0 ] || { echo 'no mobile project marker: every class N/A (no mobile surface)'; exit 0; }
printf 'root %s\n' "${ROOTS[@]}"
# Never shipped in a release build: deps, build output, tests, debug source sets, generated code, docs.
X=(-g '!**/{node_modules,Pods,build,.gradle,.dart_tool,.expo,DerivedData,dist,vendor,.cxx}/**' -g '!**/src/{test,androidTest,debug}/**'
   -g '!**/{test,tests,__tests__,__mocks__,mocks,fixtures,__fixtures__,testdata,e2e,integration_test,.maestro,docs,ai}/**'
   -g '!**/*{Tests,UITests}/**' -g '!**/*.{test,spec,stories}.*' -g '!**/*_test.dart' -g '!**/*.{g,freezed,mocks}.dart' -g '!**/app_localizations*.dart' -g '!**/*.{md,mdx,lock,snap,map}')
NC=(rg -v --pcre2 '^[^:]+:\d+:\s*(//|/\*|\*(\s|/|$)|#(?!\{)|<!--)')
JS=(-g '*.{js,jsx,ts,tsx}'); KT=(-g '*.{kt,java}'); DA=(-g '*.dart'); SW=(-g '*.swift'); MF=(-g 'AndroidManifest.xml')
SRC=(-g '*.{js,jsx,ts,tsx,kt,java,dart,swift,m,mm}'); NAT=(-g '*.{swift,m,mm}'); CFG=(-g 'package.json' -g 'pubspec.yaml' -g '*.{gradle,kts,toml}' -g '{Podfile,Package.swift}')
IROOTS=(); AROOTS=(); for r in "${ROOTS[@]}"; do E=0; rg -q --pcre2 '"expo"\s*:' -g 'package.json' "$r" && E=1
  { [ $E = 1 ] || [ -d "$r/ios" ] || rg --files -g '**/*.xcodeproj/project.pbxproj' "$r" | rg -q .; } && IROOTS+=("$r")
  { [ $E = 1 ] || [ -d "$r/android" ] || rg --files -g '**/src/main/AndroidManifest.xml' "$r" | rg -q .; } && AROOTS+=("$r"); done
printf 'today %s · ios: %s · android: %s\n' "$(date +%F)" "${IROOTS[*]:-none}" "${AROOTS[*]:-none}"
# The app's merged manifest (release variant, one ABI copy) is git-ignored build output: name it explicitly. None → every
# manifest row is source-only (tier A unreached).
MM=(); while IFS= read -r f; do MM+=("$f"); done < <(rg --files --no-ignore -g '**/intermediates/merged_manifests/**/AndroidManifest.xml' "${ROOTS[@]}" | rg --pcre2 '/release/' | awk -F/intermediates/ '!seen[$1]++')
printf 'merged %s\n' "${MM[@]:-none (source manifests only)}"
AM=("${MM[@]}"); [ ${#MM[@]} -gt 0 ] || while IFS= read -r f; do AM+=("$f"); done < <(rg --files -g '**/src/main/AndroidManifest.xml' "${X[@]}" "${ROOTS[@]}")

# 0. Versions the gates key on (the Gradle project root may sit one level above an app module).
GROOTS=(); for r in "${ROOTS[@]}"; do if [ -f "${r%/*}/settings.gradle" ] || [ -f "${r%/*}/settings.gradle.kts" ]; then GROOTS+=("${r%/*}"); else GROOTS+=("$r"); fi; done
rg -n --pcre2 '"(?:expo|react-native|expo-build-properties|react-native-iap|expo-iap|react-native-purchases)"\s*:' -g 'package.json' "${X[@]}" "${ROOTS[@]}"
rg -n --pcre2 '^\s+(?:flutter|in_app_purchase\w*|purchases_flutter):\s*["^>=]*\d' -g 'pubspec.yaml' "${ROOTS[@]}"

# 1. Privacy manifest. 1a an iOS root that uses a required-reason API family and ships no manifest (nor Expo
#    ios.privacyManifests); 1b a family used in native code and absent from every manifest of the root; 1c SDKs on
#    Apple's list declared directly (read the locked version: it must ship its own signed manifest).
for r in "${IROOTS[@]}"; do PM=$(rg --files -g 'PrivacyInfo.xcprivacy' "${X[@]}" "$r"; rg -l 'privacyManifests' -g 'app.{json,config.js,config.ts}' "$r")
  while IFS='~' read -r cat api; do U=$(rg -l --pcre2 "$api" "${NAT[@]}" "${X[@]}" "$r" | head -3 | tr '\n' ' '); [ -n "$U" ] || continue
    if [ -z "$PM" ]; then echo "1a $r: no privacy manifest; $cat used in $U"
    else printf '%s\n' "$PM" | while IFS= read -r m; do rg -q "NSPrivacyAccessedAPICategory$cat" "$m" && echo ok; done | rg -q . || echo "1b $r: $cat used in $U, not declared in $(echo $PM | tr '\n' ' ')"; fi; done <<'MAP'
UserDefaults~\b(?:UserDefaults|NSUserDefaults)\b|@AppStorage\b
FileTimestamp~\.(?:creationDate|modificationDate|fileModificationDate|contentModificationDate)(?:Key)?\b|\b(?:getattrlist\w*|fgetattrlist|fstat|fstatat|lstat)\(|\bstat\(
SystemBootTime~\bsystemUptime\b|\bmach_absolute_time\(
DiskSpace~\bvolume(?:Available|Total)Capacity\w*|\bsystem(?:Free)?Size\b|\b(?:statv?fs|fstatv?fs)\(|NSFileSystem(?:Free)?Size
ActiveKeyboards~\bactiveInputModes\b
MAP
done
rg -n --pcre2 "^\s*pod\s+'(?:Firebase\w*|GoogleSignIn|Google-Mobile-Ads-SDK|FBSDK\w*|Alamofire|AFNetworking|Kingfisher|SDWebImage|RealmSwift|lottie-ios|OneSignal\w*)'|^\s+(?:sqflite|shared_preferences|path_provider|url_launcher|image_picker|webview_flutter|flutter_inappwebview|flutter_local_notifications|device_info_plus|package_info_plus|connectivity_plus|share_plus|file_picker|geolocator|fluttertoast|wakelock\w*|firebase_\w+):\s" -g 'Podfile' -g 'pubspec.yaml' "${IROOTS[@]:-/dev/null}"

# 2. Declarations vs use. 2a purpose strings blank or placeholder (Info.plist, build settings, Expo config); 2b a purpose
#    string declared with no API and no plugin that needs it; 2c restricted or declaration-form Android permissions in the
#    merged manifest (else the source), with the remove marker if any; 2d foreground-service types to declare in Play Console.
rg -n -U --pcre2 '<key>(NS\w+UsageDescription)</key>\s*<string>\s*(?:TODO\w*|TBD|FIXME|\$\(PRODUCT_NAME\)[^<]{0,20}|[^<]{0,12})\s*</string>|<key>NS\w+UsageDescription</key>\s*<string/>' -g 'Info.plist' "${X[@]}" "${IROOTS[@]:-/dev/null}"
rg -n --pcre2 '"?(?:INFOPLIST_KEY_)?NS\w+UsageDescription"?\s*[:=]\s*"(?:\s*|TODO[^"]*|TBD|[^"]{0,12})"' -g '*.{pbxproj,xcconfig}' -g 'app.{json,config.js,config.ts}' "${X[@]}" "${IROOTS[@]:-/dev/null}"
for r in "${IROOTS[@]}"; do while IFS='~' read -r key api dep; do rg -q "$key" -g 'Info.plist' -g '*.{pbxproj,xcconfig}' -g 'app.{json,config.js,config.ts}' "${X[@]}" "$r" || continue
  rg -q --pcre2 "$api" "${NAT[@]}" "${X[@]}" "$r" || rg -q --pcre2 "$dep" "${CFG[@]}" "${X[@]}" "$r" || echo "2b $r: $key declared, no API or plugin uses it"; done <<'MAP'
NSCameraUsageDescription~\bAVCaptureDevice\b|UIImagePickerController|\bVNDocumentCamera~\b(?:camera|image_picker|mobile_scanner|qr_code_scanner|expo-camera|expo-image-picker|react-native-vision-camera|react-native-image-picker|expo-barcode-scanner)\b
NSMicrophoneUsageDescription~\bAVAudio(?:Recorder|Session|Engine)\b|SFSpeechRecognizer~\b(?:record|flutter_sound|speech_to_text|camera|expo-av|expo-audio|react-native-vision-camera|react-native-audio-recorder-player)\b
NSPhotoLibraryUsageDescription~\bPHPhotoLibrary\b|PHPicker|UIImagePickerController~\b(?:image_picker|photo_manager|expo-image-picker|expo-media-library|react-native-image-picker|@react-native-camera-roll)\b
NSContactsUsageDescription~\bCNContactStore\b~\b(?:flutter_contacts|contacts_service|expo-contacts|react-native-contacts)\b
NSLocationWhenInUseUsageDescription~\bCLLocationManager\b|requestWhenInUseAuthorization~\b(?:geolocator|location|expo-location|react-native-geolocation-service|@react-native-community/geolocation)\b
NSFaceIDUsageDescription~\bLAContext\b~\b(?:local_auth|expo-local-authentication|react-native-biometrics|react-native-keychain)\b
NSBluetoothAlwaysUsageDescription~\bCBCentralManager\b|CBPeripheralManager~\b(?:flutter_blue\w*|react-native-ble-\w+|react-native-ble-plx)\b
NSUserTrackingUsageDescription~\bATTrackingManager\b~\b(?:app_tracking_transparency|expo-tracking-transparency|react-native-tracking-transparency)\b
NSCalendarsFullAccessUsageDescription~\bEKEventStore\b~\b(?:device_calendar|expo-calendar|react-native-calendar-events)\b
MAP
done
RP='QUERY_ALL_PACKAGES|MANAGE_EXTERNAL_STORAGE|ACCESS_BACKGROUND_LOCATION|READ_MEDIA_(?:IMAGES|VIDEO)|USE_EXACT_ALARM|REQUEST_INSTALL_PACKAGES|(?:READ|RECEIVE|SEND)_SMS|(?:READ|WRITE)_CALL_LOG|PROCESS_OUTGOING_CALLS|BIND_ACCESSIBILITY_SERVICE|BIND_VPN_SERVICE|USE_FULL_SCREEN_INTENT|permission\.health\.\w+|BODY_SENSORS\w*'
[ ${#AM[@]} -eq 0 ] || rg -H -n --no-ignore --pcre2 "<uses-permission[^>]*android:name=\"[\w.]*\.(?:$RP)\"(?![^>]*tools:node=\"remove\")" "${AM[@]}"
[ ${#AM[@]} -eq 0 ] || rg -o --no-ignore --no-filename --pcre2 'foregroundServiceType="\K[^"]+' "${AM[@]}" | tr '|' '\n' | sort | uniq -c | sed 's/^/2d fgs type /'

# 3. Tracking. 3a an iOS root reading the IDFA or linking an ad/attribution SDK with no ATT request; 3b ATT requested
#    with no NSUserTrackingUsageDescription; 3c a manifest saying NSPrivacyTracking false beside such an SDK;
#    3d Android code reading the advertising ID while the manifest removes AD_ID.
AD='\bASIdentifierManager\b|\badvertisingIdentifier\b|google_mobile_ads|react-native-google-mobile-ads|Google-Mobile-Ads-SDK|play-services-ads|FBSDKCoreKit|facebook_app_events|react-native-fbsdk-next|appsflyer|react-native-adjust|adjust_sdk|AppLovin|applovin_max|unity_ads'
ATT='ATTrackingManager|requestTrackingAuthorization|app_tracking_transparency|expo-tracking-transparency|react-native-tracking-transparency|requestTrackingPermission'
for r in "${IROOTS[@]}"; do rg -q -i --pcre2 "$AD" "${SRC[@]}" "${CFG[@]}" "${X[@]}" "$r" || continue
  rg -q --pcre2 "$ATT" "${SRC[@]}" "${CFG[@]}" "${X[@]}" "$r" || echo "3a $r: IDFA or ad SDK, no ATT request ($(rg -l -i --pcre2 "$AD" "${SRC[@]}" "${CFG[@]}" "${X[@]}" "$r" | head -2 | tr '\n' ' '))"
  rg -q --pcre2 "$ATT" "${SRC[@]}" "${CFG[@]}" "${X[@]}" "$r" && ! rg -q --pcre2 'NSUserTrackingUsageDescription|userTrackingPermission' -g 'Info.plist' -g '*.{pbxproj,xcconfig}' -g 'app.{json,config.js,config.ts}' "${X[@]}" "$r" && echo "3b $r: ATT requested, no NSUserTrackingUsageDescription"
  rg -l -U --pcre2 'NSPrivacyTracking</key>\s*<false/>|"NSPrivacyTracking"\s*:\s*false' -g 'PrivacyInfo.xcprivacy' -g 'app.{json,config.js,config.ts}' "${X[@]}" "$r" | sed 's/^/3c tracking declared false beside an ad SDK: /'; done
for r in "${AROOTS[@]}"; do rg -q --pcre2 '\bAdvertisingIdClient\b|getAdvertisingIdInfo' "${SRC[@]}" "${X[@]}" "$r" && rg -q --pcre2 'AD_ID"[^>]*tools:node="remove"' "${MF[@]}" "${X[@]}" "$r" && echo "3d $r: advertising ID read, AD_ID removed from the manifest"; done

# 4. Account duties. 4a account creation with no in-app deletion path (Sign in with Apple token revocation is read, not
#    grepped: it is usually server-side); 4c sign-in on Android with no Restore Credentials (Play, from April 2027).
SU='\bsign_?[uU]p\w*\s*\(|\bregister(?:User|Account)\s*\(|\bcreateUserWithEmailAndPassword\b|\bcreate(?:User|Account)\w*\s*\(|["\x27/](?:auth/)?(?:signup|sign-up|register)["\x27/?]'
DEL='(?i)delete_?(?:my_?)?account|delete_?user|remove_?account|close_?account|account/delete|currentUser!?\??\.delete\(|\buser\.delete\(|\.delete\(\s*["\x27`]/(?:me|account|users?)\b|DELETE[^\n]{0,40}/(?:me|account|users?)\b'
for r in "${ROOTS[@]}"; do rg -q --pcre2 "$SU" "${SRC[@]}" "${X[@]}" "$r" || continue
  rg -q --pcre2 "$DEL" "${SRC[@]}" "${X[@]}" "$r" || echo "4a $r: account creation ($(rg -l --pcre2 "$SU" "${SRC[@]}" "${X[@]}" "$r" | sort | head -2 | tr '\n' ' ')), no deletion path"
  done
for r in "${AROOTS[@]}"; do rg -q --pcre2 "$SU|\bsign_?[iI]n\w*\s*\(|\blogin\w*\s*\(" "${SRC[@]}" "${X[@]}" "$r" && ! rg -q --pcre2 'RestoreCredential|createRestoreCredential|GetRestoreCredentialOption' "${SRC[@]}" "${X[@]}" "$r" && echo "4c $r: sign-in, no Restore Credentials (Play requirement from 2027-04)"; done

# 5. Login 4.8. 5a an iOS root offering a third-party login with no Sign in with Apple or other equivalent option (verify).
for r in "${IROOTS[@]}"; do rg -q --pcre2 '\bGIDSignIn\b|google_sign_in|@react-native-google-signin|FBSDKLoginKit|flutter_facebook_auth|react-native-fbsdk-next|expo-auth-session/providers/(?:google|facebook)|\bLineSDK\b' "${SRC[@]}" "${CFG[@]}" "${X[@]}" "$r" &&
  ! rg -q --pcre2 'ASAuthorizationAppleIDProvider|sign_in_with_apple|expo-apple-authentication|apple-authentication|SignInWithAppleButton|AppleAuthProvider|OAuthProvider\(\s*["\x27]apple\.com' "${SRC[@]}" "${CFG[@]}" "${X[@]}" "$r" && echo "5a $r: third-party login, no Sign in with Apple or equivalent (verify 4.8)"; done

# 6. Target and build SDK. 6a the target per Android root (merged first); 6b the iOS deployment target; 6c the Xcode that
#    builds uploads (CI, Fastlane, EAS); 6d Wear OS / Automotive markers, whose floor is 35, not 36.
[ ${#MM[@]} -eq 0 ] || rg -H -n -o --no-ignore --pcre2 'android:targetSdkVersion="\d+"' "${MM[@]}"
rg -n --pcre2 '\btargetSdk(?:Version)?\b\s*[=:]?\s*(?:\d+|flutter\.\w+|libs\.\S+)|"targetSdkVersion"\s*:\s*\d+' -g '*.{gradle,kts,toml}' -g 'app.{json,config.js,config.ts}' "${X[@]}" "${GROOTS[@]}"
rg -n --pcre2 'IPHONEOS_DEPLOYMENT_TARGET\s*=\s*[\d.]+|^\s*platform\s+:ios\s*,\s*["\x27][\d.]+|"deploymentTarget"\s*:\s*"[\d.]+"' -g '*.{pbxproj,xcconfig}' -g 'Podfile' -g 'app.{json,config.js,config.ts}' "${X[@]}" "${IROOTS[@]:-/dev/null}"
rg -n --hidden --pcre2 'xcode-version:\s*["\x27]?[\d.]+|\bxcodes?\(\s*version:\s*"[\d.]+|\bxcversion\(\s*version:\s*"[\d.]+|Xcode_[\d.]+\.app|"image"\s*:\s*"[^"]*(?:macos|xcode)[^"]*"|^\s*(?:runs-on|xcode):\s*["\x27]?(?:macos-\d+|[\d.]+)' -g '.github/workflows/*.{yml,yaml}' -g '{Fastfile,eas.json,codemagic.yaml,bitrise.yml,.xcode-version}' -g '!**/node_modules/**' .
[ ${#AM[@]} -eq 0 ] || rg -H -n --no-ignore --pcre2 'android\.hardware\.type\.(?:watch|automotive)|com\.google\.android\.gms\.car\.application' "${AM[@]}"

# 7. 16 KB pages. 7a the AGP version (needs >= 8.5.1); 7b the NDK version (r28 aligns by default; older needs the
#    max-page-size flags); 7c prebuilt .so files shipped from the repo — the probe decides each.
rg -n --pcre2 'com\.android\.tools\.build:gradle:[\d.]+|id\s*\(?\s*["\x27]com\.android\.(?:application|library)["\x27]\s*\)?\s*version\s*["\x27][\d.]+|^\s*(?:agp|androidGradlePlugin|android-gradle-plugin)\s*=\s*["\x27][\d.]+' -g '*.{gradle,kts,toml}' "${X[@]}" "${GROOTS[@]}"
rg -n --pcre2 '\bndkVersion\b\s*[=:]?\s*["\x27]?[\d.]+|max-page-size=16384' -g '*.{gradle,kts,txt,mk,cmake}' "${X[@]}" "${GROOTS[@]}"
rg --files -g '*.so' -g '!**/{node_modules,build,.gradle,.cxx,Pods}/**' "${AROOTS[@]:-/dev/null}" | sed 's/^/7c prebuilt native library: /'

# 8. Data declarations vs SDKs. 8a data-collecting SDKs (the inventory the judge reconciles against App Privacy and Data
#    safety) — npm / pub names, pods, Gradle coordinates (`group:artifact`), scoped and `react-native-` wrappers; 8b a
#    manifest whose collected-data list is empty beside such an SDK; 8c Data safety exports kept in the repo.
SDK='firebase[_-]?analytics|FirebaseAnalytics|firebase_crashlytics|FirebaseCrashlytics|@react-native-firebase/(?:analytics|crashlytics)|sentry|bugsnag|datadog|instabug|amplitude|mixpanel|segment|posthog|appsflyer|adjust|branch|onesignal|braze|google_mobile_ads|react-native-google-mobile-ads|play-services-ads|Google-Mobile-Ads|FBSDK|facebook_app_events|react-native-fbsdk-next|dd-sdk-android'
rg -n -i --pcre2 "(?:[\"\x27 ]|[:@](?=(?:$SDK)[\"\x27:/-])|-(?=(?:$SDK)[\"\x27:]))(?:$SDK)[\w.:/-]*[\"\x27:]" "${CFG[@]}" "${X[@]}" "${ROOTS[@]}" | sed 's/^/8a /'
for r in "${IROOTS[@]}"; do rg -q -i --pcre2 "$SDK" "${CFG[@]}" "${X[@]}" "$r" || continue
  rg -l -U --pcre2 'NSPrivacyCollectedDataTypes</key>\s*(?:<array/>|<array>\s*</array>)|"NSPrivacyCollectedDataTypes"\s*:\s*\[\s*\]' -g 'PrivacyInfo.xcprivacy' -g 'app.{json,config.js,config.ts}' "${X[@]}" "$r" | sed 's/^/8b no collected data declared beside a data SDK: /'; done
rg --files -g '*{data_safety,data-safety,datasafety}*' -g '!**/node_modules/**' "${ROOTS[@]}"

# 9. Payments. 9a a web checkout opened from the app (digital unlock 3.1.1 vs physical goods 3.1.5: read); 9b IAP with no
#    restore path; 9c the Play Billing Library version (8+ for new apps and updates from 2026-08-31).
rg -n --pcre2 'buy\.stripe\.com|checkout\.stripe\.com|paypal\.com/checkoutnow|\bredirectToCheckout\b|(?:openURL|launchUrl|open)\([^)]*(?:checkout|subscribe|upgrade|premium|pricing|/pro\b)' "${SRC[@]}" "${X[@]}" "${ROOTS[@]}" | "${NC[@]}"
for r in "${ROOTS[@]}"; do rg -q --pcre2 '\bStoreKit\b|SKPaymentQueue|Product\.products|react-native-iap|expo-iap|\bin_app_purchase\b|purchases_flutter|react-native-purchases|\bBillingClient\b|billingclient' "${SRC[@]}" "${CFG[@]}" "${X[@]}" "$r" || continue
  rg -q --pcre2 'restore(?:Completed)?(?:Transactions|Purchases)\w*|AppStore\.sync|getAvailablePurchases|queryPurchases(?:Async)?|Purchases\.(?:shared\.)?restore' "${SRC[@]}" "${X[@]}" "$r" || echo "9b $r: in-app purchase, no restore path"; done
rg -n --pcre2 'com\.android\.billingclient:billing(?:-ktx)?:[\d.]+' -g '*.{gradle,kts,toml}' "${X[@]}" "${GROOTS[@]}"
```

A row is a grep hit **plus** the effective config **plus** the gate's date against today. Three blind spots are structural:

- **No build, no merged manifest.** The script falls back to source manifests and says so; a library-injected permission, an SDK's `AD_ID` and `flutter.targetSdkVersion` are invisible until a release build exists. Mark those rows `[report-flagged]` with the build and probe that settle them.
- **Required-reason APIs in SDK binaries.** § 1 greps your Swift and Objective-C; an SDK's use is covered only by that SDK's own manifest (1c prints the listed SDKs to read).
- **The Xcode that uploads is in CI.** § 6c reads Fastlane, GitHub Actions, EAS and similar; a build machine configured outside the repo is invisible — read the archive's `DTXcode`.

**Measured** (2026-10-05, ripgrep 15.2.0; bash 3.2 and zsh give the same sorted hit set, with stdin piped or not; under 1 s). On the program's seeded multi-stack sample (23 store positives, 2 SCHEDULE rows, 20 decoys across the nine classes; one merged manifest with a library-injected `QUERY_ALL_PACKAGES`) the script surfaces every positive and prints no decoy as a tagged row or a §§ 1–5, 8–9 hit; §§ 6–7 print every version line, decoys included, because the gate comparison against today is the read step. On every web and server fixture in `benchmarks/fixtures/*` it finds no mobile root and prints `N/A`; on `mobile-defects` (five mobile roots, measured 2026-10-10) it prints all 12 of its seeds in 51 lines — its `DEFECTS.md` § Detector measurement. A first version left four data SDKs out of the 8a inventory there: the id had to follow a quote or a space, so Gradle coordinates (`com.google.firebase:firebase-analytics`, `io.sentry:sentry-android`, `com.datadoghq:dd-sdk-android-rum`) and a `react-native-appsflyer` wrapper were missed; a `:` / `@` / `-` prefix now counts when the id ends at a separator. On a read-only real Flutter app (1,167 files) the first version found no merged manifest — Flutter writes Android output to `build/app/intermediates`, not `android/app/build` — so `targetSdk = flutter.targetSdkVersion` stayed unresolved; matching `**/intermediates/merged_manifests/**` (release variant, one ABI copy) resolves it to 36. The run prints 0 findings, 1 SCHEDULE row (§ 4c) and 4 listed-SDK lines for the read. The A-tier probe on that app's release APK (built 2026-09-12): `aapt2 dump badging` → `targetSdkVersion:'36'`; `zipalign -c -P 16 -v 4` → `Verification successful`; `apkanalyzer` failed for want of a Java runtime, so the probe uses `aapt2`. No iOS archive and no Xcode on the host: every iOS probe was `SKIPPED`.

## The 3,000-hit path

Store rows rarely reach thousands, but SDK inventories and permission lists in a monorepo of white-label apps do:

1. **Intersect** with what ships: a flavour or target that no release lane builds is dismissed with one read of the CI config.
2. **Group** by declaration file and gate: one merged manifest with six restricted permissions is one § 2c group; one `PrivacyInfo.xcprivacy` missing three categories is one § 1 group.
3. **Rank** by axis and date: HARD-BLOCK past its date, then HARD-BLOCK within 30 days, REJECTION, PENALTY, SCHEDULE.
4. **Read the top 30 groups fully**, each against its gate row.
5. **Prefer the bulk probe at scale**: one `aapt2 dump badging` per release artifact and one `plutil -p` per built app settle §§ 1, 2, 6 for every flavour at once.
6. **Ledger the rest** as `Live, unreviewed (k groups / n hits)` with the command that continues them. Never `checked`.

## Scans for

| § | Class | Gate | Tier | Axis |
|---|---|---|---|---|
| 1 | Privacy manifest and required-reason APIs; listed SDKs | G4, G5 | A | HARD-BLOCK |
| 2 | Purpose strings blank, placeholder or unused; restricted Android permissions; FGS types to declare | G9, G11, G13, G14 | A | REJECTION |
| 3 | Tracking: IDFA or ad SDK with no ATT, ATT with no string, manifest says no tracking; `AD_ID` removed but used | G9, G12 | A + D | REJECTION |
| 4 | Account creation with no in-app deletion; Restore Credentials on Android | G7, G8, G18 | D | REJECTION · SCHEDULE |
| 5 | Third-party login with no equivalent option | G9 (4.8) | S | VERIFY |
| 6 | Target API, deployment target, the Xcode that uploads | G1, G2, G3 | A | HARD-BLOCK |
| 7 | 16 KB pages: AGP, NDK, prebuilt native libraries | G16 | A | SCHEDULE → HARD-BLOCK |
| 8 | Data declarations vs the SDKs that collect | G9, G10 | A + read | REJECTION |
| 9 | Payments: web checkout for digital unlocks, no restore, an old Billing Library | G9 (3.1.1), G15 | S · D · A | REJECTION · HARD-BLOCK |

### 1. Privacy manifest and required-reason APIs

```
BAD:   url.resourceValues(forKeys: [.contentModificationDateKey]) and .volumeAvailableCapacityForImportantUsageKey
       with PrivacyInfo.xcprivacy declaring only NSPrivacyAccessedAPICategoryUserDefaults (CA92.1)
GOOD:  NSPrivacyAccessedAPICategoryFileTimestamp (C617.1: files inside the app container) + NSPrivacyAccessedAPICategoryDiskSpace (E174.1: check before writing)
```
**Read the code:** Which reason matches the real use? The five categories and their codes (Apple `NSPrivacyAccessedAPIType` reference, read 2026-10-05): UserDefaults CA92.1 / 1C8F.1 / C56D.1 / AC6B.1; FileTimestamp DDA9.1 / C617.1 / 3B52.1 / 0A2A.1; SystemBootTime 35F9.1 / 8FFB.1 / 3D61.1; DiskSpace 85F4.1 / E174.1 / 7D9E.1 / B728.1; ActiveKeyboards 3EC4.1 / 54BD.1. Is `.modificationDate` a file attribute or the app's own model field (not covered)? Does each listed SDK's locked version ship its manifest (1c)? In an Expo app, is the declaration in `ios.privacyManifests`? **Finding when** a category used by app code is in no manifest the app ships. **Axis:** HARD-BLOCK (G4). **Probe:** `plutil -p Payload/<App>.app/PrivacyInfo.xcprivacy` on the archive, and Organizer's privacy report.

### 2. Declarations vs use

```
BAD:   <key>NSMicrophoneUsageDescription</key><string></string>     <key>NSContactsUsageDescription</key><string>TODO</string>
       merged manifest: android.permission.QUERY_ALL_PACKAGES (injected by an SDK, absent from the source manifest)
GOOD:  a sentence naming the feature and the data; tools:node="remove" for an SDK-injected permission the app does not need
```
**Read the code:** Is the key supplied by a build setting or a config plugin (precedents § 24 — confirm in the prebuild output)? Is a declared key used by a plugin the map does not know? For each restricted permission: is it core to the app (G11, G13; a gallery, a file manager), declared in Play Console, or removable? Which FGS types (2d) must the App content declaration describe (G14)? **Finding when** a shipped string is blank or a placeholder, a string describes no use in the app, or a restricted permission ships without core use. **Axis:** REJECTION. **Probe:** `aapt2 dump badging <apk> | rg uses-permission`; `plutil -p` the built Info.plist.

### 3. Tracking

```
BAD:   ASIdentifierManager.shared().advertisingIdentifier   // no ATTrackingManager request anywhere in the root
       PrivacyInfo.xcprivacy: NSPrivacyTracking false, beside FirebaseAnalytics / an ad SDK
GOOD:  requestTrackingPermissionsAsync() before the SDK starts + userTrackingPermission / NSUserTrackingUsageDescription
```
**Read the code:** Does the SDK track (links data with third-party data for ads or shares with a data broker), or only measure first-party use? Is tracking started before the prompt is answered, or gated behind it? Is any feature or reward conditioned on allowing tracking (5.1.2(i) forbids it)? On Android, is `AD_ID` declared (often merged in by the ads SDK — G12) or removed while code reads the ID? **Finding when** the app tracks without the ATT flow, or its manifest denies tracking it does. **Axis:** REJECTION. **Probe:** D — a fresh install with tracking denied: a proxy shows no ad-ID or attribution request before the answer.

### 4. Account duties

```
BAD:   signUp() → api.post('/auth/register', …)   and no delete-account path anywhere in the app
GOOD:  Settings → Delete account → DELETE /me (+ Sign in with Apple token revoked server-side) · Play: a web deletion link in Data safety
```
**Read the code:** Can a user create an account in the app (not only sign in to one issued elsewhere)? Is deletion reachable in the app, and does it remove the account record, not deactivate it (G7)? With Sign in with Apple, does the server revoke the token through Apple's REST API (`/auth/revoke`) — usually in the backend, so read it there or record `unconfirmed`. Does the Play listing carry the web deletion link (G8; Console, not repo)? § 4c is SCHEDULE until April 2027 (G18). **Finding when** accounts can be created and not deleted in the app. **Axis:** REJECTION; 4c SCHEDULE with days remaining. **Probe:** D — the store flow walk: delete from inside the app for each sign-in provider.

### 5. Login 4.8

```
BAD:   GIDSignIn.sharedInstance.signIn(…) as the only way in, no Sign in with Apple or other equivalent option
GOOD:  Sign in with Apple, or another login limited to name and email with a private-email option and no ad tracking
```
**Read the code:** Is the third-party login the primary account method? Does an exception apply (the company's own account system only, education or enterprise, government ID, a client for that third-party service)? Is the existing email login an *equivalent* (name and email only, private email allowed, no ad tracking without consent)? **Finding when** a primary third-party login has no equivalent. **Axis:** VERIFY — 4.8 asks for an equivalent, not Sign in with Apple specifically (precedents § 49). **Probe:** S (the login screen's options) and the reviewer's judgement.

### 6. Target API, deployment target, the Xcode that uploads

```
BAD:   merged android:targetSdkVersion="35" (G1: updates refused after 2026-11-01)
       platform :ios, '12.0' (G3)                xcodes(version: "16.4") in the release lane (G2)
GOOD:  targetSdk 36 · IPHONEOS_DEPLOYMENT_TARGET 13.0+ · the release lane on Xcode 26
```
**Read the code:** Which value wins — the merged manifest over `build.gradle`, `expo-build-properties` over Expo's default, the Podfile over the project (CocoaPods targets can differ from the app)? Is the app Wear OS or Automotive (6d → floor 35)? Raising `targetSdk` to 36 opts into Android 16 behaviour (predictive back, ignored orientation locks at sw600dp+, edge-to-edge) — route that work to `platform-conventions-audit` and `mobile-lifecycle-scan` rather than planning it as a one-line change (precedents § 52). **Finding when** the shipped value is below the gate on the run's date. **Axis:** HARD-BLOCK — or, where Play granted the extension, HARD-BLOCK on its date with the days to it. **Probe:** `aapt2 dump badging <apk> | rg targetSdkVersion`; `plutil -p Payload/<App>.app/Info.plist | rg "DTXcode|DTSDKName|MinimumOSVersion"`.

### 7. 16 KB pages

```
BAD:   id("com.android.application") version "8.3.2"   ·   ndkVersion = "27.1.12297006" with no max-page-size flags
       src/main/jniLibs/arm64-v8a/libimagefilter.so (prebuilt, alignment unknown)
GOOD:  AGP ≥ 8.5.1 · NDK r28+ (aligned by default) or -Wl,-z,max-page-size=16384 · vendor rebuilds of prebuilt libraries
```
**Read the code:** Does the app ship native code at all — directly, or through a runtime (React Native, Flutter, Expo) or an SDK? Java/Kotlin-only apps already comply (G16 page). Is each prebuilt `.so` rebuilt aligned by its vendor? **Finding when** the release artifact fails the alignment probe, or the build cannot produce an aligned one (AGP < 8.5.1, NDK < r28 without the flags). **Axis:** SCHEDULE → HARD-BLOCK on 2027-02-01. **Probe:** `zipalign -c -P 16 -v 4 <apk>` → `Verification successful`; `check_elf_alignment.sh <apk>` or `llvm-objdump -p <lib>.so | rg LOAD` (`align 2**14`).

### 8. Data declarations vs SDKs

```
BAD:   pod 'FirebaseAnalytics' with PrivacyInfo.xcprivacy NSPrivacyCollectedDataTypes = []
GOOD:  each collected type (identifiers, usage data, diagnostics) declared, linked / tracking flags set, mirrored in App Privacy and Data safety
```
**Read the code:** Which data does each SDK in 8a collect in this app's configuration (crash-only Crashlytics vs analytics; ads)? Do the in-repo declarations (manifest, a Data safety export in 8c) match? The App Store Connect answers and the Play form live outside the repo: hand the inventory to `@app-store-reviewer` for that reconciliation. **Finding when** a shipped declaration contradicts an SDK the app ships (G10: SDK practices count). **Axis:** REJECTION. **Probe:** A — the manifests in the archive; the merged manifest's SDK components.

### 9. Payments

```
BAD:   UIApplication.shared.open(URL(string: "https://buy.stripe.com/acme-pro")!)   // a digital "Pro" unlock
       buyNonConsumable(…) and no restorePurchases()   ·   com.android.billingclient:billing-ktx:7.1.1 (G15)
GOOD:  StoreKit / Play Billing for digital unlocks (or a US-storefront link-out the team chose deliberately); Restore Purchases; PBL 8+
```
**Read the code:** Is the item digital (3.1.1) or a physical good or service (3.1.5 — card payment allowed, precedents § 49)? Which storefronts ship — the US link-out exception does not travel. Does a fresh install on a second device get its non-consumables and subscriptions back? Which Billing Library does a cross-platform plugin bundle (read its version)? **Finding when** a digital unlock bypasses the store's billing outside an allowed case, a restorable purchase cannot be restored, or the Billing Library is below G15. **Axis:** REJECTION (VERIFY per storefront for 9a); HARD-BLOCK for 9c past its extension. **Probe:** D — the store flow walk (restore on a fresh install); A for the Billing Library in the artifact's dependencies.

## Proof — the store probes

The probe shapes and the store flow walk are in [`proof-oracles.md`](../../../../snippets/proof-oracles.md) § Mobile (store probe, store flow walk). Run them on the artifact that will be uploaded — a probe on yesterday's build proves nothing about today's — and record its build date beside the result:

```bash
aapt2 dump badging app-release.apk | rg "targetSdkVersion|uses-permission"      # Android: what Play reads
zipalign -c -P 16 -v 4 app-release.apk                                          # 16 KB: "Verification successful"
plutil -p Payload/App.app/Info.plist | rg "DTXcode|DTSDKName|MinimumOSVersion"  # iOS: the Xcode, SDK and target that built it
plutil -p Payload/App.app/PrivacyInfo.xcprivacy                                 # and each Frameworks/*.framework manifest
```

For an AAB, build a universal APK with `bundletool build-apks --mode=universal` first. No artifact or no toolchain: the row is `[report-flagged]` with these commands written out — never PASS.

## Output

```
store-compliance-scan — run 2026-10-05 · lanes: android-native (AGP 8.3.2, merged manifest release), expo SDK 57,
                        flutter 3.47, ios-app (Podfile, Fastfile) · gate table read 2026-10-05
Artifacts: android-native app-release.apk (built 2026-10-04); no iOS archive → iOS probes SKIPPED

Rows: 3 HARD-BLOCK · 2 REJECTION · 2 SCHEDULE · 1 VERIFY · Unconfirmed: 2

1. android-native/app/build/intermediates/merged_manifests/release/processReleaseManifest/AndroidManifest.xml:3   [report-with-fix]
   §6 G1 targetSdk 35 — HARD-BLOCK now unless Play granted the extension; then on 2026-11-01 (27 days). Probe: aapt2 → targetSdkVersion:'35'.
   Fix: targetSdk = 36 in app/build.gradle.kts:5; route Android 16 behaviour to platform-conventions-audit.

2. ios-app/Acme/Store/CacheJanitor.swift:7                                                                       [report-flagged]
   §1 G4 FileTimestamp and DiskSpace used, PrivacyInfo.xcprivacy declares only UserDefaults — HARD-BLOCK (since 2024-05-01).
   Unproven link: no archive. Settling probe: plutil -p Payload/Acme.app/PrivacyInfo.xcprivacy after archiving.
   Fix: add FileTimestamp C617.1 and DiskSpace E174.1.

3. android-native/settings.gradle.kts:3                                                                          [report-with-fix]
   §7 G16 AGP 8.3.2 (< 8.5.1) + NDK r27 without max-page-size + a prebuilt .so — SCHEDULE → HARD-BLOCK 2027-02-01 (119 days).
   Probe: zipalign -c -P 16 -v 4 → lib/arm64-v8a/libimagefilter.so (BAD) (fails).

Verification: 25 candidates → 8 rows · 2 unconfirmed · 1 hardening · 14 refuted
Routed: purpose-string wording → @app-store-reviewer · vitals (G17) → mobile-perf-scan · targetSdk 36 behaviour → platform-conventions-audit

Class coverage:
  §1  privacy manifest            checked (2 hits → 1 row)
  §2  declarations vs use         checked (6 hits → 2 rows; READ_MEDIA_IMAGES routed to lifecycle §3e for partial access)
  §3  tracking                    checked (2 hits → 1 row)
  §4  account duties              checked (3 hits → 1 row · 2 SCHEDULE)
  §5  login 4.8                   checked (1 hit → 1 VERIFY)
  §6  target / build SDK          checked (8 lines → 3 rows)
  §7  16 KB pages                 checked (5 lines → 1 group)
  §8  data declarations           checked (3 lines → 1 row)
  §9  payments                    checked (4 hits → 2 rows; Stripe for deliveries is precedent § 49)
```

`[report-with-fix]`: the shipped value, the gate row, the date against today and a probe on the artifact are cited, and the fix is local. `[report-flagged]`: one link is unproven (no artifact, no merged manifest, a Console-side fact), and the row names the probe. The coverage block lists **all nine** classes on every run: `checked`; `N/A (<reason>)` only for a missing surface (no iOS target, no accounts, no purchases); `blocked (<reason>)` when a grep failed; `Live, unreviewed (k groups / n hits)` for a partial review.

## False positives / precedents

The verifier reads [`precedents/mobile.md`](../../../../snippets/precedents/mobile.md) — § 3 (fix Expo CNG in app config), § 6 (store-text quality is the reviewer's), § 18 (legitimate special access), § 24–25 (plugin-supplied strings, removed permissions), § 49 (3.1.5, 4.8 as VERIFY, "per the page as of"), § 52 (what raising `targetSdk` opts into), and the store-specific § 80–83: a missing manifest is not a finding by itself (§ 80, § 1c here); SDK-merged `AD_ID` in an app that uses ads (§ 81, G12); debug-only manifests and entitlements (§ 82); dates past their extension are HARD-BLOCK, not SCHEDULE (§ 83) — and [`refute-before-report.md`](../../../../snippets/refute-before-report.md) § 4.

## When to run

- On any diff that touches a manifest, `Info.plist`, a privacy manifest, app config, Gradle or Podfile versions, CI release lanes, a sign-up or sign-in flow, an ads, analytics or payments SDK — the `/mobile-audit` dispatch signal.
- Before every store submission, and on the first run after any gate's date in the table passes.

## Halt conditions

- Do not report a row as confirmed until a verifier other than the run that found it has passed it through [`refute-before-report.md`](../../../../snippets/refute-before-report.md) with [`precedents/mobile.md`](../../../../snippets/precedents/mobile.md), § 80–83 above all. Under `/mobile-audit` that is its verification phase; standalone, apply the protocol as a separate pass, tag those rows `self-verified`, and keep the rest as Unconfirmed, Hardening or Refuted. Never drop them.
- Halt on any row without the `<file:line>`, the gate row and its date, and the axis.
- Do not give a store row a security severity, or a security finding a store date.
- Do not quote a gate whose page was last read more than 90 days before the run without re-reading it; do not quote a date or a guideline number that is not in the table or read on this run.
- Do not mark `[report-with-fix]` without a probe on the artifact being shipped; no artifact, Xcode or emulator → `SKIPPED`, never PASS.
- Do not judge a manifest class from the source manifest when a merged manifest or a build exists; do not put a fix into git-ignored `ios/` or `android/` of an Expo CNG project.
- Do not print "store ready" without the class-coverage block; a class whose grep did not run is `blocked`, never `checked`.
- Do not re-derive a class another skill owns (§ Boundaries). Route it.

## Related

- `/mobile-audit` dispatches this skill and folds its coverage block into the class ledger; `/mobile-fix` closes rows failing-first and re-runs this detector; `@app-store-reviewer` (this pack) judges and buckets them against the live policy.
- `mobile-lifecycle-scan` owns the crash half of purpose strings and FGS types; `offline-sync-scan` owns what logout leaves behind; `mobile-perf-scan` measures the vitals G17 judges.
- `mobile-security-scan` (security pack, when installed) owns storage, transport, IPC and release-signing classes.
- `ai-patterns/release-pipeline.md` and `permissions.md` (this pack) hold the design guidance; other mobile files cite § The dated store gates here instead of repeating a date.
