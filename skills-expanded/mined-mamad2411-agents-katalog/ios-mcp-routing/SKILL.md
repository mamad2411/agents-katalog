---
name: ios-mcp-routing
description: >
  Route Apple/iOS agent work between Argent MCP and XcodeBuildMCP (and when to
  combine both in one session). Use when choosing tooling for build, compile,
  test, run, install, launch, simulator control, UI automation, screenshots,
  QA, LLDB debug, logs, permissions, profiling, physical device, macOS, Android,
  Chromium, TV, or when both MCP servers are available and the agent might pick
  the wrong one. Triggers: "which tool", "Argent or XcodeBuild", "XcodeBuildMCP",
  build then verify UI, fix compile error then QA, run on simulator, XCTest,
  snapshot_ui vs describe. Slash: /ios-mcp-routing
---

# iOS MCP routing (Argent vs XcodeBuildMCP)

Decide the **primary** tool by task class. Prefer one owner per phase. Combine
only at clean handoff points (usually: **XcodeBuildMCP builds → Argent verifies**).

## 0. Availability check (once per session)

1. **XcodeBuildMCP** — MCP tools present (`XcodeBuildMCP__*`) and/or `command -v xcodebuildmcp`.
2. **Argent** — MCP tools present (`argent__*`) and/or `command -v argent`.
3. If only one is available, use it within its strengths; do not invent the missing one.
4. If neither is available, fall back to shell (`xcodebuild`, `xcrun simctl`, `adb`) and say so.

Load this skill before defaulting to either stack for Apple platform work.

## 1. One-line rule

| Need | Primary |
| --- | --- |
| Compile, scheme/test, LLDB, coverage, project/schemes, macOS, physical iOS device build | **XcodeBuildMCP** |
| Drive UI, QA, screenshots/diff, permissions, flows, multi-platform (Android/Chromium/TV), RN runtime inspect, native perf traces | **Argent** |
| "Change code → build → prove the UI" | **Both** (XcodeBuildMCP then Argent) |

## 2. Decision tree

```
What is the bottleneck / goal?
│
├─ Does it need a successful Xcode/SwiftPM build or XCTest run?
│  └─ YES → XcodeBuildMCP (session defaults → build / test / build_run_sim)
│
├─ Is the app already installed and the task is "use / verify the product"?
│  └─ YES → Argent (list-devices → launch-app → describe → interact)
│
├─ Compile/link/signing failure?
│  └─ XcodeBuildMCP only (fix build; do not start Argent UI loops)
│
├─ Runtime crash / wrong UI / flow / visual regression?
│  └─ Prefer Argent for interaction + evidence
│     (optional: XcodeBuildMCP log capture / LLDB if you need native stack)
│
├─ Android, Chromium/Electron, Fire TV / Apple TV remote, RN Metro inspect?
│  └─ Argent only (XcodeBuildMCP does not own these)
│
└─ Physical iOS device install/run/test, or macOS app?
   └─ XcodeBuildMCP (Argent iOS path is simulator-first)
```

## 3. Capability map (what each owns)

### XcodeBuildMCP — build system + Apple toolchain

**Owns:**

- Project discovery: `discover_projs`, `list_schemes`, `show_build_settings`
- Session defaults: `session_show_defaults` / `session_set_defaults` (required before first build/run/test)
- Simulator: `build`, `build_run_sim`, `test_sim`, `install_app_sim`, `launch_app_sim`, `stop_app_sim`, `boot_sim`, `open_sim`, `list_sims`
- Clean / app path / bundle id extraction
- Physical device and macOS build/run/test
- SwiftPM build/test/run
- LLDB: attach, breakpoints, stack, variables, continue/detach
- Code coverage from xcresult
- Sim management extras: erase, location, appearance, status bar, video record
- Built-in UI automation via **elementRef** (`snapshot_ui` → `tap` / `type_text` / `swipe` / `wait_for_ui` / `batch`)

**Does not own (or is weak for):**

- Android / Chromium / Vega
- Permission grant/deny/reset without Settings UI
- Screenshot pixel-diff workflows, record/replay flows
- React Native Metro component tree / JS eval
- Native Instruments/Perfetto-style profiling pipelines Argent provides
- Cross-app system AX for arbitrary foreground content as rich as Argent `describe` (Argent is preferred for agent QA loops)

**Mandatory session habit:** before first build/run/test call, `session_show_defaults`. If project/scheme/simulator missing, set them. Prefer `build_run_sim` over separate build+install+launch unless you need a compile-only check.

### Argent — device runtime, interaction, QA

**Owns:**

- Multi-platform device inventory: `list-devices` (iOS sim, Android emu/device, Chromium CDP, Vega)
- Boot/launch/restart/reinstall: `boot-device`, `launch-app`, `restart-app`, `reinstall-app`
- Discovery: `describe` (AX/DOM), `native-describe-screen` (iOS UIKit), RN `debugger-component-tree`
- Interaction: gestures, keyboard (incl. secret placeholders), hardware buttons, deep links (`open-url`)
- Waiting: `await-ui-element`, `await-screen-idle`
- Evidence: `screenshot`, `screenshot-diff`
- Setup: `settings-permissions`
- Automation reuse: flow record/execute (`.argent/flows/`)
- Profiling: native profiler (+ RN profiler when RN)
- TV: `tv-remote` + focus-oriented `describe`

**Does not own:**

- Xcode scheme builds, clean, XCTest orchestration, coverage reports
- LLDB source-level debugging of native binaries
- Guaranteed physical-iOS parity (treat Argent iOS as **simulator-first**)
- Replacing `pnpm ios:prepare` / XcodeGen / Fastlane release pipelines

**Mandatory interaction habit:** never guess tap coordinates from a screenshot alone — always discover (`describe` / native / RN tree) first. Prefer `launch-app` over home-screen icon taps.

### Overlap zone (pick one primary)

Both can: boot a sim, launch an installed app, screenshot, basic tap/type.

| Overlap task | Prefer | Why |
| --- | --- | --- |
| Build + install + first launch after code change | **XcodeBuildMCP** `build_run_sim` | Compiles; Argent cannot build |
| Re-launch already installed app for QA | **Argent** `launch-app` / `restart-app` | Faster; native-devtools prep on iOS |
| UI exploration / multi-step QA | **Argent** | Richer discovery, waits, diffs, flows, multi-platform |
| Quick elementRef taps right after an XcodeBuildMCP run | **XcodeBuildMCP** UI tools OK for short checks | Same stack; avoid thrashing |
| Long QA, visual regression, permissions, RN/Android | **Argent** | Specialty tools |
| XCTest / unit/UI test targets | **XcodeBuildMCP** `test_sim` / device test | Real test runner |
| Manual agent "click through the app" | **Argent** | Designed agent loop |

**Do not** interleave Argent gestures and XcodeBuildMCP `snapshot_ui`/`tap` on the same screen without a deliberate refresh — elementRefs and coordinate spaces are stack-specific. Finish one automation style, then switch only at a stable boundary (e.g. after navigation settle).

## 4. When to combine in one session

### Pattern A — implement → build → UI verify (most common)

1. Edit code.
2. **XcodeBuildMCP:** `session_show_defaults` → fix defaults → `build_run_sim` (or `build` if install not needed).
3. On build failure: stay on XcodeBuildMCP until green. Do not open Argent yet.
4. On success: note **simulator UDID/name** and **bundle id** from defaults / `get_app_bundle_id`.
5. **Argent:** `list-devices` → same UDID → `describe` / interact / `screenshot` / optional `screenshot-diff`.
6. If UI wrong → fix code → return to step 2 (rebuild). If only JS/web content in a hybrid shell and no native rebuild needed, relaunch/reload as the project requires, then Argent again.

### Pattern B — compile-only gate, then manual QA later

1. XcodeBuildMCP `build` (simulator, no launch).
2. Later Argent session for QA against an already-installed build (or reinstall via Argent `reinstall-app` using `get_sim_app_path` / known `.app` path).

### Pattern C — crash / native bug

1. Reproduce with Argent (or XcodeBuildMCP UI) to get to the crash.
2. Attach **XcodeBuildMCP** LLDB (`debug_attach_sim`, breakpoints, stack, variables).
3. After fix: XcodeBuildMCP rebuild; Argent re-verify the flow.

### Pattern D — test suite + exploratory QA

1. XcodeBuildMCP `test_sim` for automated tests / coverage.
2. Argent for scenarios tests do not cover (permissions matrix, visual diff, multi-step product flows).

### Pattern E — hybrid monorepo (native host + web/miniapps)

1. Native host changes → XcodeBuildMCP build/run.
2. In-app UX / miniapp surface → Argent `describe` + screenshots (WKWebView content may be sparse in AX; use screenshot + careful discovery).
3. Pure web package work → not these tools (web browser tooling / project web scripts).

## 5. Shared identifiers (handoff contract)

When combining tools, pass these explicitly between phases:

| Token | Source | Consumers |
| --- | --- | --- |
| Simulator UDID | XcodeBuildMCP defaults / `list_sims`; Argent `list-devices` | All launch/interact tools |
| Scheme + configuration | XcodeBuildMCP defaults | Rebuilds |
| Bundle ID | project / `get_app_bundle_id` / session `bundleId` | Argent `launch-app`, permissions, reinstall |
| `.app` path | XcodeBuildMCP `get_sim_app_path` | Argent `reinstall-app` after clean install needs |
| Log file path | XcodeBuildMCP launch/build_run responses | Crash diagnosis |

**Prefer one booted simulator for the whole session.** If XcodeBuildMCP boots sim A and Argent boots sim B, launches and UI state diverge.

## 6. Anti-patterns

1. **Argent for compile errors** — it will not fix or surface xcodebuild diagnostics; use XcodeBuildMCP.
2. **XcodeBuildMCP as the only tool for multi-step product QA** when Argent is available — weaker flows, no screenshot-diff/permissions/Android.
3. **Building with raw `xcodebuild`/`simctl` when XcodeBuildMCP is connected** — prefer MCP session defaults (skill: `xcodebuildmcp-cli`).
4. **Tapping from screenshots with either stack** when a discovery API exists.
5. **Starting Argent UI work before the new binary is installed** after native code changes — rebuild first.
6. **Assuming the repo is React Native** because Argent has RN skills — detect project type; native-only hosts skip Metro/debugger-component-tree.
7. **Mixing elementRef taps and Argent coordinate taps** mid-flow without re-discovering.
8. **Physical device QA defaulting to Argent** — use XcodeBuildMCP device workflow unless Argent explicitly supports the target in this environment.

## 7. Suggested skill handoff

After choosing the primary tool, load the specialized skill (do not re-encode their full procedures here):

| Situation | Next skill |
| --- | --- |
| XcodeBuildMCP usage / CLI discovery | `xcodebuildmcp-cli` |
| Argent iOS sim boot | `argent-ios-simulator-setup` |
| Argent taps/gestures/screenshots | `argent-device-interact` |
| Agent QA loops | `argent-test-ui-flow` |
| Visual regression | `argent-screenshot-diff` |
| Permissions without Settings UI | `argent-settings-permissions` |
| Record/replay | `argent-create-flow` |
| Native perf | `argent-native-profiler` |
| RN (only if project is RN) | `argent-react-native-app-workflow`, `argent-metro-debugger` |
| Android / TV | `argent-android-emulator-setup`, `argent-tv-interact` |

## 8. Quick recipes

### "Build the iOS app"

XcodeBuildMCP only → defaults → `build` or `build_run_sim`.

### "Is the new button on screen / does the menu work?"

If binary current: Argent only.
If you just changed native UI code: XcodeBuildMCP `build_run_sim`, then Argent QA.

### "XCTest failed"

XcodeBuildMCP `test_sim` (and logs/coverage). Use Argent only if you need to reproduce a manual path the test does not cover.

### "Need Android or webview Electron too"

Argent. XcodeBuildMCP is out of scope.

### "LLDB breakpoint in Swift"

XcodeBuildMCP debugging workflow. Argent does not replace LLDB.

## 9. Exit criteria

Before acting, state (internally or briefly to the user when ambiguous):

1. **Primary tool** for this step: Argent | XcodeBuildMCP | both (ordered).
2. **Why** (one sentence from the decision tree).
3. **Handoff tokens** if both: UDID, bundle id, scheme.
4. **Specialized skill** loaded next.

If the user already named a tool, honor that unless it is impossible (e.g. "Argent build my scheme" → explain and use XcodeBuildMCP for build).

## References

- Capability detail and edge cases: `references/capability-matrix.md`
