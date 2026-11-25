---
name: usage-monitor-nsis-installer
description: Build, inspect, and troubleshoot the NSIS installer workflow for the usage-monitor repository, including the Gradle packaging path, the Windows icon-patched helper flow, and the known freeze diagnostics. Use when Codex needs to create, debug, or validate the Windows installer for this project.
---

# Usage Monitor NSIS Installer

Build and troubleshoot the Windows installer while preserving the repository's known-good NSIS rules.

## Workflow

1. Read [AGENTS.md](../../../AGENTS.md), [README.md](../../../README.md), [build.gradle.kts](../../../build.gradle.kts), and [src/installer/UsageMonitor.nsi](../../../src/installer/UsageMonitor.nsi) first.
2. Prefer the Gradle path first:
   - `gradlew.bat createDistributable`
   - `gradlew.bat packageInstaller`
3. Use the helper [build-with-icon.ps1](../../../build-with-icon.ps1) only when the task specifically needs the icon-patched Windows executable plus a local installer build.
4. Validate the expected output:
   - `build/compose/binaries/main/app/Usage Monitor`
   - `build/installer/UsageMonitor-Setup-<version>.exe`
5. When debugging installer freezes, use the repository's known lessons:
   - Freeze at 99 percent strongly suggests compression trouble.
   - Freeze on the finish screen strongly suggests a blocking process launch.
   - Keep `SetCompressor zlib` in the NSIS script.
   - Avoid blocking success flows with `ExecWait`.
6. Preserve the current installer behavior unless the user explicitly wants to change it:
   - user-level install
   - uninstall registry handling
   - Start Menu and desktop shortcuts
   - optional Windows auto-start entry

## Guardrails

- Do not assume NSIS is installed; verify it first on Windows.
- Do not replace the Gradle packaging path with ad hoc file copies unless the user is explicitly debugging the helper flow.
- When changing installer behavior, inspect both [src/installer/UsageMonitor.nsi](../../../src/installer/UsageMonitor.nsi) and the related Gradle tasks in [build.gradle.kts](../../../build.gradle.kts).
