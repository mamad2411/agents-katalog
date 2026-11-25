---
name: mobile-perf-scan
description: Mobile performance detector for RN/Expo, Flutter, Compose and SwiftUI — lists, identity, render waste, main-thread blocking, image decode, startup and leaks, measured in release builds.
kind: skill
pack: mobile
allowed-tools: [Read, Grep, Glob, Bash]
---

# Skill: mobile-perf-scan

## Premise

A phone has one UI thread, a frame budget of 16.7 ms at 60 Hz (8.3 ms at 120 Hz), a memory ceiling the OS enforces by killing the process, and a user who judges the app in its first second. Most of what breaks those budgets is written in source: a list that builds every row up front, a row whose identity changes on every update, a parent that rebuilds the whole screen per scroll pixel, a disk or network read on the main thread, a 12-megapixel photo decoded into a 64-point thumbnail, five SDKs started before the first frame, and a listener that outlives its screen and keeps it alive. This skill finds those shapes on React Native / Expo, Flutter, Jetpack Compose and Android Views, SwiftUI and UIKit — **version-gated**, because 2025–2026 turned many textbook findings into decoys (Compose strong skipping, the React Compiler, FlashList v2, Hermes V1, `InteractionManager`'s removal).

**Every finding cites the code `<file:line>` + the screen or launch path that runs it + the version gate (lockfile or build-file line) + the oracle at its tier with its build type and device, or the command that would settle it + the fix, named in `rules/render-discipline.md`'s closure verbs where one applies.** A grep hit is never a finding, and a number never comes from anywhere but a tool ([`refute-before-report.md`](../../../../snippets/refute-before-report.md) § 4, precedent 3). "No performance defect found" is never printed without the class-coverage block (§ Output).

**Existence by invariant, cost by statistics** ([`proof-oracles.md`](../../../../snippets/proof-oracles.md) § Mobile). A leak, a main-thread tripwire or an oversized-decode log is a run-invariant check: it fails or it does not. A cost (frames, launch time, render counts) is measured on a **release or profile build**, on a named device, with repeated runs — `THR-PERF-REGRESSION`: at least 10 runs a side, a 10 % threshold, an interval that excludes zero. A figure from a debug build, a JIT Flutter run or one sample is refuted, not scaled. **No booted device or emulator means `SKIPPED`, never PASS**, and a candidate below its tier is **Unconfirmed** with the settling command ([`precedents/mobile.md`](../../../../snippets/precedents/mobile.md) § The claim, restated).

## The rule

A candidate is a finding when all five hold:

1. **It ships and runs on a hot path.** A release build (not `__DEV__`, `kDebugMode`, `src/debug/`, a mock API, `tool/`), reached from launch, a list binding, a scroll, an animation or a user tap — the path decides severity.
2. **The version gate holds** ([`precedents/mobile.md`](../../../../snippets/precedents/mobile.md) § 32–36, § 51, § 53, § 58): the React Compiler is off, Kotlin < 2.0.20 or strong skipping disabled, the FlashList major, the `react-native` version, the Swift default isolation — read from grep 0.
3. **N is unbounded or large.** The list comes from a fetch, a query, pagination or user data — not an enum or about 20 static rows (§ 36). The image is a camera or remote photo, not an icon. The JSON is a payload, not a config file.
4. **Nothing neutralizes it.** A library owns the lifecycle (Glide with a fragment, Coil in Compose, `cached_network_image`, Reanimated worklets on the UI thread), a wrapper resizes, a parent disposes, a Worker or IO dispatcher runs the call.
5. **The oracle fired at the class's tier**, release build, named device — or the candidate stays Unconfirmed.

## Boundaries

- **The closure verbs** for § 1–§ 3 are `rules/render-discipline.md`'s (this pack): `virtualize-list`, `memoize`, `scope-state-down`, `extract-const-subtree`, `scope-animation`, `split-store-selector`. This skill is the detector those 8 detectors lacked; it emits no competing verb.
- **The measurer and ranker** is `@device-performance-auditor` (this pack): it owns *that* a frame, a launch or a footprint is slow, on which device, against which budget (MOB-9). This skill hands it each finding with its oracle; a cost claim the auditor has not measured stays Unconfirmed.
- **App size** (minify, R8, assets, 16 KB alignment) → `app-size-scan` and `/optimize-bundle` (this pack). **Lifecycle-scoped work** (`GlobalScope`, collection without `repeatOnLifecycle`, wake locks, background work) → `mobile-lifecycle-scan`, which routes every listener, observer, controller and subscription leak here (§ 7).
- **Sync TurboModule calls and bridge threading** → `native-bridge-audit` (this pack). **Crash-prone code** (force-unwraps, `!!`, unhandled rejections) and **concurrency** (data races, Swift escape hatches) → the code-quality pack's correctness detector when installed; without it, `N/A (owner pack code-quality not installed)`.
- **Web vitals** (LCP, CLS, INP, hydration) → the frontend and performance packs. **Server latency** behind the API → `performance-optimizer` (performance pack, when installed); without it, the client-side measurement is reported and the server cause stays Unconfirmed.

## Adapt to the codebase — lanes

Read the versions grep 0 prints before applying any row, and print the lanes you ran. Every gate below is a precedent the verifier re-checks.

| Lane | List primitive | Identity | Render-waste gate | Off-main primitive | Lint lane (project config; keep only the rule) | Cost oracle |
|---|---|---|---|---|---|---|
| **React Native** (≥ 0.82, New Architecture only; Hermes V1 default from 0.84) | `FlatList` / `SectionList`, FlashList v2 (new arch only; `estimatedItemSize` removed) | `keyExtractor`; no `key` inside a FlashList item | React Compiler on ⇒ missing memo is noise (§ 33) | `requestIdleCallback`; `InteractionManager` no-op from 0.80, removed in 0.87 (§ 51) | `react-hooks/exhaustive-deps`; eslint-plugin-react-perf `jsx-no-new-*-as-prop` | Reassure 1.6.0 `measureRenders` (I); Flashlight (Android) |
| **Expo** (SDK 53–57) | as RN; `expo-image` with `recyclingKey` | as RN | `experiments.reactCompiler` in app config | as RN | as RN | as RN; release via a dev build or EAS |
| **Flutter** (3.x, Impeller) | `ListView.builder`, slivers | `Key` on reorderable / animated rows | `const`, scoped `setState`, `AnimatedBuilder` child | `Isolate.run`, `compute` | `flutter analyze` (very_good_analysis enables `cancel_subscriptions`; `close_sinks` is opt-in in every set) | `flutter drive --profile` + `traceAction` (D); `debugInvertOversizedImages` (I) |
| **Jetpack Compose** | `LazyColumn` / `LazyRow` | `items(list, key = { it.id })` — no lint rule exists, grep 2d fills it | strong skipping default from Kotlin 2.0.20 (§ 32) | `Dispatchers.IO`, WorkManager | Compose lint `FrequentlyChangingValue`, `ConstantContentStateKeyInItemsCall`; compose-rules 0.6.7 | Macrobenchmark 1.5.0 `FrameTimingMetric` (D); compiler metrics |
| **Android Views** | `RecyclerView` + `DiffUtil` | stable ids | `notifyDataSetChanged` | as Compose | lint `NotifyDataSetChanged`, `DrawAllocation`, `StaticFieldLeak`, `HandlerLeak`, `ApplySharedPref`, `WrongThread` | Macrobenchmark; `dumpsys gfxinfo <pkg> framestats` |
| **SwiftUI / UIKit** | `List`, `LazyVStack`, diffable data source | `Identifiable`, unique `id:` | `@Observable` / `@StateObject`, not `@ObservedObject` created in place | `Task.detached`, `@concurrent`; Swift 6.2 default MainActor (§ 58) | SwiftLint `weak_delegate`, `discarded_notification_center_observer` (opt-in) | `XCTApplicationLaunchMetric` (iOS 13+), Instruments; Thread Performance Checker in the test plan (D) |

## Pre-flight greps

Run as **one** script from the repo root. Grep **N** feeds detector **§N**; grep 0 is context. Every `rg` names its path (`.` or `"${ROOTS[@]}"`); per-file checks use `while read` with an explicit file, never a bare `xargs rg`. `win` keeps a hit by what the lines around it contain — the Worker above a blocking call, the `remember` inside a lazy item, the release after an acquire. The mobile-root computation is `mobile-lifecycle-scan`'s: on a web repo the script prints `N/A`, so the list and listener greps never fire on DOM code. A line printed with a `6b` tag is a per-module check; the rest are grep hits. Any `rg` error on stderr is a failed grep, never zero hits.

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
X=(-g '!**/{node_modules,Pods,build,.gradle,.dart_tool,.expo,DerivedData,dist,vendor,.cxx}/**' -g '!**/src/{test,androidTest,debug,benchmark}/**'
   -g '!**/{test,tests,__tests__,__mocks__,mocks,fixtures,__fixtures__,testdata,e2e,integration_test,.maestro,docs,ai,storybook,.storybook,tool,bin}/**'
   -g '!**/*{Tests,UITests}/**' -g '!**/*.{test,spec,stories,perf-test}.*' -g '!**/*_test.dart' -g '!**/*.{g,freezed,mocks}.dart' -g '!**/app_localizations*.dart' -g '!**/*.{md,mdx,lock,snap,map}')
NC=(rg -v --pcre2 '^[^:]+:\d+:\s*(//|/\*|\*(\s|/|$)|#(?!\{)|<!--)')
JS=(-g '*.{js,jsx,ts,tsx}'); KT=(-g '*.{kt,java}'); DA=(-g '*.dart'); SW=(-g '*.swift'); OC=(-g '*.{m,mm}')
TB='(?:[^>{]|\{(?:[^{}]|\{[^{}]*\})*\})*'; BAL='(\((?:[^()]++|(?1))*\))'
# win B A PAT has|lacks — keep an `rg -H -n` hit when lines l-B..l+A of its file do / do not match PAT (multi-line aware).
win() { while IFS=: read -r f l r; do s=$((l > $1 ? l - $1 : 1)); if sed -n "${s},$((l + $2))p" "$f" | rg -q -U --pcre2 "$3" -; then [ "$4" = has ] && echo "$f:$l:$r"; else [ "$4" = lacks ] && echo "$f:$l:$r"; fi; done; }

# 0. Version gates: React Compiler, FlashList major, Reanimated, Kotlin (strong skipping from 2.0.20), Compose compiler
#    flags, Flutter, Swift language mode and default isolation, baseline-profile / benchmark wiring, Reassure.
rg -n --pcre2 '"(?:react-native|expo|react|@shopify/flash-list|react-native-reanimated|babel-plugin-react-compiler|react-native-fast-image|expo-image|reassure)"\s*:\s*"' -g 'package.json' "${X[@]}" "${ROOTS[@]}"
rg -n --pcre2 '"reactCompiler"\s*:\s*true|babel-plugin-react-compiler|\breactCompiler\s*:\s*true' -g 'app.json' -g 'app.config.*' -g 'babel.config.*' "${X[@]}" "${ROOTS[@]}"
rg -n --pcre2 'org\.jetbrains\.kotlin[\w.:-]*"?\)?\s*version\s*"[\d.]+"|^\s*kotlin\s*=\s*"[\d.]+"|StrongSkipping|strongSkipping|ComposeFeatureFlag|reportsDestination|metricsDestination|androidx\.baselineprofile|profileinstaller|benchmark-macro' -g '*.{gradle,kts,toml}' "${ROOTS[@]}"
rg -n --pcre2 '^\s+flutter:\s*["^>=]' -g 'pubspec.yaml' "${ROOTS[@]}"; rg -n --pcre2 'SWIFT_VERSION|SWIFT_DEFAULT_ACTOR_ISOLATION|SWIFT_STRICT_CONCURRENCY|defaultIsolation' -g '*.{pbxproj,xcconfig}' -g 'Package.swift' "${ROOTS[@]}"

# 1. Unvirtualized list over data. 1a RN ScrollView + .map (UPPER_CASE constant arrays skipped); 1b Flutter ListView(children:)
#    and a scroll view around a Column built from data; 1c Compose Column/Row + forEach in a scroll; 1d SwiftUI eager stack.
rg -n -U --pcre2 '<ScrollView\b(?='"$TB"'>(?:(?!</ScrollView>|<(?:FlatList|FlashList|SectionList|VirtualizedList)\b)[\s\S]){0,400}?\{\s*(?![A-Z][A-Z0-9_]*\.map\b)[\w.?]+\.map\()' "${JS[@]}" "${X[@]}" "${ROOTS[@]}"
rg -n -U --pcre2 '\bListView\((?=(?:[^()]|'"$BAL"')*?\bchildren\s*:\s*(?!const\b)[^()]{0,60}?(?:\.map\(|\bfor\s*\())|\bSingleChildScrollView\((?=(?:[^()]|'"$BAL"')*?\bchild\s*:\s*(?:Column|Row|Wrap)\((?:[^()]|'"$BAL"')*?\bchildren\s*:\s*(?!const\b)[^()]{0,60}?(?:\.map\(|\bfor\s*\())' "${DA[@]}" "${X[@]}" "${ROOTS[@]}"
rg -n --pcre2 '\bshrinkWrap:\s*true\b' "${DA[@]}" "${X[@]}" "${ROOTS[@]}" | "${NC[@]}"
rg -n -U --pcre2 '\b(?:Column|Row)\s*(?=\((?:[^()]|\((?:[^()]|\([^()]*\))*\))*\b(?:vertical|horizontal)Scroll\b(?:[^()]|\((?:[^()]|\([^()]*\))*\))*\)\s*\{(?:[^{}]|\{[^{}]*\})*?\b(?![A-Z][A-Z0-9_]*\.)[\w.]+\.forEach(?:Indexed)?\s*\{)' "${KT[@]}" "${X[@]}" "${ROOTS[@]}"
rg -n -U --pcre2 '\bScrollView\b(?=\s*(?:\([^)]*\))?\s*\{\s*(?:VStack|HStack)\b\s*(?:\([^)]*\))?\s*\{\s*ForEach\()' "${SW[@]}" "${X[@]}" "${ROOTS[@]}"

# 2. List identity. 2a FlatList / SectionList with no keyExtractor; 2b FlashList item with its own key (breaks recycling);
#    2c FlashList estimatedItemSize (a dead prop on v2, required on v1 — grep 0 decides); 2d Compose items() with no
#    key over rows that hold state; 2e SwiftUI index or \.self identity; 2f Flutter reorderable / animated children.
rg -n -U --pcre2 '(?<![\w.<])<(?:FlatList|SectionList)\b(?!'"$TB"'\bkeyExtractor=)' "${JS[@]}" "${X[@]}" "${ROOTS[@]}"
rg -n --pcre2 '<FlashList\b(?='"$TB"'\brenderItem=\{(?:[^{}]|\{[^{}]*\})*?\bkey=\{)' "${JS[@]}" "${X[@]}" "${ROOTS[@]}"
rg -n --pcre2 '<FlashList\b(?='"$TB"'\bestimatedItemSize=)' "${JS[@]}" "${X[@]}" "${ROOTS[@]}"
rg -H -n --pcre2 '\bitems(?:Indexed)?\(\s*[\w.]+\s*\)\s*\{' "${KT[@]}" "${X[@]}" "${ROOTS[@]}" | win 0 12 '\A[^{]*\{(?:[^{}]|\{(?:[^{}]|\{[^{}]*\})*\})*?\b(?:remember(?:Saveable)?|animate\w*AsState|LaunchedEffect)\b' has
rg -n --pcre2 '\bForEach\(\s*(?:0\s*\.\.<\s*[\w.]+\.count|[\w.]+\.indices)\b|\bForEach\([^)]*\bid:\s*\\\.self\b' "${SW[@]}" "${X[@]}" "${ROOTS[@]}" | "${NC[@]}"
rg -H -n --pcre2 '\b(?:ReorderableListView|AnimatedList|SliverAnimatedList)\(' "${DA[@]}" "${X[@]}" "${ROOTS[@]}" | win 0 3 '\bkey\s*:' lacks

# 3. Re-render / rebuild / recompose waste. 3a RN context value built inline (noise when the React Compiler is on);
#    3b Flutter setState from a scroll or animation listener, animated Opacity; 3c Compose frequently-changing reads and
#    allocation or sorting in composition without remember; 3d SwiftUI observed object created in place, formatter in body.
rg -n --pcre2 '\.Provider\b[^>]*\bvalue=\{\{' "${JS[@]}" "${X[@]}" "${ROOTS[@]}"
rg -n --pcre2 '\.addListener\(\s*\(\)\s*(?:=>|\{)\s*setState\(|\bOpacity\(\s*opacity:\s*[\w.]*\.value\b' "${DA[@]}" "${X[@]}" "${ROOTS[@]}" | "${NC[@]}"
rg -l '@Composable' "${KT[@]}" "${X[@]}" "${ROOTS[@]}" | while IFS= read -r f; do
  rg -H -n --pcre2 '^\s*(?:val|var)\s+\w+\s*=\s*(?!remember\b)[^\n]*\b(?:firstVisibleItem(?:Index|ScrollOffset)|layoutInfo)\b|^\s*(?:val|var)\s+\w+\s*=\s*(?!remember\b)[^\n]*(?:\.sorted(?:By|With|Descending|ByDescending)?\b|\.filter\s*\{|\bSimpleDateFormat\(|DateTimeFormatter\.ofPattern\(|\bRegex\()' "$f"; done | rg -v --pcre2 'derivedStateOf|remember\s*[({]'
rg -n --pcre2 '@ObservedObject\s+(?:(?:private|public|internal)\s+)?var\s+\w+\s*(?::\s*\w+\s*)?=\s*\w+\(' "${SW[@]}" "${X[@]}" "${ROOTS[@]}"
rg -H -n --pcre2 '\b(?:let|var)\s+\w+\s*=\s*(?:Date|Number|ISO8601Date|ByteCount|DateComponents|Measurement)Formatter\(\)' "${SW[@]}" "${X[@]}" "${ROOTS[@]}" | win 3 0 '\bvar\s+body\s*:' has

# 4. Main- or JS-thread blocking. 4a RN animation off the native driver, InteractionManager (gated);
#    4b Android blocking calls outside a Worker or IO dispatcher; 4c iOS sync IO and main-queue sync; 4d Flutter *Sync IO and
#    jsonDecode outside an isolate.
rg -n --pcre2 '\buseNativeDriver\s*:\s*false\b|\bInteractionManager\.runAfterInteractions\b' "${JS[@]}" "${X[@]}" "${ROOTS[@]}" | "${NC[@]}"
rg -H -n --pcre2 '\brunBlocking\s*[({]|\ballowMainThreadQueries\(\)|\bedit\(\)[^\n]*\.commit\(\)|\bedit\(\s*commit\s*=\s*true|\.execute\(\)\s*(?:$|\.body)|\bThread\.sleep\(|\bpermit(?:All|DiskReads|DiskWrites|Network)\(\)' "${KT[@]}" "${X[@]}" "${ROOTS[@]}" | "${NC[@]}" | win 10 0 '\bfun\s+doWork\b|withContext\(\s*Dispatchers\.(?:IO|Default)|Dispatchers\.IO\)|Executors\.' lacks
rg -H -n --pcre2 '\b(?:Data|String|NSData|NSString|NSDictionary|NSArray)\(contentsOf(?:URL|File)?:|\bDispatchQueue\.main\.sync\b|\.wait\(\s*\)|\bDispatchSemaphore\(value:\s*0\)|\bsendSynchronousRequest\b' "${SW[@]}" "${X[@]}" "${ROOTS[@]}" | "${NC[@]}" | rg -v --pcre2 'Task\.detached|DispatchQueue\.global' | win 3 0 '(?:Task\.detached|DispatchQueue\.global\([^)]*\)\.async|Task\s*\(priority:[^)]*\))\s*\{[^}\n]*$|@concurrent\b|\bnonisolated\b' lacks
rg -n --pcre2 '\b(?:readAs(?:String|Bytes|Lines)Sync|writeAs(?:String|Bytes)Sync|existsSync|listSync|statSync|copySync|deleteSync)\(|\bjsonDecode\((?![^\n]*\b(?:Isolate\.run|compute)\b)' "${DA[@]}" "${X[@]}" "${ROOTS[@]}" | "${NC[@]}" | rg -v --pcre2 'Isolate\.run|\bcompute\('

# 5. Image decode. 5a Flutter without cacheWidth/Height; 5b RN core Image from a remote uri (files not on expo-image)
#    and the unmaintained fast-image; 5c Android original-size decode; 5d iOS full decode in cells, unbounded NSCache.
rg -n -U --pcre2 '\bImage\.(?:network|file|memory)\((?!(?:[^()]|'"$BAL"')*?\bcache(?:Width|Height)\s*:)|\bCachedNetworkImage\((?!(?:[^()]|'"$BAL"')*?\bmemCache(?:Width|Height)\s*:)' "${DA[@]}" "${X[@]}" "${ROOTS[@]}"
rg -l --pcre2 '<Image\b'"$TB"'\bsource=\{\{\s*uri\s*:' "${JS[@]}" "${X[@]}" "${ROOTS[@]}" | while IFS= read -r f; do rg -q --pcre2 'from\s+["\x27]expo-image["\x27]' "$f" || rg -H -n --pcre2 '<Image\b' "$f"; done
rg -n --pcre2 'from\s+["\x27]react-native-fast-image["\x27]' "${JS[@]}" "${X[@]}" "${ROOTS[@]}"
rg -n --pcre2 '\boverride\(\s*(?:Target\.)?SIZE_ORIGINAL\b|\bSize\.ORIGINAL\b|\b(?:HashMap|mutableMapOf|LinkedHashMap)<String,\s*Bitmap>' "${KT[@]}" "${X[@]}" "${ROOTS[@]}" | "${NC[@]}"
rg -l --pcre2 '\bBitmapFactory\.decode(?:File|Stream|Resource|ByteArray)\(' "${KT[@]}" "${X[@]}" "${ROOTS[@]}" | while IFS= read -r f; do rg -q --pcre2 'inSampleSize|inJustDecodeBounds' "$f" || rg -H -n --pcre2 '\bBitmapFactory\.decode\w*\(' "$f"; done
rg -H -n --pcre2 '\bUIImage\((?:data|contentsOfFile):' "${SW[@]}" "${X[@]}" "${ROOTS[@]}" | win 2 2 'preparingThumbnail|byPreparingThumbnail|CGImageSourceCreateThumbnailAtIndex' lacks
rg -H -n --pcre2 '\bNSCache<[^>]*>\(\)' "${SW[@]}" "${X[@]}" "${ROOTS[@]}" | rg -v 'countLimit|totalCostLimit' | while IFS=: read -r f l r; do n=$(printf '%s' "$r" | rg -o --pcre2 '\b(?:let|var)\s+\K\w+' | head -1); rg -q --pcre2 "\\b$n\\.(?:countLimit|totalCostLimit)" "$f" || echo "$f:$l:$r"; done

# 6. Startup. 6a Android Application.onCreate with 3+ SDK starts; 6b app modules with no baseline profile; 6c RN/Expo
#    inline requires off, whole-library imports; 6d iOS / ObjC static initializers; 6e Flutter 3+ awaits before runApp.
rg -H -n --pcre2 '\bclass\s+\w+\s*:\s*(?:Multidex)?Application\(\)' "${KT[@]}" "${X[@]}" "${ROOTS[@]}" | win 0 15 '(?s)(?:\.(?:init|initialize|start|setup|configure)\w*\(.*?){3}' has
rg -l --pcre2 'com\.android\.application|android\.application' -g 'build.gradle*' "${X[@]}" "${ROOTS[@]}" | while IFS= read -r f; do m=$(dirname "$f"); rg -q --pcre2 'baselineprofile|profileinstaller|dev\.flutter\.flutter-gradle-plugin|com\.facebook\.react\b' "$f" || [ -n "$(rg --files -g 'baseline-prof.txt' "$m")" ] || echo "6b $f: no baseline profile / profileinstaller"; done
rg -n --pcre2 '\binlineRequires\s*:\s*false\b' -g 'metro.config.*' "${X[@]}" "${ROOTS[@]}"; rg -n --pcre2 '^import\s+(?:\w+|\*\s+as\s+\w+)\s+from\s+["\x27](?:lodash|moment|date-fns|rxjs|ramda)["\x27]' "${JS[@]}" "${X[@]}" "${ROOTS[@]}"
rg -n --pcre2 '^\s*\+\s*\(void\)\s*load\b|__attribute__\(\(constructor' "${OC[@]}" "${X[@]}" "${ROOTS[@]}"
rg -H -n --pcre2 '\brunApp\(' "${DA[@]}" "${X[@]}" "${ROOTS[@]}" | win 12 0 '(?s)(?:\bawait\b.*?){3}' has

# 7. Leaks — retained after the owner dies. 7a RN listener / interval in an effect with no release nearby; 7b Flutter
#    controller, subscription or timer field never disposed or cancelled; 7c Android binding not cleared, Context or View
#    in a static, receiver never unregistered; 7d iOS timer target, strong delegate, stored closure or sink on self,
#    discarded block observer token.
rg -l --pcre2 '\buse(?:Layout)?Effect\(|\buseFocusEffect\(|\bcomponentDidMount\b' "${JS[@]}" "${X[@]}" "${ROOTS[@]}" | while IFS= read -r f; do
  rg -H -n --pcre2 '(?<!return )\b(?:AppState|Keyboard|Dimensions|Linking|NetInfo|BackHandler|DeviceEventEmitter|AccessibilityInfo|\w+Emitter)\.add(?:Event)?Listener\(|(?<!return )\bnavigation\.addListener\(|\bsetInterval\(' "$f" | win 0 8 '\.remove\(\)|\bclear(?:Interval|Timeout)\(|\bunsubscribe\b|\breturn\s*\(\)\s*=>|\breturn\s+\w+\s*;?\s*$' lacks; done
rg -l --pcre2 '\bextends\s+State<' "${DA[@]}" "${X[@]}" "${ROOTS[@]}" | while IFS= read -r f; do
  rg -o --no-filename --pcre2 '\b_\w+(?=\s*=\s*(?:(?:widget\.)?[\w.]+\.listen\(|(?:Text\w*Controller|AnimationController|ScrollController|PageController|TabController|FocusNode|Timer\.periodic)\b))' "$f" | sort -u | while IFS= read -r n; do
    rg -q --pcre2 "\\b$n\\??\\.(?:dispose|cancel)\\(" "$f" || rg -H -n --pcre2 "\\b$n\\s*=\\s*" "$f" | head -1; done; done
rg -H -n --pcre2 '\bprivate\s+var\s+_binding\b' "${KT[@]}" "${X[@]}" "${ROOTS[@]}" | win 0 60 '\A(?:(?!\n(?:[\w@]+\s+)*class\s)[\s\S])*?_binding\s*=\s*null' lacks
rg -H -n --pcre2 '^\s*(?:(?:private|internal|public|lateinit)\s+)*(?:var|val)\s+\w+\s*:\s*(?:Activity|Context|View|Fragment|\w+Activity|\w+Fragment)\??\s*(?:=|$)' "${KT[@]}" "${X[@]}" "${ROOTS[@]}" | win 8 0 '\bobject\s+\w+|\bcompanion\s+object\b' has
rg -l --pcre2 '\bregisterReceiver\(' "${KT[@]}" "${X[@]}" "${ROOTS[@]}" | while IFS= read -r f; do rg -q 'unregisterReceiver' "$f" || rg -H -n --pcre2 '\bregisterReceiver\(' "$f"; done
rg -l --pcre2 '\b(?:Timer\.scheduledTimer\([^)]*target:\s*self|CADisplayLink\(target:\s*self)' "${SW[@]}" "${X[@]}" "${ROOTS[@]}" | while IFS= read -r f; do rg -q 'invalidate()' "$f" || rg -H -n --pcre2 'target:\s*self' "$f"; done
rg -n --pcre2 '^\s*(?!.*\b(?:weak|unowned)\b)(?:(?:private|public|internal|open|fileprivate)\s+)?var\s+(?!reactNativeDelegate\b)\w*[dD]elegate\s*:\s*\w+\??\s*$|\bself\.\w+\s*=\s*\{(?!\s*\[(?:weak|unowned)\s+self\])[^}]*\bself\.|\.sink\s*\{(?!\s*\[(?:weak|unowned)\s+self\])[^}]*\bself\.|^\s*(?:NotificationCenter\.default|\w*[cC]enter)\.addObserver\(forName:' "${SW[@]}" "${X[@]}" "${ROOTS[@]}" | "${NC[@]}"
```

A finding is a grep hit **plus** a read of the data source, the call path and the owner **plus** the version gate **plus** the oracle. Three blind spots are structural:

- **N is not in the code.** Grep 1 cannot tell a 6-row settings list from a paginated feed beyond the `UPPER_CASE` constant skip; read where the array comes from (precedent § 36). A shrink-wrapped list in a sheet is fine for an enum of options and a defect for a page of products.
- **The merged manifest and the build decide startup.** Libraries register `<provider>` initializers invisible in source; when a build exists, count them in `build/intermediates/merged_manifests/**` (git-ignored, name it explicitly). Grep 6b skips Flutter and React Native host modules, where a baseline profile covers only the embedding.
- **Windows are heuristics.** `win` looks 1–12 lines around a hit; a release in a separate `useEffect`, a `dispose` in a mixin or a Worker two calls up is the read step's.

**Measured** (2026-10-05, ripgrep 15.2.0, bash 3.2 and zsh, identical hit sets). On the program's seeded multi-stack sample (bare RN 0.82 without the React Compiler, Expo SDK 57 / RN 0.87 with it, Flutter 3.47, Kotlin 2.2 + Compose + Views, SwiftUI + UIKit; 56 positives and 37 decoys across the seven classes) the script runs in under 1 s and surfaces every positive and no decoy; two printed lines are left to the gate and the read step by design (an inline context value under the React Compiler, a `ForEach(id: \.self)` over strings that may repeat). On every web and server fixture in `benchmarks/fixtures/*` it finds no mobile root and prints `N/A`; on `mobile-defects` (five mobile roots, measured 2026-10-10) it prints all 14 of its seeds in 44 lines, and the one decoy it prints (an inline Provider value under the React Compiler) is refuted by the gate — its `DEFECTS.md` § Detector measurement. A first version printed 8 false lines there: 2a ran without `-U`, so a multi-line `<FlatList` with `keyExtractor` on a later line and the generic in `useRef<FlatList<…>>` printed, and 7d read the React Native template's owned `var reactNativeDelegate` as a strong delegate. On a read-only real Flutter app (65,953 files, 440 Dart) it printed 23 lines: the root, 7 version lines, 2 `ListView(children:)` over an enum on a developer screen and 7 `shrinkWrap: true` (one true § 1 candidate — a paginated product list shrink-wrapped in a sheet; eight bounded option lists and grids, precedent § 36), and 6 § 4 lines (three sync writes in mock APIs not in the release graph, two single `existsSync` stats, one small session `jsonDecode` — all refuted). A first version also flagged the Flutter host module for a missing baseline profile and a local `AnimationController` handed to a disposed field; 6b now skips Flutter and RN hosts and 7b reads `_`-prefixed `State` fields only.

## The 3,000-hit path

1. **Intersect** with reachability: a screen no navigator reaches, a debug menu, a mock API or a `tool/` script is dismissed with one read and named in the coverage block.
2. **Group** by (root cause, owner): one base list component, one image wrapper, one `BaseFragment`, one shared provider is one group however many call sites use it.
3. **Rank** by user cost: field signals first when present (Play vitals ANR and slow-frame clusters, Xcode Organizer hangs and launch reports, Crashlytics / Sentry performance), then launch, the longest list and the heaviest screen, then the rest.
4. **Read the top 30 groups fully.**
5. **Prefer the bulk oracle at scale**: one Macrobenchmark `StartupTimingMetric` + `FrameTimingMetric` run, one `flutter drive --profile` trace, one Reassure suite over the top screens, or StrictMode `penaltyDeath` / Main Thread Checker enabled across the instrumented suite settles whole groups.
6. **Ledger the rest** as `Live, unreviewed (k groups / n hits)` with the command that continues them. Never `checked`.

## Scans for

Severity assumes a release build on a hot path. Raise one step when Play's ANR, slow-frame or memory vitals are already out of band (store visibility, `@app-store-reviewer`); drop one for a screen used rarely. **Critical** only with production evidence (an ANR or OOM cluster).

| § | Class | render-discipline / auditor label | Lint id | Tier | Default |
|---|---|---|---|---|---|
| 1 | Unvirtualized list over unbounded data | #5 `unvirtualized-list` | DCM `avoid-shrink-wrap-in-lists` (optional) | I (D for frames) | high for remote or paginated data |
| 2 | Missing or unstable list identity | #4 `unstable-list-item-props` | `ConstantContentStateKeyInItemsCall`; `NotifyDataSetChanged` | I | medium (state attaches to the wrong row); low for a dead prop |
| 3 | Re-render / rebuild / recompose waste | #1 `oversized-state-scope`, #3, #6 `animation-rebuilds-subtree`, #7 `store-overinvalidation` | `FrequentlyChangingValue`; `react-hooks` compiler rules | I | medium on lists and animations; low elsewhere unless measured |
| 4 | Main- or JS-thread blocking | `main-thread-io` | `ApplySharedPref`, `WrongThread`; Slack `DenyListedBlockingApi` | I / D | high for network or a remote read; medium for disk on a launch or scroll path |
| 5 | Full-resolution image decode, unbounded image cache | `decode-at-full-resolution`, `unbounded-cache` | `DrawAllocation` | I / D | high in lists; low for one hero image |
| 6 | Startup work before the first useful frame | `launch-work-pile` | `EnsureInitializerMetadata`; App Startup lint | D | medium; high when launch p90 is over the project budget (MOB-9) |
| 7 | Leaks — retained after the owner dies | `repeat-cycle-growth` | `StaticFieldLeak`, `HandlerLeak`; Dart `cancel_subscriptions`, `close_sinks`; SwiftLint `weak_delegate` | I | high when it grows per navigation; low for one app-scope object |

### 1. Unvirtualized list over unbounded data

```
BAD:   <ScrollView>{orders.map((o) => <OrderRow key={o.id} order={o} />)}</ScrollView>
       ListView(children: orders.map((o) => ListTile(…)).toList())      SingleChildScrollView(child: Column(children: [for (final m in messages) …]))
       Column(Modifier.verticalScroll(rememberScrollState())) { notes.forEach { NoteRow(it) } }       ScrollView { VStack { ForEach(messages) { … } } }
GOOD:  FlatList / FlashList · ListView.builder · LazyColumn { items(notes, key = { it.id }) { … } } · ScrollView { LazyVStack { ForEach … } } / List
```
**Read the code:** Where does the array come from — a query, a page, user content (unbounded), or a constant of about 20 items (precedent § 36)? Is a `shrinkWrap: true` list nested in another scrollable, forcing full layout? **Finding when** the list is unbounded and built eagerly. **Severity:** high for remote or paginated data; medium for local data that grows. **Verb:** `virtualize-list`. **Proof:** Reassure mount time and render count against the baseline with 200 rows (I); Flutter `flutter drive --profile` `traceAction` frame-budget fields; Macrobenchmark `FrameTimingMetric` on the scroll (D, release).

### 2. Missing or unstable list identity

```
BAD:   <FlatList data={orders} renderItem={…} />  // no keyExtractor       <FlashList renderItem={({ item }) => <Row key={item.id} …/>} />
       items(sorted) { note -> var expanded by remember { mutableStateOf(false) } … }   // no key, stateful row
       ForEach(0..<tags.count, id: \.self) { … }      ReorderableListView(children: [for (final o in orders) ListTile(…)])  // no Key
GOOD:  keyExtractor={(o) => o.id} · FlashList without per-item key (v2) · items(list, key = { it.id }) · ForEach(items) with Identifiable · ListTile(key: ValueKey(o.id))
```
**Read the code:** Is the list reorderable, filterable or inserted into, and does a row hold state (`remember`, an animation, a text field)? An append-only, stateless list needs no key. FlashList: on v2 `estimatedItemSize` is a dead prop and a per-item `key` breaks recycling; on v1 the missing estimate is the finding (precedent § 34). Are `\.self` values unique? **Finding when** moving or inserting an item gives its state to the wrong row, or recycling breaks. **Severity:** medium; low for a dead prop. **Verb:** `memoize` / stable keys. **Proof:** a test that moves an item and asserts the expanded row stays with its item (I).

### 3. Re-render, rebuild and recompose waste

```
BAD:   <CartContext.Provider value={{ items, add }}>        // every consumer re-renders each render (React Compiler off)
       _scroll.addListener(() => setState(() {}));           Opacity(opacity: _fade.value, child: …)   // saveLayer per frame
       val showTop = listState.firstVisibleItemIndex > 0     val sorted = notes.sortedBy { it.date }   val fmt = SimpleDateFormat("dd MMM")
       @ObservedObject var vm = InboxViewModel()             let formatter = DateFormatter()   // in var body
GOOD:  useMemo value (or the React Compiler) · ValueListenableBuilder / AnimatedBuilder child · FadeTransition
       derivedStateOf · remember(notes) { … } · @StateObject / @State with @Observable · formatter hoisted
```
**Read the code:** Is the React Compiler on (grep 0; precedent § 33) — then memo advice is noise. Kotlin ≥ 2.0.20 with strong skipping: an "unstable parameter" is not a finding; a new instance per recomposition or a frequently changing read in composition is (§ 32). Is the subtree large and is the trigger frequent (scroll, animation, typing)? **Finding when** a measured render or rebuild count grows with an unrelated update. **Severity:** medium on lists, scroll and animation; low elsewhere unless measured. **Verb:** `scope-state-down`, `scope-animation`, `split-store-selector`, `extract-const-subtree`. **Proof:** Reassure `measureRenders` count delta (I); Flutter rebuild count via `debugProfileBuildsEnabled` [K]; Compose compiler metrics and a recomposition counter [K]; Instruments SwiftUI template [K].

### 4. Main- or JS-thread blocking

```
BAD:   Animated.timing(fade, { toValue: 1, useNativeDriver: false })   InteractionManager.runAfterInteractions(…)  // no-op from RN 0.80, removed in 0.87
       prefs.edit().putString(…).commit()   runBlocking { api.fetch() }   // from a click handler
       let data = try? Data(contentsOf: remoteURL)   DispatchQueue.main.sync { }   File(p).readAsStringSync()   jsonDecode(raw)  // on the UI isolate
GOOD:  useNativeDriver: true (transform / opacity) · requestIdleCallback · apply() · withContext(Dispatchers.IO) · URLSession async · Task.detached · Isolate.run(() => jsonDecode(raw))
```
**Read the code:** Is the call reachable from a tap, a list bind, a composition or launch, and not inside a Worker, an IO dispatcher, `Task.detached` or an isolate (precedent § 21)? Does `useNativeDriver: false` animate a layout property the native driver cannot take (width, top — then it is not a finding)? Is the payload large? Is the Swift target on default MainActor isolation (§ 58)? **Finding when** the tripwire fires or a hang is measured on the path. **Severity:** high for network or a remote read; medium for disk on a launch or scroll path; low for a one-off small read. **Proof:** StrictMode `detectDiskReads().detectNetwork().penaltyDeath()` in an instrumented test (fails first); Thread Performance Checker and Main Thread Checker enabled **in the test plan**; Flutter `traceAction` missed-frame fields; RN DevTools Performance trace [K].

### 5. Full-resolution image decode, unbounded image cache

```
BAD:   itemBuilder: (c, i) => Image.network(photos[i])        <Image source={{ uri: order.photoUrl }} />  // core Image in a list row
       import FastImage from 'react-native-fast-image'         Glide.with(v).load(url).override(Target.SIZE_ORIGINAL)
       BitmapFactory.decodeFile(path)  // no inSampleSize       imageView.image = UIImage(data: data)  // in a cell     NSCache<NSString, UIImage>()  // no limits
GOOD:  Image.network(url, cacheWidth: 300) · expo-image with recyclingKey · Glide/Coil sized to the view · inSampleSize · byPreparingThumbnail(ofSize:) · countLimit / totalCostLimit
```
**Read the code:** Compare decoded size with display size × screen scale (a 300 pt thumbnail legitimately needs 900 px). Is the URL already resized by a CDN (`?w=`, `/resize/`)? Is `SIZE_ORIGINAL` a zoom viewer with subsampling? `react-native-fast-image` is unmaintained; verify any fork's publisher before recommending it (research open item). **Finding when** the decode is larger than display × scale in a list, or a cache has no bound. **Severity:** high in lists (Play's bitmap-memory vital counts from February 2027, per the vitals page as of 2026-09-21); low for one hero image. **Proof:** Flutter `debugInvertOversizedImages = true` and assert no "decoded … display" log line (I); a heap dump's bitmap total or `dumpsys meminfo` before and after (D); Instruments Allocations (D).

### 6. Startup work before the first useful frame

```
BAD:   class NotesApp : Application() { onCreate { Analytics.init(this); Maps.initialize(this); CrashSdk.init(this); … } }
       app module with no androidx.baselineprofile / profileinstaller      inlineRequires: false      import _ from 'lodash'
       + (void)load { … }   // ObjC static initializer        Future<void> main() async { await a(); await b(); await c(); runApp(…) }
GOOD:  App Startup / by lazy holders · a generated baseline profile · inlineRequires: true · import debounce from 'lodash/debounce'
       work after the first frame (WidgetsBinding.addPostFrameCallback, Task after launch)
```
**Read the code:** What must finish before the first *useful* frame, and what can wait? Count initializers in the **merged** manifest too. Is there a launch budget (MOB-9)? Apple publishes no launch target; Android vitals treats a cold start of 5 s or longer as excessive (`@device-performance-auditor` cites both). **Finding when** launch time against the project budget, measured, regresses or exceeds it, with the attributable work at `<file:line>`. **Severity:** medium; high when p90 is over budget. **Proof:** Macrobenchmark `StartupTimingMetric` (`timeToInitialDisplayMs`, cold, `CompilationMode.None()` vs `Partial()`) on a release, profileable build (D); `XCTApplicationLaunchMetric` in `measure(metrics:)` (D); `flutter run --profile --trace-startup`, which writes its start-up timings as JSON under `build/` (D).

### 7. Leaks — retained after the owner dies

```
BAD:   useEffect(() => { Keyboard.addListener('keyboardDidShow', f) }, [])       setInterval(…)  // no clearInterval
       final _search = TextEditingController();   _sub = feed.listen(…)   // State with no dispose / cancel
       private var _binding: FragmentDetailBinding? = null   // never nulled in onDestroyView      object Session { var activity: Activity? }
       Timer.scheduledTimer(…, target: self, …)  // never invalidated     var delegate: PlayerDelegate?     self.onUpdate = { self.render() }
       NotificationCenter.default.addObserver(forName: …) { … }  // block token discarded
GOOD:  return () => sub.remove() · dispose() / cancel() · _binding = null in onDestroyView · applicationContext only · invalidate() · weak var delegate · [weak self] · stored token removed
```
**Read the code:** Is there a destroyed owner and a retaining path (a big heap is § 5, not this)? Is the listener app-lifetime at module scope, or `return navigation.addListener(…)` (that *is* the cleanup; precedent § 14)? Selector-based observers are auto-removed (§ 15); non-escaping closures and short-lived `Task {}` need no `[weak self]` (§ 16). Is the controller passed in by a parent that disposes it? **Finding when** the owner is retained after it is destroyed, proven by the leak oracle. **Severity:** high when it grows per navigation (a screen, an Activity, a view controller per visit); low for one app-scope object. **Proof:** LeakCanary `DetectLeaksAfterTestSuccess` (2.14) in an instrumented test (I/D); XCTest `addTeardownBlock { [weak sut] in XCTAssertNil(sut) }` [K]; `leaks -atExit -- <cmd>` exits 1 on a leak; Flutter `LeakTesting.enable()` (leak_tracker) in `flutter_test_config.dart` (I); Jest fake timers — timer and listener counts are zero after unmount (I).

## Proof — the oracles

The oracle shapes and the whole-class variants are in [`proof-oracles.md`](../../../../snippets/proof-oracles.md) § Mobile (render count, release-mode tripwire, frame and render cost, oversized-decode log, startup metric, leak assertion); `device-harness` (this pack) boots the device and records the runs. Verified 2026-10-05: Reassure 1.6.0 `measureRenders(<C />, { scenario })`; `androidx.benchmark:benchmark-macro-junit4:1.5.0` with `StartupTimingMetric` and `FrameTimingMetric` (stable); `XCTApplicationLaunchMetric` (iOS 13+; the minimum Xcode is not stated by Apple and is not asserted here); Dart `cancel_subscriptions` and `close_sinks` (stable, in no default rule set). Every existence oracle **fails before the fix**; every cost comparison runs both sides on the same device, build type and run count, and reports the spread. A debug-build figure, an emulator figure presented as user experience, or a single run is refuted (`@device-performance-auditor`: `debug-build-number`, `simulator-absolute`, `single-sample`). No booted device: the D rows are `SKIPPED (no device)` and the finding is `[report-flagged]` — never PASS.

## Output

```
mobile-perf-scan — lanes: react-native 0.82 (rn-app/package.json:6, React Compiler off), expo SDK 57 / RN 0.87 (expo-app/app.json:18, compiler on),
                    flashlist 2.3.3, flutter 3.47, kotlin 2.2.20 (strong skipping default), swiftui
Roots: 6    Device: emulator-5554 (API 35, release build); no iOS simulator → iOS cost rows Unconfirmed

Findings: 3 · Unconfirmed: 1

1. rn-app/src/screens/OrderListScreen.tsx:21                                    [report-with-fix]   high
   §1 orders (useQuery, paginated) rendered in a ScrollView with .map. Proof: Reassure measureRenders with 200 orders —
   render duration past THR-PERF-REGRESSION against the FlashList variant (10 runs a side; the delta and its interval are
   in .reassure/output.md). Fix (virtualize-list): FlashList, keyExtractor, no per-item key.

2. expo-app/src/perf/StopsProvider.tsx:9                                       [report-with-fix]   high
   §4 InteractionManager.runAfterInteractions on react-native 0.87 (expo-app/package.json:12): removed in 0.87 — a build break,
   not a deferral (precedent § 51). Fix: requestIdleCallback, or move the work into the effect that needs it.

3. android-native/app/src/main/java/com/acme/notes/perf/Leaks.kt:19            [report-with-fix]   high
   §7 DetailFragment keeps _binding after onDestroyView. Proof: LeakCanary DetectLeaksAfterTestSuccess — open, back, repeat:
   "View.mContext references a destroyed activity" (fails first). Fix: _binding = null in onDestroyView.

4. ios-app/Acme/Perf/PhotoCell.swift:7                                         [report-flagged]    high
   §5 UIImage(data:) decoded at full size per cell. Unproven link: no simulator. Settling run: Instruments Allocations on the
   feed scroll before / after byPreparingThumbnail(ofSize:).

Verification: 58 candidates → 3 findings · 1 unconfirmed · 9 hardening · 0 pre-existing · 45 refuted
Handed to @device-performance-auditor: 1, 4 (cost rows, with their oracle commands)

Class coverage:
  §1  unvirtualized lists           checked (5 hits → 1 finding)
  §2  list identity                 checked (7 hits → 0 findings; FlashList estimatedItemSize on v2: hardening)
  §3  render waste                  checked (9 hits → 0 findings; expo-app Provider value: compiler on, precedent § 33)
  §4  main-thread blocking          checked (10 hits → 1 finding)
  §5  image decode                  checked (7 hits → 1 unconfirmed)
  §6  startup                       checked (6 hits → 0 findings; no launch budget recorded — handed to the auditor as budget-absent)
  §7  leaks                         checked (15 hits / 9 groups → 1 finding)
```

`[report-with-fix]`: the path, the version gate and the oracle's result (with build type, device and run count for a cost) are cited, and the fix is local. `[report-flagged]`: one link is unproven (no device, no release build, the data source not read), and the row names it and the settling run. The coverage block lists **all seven** classes on every run: `checked (k hits → m findings)` only when the grep ran on a present lane; `N/A (<reason>)` only when the repo has no such surface; `blocked (<reason>)` when a grep failed or a file could not be read; `Live, unreviewed (k groups / n hits)` for a partial review.

## False positives / precedents

The verifier reads [`precedents/mobile.md`](../../../../snippets/precedents/mobile.md) and [`refute-before-report.md`](../../../../snippets/refute-before-report.md) § 4. The ones this skill meets most: app-lifetime listeners and returned unsubscribes (§ 14); selector observers (§ 15); `[weak self]` not needed (§ 16); off-main blocking inside a Worker or IO dispatcher (§ 21); strong skipping (§ 32); the React Compiler (§ 33); FlashList v2 (§ 34); Hermes the default (§ 35); about 20 static items (§ 36); `InteractionManager` by version (§ 51); AGP 9.3 minify DSL (§ 53); Swift default isolation (§ 58); library-owned lifecycle and threads (§ 67); small and one-off work (§ 68); a layout property the native driver cannot animate (§ 69); a controller or context owned elsewhere (§ 70); images sized by design (§ 71); code that does not ship (§ 72).

## When to run

- On any diff that adds or changes a list, a list row, a context or store provider, an animation, an image in a list, an `Application` / `AppDelegate` / `main()` start-up path, a listener, timer, controller or subscription, or a dependency import at module scope — the `/mobile-audit` dispatch signal.
- On every whole-repo `/mobile-audit`, reporting all seven classes; `lane-mobile` (delivery pack, when installed) runs it on T2/T3 changes to the files above.
- When field signals show slow frames, ANRs, hangs, slow launches or memory kills — then seed the sibling sweep (refute-before-report § 6) from the top signature.

## Halt conditions

- Do not report a high row as confirmed until a verifier other than the run that found it has passed it through [`refute-before-report.md`](../../../../snippets/refute-before-report.md) with [`precedents/mobile.md`](../../../../snippets/precedents/mobile.md). Under `/mobile-audit` that happens in its verification phase; run standalone, apply the protocol as a separate second pass, tag those rows `self-verified`, and list the rest as Unconfirmed, Hardening, Pre-existing or Refuted. Never drop them.
- Halt on any finding without the `<file:line>`, the hot path, the version-gate line and the fix.
- Do not mark a row `[report-with-fix]` without its oracle failing (existence) or measured past `THR-PERF-REGRESSION` (cost) on a release or profile build. No device → `SKIPPED` for the device rows and `[report-flagged]` for the finding — never PASS.
- Do not report a number no tool produced, a debug-build figure, a single run, or an emulator figure as user experience.
- Do not report "add memo" when the React Compiler is on, or "unstable parameter" under strong skipping, or a FlashList prop outside its major (§ 32–34).
- Do not print "no performance defect found" without the class-coverage block; a class whose grep did not run is `blocked`, never `checked`.
- Do not re-derive a class another skill owns (§ Boundaries). Route it.

## Related

- `/mobile-audit` dispatches this skill and folds its coverage block into the class ledger; `/mobile-fix` closes the findings failing-first and re-runs this detector on the patched lines.
- `@device-performance-auditor` (this pack) measures and ranks the cost rows; `rules/render-discipline.md` (this pack) holds the closure verbs; `device-harness` (this pack) runs the D-tier oracles.
- `mobile-lifecycle-scan` (this pack) routes listener and controller leaks to § 7; `app-size-scan` / `/optimize-bundle` (this pack) own app size; `native-bridge-audit` (this pack) owns bridge threading.
- `performance-optimizer` (performance pack, when installed) owns server latency behind the API; the frontend pack owns web vitals.
