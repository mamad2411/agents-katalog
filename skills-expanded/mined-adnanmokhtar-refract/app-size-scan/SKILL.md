---
name: app-size-scan
description: Find what makes an RN/Expo, Flutter, iOS or Android release bigger than it needs to be — shrinking off, emulator ABIs, oversized or unused assets, heavy imports, debug payload, unused deps, APK uploads — each proved by a release-artifact size delta.
kind: skill
pack: mobile
allowed-tools: [Read, Grep, Glob, Bash]
---

# Skill: app-size-scan

Renamed from the mobile pack's `bundle-analyze` (1.x): the frontend pack ships a skill of that name, and a project with both packs installed got the second one as `bundle-analyze.mobile` while dispatchers asked for the bare name.

## Premise

App size is paid on every install and every update, on the slowest connection the product reaches, and since Play's 2026 vitals it is also paid in store visibility: R8 off leaves DEX unoptimized, and the DEX-optimization and memory vitals carry store-visibility impact from February 2027 (developer.android.com *Android vitals*, updated 2026-09-21, research catalog). Size grows by **class of mistake** — shrinking off, every ABI shipped to every device, a 3x asset where a vector would do, a whole library imported for one function — so a class found once is swept everywhere.

**Every finding cites the config or code `<file:line>` + the release artifact it inflates (AAB / APK / IPA / JS or Dart bundle) + the measured size before and after on the same artifact type, or the command that would measure it + the fix.** No saving is stated that was not measured; "est. saving" from a hunch is the failure this skill exists to prevent. "Size is fine" is never printed without the class-coverage block (§ Output).

## Halt conditions (read first)

- Refuse to report a size from a debug or dev build — source maps, dev tooling and no shrinking make it fiction. Release (or profile for Flutter `--analyze-size`) only.
- Refuse to claim a saving without the before → after delta on the **same** artifact type (per-device AAB download size, never a universal APK against an AAB).
- Halt if the analyzer or the release build failed — fix the build first; there is no partial size of a binary that does not exist.
- Do not propose removing a dependency or an asset without reading its use sites (§ 6's set-difference is a candidate list, not a verdict).
- Do not re-derive the 16 KB page-size gate or a store size limit: `store-compliance-scan` § 7 (this pack) owns the dated gate; `/optimize-bundle` § the published-limits table owns the store caps.
- Do not report a high row as confirmed until a verifier other than the run that found it has passed it through [`refute-before-report.md`](../../../../snippets/refute-before-report.md) with [`precedents/mobile.md`](../../../../snippets/precedents/mobile.md); standalone, apply it as a separate pass and tag those rows `self-verified`. Never drop a candidate.
- Do not print "size is fine" without the class-coverage block; a class whose grep did not run is `blocked`, never `checked`.

## Boundaries

- Startup cost of eager imports and `inlineRequires: false` → `mobile-perf-scan` § 6; the same `import _ from 'lodash'` line is credited to both and deduped by `<file:line>` (that skill owns milliseconds, this one owns bytes).
- 16 KB native alignment, target-API dates, store size caps → `store-compliance-scan` § 7 and `@app-store-reviewer` (this pack).
- Cold start as a measured cost → `@device-performance-auditor`, which consumes this skill's size number and never produces one.
- Applying the reductions → `/optimize-bundle` (this pack), which runs this skill for the measurement.
- Shipped secrets, debuggable release builds, signing → `mobile-security-scan` when the security pack is installed.

## Measure — the toolchain table

**One toolchain table, shared with `/optimize-bundle`**, which runs this skill rather than keeping a list of its own.

| Stack | Release artifact | Composition command | Notes |
|---|---|---|---|
| Expo | `eas build` / `npx --no expo export` | `EXPO_ATLAS=true npx --no expo export`, then `npx --no expo-atlas .expo/atlas.jsonl` (expo-atlas 0.4.3; docs.expo.dev *analyzing bundles*, read 2026-10-05) | Atlas shows the JS bundle per module and per platform |
| React Native (Metro) | `index.android.bundle` / `main.jsbundle` from a release build | `npx --no react-native-bundle-visualizer` (4.0.0) · `npx --no source-map-explorer <bundle> <bundle>.map` | Hermes compiles to bytecode (the default engine; Hermes V1 from 0.84): measure the `.hbc` the release ships |
| Flutter | `flutter build appbundle` / `ipa` | `flutter build appbundle --analyze-size` (APK needs `--target-platform`) → the `*-code-size-analysis_*.json` for DevTools' App Size tool (docs.flutter.dev *app size*, read 2026-10-05) | release only; `--split-debug-info=<dir>` moves symbols out of the binary |
| Android | `./gradlew :app:bundleRelease` (AAB) | Android Studio *Analyze APK*; `bundletool get-size total --apks=<app>.apks` for per-device download size [K] | AGP 9.3 replaced `isMinifyEnabled` / `isShrinkResources` with `optimization { enable = true }`; AGP 9.0 dropped `proguard-android.txt` (developer.android.com *enable app optimization*, updated 2026-08-27) |
| iOS | Archive → `.ipa` | App Thinning Size Report: Organizer → Distribute, or `xcodebuild -exportArchive` with `thinning` in the export options [K: not runnable on this host] | `xcrun altool` uploads and validates; it produces **no** size analysis — never cite it as a measurement. Periphery 3.8.0 finds dead Swift |
| Assets | the files themselves | `cwebp` / `pngquant` / `ImageOptim`; `ffprobe` for video | the only number that belongs in a report is the measured before → after for these files |

## Adapt to the codebase — lanes

Read grep 0 first: the AGP version decides which shrink DSL is current, the RN version which engine is default, Expo CNG whether native config lives in `app.json` (`expo-build-properties`) or in `android/`. A fix written into the git-ignored native folders of an Expo CNG project is lost at the next prebuild ([`precedents/mobile.md`](../../../../snippets/precedents/mobile.md) § 3).

## Pre-flight greps

Run as **one** script from the repo root. Grep **N** feeds detector **§N**; grep 0 is context. Lines tagged `1`, `2`, `3a`–`3c`, `6` are file-level or set-difference results; the rest are grep hits. Any `rg` error on stderr is a failed grep, never zero hits.

```bash
# Mobile roots (same computation as the other mobile detectors).
ROOTS=()
while IFS= read -r d; do ROOTS+=("$d"); done < <(
  { rg -l --pcre2 '"(?:react-native|expo)"\s*:' -g 'package.json' -g '!**/node_modules/**' .
    rg -l --pcre2 '^\s+sdk:\s*flutter\b' -g 'pubspec.yaml' -g '!**/.dart_tool/**' .
    rg --files -g '**/src/main/AndroidManifest.xml' -g '!**/{build,node_modules,.gradle}/**' . | sed 's#/src/main/AndroidManifest\.xml$#/x#'
    rg --files -g '**/*.xcodeproj/project.pbxproj' -g '!**/{Pods,node_modules,DerivedData}/**' . | sed 's#/[^/]*\.xcodeproj/project\.pbxproj$#/x#'
  } | while IFS= read -r f; do dirname "$f"; done | sort -u | awk 'p != "" && index($0, p "/") == 1 { next } { print; p = $0 }')
[ ${#ROOTS[@]} -gt 0 ] || { echo 'no mobile project marker: every class N/A (no mobile surface)'; exit 0; }
printf 'root %s\n' "${ROOTS[@]}"
# Gradle modules can sit beside an Android root (a library module with no manifest): search the parent of an `…/app` root
# too, only when that parent is the Gradle build root (it holds settings.gradle*) — an Expo root named `app` never adds `.`.
GROOTS=(); while IFS= read -r d; do GROOTS+=("$d"); done < <(for r in "${ROOTS[@]}"; do echo "$r"; p=$(dirname "$r")
  [ "${r##*/}" = app ] && { [ -f "$p/settings.gradle" ] || [ -f "$p/settings.gradle.kts" ]; } && echo "$p"; done | sort -u | awk 'p != "" && index($0, p "/") == 1 { next } { print; p = $0 }')
X=(-g '!**/{node_modules,Pods,build,.gradle,.dart_tool,.expo,DerivedData,dist,vendor,.cxx}/**' -g '!**/src/{test,androidTest,debug}/**'
   -g '!**/{test,tests,__tests__,__mocks__,mocks,fixtures,__fixtures__,testdata,e2e,integration_test,.maestro,docs,ai}/**'
   -g '!**/*{Tests,UITests}/**' -g '!**/*.{test,spec,stories}.*' -g '!**/*_test.dart' -g '!**/*.{g,freezed,mocks}.dart' -g '!**/*.{md,mdx,lock,snap,map}')
JS=(-g '*.{js,jsx,ts,tsx}'); DA=(-g '*.dart'); IMG=(-g '*.{png,jpg,jpeg,gif,webp,bmp,tif,tiff,heic}')

# 0. Versions: AGP (9.3 changes the shrink DSL), Expo build properties, RN, Flutter; the release command CI really runs.
rg -n --pcre2 'com\.android\.tools\.build:gradle:[\d.]+|id\("com\.android\.application"\)\s*version\s*"[\d.]+"|^\s*agp\s*=\s*"[\d.]+"' -g '*.{gradle,kts,toml}' "${X[@]}" "${GROOTS[@]}"
rg -n --pcre2 '"(?:react-native|expo|expo-build-properties)"\s*:' -g 'package.json' "${X[@]}" "${ROOTS[@]}"; rg -n --pcre2 '^\s+flutter:\s*["^>=]' -g 'pubspec.yaml' "${X[@]}" "${ROOTS[@]}"
rg -n --pcre2 '\b(?:assemble|bundle)Release\b|\bflutter\s+build\s+(?:apk|appbundle|ipa|ios)\b|\beas\s+build\b|\bgradle\(\s*task:' -g '*.{sh,yml,yaml}' -g 'Fastfile' -g 'eas.json' -g 'package.json' "${X[@]}" .

# 1. Release code shrinking off in an APPLICATION module (a library module is exempt: the app shrinks with consumer rules;
#    a root build file that declares the plugin `apply false` is not a module): no minify / optimization in release,
#    minify bound to a variable that is false, the dropped proguard-android.txt.
rg -l --pcre2 '^(?!.*\bapply\s+false\b).*com\.android\.application' -g 'build.gradle*' "${X[@]}" "${GROOTS[@]}" | sort -u | while IFS= read -r f; do
  rg -q --pcre2 'dev\.flutter\.flutter-gradle-plugin' "$f" && continue
  v=$(rg -o --no-filename --pcre2 '\bminifyEnabled\s+\K[a-z]\w*' "$f" | head -1)
  if [ -n "$v" ] && [ "$v" != true ]; then rg -q --pcre2 "\\b$v\\s*=\\s*true\\b" "$f" || rg -H -n --pcre2 "\\bminifyEnabled\\s+$v\\b|\\b$v\\s*=\\s*false\\b" "$f"
  elif ! rg -q --pcre2 'isMinifyEnabled\s*=\s*true|minifyEnabled\s*(?:=\s*)?true|optimization\s*\{[^}]*\benable\s*=\s*true' -U "$f"; then echo "1 $f: application module with no release shrinking"; fi; done
rg -n --pcre2 'proguard-android\.txt' -g 'build.gradle*' "${X[@]}" "${GROOTS[@]}"
rg -n --pcre2 '"enable(?:Proguard|Minify|ShrinkResources)InReleaseBuilds"\s*:\s*false' -g 'app.json' -g 'app.config.*' "${X[@]}" "${ROOTS[@]}"

# 2. Native code and ABIs: emulator ABIs shipped in release, universal APKs, the .so inventory with sizes (16 KB page
#    alignment is store-compliance-scan § 7's).
rg -n --pcre2 '\babiFilters\b[^\n]*\bx86|\buniversalApk\s*(?:=\s*)?true\b|\buseLegacyPackaging\s*(?:=\s*)?true\b' -g 'build.gradle*' "${X[@]}" "${GROOTS[@]}"
rg --files -g '*.so' "${X[@]}" "${GROOTS[@]}" | sort -u | while IFS= read -r f; do printf '2 %s %s KB\n' "$f" "$(( $(wc -c < "$f") / 1024 ))"; done

# 3. Assets. 3a every bundled raster of 256 KB or more (the budget is the project's: read it); 3b assets no file names;
#    3c iOS images outside an asset catalog (never sliced by app thinning).
rg --files "${IMG[@]}" -g '!**/{node_modules,build,.gradle,Pods,DerivedData,.dart_tool,ios/Runner/Assets.xcassets/AppIcon.appiconset,res/mipmap-*}/**' -g '!**/{test,tests,__tests__,fixtures,docs,ai}/**' "${ROOTS[@]}" | while IFS= read -r f; do s=$(( $(wc -c < "$f") / 1024 )); [ "$s" -ge 256 ] && echo "3a $f ${s} KB"; done
rg --files "${IMG[@]}" "${X[@]}" "${ROOTS[@]}" | rg '/assets/' | while IFS= read -r f; do b=$(basename "$f"); n=${b%.*}; n=${n%@[23]x}
  rg -q -F "$n" -g '*.{js,jsx,ts,tsx,dart,kt,java,swift,json,yaml,xml,plist}' "${X[@]}" "${ROOTS[@]}" || echo "3b $f: referenced nowhere"; done
for r in "${ROOTS[@]}"; do [ -n "$(rg --files -g '*.pbxproj' "$r" | head -1)" ] || continue
  rg --files "${IMG[@]}" -g '!**/*.xcassets/**' "${X[@]}" "$r" | rg -v --pcre2 '/(?:android|assets|lib|src|web|macos|windows|linux)/' | sed 's#^#3c #'; done

# 4. JS / Dart bundle composition: heavy whole-library dependencies and whole-library imports (measure with the analyzer).
rg -n --pcre2 '"(?:moment|moment-timezone|lodash|aws-sdk|firebase|@fortawesome/fontawesome-free|crypto-js|core-js|rxjs|date-fns-tz|libphonenumber-js|react-native-vector-icons)"\s*:' -g 'package.json' "${X[@]}" "${ROOTS[@]}"
rg -n --pcre2 '^import\s+(?:\w+|\*\s+as\s+\w+)\s+from\s+["\x27](?:lodash|moment|aws-sdk|firebase|rxjs|ramda)["\x27]|require\(\s*["\x27](?:lodash|moment|aws-sdk)["\x27]\s*\)' "${JS[@]}" "${X[@]}" "${ROOTS[@]}"

# 5. Engine and debug payload in release: Hermes opted out; Flutter release builds without --split-debug-info; iOS Release
#    settings that keep symbols or dead code; the stale bitcode flag.
rg -n --pcre2 '^\s*hermesEnabled\s*=\s*false\b|:hermes_enabled\s*=>\s*false|"jsEngine"\s*:\s*"jsc"' -g 'gradle.properties' -g 'Podfile' -g 'app.json' "${X[@]}" "${ROOTS[@]}"
rg -n -U --pcre2 '\bflutter\s+build\s+(?:apk|appbundle|ipa|ios)\b(?!(?:[^\n]*\\\n)*[^\n]*--split-debug-info)' -g '*.{sh,yml,yaml}' -g 'Fastfile' -g 'Makefile' "${X[@]}" . | rg -v --pcre2 '^[^:]+:\d+:\s*#'
rg -n --pcre2 '\bENABLE_BITCODE\s*=\s*YES\b|\bDEAD_CODE_STRIPPING\s*=\s*NO\b|\bSTRIP_INSTALLED_PRODUCT\s*=\s*NO\b|\bASSETCATALOG_COMPILER_OPTIMIZATION\s*=\s*""' -g '*.{pbxproj,xcconfig}' "${X[@]}" "${ROOTS[@]}"

# 6. Dependencies nothing imports (JS: package.json minus import / require specifiers; Dart: pubspec minus package: imports).
#    Native-only and config-plugin packages are read, not reported: autolinking and app.json plugins use them with no import.
for r in "${ROOTS[@]}"; do
  if [ -f "$r/package.json" ]; then used=$(rg -o --no-filename --pcre2 '(?:from\s+|require\(\s*|import\(\s*)["\x27]\K(?:@[\w.-]+/)?[\w.-]+' "${JS[@]}" "${X[@]}" "$r" | sort -u)
    if [ -z "$used" ] && [ -n "$(rg --files "${JS[@]}" "$r" | head -1)" ]; then echo "6 $r: every source file is under an excluded path — not compared"; else
    plug=$(rg -o --no-filename --pcre2 '"plugins"\s*:\s*\[[\s\S]*?\]' -U -g 'app.json' "$r" | rg -o --pcre2 '"\K(?:@[\w.-]+/)?[\w.-]+(?=")' | sort -u)
    python3 -c 'import json,sys; print("\n".join(sorted(json.load(open(sys.argv[1])).get("dependencies",{}))))' "$r/package.json" | while IFS= read -r d; do
      printf '%s\n' "$used" | rg -q -x -F "$d" && continue; printf '%s\n' "$plug" | rg -q -x -F "$d" && continue
      case "$d" in react|react-native|expo|react-dom|react-native-web|react-native-screens|expo-updates|expo-dev-client|expo-build-properties|expo-system-ui|@types/*|*babel*|*eslint*) continue ;; esac; echo "6 $r: $d imported nowhere (read: autolinked native module, peer, or config plugin?)"; done; fi; fi
  if [ -f "$r/pubspec.yaml" ]; then used=$(rg -o --no-filename --pcre2 "^(?:import|export)\\s+['\"]package:\\K\\w+" "${DA[@]}" "$r" | sort -u)
    sed -n '/^dependencies:/,/^[a-z_]*:/p' "$r/pubspec.yaml" | rg -o --pcre2 '^\s{2}\K\w+(?=:)' | while IFS= read -r d; do
      [ "$d" = flutter ] && continue; printf '%s\n' "$used" | rg -q -x -F "$d" || echo "6 $r: $d imported nowhere (read: plugin registered natively?)"; done; fi; done

# 7. Distribution format: an APK uploaded to Play (every ABI and density downloaded) where an App Bundle is the format.
rg -n --pcre2 'upload_to_play_store\([^)]*\bapk:|supply\([^)]*\bapk:|\bgradle\(\s*task:\s*["\x27]assemble(?:Release)?["\x27]' -g 'Fastfile' -g '*.{yml,yaml,sh}' "${X[@]}" .
:
```

A finding is a script line **plus** a read **plus** a measurement. Three blind spots are structural: **merged config** (a Gradle convention plugin or `buildSrc` can turn shrinking on for every module — read it before calling a module unshrunk); **assets referenced by computed names** (`require(\`./img/${name}.png\`)` is invisible to § 3b — read before deleting); **native-only dependencies** (autolinked modules and config plugins are used with no import — § 6 prints them for a read, never as a verdict).

**Measured** (2026-10-05, ripgrep 15.2.0; bash 3.2 and zsh give the same hit set, stdin piped or not; < 1 s). On the program's multi-stack sample (14 positives across the seven classes, 6 decoys) every positive surfaces and no decoy does: a library module with `isMinifyEnabled = false` (precedent § 41), referenced assets, an asset inside an asset catalog (sized, never flagged as unsliced), a Flutter build line that already passes `--split-debug-info`, packages consumed without imports. Six lines are left to the read step by design: four § 6 packages the sample declares and never imports, a 300 KB image inside an asset catalog (sized against the budget), and the `.so` inventory. On every web and server fixture in `benchmarks/fixtures/*` it prints `N/A`; on `mobile-defects` (five mobile roots, measured 2026-10-10) it prints all 8 of its seeds in 27 lines — its `DEFECTS.md` § Detector measurement. A first version printed 7 noise lines there: an Expo root named `app` added `.` to `GROOTS` (every grep 0–2 hit twice, and the whole repository searched), and § 1 read a root build file whose `plugins {}` declares `com.android.application` with `apply false` as an unshrunk application module. Run from this repository's root, greps 0–2 now carry `X` and § 6 says `not compared` for a root whose every source file sits under an excluded path, instead of listing each dependency as unimported (35 lines → 10). On a read-only real Flutter app (440 Dart files) the first version printed 444 lines in 7.7 s, 442 false: 441 test screenshots and goldens counted as unused assets because two `-g` include globs are ORed (the asset filter is now a path filter after the exclusions), and a CI command in a shell comment continued with `\` onto the line carrying `--split-debug-info` (the grep now follows continuations and skips comments). After the fixes: 2 lines, both context (the AGP version, the release command), 0 candidates — the app shrinks in release and every dependency is imported.

## The 3,000-hit path

1. **Intersect** with what ships: assets outside the bundled directories, modules not in the release variant and dependencies only in `devDependencies` are dismissed with one read.
2. **Group** by class and root cause: one Gradle convention plugin, one icon font, one `moment` dependency is one group however many call sites it has.
3. **Rank** by measured bytes when the analyzer ran; otherwise R8 off, debug payload and ABIs first (whole-binary multipliers), then assets by size, then imports.
4. **Read the top 30 groups.**
5. **Prefer the analyzer as the bulk oracle**: one Atlas / `--analyze-size` / *Analyze APK* run ranks every module at once.
6. **Ledger the rest** `Live, unreviewed (k groups / n hits)`.

## Scans for

| § | Class | Proof tier | Default |
|---|---|---|---|
| 1 | Release code shrinking off in an application module | A (artifact delta) | high (size, DEX vital, reverse engineering) |
| 2 | Native code and ABIs: emulator ABIs in release, universal APKs, large `.so` | A | medium |
| 3 | Assets: oversized, unused, unsliced on iOS | A | medium by measured size; low under the project budget |
| 4 | JS / Dart bundle composition: heavy whole-library dependencies and imports | A (analyzer) | medium |
| 5 | Engine and debug payload in release: Hermes opted out, Flutter symbols in the binary, iOS Release keeping dead code | A | medium; high for Hermes off on RN |
| 6 | Dependencies nothing imports | S + A | low until measured |
| 7 | Distribution format: an APK uploaded to Play | A | medium |

### 1. Release code shrinking off

```
BAD:   def enableProguardInReleaseBuilds = false … release { minifyEnabled enableProguardInReleaseBuilds }   // the RN template default
       android { … }   // application module, no release block at all · proguardFiles getDefaultProguardFile("proguard-android.txt")
GOOD:  release { isMinifyEnabled = true; isShrinkResources = true; proguardFiles(getDefaultProguardFile("proguard-android-optimize.txt"), …) }
       AGP ≥ 9.3: optimization { enable = true } · Expo: expo-build-properties android.enableProguardInReleaseBuilds (read the installed plugin)
```
**Read the code:** Is it an application module (a library module minifies through consumer rules — precedent § 41)? Does a convention plugin or `buildSrc` enable shrinking (the module file is then silent)? On AGP ≥ 9.3, is the new DSL in use (a missing `isMinifyEnabled` is then not a finding — precedent § 53)? Are keep rules present for reflection-heavy libraries, so turning R8 on does not crash? **Finding when** an application module's release build ships unshrunk. **Severity:** high. **Proof:** A — `bundleRelease` before and after; the per-device download size and the DEX size drop; the release smoke test on a device passes with shrinking on.

### 2. Native code and ABIs

```
BAD:   ndk { abiFilters "armeabi-v7a", "arm64-v8a", "x86", "x86_64" }   // emulator ABIs shipped to every APK user
       splits { abi { enable true; universalApk true } } on the artifact users install · useLegacyPackaging true
GOOD:  release ABIs = the devices in scope; Play splits per device from the AAB; x86 only in a debug or test flavour
```
**Read the code:** Is the artifact an AAB (Play then delivers one ABI per device and the filter matters less) or an APK distributed directly? Is `x86_64` there for Chromebooks the product supports? The `.so` inventory prints each native library with its size; alignment is `store-compliance-scan` § 7's. **Finding when** release artifacts carry ABIs or packaging no shipped device needs. **Severity:** medium. **Proof:** A — APK / AAB size per ABI before and after.

### 3. Assets

```
BAD:   assets/images/onboarding-hero.png 700 KB    assets/images/unused-banner.png referenced nowhere
       ios-app/Acme/Resources/splash@3x.png outside an asset catalog → shipped to every device, never sliced by app thinning
GOOD:  WebP / AVIF or a vector at the displayed size; asset catalogs on iOS; unused files deleted after a read of computed names
```
**Read the code:** What is the displayed size × scale (a 300 pt hero on a 3x screen legitimately needs 900 px)? Is the asset loaded by a computed name? Is a 3x raster needed at all (a vector, an SF Symbol)? The 256 KB print floor is a reading aid, not a budget: the project's budget decides. **Finding when** an asset is unused, unsliced, or measurably larger than its display needs. **Severity:** medium by measured bytes; low below the project budget. **Proof:** A — the file sizes before and after, and the artifact size delta.

### 4. JS / Dart bundle composition

```
BAD:   "moment": "…" + import moment from 'moment'          import _ from 'lodash'          the whole icon font set
GOOD:  Intl / date-fns per function · import debounce from 'lodash/debounce' · only the glyph sets used, or a subset font
```
**Read the code:** What does the analyzer attribute to the package (Atlas, the visualizer)? Are the call sites compatible with the lighter replacement (a blind swap breaks runtime)? How many sibling imports of the same class exist (sweep them all)? **Finding when** a dependency's bundled bytes are large and the used surface is small. **Severity:** medium. **Proof:** A — the analyzer before and after on the release bundle.

### 5. Engine and debug payload in release

```
BAD:   hermesEnabled=false (gradle.properties) · :hermes_enabled => false (Podfile)       // JSC on RN ≥ 0.84 is third-party
       flutter build appbundle --release                                                 // symbols stay in the binary
       ENABLE_BITCODE = YES · DEAD_CODE_STRIPPING = NO · STRIP_INSTALLED_PRODUCT = NO (Release)
GOOD:  Hermes on (the default — precedent § 35) · flutter build … --split-debug-info=<dir> [--obfuscate] · Release strips and dead-strips
```
**Read the code:** Is Hermes off for a documented reason (a library that needs JSC)? Does CI upload the split debug symbols to the crash reporter, so the split costs no diagnosability? Is the setting in the Release configuration or only Debug? Bitcode has been gone since Xcode 14 [K], so the flag is stale config. **Finding when** a release ships an engine, symbols or code it does not need. **Severity:** medium; high for Hermes off on RN. **Proof:** A — artifact size before and after; for Hermes, also the cold-start delta from `@device-performance-auditor` (never inferred from size).

### 6. Dependencies nothing imports

The set-difference prints every declared dependency no source file imports, minus app-config plugins and a short list of packages consumed without imports (React Navigation's `react-native-screens`, `expo-updates`, `expo-dev-client`, `expo-build-properties`). **Read the code:** Is it autolinked native code used through another package, a peer dependency, a Babel or Metro plugin, a Flutter plugin registered natively? `knip` (JS) and `dart pub deps` / a dependency validator are the lint lane when the project configures them. **Finding when** a dependency ships code no path uses. **Severity:** low until measured. **Proof:** A — remove it, the release build and the smoke test pass, and the artifact shrinks.

### 7. Distribution format

```
BAD:   gradle(task: "assembleRelease") + upload_to_play_store(apk: "…/app-release.apk")   // every ABI and density to every user
GOOD:  gradle(task: "bundle", build_type: "Release") + upload_to_play_store(aab: "…/app-release.aab")
```
**Read the code:** Is the APK for Play (a bundle is the format; the legacy APK cap is in `/optimize-bundle`'s table) or for direct distribution (then § 2's splits matter)? **Finding when** Play receives an APK. **Severity:** medium. **Proof:** A — per-device download size of the AAB (`bundletool get-size total`) against the APK.

## Proof — the release-artifact delta

[`proof-oracles.md`](../../../../snippets/proof-oracles.md) § Mobile, *Release-artifact size delta*: build the release artifact the store receives, before and after, with the same toolchain versions; report bytes for the same artifact type and, for Play, the per-device download size; repeat once to show the number is stable. A class proven only on a debug build is refuted. No build possible on the host → the row is `[report-flagged]` with the exact build and analyzer commands, never a size estimate.

## Output

```
app-size-scan — lanes: AGP 8.12.0 (rn-app/android/build.gradle:9), react-native 0.82.1, expo 57 / RN 0.87, flutter 3.47
Roots: 6 · Analyzer runs: none on this host (no Android SDK / Xcode) → measured rows SKIPPED, findings [report-flagged]

1. rn-app/android/app/build.gradle:13                                          [report-flagged]   high
   §1 release minify bound to enableProguardInReleaseBuilds = false (:4); proguard-android.txt (:14) is dropped in AGP 9.
   Settling run: ./gradlew :app:bundleRelease before/after; bundletool get-size total. Fix: true + proguard-android-optimize.txt.

2. rn-app/android/gradle.properties:3                                          [report-flagged]   high
   §5 hermesEnabled=false on react-native 0.82.1 — the release ships JSC and plain JS.
   Settling run: release bundle size and @device-performance-auditor cold start, before/after. Fix: remove the opt-out.

Verification: 21 candidates → 0 findings · 2 unconfirmed · 4 hardening · 0 pre-existing · 15 refuted
Routed: 16 KB alignment → store-compliance-scan § 7 · CartProvider.tsx:3 deduped with mobile-perf-scan § 6

Class coverage:
  §1 shrinking            checked (4 hits → 1 unconfirmed; feature-lib is a library module, precedent § 41)
  §2 native / ABIs        checked (2 hits → 0 findings; 1 hardening: x86 in release abiFilters, AAB delivery)
  §3 assets               checked (5 hits → 0 findings; 3 hardening, under no declared budget)
  §4 bundle composition   checked (2 hits → 0 findings here; deduped with mobile-perf-scan § 6)
  §5 engine / debug       checked (5 hits → 1 unconfirmed)
  §6 unused dependencies  checked (4 lines → 0 findings; all native-only or unread sample packages)
  §7 distribution         checked (2 hits → 0 findings; 1 hardening: APK upload to Play)
```

`[report-with-fix]`: the release artifact was built and measured before and after, and the fix is local. `[report-flagged]`: no measurement on this host, and the row names the build and analyzer commands that settle it. The coverage block lists **all seven** classes on every run: `checked`, `N/A (<reason>)` (no Android module → § 1, 2, 7 N/A), `blocked (<reason>)`, or `Live, unreviewed (k groups / n hits)`.

Write the report to `ai/runtime/app-size-<date>.md`; optionally append a row (date, commit, artifact, bytes) to `ai/runtime/app-size-trend.csv` for trending.

## False positives / precedents

The verifier reads [`precedents/mobile.md`](../../../../snippets/precedents/mobile.md) and [`refute-before-report.md`](../../../../snippets/refute-before-report.md) § 4: minify off in a library module (§ 41); a missing `isMinifyEnabled` on AGP ≥ 9.3 with the `optimization` DSL (§ 53); "enable Hermes" when the build does not opt out (§ 35); a fix in generated Expo CNG folders (§ 3). And the size-specific § 94–97: a debug or universal-APK size compared with an AAB (§ 94); an asset in a design gallery or test target (§ 95); a large asset that is the product — a bundled offline map, a sound library (§ 96); a dependency used only through autolinking or a config plugin (§ 97).

## When to run

- On a diff that adds a dependency, an asset, a native library, or changes a Gradle release block, `gradle.properties`, the Podfile, the Xcode Release configuration, `app.json` build properties or the release lane — and on every whole-repo `/mobile-audit`, reporting all seven classes.
- Before and after a dependency upgrade (the size delta), and as a pre-release check when `/optimize-bundle` runs.

## Related

- `/optimize-bundle` (this pack) — runs this skill for the measurement and applies the reductions; holds the published store size limits.
- `store-compliance-scan` § 7 (16 KB pages) and `@app-store-reviewer` (store consequences) (this pack).
- `@device-performance-auditor` and `mobile-perf-scan` § 6 (this pack) — cold start and eager imports; they consume this skill's size number.
- `device-harness` (this pack) — the release smoke test after a shrink change.
