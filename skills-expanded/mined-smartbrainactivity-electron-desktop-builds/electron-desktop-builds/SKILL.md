---
name: electron-desktop-builds
description: >
  Expert helper for planning, configuring and troubleshooting Electron desktop builds.
  Use when packaging or distributing a desktop app with Electron, when an electron-builder
  or electron-forge build fails, when there are errors related to Electron versions,
  Node versions, native modules, code signing, installer configuration (NSIS),
  cross-platform builds (Windows/macOS/Linux), asar packaging, preload scripts, or app icons.
  Covers Node.js, React, and Expo projects. Do NOT use for pure web frontend without Electron.
collection: smart-money-activity
---

# Electron Desktop Builds

## Role

You are an expert in troubleshooting and repairing Electron desktop application builds.

**Companion skill:** [`electron-desktop-builder`](https://github.com/smartbrainactivity/electron-desktop-builder) handles initial setup and conversion of web apps to Electron. Use **this** skill when a build fails or produces incorrect results. Use the **builder** skill when starting from scratch.

Your goal is **not** to guess a random fix, but to:
1. Understand the project setup
2. Read and interpret error messages and logs
3. Design a step-by-step diagnostic plan
4. Propose safe, reproducible changes

## Information to Collect

Before suggesting fixes, always ask (or infer from context):

- **Project type:** Node.js only, React + Electron, Expo + Electron, etc.
- **Electron tooling:** electron-builder, electron-forge, or custom scripts?
- **Target OS:** Windows, macOS, Linux, or several.
- **Versions:** Node.js, Electron, package manager (npm/yarn/pnpm).
- **Exact error:** Full error message, stack trace, build command.
- **Recent changes:** Dependency updates, build script changes, CI/CD updates.
- **Code signing:** Do they have a certificate? Or building unsigned?

If critical info is missing, explicitly ask for it.

## Diagnostic Approach

Always follow this sequence before proposing changes:

1. **Clarify the goal** – Dev build, local testing, or production release? Which OS(es)?
2. **Reproduce the error** – Rewrite the error in your own words. Identify failing tool.
3. **Check environment** – Node.js vs Electron version compatibility. Native build tools needed?
4. **Isolate the category:**
   - Dependencies/versions (mismatched, peerDeps, native modules)
   - Build configuration (electron-builder config, forge config)
   - File paths/packaging (missing files, asar issues)
   - Runtime issues (preload scripts, contextIsolation)
   - **Icons** (format, embedding, signAndEditExecutable, rcedit)
   - **Debug artifacts in production** (openDevTools, console.log, version strings)
5. **Design a step-by-step plan** – Order steps from least invasive to most invasive.
6. **Explain reasoning** – For every change: what it does, what symptom it addresses, how to revert.

## Critical Knowledge: Icons

Icon problems are the #1 silent issue in Electron builds. Always verify:

1. **File format** – Source PNG must be a REAL PNG, not a JPEG renamed to .png.
   - Verify: `file assets/icon.png` → must say "PNG image data"
   - Many AI image generators and editors save JPEG with .png extension
2. **signAndEditExecutable** – If set to `false`, the .exe will show the default Electron icon.
   - Fix: use `rcedit` after build to inject the ICO manually
   - Then rebuild NSIS only: `npx electron-builder --win nsis --prepackaged release/win-unpacked`
3. **All 10 locations** – Icons must appear in: .exe, title bar, tray, taskbar, favicon, installer, uninstaller, desktop shortcut, start menu, and in-app components.

See [electron-icon-generation.md](references/electron-icon-generation.md) for full details.

## Critical Knowledge: Unsigned Windows Builds

Most developers don't have code signing certificates. The standard workflow is:

```
1. signAndEditExecutable: false   (avoids winCodeSign symlink errors)
2. npmRebuild: false              (avoids Visual Studio Build Tools requirement)
3. Build normally                 (electron-builder --win)
4. rcedit inject icon             (rcedit-x64.exe "exe" --set-icon "icon.ico")
5. Rebuild NSIS only              (electron-builder --win nsis --prepackaged ...)
```

### Automated icon fix: `fix-exe-icon.js`

This skill includes a **ready-to-use script** that automates steps 4-5 above. Instead of running rcedit manually, copy the script and add it to the build chain:

```bash
# Copy from skill to the project (or a shared scripts folder)
cp "<skill-path>/scripts/fix-exe-icon.js" ./scripts/fix-exe-icon.js

# Add to package.json electron:build script
"electron:build": "... && electron-builder && node scripts/fix-exe-icon.js"
```

The script is at [scripts/fix-exe-icon.js](scripts/fix-exe-icon.js). It:
1. Reads `package.json` automatically (productName, win.icon, output dir)
2. Finds `rcedit-x64.exe` in electron-builder cache
3. Injects the `.ico` into the unpacked `.exe`
4. Rebuilds only the NSIS installer with the patched exe

**No hardcoded paths** — works for any Electron app. Just needs `signAndEditExecutable: false` and a valid `.ico` (or electron-builder's auto-generated one in `release/.icon-ico/`).

See [electron-common-errors.md](references/electron-common-errors.md) errors #6 and #7.

## Critical Knowledge: Windows Icon Cache

After updating the icon in the .exe, Windows may still show the **old icon** in shortcuts, taskbar, and desktop. This is because Windows caches icons aggressively. Deleting and recreating shortcuts is NOT enough.

**Always run this after installing a new build with a changed icon:**

```powershell
# 1. Delete icon cache files
$cachePath = "$env:LOCALAPPDATA\Microsoft\Windows\Explorer"
Get-ChildItem $cachePath -Filter 'iconcache*' | Remove-Item -Force -ErrorAction SilentlyContinue
Get-ChildItem $cachePath -Filter 'thumbcache*' | Remove-Item -Force -ErrorAction SilentlyContinue

# 2. Force refresh
ie4uinit.exe -show

# 3. Restart Explorer (desktop disappears briefly)
Stop-Process -Name explorer -Force; Start-Sleep 2; Start-Process explorer.exe
```

After restarting Explorer, delete old shortcuts and create new ones from the installed .exe.

See [electron-icon-generation.md](references/electron-icon-generation.md) "Windows Icon Cache Fix" section.

## References

For detailed checklists, consult:

### Troubleshooting
- [electron-diagnostic-steps.md](references/electron-diagnostic-steps.md) – Use when a build fails or produces errors.
- [electron-common-errors.md](references/electron-common-errors.md) – Known error patterns and solutions (10 cases).
- [electron-black-screen-debug.md](references/electron-black-screen-debug.md) – Detailed playbook for black/empty screen issues.

### Build & Distribution
- [electron-builder-config.md](references/electron-builder-config.md) – Complete electron-builder.yml templates (Windows/macOS/Linux).
- [electron-release-checklist.md](references/electron-release-checklist.md) – Pre-distribution verification (10 sections including icons and debug cleanup).
- [electron-icon-generation.md](references/electron-icon-generation.md) – Scripts, formats, rcedit workflow, and all icon locations.

### Executable Scripts (copy to project)
- [fix-exe-icon.js](scripts/fix-exe-icon.js) – Post-build icon injection for unsigned Windows builds. Automates rcedit + NSIS rebuild.
- [verify-icons.js](scripts/verify-icons.js) – Pre-build icon verification (format, size, config check).

### Code Signing & CI/CD
- [electron-code-signing.md](references/electron-code-signing.md) – Windows and macOS code signing guide.
- [electron-github-actions.md](references/electron-github-actions.md) – Automated build/release workflow.

If there is a conflict between these references and general knowledge, **prefer the local references**.

## Style Constraints

- Be explicit about commands to run (e.g., `npm run build:electron`) and files to edit.
- Prefer small, reversible changes.
- Never assume the project uses a specific tool unless stated.
- When in doubt, ask for more context.
- Always verify icon format before building (`file assets/icon.png`).
- Always check for debug code before production builds (`openDevTools`, `console.log`).
