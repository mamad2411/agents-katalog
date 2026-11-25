---
name: mobile-a11y-scan
description: Native accessibility detector for RN/Expo, Flutter, Compose, Android Views, SwiftUI and UIKit — 8 classes, each proved by the platform's a11y checker.
kind: skill
pack: mobile
allowed-tools: [Read, Grep, Glob, Bash]
---

# Skill: mobile-a11y-scan

## Premise

A screen reader user meets a native app through its accessibility tree, not its pixels: TalkBack and VoiceOver read the name, role and state of each node, move in the order the tree gives, and act through the actions it exposes. An icon button with no name is a silent "button", a `GestureDetector` is a tap target with no role, a swipe-to-delete row has no way in without a swipe, a toast is never spoken, and text pinned to one size breaks the moment the user turns the font up. Every class here is visible in source long before anyone renders the screen, on all six native stacks: React Native / Expo, Flutter, Jetpack Compose, Android Views, SwiftUI and UIKit.

**Every finding cites the source `<file:line>` + the screen that renders it + the WCAG 2.2 criterion it fails as applied to native apps (WCAG2ICT) and the platform rule (`THR-A11Y`: 44 pt iOS, 48 dp Android; engineering baseline MOB-7, MOB-10) + the checker that proved it (or the test that would settle it) + the fix in the project's own components.** A lint message or a grep hit is never a finding by itself, and "no accessibility issue found" is never printed without the class-coverage block (§ Output).

**Detect statically, prove with the platform's own checker.** Agents that were asked for accessible UI produced *more* accessibility errors, not fewer (Rabelo et al., MOBILESoft 2025, via the mobile research catalog), so "the labels were added" is never evidence: a checker run is. The proof tiers are the pack's — D (device or emulator), I (instrumented or widget test), A (shipped artifact), S (static trace) — [`precedents/mobile.md`](../../../../snippets/precedents/mobile.md) § The claim, restated. **No booted emulator or simulator means `SKIPPED`, never PASS**, and a candidate below its tier is **Unconfirmed** with the settling test, never dropped and never promoted on reading alone ([`refute-before-report.md`](../../../../snippets/refute-before-report.md) § 2, gate 6). A clean run is the automated floor: the TalkBack / VoiceOver walk at the largest font stays, and the report says so.

## The rule

A candidate is a finding when all five hold:

1. **It ships and renders.** A release build (not `__DEV__`, `kDebugMode`, `#if DEBUG`, `src/debug/`, a design gallery or a story) reaches the screen, in a state a user can reach.
2. **A real user meets it.** TalkBack or VoiceOver, Switch Access / Full Keyboard Access, the largest font or display size, the dark theme.
3. **Nothing already provides it.** The component library or a wrapper supplies the name, role, size or action (Material components pad to 48 dp — [`precedents/mobile.md`](../../../../snippets/precedents/mobile.md) § 37; a merged parent carries the label; Flutter's `SnackBar` is its own live region; precedents § 60–63).
4. **The version gate holds.** The API and its default exist on the project's versions, read from grep 0: `react-native`, `expo`, Flutter, the Compose BOM / Material 3, the iOS deployment target.
5. **The checker fired at the class's tier**, or the failure is a static fact fully visible in source (an unlabelled element with no wrapper, a literal `allowFontScaling={false}`). Otherwise it stays Unconfirmed.

## Boundaries

- **Web accessibility** (DOM, ARIA, axe, keyboard on a page) is `a11y-code-scan` and `a11y-scan` (frontend pack). DOM tooling on a native tree proves nothing; a React Native Web or Expo web target is theirs for its web build.
- **The judge** is `@ux-reviewer` (ui-ux pack): when the mobile pack is installed it dispatches this skill and owns the WCAG verdict and the fix vocabulary. Without ui-ux, this skill's output is the verdict, run standalone under the protocol (§ Halt conditions), and the delivery lane reports `UNREVIEWED(a11y) — ux-reviewer not installed (ui-ux pack)` for the human pass.
- **The visual fix** — expand a tap target, lift contrast, clarify an affordance — is the ui-ux pack's closure verbs (`ui-design-sweep`) when installed; contrast token pairs are `design-token-audit`'s.
- **RTL mirroring, hard-coded strings and locale formatting** → `i18n-scan` (frontend pack, web and mobile catalogs) when installed. A hard-coded `accessibilityLabel` literal is i18n's; the missing label is this skill's.
- **Platform conventions** (back, edge-to-edge insets, safe areas, keyboard avoidance) → `platform-conventions-audit` (this pack). **Rendered loading, empty and error states** → `ui-state-scan` (ui-ux pack, when installed); § 7 here owns only whether a state change is *spoken*.
- **`FLAG_SECURE` / `.privacySensitive` and accessibility-service data leaks** → `mobile-security-scan` (security pack, when installed); without it, tagged `security-class (owner pack not installed)`.

## Adapt to the codebase — lanes

Read every version from grep 0 and print the lanes you ran in the output header. Under Expo CNG (`android/` and `ios/` git-ignored), ripgrep skips the generated folders; the fix belongs in the JS source, which is where every class here lives anyway ([`precedents/mobile.md`](../../../../snippets/precedents/mobile.md) § 3).

| Lane | Name / role primitive | Target-size primitive | Text scaling | Lint lane (project config; keep only the rule) | Checker (tier) |
|---|---|---|---|---|---|
| **React Native** (bare, ≥ 0.82) incl. Paper, Tamagui, gluestack | `accessibilityLabel` / `aria-label`, `accessibilityRole` / `role`; touchables read child `Text` | `minWidth`/`minHeight`; `hitSlop` enlarges the touch area only | `allowFontScaling` (default on), `maxFontSizeMultiplier` | eslint-plugin-react-native-a11y 3.5.1 (2024-11-04; peer ESLint ≤ 8), § Lint lanes | RNTL 14.0.1 `getByRole(role, { name })` (I, host) |
| **Expo** (SDK 53–57) | as RN | as RN | as RN | as RN | as RN; device run through a dev build |
| **Flutter** (3.x) | `IconButton.tooltip`, `Semantics(button:, label:)`, `semanticLabel` | `MaterialTapTargetSize.padded`, `kMinInteractiveDimension` | `TextScaler`, `MediaQuery.withClampedTextScaling` | none for semantics; `flutter analyze` sees none of these classes | `meetsGuideline(…)` after `tester.ensureSemantics()` (I, host) |
| **Jetpack Compose** | `contentDescription`, `Modifier.semantics`, `clickable(role =, onClickLabel =)` | `minimumInteractiveComponentSize()` (Material 3 default) | `sp`; `LocalDensity.fontScale` | none for these classes | `enableAccessibilityChecks()` + `tryPerformAccessibilityChecks()` (D; I under Robolectric where the project runs it) |
| **Android Views** | `android:contentDescription`, `importantForAccessibility`, `ViewCompat` actions | `minWidth` / `minHeight` 48 dp | `sp` text sizes | Android lint `ContentDescription`, `ClickableViewAccessibility`, `KeyboardInaccessibleWidget`, `SpUsage`, `SmallSp` | Espresso `AccessibilityChecks.enable()` (ATF) (D) |
| **SwiftUI** | `.accessibilityLabel`, `.accessibilityAddTraits(.isButton)`, `Image(decorative:)` | `.frame(minWidth: 44, minHeight: 44)`, `.contentShape` | text styles, `@ScaledMetric`, `.custom(_:size:)` | SwiftLint has no rule for these classes this pack verified | XCUITest `performAccessibilityAudit()` (D, simulator) |
| **UIKit** | `accessibilityLabel`, `accessibilityTraits`, `accessibilityCustomActions` | 44 × 44 pt hit area | `UIFontMetrics`, `adjustsFontForContentSizeCategory` | — | as SwiftUI |

## Lint lanes

Run in a scratch directory, never in the project, and never commit the config. The React Native plugin's peer range stops at ESLint 8, so it runs from a separate ESLint 8 toolchain the user installed once (`$REFRACT_RN_A11Y_LINT`, default `~/.cache/refract/rn-a11y-lint`) — the audit never installs it. Keep only `react-native-a11y/*` ids; each message is a candidate for the § its rule maps to: `has-valid-accessibility-descriptors` → § 1 / § 2, `has-valid-accessibility-role` / `-state` / `-value` → § 2, `has-valid-accessibility-actions` → § 6, `no-nested-touchables` → § 5, `has-valid-accessibility-live-region` → § 7. Without that toolchain the lane prints `NOT-RUN (toolchain not installed — to enable: <the exact npm i>)`; the class's greps still run.

```bash
# The toolchain is installed once BY THE USER, never by this audit: T holds it, L is this run's scratch (configs, output).
T="${REFRACT_RN_A11Y_LINT:-$HOME/.cache/refract/rn-a11y-lint}"; L="$(mktemp -d "${TMPDIR:-/tmp}/mobile-a11y-lint.XXXXXX")"
if [ -x "$T/node_modules/.bin/eslint" ]; then ln -s "$T/node_modules" "$L/node_modules"
else echo "react-native-a11y lint lane NOT-RUN (toolchain not installed — to enable: mkdir -p \"$T\" && cd \"$T\" && echo '{\"private\":true}' > package.json && npm i --no-audit --no-fund eslint@8 eslint-plugin-react-native-a11y@3.5.1 @typescript-eslint/parser@7 typescript@5)"; fi
cat > "$L/rn.json" <<'EOF'
{ "root": true, "parser": "@typescript-eslint/parser", "parserOptions": { "ecmaVersion": "latest", "sourceType": "module", "ecmaFeatures": { "jsx": true } },
  "plugins": ["react-native-a11y"], "extends": ["plugin:react-native-a11y/all"],
  "rules": { "react-native-a11y/has-accessibility-hint": "off", "react-native-a11y/has-valid-accessibility-ignores-invert-colors": "off" },
  "ignorePatterns": ["**/node_modules/**", "**/__tests__/**", "**/*.test.*", "**/*.stories.*", "android/**", "ios/**"] }
EOF
[ -e "$L/node_modules" ] && for r in "${ROOTS[@]}"; do [ -f "$r/package.json" ] && ESLINT_USE_FLAT_CONFIG=false "$L/node_modules/.bin/eslint" --no-eslintrc --resolve-plugins-relative-to "$L" -c "$L/rn.json" --ext .js,.jsx,.ts,.tsx -f unix "$r"; done
for r in "${ROOTS[@]}"; do [ -x "$r/gradlew" ] && (cd "$r" && ./gradlew -q lintRelease); done   # then keep ContentDescription, ClickableViewAccessibility, KeyboardInaccessibleWidget, SpUsage, SmallSp from app/build/reports/lint-results-release.xml
```

The two rules turned off are advice, not failures: a hint is optional (missing hints are Low at most) and the invert-colours prop is cosmetic. **Measured** (2026-10-05, the program's multi-stack sample): with them on, the lane printed 12 messages, 7 of them those two rules; with them off, 5 — `has-valid-accessibility-descriptors` on 4 of the 5 unnamed or role-less React Native touchables, and `no-nested-touchables` on the one accessible container hiding a switch and a button. It saw no target size, text scaling, gesture or announcement class; the greps did.

## Pre-flight greps

Run as **one** script from the repo root. Grep **N** feeds detector **§N**; grep 0 is context. Every `rg` names its path (`.` or `"${ROOTS[@]}"`); per-file checks use `while read` with an explicit file, never a bare `xargs rg` (given no path, ripgrep reads stdin under an agent's shell and returns a silent zero or hangs). `win` keeps a hit by what the lines around it contain — the merged parent, the trait on the next line — and reads the file named on the hit. `TB` is a JSX-aware tag body: `[^>]*` stops at the `>` of `onPress={() => x}`. Any `rg` error on stderr is a failed grep, never zero hits. The mobile-root computation is the one `mobile-lifecycle-scan` uses: on a web repo it prints `N/A`, so the JSX greps never fire on DOM code.

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
   -g '!**/{test,tests,__tests__,__mocks__,mocks,fixtures,__fixtures__,testdata,e2e,integration_test,.maestro,docs,ai,storybook,.storybook}/**'
   -g '!**/*{Tests,UITests}/**' -g '!**/*.{test,spec,stories}.*' -g '!**/*_test.dart' -g '!**/*.{g,freezed,mocks}.dart' -g '!**/app_localizations*.dart' -g '!**/*.{md,mdx,lock,snap,map}')
NC=(rg -v --pcre2 '^[^:]+:\d+:\s*(//|/\*|\*(\s|/|$)|#(?!\{)|<!--)')
JS=(-g '*.{js,jsx,ts,tsx}'); KT=(-g '*.{kt,java}'); DA=(-g '*.dart'); SW=(-g '*.swift'); XL=(-g '**/res/layout*/*.xml')
TB='(?:[^>{]|\{(?:[^{}]|\{[^{}]*\})*\})*'; TG='(?:[^>]|(?<==)>)*?'   # JSX tag body; the same, lazily, for lookaheads
BAL='(\((?:[^()]++|(?1))*\))'                                        # one balanced (...) group (Dart / Kotlin call args)
# win B A PAT has|lacks — keep an `rg -n` hit when lines l-B..l+A of its file do / do not match PAT (stdin: rg -H -n output).
win() { while IFS=: read -r f l r; do s=$((l > $1 ? l - $1 : 1)); if sed -n "${s},$((l + $2))p" "$f" | rg -q -U --pcre2 "$3" -; then [ "$4" = has ] && echo "$f:$l:$r"; else [ "$4" = lacks ] && echo "$f:$l:$r"; fi; done; }

# 0. Lanes, versions and existing oracles. 0a versions; 0b a11y tests already in the repo (tests INCLUDED); 0c suppressions.
rg -n --pcre2 '"(?:react-native|expo|react-native-paper|tamagui|@gluestack-ui/[\w-]+|react-native-gesture-handler|eslint-plugin-react-native-a11y|@testing-library/react-native|@react-native-ama/core)"\s*:' -g 'package.json' "${X[@]}" "${ROOTS[@]}"
rg -n --pcre2 '^\s+(?:flutter|flutter_slidable):\s*["^>=]*\d|^\s+flutter:\s*["^>=]' -g 'pubspec.yaml' "${ROOTS[@]}"; rg -n --pcre2 'compose[-.]bom|material3|ui-test-junit4-accessibility|ui-test-accessibility|espresso-accessibility|accessibility-test-framework|IPHONEOS_DEPLOYMENT_TARGET' -g '*.{gradle,kts,toml,pbxproj,xcconfig}' "${ROOTS[@]}"
rg -l --pcre2 'performAccessibilityAudit|meetsGuideline\(|enableAccessibilityChecks\(|AccessibilityChecks\.enable\(|getByRole\(|toHaveAccessibilityValue|tryPerformAccessibilityChecks' -g '!**/{node_modules,Pods,build,.dart_tool}/**' "${ROOTS[@]}"
rg -n --pcre2 'SuppressLint\("(?:ClickableViewAccessibility|ContentDescription)"|tools:ignore="[^"]*(?:ContentDescription|SpUsage|TouchTargetSizeCheck)|eslint-disable[^\n]*react-native-a11y|swiftlint:disable[^\n]*accessibility' "${X[@]}" "${ROOTS[@]}"

# 1. Interactive element with no accessible name. 1a RN touchable with no label and no text child; 1b Flutter IconButton
#    without tooltip; 1c Flutter tap handler around an icon/image with no Semantics; 1d Compose icon with a null description
#    as the only content of a button or a tap target; 1e Android XML image controls; 1f SwiftUI icon-only Button; 1g UIKit.
rg -n -U --pcre2 '<(Pressable|Touchable(?:Opacity|Highlight|WithoutFeedback|NativeFeedback))\b(?!'"$TB"'\b(?:accessibilityLabel|aria-label|aria-labelledby|accessibilityLabelledBy)\b)(?='"$TB"'>(?:(?!</\1>|<\w*(?:Text|Typography|Label)\b)[\s\S])*</\1>)' "${JS[@]}" "${X[@]}" "${ROOTS[@]}"
rg -n -U --pcre2 '\bIconButton(?:\.\w+)?\((?!(?:[^()]|'"$BAL"')*?\btooltip\s*:)' "${DA[@]}" "${X[@]}" "${ROOTS[@]}" | "${NC[@]}"
rg -H -n -U --pcre2 '\b(?:GestureDetector|InkWell)\((?=(?:[^()]|'"$BAL"')*?\bchild\s*:\s*(?:const\s+)?(?:Icon|Image(?:\.\w+)?)\((?![^()]*semanticLabel))' "${DA[@]}" "${X[@]}" "${ROOTS[@]}" | win 3 0 '\bSemantics\(' lacks
rg -n -U --pcre2 '\bIconButton\s*\([^)]*\)\s*\{\s*Icon\([^)]*contentDescription\s*=\s*null|contentDescription\s*=\s*null[^\n]*\.(?:clickable|pointerInput)\b|\.(?:clickable|pointerInput)\b[^\n]*contentDescription\s*=\s*null' "${KT[@]}" "${X[@]}" "${ROOTS[@]}" | "${NC[@]}"
rg -n --pcre2 '<(?:ImageButton|ImageView|[\w.]*FloatingActionButton)\b(?![^>]*android:(?:contentDescription|importantForAccessibility="no))[^>]*>' "${XL[@]}" "${X[@]}" "${ROOTS[@]}"
rg -n -U --pcre2 '\bButton(?=\s*(?:\([^()]*(?:\([^()]*\)[^()]*)*\))?\s*\{\s*Image\((?:systemName:\s*)?"[^"]*"\)\s*\}|\s*\{(?:[^{}]|\{[^{}]*\})*\}\s*label:\s*\{\s*Image\((?:systemName:\s*)?"[^"]*"\)\s*\})(?!(?:\s*(?:\((?:[^()]|\([^()]*\))*\))?\s*\{(?:[^{}]|\{[^{}]*\})*\}(?:\s*label:\s*\{[^{}]*\})?)(?:\s*\.\w+\((?:[^()]|\([^()]*\))*\))*\s*\.accessibilityLabel\()' "${SW[@]}" "${X[@]}" "${ROOTS[@]}"
rg -l --pcre2 '\bsetImage\(' "${SW[@]}" "${X[@]}" "${ROOTS[@]}" | while IFS= read -r f; do rg -q --pcre2 '\baccessibilityLabel\s*=|\bsetTitle\(' "$f" || rg -H -n --pcre2 '\bsetImage\(' "$f"; done

# 2. Missing role or trait. 2a RN touchable with no role; 2b Flutter tap handler with no button semantics;
#    2c Compose clickable with no role; 2d Compose raw tap detection; 2e Views touch listener with no performClick;
#    2f SwiftUI onTapGesture with no button trait.
rg -n -U --pcre2 '<(?:Pressable|Touchable(?:Opacity|Highlight|WithoutFeedback|NativeFeedback))\b(?!'"$TB"'\b(?:accessibilityRole|role)=)' "${JS[@]}" "${X[@]}" "${ROOTS[@]}"
rg -H -n -U --pcre2 '\b(?:GestureDetector|InkWell)\((?=(?:[^()]|'"$BAL"')*?\bon(?:Tap|DoubleTap)\s*:)' "${DA[@]}" "${X[@]}" "${ROOTS[@]}" | win 3 0 '\bSemantics\(' lacks
rg -n --pcre2 '\.(?:clickable|combinedClickable)\s*(?:\{|\((?![^\n]*\brole\s*=))' "${KT[@]}" "${X[@]}" "${ROOTS[@]}" | "${NC[@]}"
rg -n --pcre2 '\bpointerInput\([^)]*\)\s*\{\s*detectTapGestures\b' "${KT[@]}" "${X[@]}" "${ROOTS[@]}" | "${NC[@]}"
rg -l --pcre2 '\bsetOnTouchListener\b|\boverride\s+fun\s+onTouchEvent\(' "${KT[@]}" "${X[@]}" "${ROOTS[@]}" | while IFS= read -r f; do rg -q 'performClick' "$f" || rg -H -n --pcre2 '\bsetOnTouchListener\b|\boverride\s+fun\s+onTouchEvent\(' "$f"; done
rg -H -n --pcre2 '\.onTapGesture\b' "${SW[@]}" "${X[@]}" "${ROOTS[@]}" | win 3 3 'accessibilityAddTraits\(\s*\.isButton|\.accessibilityAction\b' lacks

# 3. Touch target below 44 pt / 48 dp. 3a RN touchable sized inline below 44 with no hitSlop; 3b RN style entries
#    under 44 x 44 (read which touchable uses them); 3c Flutter target shrunk; 3d Compose size < 48.dp on a tap target
#    and the minimum turned off; 3e Android XML; 3f SwiftUI frame < 44 on a tap target.
rg -n -U --pcre2 '<(?:Pressable|Touchable(?:Opacity|Highlight|WithoutFeedback|NativeFeedback))\b(?!'"$TB"'\bhitSlop=)(?='"$TB"'\{[^}]*?\b(?:width|height)\s*:\s*(?:[1-3]?\d|4[0-3])\b)' "${JS[@]}" "${X[@]}" "${ROOTS[@]}"
rg -n --pcre2 '\b\w+\s*:\s*\{[^{}]*\bwidth\s*:\s*(?:[1-3]?\d|4[0-3])\b[^{}]*\bheight\s*:\s*(?:[1-3]?\d|4[0-3])\b[^{}]*\}' "${JS[@]}" "${X[@]}" "${ROOTS[@]}" | "${NC[@]}"
rg -n --pcre2 'MaterialTapTargetSize\.shrinkWrap|\bconstraints:\s*(?:const\s+)?BoxConstraints\(\s*\)|\bminimumSize:\s*(?:const\s+)?Size(?:\.square)?\(\s*(?:[1-3]?\d|4[0-7])(?:\.0)?\b' "${DA[@]}" "${X[@]}" "${ROOTS[@]}" | "${NC[@]}"
E='(?:\s*\.\s*\w+\s*(?:\((?:[^()]|\([^()]*\))*\))?\s*(?:\{[^{}]*\})?)'; SZ='\.\s*size\(\s*(?:[1-3]?\d|4[0-7])\.dp\s*[,)]'; CL='\.\s*(?:clickable|combinedClickable|toggleable|selectable)\b'
rg -n -U --pcre2 "\bModifier(?=(?:$E)*?\s*$SZ(?:[^()]|\([^()]*\))*\)?(?:$E)*?\s*$CL|(?:$E)*?\s*$CL(?:$E)*?\s*$SZ)" "${KT[@]}" "${X[@]}" "${ROOTS[@]}"
rg -n --pcre2 'LocalMinimumInteractiveComponent(?:Size\s+provides\s+(?:0\.dp|Dp\.Unspecified)|Enforcement\s+provides\s+false)' "${KT[@]}" "${X[@]}" "${ROOTS[@]}"
rg -n --pcre2 '<(?:ImageButton|Button|[\w.]*FloatingActionButton|\w[\w.]*(?=[^>]*android:(?:clickable="true"|onClick=)))\b(?=[^>]*android:layout_(?:width|height)="(?:[1-3]?\d|4[0-7])dp")(?![^>]*android:min(?:Width|Height)="(?:4[89]|[5-9]\d|\d{3})dp")' "${XL[@]}" "${X[@]}" "${ROOTS[@]}"
rg -H -n --pcre2 '\.frame\(\s*width:\s*(?:[1-3]?\d|4[0-3])(?:\.\d+)?\s*,\s*height:\s*(?:[1-3]?\d|4[0-3])(?:\.\d+)?\s*\)' "${SW[@]}" "${X[@]}" "${ROOTS[@]}" | win 6 0 '\bButton\b|onTapGesture' has

# 4. Text that does not scale. 4a RN; 4b Flutter (a clamp below 2.0 blocks 200 %); 4c Compose (dp-sized text, fontScale
#    pinned); 4d Android XML and Views; 4e SwiftUI fixed sizes and Dynamic Type caps below the accessibility sizes; 4f UIKit.
rg -n --pcre2 'allowFontScaling(?:=\{|\s*:\s*)false\b|maxFontSizeMultiplier(?:=\{|\s*:\s*)1(?:\.0)?\b(?!\.[1-9])|\.defaultProps\s*(?:\.\s*(?:allowFontScaling|maxFontSizeMultiplier)\b|=\s*\{[^}]*allowFontScaling\s*:\s*false)' "${JS[@]}" "${X[@]}" "${ROOTS[@]}" | "${NC[@]}"
rg -n --pcre2 'TextScaler\.noScaling|\bwithNoTextScaling\(|\btextScaleFactor\s*:|\bTextScaler\.linear\(\s*1(?:\.0)?\s*\)|\bwithClampedTextScaling\((?:[^()]*?)\bmaxScaleFactor:\s*1(?:\.\d+)?\b' "${DA[@]}" "${X[@]}" "${ROOTS[@]}" | "${NC[@]}"
rg -n --pcre2 '\.dp\.toSp\(\)|\bfontScale\s*=\s*1(?:\.0)?f\b' "${KT[@]}" "${X[@]}" "${ROOTS[@]}" | "${NC[@]}"
rg -n --pcre2 'android:textSize="\d+(?:\.\d+)?(?:dp|dip|px)"|setTextSize\(\s*TypedValue\.COMPLEX_UNIT_(?:DIP|PX)\b' "${XL[@]}" "${KT[@]}" "${X[@]}" "${ROOTS[@]}"
rg -n --pcre2 '\.font\(\s*\.system\(\s*size:|\.font\(\s*\.custom\([^)]*\bfixedSize:|\.dynamicTypeSize\(\s*(?:\.\.\.|\.\.<)?\s*(?:DynamicTypeSize)?\.(?:xSmall|small|medium|large|xLarge|xxLarge|xxxLarge)\b' "${SW[@]}" "${X[@]}" "${ROOTS[@]}" | "${NC[@]}"
rg -l --pcre2 '\bUIFont\.(?:systemFont|boldSystemFont|italicSystemFont|monospacedSystemFont)\(ofSize:|\bUIFont\(name:' "${SW[@]}" "${X[@]}" "${ROOTS[@]}" | while IFS= read -r f; do rg -q --pcre2 'UIFontMetrics|preferredFont\(forTextStyle' "$f" || rg -H -n --pcre2 '\bUIFont\.\w+\(ofSize:|\bUIFont\(name:' "$f"; done
rg -n --pcre2 '\badjustsFontForContentSizeCategory\s*=\s*false' "${SW[@]}" "${X[@]}" "${ROOTS[@]}"

# 5. Grouping and hiding. 5a RN accessible container with interactive children; 5b Flutter / 5c Compose / 5e SwiftUI
#    semantics cleared over interactive children; 5d Views; 5f SwiftUI asset image neither labelled nor hidden.
rg -n -U --pcre2 '<View\b(?='"$TG"'\baccessible(?:=\{true\})?(?=[\s/>]))(?='"$TG"'>(?:(?!</View>)[\s\S])*?<(?:Pressable|Touchable\w*|Switch|TextInput|Button)\b)' "${JS[@]}" "${X[@]}" "${ROOTS[@]}"
rg -n --pcre2 'importantForAccessibility=["{]*["\x27]?no-hide-descendants|\baccessibilityElementsHidden\b(?!=\{false\})' "${JS[@]}" "${X[@]}" "${ROOTS[@]}"
rg -H -n --pcre2 '\bExcludeSemantics\(|\bexcludeSemantics:\s*true|\bBlockSemantics\(' "${DA[@]}" "${X[@]}" "${ROOTS[@]}" | win 0 5 '\bonPressed\s*:|\bonTap\s*:|Button\(|TextField\(|Switch\(|Checkbox\(' has
rg -H -n --pcre2 '\bclearAndSetSemantics\b|\bsemantics\(\s*mergeDescendants\s*=\s*true\s*\)|\binvisibleToUser\(\)|\bhideFromAccessibility\(\)' "${KT[@]}" "${X[@]}" "${ROOTS[@]}" | win 0 5 '\bButton\(|\bonClick\b|\.clickable\b|\bSwitch\(|\bCheckbox\(|TextField\(' has
rg -n 'importantForAccessibility="noHideDescendants"' "${XL[@]}" "${X[@]}" "${ROOTS[@]}"
rg -H -n --pcre2 '\.accessibilityElement\(\s*children:\s*\.ignore\s*\)|\.accessibilityHidden\(\s*true\s*\)' "${SW[@]}" "${X[@]}" "${ROOTS[@]}" | win 6 0 '\bButton\b|onTapGesture|\bToggle\(|TextField\(' has
rg -n -U --pcre2 '\bImage\(\s*"[^"]+"\s*\)(?!(?:\s*\.\w+\((?:[^()]|\([^()]*\))*\))*\s*\.accessibility(?:Label|Hidden)\()' "${SW[@]}" "${X[@]}" "${ROOTS[@]}"

# 6. Custom gesture with no accessibility action — per file: a swipe / drag / dismiss gesture and no action API.
for p in "${JS[*]}~\b(?:Swipeable|ReanimatedSwipeable|PanResponder\.create|Gesture\.(?:Pan|Fling))\b~accessibilityActions|onAccessibilityAction" \
         "${DA[*]}~\b(?:Dismissible|Slidable)\(|\bonHorizontalDrag(?:End|Update)\s*:|\bonPan(?:End|Update)\s*:~customSemanticsActions|CustomSemanticsAction" \
         "${KT[*]}~\bSwipeToDismissBox\b|\banchoredDraggable\b|\bdetect(?:Horizontal)?DragGestures\b|\bItemTouchHelper\b|\bSwipeDismissBehavior\b~customActions|CustomAccessibilityAction|addAccessibilityAction|AccessibilityActionCompat|replaceAccessibilityAction" \
         "${SW[*]}~\bDragGesture\(|\.onLongPressGesture\b|\bUI(?:Swipe|Pan|LongPress)GestureRecognizer\(~\.accessibilityAction\b|accessibilityCustomActions|accessibilityAdjustableAction"; do
  IFS='~' read -r g a r <<<"$p"; g=${g#-g }
  rg -l --pcre2 "$a" -g "$g" "${X[@]}" "${ROOTS[@]}" | while IFS= read -r f; do rg -q --pcre2 "$r" "$f" || rg -H -n --pcre2 "$a" "$f" | rg -v --pcre2 '^[^:]+:\d+:\s*(?:import\b|</)'; done; done

# 7. A toast, banner or snackbar the app draws itself, with no announcement or live region — per file.
for p in "${JS[*]}~\b(?:function|const|class)\s+\w*(?:Toast|Snackbar|Banner|Notice|Flash)\b~announceForAccessibility|accessibilityLiveRegion|aria-live" \
         "${DA[*]}~\bclass\s+\w*(?:Toast|Snackbar|Banner|Notice)\b~SemanticsService\.(?:announce|sendAnnouncement)|liveRegion:\s*true" \
         "${KT[*]}~\b(?:fun|class)\s+\w*(?:Toast|Snackbar|Banner|Notice)\b~liveRegion|announceForAccessibility|accessibilityLiveRegion" \
         "${SW[*]}~\b(?:struct|class)\s+\w*(?:Toast|Snackbar|Banner|Notice)\w*\b~AccessibilityNotification|UIAccessibility\.post\(|\.updatesFrequently"; do
  IFS='~' read -r g a r <<<"$p"; g=${g#-g }
  rg -l --pcre2 "$a" -g "$g" "${X[@]}" "${ROOTS[@]}" | while IFS= read -r f; do rg -q --pcre2 "$r" "$f" || rg -H -n --pcre2 "$a" "$f"; done; done

# 8. Contrast is decided by the platform checker on a render. This lists literal text colours outside theme and token
#    files — the pairs to check first. Never a finding by itself.
T=(-g '!**/{theme,themes,tokens,design-tokens,styles/tokens}/**' -g '!**/*{colors,Colors,tokens,Tokens,theme,Theme}.*' -g '!**/res/values*/**')
rg -n --pcre2 '\bcolor\s*:\s*["\x27]#[0-9A-Fa-f]{3,8}["\x27]|\bTextStyle\([^)]*\bcolor:\s*(?:const\s+)?(?:Color\(0x|Colors\.grey)|\bText\([^\n]*\bcolor\s*=\s*Color(?:\(0x|\.(?:Gray|LightGray))|android:textColor="#|\.foregroundColor\(\s*Color\((?:red|white|hex)' "${JS[@]}" "${DA[@]}" "${KT[@]}" "${XL[@]}" "${SW[@]}" "${T[@]}" "${X[@]}" "${ROOTS[@]}" | "${NC[@]}"
```

A finding is a grep hit **plus** a read of the component and its parent **plus** the version gate **plus** the checker. Three blind spots are structural:

- **Wrappers decide.** A project `AppButton`, `IconAction` or `Tappable` that sets the role and requires a label closes every call site; one that forwards `onPress` to a bare `Pressable` opens all of them. Read each wrapper once (grep 0 lists the UI kits), then judge the call sites through it — add its name to the touchable alternation in greps 1a, 2a and 3a.
- **Names come from more than one place.** A React Native touchable reads its child `Text`; a Compose `clickable` merges its descendants' text; a Flutter `InkWell` reads its `Text` child. Greps 1a and 1c skip text children; everything else needs the read.
- **Windows and indentation are heuristics.** `win` looks 3–8 lines around a hit; a label applied further away, or a modifier chain split oddly, is the read step's.

**Measured** (2026-10-05, ripgrep 15.2.0, bash 3.2 and zsh, identical hit sets). On the program's seeded multi-stack sample (bare RN 0.82, Expo SDK 57, Flutter 3.47, Kotlin + Compose + Views at `targetSdk` 35, SwiftUI + UIKit; 58 positives and 54 decoys across the eight classes) the script runs in under 1 s, surfaces every positive and no decoy. On every web and server fixture in `benchmarks/fixtures/*` it finds no mobile root and prints `N/A`; on `mobile-defects` (five mobile roots, measured 2026-10-10) it prints all 12 of its seeds in 33 lines, and the one decoy it prints (a fixed-size monogram) is refuted by the read — its `DEFECTS.md` § Detector measurement. A first version ran 2a and 3a without `-U`, so a multi-line `<Pressable` whose `accessibilityRole` or `hitSlop` sits on a later line printed as role-less (6 false lines there). On a read-only real Flutter app (65,953 files, 440 Dart) it printed 20 lines: 3 version lines, 1 icon button with no tooltip on a design-gallery screen (a true pattern; whether the gallery ships decides), 5 `InkWell` wrappers with no button flag (true § 2 candidates — Flutter's `InkWell` exposes a tap action but no button role [V: flutter stable `ink_well.dart`, read 2026-10-05]; one group per shared wrapper), 6 `withNoTextScaling` / `TextScaler.noScaling` lines (all refuted on read: fixed-size marks and spinners, and a measurement helper), and 4 banners with no live region (Unconfirmed until the semantics test runs). A first version also printed a long-press-only `GestureDetector` as role-less; long press is exposed as an action, so § 2 now keys on tap handlers only.

## The 3,000-hit path

1. **Intersect** with reachability: a component no screen, navigator or route imports is dismissed with one read; a design gallery, a Storybook or a debug menu is dismissed with one read that shows it is not in the release navigator, and named in the coverage block.
2. **Group** by (wrapper, class): one `AppIconButton` with no required label is one group however many call sites it has; fixing the wrapper closes them.
3. **Rank** by flow: sign-in, checkout, compose and primary navigation first; then list rows and settings; then the rest. Analytics on the screens' traffic outranks code order when present.
4. **Read the top 30 groups fully.**
5. **Prefer the bulk checker at scale**: one `performAccessibilityAudit()` per top screen, one Flutter test calling `meetsGuideline` for each guideline over each top route, or one Compose / Espresso suite with the checks enabled settles whole groups at once.
6. **Ledger the rest** as `Live, unreviewed (k groups / n hits)` with the command that continues them. Never `checked`.

## Scans for

Severity assumes a release build and a reachable screen. **High** when the defect blocks a primary action (sign-in, pay, submit, navigate back) for a screen-reader or large-font user; **medium** otherwise; **low** for a missing hint or an unlabelled decorative image. Raise one step on payment, health or account flows; **critical** only with checker evidence that a primary flow cannot be completed at all.

| § | Class | WCAG 2.2 (native, WCAG2ICT) · platform | Lint id | Tier | Default |
|---|---|---|---|---|---|
| 1 | Interactive element with no accessible name | 4.1.2 (A), 1.1.1 (A) · MOB-7 | RN `has-valid-accessibility-descriptors`; Android `ContentDescription` | I (S when static) | high on primary actions, else medium |
| 2 | Missing role or trait | 4.1.2 (A) | RN `has-valid-accessibility-role`; Android `ClickableViewAccessibility` | I | medium; high for raw tap detection with no semantics |
| 3 | Touch target below 44 pt / 48 dp | 2.5.8 (AA, 24 px) · `THR-A11Y` 44 pt / 48 dp | — | I / D | medium; high when the control is a primary action |
| 4 | Text that does not scale | 1.4.4 (AA) · MOB-10 | Android `SpUsage`, `SmallSp` | S + D (clipping) | high when app-wide; medium per element |
| 5 | Grouping, hiding and reading order | 1.3.1 (A), 1.3.2 (A), 4.1.2 (A) | RN `no-nested-touchables` | I / D | high when an interactive child is hidden; low for a decorative image left in the tree |
| 6 | Custom gesture with no accessibility action | 2.5.1 (A), 2.1.1 (A) | RN `has-valid-accessibility-actions` | I | high when the gesture is the only path; medium when a menu also offers it |
| 7 | Status or async result not announced | 4.1.3 (AA) | RN `has-valid-accessibility-live-region` | I | medium; high for errors on submit |
| 8 | Contrast on native screens | 1.4.3 (AA), 1.4.11 (AA) | — | D only | medium; high for body text below 4.5 : 1 |

### 1. Interactive element with no accessible name

```
BAD:   <Pressable onPress={add}><Icon name="cart" /></Pressable>          IconButton(icon: const Icon(Icons.delete), onPressed: f)
       IconButton(onClick = onBack) { Icon(Icons.AutoMirrored.Filled.ArrowBack, contentDescription = null) }
       <ImageButton android:src="@drawable/ic_delete" />                    Button { fav() } label: { Image("heart_outline_24") }
GOOD:  <Pressable accessibilityRole="button" accessibilityLabel="Add to cart" …>      IconButton(tooltip: 'Delete', …)
       Icon(…, contentDescription = stringResource(R.string.back))       android:contentDescription="@string/delete"
       Button { fav() } label: { Image("heart_outline_24") }.accessibilityLabel("Favourite")
```
**Read the code:** Does a child `Text`, a merged parent (`Row(Modifier.clickable{…}){ Icon(null); Text("Settings") }`) or a wrapper supply the name? Is the SwiftUI image an SF Symbol whose derived name is adequate (the audit's `sufficientElementDescription` decides; a custom asset name such as "heart_outline_24" never is) [K: SF Symbol derived labels]? Is the label a real word in the user's language, not "icon", "button" or a file name? **Finding when** the checker reports an unnamed or insufficiently described control, or the element and every possible label source are visible in source and absent. **Severity:** high on primary or destructive actions, else medium. **Proof:** RNTL `screen.getByRole('button', { name: 'Add to cart' })` fails first; Flutter `meetsGuideline(labeledTapTargetGuideline)`; Compose / Espresso ATF; `performAccessibilityAudit(for: .sufficientElementDescription)`.

### 2. Missing role or trait

```
BAD:   <Pressable onPress={open}><Text>{title}</Text></Pressable>         GestureDetector(onTap: fav, child: const Icon(Icons.favorite))
       Box(Modifier.size(32.dp).clickable { fav() })                       Modifier.pointerInput(Unit) { detectTapGestures(onTap = { play() }) }
       view.setOnTouchListener { _, _ -> open(); true }                    Image(systemName: "star").onTapGesture { rate() }
GOOD:  role="button" · Semantics(button: true, …) · clickable(role = Role.Button) · performClick() · Button { rate() } or .accessibilityAddTraits(.isButton)
```
**Read the code:** Does the component set a role internally (Paper, gluestack and core `Button` do; a bare `Pressable` does not)? Is `pointerInput` the only handler — then the node has no click action at all and the element is invisible to TalkBack, which is § 1 and § 2 at once (high)? Does a Views touch listener call `performClick()`, and was `ClickableViewAccessibility` suppressed (grep 0c)? **Finding when** the checker reports a missing trait, or the screen reader announces the element without "button". **Severity:** medium; high for raw tap detection with no semantics. **Proof:** RNTL `getByRole('button', …)` fails first; Flutter `tester.getSemantics(find.byIcon(…))` lacks the button flag [K: `matchesSemantics(isButton: true)`]; ATF; audit `.trait`.

### 3. Touch target below 44 pt / 48 dp

```
BAD:   <TouchableOpacity style={{ width: 28, height: 28 }}>                 icon: { width: 24, height: 24 }  // used by a Pressable
       IconButton(constraints: const BoxConstraints(), padding: EdgeInsets.zero, …)   tapTargetSize: MaterialTapTargetSize.shrinkWrap
       Modifier.size(32.dp).clickable { … }         LocalMinimumInteractiveComponentSize provides 0.dp
       <ImageButton android:layout_width="32dp" …>   Button { … }.frame(width: 24, height: 24)
GOOD:  minWidth/minHeight 44 (iOS) / 48 (Android) · Material defaults · Modifier.minimumInteractiveComponentSize() · .frame(minWidth: 44, minHeight: 44).contentShape(Rectangle())
```
**Read the code:** Is the small element inside a 48 dp Material container (precedents § 37)? Is `hitSlop` the only enlargement on React Native — it enlarges the touch area, not the accessibility frame the checker measures, so it stays Unconfirmed until the checker runs? Does the minimum apply per platform (44 pt iOS, 48 dp Android, `THR-A11Y`)? Inline text links are exempt. **Finding when** the checker reports a target below the platform minimum on a control a user must hit. **Severity:** medium; high on a primary action or a destructive control next to another target. **Proof:** Flutter `meetsGuideline(androidTapTargetGuideline)` and `iOSTapTargetGuideline` (48 × 48 and 44 × 44); ATF touch-target check; audit `.hitRegion`.

### 4. Text that does not scale

```
BAD:   <Text allowFontScaling={false}>   maxFontSizeMultiplier={1}       builder: (c, child) => MediaQuery.withNoTextScaling(child: child!)
       LocalDensity provides Density(density, fontScale = 1f)            fontSize = with(LocalDensity.current) { 14.dp.toSp() }
       android:textSize="14dp"            .font(.system(size: 13))        .font(.custom("Inter", fixedSize: 15))
       .dynamicTypeSize(...DynamicTypeSize.large)                        UIFont.systemFont(ofSize: 15)  // no UIFontMetrics
GOOD:  sp · text styles · .custom(_:size:) (scales with body [K]) · @ScaledMetric · UIFontMetrics + adjustsFontForContentSizeCategory · a clamp ≥ 2.0
```
**Read the code:** Is the scope app-wide (a root `builder:`, a theme-level `Density`, a global default) — high — or one fixed-size mark (a badge, an avatar initial, a spinner slot) that must not grow (precedents § 61)? Does a clamp below 2.0 stop body text reaching 200 %? Does the text clip or truncate at the largest size instead of wrapping? **Finding when** body or control text cannot reach 200 %, or clips at the largest setting. **Severity:** high when app-wide; medium per element. **Proof:** static fact for a literal pin; for clipping, a D-tier render at the largest size — `adb shell settings put system font_scale 2.0`, iOS simulator `xcrun simctl ui booted content_size accessibility-extra-extra-extra-large` [K], audit `.dynamicType` and `.textClipped`; Flutter test with `TextScaler.linear(2.0)`.

### 5. Grouping, hiding and reading order

```
BAD:   <View accessible={true}> … <Switch/> <Pressable>Reset</Pressable> </View>     // children unreachable
       ExcludeSemantics(child: Row(children: [Text(total), TextButton(onPressed: cancel, …)]))
       Row(Modifier.clearAndSetSemantics { contentDescription = "Order 42" }) { …; Button(onClick = cancel) { … } }
       HStack { Text(total); Button("Remove", action: remove) }.accessibilityElement(children: .ignore)
       Image("banner_promo")   // decorative, read aloud by asset name
GOOD:  group static content only (rating stars, a price with its label) · Image(decorative:) / .accessibilityHidden(true) · accessible={false} on decorative wrappers
```
**Read the code:** Is every node the merge or clear hides non-interactive? Does the merged label say everything the children said? Is the visual order the reading order (RN `experimental_accessibilityOrder`, SwiftUI `.accessibilitySortPriority`)? **Finding when** an interactive child is unreachable, or the checker's parent-child or element-detection audit fails. **Severity:** high for a hidden control; low for a decorative image left in the tree. **Proof:** RNTL query for the child fails; Flutter semantics test; ATF; audit `.parentChild` / `.elementDetection`; a TalkBack / VoiceOver walk (D) for order.

### 6. Custom gesture with no accessibility action

```
BAD:   <Swipeable renderRightActions={…delete…}>              Dismissible(onDismissed: (_) => delete(), …)
       SwipeToDismissBox(state, backgroundContent = { … }) { … }    ItemTouchHelper(…onSwiped…)    .gesture(DragGesture().onEnded { … delete() })
GOOD:  accessibilityActions + onAccessibilityAction · Semantics(customSemanticsActions: {…}) · Modifier.semantics { customActions = … }
       ViewCompat.addAccessibilityAction(row, "Delete") { … } · .accessibilityAction(named: "Delete") { … } · accessibilityCustomActions
```
**Read the code:** Is the swipe the only way to the action, or does a visible button or long-press menu offer it too? Does the library expose actions itself (SwiftUI `.swipeActions` [K]; Flutter's `Dismissible` exposes none [V: flutter stable `dismissible.dart`, read 2026-10-05])? **Finding when** an action is reachable only by a path-based or multi-finger gesture. **Severity:** high when it is the only path; medium when duplicated elsewhere. **Proof:** invoke the action through the accessibility API in a test — RNTL `fireEvent(row, 'accessibilityAction', { nativeEvent: { actionName: 'delete' } })` [K], Compose `performSemanticsAction` on `SemanticsActions.CustomActions` [K], audit `.action`.

### 7. Status or async result not announced

```
BAD:   export function CartToast({ message }) { return <Animated.View>…<Text>{message}</Text></Animated.View> }
       class SavedToast extends StatelessWidget …    fun SavedBanner(…) { AnimatedVisibility(visible) { Text(message) } }    struct ToastView: View
GOOD:  accessibilityLiveRegion="polite" + AccessibilityInfo.announceForAccessibility · Semantics(liveRegion: true) / SemanticsService.sendAnnouncement
       Modifier.semantics { liveRegion = LiveRegionMode.Polite } · AccessibilityNotification.Announcement(message).post()
```
**Read the code:** Does the message appear without focus moving to it (a toast, a banner that appears, an inline error after submit, a cart count)? Does the platform component already announce (Flutter's `SnackBar` wraps its content in a live region [V: flutter stable `snack_bar.dart`]; Material 3 `Snackbar` [K])? A persistent banner present on first render needs no announcement; one that appears later does. `SemanticsService.announce` is deprecated after Flutter 3.35 for `sendAnnouncement` [V: flutter stable `semantics_service.dart`]. **Finding when** a status change the user must know about is never spoken. **Severity:** medium; high for a submit error or a lost-connection banner on a write flow. **Proof:** RNTL / jest spy on `AccessibilityInfo.announceForAccessibility` or assert the live-region prop; Flutter semantics test asserting the live-region flag; Compose semantics assertion on `LiveRegion` [K]; on device, the TalkBack / VoiceOver walk (D).

### 8. Contrast on native screens

Contrast depends on the rendered pair, the theme and the state; grep 8 only lists literal text colours outside theme and token files, as the pairs to check first. **Finding when** the platform checker reports a pair below 4.5 : 1 for text (3 : 1 large text and non-text) on a rendered screen. Without a render, every row is `blocked (no harness)` — never `checked`. **Severity:** medium; high for body text on a primary flow. **Proof:** Flutter `meetsGuideline(textContrastGuideline)`; ATF contrast check; audit `.contrast`; run in light and dark themes.

## Proof — the checkers

The oracle shapes and the whole-class variants are in [`proof-oracles.md`](../../../../snippets/proof-oracles.md) § Mobile (the native a11y checker, the name and role query, the largest-size render); `device-harness` (this pack) boots the device and captures the tree and screenshots. Verified 2026-10-05 against each primary source:

```text
RN       @testing-library/react-native 14.0.1: await render(<Screen/>); screen.getByRole('button', { name: 'Add to cart' })      (I, host)
Flutter  final h = tester.ensureSemantics(); await expectLater(tester, meetsGuideline(androidTapTargetGuideline));
         … iOSTapTargetGuideline · labeledTapTargetGuideline · textContrastGuideline; h.dispose();                                 (I, host)
Compose  androidx.compose.ui:ui-test-junit4-accessibility (Compose ≥ 1.8.0): composeTestRule.enableAccessibilityChecks();
         composeTestRule.onRoot().tryPerformAccessibilityChecks()                                                                   (D)
Views    androidx.test.espresso:espresso-accessibility 3.7.0 → AccessibilityChecks.enable().setRunChecksFromRootView(true);
         ATF com.google.android.apps.common.testing.accessibility.framework:accessibility-test-framework 4.1.1 (Google Maven)       (D)
iOS      XCUIApplication().performAccessibilityAudit(for: [.sufficientElementDescription, .hitRegion, .trait, .action, .parentChild,
         .dynamicType, .textClipped, .contrast, .elementDetection])   — iOS 17 / Xcode 15 and later                                (D, simulator)
```

Each test **fails before the fix**; a test written after the fix that passes on the unfixed code proves nothing. Run every screen in each state it has (loading, empty, error, content), at the largest font, in dark theme and on both platforms the product ships to. No booted emulator or simulator: the D rows are `SKIPPED (no device)` and the finding is `[report-flagged]` with the test written out — never PASS. Host-runnable RNTL and Flutter tests still run.

## Output

```
mobile-a11y-scan — lanes: react-native 0.82 (rn-app/package.json:6), expo SDK 57 / react-native 0.87 (expo-app/package.json:5,12),
                    flutter 3.47 (flutter_app/pubspec.yaml:4), compose + views (android-native/app), swiftui + uikit (ios-app)
Roots: 6 · Lint: react-native-a11y 5 messages (2 rules off)    Device: none → Compose / Views / iOS checker rows SKIPPED (no device)

Findings: 2 · Unconfirmed: 1

1. flutter_app/lib/a11y/app_shell.dart:10                                     [report-with-fix]   high
   §4 text pinned app-wide — MaterialApp builder wraps every route in MediaQuery.withNoTextScaling (Flutter 3.47).
   Proof: test/a11y/text_scale_test.dart pumps ShellApp under TextScaler.linear(2.0) and asserts
   MediaQuery.textScalerOf(context).scale(14) == 28 — fails (14). Fix: drop the wrapper; clamp with withClampedTextScaling(maxScaleFactor: 2.0) if layout needs a bound.

2. rn-app/src/a11y/ProductCard.tsx:9                                          [report-with-fix]   high
   §1 + §3 icon-only "add to cart" with no name and a 24 × 24 target (style s.icon, :30). Proof: RNTL
   getByRole('button', { name: 'Add to cart' }) throws (fails first). Fix: accessibilityRole="button" accessibilityLabel="Add to cart",
   minWidth/minHeight 48 in the shared style.

3. android-native/app/src/main/java/com/acme/notes/a11y/OrderRow.kt:14        [report-flagged]    high
   §5 clearAndSetSemantics hides the Cancel button inside the row. Unproven link: no emulator. Settling run:
   composeTestRule.enableAccessibilityChecks(); onNodeWithText("Cancel").assertExists() under useUnmergedTree = false.
   Fix: mergeDescendants on the text only; keep the button its own node.

Verification: 41 candidates → 2 findings · 1 unconfirmed · 6 hardening · 0 pre-existing · 32 refuted
Routed: hard-coded label text → i18n-scan (frontend pack not installed: N/A)

Class coverage:
  §1  accessible name             checked (11 hits → 1 finding)
  §2  role / trait                checked (10 hits → 0 findings; 4 folded into §1 rows)
  §3  target size                 checked (9 hits → 1 finding, merged with §1 above)
  §4  text scaling                checked (10 hits → 1 finding)
  §5  grouping / hiding           checked (6 hits → 1 unconfirmed)
  §6  gesture actions             checked (6 hits → 0 findings; 6 Unconfirmed folded into the device gap)
  §7  announcements               checked (4 hits → 0 findings; 4 Unconfirmed)
  §8  contrast                    blocked (no harness: 3 literal colour pairs listed for the checker)
```

`[report-with-fix]`: the screen, the version gate and the checker's failure are cited and the fix is local. `[report-flagged]`: one link is unproven (no device, a wrapper not read, an SF Symbol's derived name), and the row names it and the settling test. The coverage block lists **all eight** classes on every run: `checked (k hits → m findings)` only when the grep ran on a present lane; `N/A (<reason>)` only when the repo has no such surface; `blocked (<reason>)` when a grep failed, a file could not be read, or the class needs a render that did not happen; `Live, unreviewed (k groups / n hits)` for a partial review.

## False positives / precedents

The verifier reads [`precedents/mobile.md`](../../../../snippets/precedents/mobile.md) (§ 1–8 posting rules, § 37 Material 48 dp padding) and [`refute-before-report.md`](../../../../snippets/refute-before-report.md) § 10 (the accessibility column of the gate table). The ones this skill meets most, each with the evidence that flips it back: names from structure (§ 60); fixed-size marks while body text scales (§ 61); decorative content hidden on purpose (§ 62); library-owned semantics (§ 63); a persistent banner present on first render (§ 64); hints are optional (§ 65); not a native tree (§ 66).

## When to run

- On any diff that adds or changes a screen, a touchable or tap handler, an icon button, a list row with a swipe, a toast or banner, a text style or theme, or a font-scale setting — the `/mobile-audit` dispatch signal.
- On every whole-repo `/mobile-audit`, reporting all eight classes; `@ux-reviewer` dispatches it on mobile diffs when the ui-ux pack is installed, and `lane-mobile` (delivery pack, when installed) runs it on T2/T3 UI changes.
- Before a release that changes navigation or theming, and when a user reports "TalkBack / VoiceOver can't …" or large-font breakage.

## Halt conditions

- Do not report a high row as confirmed until a verifier other than the run that found it has passed it through [`refute-before-report.md`](../../../../snippets/refute-before-report.md) with [`precedents/mobile.md`](../../../../snippets/precedents/mobile.md). Under `/mobile-audit` or `@ux-reviewer` that happens in their verification phase; run standalone, apply the protocol as a separate second pass, tag those rows `self-verified`, and list the rest as Unconfirmed, Hardening, Pre-existing or Refuted. Never drop them.
- Halt on any finding without the `<file:line>`, the screen, the WCAG criterion or platform rule, and the fix.
- Do not mark a row `[report-with-fix]` without its checker failing at the class's tier, or a static fact fully visible in source (§ The rule, 5). No emulator or simulator → `SKIPPED` for the device rows and `[report-flagged]` for the finding — never PASS.
- Do not accept "the labels were added" or a lint-clean run as proof; run the checker.
- Do not run DOM tooling (axe, Lighthouse, Playwright) on a native screen, and do not judge a web target here.
- Do not print "no accessibility issue found" without the class-coverage block; § 8 without a render is `blocked`, never `checked`.
- Do not re-derive a class another skill owns (§ Boundaries). Route it.

## Related

- `@ux-reviewer` (ui-ux pack, when installed) dispatches this skill on mobile work and judges its findings; `/mobile-audit` folds its coverage block into the class ledger; `/mobile-fix` closes the findings failing-first and re-runs this detector on the patched lines.
- `device-harness` (this pack) runs the D-tier checkers and the largest-font render; `platform-conventions-audit` and `mobile-perf-scan` (this pack) own the neighbouring classes.
- `a11y-code-scan` and `a11y-scan` (frontend pack) are the web counterparts; `i18n-scan` (frontend pack) owns label text and RTL.
- `rules/mobile-principles.md` (this pack) holds the accessibility MUSTs this detector checks against; engineering baseline MOB-7 and MOB-10 and `THR-A11Y` are the thresholds.
