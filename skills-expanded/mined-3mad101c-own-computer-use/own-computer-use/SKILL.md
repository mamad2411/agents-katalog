---
name: own-computer-use
description: >-
  Drive the user's Windows desktop GUI through the own-computer-use MCP server
  (computer_screenshot / computer_click / computer_type / computer_key /
  computer_scroll / computer_drag / computer_zoom). Use when a task needs to see
  or control a native app window, system dialog, or any GUI element that shell,
  filesystem, or browser tools cannot reach. Always prefer programmatic paths
  (Bash, file tools) over GUI control when they can complete the task.
---

# Own Computer Use

You control the user's Windows 11 desktop through the `own-computer-use` MCP
server. Follow this exact loop discipline — it is what makes GUI control reliable.

## Coordinate system rule (critical)

1. Call `computer_screenshot` first. The image it returns defines the coordinate
   space: (0,0) = top-left of the returned screenshot.
2. All x/y you pass to click/scroll/drag/zoom MUST be pixel coordinates **in the
   most recent screenshot**, never in real screen resolution. The server handles
   conversion internally (it downscales to 1568px max edge).
3. After every action that can change the screen (click, key, type, scroll,
   drag), take a fresh `computer_screenshot` before deciding the next step.
   Never chain more than two actions blind.

## Loop discipline

1. **Look → act → look.** Screenshot, pick the exact target pixel, act, screenshot
   again to verify the effect.
2. **Prefer keyboard over mouse** when possible: `computer_key` ("ctrl+s",
   "alt+Tab") is more reliable than clicking menu paths.
3. **Type**: `computer_type` pastes via clipboard — Arabic and Unicode are safe.
   Click the target field first, verify the caret is in it, then type.
4. **Small text**: use `computer_zoom` on the region, but keep acting on
   full-screenshot coordinates (zoom is for reading only, coordinates never
   shift).
5. **Scroll**: give x/y of the point to scroll at, direction up/down/left/right,
   amount in wheel notches.

## Safety

- Actions run on the real desktop. Confirm with the user before: deleting files,
  closing windows with unsaved work, sending messages/emails, purchases, or any
  irreversible step.
- Failsafe: jamming the mouse into a screen corner aborts pyautogui (host-side).
- If a screenshot shows a login, payment, or consent dialog you did not expect,
  stop and ask the user.

## When NOT to use

- File/command/HTTP tasks → use Bash and file tools instead.
- Browser-only tasks → prefer browser tools; use computer use only for OS
  dialogs outside the browser (file pickers, native menus, system settings).
