---
name: agent-browser-ios
description: "[INTERNAL TEMPLATE] iOS Simulator execution protocol. Called by agent-browser orchestrator."
---

# Agent Browser — iOS Simulator

> **Internal template.** Entry point: `agent-browser` skill.

**Recommended config:** `agent-browser -p ios` (short for `--provider ios`)

---

## NEVER

```
NEVER run commands before Simulator is booted — daemon can't connect; boot first with xcrun simctl
NEVER use `scroll` on iOS — use `swipe up` / `swipe down` instead
NEVER use `click` on native touch targets — prefer `tap @ref` for iOS elements
NEVER copy element refs across navigations — re-run `snapshot -i` after every screen change
NEVER assume WebView content is inspectable — must enable Web Inspector in Safari → Develop → [device]
```

---

## Prerequisites

iOS Simulator requires:
1. **macOS** (Apple Silicon or Intel)
2. **Xcode** with iOS Simulator — install from Mac App Store
3. **Appium** — `npm install -g appium && appium driver install xcuitest`
4. Simulator must be **running in Xcode** before starting agent-browser

```bash
# Verify prerequisites
xcodebuild -version         # Xcode installed?
appium --version            # Appium installed?
appium driver list --installed   # XCUITest driver present?
```

---

## Environment Check

```bash
printenv | grep AGENT_BROWSER   # already set? Omit the corresponding inline flag
```

---

## Workflow

```bash
# 1. Start Simulator in Xcode first (or via xcrun)
xcrun simctl boot "iPhone 15 Pro"
open -a Simulator

# 2. List available simulators
agent-browser -p ios device list

# 3. Open app in simulator
agent-browser -p ios --device "iPhone 15 Pro" open https://app.example.com

# 4. Explore interactive elements
agent-browser -p ios snapshot -i

# 5. iOS-native gestures
agent-browser -p ios tap @e1
agent-browser -p ios swipe up           # scroll up
agent-browser -p ios swipe down         # scroll down
agent-browser -p ios swipe left         # swipe carousel / delete row
agent-browser -p ios swipe right        # go back (swipe edge)

# 6. Standard commands work too
agent-browser -p ios screenshot --full ios-result.png
agent-browser -p ios find role button click --name "Submit"
agent-browser -p ios get text @e3
agent-browser -p ios wait --load networkidle
```

---

## Key Patterns

| Pattern | Command |
|:---|:---|
| List simulators | `agent-browser -p ios device list` |
| Target specific device | `-p ios --device "iPhone 15 Pro"` |
| iOS scroll | `swipe up` / `swipe down` (not `scroll`) |
| iOS tap | `tap @e1` (preferred over `click` for touch targets) |
| Navigate back | `swipe right` (edge swipe) |
| Dismiss bottom sheet | `swipe down` |
| Take evidence screenshot | `screenshot --full ios-result.png` |
| Inspect DOM (WebView) | `snapshot -i` (for web content in WKWebView) |

---

## Chrome Commands That Still Work on iOS

These standard commands work with `-p ios`:

- `open <url>` — navigate
- `snapshot` / `snapshot -i` — accessibility tree
- `find role button click --name "..."` — semantic locator
- `get text @e1` / `get value @e1`
- `screenshot [path]` / `screenshot --full`
- `wait @e1` / `wait --load networkidle`
- `is visible @e1` / `is enabled @e1`
- `errors` / `console` (for WebView content)

---

## Pitfalls

| Mistake | Fix |
|:---|:---|
| Simulator not started before running | Start Simulator in Xcode first, or `xcrun simctl boot "iPhone 15 Pro"` |
| Appium not installed | `npm install -g appium && appium driver install xcuitest` |
| Using `scroll` instead of `swipe` | iOS uses `swipe up`/`swipe down`, not `scroll` |
| Using `click` on touch-only elements | Prefer `tap @e1` for native touch targets |
| `device list` shows no devices | Simulator not booted — open Xcode → Simulators and boot one |
| XCUITest driver missing | `appium driver install xcuitest` |
| WebView content not inspectable | Enable "Web Inspector" in Safari → Develop → [device name] |

