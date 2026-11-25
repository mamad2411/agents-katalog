---
name: storage-clean
description: Use for low disk space or storage cleanup — cache pruning, Downloads triage, Docker/Podman/WSL bloat, package-manager caches, Windows Update cleanup, Linux journal/snapshot cleanup, or safe ways to reclaim disk space on macOS, Windows, or Linux.
---

# Storage Clean

## Overview

Reclaim disk space by measuring first, separating disposable caches from user data, and requiring confirmation before deletion. Prefer built-in cleanup tools and tool-specific prune commands over manual deletion. Treat user files, databases, virtual machines, model weights, Docker volumes, WSL distros, and unknown application state as high risk until proven otherwise.

## Workflow

1. **Identify** the OS, target volume, free space, and whether the user wants analysis only or approved cleanup.
2. **Measure** read-only: volume pressure, top-level directory sizes, cache sizes, and large user-created files.
3. **Load** the platform reference for the target machine:
   - macOS: `references/macos.md`
   - Windows: `references/windows.md`
   - Linux: `references/linux.md`
4. **Group** candidates by risk category:
   - **Low**: re-downloadable caches and tool-managed temporary data.
   - **Medium**: installers, disk images, archives, exports, logs, old downloads.
   - **High**: documents, photos, project folders, databases, VM images, Docker volumes, WSL distros, local models, checkpoints.
   - **System-critical**: OS internals and package installer state — only handle via official OS tools.
5. **Present** exact candidates with path, size, category, risk, command, admin requirement, and re-download/rollback cost.
   - Never delete user files automatically, even if old or large.
   - Never empty Trash or Recycle Bin without explicit confirmation.
   - Never use broad recursive deletion on `AppData`, `Library`, `ProgramData`, `Windows`, project roots, or application support directories.
   - Never manually delete system internals when an OS cleanup tool exists.
   - Require explicit approval before pruning Docker volumes, unregistering WSL distros, removing toolchains, or deleting model caches.
   - On Linux, never manually delete package databases, `/var/lib/*` state, `/boot` kernels, Docker/Podman storage internals, or Btrfs/Snapper/Timeshift snapshots.
6. **Execute** only explicitly approved actions.
7. **Re-measure** with the same baseline and report before/after free space plus anything intentionally left untouched. Re-read command output and verify counts, sizes, and free space — do not stop after running commands.

## Platform Reference

| Platform | Key paths & tools | Reference |
|---|---|---|
| macOS | `/Users`, `~/Library`, Homebrew, Trash, APFS snapshots, Docker Desktop | `references/macos.md` |
| Windows | `C:\`, PowerShell, Storage Sense, Disk Cleanup, DISM, WSL2, WinGet, Scoop, Chocolatey, Docker Desktop | `references/windows.md` |
| Linux | `/home`, `/var`, `/boot`, systemd journal, APT/DNF/Zypper/Pacman/APK, Flatpak, Snap, Docker, Podman, Btrfs, Snapper, Timeshift | `references/linux.md` |

**Cross-platform**: Determine where cleanup runs before choosing commands. Do not apply Windows deletion commands to mounted macOS paths, macOS shell commands to WSL/PowerShell paths, or Linux commands to Windows/macOS host storage unless the target is explicitly a Linux environment.

## Reporting Format

For each proposed deletion or cleanup command, report:

```text
Path:
Size:
Category:
Risk:
Why it is probably safe/risky:
Cleanup command:
Rollback/re-download cost:
Needs admin:
Requires explicit confirmation:
```

For each meaningful decision, include:

- Conclusion
- Reason
- Risk
- Next step
- Scope and validation method when changing or deleting anything
