---
name: android-cli-ui-automation-skill
description: Automate UI on a connected Android device or emulator via the Android CLI. Use when asked to launch an app, tap a button, enter text, navigate a URL, or drive any on-screen flow to a goal.
---

Drive the device in a tight **launch → observe → act → re-observe** loop until the goal is reached.
Prefer `android layout` for structured UI. Use screenshot mode whenever it is faster or more reliable.

If multiple devices are connected, get the serial with `adb devices -l`. Pass `--device=<serial>` to `android ...` and `-s <serial>` to `adb ...`.

## 1. Launch

- URL in a browser:
  `adb -s <serial> shell am start -a android.intent.action.VIEW -d '<url>'`
- Already-installed app:
  `adb -s <serial> shell monkey -p <pkg> -c android.intent.category.LAUNCHER 1`
- APK file:
  `android run --apks=<path> --device=<serial> [--activity=<name>]`

## 2. Observe with `android layout`

```bash
android layout --device=<serial> --pretty --output=/tmp/ui.json
```

Match targets by `text`, `content-desc`, or `resource-id`. Use the node's `center` as tap coordinates.

Re-observe after each action with the mode you chose. `android layout --device=<serial> --diff` is useful when you only need to see what changed.

## 3. Use screenshot mode when visual targeting is easier

Screenshot mode is often the better choice for:
- WebView or browser page content
- Icon-only custom views
- Canvas, map, or game surfaces
- Any screen where `layout` is noisy, incomplete, or slower to interpret than the image

```bash
android screen capture --output=/tmp/ui.png --annotate
android screen resolve --screenshot=/tmp/ui.png --string="input tap #N"
```

Labels are valid only for that screenshot. Capture again after every UI change.

## 4. Act with `adb shell input`

```bash
adb -s <serial> shell input tap <x> <y>
adb -s <serial> shell input text '<text-with-%s-for-spaces>'
adb -s <serial> shell input swipe <x1> <y1> <x2> <y2> <ms>
adb -s <serial> shell input keyevent <KEYCODE>
```

Example: `adb -s <serial> shell input text 'hello%sworld'`

## Rules

- Re-observe after every action. Coordinates and screenshot labels go stale immediately.
- Clear blockers first: permission dialogs, onboarding sheets, update prompts.
- Use the observation mode that is clearer: `layout` for structured UI, screenshot for visual UI.

## Notes

- Don't type URLs into the address bar. Open them with `am start -a VIEW -d '<url>'`.
- If the foreground app is unclear, check it with `adb -s <serial> shell dumpsys window | rg 'mCurrentFocus|mFocusedApp'`.
