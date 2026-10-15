---
name: yabai-skhd-doctor
description: Health-check the macOS yabai (tiling window manager) and skhd (hotkey daemon) services — verify they are installed, their launchd services are running, they hold Accessibility permission, configs exist, and yabai's scripting-addition prereqs (SIP, sudoers) are met. When anything is wrong it prints a concrete fix path. Use when yabai or skhd stopped working, hotkeys/window management aren't responding, after a macOS update, or when the user asks to check/verify/diagnose/fix their yabai or skhd setup.
---

# yabai + skhd doctor

Read-only diagnostic for a macOS yabai + skhd setup. It changes nothing — it
inspects the system and proposes a fix path the user (or you) can act on.

## Run it

```bash
bash scripts/diagnose.sh
```

macOS only (uses `launchctl`, `csrutil`, `sw_vers`). Run as the logged-in user,
**not** sudo — the Accessibility checks must see that user's session.

## What it checks

Per service (yabai, skhd):
- Binary installed + version.
- launchd service registered and running (with last exit code).
- Config present (`~/.config/<svc>/<svc>rc`, falling back to `~/.<svc>rc`).
- Accessibility permission: yabai is probed with `yabai -m query` (a response
  proves running + AX); skhd is inferred from `/tmp/skhd_$USER.err.log`.

yabai scripting addition (optional, advanced):
- SIP status (`csrutil status`) — SA needs it partially disabled.
- Passwordless `--load-sa` sudoers entry.

## Reading the output

`✓` healthy · `✗` broken, has a fix · `?` unknown/advisory. Findings print per
section; a numbered **Proposed fix path** collects every remediation at the end.

## Acting on the fix path

Present the fix path to the user. Most fixes are safe to run for them
(`brew install ...`, `yabai --start-service`, `--restart-service`). Two cannot
be done from the CLI and must be handed to the user:

- **Accessibility permission** — only grantable in System Settings ▸ Privacy &
  Security ▸ Accessibility (toggle yabai / skhd on). After granting, restart the
  service; macOS does not apply a new permission to a running process.
- **SIP / scripting addition** — disabling SIP needs a Recovery-mode reboot;
  only pursue if the user actually wants SA features. Link the yabai wiki, don't
  attempt it.

Never `sudo` the script or auto-disable SIP. Confirm with the user before any
change beyond starting/restarting a service.
