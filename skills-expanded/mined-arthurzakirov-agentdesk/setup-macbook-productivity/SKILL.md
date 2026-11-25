---
name: setup-macbook-productivity
description: "Configure repeatable macOS productivity settings on a user's MacBook, including voice typing / Dictation and Raycast-friendly Google Drive launching. Use when Codex is asked to set up, repair, or document MacBook productivity features such as Dictation, shortcuts, microphone input, Google Drive for Desktop, Raycast launch behavior, or similar local macOS workflow preferences."
---

# Setup MacBook Productivity

## Overview

Use this skill to configure local macOS productivity preferences with a bias toward repeatable setup, verification, and opening the relevant System Settings pane when macOS requires a user confirmation.

Supported workflows:

- Voice typing / Dictation with a Control-Control shortcut.
- A Raycast-friendly Google Drive launcher for Macs where Google Drive runs correctly but Raycast activation does not reopen its UI.

## Voice Typing Workflow

1. Confirm the host is macOS:

```bash
sw_vers
```

2. Run the bundled setup script:

```bash
python3 "$CODEX_HOME/skills/setup-macbook-productivity/scripts/setup_voice_typing.py"
```

When `CODEX_HOME` is unset, use:

```bash
python3 "$HOME/.codex/skills/setup-macbook-productivity/scripts/setup_voice_typing.py"
```

3. Tell the user that macOS may still show a one-time Dictation privacy or download prompt. They should click **Enable** if asked. For Apple audio sharing, recommend **Not Now** unless the user explicitly wants to share recordings.

4. Ask the user to test in any text field by pressing **Control** twice. They can stop Dictation with **Esc** or by pressing the same shortcut again.

### What The Dictation Script Does

- Enables the known Dictation preference flags.
- Sets the Dictation symbolic hotkey (`AppleSymbolicHotKeys` id `164`) to the working Control-Control modifier shortcut.
- Restarts preference services so macOS notices the change.
- Opens **System Settings > Keyboard** so the user can approve any required prompt and inspect Dictation settings.
- Prints the resulting Dictation and shortcut state for verification.

### Dictation Verification

```bash
defaults read com.apple.HIToolbox AppleDictationAutoEnable 2>/dev/null
defaults read com.apple.assistant.support "Dictation Enabled" 2>/dev/null
defaults read com.apple.symbolichotkeys AppleSymbolicHotKeys | sed -n '/164 =/,/};/p'
```

Expected signal:

- The first two commands return `1`.
- Hotkey `164` has `enabled = 1`, `type = modifier`, and parameters matching Control-Control.

If Dictation still does not start, open **System Settings > Keyboard > Dictation**, verify Dictation is on, set **Shortcut** to **Press Control Key Twice**, and choose the intended microphone source.

## Google Drive + Raycast Workflow

Use this workflow when all of the following are true:

- Google Drive for Desktop is installed and its files are mounted or otherwise accessible.
- Opening **Google Drive.app** directly in Finder successfully reopens the Drive UI.
- Launching **Google Drive** from Raycast appears to do nothing because Drive is already running as a background/menu-bar app.
- The user wants a normal Raycast / `⌘ Space` workflow rather than terminal commands.

Run:

```bash
python3 "$CODEX_HOME/skills/setup-macbook-productivity/scripts/setup_google_drive_raycast_launcher.py"
```

When `CODEX_HOME` is unset, use the equivalent installed skill path for the active harness.

### What The Google Drive Launcher Script Does

The script creates:

`~/Applications/Google Drive Launcher.app`

The launcher:

- Has its own bundle identifier so macOS and Raycast can index it as a separate app.
- Uses the Google Drive icon when available.
- Calls macOS LaunchServices to reopen `/Applications/Google Drive.app`.
- Avoids modifying Raycast's proprietary internal databases.
- Keeps the user's everyday interaction fully graphical: search for **Google Drive Launcher** in Raycast and press Enter.

The script is idempotent: rerunning it recreates the same launcher bundle in place.

### Google Drive Verification

After setup, verify that macOS can resolve the launcher:

```bash
open -Ra "Google Drive Launcher"
```

Then launch it once:

```bash
open "$HOME/Applications/Google Drive Launcher.app"
```

For a stronger behavioral check, inspect the recent Google Drive log for a reopen event:

```bash
tail -80 "$HOME/Library/Application Support/Google/DriveFS/Logs/drive_fs.txt" \
  | grep 'applicationShouldHandleReopen'
```

A successful run should produce a recent `applicationShouldHandleReopen` / `Got double launch` entry and reopen the same Drive UI that Finder opens.

If Raycast does not immediately show **Google Drive Launcher**, restart Raycast after the launcher has been indexed by macOS.

### Diagnosis Notes

Do not assume that a missing Google Drive menu-bar icon means Drive itself is broken. First distinguish:

1. Drive process and mounted files work.
2. Finder reopening the app works.
3. Raycast activation alone fails.

When those three conditions hold, prefer the launcher workaround above over reinstalling Drive or patching Raycast databases.

On macOS versions that protect Control Center state behind TCC, do not bypass privacy controls to inspect or mutate protected menu-bar registries. Treat missing Screen Recording or Accessibility permission as a boundary, not as evidence that Drive is corrupt.

## Boundaries

Do not try to bypass macOS privacy prompts. Open Settings and let the user approve prompts that require a human choice.

Do not enable full **Voice Control** unless the user asks for Mac control by voice. Voice Control replaces standard Dictation behavior while it is on.

Do not edit Raycast's proprietary databases directly when a supported indexed-app or Script Command mechanism can achieve the same outcome.
