---
name: device-harness
description: Boot a named simulator or emulator, install the app and capture evidence on both platforms — screenshots, the UI tree, cold start, a deep-link open, a process-death restore. Produces evidence, never judges it; SKIPPED when no device is available.
kind: skill
pack: mobile
allowed-tools: [Read, Grep, Glob, Bash]
---

# Skill: device-harness

The mobile pack can describe what a screen should do on two platforms and has, until now, had no way to look at either one. This skill is that way. It boots a device, installs the build, drives it, and writes down what it saw — so a claim about the running app is **rendered, not asserted**.

## Premise

Evidence only. Every artifact this skill produces names the **device it ran on** (model and OS version, by name), the **build variant** (debug / release), and the **commit** the build came from. A screenshot with no device name is not evidence — the same layout is correct on one screen size and broken on another, and a perf number from an unnamed device is a number about nothing.

**What this skill asserts is exactly what it captured.** It reports "the screen rendered as attached, on this device, from this build". It does not report that the screen is *correct*, *conformant*, or *accessible* — those are judgements, and they belong to `platform-conventions-audit`, the `ui-ux` pack's floor, and a human. A run that captures nothing reports `SKIPPED` with the reason. It never fills the gap with a description of what the screen probably looks like.

## Halt conditions

- **No simulator / emulator and no physical device available → HALT with `SKIPPED`** and the reason. Do not describe the UI from the source code; that is the exact failure this skill exists to prevent.
- **Build failed → HALT.** Fix the build first. There is no partial evidence from a binary that does not exist.
- **Only one platform was exercised → report `PARTIAL`**, naming the platform that was not covered. Never generalise a one-platform observation to "both platforms".
- **Refuse to report a performance number from a debug build.** Debug builds carry dev tooling and unoptimised code; a startup or frame number from one is fiction. Either build release or report the measurement as `not measured`.
- **Refuse to report a startup or frame figure from a single run.** Report the runs individually or report a median with the run count; a single sample from a warm simulator is noise.
- **Refuse to name a device generically.** "an iPhone", "an Android phone", "a mid-range device" are not device names. Take the identifier from the tooling output.
- **Refuse to claim a deep link, push, or permission dialog "works" without the captured screenshot or command output showing it.**

## When to use

- A change must be seen running before it is called done — a new screen, a navigation change, a platform-conditional branch.
- `/polish` on a `mobile-*` stack needs a per-platform UI tree or screenshots for `platform-conventions-audit` to reason over.
- A deep-link route table needs each entry actually opened on a device rather than read off the config.
- A lifecycle claim needs the cold-start-after-process-death test from `app-lifecycle` actually run.
- Before a build goes to beta testers (`release-pipeline`) — the last cheap moment to catch an install-over-upgrade or first-launch failure.
- A bug report says "only on Android" / "only on iOS" and the divergence has to be reproduced rather than reasoned about.

**Not for:** bundle or binary size (`app-size-scan`); JS↔native bridge correctness (`native-bridge-audit`); deciding whether a static component tree conforms to a platform spec (`platform-conventions-audit` — this skill supplies its inputs); production performance profiling (the `performance` pack); automated regression suites (the `testing` pack owns E2E strategy and framework choice — this skill is a one-shot look, not a suite).

## Inputs (precise contract)

| Input | Source | Required |
|---|---|---|
| Codebase root | Orchestrator | YES |
| Mobile surface | Derived from the repo markers (§ 1): an `android/` folder or Gradle app module, an `ios/` folder or Xcode project, an Expo or Flutter config. No marker → halt, `SKIPPED (no mobile project)` | derived |
| Target platforms | Derived from the same markers (an Expo CNG project with no `ios/` still targets iOS — read `app.json`); the caller may narrow them | derived |
| Build variant | Caller (default: debug for visual capture, release for any measurement) | NO |
| Target screens / routes | Caller, or the navigation config | NO (default: launch screen only) |
| Named device(s) | Caller, else the first available from the tooling, recorded by name | NO |
| Deep links to exercise | `deep-linking`'s route table, if present | NO |

## Procedure

### 1. Detect the stack and its run command

Read the project markers before choosing a command — the wrong launcher produces a build that does not match what CI ships.

| Marker present | Build / run route |
|---|---|
| A cross-platform JS runtime with a native project directory | The project's own run script for each platform, or the platform toolchains directly |
| A cross-platform JS runtime with a managed native layer | The project's dev-client or prebuild route — a managed project may not have native directories to build from |
| A Dart-runtime project | The framework CLI with an explicit device id |
| A native iOS project only | `xcodebuild` for the simulator destination, then install |
| A native Android project only | The Gradle install task for the debug variant |

If the stack cannot be determined from markers, halt and ask — do not guess a build command.

**The iOS half is unverified.** Every command tagged `[K]` below comes from the research catalog and has not been executed by any run of this skill: the authoring host had Command Line Tools only, no Xcode (checked 2026-10-05: `xcrun --find simctl` fails). Before relying on one, run `xcrun simctl help <subcommand>` (or `xcrun xctrace help`) on the Mac with Xcode; a command that errors is `SKIPPED (<command> unavailable)` for that row, never a pass and never replaced by a description of what it would have shown.

### 2. Enumerate and boot a **named** device

```bash
# iOS — list what actually exists on this machine, then boot by UDID
xcrun simctl list devices available
xcrun simctl boot "<UDID>"
open -a Simulator

# Android — list AVDs, start one, wait for it to be ready
emulator -list-avds
emulator -avd "<AVD_NAME>" -no-snapshot-load &
adb wait-for-device
adb shell 'while [[ "$(getprop sys.boot_completed)" != "1" ]]; do sleep 1; done'

# Physical devices, if any
xcrun devicectl list devices
adb devices -l
```

Record the exact device name and OS version from this output. It goes in the report header, and every later claim is scoped to it.

### 3. Install and launch

```bash
# iOS simulator
xcrun simctl install booted "<path/to/App.app>"
xcrun simctl launch booted "<bundle.identifier>"

# Android
adb install -r "<path/to/app-debug.apk>"
adb shell am start -n "<application.id>/<.MainActivity>"
```

For an **install-over-upgrade** check, install the previously released build first, launch it once, then install the new one **without** uninstalling. A clean install passing tells you nothing about the upgrade path, and the upgrade path is where migrations fail.

### 4. Drive to the target screen

Prefer a deterministic entry over tapping through the UI — taps are coordinate-dependent and break with every layout change.

```bash
# Deep link — the same URLs deep-linking tabulates
xcrun simctl openurl booted "<scheme-or-universal-link>"
adb shell am start -W -a android.intent.action.VIEW -d "<scheme-or-app-link>" "<application.id>"
```

Every route in the project's deep-link table gets opened, and the resulting screen is captured. A route that opens the wrong screen, or the launch screen, is a finding with its command and screenshot attached.

### 5. Capture evidence

```bash
# Screenshots
xcrun simctl io booted screenshot "<out>/ios-<screen>.png"
adb exec-out screencap -p > "<out>/android-<screen>.png"

# Android UI tree — the structured input platform-conventions-audit reasons over; its content-desc order is
# the reading order mobile-a11y-scan § 5 reads
adb shell uiautomator dump /sdcard/window_dump.xml
adb pull /sdcard/window_dump.xml "<out>/android-<screen>-tree.xml"

# iOS accessibility tree [K] — the research catalog records no simctl subcommand that dumps it; use one of:
#   a UI test that prints the element tree: print(XCUIApplication().debugDescription)   (xcodebuild test, below)
#   maestro hierarchy                       (Maestro CLI, booted simulator)
#   idb ui describe-all --udid "<UDID>"     (idb + idb-companion installed)
xcodebuild test -scheme "<UITestScheme>" -destination "platform=iOS Simulator,id=<UDID>" \
  -only-testing:"<UITests>/TreeDump/testDumpTree" > "<out>/ios-<screen>-tree.txt"   # [K]

# Logs during the interaction
xcrun simctl spawn booted log stream --level debug > "<out>/ios-<screen>.log" &
adb logcat -c && adb logcat -d > "<out>/android-<screen>.log"
```

Capture the **same screens on both platforms**, with the same entry route, or the comparison is not a comparison. A tree is evidence for `mobile-a11y-scan` and `platform-conventions-audit`; this skill does not read it for a verdict.

**Variant captures** the detectors ask for — each is a separate capture, named in the file:

```bash
# Android: largest font, dark, 3-button vs gesture navigation (edge-to-edge insets at targetSdk 35 / 36)
adb shell settings put system font_scale 2.0                                     # [K]
adb shell cmd uimode night yes                                                   # [K]
adb shell cmd overlay enable com.android.internal.systemui.navbar.threebutton   # [K] overlay name per image
adb shell cmd overlay enable com.android.internal.systemui.navbar.gestural      # [K]

# iOS simulator [K]: largest Dynamic Type size, dark appearance, a fixed status bar for comparable screenshots
xcrun simctl ui booted content_size accessibility-extra-extra-extra-large
xcrun simctl ui booted appearance dark
xcrun simctl status_bar booted override --time "9:41"
```

Reset every variant after the run (`font_scale 1.0`, `night no`, `content_size large`, `status_bar booted clear`) and record the reset — a later run inheriting a variant is the confusion the failure modes list names.

### 6. Optional measurements — release build only

```bash
# Android cold start: force-stop first, then measure; repeat and report each run
adb shell am force-stop "<application.id>"
adb shell am start -W -n "<application.id>/<.MainActivity>"   # reports TotalTime

# iOS cold start [K] — Release configuration, repeated runs; either the launch metric in a UI test:
#   func testLaunch() { measure(metrics: [XCTApplicationLaunchMetric()]) { XCUIApplication().launch() } }
xcodebuild test -scheme "<UITestScheme>" -configuration Release \
  -destination "platform=iOS Simulator,id=<UDID>" -only-testing:"<UITests>/LaunchTests/testLaunch"
# or an Instruments trace (template names unverified on a CLT-only host; list them with `xcrun xctrace list templates`)
xcrun xctrace record --template 'App Launch' --device "<UDID>" --launch -- "<path/to/App.app>" --output "<out>/ios-launch.trace"
```

`TotalTime` from `am start -W` is a real, tool-reported number for **this device, this build, this run**. Report it with the device name and the run count, never as "the app's cold start". The iOS launch metric reports its own runs and spread; a simulator number is a regression signal on the same simulator, never a device-class claim. Where neither command runs, report `not measured` rather than substituting a stopwatch.

### 7. Optional lifecycle checks

```bash
# Process death, then relaunch from Recents — the app-lifecycle restoration test.
# STEP 1 IS NOT OPTIONAL: `am kill` "kills only processes that are safe to kill and that will
# not impact the user experience" — a FOREGROUNDED app is not safe to kill, so on a foregrounded
# app this line is a no-op and the relaunch below resumes the live process.
adb shell input keyevent KEYCODE_HOME      # background it first, or the kill does nothing
adb shell am kill "<application.id>"       # system-style kill; NOT a task-switcher swipe
adb shell ps -A | grep "<application.id>"  # MUST print nothing — this is the proof the kill landed
adb shell input keyevent KEYCODE_APP_SWITCH   # open Recents; the killed app's task is still listed
adb shell screencap -p /sdcard/recents.png && adb pull /sdcard/recents.png "<out>/recents.png"   # find its card
adb shell input tap "<x>" "<y>"                # tap the app's card — the task relaunches with its saved state
# Instrumented form: UiDevice.pressHome(); executeShellCommand("am kill <application.id>"); pressRecentApps(); click the task.

# Permission states — reset to exercise the not-determined path; revoke to exercise the denied one
adb shell pm reset-permissions
adb shell pm revoke "<application.id>" "<android.permission.X>"     # the OS kills the process; the relaunch must re-check
xcrun simctl privacy booted reset all "<bundle.identifier>"
xcrun simctl privacy booted revoke "<service>" "<bundle.identifier>"   # [K]
```

`adb shell am kill` exercises the saved-state path that a task-switcher swipe does not. This is the mechanism behind `app-lifecycle`'s cold-start-after-process-death test; run it, capture the restored screen, and compare against the screen you left. **Relaunch from Recents, never from the launcher** (`monkey -c android.intent.category.LAUNCHER`, the home-screen icon, `am start` of the launcher activity): the restoration contract is the task being brought back with its saved state, which is the path the research catalog's process-death row and `mobile-lifecycle-scan` § Proof specify; a launcher intent is a different entry, and whether it resumes the task or starts the root activity again depends on the root activity's launch mode and flags — so a pass through it is not this test. Record which entry ran.

**Report the process check, not just the restore.** The `ps` line above is the only evidence that a kill happened at all, and without it this step is the easiest false PASS in the pack: a no-op kill followed by a resume looks exactly like a perfect restoration. If `ps` still shows the process, the step is `SKIPPED (kill did not land)` — never a restore claim. `@offline-sync-auditor` caps every `durable` verdict at `unproven` without a real kill, so a false PASS here launders an unproven write into a proven one. (`am force-stop` stops everything associated with the package, but it also clears state the saved-state path is supposed to exercise — it is the wrong instrument for *this* test and the right one for the cold-start measurement in step 6.)

**iOS process death [K].** There is no `am kill` equivalent, and the research catalog leaves one question open: whether `xcrun simctl terminate` after backgrounding keeps restoration data (the Flutter restoration docs use Xcode's Stop button instead). Until a run settles it, the recipe is the one closest to the OS's own kill, and each step records its output:

```bash
xcrun simctl launch booted com.apple.Preferences                        # [K] foreground another app: ours is backgrounded
xcrun simctl spawn booted launchctl list | grep "<bundle.identifier>"   # [K] note the PID of the backgrounded app
kill -9 "<PID>"                                                         # [K] the simulator app is a host process
xcrun simctl spawn booted launchctl list | grep "<bundle.identifier>"   # [K] MUST show no PID — the proof the kill landed
xcrun simctl launch booted "<bundle.identifier>"                        # [K] relaunch, then capture and compare
```

The same rules hold as on Android: no proof the process died → `SKIPPED (kill did not land)`; XCUITest `terminate()` + `launch()` is a cold start and never this test; a swipe from the app switcher is not process death. Where Xcode is available interactively, background the app and press Stop, then relaunch from the home screen — the variant the platform docs use — and record which of the two ran.

```bash
# Push to a booted simulator [K] — a local payload, not APNs delivery
xcrun simctl push booted "<bundle.identifier>" "<payload.apns>"
```

### 8. Tear down and write the report

Uninstall the build if the device is shared, stop any log stream, and write the artifact below. Leave the captured files in place — the report references them by path and a report whose evidence has been deleted is an assertion again.

## What this harness cannot decide

Stated plainly, because a skill that captures evidence is dangerous exactly where it starts editorialising:

- **Whether the screen is correct.** It captures pixels. Intent lives in the design and the spec; `platform-conventions-audit` and the `ui-ux` pack's floor judge conformance, and a human judges intent.
- **Whether it is accessible.** A screenshot cannot see focus order, screen-reader labels, or announcement text. The captured tree is evidence for `mobile-a11y-scan` (this pack), judged by `@ux-reviewer` (ui-ux pack, when installed); this harness does not read it for a verdict.
- **Real-world performance.** A simulator runs on desktop-class hardware; an emulator is not a phone. Startup and frame numbers from either are useful as a *regression signal on the same device*, never as a device-class claim.
- **Thermal, radio, and battery behaviour.** None of it exists on a simulator. Anything that depends on a real radio, a real battery, or a real GPS fix must be run on hardware, and the report must say which.
- **Push delivery end to end.** A simulator can be handed a local payload; it is not an APNs/FCM delivery. The token lifecycle stays `push-notifications`' problem.
- **In-app purchases, and anything behind a store account.** Sandbox behaviour differs from production and neither is reproducible here.
- **Whether the *release* build behaves like this.** Unless the run explicitly built release, everything captured is debug behaviour — different optimisation, different logging, and on Android a different obfuscation state.
- **Anything on a device it did not run on.** One device is one data point. Two platforms is two data points.

## Output format

```
## Device harness — <date>

Build: <commit> · variant <debug|release>
Devices:
  - iOS      <device name> · <OS version> · <simulator|physical>
  - Android  <device name or AVD> · <API level> · <emulator|physical>
Status: OK | PARTIAL (<platform not covered>) | SKIPPED (<reason>)

### Captured
| Screen / route | Entry command | iOS | Android |
|---|---|---|---|
| <name> | <deep link or launch> | <path/to/ios.png> | <path/to/android.png> |

### Divergences observed
- <what differs between the two captures — described, not judged>

### Deep links exercised
| Route | Command | Landed on | Expected | Match |
|---|---|---|---|---|

### Measurements (release build only)
| Metric | Device | Runs | Values | Source |
|---|---|---|---|---|
| Cold start TotalTime | <Android device> | <n> | <ms per run> | `am start -W` |
| Launch duration | <iOS device> | <n> | <per run, as the metric reports> | `XCTApplicationLaunchMetric` / `xctrace` App Launch — or `not measured (<reason>)` |

### UI trees
| Screen | iOS tree | Android tree |
|---|---|---|
| <name> | <path, or SKIPPED (<command> unavailable)> | <path/to/android-tree.xml> |

### Lifecycle checks
- Process death → relaunch from Recents (Android, `am kill` + `ps` proof): <restored to <screen> | lost state | SKIPPED (kill did not land) | not run>
- Process death → relaunch (iOS, which variant ran: `kill -9` + launchctl proof, or Xcode Stop): <restored | lost state | SKIPPED (<reason>) | not run>
- Install-over-upgrade: <clean | failed at <step> | not run>

### Not determined by this run
- <every claim the caller might want that this harness cannot support — see "What this harness cannot decide">
```

## Outputs

- `ai/runtime/device-harness-<date>.md` — the report above.
- `ai/runtime/device-harness-<date>/` — the captured screenshots, UI trees, and logs it references.
- When dispatched by `/polish`: the per-platform captures that `platform-conventions-audit` reads as its UI-tree input.

## Hard rules

- **No claim about the running app without a captured artifact.** A sentence in the report maps to a file in the output directory, or it does not ship.
- **No device without a name.** Model / AVD and OS version, taken from tooling output, in the report header.
- **No measurement from a debug build**, and no single-run measurement reported as a figure.
- **No cross-platform claim from one platform.** `PARTIAL` is an honest status; a generalisation is not.
- **No UI judgement.** Describe the divergence; route the verdict to the skill that owns the axis.
- **`SKIPPED` beats invention.** A run with no device produces a status line and a reason, never a description.

## Failure modes (your own work)

- Captured a screenshot before the screen finished loading, and reported an empty state as the screen.
- Booted a device with a stale build installed; the capture shows last week's UI. Always install as part of the run.
- Compared an iOS capture from one route against an Android capture from another and called the difference a platform divergence.
- Reported an emulator startup number as a device-class claim.
- Ran only the clean-install path and missed a migration that fails on upgrade.
- Left `pm reset-permissions` / privacy reset applied and confused a later run's permission state; left a font-scale, dark-mode or status-bar override in place for the next run.
- Reported an iOS row from a `[K]` command that was never run on a Mac with Xcode.
- Treated a task-switcher swipe as process death — it does not exercise the saved-state path.
- Relaunched from the launcher icon or `monkey` after the kill and reported the result as a Recents restore.
- Let the log stream keep running after the app exited, filling the artifact directory with noise the report then cites.

## Related

- `platform-conventions-audit` (skill) — consumes this skill's per-platform captures (API 35 / 36, gesture and 3-button navigation, a notched simulator); it judges conformance, this skill produces the evidence.
- `mobile-a11y-scan` and `mobile-lifecycle-scan` (skills) — read the trees, the largest-font captures and the process-death runs this skill produces.
- `app-lifecycle.md` — defines the cold-start-after-process-death test that step 7 performs.
- `deep-linking.md` — owns the route table; step 4 opens every entry in it.
- `app-size-scan` (skill) — sizes the release artifact; this skill runs the release smoke test after a shrink change.
- `release-pipeline.md` — the last check before a build reaches a beta tester.
- `native-bridge-audit` (skill) — bridge correctness by inspection; this skill can reproduce a bridge bug on a device but does not audit the code.
- cross-pack `testing` — owns E2E strategy and framework choice; this skill is a one-shot look, not a regression suite.
