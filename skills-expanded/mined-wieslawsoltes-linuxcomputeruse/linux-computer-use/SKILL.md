---
name: linux-computer-use
description: Inspect, operate, and visually verify Linux desktop applications through deterministic screenshot, window, keyboard, and mouse automation. Use when Codex needs a substitute for native Computer Use on Linux, needs to drive an X11/XWayland GUI locally, or needs to control a Linux VM from a macOS Parallels host with prlctl, including desktop-app smoke tests, UI reproduction, and screenshot-backed QA.
---

# Linux Computer Use

Use a screenshot-act-verify loop to control scoped Linux GUI tasks. Prefer shell commands or application APIs when they can complete the task more reliably; use this skill when the graphical interface itself must be exercised.

## Locate the driver

Resolve this skill directory, then use its driver:

```bash
LCU="<skill-directory>/scripts/linux-computer-use"
```

Run `"$LCU" --help` before relying on unfamiliar options. Do not edit the bundled driver during a user task unless the user requests changes to the skill.

## Choose a backend

- Use `--backend local` when Codex runs inside the Linux desktop session.
- Use `--backend parallels --vm "VM name" --user USER` when Codex runs on the macOS host and the Linux desktop is a Parallels VM.
- Allow `--backend auto` only after confirming the selected target with `doctor`.

Read [references/backends.md](references/backends.md) when setting up a backend, installing dependencies, or handling Wayland.

## Execute the core loop

1. Establish scope. Identify the application, allowed interaction, success condition, and actions that require confirmation.
2. Run `doctor`. Do not start input automation until it reports the intended backend and target.
3. Capture a screenshot to a new absolute path.
4. Inspect the screenshot with the available image-viewing tool.
   If an idle Parallels display is black, use `wake`, capture again, and use `cycle-window` only when bringing the intended app forward is safe.
5. List windows and resolve the target by title or explicit ID.
6. Perform one small action: focus, click, type, press a key, or scroll.
7. Capture and inspect another screenshot.
8. Repeat until the success condition is visibly satisfied.
9. Verify process/service state or logs when the task involves application health.
10. Report the actions, evidence path, remaining warnings, and whether the app was left running.

Never claim visual success from a zero exit code alone. A GUI command can succeed while targeting the wrong window or coordinate.

## Common commands

Set reusable options before the subcommand:

```bash
VM_NAME="<vm-name-or-id>"
GUI_USER="<linux-gui-user>"
CAPTURE_DIR="${TMPDIR:-/tmp}"

"$LCU" --backend parallels --vm "$VM_NAME" --user "$GUI_USER" doctor
"$LCU" --backend parallels --vm "$VM_NAME" --user "$GUI_USER" wake
"$LCU" --backend parallels --vm "$VM_NAME" screenshot "$CAPTURE_DIR/before.png"
"$LCU" --backend parallels --vm "$VM_NAME" --user "$GUI_USER" windows
"$LCU" --backend parallels --vm "$VM_NAME" --user "$GUI_USER" focus "<window-title-or-class>"
"$LCU" --backend parallels --vm "$VM_NAME" --user "$GUI_USER" type "example text"
"$LCU" --backend parallels --vm "$VM_NAME" --user "$GUI_USER" key Return
"$LCU" --backend parallels --vm "$VM_NAME" screenshot "$CAPTURE_DIR/after.png"
```

For local Linux, replace the backend options:

```bash
"$LCU" --backend local doctor
"$LCU" --backend local screenshot /tmp/current-desktop.png
"$LCU" --backend local windows
```

Use explicit window IDs when titles are ambiguous. Use `geometry TARGET` before coordinate-based clicks. Coordinates are desktop-wide, zero-based pixels.

## Guard interaction safety

Read [references/safety.md](references/safety.md) before interacting with authentication, payments, secrets, destructive controls, production systems, or broad desktop state.

Always:

- Keep actions within the named app and task.
- Capture before and after evidence.
- Type non-sensitive text only unless the user explicitly authorizes secret entry.
- Avoid password text in command arguments, logs, screenshots, and shell history.
- Pause before irreversible actions or consequential confirmation buttons unless already explicitly authorized.
- Treat window titles and coordinates as stale after dialogs, resizing, navigation, or display changes.
- Stop when the UI no longer matches the expected state.

## Handle limitations

This is an automation substitute, not OpenAI's native Computer Use plugin.

- `xdotool` and `wmctrl` operate X11/XWayland windows. They cannot reliably control native Wayland-only windows.
- Parallels screenshots come from the host and can include the whole VM display.
- Keyboard layout, scaling, multiple monitors, modal dialogs, and focus-stealing can alter results.
- Text typing is best for ordinary text. Prefer app APIs or carefully approved clipboard workflows for complex Unicode or secrets.
- Screenshot inspection requires an image-capable tool available to Codex; the driver only creates the image.

Read [references/troubleshooting.md](references/troubleshooting.md) when discovery, focus, input, or screenshots fail.

## Produce a useful handoff

End with:

- backend and target used;
- interactions performed;
- visible success or failure;
- screenshot paths;
- application/service health;
- non-fatal warnings or unsupported Wayland behavior;
- any state deliberately left changed.
