---
name: windows-c-drive-cleanup
description: "Safe Windows C: drive space analysis and cleanup workflow. Use when a user asks Codex to scan, diagnose, clean, free space, remove large files, identify uninstall candidates, or troubleshoot low disk space on a Windows system drive, especially C:\\. Emphasizes read-only analysis first, risk classification, explicit user approval before deletion or uninstalling, privacy-preserving local-only scans, and safe handling of Windows Installer, WinSxS, AppData, ProgramData, caches, personal files, and large application data."
---

# Windows C Drive Cleanup

## Core Rule

Treat Windows system-drive cleanup as a staged safety workflow, not a deletion task.

Never delete, move, uninstall, change ACLs, or take ownership until the user explicitly approves a named operation on exact paths or packages.

## Safety Principles

- Start with read-only scans.
- Do not upload, transmit, or summarize private file contents.
- Report paths and sizes only as needed for cleanup decisions.
- Classify each candidate before recommending action.
- Prefer clearing cache contents over deleting parent app folders.
- Preserve user data by default.
- Use vendor uninstallers or package managers for installed applications.
- Use Windows-supported tools for component stores and updates.
- Treat `C:\Windows\Installer` as high risk and use quarantine, hash verification, and logs before any deletion.

## Workflow

1. Confirm scope.
   - Identify the drive, usually `C:\`.
   - Confirm whether the user wants analysis only or has approved a specific cleanup action.

2. Run read-only inventory.
   - Prefer `scripts/Analyze-CDrive.ps1`.
   - Gather drive usage, top-level directory sizes, user profile breakdown, `AppData`, `ProgramData`, `Program Files`, `Windows`, and largest user files.

3. Classify findings.
   - Load `references/cleanup-policy.md`.
   - Load `references/windows-installer-msp.md` before any `C:\Windows\Installer` work.

4. Present options.
   - Group findings into low-risk cache, user data, uninstall-only, and avoid/manual-system-tool categories.
   - Include expected savings and exact paths.
   - Ask for approval before destructive actions.

5. Execute only approved cleanup.
   - Use exact paths and `-LiteralPath` semantics.
   - Use allowlists for scripted deletion.
   - For personal data, delete or move only what the user explicitly named.
   - For Windows Installer orphan-like MSP files, use `scripts/Quarantine-OrphanMsp.ps1`.

6. Verify.
   - Recheck drive free space.
   - Recheck target paths.
   - Report what changed, what was skipped, and where any quarantine backup is stored.

## Bundled Scripts

- `scripts/Analyze-CDrive.ps1`: read-only inventory script.
- `scripts/Quarantine-OrphanMsp.ps1`: Windows Installer orphan-like MSP quarantine helper. Defaults to dry-run unless `-DeleteOriginals` is supplied.

## Common Cleanup Categories

- Low-risk caches: temp files, browser caches, Electron app caches, crash dumps, GPU caches, game shader caches.
- Confirm first: downloads, documents, chat files, recordings, game saves, project files, old app version folders.
- Uninstall only: Office, Adobe, SQL Server, VPN/security clients, launchers, Python distributions, NVIDIA tools, Lenovo/OEM tools.
- Avoid manual deletion: `WinSxS`, `System32`, `SysWOW64`, `servicing`, registry hives, page/swap/hibernation files, and active installer caches.

## Response Pattern

Lead with the highest-impact safe options. Explain risk in plain language. Never imply that all large files are safe to delete. For any destructive step, repeat the exact action and wait for confirmation unless the user already gave a clear command.
