---
name: phone-control
description: Use the user's Android phone through the android-agent-bridge MCP tools (phone_*) or the `phonectl` CLI — open apps, read the screen, tap, type, scroll, fill forms.
---

# Using the user's Android phone

You control a real phone through the `phone_*` tools (or the `npx android-agent-bridge <command>` CLI with the same commands).

## Loop

1. `phone_status` first. If no phone is connected, give the user the pairing instructions it returns and stop.
2. Look: `phone_elements` (cheap text) for most steps; `phone_screen` when you need pixels (images, icons without labels, games, verifying layout).
3. Act with one tool call. Every action returns the updated element list, so you rarely need to look again separately.
4. Repeat until done. Report what you did and what you saw.

## Targets

`phone_tap`, `phone_type`, `phone_swipe`, `phone_scroll` take a target:

- `"12"`: element number from the latest `phone_elements` or `phone_screen` (most reliable). Numbers change when the screen changes, so use the newest list.
- `"Sign in"`: visible text or label on screen. The app's own controls win over the Android system bar, and text that the app hides from accessibility is found by reading the screen (OCR) automatically.
- `"C7"`: grid cell from `phone_screen` with `mode: "grid"`. Use this for spots with no element: maps, games, images, canvases.
- `"540,1200"`: screen pixels, as listed after `@` in the element list.

## Tips

- Typing does not need the keyboard: `phone_type` with `target` puts the text straight into the field. Add `submit: true` to press Enter/Search.
- `phone_open_app` opens an app by name. Use `phone_key` `home`/`back` to navigate.
- `phone_scroll` `direction: "down"` brings what is below into view.
- `phone_wait_for` waits for text to appear after loading.
- Use the direct device tools instead of navigating Settings: `phone_volume`, `phone_brightness`, `phone_toggle` (flashlight, rotation, Do Not Disturb, ringer), `phone_settings` (jump to any settings page), `phone_open_link` (web pages and deep links), `phone_device_info` (battery, app in front, permissions), `phone_notifications`. `phone_dial` only fills in the number; it never calls.
- If you can see something in a screenshot that `phone_elements` doesn't list (custom tab bars, payment rows), call `phone_ocr`: it returns the text drawn on screen with positions. `phone_elements` with `all: true` also lists elements hidden under sheets.
- Banking, streaming and some other apps block screenshots; the element list usually still works.
- Ask the user before sending messages, posting, paying, deleting or anything else that can't be undone. Never type passwords or card numbers; ask the user to do that part on the phone.
- On Android 5–6 some actions need the phone plugged in over USB; the error message says so. Tell the user.
