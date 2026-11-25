---
name: native-bridge-audit
description: Find defects at the JS/Dart-to-native boundary — legacy bridge use on New-Architecture-only RN, calls the other side never answers, swallowed native errors, blocking sync methods, leaked native listeners, removed RN APIs — proved by a contract test on both sides.
kind: skill
pack: mobile
allowed-tools: [Read, Grep, Glob, Bash]
---

# Skill: native-bridge-audit

## Premise

The boundary between JavaScript or Dart and native code is where a mobile app's two halves stop sharing a type system. A method one side calls and the other never exports fails only at run time, on one platform. A native `catch` that logs and returns leaves a JavaScript `await` that never settles. A synchronous native method blocks the JS thread for as long as it runs. And since React Native 0.82 the boundary itself changed: the New Architecture is the only architecture, `newArchEnabled=false` is ignored, and 0.81 / Expo SDK 54 were the last releases that could run the legacy one (RN 0.82 release post, 2025-10-08). The interop layers that keep legacy modules working stay "for the foreseeable future" (same post), so legacy code still runs — untyped, resolved at run time, and on a removal path.

**Every finding cites `<path:line>` on both sides of the boundary — the JS / Dart call site and the native implementation, per platform — + the version gate (grep 0) + the contract test that fails (or the run that would) + the fix.** A missing side is itself the evidence (a method no platform exports). "Type mismatch" quotes both signatures; "never settles" names the branch that neither resolves nor rejects. No accusation without coordinates, and no "bridge is clean" without the class-coverage block (§ Output).

## The rule

A candidate is a finding when all four hold:

1. **It ships** — release build, not a test host or `__DEV__` path, and a screen or job reaches the call.
2. **The version gate holds** — read `react-native`, `expo`, Flutter and Pigeon from grep 0. On RN ≥ 0.82 "migrate to the New Architecture" is noise ([`precedents/mobile.md`](../../../../snippets/precedents/mobile.md) § 50); a legacy-only module, a dead architecture flag and an untyped `NativeModules` call are the real findings there.
3. **Both sides are read** — the JS/Dart side and every native platform the app ships. A one-platform audit is `PARTIAL`, never "clean".
4. **The contract test fails** — a call the other side does not answer, an error that never arrives, a JS thread blocked by a synchronous call, a listener alive after teardown.

## Boundaries

- WebView bridges (`addJavascriptInterface`, `onMessage`, `WKScriptMessageHandler`, `JavaScriptChannel`) → `mobile-security-scan` when the security pack is installed (exposure is an attacker question). Without it, § 7 rows are reported here, tagged `security-class (owner pack not installed)`.
- Main-thread and JS-thread cost in general (`InteractionManager` as jank, `JSON.parse` on the JS thread) → `mobile-perf-scan` § 4. § 6 here owns the **build break** and the removed API; both runs dedupe by `<file:line>`.
- A permission-gated API behind the bridge → `mobile-lifecycle-scan` § 3 (crash on denial, purpose strings).
- Whether a bridge should exist at all → `@mobile-architect` (design, not audit).

## Inputs and outputs

Inputs: the codebase root (roots are derived from the markers), optionally a module or channel name to scope to, and crash reports when present. Output: `ai/audits/bridge-audit-<module|all>-<date>.md` in the § Output form.

## Adapt to the codebase — lanes

| Lane | Typed contract | Legacy surface (works through interop, untyped) | Sync call | Teardown |
|---|---|---|---|---|
| **React Native** (≥ 0.82) | Turbo Native Module: a `Native*.ts` spec `extends TurboModule`, `TurboModuleRegistry.getEnforcing<Spec>()`, `codegenConfig` in `package.json`, codegen at build (`generateCodegenArtifactsFromSchema` on Android) — reactnative.dev *Turbo Native Modules*, read 2026-10-05 | `NativeModules.X`, `ReactContextBaseJavaModule` + `@ReactMethod`, `RCT_EXPORT_MODULE` / `RCT_EXPORT_METHOD`, `requireNativeComponent` | spec methods returning a value (allowed; the body must be cheap), `isBlockingSynchronousMethod = true`, `RCT_EXPORT_BLOCKING_SYNCHRONOUS_METHOD` | `invalidate()` |
| **Expo** (SDK 53–57, RN 0.79–0.87) | Expo Modules API (`Module`, `Function`, `AsyncFunction`, `Events`) [K: semantics per SDK, read the installed `expo-modules-core`] | as RN | `Function` (sync) [K] | `OnDestroy` [K] |
| **Flutter** (3.x) | Pigeon-generated channels | `MethodChannel` / `EventChannel` (`dynamic` payloads) | — (channels are async; the **platform** handler runs on the main thread unless a task queue is used — docs.flutter.dev *platform channels*, read 2026-08-20) | `FlutterStreamHandler.onCancel` |

RN versions that change a verdict (RN CHANGELOG and release posts, read 2026-10-05): **0.80** `InteractionManager` no longer defers; **0.82** New Architecture only, `InteractionManager` ignores interaction handles; **0.84** Hermes V1 the default; **0.87** `InteractionManager` removed (use `requestIdleCallback`), the `useTurboModules` flag removed (TurboModules always on), `RCTTurboModuleEnabled()` / `RCTEnableTurboModule()` and `addUIBlock` deprecated, the Strict TypeScript API the default (deep imports into `react-native/Libraries/` inaccessible unless the `react-native-legacy-deep-imports` condition is set, available through 0.88). The 0.88 release candidate adds opt-in `RCT_REMOVE_LEGACY_MODULE_INTEROP` / `RCT_REMOVE_LEGACY_COMPONENT_INTEROP`, default off (research catalog, RN CHANGELOG).

## Pre-flight greps

Run as **one** script from the repo root. Grep **N** feeds detector **§N**; grep 0 is context. Lines tagged `2a` / `2b` are set-difference results (what one side calls minus what the other answers, per root and platform; an absent platform folder is said once, never compared); `1b`, `3b`, `5a`, `5b` are file-level results; the rest are grep hits. Any `rg` error on stderr is a failed grep, never zero hits.

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
X=(-g '!**/{node_modules,Pods,build,.gradle,.dart_tool,.expo,DerivedData,dist,vendor,.cxx}/**' -g '!**/src/{test,androidTest,debug}/**'
   -g '!**/{test,tests,__tests__,__mocks__,mocks,fixtures,__fixtures__,testdata,e2e,integration_test,.maestro,docs,ai,tool}/**'
   -g '!**/*{Tests,UITests}/**' -g '!**/*.{test,spec,stories}.*' -g '!**/*_test.dart' -g '!**/*.{g,freezed,mocks}.dart' -g '!**/*.{md,mdx,lock,snap,map}')
NC=(rg -v --pcre2 '^[^:]+:\d+:\s*(//|/\*|\*(\s|/|$)|#(?!\{)|<!--)')
JS=(-g '*.{js,jsx,ts,tsx}'); KT=(-g '*.{kt,java}'); DA=(-g '*.dart'); SW=(-g '*.swift'); NT=(-g '*.{kt,java,swift,m,mm}')

# 0. Versions and architecture flags: react-native / expo / webview / pigeon; flags that pretend the legacy architecture is on.
rg -n --pcre2 '"(?:react-native|expo|expo-modules-core|react-native-webview)"\s*:|"codegenConfig"\s*:' -g 'package.json' "${X[@]}" "${ROOTS[@]}"
rg -n --pcre2 '^\s+(?:flutter|pigeon):\s*["^>=]*\d|^\s+flutter:\s*["^>=]' -g 'pubspec.yaml' "${ROOTS[@]}"
rg -n --pcre2 '^\s*newArchEnabled\s*=\s*false\b|RCT_NEW_ARCH_ENABLED\W+0\b|"newArchEnabled"\s*:\s*false|\buseTurboModules\b|\bRCT(?:Enable|)TurboModule(?:Enabled)?\(' -g 'gradle.properties' -g 'Podfile' -g 'app.json' -g '*.{kt,java,m,mm,swift}' "${X[@]}" "${ROOTS[@]}" | "${NC[@]}"

# 1. Legacy bridge surface. 1a JS reaching modules through NativeModules (untyped, resolved at run time); 1b native modules with
#    no codegen spec; 1c legacy view interop.
rg -n --pcre2 '\bNativeModules\.\w+|\{[\w\s,]+\}\s*=\s*NativeModules\b' "${JS[@]}" "${X[@]}" "${ROOTS[@]}" | "${NC[@]}"
rg -l --pcre2 '\bextends\s+(?:ReactContextBaseJavaModule|BaseJavaModule)\b|:\s*(?:ReactContextBaseJavaModule|BaseJavaModule)\(|\bRCT_EXPORT_MODULE\(|\bRCTBridgeModule\b' "${NT[@]}" "${X[@]}" "${ROOTS[@]}" | while IFS= read -r f; do rg -q --pcre2 '\bNative\w+Spec\b|\bTurboModule\b|getTurboModule\b' "$f" || echo "1b $f: native module with no codegen spec"; done
rg -n --pcre2 '\brequireNativeComponent\(|\bUIManager\.dispatchViewManagerCommand\(|\bcodegenNativeComponent\b' "${JS[@]}" "${X[@]}" "${ROOTS[@]}" | "${NC[@]}" | rg -v 'codegenNativeComponent'

# 2. Contract set-difference — what one side calls minus what the other side answers, per root, module or channel, and
#    platform. A platform folder that is absent (Expo CNG, single-platform) is said once, never compared.
#    2a RN: methods called on a NativeModules module minus @ReactMethod / RCT_EXPORT_METHOD / RCT_REMAP_METHOD / @objc names.
for r in "${ROOTS[@]}"; do [ -f "$r/package.json" ] || continue
 for m in $(rg -o --no-filename --pcre2 '\bNativeModules\.\K\w+|\{\s*\K[\w\s,]+(?=\}\s*=\s*NativeModules\b)' "${JS[@]}" "${X[@]}" "$r" | tr ',' '\n' | tr -d ' ' | sort -u); do
  called=$(rg -o --no-filename --pcre2 "\\b(?:NativeModules\\.)?$m\\??\\.\\K\\w+(?=\\()" "${JS[@]}" "${X[@]}" "$r" | sort -u)
  for plat in android ios; do
    [ -d "$r/$plat" ] || { echo "2a $m: no $r/$plat folder (CNG or single-platform) — read the dependency or config plugin"; continue; }
    [ "$plat" = android ] && G=(-g '*.{kt,java}') || G=(-g '*.{m,mm,swift}')
    files=$(rg -l --pcre2 "getName\\(\\)\\s*(?::\\s*String\\s*)?(?:=|\\{\\s*return)\\s*\"$m\"|RCT_EXPORT_MODULE\\(\\s*$m?\\s*\\)|@objc\\(\\s*$m\\s*\\)|RCT_EXTERN_MODULE\\(\\s*$m\\b" "${G[@]}" "${X[@]}" "$r/$plat")
    [ -n "$files" ] || { echo "2a $m: called from $r, no $plat implementation in the repo (a dependency, or undefined at run time)"; continue; }
    have=$(printf '%s\n' "$files" | while IFS= read -r f; do rg -A2 --no-filename '@ReactMethod' "$f" | rg -o --pcre2 '\b(?:fun|void|[A-Z]\w*|boolean|double|int)\s+\K\w+(?=\s*\()'
      rg -o --no-filename --pcre2 'RCT_EXPORT_METHOD\(\s*\K\w+|RCT_REMAP_METHOD\(\s*\w*\s*,\s*\K\w+|RCT_EXTERN_METHOD\(\s*\K\w+|@objc\s+(?:func\s+)?\K\w+(?=[(:])' "$f"; done | sort -u)
    comm -23 <(printf '%s\n' "$called") <(printf '%s\n' "$have") | sed "s#^#2a $m.#; s#\$# called in JS, not exported on $plat#"; done; done; done
#    2b Flutter: MethodChannel methods invoked from Dart minus the methods the native handler for that channel name answers.
for r in "${ROOTS[@]}"; do [ -f "$r/pubspec.yaml" ] || continue
 rg -o --no-filename --pcre2 '\b\w+\s*=\s*(?:const\s+)?MethodChannel\(\s*["\x27]\K[^"\x27]+' "${DA[@]}" "${X[@]}" "$r" | sort -u | while IFS= read -r ch; do
  called=$(rg -l -F "'$ch'" "${DA[@]}" "${X[@]}" "$r" | while IFS= read -r f; do v=$(rg -o --no-filename --pcre2 "\\b\\w+(?=\\s*=\\s*(?:const\\s+)?MethodChannel\\(\\s*[\"']${ch}[\"'])" "$f" | head -1)
    [ -n "$v" ] && rg -o --no-filename --pcre2 "\\b$v\\.invoke(?:List|Map)?Method(?:<[^>]*>)?\\(\\s*[\"']\\K\\w+" "$f"; done | sort -u)
  for plat in android ios; do [ -d "$r/$plat" ] || continue
    [ "$plat" = android ] && G=(-g '*.{kt,java}') || G=(-g '*.{swift,m,mm}')
    files=$(rg -l -F "\"$ch\"" "${G[@]}" "${X[@]}" "$r/$plat")
    [ -n "$files" ] || { echo "2b $ch: no $plat handler in $r/$plat (a plugin, or MissingPluginException at run time)"; continue; }
    have=$(printf '%s\n' "$files" | while IFS= read -r f; do rg -o --no-filename --pcre2 '(?:\bcase\s+|call\.method\s*==\s*|^\s*)"\K\w+(?="\s*(?::|->|\{|\)|$))' "$f"; done | sort -u)
    comm -23 <(printf '%s\n' "$called") <(printf '%s\n' "$have") | sed "s#^#2b $ch.#; s#\$# invoked from Dart, not handled on $plat#"; done; done; done

# 3. Errors that never reach the caller. 3a a catch in a promise-taking RN method with no reject (the JS await never settles);
#    3b a Flutter handler that can fall through without notImplemented (the Dart future never completes).
rg -l --pcre2 '@ReactMethod|RCTPromiseRejectBlock' "${NT[@]}" "${X[@]}" "${ROOTS[@]}" | while IFS= read -r f; do rg -H -n -U --pcre2 '\bcatch\s*(?:\([^)]*\))?\s*\{(?=(?:(?!\breject\b|\bthrow\b)[^{}]|\{[^{}]*\})*\})' "$f"; done
rg -l --pcre2 '\bsetMethodCallHandler\b' "${NT[@]}" "${X[@]}" "${ROOTS[@]}" | while IFS= read -r f; do h=$(rg -c 'setMethodCallHandler' "$f"); n=$(rg -c --pcre2 'FlutterMethodNotImplemented|\bnotImplemented\(\)' "$f"); [ "$h" -gt "${n:-0}" ] && echo "3b $f: $h handler(s), ${n:-0} notImplemented"; done

# 4. Threading. 4a synchronous native methods (block the JS thread for their whole duration: read the body); 4b modules pinned to
#    the main queue; 4c Flutter handlers doing I/O on the platform main thread with no task queue; 4d Android UI from a module.
rg -n --pcre2 'isBlockingSynchronousMethod\s*=\s*true|\bRCT_EXPORT_BLOCKING_SYNCHRONOUS_METHOD\b|requiresMainQueueSetup[^\n]*\b(?:YES|true)\b|methodQueue[^\n]*(?:dispatch_get_main_queue|DispatchQueue\.main)' "${NT[@]}" "${X[@]}" "${ROOTS[@]}" | "${NC[@]}"
rg -l --pcre2 '\bextends\s+TurboModule\b' -g 'Native*.{ts,js}' "${X[@]}" "${ROOTS[@]}" | while IFS= read -r f; do rg -H -n --pcre2 '^\s+\w+\([^)]*\)\s*:\s*(?!Promise\b|void\b)\w' "$f"; done
rg -l --pcre2 '\bsetMethodCallHandler\b' "${NT[@]}" "${X[@]}" "${ROOTS[@]}" | while IFS= read -r f; do rg -q --pcre2 'makeBackgroundTaskQueue|taskQueue' "$f" || rg -H -n --pcre2 '\bData\(contentsOf|\bFileManager\b|\breadText\(|\breadBytes\(|\bFile\(|\bSQLite|\bJSONDecoder\(\)\.decode|\bBitmapFactory\.' "$f"; done
rg -l --pcre2 '\bReactContextBaseJavaModule\b' "${KT[@]}" "${X[@]}" "${ROOTS[@]}" | while IFS= read -r f; do rg -q --pcre2 'runOnUiThread|UiThreadUtil|Dispatchers\.Main|Handler\(Looper\.getMainLooper' "$f" || rg -H -n --pcre2 '\.(?:setText|addView|removeView|setVisibility)\(|\bToast\.makeText\(|\.show\(\)' "$f"; done

# 5. Lifecycle. 5a Android modules that acquire listeners, sensors or threads with no invalidate(); 5b iOS emitters with no
#    stopObserving / invalidate; 5c Flutter stream handlers whose onCancel releases nothing onListen acquired.
rg -l --pcre2 '\bReactContextBaseJavaModule\b|\bTurboModule\b' "${KT[@]}" "${X[@]}" "${ROOTS[@]}" | while IFS= read -r f; do rg -q --pcre2 '\b(?:registerListener|addListener|registerReceiver|requestLocationUpdates|Executors\.new\w+|HandlerThread\(|scheduleAtFixedRate)\b' "$f" && ! rg -q --pcre2 '\boverride\s+fun\s+invalidate\(|\bpublic\s+void\s+invalidate\(' "$f" && echo "5a $f: acquires, no invalidate()"; done
rg -l --pcre2 '\bRCTEventEmitter\b' -g '*.{m,mm,swift}' "${X[@]}" "${ROOTS[@]}" | while IFS= read -r f; do rg -q --pcre2 'stopObserving|invalidate' "$f" || echo "5b $f: emitter with no stopObserving / invalidate"; done
rg -H -n -U --pcre2 'func\s+onCancel\([^)]*\)\s*->\s*FlutterError\?\s*\{(?=\s*return\s+nil\s*\})|override\s+fun\s+onCancel\([^)]*\)\s*\{(?=\s*\})' "${NT[@]}" "${X[@]}" "${ROOTS[@]}" | while IFS=: read -r f l r; do rg -q --pcre2 'addObserver|\.listen\(|register\w*\(|addListener' "$f" && echo "$f:$l:$r"; done

# 6. Runtime APIs removed or deprecated at the boundary (gate on grep 0): InteractionManager (no deferral 0.80, removed 0.87);
#    deep imports into react-native/Libraries (inaccessible under the 0.87 Strict API); UI blocks; legacy teardown hook.
rg -n --pcre2 '\bInteractionManager\.\w+|from\s+["\x27]react-native/Libraries/|require\(\s*["\x27]react-native/Libraries/|\b(?:add|prepend)UIBlock\(|\bonCatalystInstanceDestroy\b|\bNativeMethodsMixin\b|\bAppState\.removeEventListener\(' "${JS[@]}" "${KT[@]}" "${X[@]}" "${ROOTS[@]}" | "${NC[@]}"

# 7. WebView bridges: routed to the security pack's mobile-security-scan when installed.
rg -n --pcre2 '\baddJavascriptInterface\(|<WebView\b[^>]*\bonMessage=|\bWKScriptMessageHandler\b|\bJavaScriptChannel\(|\baddJavaScriptHandler\(|\bjavascriptChannels\s*:' "${JS[@]}" "${NT[@]}" "${DA[@]}" "${X[@]}" "${ROOTS[@]}" | "${NC[@]}"
:
```

A finding is a script line **plus** a read of both sides **plus** the version gate. Three blind spots are structural: **dependencies** (a module implemented in `node_modules` or a Flutter plugin package has no implementation in the repo — read the package's native folder before calling the call unanswered); **dynamic names** (`NativeModules[name]`, `invokeMethod(variable)` are invisible to a set-difference — read them); **codegen** (a Turbo Native Module whose spec and implementation disagree fails the build, so a codegen'd module is `checked` by the build log, not by this script).

**Measured** (2026-10-05, ripgrep 15.2.0; bash 3.2 and zsh give the same hit set, stdin piped or not; < 1 s). On the program's multi-stack sample (bare RN 0.82, Expo SDK 57 / RN 0.87 with no `ios/`, Flutter 3.47; 17 positives, two of them the perf sample's `InteractionManager` files, and 6 decoys) every positive surfaces and no decoy does: a fully handled `acme/flash` channel with a `default:` branch, a Promise-returning spec method, exported methods, a TurboModule spec, and two roots whose missing platform folder is said once instead of compared. One line is left to the read step by design (a synchronous spec method that may return a cached value). The first version printed 6 false lines: two exported methods missed because `rg -o -U` with `\K` across lines prints the whole line (now a two-line read after `@ReactMethod`), and four comparisons against platform folders that do not exist; under zsh, `$ch[…]` parsed as a subscript (now `${ch}`). On every web and server fixture in `benchmarks/fixtures/*` it prints `N/A`; on `mobile-defects` (five mobile roots, measured 2026-10-10) it prints all 8 of its seeds in 20 lines — its `DEFECTS.md` § Detector measurement. On a read-only real Flutter app (440 Dart files, no custom channels — its plugins are packages) it prints only the root line.

## The 3,000-hit path

1. **Intersect** with reachability: a module or channel no screen or job calls is dismissed with one read and named.
2. **Group** by module or channel: every unanswered method of one module is one group; one wrapper (`callNative(name, …)`) is one group.
3. **Rank** by consequence: payment, auth and storage modules first; then modules on cold-start paths; then the rest.
4. **Read the top 30 groups on both sides.**
5. **Prefer the build as the bulk oracle**: generating a Turbo Native Module spec or Pigeon file for a module turns every contract mismatch into a compile error at once.
6. **Ledger the rest** `Live, unreviewed (k groups / n hits)`.

## Scans for

| § | Class | Standard / gate | Proof tier | Default |
|---|---|---|---|---|
| 1 | Legacy bridge surface on a New-Architecture-only runtime; dead architecture flags | RN ≥ 0.82 | A (build) + S | medium; high when the module is legacy-only and unmaintained |
| 2 | Contract gap: called on one side, not answered on the other, per platform | CWE-628 | I (contract test) | high (crash, `MissingPluginException`, `undefined is not a function`) |
| 3 | Error that never reaches the caller (await never settles) | CWE-755 | I | high |
| 4 | Blocking or wrong-thread native work | — | I/D (tripwire) | high on cold start or input paths, else medium |
| 5 | Native listener, sensor or thread alive after teardown | CWE-401 | I/D (leak) | medium; high when it holds an Activity or fires callbacks into a dead JS context |
| 6 | Removed or deprecated runtime APIs at the boundary | RN 0.80 / 0.82 / 0.87 | A (build) | high on ≥ 0.87 (build break); medium on 0.80–0.86 (no-op) |
| 7 | WebView bridge (routed) | MASVS-PLATFORM | — | routed |

### 1. Legacy bridge surface on a New-Architecture-only runtime

```
BAD:   const { Biometrics } = NativeModules; Biometrics.authenticate(r)   // untyped; `undefined` if the module is absent
       class BiometricsModule(ctx) : ReactContextBaseJavaModule(ctx) { @ReactMethod fun authenticate(…) }   // no spec
       newArchEnabled=false (gradle.properties) on react-native 0.82.1   // ignored: the team thinks legacy mode is on
GOOD:  specs/NativeBiometrics.ts: export interface Spec extends TurboModule { authenticate(reason: string): Promise<boolean> }
       export default TurboModuleRegistry.getEnforcing<Spec>('NativeBiometrics');  + codegenConfig + the generated base class
```
**Read the code:** Is the module first-party (migrate it) or a dependency (is a New-Architecture release out; is it maintained)? Does the JS side guard the module's absence (`NativeModules.X?.`) — that turns a crash into a silent no-op, which is worse on a payment path. Is a dead flag (`newArchEnabled=false`, `RCT_NEW_ARCH_ENABLED=0`, `useTurboModules`) the reason someone believes a legacy behaviour still applies? **Finding when** a shipped call goes through the legacy surface on RN ≥ 0.82, or a flag claims an architecture the runtime ignores. **Severity:** medium; high for a legacy-only, unmaintained dependency on a primary flow. **Proof:** A — add the spec; codegen and the build fail on every signature the native side does not match; for a dead flag, the build log shows the New Architecture regardless.

### 2. Contract gap — called on one side, not answered on the other

```
BAD:   JS: Biometrics.cancel()             Android: no @ReactMethod fun cancel        iOS: no ios/ folder → reported as absent
       Dart: _scanner.invokeMethod('torch')  iOS handler: answers "start", "stop" only  → MissingPluginException / a hang
GOOD:  every called method exported on every shipped platform, or the call guarded by Platform.OS with a fallback; Pigeon / codegen
```
**Read the code:** Is the method implemented in a dependency the script cannot see? Is the call platform-guarded (`Platform.OS === 'android'`, `defaultTargetPlatform`)? Does the native handler use a dynamic dispatch the regex missed (a map of handlers)? **Finding when** a shipped call reaches a platform whose native side does not answer it. **Severity:** high. **Proof:** I — a contract test per platform: the JS test calls every method the spec names against the real native module in an instrumented build (Detox / an Android instrumented test / XCTest), or a host test asserting the exported method set equals the called set; the BAD build fails on the missing method.

### 3. Errors that never reach the caller

```
BAD:   @ReactMethod fun authenticate(r: String, promise: Promise) { try { promise.resolve(prompt(r)) } catch (e: Exception) { Log.w(…) } }
       scanner.setMethodCallHandler { call, result in if call.method == "start" { result(nil) } else if call.method == "stop" { … } }
GOOD:  catch (e: Exception) { promise.reject("E_AUTH", e.message, e) } · a final else / default: result(FlutterMethodNotImplemented)
```
**Read the code:** Does every exit of the method resolve or reject exactly once (including early returns and the cancelled path)? Is a Kotlin `when (call.method)` missing `else -> result.notImplemented()`? Does the JS caller time out (a bounded `await` turns a hang into an error — still a finding, lower)? **Finding when** an error path, or an unknown method, leaves the caller's promise or future pending forever. **Severity:** high (a spinner that never ends, a flow that never continues). **Proof:** I — a native unit test forces the failure (throw in `prompt`, an unknown method name) and asserts the promise rejects or the result is `notImplemented` within a bound; it hangs on the BAD code.

### 4. Blocking or wrong-thread native work

```
BAD:   @ReactMethod(isBlockingSynchronousMethod = true) fun readKeyBlob(): String = File(…).readText()   // JS thread waits on disk
       spec: exportLogs(path: string): string   // sync JSI call doing I/O
       Flutter handler reading a file on the platform main thread with no task queue
GOOD:  Promise-returning method, work on a background executor · getBatteryLevel(): number reading a cached value (a sync constant is fine)
       makeBackgroundTaskQueue() for the channel (Flutter) · UI calls marshalled with UiThreadUtil.runOnUiThread / DispatchQueue.main
```
**Read the code:** What does the synchronous body do — read a constant (fine; the RN docs' own example spec is synchronous) or touch disk, network, Keychain or a database? Does a module pinned to the main queue (`requiresMainQueueSetup` YES, `methodQueue` main) do heavy work there? Does an Android module touch Views off the UI thread? **Finding when** a sync or main-pinned call does I/O or unbounded work on a path a user waits on. **Severity:** high on cold start and input handlers. **Proof:** I/D — the release-mode tripwire (StrictMode `penaltyDeath`, Main Thread Checker in the test plan) fails on the call; a frame or long-task trace from `device-harness` on a named device in a release build.

### 5. Native listener, sensor or thread alive after teardown

```
BAD:   @ReactMethod fun watchProximity(l) { sm.registerListener(l, …) }   // no invalidate(): alive after reload / teardown
       func onCancel(withArguments:) -> FlutterError? { return nil }        // the observer onListen added is never removed
GOOD:  override fun invalidate() { sm.unregisterListener(l); executor.shutdown() } · onCancel removes the token and clears the sink
```
**Read the code:** What does the module acquire (listeners, sensors, receivers, executors, timers) and where is each released? Does an emitter stop observing when the last JS listener goes? Does a native object keep a strong reference to an Activity or a JS callback? **Finding when** something acquired at the boundary outlives its owner. **Severity:** medium; high when it holds an Activity or delivers events into a torn-down context (a crash after a reload). **Proof:** I/D — the leak assertion (LeakCanary `DetectLeaksAfterTestSuccess`, an XCTest weak-reference teardown) after the module is invalidated; an event delivered after `onCancel` fails the test.

### 6. Runtime APIs removed or deprecated at the boundary

```
BAD:   InteractionManager.runAfterInteractions(() => NativeModules.Printer.print(id))   // RN 0.87: removed — build break
       import { flattenStyle } from 'react-native/Libraries/StyleSheet/flattenStyle'      // 0.87 Strict API: deep import inaccessible
       uiManager.addUIBlock { … } · RCTEnableTurboModule(YES) · onCatalystInstanceDestroy()  // deprecated
GOOD:  requestIdleCallback(…) · StyleSheet.flatten(…) from 'react-native' · View Commands / UIManagerListener · invalidate()
```
**Read the code:** Which RN version does this root pin (grep 0)? On 0.80–0.86 `InteractionManager` runs the callback immediately (no deferral — `mobile-perf-scan` § 4 owns the jank); on ≥ 0.87 it does not exist. Is the deep-import opt-out condition set in `tsconfig.json`? `AppState.removeEventListener` has been gone since 0.70 ([`precedents/mobile.md`](../../../../snippets/precedents/mobile.md) § 51). **Finding when** a shipped file uses an API its pinned RN version removed or that the next version removes. **Severity:** high on the version that removed it; medium one version ahead. **Proof:** A — `tsc` / the Metro bundle / the native build on the pinned version fails on the BAD line and passes on the fix.

### 7. WebView bridges — routed

Every `addJavascriptInterface`, `onMessage` without an origin check, `WKScriptMessageHandler`, `JavaScriptChannel` or `addJavaScriptHandler` is emitted as `routed_to: mobile-security-scan` (security pack, when installed), with both sides' coordinates. Without the security pack: reported here, `security-class (owner pack not installed)`, severity per the security pack's calibration in [`precedents/mobile.md`](../../../../snippets/precedents/mobile.md) § 42–48.

## Proof — the contract test on both sides

[`proof-oracles.md`](../../../../snippets/proof-oracles.md) § Mobile, *Bridge contract test*: for each module or channel, (a) the set of methods the JS/Dart side calls equals the set every shipped platform answers — asserted by a host test over the codegen schema, or by calling each method once in an instrumented build; (b) each method's failure path rejects within a bound; (c) a sync method stays under the release-mode tripwire. The test **fails before the fix**. A platform with no device or simulator on the host is `SKIPPED (no <platform> runtime)` for (a)–(c) — never PASS, and the row is `[report-flagged]` with the exact test to run.

## Output

```
native-bridge-audit — lanes: react-native 0.82.1 (rn-app/package.json:6), expo 57 / react-native 0.87.0 (expo-app/package.json:5,12),
                      flutter 3.47; codegen: rn-app specs/NativeDeviceInfo.ts (no codegenConfig)
Roots: 6 · Platforms read: rn-app android (no ios/), expo-app none (CNG), flutter_app ios (no android/) → PARTIAL

1. rn-app/src/native/biometrics.ts:11 ↔ rn-app/android/…/bridge/BiometricsModule.kt (no cancel)      [report-with-fix]   high
   §2 Biometrics.cancel() is called from JS and exported on no platform — `undefined is not a function` on the unlock screen.
   Proof: instrumented contract test calls every Biometrics method on Android: cancel throws (fails). Fix: @ReactMethod fun cancel().

2. rn-app/android/…/bridge/BiometricsModule.kt:20                                                    [report-with-fix]   high
   §3 the catch logs and returns: authenticate()'s promise never settles; the unlock button spins forever.
   Proof: native test forces prompt() to throw; the promise neither resolves nor rejects in 5 s (fails). Fix: promise.reject("E_AUTH", …).

3. flutter_app/lib/native/camera_channel.dart:7 ↔ flutter_app/ios/Runner/CameraChannel.swift:8      [report-flagged]    high
   §2/§3 'torch' is invoked and the iOS handler answers only start/stop, with no notImplemented fallback: the future never completes.
   Unproven link: no iOS simulator on the host. Settling run: integration_test invoking every method on an iOS simulator.

Verification: 19 candidates → 2 findings · 1 unconfirmed · 3 hardening · 0 pre-existing · 13 refuted
Routed: §7 1 row → mobile-security-scan (security pack installed)

Class coverage:
  §1 legacy surface            checked (4 hits → 0 findings; 2 hardening: migrate Biometrics to a spec)
  §2 contract gap              checked (6 lines → 1 finding, 1 unconfirmed; Printer: no implementation in repo, read the dependency)
  §3 errors never delivered    checked (2 hits → 1 finding)
  §4 blocking / thread         checked (3 hits → 0 findings; getBatteryLevel reads a cached value)
  §5 teardown                  checked (2 hits → 0 findings; 1 hardening)
  §6 removed APIs              checked (3 hits → 0 findings here; StopsProvider:9 deduped with mobile-perf-scan § 4)
  §7 WebView bridge            routed (1 row)
```

`[report-with-fix]`: both sides cited, the gate read, the contract test failed. `[report-flagged]`: one side or the runtime was unavailable, and the row names the settling run. The coverage block lists **all seven** classes on every run: `checked (k hits → m findings)` only when the grep ran on a present lane; `N/A (<reason>)` when the repo has no such surface (no native modules, no channels); `blocked (<reason>)` when a grep failed or a side could not be read; `Live, unreviewed (k groups / n hits)` for a partial review.

## False positives / precedents

The verifier reads [`precedents/mobile.md`](../../../../snippets/precedents/mobile.md) and [`refute-before-report.md`](../../../../snippets/refute-before-report.md) § 4: the New Architecture on ≥ 0.82 (§ 50), `InteractionManager` and `AppState.removeEventListener` by version (§ 51), a fix in generated native folders of an Expo CNG project (§ 3), Hermes the default (§ 35). And the bridge-specific § 89–93: a synchronous spec method that returns a constant or cached value (§ 89); a method implemented in a dependency's native folder (§ 90); a call guarded by a platform check with a fallback (§ 91); a Turbo Native Module whose mismatch the build already fails — a build error, not an audit finding (§ 92); a Pigeon-generated channel (§ 93).

## When to run

- On a diff that adds or changes a native module, a spec, a channel, a `NativeModules` call, a native dependency, or an RN upgrade across 0.80, 0.82 or 0.87 — and on every whole-repo `/mobile-audit`, reporting all seven classes.
- When a crash report shows `undefined is not a function` on a native call, `MissingPluginException`, or a spinner that never ends after a native call.

## Halt conditions

- Do not report a high row as confirmed until a verifier other than the run that found it has passed it through [`refute-before-report.md`](../../../../snippets/refute-before-report.md) with [`precedents/mobile.md`](../../../../snippets/precedents/mobile.md); standalone, apply it as a separate second pass and tag those rows `self-verified`. Never drop a candidate.
- Halt on any finding without both sides' `<path:line>` (or the stated absence of one side), the gate line and the fix.
- Halt with `PARTIAL` when only one platform was read; never generalise a one-platform audit to "the bridge".
- Do not call a method unanswered before reading the dependency that may implement it.
- Do not propose a Turbo Native Module or Pigeon migration without first stating what the current boundary does (§ 2's set-difference).
- Do not print "bridge is clean" without the class-coverage block.

## Hard rules

- No native boundary without a typed contract (a spec, codegen or Pigeon) on new code.
- No promise or future crossing the boundary that can stay pending; every exit settles exactly once.
- No native resource acquired at the boundary without its release in the module's teardown.
- No bridge call from a module constructor; initialization happens after the runtime is ready.

## Related

- `/mobile-audit` dispatches this skill; `/mobile-fix` closes its rows failing-first with the contract test.
- `mobile-perf-scan` § 4 (JS / main-thread cost), `mobile-lifecycle-scan` § 3 (permissions behind the bridge) (this pack); `mobile-security-scan` (security pack, when installed) for WebView bridges.
- `references/react-native.md` and `references/flutter.md` § Platform channels (this pack) — the per-stack mechanics.
- Sources (read 2026-10-05 unless marked): reactnative.dev blog 0.81, 0.82 and 0.87 release posts and *Turbo Native Modules* (via the react-native-website repository); RN CHANGELOG (InteractionManager, interop flags); docs.flutter.dev *platform channels* (read 2026-08-20). **Deliberately absent**: a bridge-call latency budget, a maximum payload size and a cross-bridge timeout value — none is published; the timeout is a project budget recorded beside the call site.
