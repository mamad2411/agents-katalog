---
name: computer-control
description: Control this Windows or Mac computer from the shell, with no app or server to install — open apps, websites, folders and Settings pages; volume, mute, microphone, media keys; brightness, dark mode, screenshots; read and click buttons on screen by their names, type text in any language (Khmer, Korean, ...), press shortcuts, mouse clicks, scroll and drag; Wi-Fi, Bluetooth, camera and microphone access; battery, power mode, lock, sleep, sleep and wake up hours later, shut down, restart; system info, heavy programs, notifications. Use when the person asks to do something on their computer ("turn the volume down", "open Bluetooth settings", "turn off the camera", "sleep and wake up in 5 hours", "click Save", "type this into Notepad", "what is using my memory"), or when a task needs to look at or use a desktop app. One command per action, JSON back.
---

# Computer control

Two scripts do everything; they need nothing but what the computer already has:

- **Windows 10/11:** `scripts/computer.ps1` (Windows PowerShell 5.1, built in)
- **macOS:** `scripts/computer.sh` (bash, osascript, pmset, networksetup, screencapture)

Each call does one action and prints one line of JSON: `{"ok":true,"action":...,"result":...}` or
`{"ok":false,"error":"..."}`. Read the error: it says what to do next.

```powershell
# Windows. $cc = this skill's folder, e.g. "$env:USERPROFILE\.claude\skills\computer-control"
powershell -NoProfile -ExecutionPolicy Bypass -File "$cc\scripts\computer.ps1" volume_set level=30
powershell -NoProfile -ExecutionPolicy Bypass -File "$cc\scripts\computer.ps1" click_item "name=Bluetooth & devices" window=Settings
```

```bash
# macOS
bash "$CC/scripts/computer.sh" volume_set level=30
bash "$CC/scripts/computer.sh" type_text "text=សួស្តី" window=Notes
```

Values are `name=value`. Quote the whole pair when the value has spaces: `"text=hello world"`.
`help` lists every action. The first Windows call takes about 3 s (it compiles small helpers into
`%LOCALAPPDATA%\computer-control`); later calls take about 0.6 s.

## Safety rules (follow every time)

1. **Ask before anything hard to undo.** `shutdown`, `restart`, `sign_out`, `hibernate`, `quit_app`,
   `stop_program` and `empty_trash` refuse to run without `confirm=yes`. Add it only after the person
   said yes to that exact action in this conversation. Never add it on your own.
2. **Name the window before typing or pressing keys.** Always pass `window=` to `type_text` and
   `press_keys`. The script brings that window to the front, checks it really is in front, and refuses
   otherwise. Without `window=`, keys go to whatever is in front, which may be the person's terminal or
   an open file.
3. **Look before you type into an existing window.** Opening an app can reopen old documents and tabs
   (Windows Notepad restores its tabs, sometimes with everything selected). Typing then replaces the
   person's text. Prefer a new, empty document (`press_keys keys=ctrl+n window=Notepad` first, then
   check with `screen_items` or `screenshot`), and never type into a file you did not create.
4. **Undo your own mistakes at once, and say so.** If text landed in the wrong place, press `ctrl+z`
   in that window (pass `window=`; on a Mac `cmd+z`), check with a screenshot, and tell the person what
   happened.
5. **Screenshots can show secrets** (open `.env` files, passwords, messages). Look only at what the
   task needs, never repeat keys or private text you see, and delete the screenshot file when done.
6. **Sleep, lock, shutdown and sign-out end your session too.** Say what will happen first; the script
   answers before it acts, so you can tell the person.

## How to do common requests

| Person says | Run |
|---|---|
| "turn it down", "볼륨 줄여", "បន្ថយសំឡេង" | `volume_down` (or `volume_set level=30`) |
| "mute" / "unmute" | `mute` / `unmute` |
| "mute my mic" | `mic_mute` |
| "open Bluetooth settings" | `open_settings page=bluetooth` (`help` lists pages) |
| "open YouTube", "search the weather" | `open_url url=youtube.com`, `web_search "query=weather"` |
| "open Downloads" | `open_folder path=downloads` |
| "open Chrome", "switch to Teams" | `open_app name=chrome`, `focus_window name=teams` |
| "turn off the camera" | `camera on=false` (Windows blocks apps from the webcam; Mac opens the privacy page) |
| "Wi-Fi off", "Bluetooth on" | `wifi on=false`, `bluetooth on=true` |
| "dark mode", "dim the screen" | `dark_mode on=true`, `brightness level=30` |
| "battery saver", "how much battery" | `power_mode mode=efficiency`, `battery` |
| "sleep and wake up in 5 hours" | `sleep_and_wake hours=5` (Windows: wake timer; Mac: asks for the admin password) |
| "lock the computer" | `lock` |
| "shut down" | ask, then `shutdown confirm=yes` (Windows waits 1 minute; `cancel_shutdown` stops it) |
| "what's eating my memory" | `top_processes`, `system_info` |
| "click Save", "press the Next button" | `click_item name=Save window=<app>` |
| "type this" | `type_text "text=..." window=<app>` |

## Using an app you cannot script (like computer use, but faster)

1. `screen_items window=<title>` lists the buttons, links, tabs, menu items and fields in that window
   with their names and centre positions. This is text, so it is much faster and cheaper than a
   screenshot. Windows reads it through UI Automation; macOS through System Events (Accessibility).
2. `click_item name=<words on it> window=<title>` presses it by name (invoke, select, toggle or expand,
   falling back to a real click). Prefer this to clicking coordinates.
3. Only when an item has no name (a canvas, an image, a game) take a `screenshot`, find the spot, and
   `click x=... y=...`. Screen position = picture position / `scale` + `left`/`top` from the result.
4. After each step check the result (`screen_items` again, or `list_windows`) before the next one.
   Apps need a moment to open: wait about 2 s after `open_app` or `open_settings`.

## Windows and macOS differences

| Action | Windows | macOS |
|---|---|---|
| camera / microphone_access | blocks or allows apps (privacy setting) | opens the privacy page; no switch exists |
| bluetooth | switches the radio | needs `brew install blueutil`, otherwise opens Settings |
| brightness | built-in laptop screen only | steps with the brightness keys |
| type_text | types any language directly | pastes through the clipboard (replaces the clipboard) |
| power_mode / sleep_and_wake / schedule_wake | no password | macOS asks for the admin password in its own dialog |
| hibernate, cancel_shutdown | yes | no |
| screen_items / click_item | UI Automation, any window | needs Accessibility permission for the terminal |
| screenshot | no permission needed | needs Screen Recording permission for the terminal |

On a Mac the first click, key or screenshot makes macOS ask to allow the terminal (or the AI app) under
System Settings → Privacy & Security → Accessibility and Screen Recording. Tell the person to allow it,
then run the action again.

## Limits

- Windows that run as administrator ignore clicks and keys from a normal process; the error says so.
- Store apps (Settings and others) appear twice in the window list with the same title; the script picks
  the frame that holds the buttons.
- Wake timers: whether the computer actually wakes depends on the hardware; most laptops do when plugged in.
- The macOS script was written against Apple's documented tools but has not been run on a Mac yet; when an
  action fails there, the JSON error carries macOS's own message.
