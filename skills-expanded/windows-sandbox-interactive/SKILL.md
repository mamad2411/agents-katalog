---
name: windows-sandbox-interactive
description: Explore and drive a Windows app step by step in a live Windows Sandbox with UI Automation, screenshots, commands and system snapshots. Use for multi-step UI testing, reproducing a bug by hand, trying prerequisites one at a time, or finding out what an action changed on the system.
---

# Drive a live Windows Sandbox

If shell access is available, use the `sbx` CLI; the optional MCP adapter uses the same engine and is not required.
For a single pass/fail check, use `sbx run` or `sandbox_run` from the windows-sandbox-app-test skill instead.
If a command or tool says the sandbox isn't ready, follow the windows-sandbox-setup skill.

## The loop

1. Start with `sbx start` or `sandbox_start`. Takes 20-40 s, and waits for the desktop to be ready. Use `--network off` or `network: "off"` when the app must not reach the internet; `"firewall"` is weaker because admin code could undo it. `sbx status` / `sandbox_status` reports readiness, the boot epoch and the verified agent version.
2. Copy the build output with `sbx push <hostPath>` or `sandbox_copy_in`; it lands in `C:\apps\<name>` by default.
3. Use `sbx launch <exe>` or `sandbox_launch` for a GUI app, and `sbx exec <command...>` or `sandbox_exec` for a console command. Long-running processes belong in `launch`. For an installed package, use its `PackageFamilyName!AppId` AUMID.
4. Look and act, using the tools below.
5. `sandbox_app_errors` with the `launchedAt` time from `sandbox_launch`, to catch crashes and .NET unhandled exceptions. `sandbox_process` shows whether the app is still running.
6. `sandbox_copy_out` logs, output files and crash dumps.
7. Stop with `sbx stop` or `sandbox_stop`. Everything inside is destroyed; artifacts stay on the host in the run's `out` folder. Always stop when finished, because only one sandbox can exist at a time.

## CLI and MCP command map

These are interfaces to the same engine and shared guest state, not two required components:

| Workflow | CLI | MCP |
|---|---|---|
| Guest lifecycle / status | `sbx start`, `status`, `stop`, `desktop-release` | `sandbox_start`, `sandbox_status`, `sandbox_stop`, `sandbox_desktop_release` |
| UI inspection / actions | `sbx ui tree`, `ui wait`, `ui click`, `ui set`, `click`, `type`, `windows`, `proc`, `errors` | `sandbox_ui_tree`, `sandbox_ui_wait`, `sandbox_ui_action`, `sandbox_click`, `sandbox_type`, `sandbox_windows`, `sandbox_process`, `sandbox_app_errors` |
| Screenshots / recording | `sbx shot`, `sbx record start`, `sbx record stop` | `sandbox_screenshot`, `sandbox_record_start`, `sandbox_record_stop` |
| Commands, files and warm deploy | `sbx exec`, `push`, `pull`, `deploy` | `sandbox_exec`, `sandbox_copy_in`, `sandbox_copy_out`, `sandbox_deploy` |
| Snapshots / prerequisites | `sbx snapshot`, `diff`, `deps`, `provision` | `sandbox_snapshot`, `sandbox_diff`, `sandbox_deps`, `sandbox_provision` |

Use the CLI when the agent can run shell commands; use MCP when its discoverable schemas, structured results or
inline screenshot images help. The tool names and output formats differ, but both reach the same implementation.

## Prefer UI Automation over pixels

- `sandbox_ui_tree` with the `pid` gives one line per control: `Button "Save" #SaveButton {invoke}`. It's cheaper and more precise than a screenshot.
- `sandbox_ui_action` finds a control by `name`, `automationId` or `controlType` and performs `click`, `setvalue` (with `value`), `toggle`, `select`, `expand`, `read` and others. A `{pending: true}` result means a modal dialog opened, which is normal.
- `sandbox_ui_wait` waits for a result label, dialog or state to appear. Use it instead of sleeping.
- `sandbox_screenshot` is for visual checks, and `sandbox_windows` lists top-level windows.
- `sandbox_click` and `sandbox_type` are the fallback when UI Automation can't see a control (custom-drawn UI, games, some Chromium content). Click coordinates refer to the most recent screenshot; pass its `captureId` to use an older one. Out-of-image points and moved or resized windows fail on purpose, so take a new screenshot. `sandbox_type` with `literal: false` uses SendKeys syntax such as `{ENTER}` or `^s`.

WinForms, WPF, Win32 and WinUI controls all appear in the tree. The first UI Automation call in a sandbox takes about 4 s. Screenshot, click, type and UI actions fail closed on a locked or secure desktop, including UAC prompts.

## Warm deploy loop

For build, deploy, relaunch, repeat: start once, then run `sbx deploy <hostDir> [guestDir] --launch MyApp.exe --restart`,
or call `sandbox_deploy` with `hostPath`, an optional `sandboxPath`, `launch: "MyApp.exe"` and `restart: true`.

- It transfers only changed files, removes deleted ones and verifies every hash. `sandbox_copy_in` is still a full replacement.
- Use a dedicated guest folder, because **extra files in it are deleted**.
- Rebuild before the deploy, not during it.
- This reuses a running sandbox, so **it isn't a clean-machine test**. Do a final `sandbox_run` before calling anything clean.

## Keep visual evidence

`sbx record start` / `sbx record stop` or `sandbox_record_start` / `sandbox_record_stop` record the desktop, even during long `sbx exec` / `sandbox_exec` calls. The defaults are 2 fps for 120 s, with caps of 5 fps, 300 s and 600 frames. Stopping publishes a self-contained HTML flipbook, plus an MP4 if ffmpeg is already on the host. Frames survive a crash, and nothing is installed in the guest.

## Sharing with the CLI

The CLI and MCP can use one guest. Commands that change the desktop take cooperative turns, while observations and `sandbox_exec` don't reserve it. A competing workflow waits up to 60 s and then gets a clear desktop-busy error. Call `sandbox_desktop_release` when you finish a turn, and don't use `sandbox_exec` to get around a turn for UI input.

## Missing prerequisites

Diagnose before installing anything: `sandbox_deps` is a host-only scan. A missing prerequisite is often the bug being hunted, so **don't install one unless the user explicitly asks**. If they do, `sandbox_provision` with `app` and `provision` (`auto`, or a list such as `vcredist:x64,desktop:10.0:x64`) installs verified Microsoft runtimes into the guest you already started. It never boots or adopts one. Label anything after that as provisioned, not clean.

## See what something changed

Call `sandbox_snapshot` with `name: "before"`, do the action, call it again with `name: "after"`, then `sandbox_diff` with `from` and `to`. The diff covers installed programs, services, autoruns, environment values, files and registry keys. Each snapshot takes about 15 s. Pass `exclude` to ignore noisy paths.

## What's in the sandbox

It's a clean Windows 11 with Windows PowerShell 5.1 and .NET Framework 4.8, and an elevated admin user. It has no dev tools, no Store apps (no Notepad, Calculator or Terminal) and no winget. Every boot is fresh.

`sandbox_exec` runs PowerShell by default; use `shell: "cmd"` for batch syntax. The sandbox shuts down after 30 idle minutes. When the MCP client disconnects, only a sandbox that client started is stopped.

Treat anything copied out of the sandbox as untrusted, especially if you ran something you don't trust in it.
