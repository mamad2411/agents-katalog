---
name: adb
version: 1.0.0
description: Use ADB to interact with an Android device or emulator. Takes a screenshot, understands the screen, performs actions (tap, swipe, type, navigate), and loops until the mission is complete.
argument-hint: "<mission description>"
---

Use ADB commands to interact with an Android device or emulator to complete a user-defined mission. Operates in a **screenshot-act-verify loop** until the mission is accomplished.

**Usage:**
- `/adb <mission>` — Describe what you want done on the device (e.g., "open Settings and enable Dark Mode")

**Prerequisites:**
- `adb` must be in PATH
- A device or emulator must be connected

**Instructions:**

1. **Verify ADB connectivity:**
   - Run `adb devices` and confirm at least one device is listed (not "unauthorized")
   - If no device is found, inform the user and **STOP**
   - If multiple devices are found, use `AskUserQuestion` to ask which device to target, then pass `-s <serial>` to all subsequent `adb` commands

2. **Understand the mission:**
   - Parse `$ARGUMENTS` as the mission description
   - If `$ARGUMENTS` is empty, use `AskUserQuestion` to ask what the user wants to accomplish on the device
   - Break the mission into a mental checklist of expected steps (do not output this — it's for your own planning)

3. **Enter the screenshot-act-verify loop:**

   Repeat the following cycle until the mission is complete or you determine it cannot be completed:

   **a) Take a screenshot:**
   ```bash
   mkdir -p .tmp && adb exec-out screencap -p > .tmp/screen.png
   ```
   - Read the screenshot with the `Read` tool to understand the current screen state

   **b) Analyze the screen:**
   - Identify what app/screen is currently displayed
   - Determine what UI elements are visible (buttons, text fields, toggles, lists, etc.)
   - Assess progress toward the mission goal
   - If the screen is unclear or you need more detail about the UI element tree, run a UI dump:
     ```bash
     adb shell uiautomator dump /sdcard/ui.xml && adb pull /sdcard/ui.xml .tmp/ui.xml
     ```
     Then read `.tmp/ui.xml` to get element bounds, text, and resource IDs for precise tap coordinates.

   **c) Decide and execute the next action:**

   Use one or more of these ADB commands:

   | Action | Command |
   |--------|---------|
   | Tap at coordinates | `adb shell input tap <x> <y>` |
   | Swipe | `adb shell input swipe <x1> <y1> <x2> <y2> [duration_ms]` |
   | Type text | `adb shell input text "<text>"` |
   | Press Back | `adb shell input keyevent 4` |
   | Press Home | `adb shell input keyevent 3` |
   | Press Enter | `adb shell input keyevent 66` |
   | Press Recent Apps | `adb shell input keyevent 187` |
   | Launch an app | `adb shell am start -n <package>/<activity>` |
   | Open a URL | `adb shell am start -a android.intent.action.VIEW -d "<url>"` |
   | Long press | `adb shell input swipe <x> <y> <x> <y> 1000` |

   **Coordinate tips:**
   - When tapping a UI element, aim for its center based on the screenshot or the `bounds` attribute from the UI dump (e.g., bounds `[0,200][1080,350]` → tap at `540,275`)
   - For scrolling down, swipe from the lower third to the upper third of the screen (e.g., `adb shell input swipe 540 1500 540 500 300`)
   - For text input, tap the field first, wait briefly, then type

   **d) Wait and verify:**
   - After each action, wait briefly for the UI to settle (`sleep 1`)
   - Take another screenshot to verify the action had the expected effect
   - If the action did not work as expected (e.g., wrong element tapped, dialog appeared, screen didn't change), adjust and retry
   - **Do not retry the same failing action more than 2 times** — if it keeps failing, try an alternative approach (different coordinates, different navigation path, use the UI dump for precise bounds)

4. **Handle common situations:**

   - **Keyboard covering the screen:** After typing, press Back (`keyevent 4`) to dismiss the keyboard before taking a verification screenshot
   - **Dialogs/popups:** If an unexpected dialog appears, read it and dismiss it appropriately (tap "OK", "Allow", "Deny", etc. based on what makes sense for the mission)
   - **Loading screens:** If the screen shows a loading state, wait 2-3 seconds and take another screenshot
   - **App not installed:** If the target app isn't found, inform the user and **STOP**
   - **Permission prompts:** Grant permissions that are necessary for the mission (tap "Allow"), deny those that aren't relevant
   - **Screen locked:** If the device shows a lock screen, try swiping up (`adb shell input swipe 540 1800 540 800`) to unlock. If a PIN/password is needed, ask the user

5. **Check logcat when things go wrong:**
   - If an app crashes or behaves unexpectedly, check recent logs:
     ```bash
     adb logcat -d -t 50
     ```
   - Use the logs to understand what happened and inform the user if the issue is not recoverable

6. **Mission complete:**
   - Once the mission objective is achieved, take a final screenshot as confirmation
   - Present the final screenshot to the user with a brief summary:
     ```
     ## Mission Complete

     <description of what was accomplished>

     Final state: <what's currently on screen>
     Actions taken: <count> steps
     ```

7. **Cleanup:**
   - Remove temporary files:
     ```bash
     rm -f .tmp/screen.png .tmp/ui.xml
     ```

---

## Edge Cases

- If `adb` is not found in PATH, display setup instructions and **STOP**
- If the device becomes disconnected mid-mission, attempt `adb devices` to check — if disconnected, inform the user and **STOP**
- If the mission requires installing an app, ask the user for the APK path or package name before proceeding
- If you get stuck in a loop (same screen after 3 attempts), take a UI dump, reassess, and try a completely different approach. If still stuck, inform the user and ask for guidance
- If the screen resolution is unknown, read it from the first screenshot dimensions or run `adb shell wm size`
