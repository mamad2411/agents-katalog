---
name: mobile-security-scan
description: On-device security for Android, iOS, React Native and Flutter — storage, transport, IPC, links, WebViews, release flags, shipped secrets.
kind: skill
pack: security
allowed-tools: [Read, Grep, Glob, Bash]
---

# Skill: mobile-security-scan

## Premise

A mobile app ships its client to the attacker. Whatever the binary holds, whatever the sandbox stores, whatever the manifest exports and whatever a WebView bridges is reachable by someone the server never authenticates: **another app on the same device**, **a network attacker** on the same Wi-Fi, **whoever holds the shipped APK / IPA**, **a web page** the app loads, and, for the L2 classes, **someone holding the device or its backup**. The rest of this pack is server-centric — before this skill it had no client-side mobile lane at all. This skill is that lane: `/security-audit` dispatches it on any `android/`, `ios/`, React Native or Flutter tree, and on every whole-repo run.

**Every finding cites the config or code at `<file:line>` + the attacker capability it assumes + the concrete fix + a severity calibrated to its MASWE profile.** A grep hit is never a finding, and "no mobile issues" is never printed without the class-coverage block (§ Output). Third-party scanners do not cover this ground: mobsfscan reads Java, Kotlin, Android XML, Info.plist, Swift and Objective-C only — **no Dart, no JS/TS** (mobsfscan 1.0.1, 2026-09-21) — so React Native and Flutter app code is covered by the greps below or by nothing.

## The claim, restated for mobile

Before any gate of [`finding-verification.md`](../../../../snippets/finding-verification.md), write the candidate as one sentence (its § 1):

> **[A malicious app on the device · a network attacker with no trusted CA · whoever holds the APK/IPA · a page the WebView loads · someone holding the device or its backup]** uses **[the exported component, link, cleartext socket, bridge, file or string at file:line]** in a **release** build to gain **[the session, another user's data, a privileged native action, a server secret]**, because **[the control that is absent]**.

Gate 1 (reachability) means the **release** build: not under `__DEV__`, `kDebugMode`, `BuildConfig.DEBUG`, `#if DEBUG`, a `src/debug/` source set or a test target. Gate 3 (no effective control) is read on the **effective** config: the merged `AndroidManifest.xml` (libraries inject components and permissions), the signed entitlements, the Expo prebuild output. Gate 6 (environment) includes the platform defaults that already protect: cleartext is off by default from `targetSdk` 28, user-installed CAs are untrusted from 24, StrandHogg is moot at `minSdk` ≥ 30. The calibration the verifier applies is [`precedents/mobile.md`](../../../../snippets/precedents/mobile.md) § 42–48.

## Severity — this pack's scale, calibrated by MASWE profile

The pack's severities (critical / high / medium / low) and buckets (Finding / Unconfirmed / Hardening / Refuted) are unchanged. What moves a row between them is the OWASP MASWE profile of its weakness (MASWE repo, 2026-09-30; MASVS 2.1.0):

- **L1** — a defect for every app: data in logs (MASWE-0005), not excluded from backup (0006), hardcoded in the package (0004), stored outside private storage (0002), cleartext (0026), broken certificate validation (0027), deep links (0029), intents (0032), native functionality exposed to a WebView (0033), WebView local resources and untrusted content (0034, 0035).
- **L2 only** — **Hardening** unless the project declares an L2 posture (a threat model, security rule, ADR or README naming MASVS-L2 or the regime that demands it): a token in **app-private** plaintext storage (MASWE-0001), missing or misconfigured identity pinning (0028), screenshots and screen recording of sensitive screens (0038). Declared L2 → a Finding at medium (high for a refresh token or card data).
- **R (resilience)** — root / jailbreak detection, obfuscation, anti-tamper are **never a finding by their absence**; they appear only in the § 8 inventory. Debug artifacts and debuggable release builds (0061, 0063) are the exception the pack has always rated: a debuggable or debug-signed release is high.

## Boundaries

This skill does not re-derive classes another skill owns; it cross-links them:
- **Committed keystores, credentials across git history, rotation** → `secret-scan-method`. A key file in the tree printed by grep 6b is credited there; § 7 here owns what the **shipped app** carries. `EXPO_PUBLIC_*` names are also `xss-scan` § 12a's grep: one finding per key, credited to whichever run proved it in the bundle, the other listed as corroboration.
- **XSS inside the web content a WebView loads** → `xss-scan`. **Bridge exposure** (what that content can call natively) is § 5 here.
- **Server-side** `verify=False` / `rejectUnauthorized: false` in backend code, server log redaction → `injection-scan` / `data-exposure-scan`. Device logs (logcat, os_log, console in a release bundle) are § 6 here.
- **A link payload that crashes or races auth at cold start** (robustness) → `mobile-lifecycle-scan` § 5 when the mobile pack is installed; without it, report the crash here at low, tagged `robustness`. Link **hijack** and links reaching a WebView or a privileged screen are § 4 here.
- **Keychain items surviving uninstall** (no first-launch wipe) and cross-account residue at logout → `offline-sync-scan` § 5 when the mobile pack is installed; without it, § 1 reports the missing wipe as medium.
- **Store policy** (ATS justification for App Review, privacy manifest, target API) → `store-compliance-scan` when the mobile pack is installed. A store gate never gets a security severity, and a security finding never gets a store date.
- **New-Architecture bridge threading, native-module contracts** → `native-bridge-audit` (mobile pack). WebView bridges route here from it.

## Adapt to the codebase

Detect the lanes from the roots the pre-flight prints and run the matching rows; **print the lanes you ran** in the output header. Read versions (`targetSdk`, `react-native`, `expo`, `flutter_secure_storage`) from build and lock files before applying a version-gated rule ([`precedents/mobile.md`](../../../../snippets/precedents/mobile.md) § 50–59). Under **Expo CNG** (`android/` / `ios/` absent or git-ignored), a finding in a generated native file is re-located to `app.json` / `app.config.*` or a config plugin ([`precedents/mobile.md`](../../../../snippets/precedents/mobile.md) § 3).

| Lane | The truth to read | Secure store (the fix) | Transport config | IPC and link surface | WebView | What ships |
|---|---|---|---|---|---|---|
| **React Native** (bare) | merged manifest; `ios/*/Info.plist`; `babel.config.js` (console strip) | `react-native-keychain` 10, `expo-secure-store`, MMKV 4 with a Keystore-derived key | NSC + manifest; ATS | manifest components and filters; `Linking` | `react-native-webview` props: `originWhitelist`, `onMessage`, file flags | `index.android.bundle` / `main.jsbundle` (Hermes bytecode decompiles: hermes-dec) |
| **Expo** (SDK 53–57) | `app.json` / `app.config.*`, config plugins, the prebuild output | `expo-secure-store` (`keychainAccessible`) | `expo-build-properties` cleartext; ATS via `ios.infoPlist` | `scheme`, `intentFilters`, `associatedDomains` | as RN | `EXPO_PUBLIC_*` inlined; an EAS "secret" read by client code is public |
| **Flutter** | `android/app/src/main/AndroidManifest.xml`, merged manifest under `build/app/intermediates`; `ios/Runner/Info.plist` | `flutter_secure_storage` 11 (v11 removed `encryptedSharedPreferences`) | NSC, ATS; `badCertificateCallback` | manifest; `app_links` / go_router | `webview_flutter` `JavaScriptChannel`, `flutter_inappwebview` handlers | `libapp.so` (`String.fromEnvironment` compiled in); `flutter_dotenv` `.env` shipped as an asset |
| **Android** (Kotlin / Java) | `apkanalyzer manifest print`, `bundletool dump manifest` on the artifact; `res/xml/` | Android Keystore (`KeyGenParameterSpec`) + your own AES-GCM; `security-crypto` is deprecated (advisory only) | NSC `<base-config>`, `<domain-config>`, `<pin-set>` | exported components, `PendingIntent`, `FileProvider` paths | `addJavascriptInterface`, file / content access | dex (jadx), `BuildConfig`, `resValue` |
| **iOS** (Swift / ObjC) | `codesign -d --entitlements :-` on the signed app; `Info.plist`; `INFOPLIST_KEY_*` | Keychain, most restrictive `kSecAttrAccessible…ThisDeviceOnly` that works | ATS (`NSAppTransportSecurity`), `NSPinnedDomains` | `CFBundleURLSchemes`, universal links | `WKScriptMessageHandler`, `loadFileURL` read access | `Info.plist`, `xcconfig`, strings in the binary |

**Tools, as triage input only** — a hit is a candidate for the matching detector, judged by the same read. `mobsfscan --sarif -o mobsfscan.sarif <root>` (LGPL-3.0, invoked, never vendored; native code only). Android lint on the release variant (`./gradlew :app:lintRelease`, with `lintChecks("com.android.security.lint:lint:1.0.4")` for the security lints): ids `TrustAllX509TrustManager`, `BadHostnameVerifier`, `WebViewClientOnReceivedSslError`, `AddJavascriptInterface`, `ExportedReceiver`, `ExportedService`, `UnsafeIntentLaunch`, `MutableImplicitPendingIntent`, `HardcodedDebugMode`, `DataExtractionRules`, `PinSetExpiry`, `MissingBackupPin`. A rule CI already fails at error level is not re-reported ([`precedents/mobile.md`](../../../../snippets/precedents/mobile.md) § 4).

## Pre-flight greps

Run the block as **one** script from the repo root (shell state does not survive between tool calls). Grep **N** feeds detector **§ N**. Every `rg` names its path — `.`, a root, or `"${ROOTS[@]}"` — because `rg` with no path reads stdin when stdin is a pipe, and returns a silent zero under an agent's shell. `X` drops what never ships in a release build; `NC` drops comment-only lines; `DBG` drops lines behind a debug guard. A root with no manifest, plist or JS is a lane that is absent, not a clean result — say so in the coverage block.

```bash
# Mobile trees: RN/Expo package.json dirs, Flutter pubspec dirs, Android modules, Xcode projects; nested roots folded.
ROOTS=(); while IFS= read -r d; do ROOTS+=("$d"); done < <(
  { rg -l --pcre2 '"(?:react-native|expo)"\s*:' -g 'package.json' -g '!**/{node_modules,test,tests,fixtures,__fixtures__,e2e}/**' .
    rg -l --pcre2 '^\s+sdk:\s*flutter\b' -g 'pubspec.yaml' -g '!**/{.dart_tool,test,tests,fixtures,__fixtures__,e2e}/**' .
    rg --files -g '**/src/main/AndroidManifest.xml' -g '!**/{build,node_modules,.gradle,test,tests,fixtures,__fixtures__,e2e}/**' . | sed 's#/src/main/AndroidManifest\.xml$#/x#'
    rg --files -g '**/*.xcodeproj/project.pbxproj' -g '!**/{Pods,node_modules,DerivedData,test,tests,fixtures,__fixtures__,e2e}/**' . | sed 's#/[^/]*\.xcodeproj/project\.pbxproj$#/x#'
  } | while IFS= read -r f; do dirname "$f"; done | sort -u | awk 'p != "" && index($0, p "/") == 1 { next } { print; p = $0 }')
[ ${#ROOTS[@]} -gt 0 ] || { echo 'no mobile tree (android/, ios/, React Native, Flutter): every class N/A'; exit 0; }
# Never shipped in a release build: deps, build output, tests, debug source sets, generated code, docs.
X=(-g '!**/{node_modules,Pods,build,.gradle,.dart_tool,.expo,DerivedData,dist,vendor,.cxx}/**' -g '!**/src/{test,androidTest,debug}/**'
   -g '!**/{test,tests,__tests__,__mocks__,mocks,fixtures,__fixtures__,testdata,e2e,integration_test,.maestro,docs,ai}/**'
   -g '!**/*{Tests,UITests}/**' -g '!**/*.{test,spec,stories}.*' -g '!**/*_test.dart' -g '!**/*.{g,freezed,mocks}.dart' -g '!**/*.{md,mdx,lock,snap,map}')
NC=(rg -v --pcre2 '^[^:]+:\d+:\s*(//|/\*|\*(\s|/|$)|#(?!\{)|<!--)')
DBG=(rg -v --pcre2 '__DEV__|kDebugMode|BuildConfig\.DEBUG|#if\s+DEBUG|isDebuggable')
JS=(-g '*.{js,jsx,ts,tsx}'); KT=(-g '*.{kt,java}'); DA=(-g '*.dart'); SW=(-g '*.{swift,m,mm}'); SRC=(-g '*.{js,jsx,ts,tsx,kt,java,dart,swift,m,mm}')
S='(?:token|jwt|bearer|secret|passw(?:or)?d|passcode|\bpin\b|otp|session|cookie|credential|api_?key|private_?key|\bssn\b|iban|card_?number|cvv)'
printf 'root %s\n' "${ROOTS[@]}"
# Per root: the manifests that are the truth (the release merged manifest when a build left one, else every source
# main manifest), the Info.plists, and whether Expo regenerates the native folders (CNG: fixes go to app config).
AM=(); PL=()
for r in "${ROOTS[@]}"; do M=$(rg --files --no-ignore -g '**/intermediates/merged_manifests/release/**/AndroidManifest.xml' "$r" | head -1)
  if [ -n "$M" ]; then AM+=("$M"); echo "manifest $r: merged $M"; else
    while IFS= read -r f; do AM+=("$f"); echo "manifest $r: source $f"; done < <(rg --files -g '**/src/main/AndroidManifest.xml' "${X[@]}" "$r"); fi
  while IFS= read -r f; do PL+=("$f"); done < <(rg --files -g 'Info.plist' "${X[@]}" "$r")
  rg -q --pcre2 '"expo"\s*:' -g 'package.json' "$r" && for d in android ios; do [ -d "$r/$d" ] || echo "cng $r: $d/ absent — expo prebuild generates it; read app.json / app.config.* and config plugins"; done; done
NSC=(); while IFS= read -r f; do NSC+=("$f"); done < <(rg -l '<network-security-config' -g '*.xml' "${X[@]}" "${ROOTS[@]}")

# 1. Sensitive-named values written to plain stores (1a); MMKV with no key or a literal key, and Hive / Realm / Room /
#    sqflite / persisted state in a file that names a credential (1b); external or world-readable locations, file
#    protection off, Keychain classes readable while locked or migrating to a new device (1c); clipboard writes in files
#    with no sensitive-clip flag (1d); sensitive screens in a root with no capture guard anywhere (1e, L2).
rg -n -i --pcre2 "(?:AsyncStorage|\bstorage|mmkv|cache|prefs|preferences)\.(?:setItem|multiSet|mergeItem|set|setString|setStringList)\(\s*['\"\x60][^'\"\x60]*$S|put(?:String|StringSet)\(\s*\"[^\"]*$S|(?:string|byteArray)PreferencesKey\(\s*\"[^\"]*$S|(?:UserDefaults(?:\.standard|\(suiteName:[^)]*\))\.set\(|NSUbiquitousKeyValueStore|@AppStorage\(\s*\")[^\n]*$S" "${SRC[@]}" "${X[@]}" "${ROOTS[@]}" | "${NC[@]}"
rg -l -i --pcre2 "$S" "${SRC[@]}" "${X[@]}" "${ROOTS[@]}" | while IFS= read -r f; do rg -H -n --pcre2 'createMMKV\(\s*\)|createMMKV\(\{(?![^}]*encryptionKey)|new MMKV\(\s*(?:\{(?![^}]*encryptionKey)[^}]*\})?\s*\)|encryptionKey\s*:\s*[\x27"\x60]|Hive\.openBox(?:<[^>]*>)?\((?![^)]*encryptionCipher)|Realm\.Configuration\((?![^)]*encryptionKey)|Room\.databaseBuilder\(|\bopenDatabase\(|persistReducer\(|createJSONStorage\(' "$f"; done | "${NC[@]}"
rg -n --pcre2 'getExternal(?:FilesDir|StorageDirectory|StoragePublicDirectory|CacheDir)\(|MODE_WORLD_(?:READABLE|WRITEABLE)|setReadable\(true,\s*false\)|ExternalDirectoryPath|getExternalStorageDirector(?:y|ies)\(|getDownloadsDirectory\(|NSFileProtectionNone|FileProtectionType\.none|\.noFileProtection|kSecAttrAccessible(?:Always(?:ThisDeviceOnly)?|AfterFirstUnlock)\b|KeychainAccessibility\.first_unlock\b|\bAFTER_FIRST_UNLOCK\b' "${SRC[@]}" "${X[@]}" "${ROOTS[@]}" | "${NC[@]}"
rg -l --pcre2 'Clipboard\.(?:setString|setStringAsync|setData)\(|setPrimaryClip\(|UIPasteboard\.general\.(?:string\s*=|setValue|setItems|items\s*=)' "${SRC[@]}" "${X[@]}" "${ROOTS[@]}" | while IFS= read -r f; do
  rg -q --pcre2 'IS_SENSITIVE|\.localOnly|expirationDate' "$f" || rg -H -n --pcre2 'Clipboard\.(?:setString|setStringAsync|setData)\(|setPrimaryClip\(|UIPasteboard\.general\.' "$f"; done | "${NC[@]}"
for r in "${ROOTS[@]}"; do SC=$(rg --files "${SRC[@]}" "${X[@]}" "$r" | rg -i --pcre2 '(?:pin|otp|passcode|card|seed|wallet|recovery)[\w-]*(?:screen|view|page|activity|fragment|sheet)\.\w+$' | head -3 | tr '\n' ' ')
  [ -n "$SC" ] && ! rg -q --pcre2 'FLAG_SECURE|SecureFlagPolicy|setRecentsScreenshotEnabled|preventScreenCapture|usePreventScreenCapture|privacySensitive|screenguard|capture-protection|no_screenshot|screen_protector|flutter_windowmanager|ScreenProtector' "${SRC[@]}" "${X[@]}" "$r" && echo "1e $r: sensitive screens ($SC) and no capture protection in the root"; done

# 2. Cleartext and trust. 2a manifest cleartext; network-security-config cleartext (local hosts and <debug-overrides>
#    dropped) and user-installed CAs trusted; 2b ATS opened (inert when a sibling key is set — not printed); 2c code that
#    accepts any certificate or host; 2d http:// literals in shipped code.
[ ${#AM[@]} -eq 0 ] || rg -H -n 'android:usesCleartextTraffic="true"' "${AM[@]}"
rg -n --pcre2 '"?(?:usesCleartextTraffic|NSAllowsArbitraryLoads)"?\s*:\s*true' -g 'app.{json,config.js,config.ts}' "${X[@]}" "${ROOTS[@]}"
[ ${#NSC[@]} -eq 0 ] || perl -0777 -ne 's{<debug-overrides\b.*?</debug-overrides>}{ (my $m = $&) =~ s/[^\n]//g; $m }gse;
  while (/<(base-config|domain-config)\b([^>]*)>(.*?)<\/\1>/gs) { my ($t, $a, $b, $p) = ($1, $2, $3, $-[0]); my $l = 1 + (substr($_, 0, $p) =~ tr/\n//);
    my @d = $b =~ /<domain\b[^>]*>\s*([^<\s]+)/g; my $loc = @d && !grep { !/^(?:localhost|10\.0\.2\.2|127\.0\.0\.1)$/ } @d;
    print "$ARGV:$l: $t cleartextTrafficPermitted=true @d\n" if $a =~ /cleartextTrafficPermitted="true"/ && !$loc;
    print "$ARGV:$l: $t trusts user-installed CAs\n" if $b =~ /<certificates\s+src="user"/ }' "${NSC[@]}"
[ ${#PL[@]} -eq 0 ] || perl -0777 -ne 'next unless /<key>NSAppTransportSecurity<\/key>\s*<dict>(.*?)<\/dict>/s; my ($a, $p) = ($1, $-[1]); my $l = 1 + (substr($_, 0, $p) =~ tr/\n//);
  my $inert = $a =~ /<key>NSAllows(?:ArbitraryLoadsInWebContent|ArbitraryLoadsForMedia|LocalNetworking)<\/key>\s*<true\s*\/>/;
  print "$ARGV:$l: ATS NSAllowsArbitraryLoads=YES (global)\n" if $a =~ /<key>NSAllowsArbitraryLoads<\/key>\s*<true\s*\/>/ && !$inert;
  print "$ARGV:$l: ATS exception allows insecure HTTP\n" if $a =~ /<key>NS(?:ThirdParty)?ExceptionAllowsInsecureHTTPLoads<\/key>\s*<true\s*\/>/;
  print "$ARGV:$l: ATS exception allows TLS 1.0/1.1\n" if $a =~ /MinimumTLSVersion<\/key>\s*<string>TLSv1\.[01]</' "${PL[@]}"
rg -n --pcre2 'checkServerTrusted\([^)]*\)\s*(?::\s*Unit\s*)?(?:=\s*Unit|\{\s*\}|\{\s*return;?\s*\})|HostnameVerifier\s*\{\s*_?\w*\s*,\s*_?\w*\s*->\s*true|\bverify\([^)]*\)\s*(?::\s*Boolean\s*)?=\s*true|ALLOW_ALL_HOSTNAME_VERIFIER|NoopHostnameVerifier|SSLCertificateSocketFactory\.getInsecure|handler\??\.proceed\(\)|DisabledTrustEvaluator|DisabledEvaluator|allHostsMustBeEvaluated:\s*false|badCertificateCallback\s*=\s*\([^)]*\)\s*(?:=>\s*true|\{\s*return\s+true;?\s*\})|ServerTrustAuthResponseAction\.PROCEED|rejectUnauthorized\s*:\s*false' "${SRC[@]}" "${X[@]}" "${ROOTS[@]}" | "${NC[@]}"
rg -l --pcre2 '\.useCredential\s*,\s*URLCredential\(trust:' "${SW[@]}" "${X[@]}" "${ROOTS[@]}" | while IFS= read -r f; do rg -q 'SecTrustEvaluate' "$f" || rg -H -n 'useCredential' "$f"; done
rg -n --pcre2 '["\x27\x60]http://(?!localhost|127\.0\.0\.1|10\.0\.2\.2|0\.0\.0\.0|schemas\.android\.com|www\.w3\.org|www\.apple\.com|ns\.adobe\.com|xmlpull\.org)[\w.-]+' "${SRC[@]}" "${X[@]}" "${ROOTS[@]}" | "${NC[@]}" | "${DBG[@]}"

# 3. IPC. 3a components exported with no permission (launcher activities dropped — precedent § 46); 3b FileProvider and
#    grant paths over the root; 3c a received Intent relaunched (intent redirection); 3d PendingIntent with no IMMUTABLE
#    flag on the line; 3e runtime receivers registered with no exported flag.
[ ${#AM[@]} -eq 0 ] || perl -0777 -ne 'while (/<(activity|activity-alias|service|receiver|provider)\b([^>]*?)(?:\/>|>(.*?)<\/\1>)/gs) { my ($k, $a, $b, $p) = ($1, $2, $3 // "", $-[0]);
    next unless $a =~ /android:exported="true"/; next if $a =~ /android:(?:read|write)?[pP]ermission="/; next if $b =~ /category\.LAUNCHER/;
    my $l = 1 + (substr($_, 0, $p) =~ tr/\n//); my ($n) = $a =~ /android:name="([^"]+)"/; my @act = $b =~ /<action\s+android:name="([^"]+)"/g;
    print "$ARGV:$l: $k $n exported, no permission", (@act ? " (actions: @act)" : ""), ($b =~ /category\.BROWSABLE/ ? " — link entry, see 4" : ""), "\n" }' "${AM[@]}"
rg -n --pcre2 '<root-path\b|<(?:files|cache|external|external-files|external-cache|external-media)-path\b[^>]*\bpath="(?:\.|/|)"|<grant-uri-permission\b[^>]*android:path(?:Prefix)?="/"' -g '*.xml' "${X[@]}" "${ROOTS[@]}"
rg -l --pcre2 'getParcelableExtra|getParcelable<Intent>|IntentCompat\.getParcelableExtra|Intent\.parseUri\(' "${KT[@]}" "${X[@]}" "${ROOTS[@]}" | while IFS= read -r f; do rg -q --pcre2 '\b(?:startActivity|startActivities|startService|startForegroundService|sendBroadcast|setResult|bindService)\(' "$f" && rg -H -n --pcre2 'getParcelableExtra|getParcelable<Intent>|Intent\.parseUri\(|\b(?:startActivity|startService|sendBroadcast|setResult)\(' "$f"; done | "${NC[@]}"
rg -n --pcre2 'PendingIntent\.get(?:Activity|Activities|Service|Broadcast|ForegroundService)\((?![^;\n]*FLAG_IMMUTABLE)|registerReceiver\((?![^;\n]*RECEIVER_(?:NOT_)?EXPORTED)' "${KT[@]}" "${X[@]}" "${ROOTS[@]}" | "${NC[@]}"

# 4. Links. 4a https/http VIEW filters without autoVerify, and every custom scheme the app claims (manifest, Info.plist,
#    Expo config); 4b a custom scheme carrying a credential or an auth / reset / payment return; 4c link entry points.
[ ${#AM[@]} -eq 0 ] || perl -0777 -ne 'while (/<intent-filter\b([^>]*)>(.*?)<\/intent-filter>/gs) { my ($a, $b, $p) = ($1, $2, $-[0]); next unless $b =~ /action\.VIEW/ && $b =~ /category\.BROWSABLE/;
    my $l = 1 + (substr($_, 0, $p) =~ tr/\n//); my @s = $b =~ /android:scheme="([^"]+)"/g;
    print "$ARGV:$l: app link not verified (no autoVerify) @s\n" if grep({ /^https?$/ } @s) && $a !~ /autoVerify="true"/;
    my @c = grep { !/^https?$/ } @s; print "$ARGV:$l: custom scheme @c\n" if @c }' "${AM[@]}"
[ ${#PL[@]} -eq 0 ] || perl -0777 -ne 'while (/<key>CFBundleURLSchemes<\/key>\s*<array>(.*?)<\/array>/gs) { my ($b, $p) = ($1, $-[0]); my $l = 1 + (substr($_, 0, $p) =~ tr/\n//); my @s = $b =~ /<string>([^<]+)<\/string>/g; print "$ARGV:$l: custom scheme @s\n" }' "${PL[@]}"
rg -n --pcre2 '"scheme"\s*:\s*(?:"[^"]+"|\[)' -g 'app.{json,config.js,config.ts}' "${X[@]}" "${ROOTS[@]}"
SCH=$( { [ ${#AM[@]} -eq 0 ] || rg -o --no-filename --pcre2 'android:scheme="\K(?!https?")[^"$]+' "${AM[@]}"; [ ${#PL[@]} -eq 0 ] || perl -0777 -ne 'while (/<key>CFBundleURLSchemes<\/key>\s*<array>(.*?)<\/array>/gs) { print "$_\n" for $1 =~ /<string>([^<\$]+)<\/string>/g }' "${PL[@]}"
  rg -o --no-filename --pcre2 '"scheme"\s*:\s*"\K[^"]+' -g 'app.{json,config.js,config.ts}' "${X[@]}" "${ROOTS[@]}"; } | sort -u | paste -sd '|' -)
[ -z "$SCH" ] || rg -n -i --pcre2 "\b(?:$SCH)://[^\s'\"\x60]*(?:auth|oauth|callback|redirect|login|signin|token|code|reset|verify|magic|pay|checkout|session)" "${SRC[@]}" -g '*.{json,plist,xml}' "${X[@]}" "${ROOTS[@]}" | "${NC[@]}"
rg -n --pcre2 '\bgetInitialURL\(|Linking\.addEventListener\(\s*["\x27]url|\buseURL\(|\bgetInitialLink\(|\buriLinkStream\b|\.onOpenURL\b|openURLContexts|application\(_[^)]*open url:|\bonNewIntent\(|getIntent\(\)\.getData\(|\bintent\??\.data\b' "${SRC[@]}" "${X[@]}" "${ROOTS[@]}" | "${NC[@]}"

# 5. WebViews. 5a native bridges, file / universal access, debugging, a URL loaded from an Intent; 5b RN WebViews that
#    expose a bridge (onMessage / injectedJavaScript) — every risky prop in those files; 5c WKScriptMessageHandlers with
#    no frame-origin check.
rg -n --pcre2 'addJavascriptInterface\(|setAllowFileAccess(?:FromFileURLs)?\(\s*true|setAllowUniversalAccessFromFileURLs\(\s*true|allow(?:FileAccess|FileAccessFromFileURLs|UniversalAccessFromFileURLs|ContentAccess)\s*=\s*true|setAllowContentAccess\(\s*true|setWebContentsDebuggingEnabled\(\s*true|loadUrl\([^)\n]*(?:getStringExtra|getQueryParameter|intent\b|\.data\b)|isInspectable\s*=\s*true|\bUIWebView\b|addJavaScriptChannel\(|JavascriptChannel\(|addJavaScriptHandler\(|allow(?:FileAccessFromFileURLs|UniversalAccessFromFileURLs):\s*true' "${SRC[@]}" "${X[@]}" "${ROOTS[@]}" | "${NC[@]}"
rg -l --pcre2 'react-native-webview' "${JS[@]}" "${X[@]}" "${ROOTS[@]}" | while IFS= read -r f; do rg -q --pcre2 'onMessage=|injectedJavaScript' "$f" || continue
  rg -q 'nativeEvent\.url' "$f" || echo "$f: onMessage acts with no nativeEvent.url check"
  rg -H -n --pcre2 'originWhitelist=\{\[\s*["\x27]\*["\x27]\s*\]\}|allow(?:FileAccess|FileAccessFromFileURLs|UniversalAccessFromFileURLs)=\{true\}|mixedContentMode=["\x27](?:always|compatibility)|webviewDebuggingEnabled=\{true\}|setSupportMultipleWindows=\{false\}|injectedJavaScript(?:BeforeContentLoaded)?=|onMessage=|source=\{\{\s*uri:\s*(?![\x27"\x60]https://)' "$f"; done
rg -l --pcre2 'WKScriptMessageHandler|didReceive message:|addScriptMessageHandler|\.add\(self,\s*name:' "${SW[@]}" "${X[@]}" "${ROOTS[@]}" | while IFS= read -r f; do rg -q --pcre2 'frameInfo|securityOrigin' "$f" || rg -H -n --pcre2 'didReceive message:' "$f"; done

# 6. Release config. 6a debuggable, and backup left on with no extraction rules (a rules file is printed to read);
#    6b release signed with the debug key, debuggable or unminified release, literal store passwords, committed keys;
#    6c get-task-allow in an entitlements file; 6d credentials in device logs and wire loggers outside a debug guard.
[ ${#AM[@]} -eq 0 ] || perl -0777 -ne 'next unless /<application\b([^>]*)>/s; my ($a, $p) = ($1, $-[0]); my $l = 1 + (substr($_, 0, $p) =~ tr/\n//);
  print "$ARGV:$l: android:debuggable=true\n" if $a =~ /android:debuggable="true"/; next if $a =~ /android:allowBackup="false"/;
  my ($r) = $a =~ /android:(?:dataExtractionRules|fullBackupContent)="([^"]+)"/;
  print "$ARGV:$l: backup ", ($a =~ /allowBackup="true"/ ? "on" : "on by default"), ($r ? " — rules $r: read for sharedpref/database/file includes" : ", no extraction rules — the whole sandbox is backed up"), "\n"' "${AM[@]}"
rg -n -U --pcre2 '\brelease\s*\{[^}]*?\b(?:signingConfig\s*=?\s*signingConfigs\.(?:getByName\(\s*"debug"\s*\)|debug)\b|isDebuggable\s*=\s*true|debuggable\s+true|minifyEnabled\s+(?:false|enableProguardInReleaseBuilds)|isMinifyEnabled\s*=\s*false)' -g '*.gradle*' "${X[@]}" "${ROOTS[@]}"
rg -n --pcre2 '(?:storePassword|keyPassword)\s*=?\s*\(?\s*["\x27](?!android["\x27])[^"\x27$]+["\x27]|^\s*(?:\w+_)?(?:STORE|KEY)_PASSWORD\s*=\s*\S' -g '*.gradle*' -g 'gradle.properties' -g 'local.properties' "${X[@]}" "${ROOTS[@]}"
rg --files -g '*.{jks,keystore,p12,p8,mobileprovision}' -g '!**/debug.keystore' "${X[@]}" "${ROOTS[@]}" | sed 's/$/: key material in the tree (secret-scan-method owns rotation)/'
rg -n -U --pcre2 '<key>get-task-allow</key>\s*<true\s*/>' -g '*.entitlements' "${X[@]}" "${ROOTS[@]}"
{ rg -n -i --pcre2 "console\.(?:log|info|debug|warn|error)\([^\n]*$S" "${JS[@]}" "${X[@]}" "${ROOTS[@]}"
  rg -n -i --pcre2 "\b(?:Log\.[vdiwe]|Timber\.[vdiwe]|println)\([^\n]*$S" "${KT[@]}" "${X[@]}" "${ROOTS[@]}"
  rg -n -i --pcre2 "\b(?:print|NSLog|debugPrint|os_log)\([^\n]*$S|privacy:\s*\.public" "${SW[@]}" "${X[@]}" "${ROOTS[@]}"
  rg -n -i --pcre2 "\b(?:print|debugPrint|log)\([^\n]*$S" "${DA[@]}" "${X[@]}" "${ROOTS[@]}"
  rg -n --pcre2 'HttpLoggingInterceptor\.Level\.(?:BODY|HEADERS)|LogInterceptor\([^)\n]*(?:requestHeader|requestBody|responseBody):\s*true|\bredux-logger\b|\breactotron\b' "${SRC[@]}" "${X[@]}" "${ROOTS[@]}"; } | "${NC[@]}" | "${DBG[@]}"
for r in "${ROOTS[@]}"; do rg -q --pcre2 '"react-native"\s*:' -g 'package.json' "$r" || continue
  rg -q 'transform-remove-console' -g 'babel.config.*' -g '.babelrc*' "$r" || echo "6d $r: console.* reaches the device log in release (no transform-remove-console)"; done

# 7. Secrets and crypto. 7a key shapes in shipped source and config (Firebase config files listed apart — precedent
#    § 44); 7b secret-named build-time values compiled into the app, and .env shipped as an asset; 7c broken crypto and
#    literal keys; 7d a non-cryptographic RNG in a file that mints OTPs, nonces, salts or tokens; 7e the shipped artifact.
rg -n --hidden --no-ignore --pcre2 '\b(?:sk_live_[0-9A-Za-z]{16,}|rk_live_[0-9A-Za-z]{16,}|AKIA[0-9A-Z]{16}|AIza[0-9A-Za-z_\-]{35}|xox[baprs]-[\w-]{10,}|ghp_[0-9A-Za-z]{30,}|sk-(?:ant|proj)-[\w-]{20,})|-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----' -g '!google-services.json' -g '!GoogleService-Info.plist' -g '!.git/**' "${X[@]}" "${ROOTS[@]}"
rg --files --hidden -g 'google-services.json' -g 'GoogleService-Info.plist' "${X[@]}" "${ROOTS[@]}" | sed 's/$/: Firebase config — a project identifier, not a secret (precedent § 44); check API-key restrictions/'
rg -n --pcre2 'buildConfigField\s*\(?\s*["\x27]String["\x27]\s*,\s*["\x27]\w*(?:SECRET|PRIVATE|PASSWORD|TOKEN|API_?KEY)|String\.fromEnvironment\(\s*["\x27]\w*(?:SECRET|PRIVATE|PASSWORD|TOKEN|KEY)|\bConfig\.\w*(?:SECRET|PRIVATE|PASSWORD)\w*|EXPO_PUBLIC_\w*(?:SECRET|PRIVATE|SERVICE_?ROLE|ADMIN|PASSWORD|SIGNING|WEBHOOK)|<key>\w*(?:Secret|SECRET|Password|PASSWORD|PrivateKey)\w*</key>' "${SRC[@]}" -g '*.{plist,xcconfig,gradle,kts,json}' -g '.env*' --hidden "${X[@]}" "${ROOTS[@]}" | "${NC[@]}"
rg -n --pcre2 '^\s*-\s*(?:\./)?(?:[\w/]*/)?\.env[\w.]*\s*$' -g 'pubspec.yaml' "${ROOTS[@]}"
rg -n --pcre2 'Cipher\.getInstance\(\s*"(?:AES|DES|DESede|RC4|Blowfish|[^"]*/ECB/[^"]*)"|SecretKeySpec\(\s*"|IvParameterSpec\(\s*(?:"|byteArrayOf|ByteArray\(\d)|MessageDigest\.getInstance\(\s*"(?:MD5|SHA-?1)"|\bInsecure\.(?:MD5|SHA1)\b|kCCOptionECBMode|\bCC_MD5\(|AESMode\.ecb|IV\.fromLength\(' "${SRC[@]}" "${X[@]}" "${ROOTS[@]}" | "${NC[@]}"
rg -l -i --pcre2 'otp|nonce|salt|secret|passw|token|verifier|\biv\b|\bpin\b' "${SRC[@]}" "${X[@]}" "${ROOTS[@]}" | while IFS= read -r f; do rg -H -n --pcre2 'Math\.random\(\)|\bnew Random\(|java\.util\.Random\b|kotlin\.random\.Random\b|(?<![.\w])Random\.next\w+\(|(?<![.\w])Random\(\)(?!\.secure)|(?<![.\w])Random\(\d+\)' "$f"; done | "${NC[@]}"
rg --files --no-ignore -g '*.{apk,aab,ipa}' -g 'index.android.bundle' -g 'main.jsbundle' -g 'libapp.so' -g '!**/node_modules/**' "${ROOTS[@]}" | head -5 | while IFS= read -r a; do
  case "$a" in *.apk|*.aab|*.ipa) H=$(unzip -p "$a" 2>/dev/null | strings -n 12 | rg -c --pcre2 'sk_live_|AKIA[0-9A-Z]{16}|PRIVATE KEY-----|EXPO_PUBLIC_\w*SECRET') ;; *) H=$(strings -n 12 "$a" | rg -c --pcre2 'sk_live_|AKIA[0-9A-Z]{16}|PRIVATE KEY-----|EXPO_PUBLIC_\w*SECRET') ;; esac
  echo "7e $a: ${H:-0} secret-shaped strings in the artifact"; done

# 8. Pinning and resilience posture (inventory, not findings). 8a every pin-set (pins, expiry); 8b pinning code per root;
#    8c root / jailbreak / integrity checks per root; 8d a declared MASVS L2 posture anywhere in the repo's docs.
[ ${#NSC[@]} -eq 0 ] || TODAY=$(date +%F) perl -0777 -ne 'while (/<pin-set\b([^>]*)>(.*?)<\/pin-set>/gs) { my ($a, $b, $p) = ($1, $2, $-[0]); my $l = 1 + (substr($_, 0, $p) =~ tr/\n//);
    my $n = () = $b =~ /<pin\b/g; my ($e) = $a =~ /expiration="([^"]+)"/;
    print "$ARGV:$l: pin-set $n pin(s), ", (!$e ? "no expiration" : $e lt $ENV{TODAY} ? "EXPIRED $e — pinning is off" : "expires $e"), ($n < 2 ? ", no backup pin" : ""), "\n" }' "${NSC[@]}"
for r in "${ROOTS[@]}"; do P=$(rg -l --pcre2 'CertificatePinner|<pin-set|NSPinnedDomains|TrustKit|react-native-ssl-(?:public-key-)?pinning|SecurityContext\(\s*withTrustedRoots:\s*false|setTrustedCertificatesBytes|http_certificate_pinning|PinnedCertificatesTrustEvaluator|PublicKeysTrustEvaluator' "${SRC[@]}" -g '*.{xml,plist,json,yaml}' "${X[@]}" "$r" | head -3 | tr '\n' ' ')
  I=$(rg -l --pcre2 'RootBeer|JailMonkey|jail-monkey|flutter_jailbreak_detection|safe_device|IOSSecuritySuite|freerasp|IntegrityManager|PlayIntegrity|DCAppAttestService|DCDevice\b' "${SRC[@]}" -g '{package.json,pubspec.yaml,Podfile}' -g '*.{gradle,kts}' "${X[@]}" "$r" | head -3 | tr '\n' ' ')
  echo "8 $r: pinning ${P:-none} · integrity checks ${I:-none}"; done
L2=$(rg -l -i --pcre2 '\bMASVS\b|\bMASWE\b|\bMAS-?L2\b|\bPCI[ -]DSS\b|\bHIPAA\b' -g '{ai,docs}/**/*.md' -g 'README*' -g 'SECURITY*' -g '.claude/rules/*.md' -g '!**/node_modules/**' . | head -3 | tr '\n' ' ')
if [ -n "$L2" ]; then echo "8d posture: read ${L2}for a declared L2 profile"; else echo "8d posture: none declared — L1, so L2-only classes are Hardening"; fi
```

A finding is a grep hit **plus** a read of the enclosing component or config **plus** the attacker's path to it. Two blind spots are structural:
- **Wrappers hide the key.** `store.write(key, value)` in a key-value wrapper never shows the literal key to grep 1a; list the wrapper's callers once and read which keys reach the plaintext backend.
- **Source manifests lie.** A library injects exported components the source never declares, and Expo plugins write the real manifest at prebuild. With no merged manifest the pre-flight reads source manifests and says so (`manifest <root>: source …`); every § 3 / § 4 / § 6 row is then `[report-flagged]` until `apkanalyzer manifest print app.apk` or the merged manifest confirms it.

## The 3,000-hit path

1. **Intersect** with the release build: drop debug, test, sample and gallery modules with one read that shows nothing in the release variant includes them (`settings.gradle*`, the scheme's targets, the app's imports); name each in the coverage block.
2. **Group** by root cause: one storage wrapper, one HTTP client factory, one base WebView, one manifest placeholder is one group however many call sites use it.
3. **Rank** by attacker capability × asset: another-app and network classes over a credential first (§ 2, § 3, § 4, § 5); shipped secrets (§ 7); then L2 and posture rows.
4. **Read the top 30 groups fully**; prove the top 5 on the artifact (tier A) or a device (tier D).
5. **Ledger the rest** as `Live, unreviewed (k groups / n hits)` with the command that continues them. Never `checked`.

## Scans for

Default severity assumes a release build, a credential or user data at stake, and the attacker capability the row names. Drop one step when the asset is non-sensitive; never drop an L1 class to "info".

| § | Class | MASVS · MASWE | CWE | Attacker | Default |
|---|---|---|---|---|---|
| 1 | Credential in plain storage, external or migrating stores; clipboard; sensitive screens | STORAGE · 0001 (L2), 0002, 0030, 0038 (L2) | CWE-312, CWE-922 | device / backup holder | Hardening (L2) · high outside private storage |
| 2 | Cleartext traffic, user CAs trusted, broken certificate or hostname validation | NETWORK · 0026, 0027 | CWE-319, CWE-295 | network | critical (trust-all) · high (cleartext credential) · medium (ATS / NSC opened) |
| 3 | Exported component without permission, intent redirection, mutable implicit `PendingIntent`, FileProvider over-scope | PLATFORM · 0032 | CWE-926, CWE-927 | another app | high |
| 4 | Deep-link and App Link hijack: unverified https links, custom schemes carrying credentials or returns | PLATFORM · 0029 | CWE-939 | another app / a web page | high |
| 5 | WebView: native bridge reachable by untrusted content, file / universal access, debugging | PLATFORM · 0033–0035 | CWE-749 | a web page | critical (bridge to a token or payment) |
| 6 | Release config: debuggable, debug-signed, backup on with no rules, `get-task-allow`, credentials in device logs | STORAGE · 0005, 0006 · R 0061, 0063 | CWE-489, CWE-530, CWE-532 | device / backup holder | high |
| 7 | Server secrets and keys shipped in the app; broken crypto; non-cryptographic RNG for secrets | STORAGE · 0004 · CRYPTO | CWE-798, CWE-321, CWE-327, CWE-338 | APK / IPA holder | critical (server secret) · high (literal key, ECB) |
| 8 | Pinning and resilience posture — inventory, findings only on misconfiguration | NETWORK-2 · 0028 (L2) · RESILIENCE | CWE-295 | network | Hardening; medium for an expired pin set once L2 |

### 1. Credential in plain storage, external locations, clipboard, sensitive screens

```
BAD:   AsyncStorage.setItem('refreshToken', t)   prefs.setString('access_token', t)   UserDefaults.standard.set(token, forKey: "authToken")
       createMMKV({ id: 'auth' })   kSecAttrAccessibleAlways   getExternalFilesDir(null) + token file   Clipboard.setString(otp)
GOOD:  SecureStore.setItemAsync('refreshToken', t, { keychainAccessible: WHEN_UNLOCKED_THIS_DEVICE_ONLY })
       FlutterSecureStorage().write(...)   Keychain kSecAttrAccessibleWhenUnlockedThisDeviceOnly   MMKV keyed from the Keystore
       ClipDescription.EXTRA_IS_SENSITIVE (API 33+) · UIPasteboard setItems(_:options: [.localOnly: true, .expirationDate: …])
```
**Read the code:** Is the value sensitive by **value**, not just by name (`tokenExpiryShown` is not a token)? Where does the store live — app-private (L2), or external storage, a world-readable mode, a backup-included file, iCloud key-value sync (`NSUbiquitousKeyValueStore`), an App Group (L1)? Is MMKV keyed, and does the key come from the Keystore / Keychain or from a literal in the bundle (§ 7)? Does redux-persist / zustand `persist` include the auth slice (`whitelist` / `partialize`)? A Keychain class of `AfterFirstUnlock` (not `ThisDeviceOnly`) migrates to a new device through encrypted backups — is that a recorded decision (handset replacement) or an accident? Is the clipboard value an OTP, card number or seed phrase? **Finding when** a credential reaches a non-private location (L1), or app-private plaintext on a declared-L2 project. **Severity:** high outside private storage; Hardening for private storage on L1 (medium / high once L2); `AfterFirstUnlock` without `ThisDeviceOnly` for a token medium on L2, Hardening with a recorded reason; EncryptedSharedPreferences is a deprecation advisory, never a vuln ([`precedents/mobile.md`](../../../../snippets/precedents/mobile.md) § 42). Grep 1e (no capture guard on PIN / card / seed screens) is L2 — Hardening on L1, and never on non-sensitive screens (§ 47). **Proof:** A — [`exploit-payloads.md`](../../../../snippets/exploit-payloads.md) § Mobile M5 (read the seeded canary token out of `shared_prefs/`, `RKStorage`, the simulator container) and M4 when the store is backup-included.

### 2. Cleartext traffic and broken certificate validation

```
BAD:   android:usesCleartextTraffic="true"   <base-config> <certificates src="user"/>   NSAllowsArbitraryLoads = YES
       override fun checkServerTrusted(...) {}   handler?.proceed()   badCertificateCallback = (c, h, p) => true
       completionHandler(.useCredential, URLCredential(trust: trust))   // no SecTrustEvaluateWithError first
GOOD:  no cleartext outside a debug-only config scoped to 10.0.2.2 / localhost; user CAs only inside <debug-overrides>
       a TrustManager that DELEGATES to the platform default; SecTrustEvaluateWithError before .useCredential
       per-domain NSExceptionDomains with a reason, never the global switch
```
**Read the code:** Is the trust-all path reachable in release, or behind a staging flavor the release variant excludes? Does a cleartext flag carry real traffic (an `http://` literal from grep 2d, an `http` base URL in config)? Is `NSAllowsArbitraryLoads` inert — `…InWebContent`, `…ForMedia` or `NSAllowsLocalNetworking` present (iOS 10+, precedent § 45)? Does the NSC's cleartext `<domain-config>` cover only local hosts? **Finding when** release traffic can be read or impersonated by a network attacker. **Severity:** critical for trust-all / hostname-allow-all / SSL-error proceed / `badCertificateCallback => true` (MASWE-0027, L1); high for cleartext carrying a credential; medium for a global ATS or NSC opening with no observed HTTP use (and an App Review justification, `store-compliance-scan`'s); medium for user CAs in `<base-config>`. **Proof:** D — [`exploit-payloads.md`](../../../../snippets/exploit-payloads.md) § Mobile M6: mitmproxy with **no** CA installed; a correct app fails the handshake, a trust-all app's flows appear.

### 3. Exported components, intent redirection, PendingIntent, FileProvider

```
BAD:   <receiver android:name=".TokenReceiver" android:exported="true"> (no permission; onReceive writes the session)
       val next = intent.getParcelableExtra<Intent>("next"); startActivity(next)   // relaunches the caller's Intent
       PendingIntent.getActivity(ctx, 0, Intent("com.acme.OPEN"), FLAG_MUTABLE)    <root-path name="r" path="."/>
GOOD:  android:exported="false", or a permission with android:protectionLevel="signature"
       validate the nested Intent: resolveActivity() inside the app's own package and not exported, strip URI grant flags
       FLAG_IMMUTABLE on an explicit Intent; FileProvider paths scoped to one directory
```
**Read the code:** What does the component do with its input — write auth state, start another component, return a result, open a file? Is the permission `signature`-level (a `normal` permission any app can request is no control)? For a receiver filtering a protected system broadcast (`BOOT_COMPLETED`), does `onReceive` check the action (an explicit Intent from another app bypasses the filter)? Is the mutable `PendingIntent` explicit (RemoteInput, bubbles — legitimate, § 46)? **Finding when** another app on the device can drive an auth-sensitive action, reach a non-exported component through redirection, or read files through a provider. **Severity:** high; critical when it yields the session or arbitrary file read. The launcher activity is required and is not printed; StrandHogg is moot at `minSdk` ≥ 30 (§ 46). **Proof:** D — [`exploit-payloads.md`](../../../../snippets/exploit-payloads.md) § Mobile M1 (`am start` / `am broadcast` / `content query` with a canary, and a test APK that nests an Intent).

### 4. Deep-link and App Link hijack

```
BAD:   <intent-filter> VIEW + BROWSABLE + https, no android:autoVerify="true"     // any app can claim the link; a chooser appears
       onLoginLink('acmeshop://login?token=…') → signInWithToken(token)            // any app can register acmeshop://
GOOD:  autoVerify="true" + assetlinks.json listing the Play App Signing SHA-256; iOS applinks: + an AASA served raw over HTTPS
       magic-link, reset and payment returns on verified https links; OAuth on a custom scheme only with PKCE (RFC 8252)
```
**Read the code:** What does the link carry — a one-time sign-in token, a reset token, an OAuth `code`, a payment result? Is the custom scheme unique to this app, or a word another app can claim? For OAuth, is PKCE on (an intercepted `code` is useless without the verifier — then Hardening)? Does a link reach a privileged screen without a session, a WebView (`source={{ uri: params.url }}`) or `openURL` with a foreign host? **Finding when** another app or a web page can receive a credential meant for this app, or drive an authenticated action through a link. **Severity:** high for credential-bearing links on a custom or unverified scheme; medium for an unverified https filter whose links carry no credential; a marketing "open the app" scheme is not a finding (§ 27). **Proof:** D — [`exploit-payloads.md`](../../../../snippets/exploit-payloads.md) § Mobile M2 (a second test app claiming the scheme receives the canary token; `pm get-app-links` shows the domain unverified).

### 5. WebView bridges and file access

```
BAD:   view.addJavascriptInterface(NotesBridge(token), "NotesApp"); view.loadUrl(intent.getStringExtra("url"))
       <WebView originWhitelist={['*']} source={{ uri: checkoutUrl }} onMessage={e => confirmPayment(JSON.parse(e.nativeEvent.data))} />
       addJavaScriptChannel('Wallet', onMessageReceived: …runJavaScript("receiveToken('$token')"))   didReceive message: → Payments.confirm
GOOD:  load only bundled HTML or an allow-listed first-party origin, enforced in shouldOverrideUrlLoading / onShouldStartLoadWithRequest;
       check nativeEvent.url / message.frameInfo.securityOrigin before acting; never pass a token into page JS
```
**Read the code:** Which origins can the WebView load — a fixed first-party URL, or one from a link, an Intent extra or an API field? What can the bridge do — read a token, pay, open a URL, read files? Does the handler check the origin (`nativeEvent.url`, `frameInfo.securityOrigin`, `isMainFrame`)? Are `allowFileAccessFromFileURLs` / `allowUniversalAccessFromFileURLs` on while untrusted content can load? Is `setSupportMultipleWindows={false}` set (re-exposes CVE-2020-6506)? **Finding when** content an attacker controls can call a native action or read local files. **Severity:** critical for a bridge exposing a token or a payment; high for file or universal access with untrusted content; medium for debugging enabled in release. A static `source={{ html }}` WebView with no bridge is not printed. **Proof:** D — [`exploit-payloads.md`](../../../../snippets/exploit-payloads.md) § Mobile M3 (a page from a host the test controls calls the bridge with a nonce).

### 6. Release config, backup and device logs

```
BAD:   release { signingConfig signingConfigs.debug }   android:debuggable="true"   <application> with no allowBackup / dataExtractionRules
       <key>get-task-allow</key><true/> in the App Store entitlements   console.log('session saved', accessToken) with no console strip
       Log.d(TAG, "token=$token")   print("refresh token stored: \(token)")   HttpLoggingInterceptor.Level.BODY outside a debug guard
GOOD:  a release signingConfig read from CI secrets; debuggable left to the build type, never set in the manifest
       android:allowBackup="false", or dataExtractionRules (API 31+) and fullBackupContent (≤ 30) that exclude the token and database files
       get-task-allow only in the Debug configuration's entitlements; transform-remove-console in release; wire loggers at NONE unless BuildConfig.DEBUG
```
**Read the code:** Is the line in the **release** variant — the merged manifest under `intermediates/merged_manifests/release`, the `release` build type, the entitlements file the Release configuration names (`CODE_SIGN_ENTITLEMENTS` per configuration in the `.pbxproj`, the reading of [`precedents/mobile.md`](../../../../snippets/precedents/mobile.md) § 29)? Is the RN template's `debug.keystore` used by `debug` only, or does `release` point at it (§ 48)? With backup on, what does the sandbox hold — a token in prefs or a database (§ 1), or only caches? Does a rules file exclude those paths in **both** `<cloud-backup>` and `<device-transfer>`, and in `fullBackupContent` for API ≤ 30? Is a log call compiled out — `transform-remove-console` in `babel.config.*`, R8 `-assumenosideeffects` on `android.util.Log`, a `kReleaseMode` / `#if DEBUG` guard? Does the logged value carry the secret, or only its name (`'token refreshed'`)? Is a `privacy: .public` interpolation a credential? **Finding when** a release build is debuggable or debug-signed, its backup carries a credential, the distribution entitlements allow a debugger to attach, or a credential reaches the device log in release. **Severity:** high for a debuggable or debug-signed release (MASWE-0061 / 0063 — the R exception) and for a credential or a `BODY` wire log in release logs (MASWE-0005, L1); high for backup on with a credential in the backed-up sandbox (MASWE-0006, L1), medium when it holds user data but no credential; medium for `get-task-allow` true in the distribution entitlements (the provisioning profile can override the file — prove it on the signed app); a literal store password beside a committed keystore is `secret-scan-method`'s. Minify off is the R profile: an § 8 inventory line, and `app-size-scan`'s shrinking row when the mobile pack is installed. **Proof:** A — [`exploit-payloads.md`](../../../../snippets/exploit-payloads.md) § Mobile M8 (`apkanalyzer manifest debuggable`, `apksigner verify --print-certs`, `codesign -d --entitlements :-` on the signed artifact); D — M4 (a seeded canary survives backup → reinstall → restore) and M5 (the canary in `adb logcat --pid` or the simulator log stream).

### 7. Server secrets shipped in the app, broken crypto, weak randomness

```
BAD:   EXPO_PUBLIC_STRIPE_SECRET_KEY=sk_live_…   GenerativeModel(apiKey: 'AIza…')   String.fromEnvironment('PAYMENT_SECRET')
       pubspec.yaml assets: [.env]   buildConfigField "String", "ADMIN_TOKEN", "\"…\""   SecretKeySpec("0123456789abcdef".toByteArray(), "AES")
       Cipher.getInstance("AES/ECB/PKCS5Padding")   java.util.Random().nextInt(1_000_000) for an OTP   Math.random() for a nonce
GOOD:  the secret stays on a server the app calls with the user's session; the client holds publishable keys and ids only
       AES-GCM under a Keystore / Keychain key with a fresh random IV
       SecureRandom · crypto.getRandomValues / expo-crypto · Random.secure() · SecRandomCopyBytes
```
**Read the code:** Is the value a **server** secret — Stripe `sk_live_`, an AWS key pair, a database URL with a password, a signing key, a Gemini Developer API key — or a publishable value or project identifier (Firebase `AIza…`, `pk_live_`, a Supabase anon key behind RLS, a Sentry DSN, an OAuth client id; [`precedents/mobile.md`](../../../../snippets/precedents/mobile.md) § 44)? Does client code read it? Any `EXPO_PUBLIC_*` read by dot access, any `--dart-define` read by `String.fromEnvironment`, and any `.env` declared as a Flutter asset is in the artifact, whatever its EAS visibility. For crypto: what does the cipher protect, and where does the key come from — a literal (CWE-321) or the Keystore / Keychain? Is the RNG output a secret (OTP, nonce, salt, token, IV) or a UI value (a shuffle, a retry jitter)? **Finding when** a server secret is in the shipped app, data is encrypted under a key the app ships, ECB or a static IV protects a secret, or a secret comes from a non-cryptographic RNG. **Severity:** critical for a server secret in the bundle or binary (MASWE-0004, CWE-798); high for a literal key or ECB over a credential (CWE-321, CWE-327); high for an OTP, nonce or token from `Math.random` / `java.util.Random` / Dart `Random()` (CWE-338), medium when the value only de-duplicates requests. A Firebase config file is a line to check API-key restrictions and App Check, never a secret. One finding per key: the same `sk_live_` printed by greps 7a and 7b, by `secret-scan-method` and by `xss-scan` § 12a is one row (§ Boundaries). 7e reads a built artifact when one is in the tree; none → the bundle proof is `blocked`, not `checked`. **Proof:** A — [`exploit-payloads.md`](../../../../snippets/exploit-payloads.md) § Mobile M7: build the release artifact with a canary in the variable (`EXPO_PUBLIC_…=canary-<uuid>`) and find the canary in the bundle (`strings`; `hbc-decompiler` for a Hermes bundle; `libapp.so` for Flutter). Rotating a real key that already shipped is `secret-scan-method`'s.

### 8. Pinning and resilience posture — inventory

```
BAD:   <pin-set expiration="2025-06-30"> with one pin, past its date      // fail-open: pinning is silently off
       a pin set or CertificatePinner with no backup pin                    // a key rotation breaks every installed client
GOOD:  no pinning on an L1 app (Android's guidance discourages it); or ≥ 2 SPKI pins, one outside the current chain,
       an expiration a release cycle ahead with an alert before it; NSPinnedDomains / TrustKit / CertificatePinner with a backup pin
```
**Read the code:** Which hosts does 8b's pinning cover, per root? Is a `<pin-set>` expired — then pinning is **absent** and is reported as absent ([`precedents/mobile.md`](../../../../snippets/precedents/mobile.md) § 43)? Does every pin set carry a backup pin? Does the project declare L2 — grep 8d prints the docs that might; a passing mention of MASVS is not a declared posture. Root / jailbreak / integrity checks (8c) and obfuscation are inventory: never a finding by their absence, and a check that only warns is not a control a § 1–7 claim may lean on. **Finding when** — only on misconfiguration: a declared-L2 project with no pinning on its auth host, an expired pin set the team believes active (a doc or comment says the app pins), or a pin set with no backup pin. **Severity:** Hardening on L1; medium on a declared L2; never above medium. **Proof:** A / D — [`exploit-payloads.md`](../../../../snippets/exploit-payloads.md) § Mobile M6: compare each pin with the server's SPKI hash; on the owner's test device, a debug build whose `<debug-overrides>` trusts the proxy CA without `overridePins` must fail the handshake to a pinned host — flows appearing mean the pin is not enforced.

## Output

```
mobile-security-scan — lanes: react-native (rn-app, source manifest), android (android-native/app, merged release manifest),
                       flutter (flutter_app), ios (ios-app); expo absent · posture: L1 (no L2 declaration found)

Findings: 3

1. flutter_app/lib/net/http_client.dart:4                              [report-with-fix]  critical
   §2 trust-all — badCertificateCallback returns true for every certificate; buildClient() is the app's only
   HTTP client and is not behind kDebugMode. Attacker: a network attacker with no trusted CA. Fix: delete the
   callback; trust the staging CA through a debug-only SecurityContext. Proof D: § Mobile M6 (no CA installed,
   the canary request appears in the proxy). MASVS-NETWORK · MASWE-0027 · CWE-295

2. rn-app/android/app/src/main/AndroidManifest.xml:27                  [report-with-fix]  high
   §3 exported receiver — .sec.TokenReceiver is exported with no permission and writes the "session" extra
   into prefs as session_token (TokenReceiver.kt:9–10). Attacker: another app on the device sets the user's
   session. Fix: android:exported="false" (nothing outside the app sends it). Proof D: § Mobile M1 — a
   broadcast to the debug build carries a canary, run-as reads it back. MASVS-PLATFORM · MASWE-0032 · CWE-926

3. rn-app/src/auth/signInLink.ts:5                                     [report-flagged]  high
   §4 credential on a custom scheme — acmeshop://login?token=… signs the user in; any app can register
   acmeshop://. Unproven link: whether sign-in emails use the custom scheme (the mail template is not in this
   repo). Fix: send sign-in links on a verified https App Link / universal link; one-time, short-lived token.
   MASVS-PLATFORM · MASWE-0029 · CWE-939

Hardening: rn-app/src/sec/session.ts:8 refresh token in AsyncStorage (app-private, L2 — § 1, precedent § 42) ·
  rn-app/src/sec/oauth.ts:4 OAuth on a custom scheme with PKCE on (§ 4) · android-native res/xml/network_config.xml:14
  pin set expired 2025-06-30, so pinning is absent (§ 8, L1)
Refuted: android-native/app/src/main/java/com/acme/notes/perf/Leaks.kt:32 (3e: receiver for a protected system broadcast)

Class coverage:
  §1 storage, clipboard, screens   checked (6 hits → 0 findings, 1 Hardening)
  §2 transport and trust           checked (3 hits → 1 finding)
  §3 IPC                           checked (4 hits → 1 finding, 1 Refuted)
  §4 links                         checked (5 hits → 1 finding, 1 Hardening)
  §5 WebView                       checked (2 hits → 0 findings: bundled HTML; onMessage checks nativeEvent.url)
  §6 release config, logs          checked (5 hits → 0 findings: every log line behind __DEV__ or stripped)
  §7 shipped secrets, crypto       checked (3 hits → 0 findings: Firebase config, pk_live_) · 7e blocked (no release artifact; build one or read CI's)
  §8 pinning and resilience        inventory (android-native: expired pin set, RootBeer; other roots: none) · posture L1
```

`[report-with-fix]` — the attacker's path, the effective config and the release reachability are read end to end, and the fix is concrete. `[report-flagged]` — the config or code is unsafe but one link is unproven (a merged manifest not built, a backend template not in the repo, a provisioning profile that may override the file); the row names that link. The class-coverage block lists **all eight** classes on every run: `checked (k hits → m findings)` only when the class's grep ran on a lane that is present, `N/A (<reason>)` when no root carries the surface (no manifest, no WebView dependency), `blocked (<reason>)` when the grep could not run or the effective config could not be read. A source-manifest run says so in the header. No mobile root at all prints one line — `no mobile tree: every class N/A` — and nothing else.

## False positives / gotchas

The calibration is [`precedents/mobile.md`](../../../../snippets/precedents/mobile.md) § 42–48; a match makes a row Hardening and the precedent's flip evidence makes it a candidate again.
- **Secure stores and private storage** (§ 42): Keychain, expo-secure-store, react-native-keychain, flutter_secure_storage and Keystore-keyed MMKV are the fix, not a hit. App-private plaintext is L2 — Hardening on L1. EncryptedSharedPreferences is a deprecation advisory. `AsyncStorage.setItem('theme', …)` never prints; `tokenExpiryShown` prints and is refuted on read.
- **Pinning** (§ 43): no pinning on L1 is not a finding; an expired pin set is reported as absent, never as present.
- **Not secrets** (§ 44): Firebase `AIza…` keys and config files, `pk_live_`, a Supabase anon key behind RLS, a Sentry DSN, OAuth client ids. The flip: a Gemini Developer API key is critical, and anything client code reads is public whatever its EAS visibility.
- **Transport exemptions** (§ 45): `NSAllowsArbitraryLoads` beside `…InWebContent` / `…ForMedia` / `NSAllowsLocalNetworking` is inert and the perl block does not print it; cleartext to `10.0.2.2` / `localhost` and user CAs inside `<debug-overrides>` are dropped before printing. A `src/debug/AndroidManifest.xml` cleartext flag is excluded by `X`.
- **IPC exemptions** (§ 46): the launcher activity, a `signature` permission, a mutable `PendingIntent` on an explicit Intent for RemoteInput or bubbles; StrandHogg at `minSdk` ≥ 30. A runtime receiver that listens only to protected system broadcasts needs no exported flag (3e prints it; the read refutes it).
- **Capture guards** (§ 47): `FLAG_SECURE` / `.privacySensitive` only on PIN, card, seed-phrase and OTP screens. Grep 1e names the screens it matched; a root with a guard anywhere is not printed — read whether the guard covers the printed screen.
- **The RN `debug.keystore`** (§ 48) with password `android` is fine unless the release `signingConfig` uses it; grep 6b drops the `android` password literal.
- **Debug-only entitlements and configs**: `get-task-allow` or `aps-environment = development` in a file only the Debug configuration names (the reading of § 29); a staging trust-all class only a staging flavor compiles — read the source sets.
- **Marketing schemes** (§ 27): a custom scheme that opens a public screen carries no credential; grep 4b keys on auth, reset and payment words, so `acmedriver://promo/spring` never prints.
- **A static WebView** (`source={{ html }}`, bundled HTML, no `onMessage` / `injectedJavaScript`) is not printed even with `originWhitelist={['*']}`.
- **Expo CNG** (§ 3): a finding in a generated `android/` / `ios/` is re-located to `app.json` / `app.config.*` or a config plugin; the pre-flight prints a `cng` line per absent folder. **CI-failing lints** (§ 4) are not re-reported.
- **Measured** (2026-10-05, ripgrep 15.2.0, bash 3.2 and zsh, stdin piped or not — identical sets): on a seeded six-root mobile sample (bare RN, two Expo apps, Flutter, Kotlin, Swift) the script prints 85 lines; every seeded defect surfaces, and no decoy prints except lines handed to the read step by design — a PKCE-protected OAuth redirect, the scheme and link-entry inventory (4a, 4c), a system-broadcast receiver (3e), a WebView whose `onMessage` only logs, and the two Firebase config files labelled with § 44. Run from the repo root it prints the single N/A line (its root computation excludes `fixtures/`); run inside `benchmarks/fixtures/mobile-defects/` it prints 46 lines covering that fixture's 12 security seeds.

## When to run

- On any diff touching `AndroidManifest.xml`, a `network_security_config`, `Info.plist`, an `.entitlements` file, `app.json` / `app.config.*`, a Gradle build type or signing config, a storage, HTTP-client, WebView, deep-link or crypto call in mobile code, an `EXPO_PUBLIC_*` / `--dart-define` / `.env` value — the `/security-audit` dispatch signal.
- On every whole-repo `/security-audit` with an `android/`, `ios/`, React Native, Expo or Flutter tree, reporting all eight classes; a repo with none prints the N/A line.
- Before a store release: §§ 6–7 against the release artifact itself (M7, M8), not only the source.

## Halt conditions

- Do not report a critical or high row as confirmed until a verifier other than the run that found it has passed it through [`finding-verification.md`](../../../../snippets/finding-verification.md). Under `/security-audit` that happens in Phase 4; run standalone, it applies the protocol as a separate second pass, tags those rows `self-verified`, and lists the rest as Unconfirmed, Hardening or Refuted — never drops them.
- Halt on any finding without the config or code `<file:line>` + the attacker capability + the concrete fix + a severity on the MASWE profile (§ Severity).
- Do not report a grep hit as a finding. Every row is a hit **plus** a read of the enclosing component or config **plus** the attacker's path to it in a release build.
- Do not rate an § 3 / § 4 / § 6 row `[report-with-fix]` from a source manifest alone; it stays `[report-flagged]` until the merged manifest or the artifact confirms it.
- Do not report an L2 or resilience class above Hardening on a project that declares no L2 posture.
- Proofs run only on the owner's own debug or test build, on an emulator or a test device the owner controls, with seeded canary values ([`exploit-payloads.md`](../../../../snippets/exploit-payloads.md) § Mobile). No booted device → the D-tier proof is `SKIPPED` and the row stays Unconfirmed with the settling command, never confirmed.
- Do not print "no mobile issues" without the class-coverage block; a class whose grep did not run is `blocked`, never `checked`.
- Do not re-derive a class another skill owns (§ Boundaries) — cross-link it.

## Related

- `/security-audit` — dispatches here on any `android/`, `ios/`, React Native, Expo or Flutter tree and on every whole-repo run, and folds this skill's class-coverage block into its class ledger; `/security-fix` closes the findings.
- `@auth-reviewer` — token lifecycle and session design; this skill reports where the token is stored and transported on the device.
- `@data-privacy-reviewer` — PII flow to analytics and third parties; device logs and backups are § 6 here.
- `secret-scan-method` — committed keystores, credentials across history, rotation. `xss-scan` § 12a — `EXPO_PUBLIC_*` in a web build. `injection-scan`, `data-exposure-scan` — the server-side counterparts (§ Boundaries).
- Mobile pack, when installed: `mobile-lifecycle-scan` § 5 (link payload robustness), `offline-sync-scan` § 5 (identity bleed, Keychain wipe), `store-compliance-scan` (ATS justification, privacy manifest, target API), `native-bridge-audit` § 7 (routes WebView bridges here), `app-size-scan` (shrinking). Without it, the robustness and wipe rows are reported here as § Boundaries says.
- [`precedents/mobile.md`](../../../../snippets/precedents/mobile.md) § 42–48 (calibration), § 50–59 (version gates); [`exploit-payloads.md`](../../../../snippets/exploit-payloads.md) § Mobile M1–M8 (confirmation steps on the owner's own build).
