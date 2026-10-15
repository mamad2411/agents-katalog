---
name: ios-simulator-testing
description: End-to-end iOS simulator testing using blitz-iphone MCP and XcodeBuildMCP. Use this skill when testing an iOS app on the simulator — building, launching, interacting with the UI, and verifying state. Covers which MCP to use and when, gesture mechanics, and interaction patterns learned from real test runs.
metadata:
  author: arjitjaiswal
  version: "1.1.0"
---

## Which tool to use and when

Two MCP servers are available for iOS testing. They have distinct roles and should not be interchanged:

### XcodeBuildMCP — build, boot, and install
Use XcodeBuildMCP for everything **before** you start touching the UI:

| Task | Tool |
|---|---|
| Check session defaults (project, scheme, simulator) | `session_show_defaults` |
| Build and run on simulator | `build_run_sim` |
| Build only (no run) | `build_sim` |
| List available simulators | `list_sims` |
| List schemes in project | `list_schemes` |
| Boot a specific simulator | `boot_sim` |
| Install a pre-built .app | `install_app_sim` |
| Capture logs from simulator | `start_sim_log_cap` / `stop_sim_log_cap` |
| Run tests | `test_sim` |

**Always call `session_show_defaults` before the first build** in a session to confirm project/scheme/simulator are configured. Never assume defaults are set.

### blitz-iphone — interact with the running app
Use blitz-iphone for everything **after** the app is running:

| Task | Tool |
|---|---|
| Take a screenshot | `get_screenshot` |
| Get full UI hierarchy with coordinates | `describe_screen` |
| Find tappable elements | `scan_ui` |
| Tap, swipe, type, press buttons | `device_action` |
| Launch an app by bundle ID | `launch_app` |
| List installed apps | `list_apps` |
| List connected devices/simulators | `list_devices` |

**blitz-iphone is the only tool you should use for UI interaction.** Do not use XcodeBuildMCP's UI automation tools (`snapshot_ui`, `tap`) in parallel — they conflict.

---

## The golden rule: screenshot after every action

**Never chain multiple actions without taking a screenshot in between.**

Every action can have unexpected results:
- A tap might open a photo viewer instead of selecting a card
- A swipe might navigate away instead of triggering a gesture
- A button might be behind a dialog you didn't know appeared
- An animation might still be in progress

The pattern is always:
```
action → get_screenshot → verify → next action
```

If you batch 3-4 actions and something goes wrong, you won't know which one caused it. Screenshots are cheap; debugging blind interactions is not.

---

## Gesture mechanics

### Swipe length matters
Short swipes (~100pt) often silently fail on gesture-based UIs (swipeable cards, dismissible sheets, paging views). **Always use swipes of 250pt or more** for intent-driven gestures:

```
# Too short — may not register
fromX: 120, toX: 220  # only 100pt

# Reliable
fromX: 60, toX: 350   # 290pt — always registers
```

For "swipe left to reject" / "swipe right to accept" card UIs, swipe from near one edge to near the other:
- Pick left: `fromX: 60, toX: 350`
- Reject/remove: `fromX: 350, toX: 50`

### Tapping images opens full-screen viewers
In iOS apps with photo/media content, **a single tap on an image usually opens a full-screen viewer**. If you meant to select it (e.g. for a ranking comparison), you've now opened the viewer instead.

To dismiss a full-screen photo viewer:
1. Try swipe down: `fromX: 200, fromY: 400, toX: 200, toY: 800`
2. If that doesn't work, use `describe_screen` to find the X/close button and tap it

Do not attempt to use macOS keyboard shortcuts (Cmd+A, Esc) via AppleScript — they don't work on the iOS simulator's UI layer. Use iOS-native gestures only.

### When taps miss
If a tap doesn't produce the expected result:
1. Call `describe_screen` to get the exact `AXFrame` of the target button
2. Calculate the center: `x = frame.x + frame.width/2`, `y = frame.y + frame.height/2`
3. Tap that exact coordinate

Don't guess coordinates from screenshots — the accessibility tree gives ground truth.

---

## First-launch handling

On a fresh or reset simulator, apps show system dialogs and onboarding that must be dismissed before testing:

- **Notification permission dialogs** — tap "Don't Allow" or "Allow" as appropriate for the test
- **Photo library access dialogs** — tap "Allow" if the app needs photo access
- **App-specific welcome/onboarding screens** — swipe or tap through them

These appear once and won't block subsequent runs on the same simulator, but always check for them at the start of a session.

---

## Standard test session flow

```
1. session_show_defaults           # verify project/scheme/simulator
2. build_run_sim                   # build and launch
3. get_screenshot                  # confirm app is running
4. [handle first-launch dialogs]   # dismiss permissions/onboarding
5. get_screenshot                  # confirm main UI is visible
6. [interact with describe_screen + device_action + get_screenshot loop]
```

---

## Navigating to the home screen / other apps

To leave the current app and go to the home screen:
```json
{ "action": "button", "params": { "button": "HOME" } }
```

To open another app (e.g. Photos to verify an export):
- Press HOME, then use Spotlight search: swipe down on home screen → type app name → tap result
- Or use `launch_app` with the bundle ID if you know it

---

## XCUITest vs agent-driven testing: when to use which

XcodeBuildMCP's `test_sim` can run XCUITest suites, which is a different mode of UI testing from the interactive blitz-iphone approach. They're complementary — choose based on what you're trying to achieve.

### Use `test_sim` + XCUITest when:
- The flow is well-defined and repeatable (login, onboarding, form submission)
- You want **regression coverage** that runs in CI without an agent
- Speed matters — XCUITest runs are 5-10x faster than agent-driven interaction
- The project already has XCUITest infrastructure to build on

### Use blitz-iphone agent-driven testing when:
- You're doing **exploratory testing** — navigating a complex multi-step flow where the next action depends on what the previous one produced
- The flow requires **visual judgment** (does this photo look correctly letterboxed? does this animation feel right?)
- You're testing a flow that doesn't yet have XCUITest coverage and you want to smoke-test it quickly
- The flow involves system-level interactions (Photos app, permission dialogs, other apps) that are awkward to script in XCUITest

### Ideal division of labour
- Write XCUITest for well-defined, high-value paths (authentication, checkout, critical happy paths)
- Use agent-driven blitz-iphone testing for exploratory sessions, new features before tests exist, and anything requiring visual confirmation
- After an agent-driven session surfaces issues or validates a flow, that's a good signal to codify it as an XCUITest

---

## Mixing interaction styles

When a UI supports both swipes and button taps (e.g. a card-based keep/remove flow), **use both** — it exercises more code paths and better simulates real users:

- Swipe right to keep, swipe left to remove, tap the Keep button, tap the Remove button — alternate between them
- Don't tap on the card image itself unless you intend to open the full-screen viewer
