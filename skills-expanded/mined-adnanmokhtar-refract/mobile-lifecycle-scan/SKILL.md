---
name: mobile-lifecycle-scan
description: Find lifecycle defects in RN/Expo, Flutter, iOS and Android apps — state lost on process death, background and FGS limits, permission dead ends, network calls with no timeout, deep-link payload crashes, push token and cold-start tap routing, OTA runtime mismatch — each proved on a device.
kind: skill
pack: mobile
allowed-tools: [Read, Grep, Glob, Bash]
---

# Skill: mobile-lifecycle-scan

## Premise

A mobile app does not own its process. The OS kills it in the background, revokes its permissions from Settings, delivers a link or a push to an app that is not running, runs its background work on the OS's schedule or not at all, and updates its JavaScript under a binary that may not match. Every class here is a gap between what the code assumes about that lifecycle and what the OS does, on the OS version and `targetSdk` the app really builds against. None of it shows in a host test: a unit test runs in a process nobody kills.

**Every finding cites the code or config `<file:line>` + the OS event that triggers it + the version gate (lockfile or build-file line) + the oracle at its required tier (or the command that would settle it) + the fix in the project's stack.** A grep hit is never a finding by itself, and "no lifecycle defect found" is never printed without the class-coverage block (§ Output).

**Detect statically, prove on a device.** The proof tiers are D (device or emulator), I (instrumented or widget test), A (shipped artifact: merged manifest, signed entitlements) and S (static trace) — [`precedents/mobile.md`](../../../../snippets/precedents/mobile.md) § The claim, restated. Each class below names its required tier. **No booted device means `SKIPPED`, never PASS**, and a candidate below its tier is **Unconfirmed** with the settling command, never dropped and never promoted on reading alone ([`refute-before-report.md`](../../../../snippets/refute-before-report.md) § 2, gate 6).

## The rule

A candidate is a finding when all five hold:

1. **It ships.** Release build, not `__DEV__` / `kDebugMode` / `BuildConfig.DEBUG` / `#if DEBUG` / `src/debug/` / a test target, and a real entry point (launcher, link, push, job, screen) reaches it.
2. **The version gate holds.** The behaviour exists on the project's versions, read from the files grep 0 prints: merged `targetSdk`, `react-native`, `expo` SDK, Flutter, iOS deployment target ([`precedents/mobile.md`](../../../../snippets/precedents/mobile.md) § 50–59).
3. **The effective config agrees.** The merged `AndroidManifest.xml` (`build/intermediates/merged_manifests/**`, or `apkanalyzer manifest print`), the signed entitlements (`codesign -d --entitlements :-`), the Expo prebuild output and config plugins — not only the source file. Libraries inject services, receivers and permissions.
4. **Nothing neutralizes it.** A wrapper, a library default, a base screen, a config plugin.
5. **The OS event really occurs** in the product's use — and the oracle at the class's tier fires, or the candidate stays Unconfirmed.

## Boundaries

- Listener, observer, controller and subscription leaks (acquire minus release) → `mobile-perf-scan` § 7 (this pack). Main-thread blocking, lists, images, startup → `mobile-perf-scan`.
- Outbox durability, retry idempotency, cross-account residue in caches and databases → `offline-sync-scan` (this pack), judged by `@offline-sync-auditor`. A push token left registered at logout stays here (§ 6); the two runs dedupe by `<file:line>`.
- Predictive back, edge-to-edge insets, navigation patterns (navigate in a composable body, unbounded stacks) → `platform-conventions-audit` (this pack).
- Purpose-string wording, FGS and permission **declarations** as store policy, privacy manifest, target-API dates, OTA content that changes the app's purpose → `store-compliance-scan` and `@app-store-reviewer` (this pack). A missing purpose string is a **crash** here (§ 3) and a release blocker there.
- Link hijack (an https filter with no `autoVerify`, a custom scheme for OAuth or payment returns), a link parameter reaching a WebView or `openURL`, token storage, cleartext → `mobile-security-scan` when the security pack is installed. Without it, § 5d rows are reported here, tagged `security-class (owner pack not installed)`.
- The **rendered** error or never-ending loading state → `ui-state-scan` § 3 and § 11 when the ui-ux pack is installed; § 4 here owns the client's timeout. Without ui-ux, § 4e rows are reported here. Both runs dedupe by `<file:line>`.
- An unhandled rejection or swallowed error in general code → code-quality's error-handling detector when that pack is installed; § 4e keeps only network calls that drive a screen.
- New-Architecture bridge threading and lifecycle → `native-bridge-audit` (this pack).

## Adapt to the codebase — lanes

Read the versions grep 0 prints before applying any row, and print the lanes you ran in the output header. Under Expo CNG (`android/` and `ios/` git-ignored), ripgrep skips the generated folders because it honours `.gitignore`; that is correct — the fix belongs in `app.json` / `app.config.*` or a config plugin ([`precedents/mobile.md`](../../../../snippets/precedents/mobile.md) § 3).

| Lane | Restoration primitive | Background API | Permission + "go to Settings" | Push | OTA | Lint lane (project config, keep only the rule) |
|---|---|---|---|---|---|---|
| **React Native** (bare, ≥ 0.82 New Architecture only) | none in JS: persist drafts; `RNScreensFragmentFactory` in `MainActivity`; React Navigation state persistence | headless JS, native modules | `react-native-permissions` `RESULTS.BLOCKED` + `openSettings`; `PermissionsAndroid` | `@react-native-firebase/messaging` | EAS Update in bare RN, hot-updater; CodePush retired | `react-hooks/exhaustive-deps`, `@typescript-eslint/no-floating-promises` |
| **Expo** (SDK 53–57) | as RN | `expo-background-task` (not `-fetch`), `TaskManager.defineTask` at module scope | `canAskAgain` + `Linking.openSettings()` | `expo-notifications` | `expo-updates`: `runtimeVersion` policy, code signing, `checkAutomatically` | as RN |
| **Flutter** (3.x) | `restorationScopeId`, `RestorationMixin`, `restorablePush*` | workmanager, `@pragma('vm:entry-point')` | permission_handler `isPermanentlyDenied` + `openAppSettings()` | `firebase_messaging` | Shorebird (Dart-only patches) | `flutter analyze`: `use_build_context_synchronously`, `unawaited_futures` |
| **Android** (Kotlin, Compose, Views) | `SavedStateHandle`, `rememberSaveable`, `onSaveInstanceState` | WorkManager, typed FGS, `canScheduleExactAlarms` | `shouldShowRequestPermissionRationale` + `ACTION_APPLICATION_DETAILS_SETTINGS` | `FirebaseMessagingService.onNewToken`, channels | — | `./gradlew lintRelease`: `ForegroundServiceType`, `ScheduleExactAlarm`, `WakelockTimeout`, `NotificationPermission`, `SelectedPhotoAccess`, `RepeatOnLifecycleWrongUsage`; detekt `GlobalCoroutineUsage` |
| **iOS** (Swift, SwiftUI, UIKit) | `@SceneStorage`, `NavigationPath` codable, `stateRestorationActivity` | `BGTaskScheduler` + `BGTaskSchedulerPermittedIdentifiers` | `UIApplication.openSettingsURLString` | `UNUserNotificationCenterDelegate` `willPresent` | — | SwiftLint `discarded_notification_center_observer`, `unhandled_throwing_task` (opt-in) |

## Pre-flight greps

Run as **one** script from the repo root (shell state does not survive between tool calls). Grep **N** feeds detector **§N**; grep 0 is context. Every `rg` names its path (`.` or `"${ROOTS[@]}"`), and set-differences use `while read` with an explicit file, never a bare `xargs rg`: given no path, ripgrep reads stdin under an agent's shell and returns zero hits or hangs. A line printed with a `2a`–`7d` tag is a set-difference result; the rest are grep hits. Any `rg` error on stderr is a failed grep, never zero hits.

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

# 0. Version gates (every rule below is gated on one of these lines) and the CNG check.
rg -n --pcre2 '"(?:react-native|expo|react-native-screens|expo-updates|expo-notifications|expo-background-(?:fetch|task)|@react-native-firebase/messaging|@notifee/react-native|react-native-code-push|axios)"\s*:' -g 'package.json' "${X[@]}" "${ROOTS[@]}"
rg -n --pcre2 '^\s+(?:flutter|dio|http|firebase_messaging|workmanager|go_router|permission_handler):\s*["^>=]*\d' -g 'pubspec.yaml' "${ROOTS[@]}"
rg -n --pcre2 '\b(?:targetSdk(?:Version)?|compileSdk(?:Version)?)\b\s*[=:]?\s*(?:\d+|flutter\.\w+)|IPHONEOS_DEPLOYMENT_TARGET|SWIFT_VERSION|"targetSdkVersion"' -g '*.{gradle,kts,pbxproj,xcconfig,json}' "${X[@]}" "${ROOTS[@]}"
rg -n --hidden --pcre2 '^/?(?:android|ios)/?\s*$' -g '.gitignore' "${ROOTS[@]}"

# 1. Process death, restoration, owner-scoped work. 1a Compose input in remember; 1b ViewModel without SavedStateHandle;
#    1c fragment add in onCreate without a restore guard; 1d RN MainActivity without the screens fragment factory;
#    1e Flutter app without restorationScopeId; 1f setState after await with no mounted check; 1g SwiftUI input
#    with no scene storage; 1h collect without repeatOnLifecycle; 1i GlobalScope.
rg -n --pcre2 '\bremember\s*\{\s*mutableStateOf\(\s*(?:""|TextFieldValue\()' "${KT[@]}" "${X[@]}" "${ROOTS[@]}" | "${NC[@]}"
rg -n -U --pcre2 'class\s+\w+\s*(?:@Inject\s+constructor\s*)?(?:\((?![^)]*SavedStateHandle)[^)]*\))?\s*:\s*(?:Android)?ViewModel\(' "${KT[@]}" "${X[@]}" "${ROOTS[@]}"
rg -n -U --pcre2 '(?s)\bonCreate\([^)]*Bundle[^)]*\)\s*\{(?:(?!(?i:override)\b|\bfun\s|savedInstanceState\s*[!=]=\s*null).)*?\bbeginTransaction\(\)' "${KT[@]}" "${X[@]}" "${ROOTS[@]}"
rg -l 'ReactActivity\b' -g 'MainActivity.{kt,java}' "${X[@]}" "${ROOTS[@]}" | while IFS= read -r f; do rg -q 'RNScreensFragmentFactory|onCreate\(null\)' "$f" || echo "1d $f"; done
rg -n -U --pcre2 '\b(?:MaterialApp|CupertinoApp|WidgetsApp)(?:\.router)?\((?![^;]*\brestorationScopeId\b)' "${DA[@]}" "${X[@]}" "${ROOTS[@]}" | "${NC[@]}"
rg -n -U --pcre2 'await [^;]+;\s*\n\s*setState\(' "${DA[@]}" "${X[@]}" "${ROOTS[@]}"
rg -l --pcre2 '\b(?:TextField|TextEditor|SecureField)\(' "${SW[@]}" "${X[@]}" "${ROOTS[@]}" | while IFS= read -r f; do rg -q '@SceneStorage|NavigationPath|stateRestorationActivity|restorationIdentifier' "$f" || rg -H -n --pcre2 '@State\s+(?:private\s+)?var\s+\w+\s*(?::\s*String\s*)?=\s*""' "$f"; done
rg -n --pcre2 'lifecycleScope\.launch(?:When\w+)?\s*\{(?!.*(?:repeatOnLifecycle|flowWithLifecycle)).*\.collect\b' "${KT[@]}" "${X[@]}" "${ROOTS[@]}" | "${NC[@]}"
rg -n --pcre2 '\bGlobalScope\.(?:launch|async)\b' "${KT[@]}" "${X[@]}" "${ROOTS[@]}" | "${NC[@]}"

# 2. Background work. 2a <service> with no FGS type; 2b dataSync/mediaProcessing FGS class with no onTimeout;
#    2c FGS started from BOOT_COMPLETED; 2d exact alarm with no capability check; 2e wake lock with no timeout;
#    2f iOS BGTask ids, plist vs register (constants resolved; duplicates kill the app); 2g Expo task API;
#    2h Flutter background entry points without @pragma('vm:entry-point').
rg -o --no-filename --pcre2 '<service\b(?![^>]*foregroundServiceType)[^>]*?android:name="[\w.]*?\K\w+(?=")' "${MF[@]}" "${X[@]}" "${ROOTS[@]}" | sort -u | while IFS= read -r c; do
  rg -l --pcre2 "\bclass\s+$c\b" "${KT[@]}" "${X[@]}" "${ROOTS[@]}" | while IFS= read -r f; do rg -q -U --pcre2 "(?s)\bclass\s+$c\b(?:(?!\n(?:[\w@]+\s+)*class\s).)*?\bstartForeground\(" "$f" && echo "2a $c $f"; done; done
rg -o --no-filename -U --pcre2 '<service\b(?=[^>]*foregroundServiceType="[^"]*(?:dataSync|mediaProcessing))[^>]*?android:name="[\w.]*?\K\w+(?=")' "${MF[@]}" "${X[@]}" "${ROOTS[@]}" | sort -u | while IFS= read -r c; do
  rg -l --pcre2 "\bclass\s+$c\b" "${KT[@]}" "${X[@]}" "${ROOTS[@]}" | while IFS= read -r f; do rg -q -U --pcre2 "(?s)\bclass\s+$c\b(?:(?!\n(?:[\w@]+\s+)*class\s).)*?\bonTimeout\(" "$f" || echo "2b $c $f"; done; done
rg -l 'BOOT_COMPLETED' "${KT[@]}" "${X[@]}" "${ROOTS[@]}" | while IFS= read -r f; do rg -H -n 'startForegroundService\(' "$f"; done
rg -l --pcre2 '\bset(?:Exact(?:AndAllowWhileIdle)?|AlarmClock)\(' "${KT[@]}" "${X[@]}" "${ROOTS[@]}" | while IFS= read -r f; do rg -q 'canScheduleExactAlarms' "$f" || echo "2d $f"; done
rg -l --pcre2 '\bnewWakeLock\(|\bWakeLock\b' "${KT[@]}" "${X[@]}" "${ROOTS[@]}" | while IFS= read -r f; do rg -H -n --pcre2 '\.acquire\(\s*\)' "$f"; done
P=$(rg -o --no-filename -U --pcre2 '(?s)BGTaskSchedulerPermittedIdentifiers</key>\s*<array>.*?</array>' -g 'Info.plist' "${X[@]}" "${ROOTS[@]}" | rg -o --pcre2 '(?<=<string>)[^<]+' | sort -u)
R=$( { rg -o --no-filename --pcre2 'forTaskWithIdentifier:\s*"\K[^"]+' "${SW[@]}" "${X[@]}" "${ROOTS[@]}"
      rg -o --no-filename --pcre2 'forTaskWithIdentifier:\s*(?:\w+\.)*\K[a-z]\w*(?=\s*,)' "${SW[@]}" "${X[@]}" "${ROOTS[@]}" | while IFS= read -r n; do
        rg -o --no-filename --pcre2 "\b(?:let|var)\s+$n\s*(?::\s*String\s*)?=\s*\"\K[^\"]+" "${SW[@]}" "${X[@]}" "${ROOTS[@]}"; done; } | sort)
comm -3 <(printf '%s\n' "$P") <(printf '%s\n' "$R" | sort -u) | awk -F'\t' '$1 != "" { print "2f permitted-no-handler " $1; next } { print "2f registered-not-permitted " $2 }'; printf '%s\n' "$R" | uniq -d | sed 's/^/2f registered-twice /'
rg -n --pcre2 '"expo-background-fetch"\s*:' -g 'package.json' "${ROOTS[@]}"; rg -n --pcre2 '^\s+TaskManager\.defineTask\(' "${JS[@]}" "${X[@]}" "${ROOTS[@]}"
rg -o --no-filename --pcre2 '(?:Workmanager\(\)\.initialize|onBackgroundMessage|onStart:)\(?\s*\K[a-zA-Z_]\w*(?=\s*[,)])' "${DA[@]}" "${X[@]}" "${ROOTS[@]}" | sort -u | while IFS= read -r n; do
  rg -q -U --pcre2 "@pragma\(\s*'vm:entry-point'\s*\)\s*\n(?:[\w<>?,]+\s+)*$n\s*\(" "${DA[@]}" "${X[@]}" "${ROOTS[@]}" || echo "2h $n has no @pragma('vm:entry-point')"; done

# 3. Permissions. 3a iOS purpose string missing for an API in use (Info.plist, build settings, Expo config);
#    3b request in an entry file at launch; 3c roots with requests and no permanently-denied path;
#    3d permission state persisted; 3e Android POST_NOTIFICATIONS / partial-photo declarations.
while IFS='~' read -r api key; do for r in "${ROOTS[@]}"; do   # per root: one app's Info.plist never covers another's API use
  rg -q --pcre2 "$api" -g '*.{swift,m,mm}' "${X[@]}" "$r" || continue
  rg -q "$key" -g 'Info.plist' -g '*.{pbxproj,xcconfig}' -g 'app.{json,config.js,config.ts}' "${X[@]}" "$r" || echo "3a $r: $key missing; used at $(rg -l --pcre2 "$api" -g '*.{swift,m,mm}' "${X[@]}" "$r" | head -3 | tr '\n' ' ')"
done; done <<'MAP'
\bAVCaptureDevice\b~NSCameraUsageDescription
\brequestWhenInUseAuthorization\(~NSLocationWhenInUseUsageDescription
\brequestAlwaysAuthorization\(~NSLocationAlwaysAndWhenInUseUsageDescription
\bPHPhotoLibrary\.(?:requestAuthorization|authorizationStatus)~NSPhotoLibraryUsageDescription
\bCNContactStore\b~NSContactsUsageDescription
\bAVAudio(?:Recorder|Session\.sharedInstance\(\)\.requestRecordPermission)~NSMicrophoneUsageDescription
\bLAContext\b~NSFaceIDUsageDescription
\bCBCentralManager\b~NSBluetoothAlwaysUsageDescription
\bATTrackingManager\b~NSUserTrackingUsageDescription
\bEKEventStore\b~NSCalendarsFullAccessUsageDescription
\bSFSpeechRecognizer\b~NSSpeechRecognitionUsageDescription
\bCMMotionActivityManager\b~NSMotionUsageDescription
MAP
RQ='\b(?:requestPermissions?|request(?:Foreground|Background)?Permissions(?:Async)?|requestAuthorization|requestWhenInUseAuthorization|requestAlwaysAuthorization|requestAccess|PermissionsAndroid\.request(?:Multiple)?|request(?=\(PERMISSIONS\.)|Permission\.\w+\.request)\s*\('
rg -n --pcre2 "$RQ" -g '{MainActivity,*Application,AppDelegate,SceneDelegate}.{kt,java,swift}' -g '{App,_layout}.{js,jsx,ts,tsx}' -g 'main.dart' "${X[@]}" "${ROOTS[@]}" | "${NC[@]}"
for r in "${ROOTS[@]}"; do n=$(rg -n --pcre2 "$RQ" "${X[@]}" "$r" | "${NC[@]}" | wc -l | tr -d ' ')
  [ "$n" -gt 0 ] && ! rg -q --pcre2 'shouldShowRequestPermissionRationale|ACTION_APP(?:LICATION_DETAILS|_NOTIFICATION)_SETTINGS|open(?:App|System|Notification)?Settings|AppSettings\.open|canAskAgain|[pP]ermanentlyDenied|RESULTS\.BLOCKED|open(?:Notification)?SettingsURLString' "${X[@]}" "$r" && echo "3c $r: $n request line(s), no permanently-denied path"; done
rg -n -i --pcre2 '(?:permission|granted|authori[sz])\w*.{0,40}(?:putBoolean|setBool|AsyncStorage\.setItem|UserDefaults|prefs\.set)|(?:putBoolean|setBool|AsyncStorage\.setItem|UserDefaults\.standard\.set|\.set(?:Bool|String)?)\(\s*["\x27]\w*(?:permission|granted|authori[sz])' "${X[@]}" "${ROOTS[@]}" | "${NC[@]}"
rg -l --pcre2 'READ_MEDIA_(?:IMAGES|VIDEO)' "${MF[@]}" "${X[@]}" "${ROOTS[@]}" | while IFS= read -r f; do rg -q 'READ_MEDIA_VISUAL_USER_SELECTED' "$f" || echo "3e partial-photo $f"; done
rg -l --pcre2 '\bNotification(?:Compat)?\.Builder\(|FirebaseMessagingService\b' "${KT[@]}" "${X[@]}" "${ROOTS[@]}" | while IFS= read -r f; do m=${f%%/src/main/*}; rg -q 'POST_NOTIFICATIONS' "${X[@]}" "$m" || echo "3e no POST_NOTIFICATIONS in $m ($f)"; done | sort -u

# 4. Network timeouts. 4a axios instance with no timeout; 4b fetch with no signal; 4c dio / http with no timeout;
#    4d a timeout set to zero (OkHttp, URLSession) and HttpURLConnection / Ktor with none; 4e .then with no .catch.
rg -n -U --pcre2 '\baxios\.create\(\s*(?:\)|\{(?![^}]*\btimeout\b)[^}]*\}\s*\))' "${JS[@]}" "${X[@]}" "${ROOTS[@]}"; rg -n --pcre2 '\bdefaults\.timeout\b' "${JS[@]}" "${X[@]}" "${ROOTS[@]}"
rg -n -U --pcre2 '(?<![.\w])fetch\((?![^)]*\bsignal\b)' "${JS[@]}" "${X[@]}" "${ROOTS[@]}" | "${NC[@]}"
rg -n -U --pcre2 '\bDio\(\s*(?:\)|BaseOptions\((?![^;]*(?:connectTimeout|receiveTimeout)))|\bhttp\.(?:get|post|put|patch|delete|head|read)\((?![^;]*\.timeout\()' "${DA[@]}" "${X[@]}" "${ROOTS[@]}" | "${NC[@]}"
rg -n --pcre2 '\b(?:connect|read|write|call)Timeout\(\s*(?:0L?\s*,|Duration\.ZERO\b|0\.(?:seconds|milliseconds)\b)|\btimeoutIntervalFor(?:Request|Resource)\s*=\s*0\b' "${KT[@]}" "${SW[@]}" "${X[@]}" "${ROOTS[@]}" | "${NC[@]}"
rg -l --pcre2 '\bopenConnection\(\)|\bHttpClient\(' "${KT[@]}" "${X[@]}" "${ROOTS[@]}" | while IFS= read -r f; do rg -q --pcre2 'setConnectTimeout|setReadTimeout|connectTimeout\s*=|readTimeout\s*=|HttpTimeout|OkHttpClient' "$f" || echo "4d $f"; done
rg -n -U --pcre2 '\b(?:fetch\w*|\w*[aA]pi\.\w+)\([^;]*?\)\s*\.then\((?![^;]*\.catch\()' "${JS[@]}" "${X[@]}" "${ROOTS[@]}" | "${NC[@]}"

# 5. Deep-link payloads. 5a link params parsed with a throwing call; 5b Expo +native-intent with no try;
#    5c link entry points and routers with no redirect (read against auth hydration); 5d routed to security.
rg -n --pcre2 'getQueryParameter\([^)]*\)!!|getStringExtra\([^)]*\)!!|getQueryParameter\([^)]*\)\S*\.to(?:Int|Long|Double)\(\)|\bint\.parse\([^)]*(?:pathParameters|queryParameters)|(?:pathParameters|queryParameters)\[[^\]]+\]!|JSON\.parse\([^)]*(?:url|params|query|link)|\bInt\([^)]*(?:queryItems|url|components)[^)]*\)!|queryItems\?\.first\([^)]*\)\??!' -i "${X[@]}" "${ROOTS[@]}" | "${NC[@]}"
rg -l . -g '+native-intent.{js,jsx,ts,tsx}' "${X[@]}" "${ROOTS[@]}" | while IFS= read -r f; do rg -q '\btry\s*\{' "$f" || echo "5b $f"; done
rg -n --pcre2 '\bgetInitialURL\(|Linking\.addEventListener\(\s*["\x27]url|\buseURL\(|\.onOpenURL\b|openURLContexts|\bonNewIntent\(|\bgetInitialLink\(|\buriLinkStream\b' "${X[@]}" "${ROOTS[@]}" | "${NC[@]}"
rg -n -U --pcre2 '\bGoRouter\((?![^;]*\bredirect\s*:)' "${DA[@]}" "${X[@]}" "${ROOTS[@]}"
rg -n -U --multiline-dotall --pcre2 '<intent-filter(?![^>]*autoVerify="true")[^>]*>(?:(?!</intent-filter>).)*?android:scheme="https?"' "${MF[@]}" "${X[@]}" "${ROOTS[@]}"; rg -n -U --multiline-dotall --pcre2 '<intent-filter\b(?:(?!</intent-filter>).)*?\K<data\b[^>]*android:scheme="(?!https?")[^"]+"' "${MF[@]}" "${X[@]}" "${ROOTS[@]}"; rg -n --pcre2 '<key>CFBundleURLSchemes</key>|"scheme"\s*:' -g 'Info.plist' -g 'app.json' "${X[@]}" "${ROOTS[@]}"

# 6. Push. 6a roots with a push SDK and no token-refresh hook; 6b logout with no token delete; 6c tap handler with no
#    cold-start read; 6d RNFB background handler outside index; 6e no Android channel; 6f iOS delegate with no
#    willPresent / Expo with no handler; 6g aps-environment per entitlements file; 6h legacy FCM error codes.
for r in "${ROOTS[@]}"; do rg -q --pcre2 '^\s+firebase_messaging:|"(?:@react-native-firebase/messaging|expo-notifications)"\s*:' -g 'pubspec.yaml' -g 'package.json' "$r" || rg -q --pcre2 'FirebaseMessagingService|registerForRemoteNotifications\(' "${KT[@]}" "${SW[@]}" "${X[@]}" "$r" || continue
  rg -q --pcre2 'onNewToken|onTokenRefresh|addPushTokenListener|didReceiveRegistrationToken|didRegisterForRemoteNotificationsWithDeviceToken' "${X[@]}" "$r" || echo "6a $r: no token-refresh hook"
  rg -q --pcre2 'onNotificationOpenedApp|onMessageOpenedApp|addNotificationResponseReceivedListener' "${X[@]}" "$r" && ! rg -q --pcre2 'getInitialNotification|getInitialMessage|useLastNotificationResponse|getLastNotificationResponse' "${X[@]}" "$r" && echo "6c $r: tap handler with no cold-start read"
  rg -q --pcre2 '\bNotification(?:Compat)?\.Builder\(|expo-notifications|@notifee' "${X[@]}" "$r" && ! rg -q --pcre2 'createNotificationChannel|NotificationChannel(?:Compat)?\(|setNotificationChannelAsync|createChannel\(|AndroidNotificationChannel' "${X[@]}" "$r" && echo "6e $r: notifications posted, no channel created"
  rg -q '"expo-notifications"' -g 'package.json' "$r" && ! rg -q 'setNotificationHandler' "${X[@]}" "$r" && echo "6f $r: expo-notifications with no setNotificationHandler"
  rg -l -i --pcre2 '\b(?:fun|func|function|Future<void>|const|def)\s+(?:log_?out|sign_?out)\b' "${X[@]}" "$r" | while IFS= read -r f; do rg -q -i --pcre2 'deleteToken|unregisterForNotificationsAsync|unregisterForRemoteNotifications|DELETE[^\n]*(?:device|push)[-_]?token|remove(?:Device|Push)Token' "$f" || echo "6b $f"; done; done
rg -l 'setBackgroundMessageHandler' "${JS[@]}" -g '!index.{js,ts}' "${X[@]}" "${ROOTS[@]}"; rg -n --pcre2 'onBackgroundMessage\(\s*(?:\(|async\b|\w+\s*=>)' "${DA[@]}" "${X[@]}" "${ROOTS[@]}"
rg -l 'UNUserNotificationCenterDelegate' "${SW[@]}" "${X[@]}" "${ROOTS[@]}" | while IFS= read -r f; do rg -q 'willPresent' "$f" || echo "6f $f"; done; rg -n '\bshouldShowAlert\b' "${JS[@]}" "${X[@]}" "${ROOTS[@]}"
rg -n -A1 'aps-environment' -g '*.entitlements' "${ROOTS[@]}"; rg -n 'CODE_SIGN_ENTITLEMENTS' -g '*.pbxproj' "${ROOTS[@]}"
rg -n --pcre2 '\b(?:NotRegistered|InvalidRegistration|MismatchSenderId)\b|fcm\.googleapis\.com/fcm/send\b' "${X[@]}" .

# 7. OTA. 7a expo-updates with no runtimeVersion; 7b self-hosted updates with no code signing; 7c launch policy;
#    7d CodePush with no self-hosted server.
for r in "${ROOTS[@]}"; do rg -q '"expo-updates"' -g 'package.json' "$r" || continue; c=$(rg --files -g 'app.{json,config.js,config.ts}' "$r" | head -1)
  [ -n "$c" ] || { echo "7a $r: expo-updates, no app config"; continue; }
  rg -q 'runtimeVersion' "$c" || echo "7a $c: no runtimeVersion"
  rg -q --pcre2 '"url"\s*:\s*"https://(?!u\.expo\.dev)' "$c" && ! rg -q 'codeSigningCertificate' "$c" && echo "7b $c: self-hosted updates url, no codeSigningCertificate"
  rg -H -n --pcre2 '"checkAutomatically"\s*:\s*"(?:NEVER|ON_ERROR_RECOVERY)"|"fallbackToCacheTimeout"\s*:\s*[1-9]' "$c"; done
rg -n --pcre2 '\b(?:checkForUpdateAsync|fetchUpdateAsync|reloadAsync)\(' "${JS[@]}" "${X[@]}" "${ROOTS[@]}"
for r in "${ROOTS[@]}"; do rg -q '"react-native-code-push"' -g 'package.json' "$r" && ! rg -q --pcre2 'CodePushServerUrl|CodePushServerURL' "$r" && echo "7d $r: react-native-code-push, no self-hosted server URL"; done; rg --files -g 'shorebird.yaml' "${ROOTS[@]}"
```

A finding is a grep hit **plus** a read of the enclosing function or config block **plus** the version gate **plus** the effective config. Three blind spots are structural:

- **The merged manifest is not in the source tree.** Grep 2a/2b/3e read `src/main/AndroidManifest.xml`; a library can add a service, a receiver or `POST_NOTIFICATIONS`. When a build exists, read `**/build/intermediates/merged_manifests/**/AndroidManifest.xml` (git-ignored, so name the path explicitly) or `apkanalyzer manifest print app.apk`, and judge on that.
- **Wrappers hide the call.** Greps 4a–4c see the client at its construction; a shared `apiClient` built once with a timeout closes every call through it, and a hand-rolled `request()` that calls `fetch` without a signal opens all of them. Read the one client module before the call sites.
- **Indentation and statement scope are heuristics.** 1f needs `setState` on the line after the `await`; 2g needs `defineTask` indented. Read each Flutter `State` with an `await`, and each task file.

**Measured** (2026-10-05, ripgrep 15.2.0; bash 3.2 and zsh give the same hit set, with stdin piped or not). On the program's seeded multi-stack sample (bare RN 0.82, Expo SDK 57, Flutter 3.47, Kotlin + Compose at `targetSdk` 35, SwiftUI; 57 positives and 41 decoys across the seven classes) the script runs in under 1 s, surfaces every positive and no decoy; two printed lines are left to the read step (a Debug-only entitlements file, an OkHttp read timeout of 0 that may be a stream). On every web and server fixture in `benchmarks/fixtures/*` it finds no mobile root and prints `N/A` — without the root computation, the § 4 fetch grep fires on every web client; on `mobile-defects` (five mobile roots, measured 2026-10-10) it prints all 14 of its seeds in 74 lines — its `DEFECTS.md` § Detector measurement. On a read-only real Flutter app (1,167 files, 440 Dart) the first version printed 8 candidate lines, 7 false — a gen-l10n doc comment, a permanently-denied path named `permanentlyDenied` / `openSystemSettings`, two logout files in an app with no push SDK (the gate had matched a doc comment), three `<queries>` schemes. The exclusion of `app_localizations*.dart`, the comment filter on 1e, the wider settings vocabulary, the manifest-based push gate and the `<intent-filter>` scope fixed all seven; the one line left (`MaterialApp.router` with no `restorationScopeId`) is a true § 1 candidate.

## The 3,000-hit path

1. **Intersect** with reachability: a screen no navigator, route file or link config reaches is dismissed with one read; a whole module (a sample app, a design-system gallery, `tool/`) is dismissed with one read that shows nothing imports it, and named in the coverage block.
2. **Group** by (root cause, wrapper): one HTTP client with no timeout is one group however many calls use it; one base screen or `BaseViewModel` is one group.
3. **Rank** by user cost: payment, checkout, compose and sign-in flows first; then screens reached from links and pushes; then the rest. Field signals (Play vitals, Crashlytics, Sentry, Xcode Organizer) outrank code order when present.
4. **Read the top 30 groups fully.**
5. **Prefer the bulk device oracle at scale**: one Maestro flow per top screen (type → `pressKey: Home` → `killApp` → `launchApp: {stopApp: false}` → assert) settles § 1 for every group on that screen; one permissions-denied launch settles § 3 for the app.
6. **Ledger the rest** as `Live, unreviewed (k groups / n hits)` with the command that continues them. Never `checked`.

## Scans for

Severity assumes a release build and a reachable screen. Raise one step on payment, health or account flows; drop one when the screen is internal-only. **Critical** only with production evidence (a crash cluster, a store rejection).

| § | Class | Standard / lint id | Tier | Default |
|---|---|---|---|---|
| 1 | State lost on process death; restore crash; work outliving its owner | lint `RememberSaveableSaverParameter`, `RepeatOnLifecycleWrongUsage`; detekt `GlobalCoroutineUsage`; dart `use_build_context_synchronously` | D (I partial) | high on input or multi-step flows, else medium |
| 2 | Background work off the platform scheduler: FGS type, timeout, boot start, exact alarms, wake locks, BGTask ids | lint `ForegroundServiceType`, `ScheduleExactAlarm`, `Wakelock`, `WakelockTimeout` | A + D | high (crash or never runs) |
| 3 | Permissions: missing purpose string, launch wall, permanently-denied dead end, cached state, A13/A14 declarations | lint `NotificationPermission`, `SelectedPhotoAccess` | D | high (crash or dead end); medium otherwise |
| 4 | Network call with no timeout; network error with no handler | CWE-1088 | I | medium; high on checkout and sign-in |
| 5 | Deep-link payload that crashes or races auth at cold start | CWE-20 | D | high |
| 6 | Push: token not refreshed or not deleted, cold-start tap lost, background handler not invocable, no channel, silent foreground | — | D | high for wrong-account delivery, else medium |
| 7 | OTA: runtime mismatch, unsigned self-hosted updates, no self-heal, retired CodePush | CWE-494 (unsigned code) | D (A for config) | high; critical for unsigned from a self-hosted server |

### 1. Process death, restoration and owner-scoped work

```
BAD:   var query by remember { mutableStateOf("") }              class CheckoutViewModel : ViewModel() { val draft = MutableStateFlow("") }
       MaterialApp.router(routerConfig: r)                        final s = await api.status(); setState(() => status = s);
       @State private var draft = ""   // compose screen          lifecycleScope.launch { repo.updates.collect { … } }
GOOD:  var query by rememberSaveable { mutableStateOf("") }      class CheckoutViewModel(h: SavedStateHandle) : ViewModel()
       MaterialApp.router(restorationScopeId: 'app', …)           if (!mounted) return; setState(…)
       @SceneStorage("draft") var draft = ""                       repeatOnLifecycle(STARTED) { repo.updates.collect { … } }
```
**Read the code:** Is the state user input or a flow position (precedents § 11: transient UI state is not), or a cache re-read on restore (precedents § 12)? Does the screen sit behind a singleton (a session object, a DI `@Singleton`) that is null after process death, so the restored top screen crashes instead of recovering? On RN Android, does `MainActivity` install `RNScreensFragmentFactory` (precedents § 13)? Does an Android 16 tablet rotate a portrait-locked screen (orientation ignored at sw600dp, `targetSdk` 36)? **Finding when** user-visible state or a multi-step position is lost, or the restore path crashes, under background + `am kill`. **Severity:** high for typed input, checkout or compose; high for a crash on restore; medium for owner-scoped work (1f, 1h, 1i). **Proof:** the process-death restore (§ Proof), never force-stop, Don't keep activities or `recreate()` alone (precedents § 9–10).

### 2. Background work off the platform scheduler

```
BAD:   <service android:name=".SyncService" />  + startForeground(…)        // targetSdk ≥ 34: throws
       foregroundServiceType="dataSync", no onTimeout()                       // targetSdk ≥ 35: killed after the budget
       BOOT_COMPLETED receiver → startForegroundService(…)                   // targetSdk ≥ 35: dataSync start forbidden
       am.setExactAndAllowWhileIdle(…)  // no canScheduleExactAlarms()       lock.acquire()  // no timeout
       BGTaskScheduler.register(forTaskWithIdentifier: "com.acme.sync")      // not in BGTaskSchedulerPermittedIdentifiers
GOOD:  foregroundServiceType="dataSync" + FOREGROUND_SERVICE_DATA_SYNC + override fun onTimeout(…) { stopSelf() }
       WorkManager enqueueUniquePeriodicWork · if (am.canScheduleExactAlarms()) … else setAndAllowWhileIdle · acquire(10 * 60_000L)
```
**Read the code:** Read the **merged** manifest for the service's type and permission. Is the work user-initiated and visible (an FGS), or deferrable (WorkManager / `expo-background-task` / `BGProcessingTask`)? Is the BG identifier a constant or a `$(PRODUCT_BUNDLE_IDENTIFIER)` expansion the set-difference must resolve (precedents § 20)? Is registration complete before `didFinishLaunching` returns, and only once (a second register kills the app)? Flutter: is every background entry point top-level with `@pragma('vm:entry-point')` (precedents § 57)? Expo: `expo-background-fetch` is deprecated (precedents § 54) and `defineTask` must run at module scope. **Finding when** the gate's `targetSdk` (precedents § 52) is met and the work crashes, is killed, or never runs. **Severity:** high; medium for battery-only (an unbounded wake lock), raised when Play's excessive-wake-lock vital is at risk. **Proof:** tier A (merged manifest, `comm -3` set-difference) for the declaration, D for behaviour: `adb shell cmd jobscheduler run -f <pkg> <id>`, `dumpsys alarm`, `dumpsys power`, LLDB `_simulateLaunchForTaskWithIdentifier` on an iOS **device** (debug only).

### 3. Permissions

```
BAD:   AVCaptureDevice.requestAccess(…)  // no NSCameraUsageDescription in Info.plist, build settings or app config → crash
       useEffect(() => { PermissionsAndroid.request(CAMERA) }, [])  ·  Flutter: Permission.camera.request() in main()  ·  Kotlin: launcher.launch(CAMERA) in onCreate
       request(…) with no RESULTS.BLOCKED / canAskAgain / isPermanentlyDenied / openSettings path
       AsyncStorage.setItem('cameraPermissionGranted', …)            // stale after revoke, reset or auto-reset
GOOD:  request on the action that needs it; on permanently denied, explain and deep-link to Settings; re-check on every use
```
**Read the code:** Is the key supplied by `INFOPLIST_KEY_*` or an Expo config plugin (precedents § 24 — confirm in the prebuild output)? Is the request on a screen the user opened for that purpose (precedents § 23)? After two denials (Android 11+) or one (iOS), what does the user see — a dead button, a loop, a crash? Does the merged manifest declare `POST_NOTIFICATIONS` at `targetSdk` ≥ 33, and is it requested at runtime? At `targetSdk` ≥ 34 with `READ_MEDIA_IMAGES`, is `READ_MEDIA_VISUAL_USER_SELECTED` declared or the Photo Picker used? **Finding when** the feature crashes, loops or dead-ends on deny, deny-twice or a Settings revoke. **Severity:** high for a missing purpose string on a reachable path and for a dead end on a primary feature; medium for launch walls and cached state. **Proof:** D — Maestro `launchApp: {permissions: {all: deny}}`; `adb shell pm revoke <pkg> <perm>` (kills the process; relaunch must re-check) and `dumpsys package <pkg>` showing `USER_FIXED`; `xcrun simctl privacy booted revoke <service> <bundle>`.

### 4. Network call with no timeout, network error with no handler

```
BAD:   axios.create({ baseURL })         fetch(url)                      Dio(BaseOptions(baseUrl: u))       http.get(uri)
       OkHttpClient.Builder().readTimeout(0, SECONDS)                    config.timeoutIntervalForRequest = 0
       fetchCart().then(setCart)   // no .catch: the screen spins forever or shows stale data silently
GOOD:  axios.create({ baseURL, timeout: 15_000 })   fetch(url, { signal: AbortSignal.timeout(10_000) })
       Dio(BaseOptions(connectTimeout: …, receiveTimeout: …))   http.get(uri).timeout(const Duration(seconds: 10))
```
**Read the code:** Which client, and what is its default (precedents § 26): axios `timeout: 0`, dio null, Dart `http` none, and RN's Android networking client (`OkHttpClientProvider`) sets 0 — while OkHttp's own builder defaults to 10 s and `URLSession` to a 60 s idle timeout. Is the client built once in a wrapper that sets a timeout (then the call sites are covered)? Is a zero timeout on a streaming client bounded by a heartbeat or a call timeout? Does the screen render an error and a retry when the call fails (the rendered half is `ui-state-scan` § 3 / § 11 when ui-ux is installed)? **Finding when** a call that drives a screen or a write can wait forever, or its failure reaches no handler. **Severity:** medium; high on checkout, sign-in and sync. **Proof:** I — a test server (MSW, `MockWebServer` with `SocketPolicy.NO_RESPONSE`, a `URLProtocol` stub) that never answers; assert the call fails within the timeout and the error state renders.

### 5. Deep-link payloads that crash or race auth at cold start

```
BAD:   intent.data?.getQueryParameter("id")!!.toLong()       int.parse(state.pathParameters['id']!)
       JSON.parse(decodeURIComponent(url.split('?data=')[1]))  export function redirectSystemPath({ path }) { return new URL(path)… }  // throws
       Linking.getInitialURL().then(url => navigate(…))        // before the session store hydrates
GOOD:  getQueryParameter("id")?.toLongOrNull() ?: return showNotFound()   int.tryParse(…) ?? fallback
       try { … } catch { return '/' } in +native-intent          go_router redirect: + refreshListenable · Stack.Protected guard={signedIn}
```
**Read the code:** Is the parameter parsed with a throwing call (`!!`, `int.parse`, `JSON.parse`, `Int(…)!`) before any validation? Is the link handled before auth state is restored — does a logged-out cold link to an account screen land on sign-in, then the target? Does an Expo Router `+native-intent` `redirectSystemPath` ever throw (Expo's docs say it must not)? Does go_router have a `redirect` and `refreshListenable` when routes need a session? **Finding when** a malformed or out-of-order link crashes, or reaches an authed screen without a session. **Severity:** high. Grep 5d (an https filter with no `autoVerify`, custom schemes) is **routed**, not judged here (§ Boundaries). **Proof:** D — the matrix {cold, warm} × {logged out, logged in, expired} × {valid, malformed, foreign host}: `adb shell am start -W -a android.intent.action.VIEW -d "<url>" <pkg>` after a force-stop (a true cold start is correct **here**), `xcrun simctl openurl booted "<url>"`, Maestro `openLink`.

### 6. Push

```
BAD:   class PushService : FirebaseMessagingService() { /* no onNewToken */ }      logout(): clears storage, keeps the push token
       messaging().onNotificationOpenedApp(…)   // no getInitialNotification: a tap from a killed app is lost
       FirebaseMessaging.onBackgroundMessage((m) async { … })                      // anonymous: never runs in release
       NotificationCompat.Builder(this, "updates") with no channel created          // Android 8+: nothing shows
       UNUserNotificationCenterDelegate with no willPresent                         // iOS: silent in the foreground
GOOD:  onNewToken → upload · logout → deleteToken() + server DELETE · getInitialNotification + onNotificationOpenedApp
       @pragma('vm:entry-point') top-level handler · createNotificationChannel at start-up · willPresent → [.banner, .list]
```
**Read the code:** Is the token uploaded on every launch (precedents § 29 — that covers refresh)? Does logout unregister the device so account B never receives account A's notifications? Is `@notifee/react-native` present (archived; ≥ 7 swallows the RNFB tap APIs, § 55)? Does server-side send code prune tokens on FCM v1 `UNREGISTERED` (404), not only the legacy `NotRegistered` (precedents § 56)? Which build configuration signs with which `.entitlements` (`CODE_SIGN_ENTITLEMENTS` in the `.pbxproj`) — `aps-environment = development` in Release breaks TestFlight and App Store delivery. **Finding when** a notification is lost, silent, or delivered to the wrong account. **Severity:** high for wrong-account delivery and a lost cold-start tap; medium otherwise. **Proof:** D — the matrix {foreground, background, terminated, killed by the system} × {notification, data-only}; log out, then send to the old token and assert nothing shows; `xcrun simctl push booted <bundle> payload.apns`; `codesign -d --entitlements :- <app>` (A) for the environment.

### 7. OTA updates

```
BAD:   "updates": { "url": "https://updates.example.com/api/manifest", "checkAutomatically": "NEVER" }   // no runtimeVersion, no codeSigningCertificate
       "react-native-code-push": "…"  // service retired 2025-03-31, no CodePushServerURL
GOOD:  "runtimeVersion": { "policy": "fingerprint" } · "codeSigningCertificate" + "codeSigningMetadata" · ON_LOAD, or NEVER + an early checkForUpdateAsync
```
**Read the code:** Does the runtime version change whenever native code changes (the `fingerprint` policy, or a CI bump — precedents § 30)? Is the update server self-hosted, and are updates signed? With `NEVER`, is there an explicit early check — error recovery only rolls back failures in the first seconds after launch? Is `fallbackToCacheTimeout` > 0 blocking launch on the network outside a kiosk? **Finding when** an update can reach a binary that lacks its native code, run unsigned from a server the team does not control, or leave a crash with no recovery path. **Severity:** high; critical for unsigned updates from a self-hosted server. **Proof:** D — publish an update that calls a new native module to a build of the previous binary (it must not be offered under `fingerprint`); a tampered or wrongly signed update must be rejected; an update that throws at first render must roll back.

## Proof — the device oracles

The oracle shapes, per stack, and the whole-class variants a fix must survive are in [`proof-oracles.md`](../../../../snippets/proof-oracles.md) § Mobile; `device-harness` (this pack) boots the device and captures the evidence. The process-death recipe, because it is the one most often run wrong:

```bash
adb shell input keyevent KEYCODE_HOME          # background first: `am kill` is a no-op on a foreground app
adb shell am kill "<application.id>"            # system-style kill — NOT force-stop, NOT stopApp
adb shell ps -A | grep "<application.id>"      # must print nothing; otherwise the step is SKIPPED (kill did not land)
# relaunch from Recents (not the launcher icon), then assert the typed text / step / selection is back
```

iOS: background (`XCUIDevice.shared.press(.home)`), then stop the process from Xcode, relaunch from the home screen; `terminate()` + `launch()` is a cold start, not this test. Flutter adds `tester.restartAndRestore()` (I). Each oracle **fails before the fix**; a test that passes on the unfixed code proves nothing. No booted device: the row is `[report-flagged]`, Unconfirmed, with the exact flow written out — never PASS.

## Output

```
mobile-lifecycle-scan — lanes: expo SDK 57 / react-native 0.87 (expo-app/package.json), android targetSdk 35 (android-native/app/build.gradle.kts:5),
                         flutter 3.47 (flutter_app/pubspec.yaml); ios deployment target not set in the repo
Roots: 4 · CNG: expo-app (android/ ios/ not ignored — prebuilt)    Device: emulator-5554 (API 35); no iOS simulator → iOS rows Unconfirmed

Findings: 2 · Unconfirmed: 1

1. android-native/app/src/main/java/com/acme/notes/SearchScreen.kt:8          [report-with-fix]   high
   §1 state lost on process death — the search query is in `remember`, the checkout draft in a ViewModel with no
   SavedStateHandle (CheckoutViewModel.kt:7). Proof: maestro flows/search-restore.yaml — type, Home, killApp,
   launchApp {stopApp:false}: the query is gone (fails). Fix: rememberSaveable; SavedStateHandle.getStateFlow("draft", "").

2. android-native/app/src/main/java/com/acme/notes/Services.kt:21              [report-with-fix]   high
   §2 dataSync foreground service with no onTimeout — UploadService, targetSdk 35 (build.gradle.kts:5); merged manifest
   confirms foregroundServiceType="dataSync". Started from BootReceiver (Services.kt:39), which Android 15 forbids.
   Fix: override onTimeout(startId, fgsType) { stopSelf() }; move the boot path to WorkManager.

3. flutter_app/lib/push/background.dart:6                                          [report-flagged]    high
   §6 background handler not invocable in release — anonymous closure passed to onBackgroundMessage.
   Unproven link: no release build on a device. Settling run: release build, data-only high-priority send while terminated.
   Fix: a top-level function annotated @pragma('vm:entry-point').

Verification: 31 candidates → 2 findings · 1 unconfirmed · 4 hardening · 0 pre-existing · 24 refuted
Routed: §5d 3 rows → mobile-security-scan (security pack installed) · §4e 1 row → ui-state-scan §11

Class coverage:
  §1  process death / restoration      checked (9 hits → 1 finding)
  §2  background work                  checked (10 hits → 1 finding; PlayerService mediaPlayback is precedent § 18)
  §3  permissions                      checked (7 hits → 0 findings; 2 Unconfirmed folded into the iOS device gap)
  §4  timeouts / error handler         checked (8 hits / 3 groups → 0 findings; the shared client sets 15 s)
  §5  deep-link payloads               checked (6 hits → 0 findings) · 5d routed
  §6  push                             checked (10 hits → 1 unconfirmed)
  §7  OTA                              checked (3 hits → 0 findings: fingerprint runtime, signed updates, ON_LOAD)
```

`[report-with-fix]`: the trigger, the version gate and the effective config are cited, the oracle at the class's tier failed, and the fix is local. `[report-flagged]`: one link is unproven (no device, no merged manifest, a wrapper not read), and the row names it and the settling run. The coverage block lists **all seven** classes on every run: `checked (k hits → m findings)` only when the grep ran on a present lane; `N/A (<reason>)` only when the repo has no such surface; `blocked (<reason>)` when a grep failed or a file could not be read; `Live, unreviewed (k groups / n hits)` for a partial review.

## False positives / precedents

The verifier reads [`precedents/mobile.md`](../../../../snippets/precedents/mobile.md) and [`refute-before-report.md`](../../../../snippets/refute-before-report.md) § 4. The ones this skill meets most: force-stop, `stopApp`, swipe-away and `terminate()` are not process death (§ 9); transient UI state and repository caches (§ 11–12); the RN screens restoration fix (§ 13); special background access in the right app (§ 18); resolved BG constants (§ 20); requests in context and plugin-supplied purpose strings (§ 23–24); clients that already time out (§ 26); public links and once-only initial messages (§ 27–28); Debug-only entitlements and idempotent token uploads (§ 29); OTA policy choices (§ 30); every rule outside its `targetSdk` or version gate (§ 50–59).

## When to run

- On any diff that adds or changes a screen with input, a ViewModel or `State`, a service, receiver, alarm, job or BG task, a permission request, an HTTP client, a link handler or route config, push wiring, a logout path, or the update config — the `/mobile-audit` dispatch signal.
- On every whole-repo `/mobile-audit`, reporting all seven classes. `lane-mobile` (delivery pack, when installed) runs it on T2/T3 changes to the files above.
- When field signals show restore crashes, ANRs in services, `ForegroundServiceStartNotAllowedException`, or "notifications stopped" reports.

## Halt conditions

- Do not report a high row as confirmed until a verifier other than the run that found it has passed it through [`refute-before-report.md`](../../../../snippets/refute-before-report.md) with [`precedents/mobile.md`](../../../../snippets/precedents/mobile.md). Under `/mobile-audit` that happens in its verification phase; run standalone, apply the protocol as a separate second pass, tag those rows `self-verified`, and list the rest as Unconfirmed, Hardening, Pre-existing or Refuted. Never drop them.
- Halt on any finding without the `<file:line>`, the triggering OS event, the version-gate line and the fix.
- Do not mark a row `[report-with-fix]` without its oracle failing at the class's tier. No device or emulator → `SKIPPED` for the run's device rows and `[report-flagged]` for the finding — never PASS, and never a pass inferred from host tests.
- Do not use `am force-stop`, Maestro `stopApp`, Don't keep activities, `recreate()` or XCUITest `terminate()` as process-death proof; do not accept a kill whose process check still shows the process.
- Do not put a fix into git-ignored `ios/` or `android/` of an Expo CNG project; it belongs in app config or a config plugin.
- Do not judge a manifest class from the source manifest alone when a merged manifest or a build is available.
- Do not print "no lifecycle defect found" without the class-coverage block; a class whose grep did not run is `blocked`, never `checked`.
- Do not re-derive a class another skill owns (§ Boundaries). Route it.

## Related

- `/mobile-audit` dispatches this skill and folds its coverage block into the class ledger; `/mobile-fix` closes the findings failing-first on a device and re-runs this detector on the patched line.
- `device-harness` (this pack) runs the D-tier oracles; `@offline-sync-auditor` caps durability claims at `unproven` without a real kill.
- `mobile-perf-scan`, `offline-sync-scan`, `platform-conventions-audit`, `store-compliance-scan`, `native-bridge-audit` (this pack) own the neighbouring classes; `@app-store-reviewer` judges store gates.
- `mobile-security-scan` (security pack, when installed) owns link hijack, WebView, storage and transport; `ui-state-scan` (ui-ux pack, when installed) owns the rendered error and loading states.
- `ai-patterns/app-lifecycle.md`, `permissions.md`, `push-notifications.md`, `deep-linking.md`, `ota-updates.md` (this pack) hold the design guidance this detector checks against.
