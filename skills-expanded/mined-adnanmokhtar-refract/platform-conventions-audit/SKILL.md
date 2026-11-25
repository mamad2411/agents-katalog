---
name: platform-conventions-audit
description: Find where an RN/Expo, Flutter, iOS or Android app breaks its platforms' conventions — edge-to-edge insets, predictive back, swipe-back, navigation stacks, safe area, per-platform drift — and close each with a /polish verb or a device-proved fix.
kind: skill
pack: mobile
allowed-tools: [Read, Write, Edit, Grep, Glob, Bash]
---

# Skill: platform-conventions-audit

## Premise

iOS and Android disagree about how an app enters, leaves and fills the screen. Android 15 draws every app targeting API 35 behind the system bars, and Android 16 stops honouring the opt-out at API 36; Android 16 also stops calling `onBackPressed` at API 36 because predictive back owns the gesture. iOS users leave a screen with an edge swipe that a hidden back button silently removes. This skill finds the places where the code still assumes the old platform, or one platform's look on the other — the cases the web has no analogue for.

**Every finding cites `<file:line>` + the platform and the version gate it depends on (the merged `targetSdk`, the RN / Flutter version — grep 0 prints them) + the screen a user reaches it from + the oracle that shows it on a device (or the run that would) + either a `/polish` closure verb or a code fix.** A grep hit is never a finding by itself, and "conforms" is never printed without the class-coverage block (§ Output).

**No input file is required.** The 1.x skill halted unless `_extracted-idioms.md § Mobile platforms` existed, and nothing in the toolchain writes that section, so it halted on every install. The platforms come from the repo's markers (`android/`, `ios/`, a Gradle module, an Xcode project, an Expo config); the conventions come from what the code already does (§ 4–6). A project's own declaration, when one exists (`ai/`, an ADR, `CLAUDE.md`), overrides the inference and is cited.

## The rule

A candidate is a finding when all four hold:

1. **It ships and is reachable** — a release build, not a debug source set or a design gallery, on a screen a navigator, link or launcher reaches.
2. **The gate holds** — the platform behaviour exists at the version the module really builds against: the `[target N]` tag the script prints is the nearest `targetSdk` above the file (merged manifest when a build exists; `expo-build-properties` for Expo; Flutter 3.27+ targets 35 by default, docs.flutter.dev read 2026-10-05).
3. **Nothing neutralizes it** — a shared wrapper, an inset-aware `Scaffold`, `react-native-safe-area-context`, a theme that already branches per platform.
4. **A user sees it** — content under a bar or the gesture area, a back gesture that skips the unsaved-changes guard, a login screen reachable by back, one platform wearing the other's controls. Convention classes (§ 4–7, 9) are finds only against the convention the code shows (§ 4–6).

## Boundaries

- Touch-target size, labels, roles, text scaling, focus order, contrast → `mobile-a11y-scan` (this pack), judged by `@ux-reviewer`; § 3 below only routes. The ui-ux pack's `tap-target` axis keeps the `/polish` verb (`expand-tap-target`).
- Typography **scale**, rhythm, hierarchy, tokens, motion → the ui-ux pack's axes, co-run by `/polish` on every `mobile-*` pass. This skill judges only *which family per platform*.
- State lost on process death, deep-link payloads, permissions → `mobile-lifecycle-scan`. An Android 16 tablet ignoring an orientation lock (sw600dp, target 36) is that skill's § 1 restore variant.
- Store consequences (target-API deadline, 16 KB pages) → `store-compliance-scan` and `@app-store-reviewer`.
- Device evidence (screenshots, the UI tree, an API 35 / 36 emulator) → `device-harness` (this pack), which produces and never judges.

## Inputs (precise contract)

| Input | Source | Required |
|---|---|---|
| Codebase root | Orchestrator | YES |
| Target platforms | Derived: an `android/` or Gradle app module, an `ios/` or Xcode project, Expo `platforms` / `android` / `ios` keys | derived — none found → every class `N/A` |
| Platform versions | Grep 0: `targetSdk` per module, `react-native`, `expo`, Flutter | derived |
| Declared conventions | Optional: an ADR, `CLAUDE.md`, `ai/` notes that state per-platform icons, fonts or controls; else inferred (§ 4–6) | NO |
| Device captures | `device-harness` output, when a run exists | NO (classes needing a render are `blocked (no device)`) |
| Scope filter | Caller | NO (default: the whole app) |

## Outputs

One finding per `<file:line>` (or per wrapper, § The 3,000-hit path):

```yaml
class: platform-conventions
subclass: <ios-hig-drift | material-spec-drift | touch-target-drift | platform-icon-drift | platform-typography-drift |
           per-platform-surface-drift | haptic-feedback-coverage | safe-area-handling | elevation-drift |
           navigation-pattern-drift | edge-to-edge-insets | predictive-back>
platform: ios | android | both
gate: <targetSdk / RN / Flutter line from grep 0, or "none">
screen: <screen-name>
file: <path:line>
canonical: <what the platform does, with the cited source>
divergence: <what this screen does instead>
closure_verb: <one of the five below — OMIT on a routed observation>
routed_to: <INSTEAD of closure_verb: the skill, pack or fix that owns it>
risk: low | medium | high
```

Under `/polish`, the run writes `ai/polish/_platform-decisions.md` with four blocks the validator (`validate-polish-artifacts.sh`, `check_mobile_evidence`) requires by name: **Per-platform UI tree evidence** (the `device-harness` captures, or `not captured: <reason>`), **iOS HIG conformance evidence**, **Material 3 conformance evidence**, **Per-screen findings**. Under `/mobile-audit` the findings use the § Output form.

### The closure-verb vocabulary is closed

`/polish` registers exactly five mobile verbs on top of the 19 ui-ux ones: **`apply-platform-spec` · `unify-platform-icon` · `apply-platform-typography` · `add-haptic-feedback` · `respect-safe-area`** (`commands/polish.md` § Mobile; `scripts/validate-polish-artifacts.sh` accepts them only when `PROJECT_KIND` is `mobile-*`). A detector that wants a sixth reuses one because the act is the same (edge-to-edge insets are `respect-safe-area`; predictive back is `apply-platform-spec --platform=android`), or emits `routed_to:` and no verb. Correctness rows that are not finish — navigation during composition, a login screen left on the stack — carry `routed_to: /mobile-fix` and a fix line; `/polish` does not execute them.

## Adapt to the codebase — lanes

| Lane | Insets / safe area | Back | Navigation | Per-platform look |
|---|---|---|---|---|
| **React Native** (≥ 0.82, New Architecture only) | `react-native-safe-area-context`; core `SafeAreaView` deprecated in 0.81; `StatusBar` `backgroundColor` / `translucent` removed in 0.87 | `BackHandler` keeps working under predictive back (RN 0.81 post); a native `onBackPressed` override does not | React Navigation `reset` / `CommonActions.reset`; `gestureEnabled` | `Platform.select`, per-platform files (`.ios.tsx`) |
| **Expo** (SDK 53–57) | as RN; `expo-build-properties` `targetSdkVersion` is the gate | as RN | Expo Router `router.replace`, `Stack.Protected` | as RN |
| **Flutter** (3.x) | `SafeArea`, `MediaQuery.paddingOf`; edge-to-edge by default from 3.27 | `PopScope` + `canPop` + `onPopInvokedWithResult` (replaces `WillPopScope`, stable 3.16) | `pushReplacement`, `pushAndRemoveUntil`, go_router `go` | `.adaptive` constructors, `Icons.adaptive`, `Cupertino*` |
| **Android** (Kotlin, Compose, Views) | `Scaffold` `innerPadding`, `WindowInsets` / `safeDrawingPadding`, `ViewCompat.setOnApplyWindowInsetsListener` | `OnBackPressedCallback`, `BackHandler` (Compose), `OnBackInvokedCallback` | `popUpTo { inclusive = true }` | Material 3 components and tokens |
| **iOS** (SwiftUI, UIKit) | safe-area modifiers; `ignoresSafeArea` only on backgrounds | system back + edge swipe (`interactivePopGestureRecognizer`) | `NavigationStack` path reset, root swap | SF Symbols, system fonts, sheets |

## Pre-flight greps

Run as **one** script from the repo root (shell state does not survive between tool calls). Grep **N** feeds detector **§N**; grep 0 is context. Every `rg` names its path, set-differences read files in a `while read` loop, and a line tagged `[target N]` has passed its gate (an unknown target prints, tagged `?`). Any `rg` error on stderr is a failed grep, never zero hits.

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
X=(-g '!**/{node_modules,Pods,build,.gradle,.dart_tool,.expo,DerivedData,dist,vendor,.cxx}/**' -g '!**/src/{test,androidTest,debug}/**'
   -g '!**/{test,tests,__tests__,__mocks__,mocks,fixtures,__fixtures__,testdata,e2e,integration_test,.maestro,docs,ai,storybook,.storybook,tool}/**'
   -g '!**/*{Tests,UITests}/**' -g '!**/*.{test,spec,stories}.*' -g '!**/*_test.dart' -g '!**/*.{g,freezed,mocks}.dart' -g '!**/*.{md,mdx,lock,snap,map}')
NC=(rg -v --pcre2 '^(?:\[[^]]*\]\s)?[^:]+:\d+:\s*(//|/\*|\*(\s|/|$)|#(?!\{)|<!--)')
JS=(-g '*.{js,jsx,ts,tsx}'); KT=(-g '*.{kt,java}'); DA=(-g '*.dart'); SW=(-g '*.swift'); RES=(-g '**/res/values*/*.xml')
TB='(?:[^>{]|\{(?:[^{}]|\{[^{}]*\})*\})*'
# tsdk FILE — the targetSdk that governs FILE: nearest build.gradle(.kts) or Expo app.json above it carrying a number;
# a Flutter root without one prints `flutter` (3.27+ targets 35 by default); nothing found prints `?`.
tsdk() { d=$(dirname "$1"); while :; do
  for g in "$d"/build.gradle "$d"/build.gradle.kts "$d"/app.json "$d"/android/build.gradle "$d"/android/build.gradle.kts "$d"/android/app/build.gradle "$d"/android/app/build.gradle.kts; do
    [ -f "$g" ] || continue; n=$(rg -o --no-filename --pcre2 '\btargetSdk(?:Version)?\b\W{0,6}\K\d{2}\b' "$g" | sort -n | tail -1); [ -n "$n" ] && { echo "$n"; return; }; done
  [ -f "$d/pubspec.yaml" ] && { echo flutter; return; }
  case "$d" in .|/|'') echo '?'; return ;; esac; d=$(dirname "$d"); done; }
# gate N — keep an `rg -H -n` hit when its targetSdk is >= N (or unknown), tagged with the target it read.
gate() { while IFS=: read -r f l r; do t=$(tsdk "$f"); case "$t" in *[!0-9]*) echo "[target $t] $f:$l:$r" ;; *) [ "$t" -ge "$1" ] && echo "[target $t] $f:$l:$r" ;; esac; done; }
win() { while IFS=: read -r f l r; do s=$((l > $1 ? l - $1 : 1)); if sed -n "${s},$((l + $2))p" "$f" | rg -q -U --pcre2 "$3" -; then [ "$4" = has ] && echo "$f:$l:$r"; else [ "$4" = lacks ] && echo "$f:$l:$r"; fi; done; }

# 0. Versions and gates: targetSdk per Android module / Expo config, RN, Flutter, the predictive-back opt-in or opt-out, RN edge-to-edge.
rg -n --pcre2 '\btargetSdk(?:Version)?\b\W{0,6}(?:\d{2}|flutter\.\w+)' -g '*.{gradle,kts}' -g 'app.json' "${X[@]}" "${ROOTS[@]}"; rg -n --pcre2 '"(?:react-native|expo|react-native-safe-area-context|react-native-edge-to-edge)"\s*:' -g 'package.json' "${X[@]}" "${ROOTS[@]}"
rg -n --pcre2 '^\s+flutter:\s*["^>=]' -g 'pubspec.yaml' "${ROOTS[@]}"; rg -n --pcre2 'enableOnBackInvokedCallback|edgeToEdgeEnabled' -g 'AndroidManifest.xml' -g 'gradle.properties' -g 'app.json' "${X[@]}" "${ROOTS[@]}"

# 1. iOS: system back and swipe-to-go-back removed; full-screen modal where a sheet is the idiom (read).
rg -n --pcre2 '\.navigationBarBackButtonHidden\(\s*true\s*\)|interactivePopGestureRecognizer\??\.isEnabled\s*=\s*false|\bgestureEnabled\s*:\s*false\b|\.interactiveDismissDisabled\(\s*\)' "${SW[@]}" "${JS[@]}" "${X[@]}" "${ROOTS[@]}" | "${NC[@]}"
rg -n --pcre2 '\.fullScreenCover\(|modalPresentationStyle\s*=\s*\.fullScreen\b|presentation\s*:\s*["\x27]fullScreenModal["\x27]' "${SW[@]}" "${JS[@]}" "${X[@]}" "${ROOTS[@]}" | "${NC[@]}"

# 2. Android Material: press feedback removed (ripple off, no-feedback touchable on an action).
rg -n --pcre2 '\bindication\s*=\s*null\b|\bsplashFactory\s*:\s*NoSplash\b' "${KT[@]}" "${DA[@]}" "${X[@]}" "${ROOTS[@]}" | "${NC[@]}"
rg -n --pcre2 '<TouchableWithoutFeedback\b(?!'"$TB"'\bonPress=\{\s*Keyboard\.dismiss\s*\})' "${JS[@]}" "${X[@]}" "${ROOTS[@]}"

# 4-6. Drift is measured against the convention the code already shows, per root: the minority side is printed, a
#      root with no adaptive site at all is one line (a single-look app is a design decision, not drift).
AD='\bIcons\.adaptive\.|\b\w+\.adaptive\(|\bshowAdaptiveDialog\b|\bshowCupertino\w+\(|\bCupertino(?:Switch|Slider|ActivityIndicator|AlertDialog|DatePicker|SliverRefreshControl)\(|Platform\.select\(\s*\{\s*ios\s*:'
MT='\b(?:Switch|Slider|Checkbox|Radio|CircularProgressIndicator|RefreshIndicator|AlertDialog)\((?!\s*\))|\bshow(?:Date|Time)Picker\(|\bIcons\.(?:arrow_back|share|more_vert|more_horiz)\b|<(?:Ionicons|Icon|MaterialIcons|Feather)\b[^>]*\bname=["\x27](?:arrow-back|share-social|share-outline|ellipsis-vertical)["\x27]'
for r in "${ROOTS[@]}"; do a=$(rg -c --pcre2 "$AD" "${DA[@]}" "${JS[@]}" "${X[@]}" "$r" | awk -F: '{ s += $NF } END { print s + 0 }'); m=$(rg -c --pcre2 "$MT" "${DA[@]}" "${JS[@]}" "${X[@]}" "$r" | awk -F: '{ s += $NF } END { print s + 0 }')
  [ "$m" -gt 0 ] || continue; [ "$a" -gt 0 ] || { echo "4-6 $r: $m single-look site(s), 0 adaptive — convention, not drift"; continue; }
  if [ "$a" -ge "$m" ]; then rg -H -n --pcre2 "$MT" "${DA[@]}" "${JS[@]}" "${X[@]}" "$r"; else rg -H -n --pcre2 "$AD" "${DA[@]}" "${JS[@]}" "${X[@]}" "$r"; fi | "${NC[@]}" | sed "s#^#[minority $a adaptive : $m single-look] #"; done
rg -n --pcre2 '\bfontFamily\s*[:=]\s*["\x27]|\bGoogleFonts\.\w+\(|\bFontFamily\(\s*Font\(|\.font\(\s*\.custom\(' "${JS[@]}" "${DA[@]}" "${KT[@]}" "${SW[@]}" -g '!**/{theme,themes,tokens,design-system,styles}/**' "${X[@]}" "${ROOTS[@]}" | "${NC[@]}"

# 7. Haptics: only when the app already uses them (its own wrapper counts); an inline long-press or a raw refresh control
#    with no haptic within the handler window. A pass-through parameter (`onLongPress: onLongPress`) is not a handler.
H=$(rg -l --pcre2 '\w*Haptic\w*\.\w+\(|expo-haptics|react-native-haptic-feedback|UI(?:Impact|Notification|Selection)FeedbackGenerator|\.sensoryFeedback\(|performHapticFeedback' "${X[@]}" "${ROOTS[@]}" | wc -l | tr -d ' ')
echo "convention: haptics in $H file(s)"; [ "$H" -gt 0 ] && rg -H -n --pcre2 '\bonLongPress\s*(?::|=(?!=))\s*+(?!(?:\w+\s*\?\s*)?onLongPress\b|null\b)|\bonLongClick\s*=\s*\{|\.onLongPressGesture\b|<RefreshControl\b|\bRefreshIndicator\(' "${DA[@]}" "${JS[@]}" "${KT[@]}" "${SW[@]}" "${X[@]}" "${ROOTS[@]}" | "${NC[@]}" | win 2 6 '[hH]aptic|sensoryFeedback|FeedbackGenerator' lacks

# 8. Safe area: RN core SafeAreaView (deprecated 0.81); SwiftUI safe-area ignored on a container that holds controls.
rg -n --pcre2 '^import\s*\{[^}]*\bSafeAreaView\b[^}]*\}\s*from\s*["\x27]react-native["\x27]' "${JS[@]}" "${X[@]}" "${ROOTS[@]}"
rg -H -n --pcre2 '^\s*\.(?:ignoresSafeArea|edgesIgnoringSafeArea)\(' "${SW[@]}" "${X[@]}" "${ROOTS[@]}" | win 12 0 '\bButton\b|\bTextField\b|\bToggle\b|\.onTapGesture\b' has

# 9. Elevation / shadow literals outside the token source (gate on a token source existing: read).
rg -n --pcre2 'defaultElevation\s*=\s*\d+(?:\.\d+)?\.dp|\bModifier\.shadow\(\s*\d+(?:\.\d+)?\.dp|\.shadow\(\s*\d+(?:\.\d+)?\.dp|\belevation\s*:\s*\d+\s*[,}]|\bshadow(?:Opacity|Radius)\s*:\s*\d|\.shadow\(\s*(?:color:[^)]*)?radius:\s*\d' "${KT[@]}" "${JS[@]}" "${DA[@]}" "${SW[@]}" -g '!**/{theme,themes,tokens,design-system}/**' "${X[@]}" "${ROOTS[@]}" | "${NC[@]}"

# 10. Navigation: 10a navigate during composition / build (not in an effect or a callback); 10b sign-in that pushes onto the
#     stack (back returns to the login screen); 10c drawer as primary navigation (read against the iOS idiom).
rg -l '@Composable' "${KT[@]}" "${X[@]}" "${ROOTS[@]}" | while IFS= read -r f; do rg -H -n --pcre2 '^\s*(?:if\s*\([^)]*\)\s*)?\w*[nN]av\w*\.navigate\(' "$f"; done | win 0 0 'LaunchedEffect|onClick|clickable|SideEffect|DisposableEffect|->' lacks
rg -H -n --pcre2 '^\s*(?:if\s*\([^)]*\)\s*)?(?:Navigator\.(?:of\(context\)\.)?push\w*|context\.(?:go|push)\w*)\(' "${DA[@]}" "${X[@]}" "${ROOTS[@]}" | win 6 0 '\bWidget\s+build\(' has
rg -l -i --pcre2 '\b(?:async\s+)?(?:function|fun|func|Future<\w+>)\s+(?:log_?in|sign_?in)\w*\b|\breturn\s+async\s+function\s+(?:log_?in|sign_?in)\b' "${X[@]}" "${ROOTS[@]}" | while IFS= read -r f; do rg -q --pcre2 'popUpTo|\breset\(|pushAndRemoveUntil|pushReplacement|\.go\(|\breplace\(|CommonActions\.reset|clearBackStack|navigateAndClear|setViewControllers|rootViewController\s*=' "$f" || rg -H -n --pcre2 '\b(?:navigate|push|pushNamed)\(' "$f"; done
rg -n --pcre2 '\bcreateDrawerNavigator\(|\bModalNavigationDrawer\(|\bdrawer\s*:\s*Drawer\(' "${X[@]}" "${ROOTS[@]}" | "${NC[@]}"

# 11. Edge-to-edge (enforced at targetSdk 35 on Android 15; opt-out ignored at 36 on Android 16): 11a the opt-out; 11b bar
#     colours that no longer apply; 11c Compose Scaffold that drops its content padding, setContent with no insets handling;
#     11d Flutter bottom-pinned content with no inset.
rg -H -n --pcre2 'windowOptOutEdgeToEdgeEnforcement' "${RES[@]}" "${X[@]}" "${ROOTS[@]}" | gate 35
rg -H -n --pcre2 '\bwindow\.(?:statusBarColor|navigationBarColor)\s*=|\bset(?:StatusBar|NavigationBar)Color\(|name="android:(?:statusBarColor|navigationBarColor)"|<StatusBar\b'"$TB"'\b(?:backgroundColor|translucent)\b|\bStatusBar\.set(?:BackgroundColor|Translucent)\(|\bsystemNavigationBarColor\s*:|\bstatusBarColor\s*:' "${KT[@]}" "${RES[@]}" "${JS[@]}" "${DA[@]}" "${X[@]}" "${ROOTS[@]}" | "${NC[@]}" | gate 35
rg -H -n -U --pcre2 '\bScaffold\((?:[^()]|\((?:[^()]|\([^()]*\))*\))*\)\s*\{\s*_\s*->' "${KT[@]}" "${X[@]}" "${ROOTS[@]}" | gate 35
rg -l --pcre2 '\bsetContent\s*\{' "${KT[@]}" "${X[@]}" "${ROOTS[@]}" | while IFS= read -r f; do rg -q --pcre2 'Scaffold\(|WindowInsets|safeDrawing|systemBars|statusBars|navigationBars|safeContent|imePadding|enableEdgeToEdge' "$f" || echo "11c $f: setContent with no Scaffold or insets"; done
rg -H -n --pcre2 '\bPositioned\([^)]*\bbottom:\s*0\b' "${DA[@]}" "${X[@]}" "${ROOTS[@]}" | win 12 2 'SafeArea\(|MediaQuery|viewPadding|padding\.bottom' lacks | gate 35

# 12. Predictive back (targetSdk 36 on Android 16: onBackPressed not called, KEYCODE_BACK not dispatched); Flutter
#     just-in-time back APIs (deprecated since 3.16); PopScope that blocks with no handler.
rg -H -n --pcre2 '\boverride\s+fun\s+onBackPressed\s*\(|\bpublic\s+void\s+onBackPressed\s*\(|\bKEYCODE_BACK\b' "${KT[@]}" "${X[@]}" "${ROOTS[@]}" | "${NC[@]}" | gate 36
rg -n --pcre2 '\bWillPopScope\(|\bonWillPop\s*:|\bNavigator\.(?:of\(context\)\.)?willPop\(|\.willPop\(\)' "${DA[@]}" "${X[@]}" "${ROOTS[@]}" | "${NC[@]}"
rg -H -n --pcre2 '\bPopScope\(' "${DA[@]}" "${X[@]}" "${ROOTS[@]}" | win 0 3 'canPop:\s*false' has | win 0 4 'onPopInvoked' lacks
:
```

A finding is a grep hit **plus** a read of the screen **plus** the gate **plus** the convention. Two blind spots are structural: the **merged** manifest and theme (a library theme can set the bar colours or the opt-out — read `build/intermediates/merged_manifests/**` and the resolved theme when a build exists), and **wrappers** (one `AppScaffold` that applies insets closes every screen built on it; one that drops them opens all of them — read the wrapper before the call sites).

**Measured** (2026-10-05, ripgrep 15.2.0; bash 3.2 and zsh give the same hit set, stdin piped or not; < 1 s). On the program's multi-stack sample (bare RN 0.82 at target 36, Expo SDK 57 / RN 0.87, Flutter 3.47, Kotlin + Compose at target 35, SwiftUI; 25 positives and 14 decoys) every positive surfaces and no decoy does: `onBackPressed` in a target-35 module, an inset-aware `Scaffold`, `LaunchedEffect` navigation, a token elevation, `router.replace` after sign-in, a keyboard-dismiss touchable, `Color.ignoresSafeArea()`, `PopScope` with a handler, a pass-through `onLongPress`. Four printed lines are left to the read step by design: a full-screen cover, a brand font on one screen (two lines), an elevation literal in a root with no token source. On every web and server fixture in `benchmarks/fixtures/*` it prints `N/A`; on `mobile-defects` (five mobile roots, measured 2026-10-10) it prints all 8 of its seeds in 28 lines and none of its three decoys — its `DEFECTS.md` § Detector measurement. On a read-only real Flutter app (440 Dart files) the first run printed 13 candidate lines, 12 false: nine Material widgets in an app with one adaptive site (now one line — the convention is the majority side), and three shared rows whose `onLongPress` is a pass-through parameter (the haptic class now skips pass-through and `==`, and counts the app's own haptic wrapper). After the fixes: 3 candidates — a `SwitchListTile.adaptive` that is the app's only adaptive control (minority, low), a raw `RefreshIndicator` that bypasses the app's haptic refresh wrapper (true, low), and a long-press whose haptic fires one call away (refuted on read).

## The 3,000-hit path

1. **Intersect** with reachability: a screen no navigator, route file or link reaches, and design galleries, are dismissed with one read and named in the coverage block.
2. **Group** by wrapper: one `AppScaffold` without insets, one base `Activity` overriding `onBackPressed`, one shared header with a custom back button is one group with N call sites.
3. **Rank** by user cost: payment, checkout, compose and sign-in screens first (a skipped back guard loses input there); then screens with bottom-pinned actions (edge-to-edge hides the button); then convention drift.
4. **Read the top 30 groups fully.**
5. **Prefer the bulk device oracle**: one `device-harness` pass per platform at the gate's API level, gesture navigation and 3-button navigation, captures every top screen at once.
6. **Ledger the rest** `Live, unreviewed (k groups / n hits)` with the command that continues them. Never `checked`.

## The detectors

Severity assumes a release build and a reachable screen. **High** only where a control is unreachable, input is lost or the app leaves a flow the user did not choose to leave; convention drift is low or medium.

| § | Class | Platform | Gate | Proof tier | Default |
|---|---|---|---|---|---|
| 1 | iOS back and modal idiom | iOS | — | D | medium; high when swipe-back is gone on a flow with no other exit |
| 2 | Material press feedback | Android | — | D | low |
| 3 | Touch target (routed) | both | — | — | — |
| 4–6 | Icon, typography, control drift from the app's own convention | both | — | S + D screenshot | low |
| 7 | Haptics against the app's own convention | both | — | S | low |
| 8 | Safe area | both | RN ≥ 0.81 for § 8a | D | medium; high when a control sits under the notch or home indicator |
| 9 | Elevation / shadow literals beside a token source | both | — | S | low |
| 10 | Navigation stack correctness | both | — | D | high (push loop, login reachable by back) |
| 11 | Edge-to-edge insets | Android | target ≥ 35 (opt-out ignored ≥ 36 on Android 16) | D | high when a control is under a bar; medium otherwise |
| 12 | Predictive back | Android | target ≥ 36 on Android 16; Flutter API deprecation any version | D | high when the dead handler guarded unsaved input or payment |

### 1. ios-hig-drift

```
BAD:   .navigationBarBackButtonHidden(true)          // custom back button: the edge swipe goes with it
       navigationController?.interactivePopGestureRecognizer?.isEnabled = false · options={{ gestureEnabled: false }}
       .fullScreenCover(…) for a short read-only page // a sheet is the idiom; full screen needs its own way out
GOOD:  system back + swipe kept; a custom leading item added with .toolbar, not by hiding the system one; .sheet for short tasks
```
**Read the code:** Is the swipe-back removal deliberate (a payment step that must not be abandoned mid-request) and is there a visible way out? Is the full-screen cover a capture flow (camera, onboarding) where full screen is the idiom? **Finding when** a screen loses the system back affordance with no equivalent, or a short task covers the whole screen with no dismiss. **Closure verb:** `apply-platform-spec --platform=ios`. **Proof:** D — `device-harness` on an iOS simulator: edge swipe from the leading edge returns to the previous screen [K: the gesture is driven from an XCUITest, `XCUICoordinate` press-and-drag].

### 2. material-spec-drift

```
BAD:   Modifier.clickable(indication = null, …) { save() }   ThemeData(splashFactory: NoSplash.splashFactory)
       <TouchableWithoutFeedback onPress={openEditor}>        // an action with no pressed state
GOOD:  default ripple; Pressable with android_ripple; TouchableWithoutFeedback only to dismiss the keyboard
```
**Read the code:** Does the surface give any other pressed state (a scale, a colour)? Is it a keyboard-dismiss backdrop (a decoy the grep already skips)? Custom components standing in for Material 3 ones (a hand-built FAB, a bottom bar) are read here too; whether the design system justifies them is cited from its ADR. **Finding when** a tappable action on Android has no pressed feedback. **Closure verb:** `apply-platform-spec --platform=android`. **Proof:** D — screenshot mid-press.

### 3. touch-target-drift — ROUTED, no verb

Owned by `mobile-a11y-scan` § 3 (detector) and the ui-ux `tap-target` axis (`expand-tap-target`). Platform minimums, cited so a routed row carries evidence: Android 48 dp × 48 dp ([Android accessibility](https://developer.android.com/guide/topics/ui/accessibility/apps)); iOS 44 pt × 44 pt ([Apple design tips](https://developer.apple.com/design/tips/), read 2026-08-21); WCAG 2.2 SC 2.5.8 24 × 24 CSS px (AA). Material components pad to 48 dp ([`precedents/mobile.md`](../../../../snippets/precedents/mobile.md) § 37). **Emits** `routed_to: mobile-a11y-scan § 3`.

### 4. platform-icon-drift · 5. platform-typography-drift · 6. per-platform-surface-drift

The convention is what the code already does, **per root**. Grep 4–6 counts adaptive sites (`Icons.adaptive`, `.adaptive(`, `showAdaptiveDialog`, `Cupertino*`, `Platform.select({ ios: … })`) against single-look sites (Material `Switch`, `showDatePicker`, `AlertDialog`, back / share / overflow glyphs) and prints the **minority** side; a root with no adaptive site prints one line — one look on both platforms is a brand decision, not a spec violation, and neither platform's guidelines forbid it.

```
BAD (root mostly adaptive):  Switch(value: v, onChanged: f)    showDatePicker(context: c, …)    Icon(Icons.share)
GOOD:                        Switch.adaptive(…)                 a platform-branched picker         Icon(Icons.adaptive.share)
```
**Read the code:** Is the minority site a deliberate exception (a brand control, a chart) or a screen built before the convention? For § 5, is the literal `fontFamily` a mark (a logo, numerals) or body text? A declared convention (ADR, `CLAUDE.md`) overrides the count. **Finding when** a screen departs from the root's convention on one platform. **Closure verbs:** § 4 `unify-platform-icon`, § 5 `apply-platform-typography`, § 6 `apply-platform-spec` (scope = surface) — each **only** when the convention is per-platform; otherwise `routed_to: /setup-project --refine (declare the convention)`. **Proof:** S (the count) + D screenshot on both platforms.

### 7. haptic-feedback-coverage

Fires only when the app already uses haptics (its own wrapper counts). Prints inline long-press handlers and raw refresh controls with no haptic in the handler window; a pass-through parameter (`onLongPress: onLongPress`) is not a handler. **Read the code:** follow the callback one call — the haptic often fires inside it. **Closure verb:** `add-haptic-feedback`. **Proof:** S; there is no published haptics-coverage standard, so this is drift from the app's own pattern only.

### 8. safe-area-handling

```
BAD:   import { SafeAreaView } from 'react-native'            // deprecated in 0.81; iOS-only, wrong under Android edge-to-edge
       VStack { …; Button("Pay") { … } }.edgesIgnoringSafeArea(.all)
GOOD:  react-native-safe-area-context (SafeAreaView / useSafeAreaInsets) · Color.blue.ignoresSafeArea() behind a VStack that keeps it
```
**Read the code:** Does the ignoring container hold controls, or only a background? Is there an inset applied further down? **Finding when** a control or text sits under the notch, the Dynamic Island, the status bar or the home indicator. **Closure verb:** `respect-safe-area`. **Proof:** D — screenshot on a notched simulator and a gesture-navigation emulator.

### 9. elevation-drift

A raw elevation or shadow literal (`defaultElevation = 6.dp`, `Modifier.shadow(8.dp)`, RN `elevation: 6`, `shadowRadius`) **where the project has an elevation token source** (an `AppElevation` object, theme tokens). No token source → no finding. The Material level values are not restated here: cite the project's tokens or `m3.material.io`. **Closure verb:** `apply-platform-spec` (scope = elevation). **Proof:** S.

### 10. navigation-pattern-drift

```
BAD:   @Composable fun Editor(nav, saved) { if (saved) nav.navigate("list") … }   // runs on every recomposition
       Widget build(…) { if (saved) Navigator.of(context).pushNamed('/list'); … } // pushes on every rebuild
       login(): await api.post(…); navigation.navigate('Home')                    // back returns to the login form
GOOD:  LaunchedEffect(saved) { if (saved) nav.navigate("list") { popUpTo("editor") { inclusive = true } } }
       WidgetsBinding.instance.addPostFrameCallback(…) or the listener · navigation.reset(…) / router.replace(…) / pushAndRemoveUntil
```
**Read the code:** Is the navigate call inside an effect, a callback or a listener the grep window did not see? After sign-in, can back reach the login form or a stale authed stack after logout? A drawer as primary navigation (`createDrawerNavigator`, `ModalNavigationDrawer`) on iOS is read against the tab-bar idiom (convention, low). **Finding when** a stack grows on recomposition or rebuild, or back crosses an auth boundary. **Severity:** high for loops and auth-boundary back; low for drawer idiom. **Fix:** effect-scoped navigation; `reset` / `replace` at auth boundaries — `routed_to: /mobile-fix` (correctness, not finish); drawer idiom → `apply-platform-spec` (scope = navigation). **Proof:** D — recompose / rebuild, then the stack depth (`adb shell dumpsys activity activities`, the navigator state); back after sign-in.

### 11. edge-to-edge-insets

Android 15 enforces edge-to-edge for apps targeting API 35: the status bar and the gesture bar are transparent and content draws behind them unless insets are applied, and `setStatusBarColor` / `R.attr#statusBarColor` are deprecated with no effect ([Android 15 behaviour changes](https://developer.android.com/about/versions/15/behavior-changes-15), updated 2026-10-01). At API 36 on Android 16, `R.attr#windowOptOutEdgeToEdgeEnforcement` is deprecated and disabled ([Android 16 behaviour changes](https://developer.android.com/about/versions/16/behavior-changes-16), updated 2026-10-01). RN 0.81 deprecated the core `SafeAreaView` for this reason, and 0.87 removed the `StatusBar` `backgroundColor` / `translucent` props (RN 0.81 and 0.87 release posts). Flutter 3.27+ apps go edge-to-edge by default on Android 15+ (docs.flutter.dev, *default-systemuimode-edge-to-edge*, updated 2026-07-31).

```
BAD:   <item name="android:windowOptOutEdgeToEdgeEnforcement">true</item>     // target 36: ignored on Android 16
       window.statusBarColor = Color.BLACK · <StatusBar backgroundColor="#0a84ff" translucent />   // no effect / removed
       Scaffold(topBar = { … }) { _ -> Column { … } }                            // content padding dropped: under the bars
       Positioned(bottom: 0, child: ElevatedButton(…))                           // under the gesture bar
GOOD:  Scaffold { padding -> Column(Modifier.padding(padding)) } · Modifier.safeDrawingPadding() · ViewCompat.setOnApplyWindowInsetsListener
       Positioned(bottom: MediaQuery.paddingOf(context).bottom, …) · SafeArea(child: …) · useSafeAreaInsets()
```
**Read the code:** Which screens rely on the opt-out today — every one of them goes edge-to-edge on Android 16 at target 36, and Play requires target 36 for updates from 2026-08-31 ([`precedents/mobile.md`](../../../../snippets/precedents/mobile.md) § 52), so the opt-out is a deadline, not a fix. Does a wrapper or theme apply insets for every screen? Does the IME push the bottom action up (`imePadding`)? **Finding when** a control or text sits under a system bar, the gesture area or the IME at the gate's target. **Severity:** high when a primary action is unreachable; medium for content under a translucent bar; low for a no-effect colour call. **Closure verb:** `respect-safe-area` (the act is applying insets). **Proof:** D — `device-harness` on an API 35 and an API 36 emulator, gesture and 3-button navigation, the screen captured with the keyboard up and down; the BAD build shows the control under the bar, the fix shows it clear.

### 12. predictive-back

For apps targeting API 36 on Android 16, `onBackPressed` is not called and `KeyEvent.KEYCODE_BACK` is not dispatched; the temporary opt-out is `android:enableOnBackInvokedCallback="false"` ([Android 16 behaviour changes](https://developer.android.com/about/versions/16/behavior-changes-16), updated 2026-10-01; [`precedents/mobile.md`](../../../../snippets/precedents/mobile.md) § 52). Flutter replaced the just-in-time back APIs — `WillPopScope`, `Navigator.willPop`, `Form.onWillPop` — with `PopScope` (`canPop` decided ahead of time, `onPopInvokedWithResult`), stable in 3.16 (docs.flutter.dev, *android-predictive-back*, updated 2026-08-01). React Native's `BackHandler` keeps working; a native `onBackPressed` override in the host activity does not (RN 0.81 post).

```
BAD:   override fun onBackPressed() { if (dirty) showDiscardDialog() else super.onBackPressed() }   // never called at target 36
       override fun onKeyDown(code, e) { if (code == KEYCODE_BACK && dirty) … }                       // never dispatched
       WillPopScope(onWillPop: () async => false, …) · PopScope(canPop: false, child: …)              // blocks back, no handler
GOOD:  onBackPressedDispatcher.addCallback(this, object : OnBackPressedCallback(dirty) { … }) · Compose BackHandler(enabled = dirty) { … }
       PopScope(canPop: !dirty, onPopInvokedWithResult: (didPop, _) { if (!didPop) confirmDiscard(); })
```
**Read the code:** What did the dead handler guard — unsaved input, a payment in flight, a multi-step flow? Is the opt-out set (then the row is a pending migration, low, with the target-36 deadline)? Does `canPop: false` give the user a way out? **Finding when** the gate holds and the back guard no longer runs, or back is blocked with no feedback. **Severity:** high when the guard protected input or money; medium otherwise; low for the opt-out still in place. **Closure verb:** `apply-platform-spec --platform=android` (scope = back). **Proof:** D — an API 36 emulator on Android 16, back gesture on the dirty screen: the BAD build leaves without the dialog, the fix shows it; Flutter `tester.binding.handlePopRoute()` in a widget test (I) as the cheap first run.

## Proof

The device oracles are `device-harness` captures at the gate's API level, on both platforms the product ships; [`proof-oracles.md`](../../../../snippets/proof-oracles.md) § Mobile holds the shared shapes (*Platform-convention capture*, *Back-gesture probe*). Each oracle **fails before the fix**. No booted device or emulator: the row is `[report-flagged]` with the exact capture to run — never PASS, never a screenshot described from source.

## Output

```
platform-conventions-audit — lanes: react-native 0.82 target 36 (rn-app/android/build.gradle:5), expo 57 / RN 0.87 target 36
                             (expo-app/app.json:33), android target 35 (android-native/app/build.gradle.kts:5), flutter 3.47
Roots: 6 · Devices: emulator-5554 (API 36, gesture nav); no iOS simulator → iOS rows Unconfirmed

1. rn-app/android/app/src/main/java/com/acme/shop/platform/CheckoutActivity.kt:9   [report-with-fix]   high
   §12 predictive back — the discard-changes guard lives in onBackPressed, never called at target 36 on Android 16.
   Proof: API 36 emulator, back gesture on a dirty checkout: leaves without the dialog (fails).
   Fix: onBackPressedDispatcher.addCallback(this, OnBackPressedCallback(dirty)) · closure_verb: apply-platform-spec --platform=android

2. rn-app/android/app/src/main/res/values/styles.xml:3                              [report-flagged]    medium
   §11 edge-to-edge opt-out at target 36 — ignored on Android 16; screens behind it draw under the bars.
   Unproven link: no API 36 capture of the affected screens. Fix: remove the opt-out; apply insets (useSafeAreaInsets).

Verification: 24 candidates → 2 findings · 1 unconfirmed · 3 hardening · 0 pre-existing · 18 refuted
Routed: §3 → mobile-a11y-scan § 3 · this skill's §10 (navigation stack) 2 rows → /mobile-fix

Class coverage:
  §1  iOS back / modal          checked (2 hits → 0 findings; 1 Unconfirmed — no simulator)
  §2  Material feedback         checked (2 hits → 0 findings)
  §3  touch target              routed (mobile-a11y-scan § 3)
  §4–6 per-platform drift        checked (5 hits / 3 roots → 0 findings; rn-app is one-look by convention)
  §7  haptics                   checked (1 hit → 0 findings)
  §8  safe area                 checked (2 hits → 0 findings)
  §9  elevation                 checked (4 hits → 0 findings; no token source in rn-app)
  §10 navigation stack          checked (3 hits → 0 findings here; 2 routed to /mobile-fix)
  §11 edge-to-edge              checked (7 hits → 1 unconfirmed)
  §12 predictive back           checked (5 hits → 1 finding)
```

`[report-with-fix]`: the gate, the screen and the convention are cited and the oracle failed at its tier. `[report-flagged]`: one link is unproven (no device at the gate's API level, a wrapper not read) and the row names the settling run. The coverage block lists **all twelve** classes on every run: `checked (k hits → m findings)` only when the grep ran on a present lane; `N/A (<reason>)` when the repo has no such surface (no Android module: § 2, 11, 12 N/A); `blocked (<reason>)` when a grep failed or a needed render is missing; `Live, unreviewed (k groups / n hits)` for a partial review.

## False positives / precedents

The verifier reads [`precedents/mobile.md`](../../../../snippets/precedents/mobile.md) and [`refute-before-report.md`](../../../../snippets/refute-before-report.md) § 4. The ones this skill meets most: every rule outside its `targetSdk` gate (§ 52) — `onBackPressed` in a target-35 module still runs; a fix located in the generated native folders of an Expo CNG project belongs in app config or a config plugin (§ 3); Material components already pad targets (§ 37); RN `marginLeft` auto-swaps in RTL (§ 38). And the platform-specific § 84–88: one look on both platforms with no adaptive site is a brand decision (§ 84); a `TouchableWithoutFeedback` that dismisses the keyboard is not an action (§ 85); `ignoresSafeArea` on a background `Color` or image is the idiom (§ 86); a `canPop: false` with `onPopInvokedWithResult` is a guarded back, not a blocked one (§ 87); a no-effect bar colour is low, never high (§ 88).

## When to run

- `/polish` on a `mobile-*` stack (with the ui-ux floor) and every whole-repo `/mobile-audit`, reporting all twelve classes.
- On any diff that raises `targetSdk` (35 and 36 are the gates), upgrades RN past 0.81 or 0.87 or Flutter past 3.27, or touches a theme, a scaffold wrapper, a back handler, a sign-in or logout path.

## Halt conditions

- Do not report a high row as confirmed until a verifier other than the run that found it has passed it through [`refute-before-report.md`](../../../../snippets/refute-before-report.md) with [`precedents/mobile.md`](../../../../snippets/precedents/mobile.md); run standalone, apply it as a separate second pass, tag those rows `self-verified`, and keep the rest as Unconfirmed, Hardening, Pre-existing or Refuted. Never drop them.
- Halt on any finding without the `<file:line>`, the platform, the gate line and the verb or fix.
- Do not mark a row `[report-with-fix]` without its capture failing at the gate's API level; no device → `SKIPPED` for the capture and `[report-flagged]` for the row, never PASS.
- Do not judge § 4–7 or § 9 without the convention line the script printed (or a declared one); no convention → a routed observation, never a verb.
- Do not invent a sixth verb; do not emit a verb on a routed row.
- Do not print "conforms" without the class-coverage block; a class whose grep did not run is `blocked`, never `checked`.

## Hard rules

- **Per-platform fix per finding** — a `both` finding produces per-platform code paths or an abstraction that handles both.
- **No iOS-styled Android, no Android-styled iOS** — each platform looks like itself where the convention is per-platform.
- **Behaviour preserved** — visual and interaction changes do not alter business logic; a back-guard migration keeps the guard's decision.
- **Per-platform build smoke** — every closure verb's commit passes on both platforms (`device-harness`), or the row stays `[report-flagged]`.

## Related

- `/polish` (§ Mobile) dispatches this skill with the ui-ux floor; `/mobile-audit` folds its coverage block into the class ledger; `/mobile-fix` closes the routed correctness rows failing-first.
- `device-harness` (this pack) — the captures at API 35 / 36 and on a notched simulator.
- `mobile-a11y-scan`, `mobile-lifecycle-scan`, `store-compliance-scan` (this pack) own the neighbouring classes; the ui-ux pack owns tokens, scale and motion.
- iOS HIG (https://developer.apple.com/design/human-interface-guidelines/) and Material 3 (https://m3.material.io/) — client-rendered pages: a figure from them is read by a human and cited with a read date, never recalled. **Deliberately absent**: a HIG tab-bar maximum, a Material 3 navigation-bar maximum and a haptics-coverage standard — none was retrievable from a citable source.
