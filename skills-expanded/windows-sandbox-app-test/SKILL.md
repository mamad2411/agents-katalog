---
name: windows-sandbox-app-test
description: Check that a Windows desktop or console app, or an MSIX package, runs on a fresh, throwaway Windows machine (Windows Sandbox) in one call, with dependency diagnosis, a screenshot, crash check, optional test script and report. Use when asked to "try my build on a clean machine", check that an exe runs without the dev box's installed runtimes, find which runtimes an app needs, smoke-test a build, or reproduce "works on my machine" bugs, using sbx or the optional MCP adapter.
---

# Test an app on a clean machine

This skill documents v1.2.0. Older ZIPs don't contain every tool below.

Windows Sandbox is a clean Windows 11 VM that boots in about 15-20 s and is **destroyed on stop**. Only **one** can run at a time. Nothing from the host is installed in it: no dev tools, no Store apps (no Notepad, Calculator, Terminal) and no winget. It has Windows PowerShell 5.1 and .NET Framework 4.8. Treat it like a brand-new customer PC.

If shell access is available, use the `sbx` CLI; the optional MCP adapter uses the same engine and is not required.

Use a different skill for other jobs:

- Testing an installer or uninstaller: windows-sandbox-installer-test
- Running a file you don't trust: windows-sandbox-detonate
- Multi-step UI work or a warm deploy loop: windows-sandbox-interactive
- "Windows Sandbox isn't ready" or missing tools: windows-sandbox-setup

## 1. Diagnose dependencies first

Run `sbx deps <path>` or call `sandbox_deps` with `path`. It's a host-only static scan that doesn't boot a sandbox, run the app or install anything. Its output includes the scan's limits and any uncertain optional components, so report those too.

## 2. Run it

Run `sbx run <app.exe|folder>` or call `sandbox_run` with `app` set to a host path. Both use the same workflow: boot the sandbox, copy the app in, run it, capture a screenshot, check the event log for crashes, optionally run a test script, copy files out, destroy the sandbox and write `report.md`. The MCP adapter can return the screenshot inline; the CLI writes it to the report folder. Measured GUI samples take roughly 40-50 s.

- **`app`** is an `.exe` (its whole folder is copied), a folder, or a package. Pass `exe` if a folder has more than one `.exe`.
- **`console: true`** is for console apps. It runs to completion and captures stdout. Without it, the app is launched as a GUI app and given `waitSec` (default 5) to settle.
- **`args`** passes command-line arguments.
- **`collect`** lists sandbox paths to copy back to the host, such as logs or output files.
- **`record: true`** records the desktop at 2 fps for up to 120 s, and the report links the recording.
- **`network`** is `on` by default. Use `off` to prove the app works with no network at all.
- **`keep: true`** leaves the sandbox running so you can investigate with the windows-sandbox-interactive tools. Call `sandbox_stop` when you're done.

## Missing runtimes are findings

A missing prerequisite is often exactly the bug being hunted. **Don't install one to get a pass unless the user explicitly asks.** Report which runtime is missing, and suggest bundling it or publishing self-contained.

If the user does ask, pass `provision: "auto"` or a list such as `desktop:10.0:x64,vcredist:x64` (CLI: `--provision auto`). The host downloads and verifies official Microsoft installers and copies them in, so guest networking can stay off. Always label that result **provisioned, not a clean-machine pass**.

## Packaged apps

For `.msix`, `.msixbundle`, `.appx` or `.appxbundle`, `sandbox_run` installs offline dependencies and activates the app, then follows the same screenshot, UI Automation and report flow. No Store or package download is attempted.

- `cert` is a public `.cer`, trusted only in the disposable guest.
- `deps` is a folder of dependency packages. It defaults to a `deps` folder beside the package.
- `appId` is required if the manifest has several applications.

```powershell
sbx run app.msix --cert devcert.cer --deps Dependencies\x64 --app-id App --network off
```

Tests for packages get `$env:SBX_APP_AUMID`. The package's install folder is read-only, so write files to `$env:SBX_OUT` or app data.

## Read the result

The run fails when the app exits non-zero, a console app times out, the test script fails, or the event log has a crash or error mentioning the exe.

**PASS doesn't prove the app works.** It means the app started and nothing crashed. A GUI app that shows an error dialog and keeps running can still pass. Always look at the returned screenshot, and describe what it shows. Add a test script to check real behavior.

Artifacts stay on the host after the sandbox is gone: `report.md`, `report.json`, screenshots and collected files in the run's `out` folder.

## Add a test script

`test` is a host `.ps1` that runs **inside** the sandbox after launch. Throw or exit non-zero to fail. It gets:

- `$env:SBX_APP_PID`, `$env:SBX_APP_DIR` and `$env:SBX_APP_EXE`
- `$env:SBX_OUT`; anything written there comes back to the host
- `Get-SbxUiTree`, `Invoke-SbxUi` and `Wait-SbxUi`, already imported

```powershell
$ErrorActionPreference = 'Stop'
$app = @{ ProcessId = $env:SBX_APP_PID }
Invoke-SbxUi @app -AutomationId NameBox -Action setvalue -Value 'Sandbox'
Invoke-SbxUi @app -Name Greet -Action click
Wait-SbxUi @app -Name 'Hello, Sandbox!' -TimeoutSec 5 | Out-Null
```

UI Automation works for WinForms, WPF, Win32 and WinUI. To find control names, start with `keep: true` and read them with `sandbox_ui_tree`.

## Common errors

- **`A sandbox is already running`:** one-shot runs don't queue. See the windows-sandbox-setup skill.
- **`Say which exe to run`:** the folder has several `.exe` files or none. Pass `exe`, or point at the right folder.
