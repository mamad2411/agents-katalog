---
name: agent-vm
description: Drive a real Windows 11 desktop in a local QEMU/KVM VM with the agent-vm CLI — restore checkpoints, run PowerShell, install and launch apps, read and click the UI through UI Automation @refs, drive WebView2 through DevTools, speak into the Windows microphone and record its speakers. Use when you need to build, install, test or debug anything on Windows from a Linux host, especially desktop apps, installers, dictation/voice features, or anything that needs a real Windows UI.
---

# agent-vm

`agent-vm` gives you a Windows 11 machine you control from the Linux host. `agent-vm <command>
--help` has flags and examples. `agent-vm doctor` tells you whether the host and VM are healthy.
Add `--json` when you parse output: errors then arrive as `{"error": {"message", "hint"}}` on
stdout. Exit codes: 1 agent-vm failed, 2 usage error; `exec`, `ui`, `web` and `install-app` pass
through the guest's exit code.

## The loop

1. **Start from a known state.** `agent-vm checkpoint restore clean` (or a later checkpoint such as
   `signed-in`). It starts the VM if needed and returns when the desktop is ready.
2. **Act** through the narrowest channel that can do the job (see the table).
3. **Observe** with `ui snapshot -i` (native UI) or `web snapshot -i` (web views), not screenshots.
4. **Verify** with a second channel before claiming success: `ui get text @eN`, a file or log read
   with `exec`, or `level` on a recorded WAV. Save a `screenshot` as evidence for humans.

## Which channel

| Need                                               | Use                                                                                                   | Notes                                                                                 |
| -------------------------------------------------- | ----------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------- |
| Install, files, registry, services, logs           | `exec '<PowerShell>'`                                                                                 | Elevated SSH session, **no desktop**. Fast (~20 ms)                                   |
| Anything that must appear on screen or see windows | `exec --desktop '<PowerShell>'`                                                                       | Runs in the signed-in user's session via agentd                                       |
| Run an installer                                   | `install-app <file>`                                                                                  | Silent: `/S` (.exe), `/qn` (.msi); `--args` to override                               |
| Start an app                                       | `launch <exe> [args]`                                                                                 | `--cdp` for WebView2/Electron DevTools, `-e K=V` for env                              |
| Read or operate native UI                          | `ui snapshot -i`, `ui click @e3`, `ui type @e5 "text"`, `ui get text @e4`, `ui wait --window "Title"` | agent-desktop over UI Automation. `agent-vm ui skills get desktop` has the full guide |
| Operate a web view                                 | `web snapshot -i`, `web click @e2`, `web eval "…"`                                                    | Needs the app started with `launch --cdp`                                             |
| Keys the app listens for globally (hotkeys)        | `key ctrl+shift+space`; hold-to-talk: `key --down ctrl+win`, `mic say …`, `key --up ctrl+win`         | Real keyboard input from the host                                                     |
| See the screen                                     | `screenshot out.png`                                                                                  | Works even when nothing in the guest responds                                         |
| Speak to the app                                   | `mic say "text" [--lang sv]`, `mic play file.wav`                                                     | Windows hears it on its default microphone                                            |
| Hear the app                                       | `speaker out.wav -s 5`, then `level out.wav`                                                          | `level` exits 3 when silent                                                           |

## Rules

- **Refs go stale.** Take a new `snapshot -i` after anything that changes the UI. Never reuse refs
  across a restore.
- **SSH sessions can't see the desktop.** A GUI started with plain `exec` is invisible and UI
  Automation returns nothing from there. Use `launch` or `exec --desktop`.
- **Paths:** use forward slashes for `push`/`pull` (`C:/Users/agent/Desktop/`). The user is `agent`.
- **Host typing (`type`) is US-layout ASCII only.** For other text use `ui type @ref "…"`, or
  `ui clipboard-set` followed by `key ctrl+v`.
- **`mic say` blocks while speaking.** To capture what the guest heard, start the recorder
  detached first:
  `exec --desktop --detach 'ffmpeg -y -f dshow -i audio="Microphone (High Definition Audio Device)" -t 8 C:/agent-vm/heard.wav'`.
- **Checkpoints are cheap.** Save one after slow setup (`checkpoint save app-installed`) and
  restore it instead of redoing the setup. Don't overwrite `clean`.
- **Apps with several web views** (Tauri and Electron apps often have hidden overlay windows):
  `web tab list`, then `web tab t2` to pick the main one before `web snapshot -i`.
- **Local dev servers:** `hosts <name…>` points names at the host (10.0.2.2), and `trust-ca <pem>`
  trusts a dev CA.
- When something is stuck, take a `screenshot` before anything else. A modal dialog (UAC,
  SmartScreen, "How do you want to open this?") is the usual cause, and `ui snapshot -i` usually
  shows it.

## Recording a video

`agent-vm record demo.mp4 --seconds 30` captures the screen (about 10 fps) with what the guest's microphone hears as the soundtrack (`--audio speaker` for what it plays, `--audio none` for silence). Run it in the background and drive the VM meanwhile; other commands keep working while it records. Stop early with SIGINT/SIGTERM.
