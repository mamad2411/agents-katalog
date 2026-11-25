---
name: appshots-automation-pipeline
description: >
  End-to-end screenshot automation skill for iOS apps using asc CLI, simctl, and AXe.
  AI agents use this to boot simulators, navigate apps, capture raw screenshots
  across multiple locales, and pipe them into appshots for final design.
---

# App Screenshot Automation Pipeline

This skill teaches an AI agent how to automate the full App Store screenshot capture workflow:

```
Boot Simulators → Set Locales → App Navigation & Capture (asc/AXe) → Design Hand-off
```

## Prerequisites

```bash
# 1. AXe — Simulator UI automation via Accessibility APIs
brew install cameroncooke/axe/axe

# 2. asc CLI — Apple's unofficial App Store Connect CLI (includes screenshot tools)
brew install rudrankriyam/asc/asc

# 3. xcrun simctl — Built-in with Xcode (no install needed)
```

## Capture Phase: Accelerator using `asc` CLI

The fastest and most reliable way to capture screenshots is using the official `asc screenshots` commands combined with a JSON capture plan.

### 1. Create the Capture Plan

Create `.asc/screenshots.json` to define the steps AXe should take in the app.

```json
{
  "version": 1,
  "app": {
    "bundle_id": "com.example.app",
    "udid": "booted",
    "output_dir": "./screenshots/raw"
  },
  "steps": [
    { "action": "launch" },
    { "action": "wait", "duration_ms": 2000 },
    { "action": "screenshot", "name": "01_home" },
    { "action": "tap", "id": "settings_tab" },
    { "action": "wait", "duration_ms": 1000 },
    { "action": "screenshot", "name": "02_settings" }
  ]
}
```

*Note: Use `axe describe-ui` to find the correct `id` and `label` values for the steps.*

### 2. Parallel Multi-Locale Capture (Recommended Pattern)

Instead of sequentially rebooting one simulator, map each target locale to a **dedicated simulator UDID** created via `xcrun simctl create`. This allows parallel capture.

```bash
#!/bin/bash
# parallel-capture.sh — Fast multi-locale capture

declare -A LOCALE_UDID=(
  ["en-US"]="UDID_EN_US"
  ["ja-JP"]="UDID_JA_JP"
  ["ko-KR"]="UDID_KO_KR"
)

# 1. Boot all simulators and set their locales
for LOCALE in "${!LOCALE_UDID[@]}"; do
  (
    UDID="${LOCALE_UDID[$LOCALE]}"
    LANG="${LOCALE%%-*}"            # e.g., 'ja'
    APPLE_LOCALE="${LOCALE/-/_}"    # e.g., 'ja_JP'

    xcrun simctl boot "$UDID" || true
    xcrun simctl spawn "$UDID" defaults write NSGlobalDomain AppleLanguages -array "$LANG"
    xcrun simctl spawn "$UDID" defaults write NSGlobalDomain AppleLocale -string "$APPLE_LOCALE"
    
    # Needs a reboot to apply locale changes cleanly
    xcrun simctl shutdown "$UDID"
    xcrun simctl boot "$UDID"

    # Install the built app
    xcrun simctl install "$UDID" build/ios/iphonesimulator/Runner.app
  ) &
done
wait

# 2. Run captures in parallel using the asc plan
for LOCALE in "${!LOCALE_UDID[@]}"; do
  (
    UDID="${LOCALE_UDID[$LOCALE]}"
    asc screenshots run \
      --plan ".asc/screenshots.json" \
      --udid "$UDID" \
      --output-dir "./screenshots/raw/$LOCALE" \
      --output json
      
    echo "Captured $LOCALE on $UDID"
  ) &
done
wait
echo "All raw captures complete."
```

## End-to-End Workflow Link

Once the raw screenshots are captured in Phase 1 above, immediately transition to the `appshots-design-workflow` skill to load these images into the App Screenshots desktop app for framing, backgrounds, text overlays, and PDF/PNG export.

---

## Agent Guidelines

### Thinking Process for AI Agents

When given a scenario like "capture screenshots of my fitness app", follow this process:

1. **Discover the app** — Find the bundle ID, build the app if needed
2. **Boot a simulator** — Pick the right device type for the target display
3. **Inspect the UI** — Run `axe describe-ui` to discover accessibility identifiers
4. **Plan navigation** — Map out the tap/swipe sequence to reach each screen
5. **Capture systematically** — Build `.asc/screenshots.json`
6. **Repeat for locales** — Use the parallel loop script with mapped UDIDs
7. **Design** — Switch to `appshots` CLI skills to set up frames, text, backgrounds, presets
8. **Translate** — Switch to `appshots-translation` skill for AI text translation
9. **Export** — Export final screenshots for all locales

### Device Selection Strategy (App Store Connect)

When choosing which simulators to boot and generate screenshots for, follow this device tiering:
- **Required Default (6.9"):** `iPhone 16 Pro Max` or `iPhone 17 Pro Max`. This covers the primary 6.9" App Store Connect requirement and should ALWAYS be captured.
- **Optional Sizes:**
  - **6.5" (Optional):** `iPhone 15 Pro Max` or `iPhone 11 Pro Max`.
  - **5.5" (Optional):** `iPhone 8 Plus` (only if legacy compatibility is explicitly requested).

### Key Tips

- **Always run `axe describe-ui` first** — Shows the accessibility tree so you know what elements to tap
- **Use `--id` over coordinates** — Accessibility identifiers are stable across locales and screen sizes
- **Use `wait` heavily in plans** — Apps need time to animate and settle
- **Status Bar Overrides are Optional** — Setting the simulator time to 9:41 and overriding network/battery states (`xcrun simctl status_bar`) is optional. By default, simulators usually look clean enough for most use cases, and `appshots` designs often use backgrounds that can mask standard status bars, or you can supply device frames without them.
