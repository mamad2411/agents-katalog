---
name: app-it-windows
description: >-
  Create Windows beta desktop launchers for local web projects: WPF + WebView2
  .exe, Start Menu shortcut, .ico, warm server, quit cleanup. Use when the user
  asks for app-it-windows, a Windows app, .exe launcher, Start Menu shortcut,
  Windows package, or desktop icon. CI-guarded but untested on Windows hardware;
  never claim runtime success without a Windows maintainer.
---

# app-it-windows - Make a project launchable on Windows (beta)

**Windows beta: scaffolded, untested on real hardware, maintainer wanted.**

The macOS `app-it` lane is proven. This Windows sibling mirrors the contract
with Windows primitives, but every runtime behavior that needs a real Windows
desktop must be marked deferred: `this needs a Windows maintainer - see
docs/WINDOWS.md`.

## Non-Negotiables

1. Run `templates/inspect.ps1` first and read the output before editing.
2. Trust disk over docs. Verify project type, scripts, ports, and desktop
   signals from files.
3. Build everything a Mac or CI can build; never claim Windows runtime behavior
   works unless it was verified on real Windows hardware.
4. Prefer the WPF + WebView2 host. Edge `--app=` is a fallback, not the default.
5. Keep Windows visibly beta in every report and user-facing summary.
6. Copy shipped templates and customize through `scripts\app-it.config.json`.
   Do not re-derive launcher patterns.
7. Verify build/lint/config checks, then list hardware-only checks as deferred.

## Reference Map

Open only what the inspection or chosen path needs:

- `references/maintainer-contract.md` - what a Mac can produce, what must be
  deferred, and the exact Windows-maintainer phrase.
- `references/inspection-and-strategies.md` - project inspection, toolchain
  probes, strategy tree, W-Native, W-Edge, W-Static, W-Multi, B, and D.
- `references/generated-files.md` - template roster, allowed target files,
  config JSON, package scripts, and Start Menu destination.
- `references/wrapper-host.md` - WebView2 host, lifecycle, Job Object ownership,
  single-instance behavior, and wrapper argument contract.
- `references/verification.md` - buildable checks, Windows-only checks, and
  deferred rows.
- `references/report-template.md` - exact beta report format.

## Templates

Templates live next to this file in `templates/`. Copy them into the target
project and keep their contracts intact:

```text
templates/
  wrapper-windows/
  desktop-build.ps1
  desktop-install.ps1
  desktop-quit.ps1
  inspect.ps1
  run-template.ps1
  run-template-edge.ps1
  desktop-icons.ps1
  placeholder-icon-gen.ps1
  PSScriptAnalyzerSettings.psd1
  app-it.config.example.json
```

The comments inside templates encode Windows traps: PATH augmentation,
WebView2/.NET prerequisites, free-port probing, Job Object ownership, Start Menu
shortcuts, SmartScreen, and icon-cache behavior. Read the matching reference
before changing launcher internals.

## Workflow

### 1. Inspect

Run the bundled probe from the target project root:

```powershell
pwsh -File path\to\plugins\app-it-windows\skills\app-it-windows\templates\inspect.ps1
```

Read `references/inspection-and-strategies.md` before deciding project shape,
ports, existing desktop tooling, names, icons, or strategy.

### 2. Decide

For each user-facing app:

```text
Existing Electron/Tauri/NW.js Windows target?
  yes -> Strategy B
  no  -> native desktop requirement beyond web shell?
           yes -> Strategy D
           no  -> .NET 8 buildable and WebView2 expected?
                    no  -> W-Edge fallback
                    yes -> static built bundle, no server?
                             yes -> W-Static
                             no  -> cohabiting frontend + backend?
                                      yes -> W-Multi
                                      no  -> W-Native (default)
```

WebView2 is Chromium, so File System Access and other Chromium APIs are reasons
to prefer the WPF host, not reasons for a polyfill.

### 3. Build

Touch as little project surface as possible. Copy the selected templates, write
`scripts\app-it.config.json`, add `desktop:*` package scripts, and generate the
`.ico`/published output when tooling is present.

Read `references/generated-files.md` before editing scripts/config/docs, and
`references/wrapper-host.md` before changing the host or PowerShell lifecycle.

### 4. Verify

On macOS, only claim buildable evidence: .NET publish when available,
PowerShell lint when available, manifest/config parse, and placeholder icon
round-trip in Windows CI. Everything involving a real window, Taskbar identity,
tray Quit, Start Menu icon cache, SmartScreen, DPI, or Job Object tree reaping
stays deferred with the maintainer phrase.

Read `references/verification.md` before reporting results.

### 5. Report

Use `references/report-template.md` inline and in
`docs\desktop-launcher.app-it-report.md`. Keep beta wording visible, separate
build/lint evidence from runtime unknowns, and append decision history.

Stage files only when the local convention or user request asks for it. Do not
commit unless asked.

## Quick Defaults

- Install destination:
  `%APPDATA%\Microsoft\Windows\Start Menu\Programs\app-it\`.
- Runtime state:
  `%LOCALAPPDATA%\app-it\<slug>\`.
- Bundle ID/key prefix: `com.user.<slug>`.
- Default strategy: W-Native when .NET 8 can build and WebView2 is expected.
- Fallback: W-Edge only when host prerequisites are unavailable.
- Icon sizes: `16, 32, 48, 64, 128, 256`.
- First-run signing stance: unsigned; SmartScreen click-through documented.

## Stop Signs

Stop and mark deferred or blocked when only Windows hardware can decide, when
the required build toolchain is missing and no fallback fits, when a port cannot
be made env-driven, when a template needed for the selected strategy is absent,
or when the requested claim would imply real Windows runtime verification that
has not happened.
