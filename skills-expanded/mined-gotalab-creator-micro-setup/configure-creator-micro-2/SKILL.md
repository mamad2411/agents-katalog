---
name: configure-creator-micro-2
description: Set up, inspect, or troubleshoot a Codex Micro or Creator Micro 2 on macOS with Work Louder Input. Use for creating another app profile or layer, checking an existing layer, preserving the built-in Codex layer, installing the Claude Desktop helper app, setting up Aqua Voice buttons, diagnosing duplicate keys or permissions, and recording a portable configuration without repeating known setup mistakes.
---

# Configure Creator Micro 2

Set up one small part at a time and test it on the real device. The goal is a repeatable app layer whose physical positions, Input keys, final actions, and test results are recorded. Call a key saved only after Input shows the change. Call the final action working only after the device performs it in the target app.

## Start safely

1. Identify the exact hardware, macOS version, Input version, target app, and requested layer.
2. Read the current layout before changing it.
3. Preserve Layer 1 when it contains the built-in Codex App controls.
4. Make a change only on the requested layer.
5. Test the emitted key, then test the final action in the target app.

Never edit `input_storage.json` or `keymap.json` as a way to configure the device. A file change does not prove Input sent the setting to the hardware.

## Choose the path

- For this repository's Claude Desktop Layer 2, read [references/claude-desktop.md](references/claude-desktop.md), then follow the root `docs/first-time-setup.md` when it is available.
- For another app, prefer its standard keyboard shortcuts. Use macOS Accessibility only when no stable shortcut exists.
- Avoid screen coordinates because app windows and layouts move.
- Keep the experimental direct device connection (raw HID) and status lighting off unless the user explicitly accepts the risk and duplicate typing has been ruled out.

For a new app layer, fill in [references/profile-template.md](references/profile-template.md) while working. Decide these items before editing Input:

1. Whether the user wants another Work Louder profile or another layer inside the current profile.
2. Which physical control performs each action.
3. Which stable app shortcut can perform the action.
4. Which harmless Input key the helper will receive when the app has no suitable shortcut.
5. What must be observed to call the action working.

Prefer unused keys such as F13 and above for helper-controlled actions. Check for conflicts with the target app and existing layers before assigning them.

## Configure Input

Use the Input app's visible controls. Add the target layer with `+` before trying to select it; a layer cannot be selected before it exists. Assign one physical control at a time and record its position, Input key, and result before moving on.

When controlling Input through macOS Accessibility, fetch a fresh screen state immediately before every click. Element numbers change quickly. Never reuse a number from an earlier screen state. If a heading has no clickable frame, try its visible text or containing tile, then confirm that Input actually saved the result.

For radial joystick slots:

1. Count the visible slots; diagonal-looking sectors are separate choices, not combinations of up and right.
2. Select one slot. In Input 0.18.0, the small `+` inside an empty sector adds or selects that direction; the outside `blank` label is not the same target.
3. Search for the exact Basic key.
4. Choose **Number Pad** 4, 6, 8, or 2 when the map calls for keypad directions. Ordinary digit keys are different.
5. Click the result tile. A visible search result alone does not save anything.
6. Reopen the ring or inspect Input's saved state to confirm the slot changed.
7. Move the physical joystick and check the emitted key and final app action separately.

If Input's editor cannot be controlled reliably, first re-read the fresh screen state and check whether the wrong part of the sector was targeted. Ask the user for the smallest physical click only after the visible controls cannot be reached. Do not claim the slot was saved from a displayed search result alone.

## Configure voice input

When Aqua Voice listens for Globe/Fn and Input can only send Caps Lock, change Caps Lock to Globe for the Creator Micro keyboard in macOS Modifier Keys. Do not change the Mac's built-in keyboard. Test hold and double-press behavior before continuing.

## Install and check the helper

From the repository root, run:

```sh
./scripts/install.sh
./scripts/diagnose.sh
./scripts/check.sh
```

Ask for Accessibility and Input Monitoring only for Codex Micro Bridge. After changing permissions, restart the helper.

After installing or replacing the Bridge, do not begin with physical session-key tests. Run the installed executable from Terminal first and require its startup line to report both `Accessibility: true` and `Input Monitoring: true`. If either is false, stop and repair the macOS permission before pressing F14 or F15; otherwise macOS may open its display or brightness controls. A successful code test does not prove these permissions or the startup service.

Also require `./scripts/diagnose.sh` to report both `update-stable local signature` and `Codex Micro Bridge is running`. An old per-build signature can leave the macOS permission switch visibly on while the background Bridge is rejected. When the system log says `Failed to match existing code requirement`, install the current build, reset only `ListenEvent` and `Accessibility` for `com.gotalab.codex-micro-bridge`, add the current app again in both permission lists, and restart. Do not repeatedly toggle unrelated apps or reset all privacy permissions.

Verify the real path:

- One session press while Claude Desktop is in front.
- Two quick presses while another app is in front.
- Voice hold and voice double-press.
- Send.
- Dial after focusing the conversation.
- Each configured joystick direction.

Report each item as passed, failed, not checked, or blocked. Separate Claude Desktop's Code view from terminal Claude Code.

## Finish the record

Update the app's saved map from [references/profile-template.md](references/profile-template.md). Include the real hardware position, including Dial and Joystick in the top row, rather than listing only the keyboard buttons. Keep these states separate:

- Assigned in Input
- Emitted by the physical device
- Performed the intended action in the target app

Note any focus requirement, delay, double-press rule, Accessibility label, macOS remapping, or version-specific behavior. This record is what lets another agent add or repair the layer without repeating the same guesses.

When a Layer 2 action behaves differently only while ChatGPT/Codex is in front, check for the app's direct Codex Micro connection before changing the Input keymap. That native device path can react to a second press even when the Bridge consumes the normal keyboard event. For this repository's Bridge, `com.openai.codex` is intentionally a one-press handoff to Claude; ordinary background apps keep the two-press guard.

## Stop conditions

Stop and ask before changing Layer 1, enabling raw HID, replacing an unrelated installed app, resetting Input, or editing private Input data by hand. When hardware behavior cannot be observed, leave the item unconfirmed and name the exact physical test needed.
