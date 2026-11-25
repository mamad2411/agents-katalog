---
name: storage-permissions
description: Explain why a path is unreadable or unwritable on Termux (missing storage link, revoked Android permission, scoped storage, a filesystem without Unix modes or symlinks, a proot bind that was never made) and choose where files should live. Use for Permission denied, a missing ~/storage, /sdcard access, or git and venv failures on shared storage. Do NOT use for Termux API permission errors (see termux-api) or for ordinary file mode problems under $HOME.
license: MIT
compatibility: Termux on Android (Bionic libc, usually aarch64). Where a skill says so, also usable from a proot distro.
metadata:
  risk: "low"
  triggers: "storage permission,permission denied android,shared storage,sdcard,termux-setup-storage,scoped storage,downloads folder empty,save to gallery,cannot save files to phone storage"
---
# Android Storage Permissions

## Purpose
Say which kind of path this is (private Termux storage, a shared-storage link, a proot-visible path, or an Android permission boundary) and what that means for permissions, symlinks, and executables.

## When to use
- `Permission denied` on `/sdcard`, `~/storage/...`, or a path outside `$HOME`.
- `~/storage` is missing, empty, or its links point nowhere.
- A tool works in Termux but not in proot.
- git, a venv, or an executable misbehaves on shared storage.

## When NOT to use
- `termux-*` API errors: use `termux-api`.
- Unix mode problems on files that live under `$HOME`: ordinary `ls -l` and `chmod` reasoning applies.

## Preconditions
Capture, read-only: `pwd`, `$HOME`, the failing path, and `sh scripts/check-storage.sh`. Do not list or print unrelated private filenames from shared storage.

## Decision tree
1. `~/storage/shared` absent in native Termux: storage access was never set up, or the links were deleted.
2. Links present but access denied: Android permission was revoked, often by the system's "remove permissions if app is unused" auto-reset. Re-granting happens in Android settings or by confirmed `termux-setup-storage`.
3. Shared storage is a FUSE-style filesystem. It has no Unix owner or mode bits, no symlinks, and no executable bit. Consequences: `chmod` has no effect, venvs fail, git reports every file as mode-changed, scripts cannot be executed in place. Keep repositories, venvs, and keys under `$HOME`; use shared storage only for exchange files.
4. A Unix mode bit is not proof of Android permission, and a granted Android permission does not give Unix rights.
5. Other apps' `Android/data` and `Android/obb` are blocked by scoped storage on recent Android. Do not try to work around it.
6. Inside proot a path is visible only if it was bound at login; a Termux path is not automatically present.
7. Prefer `$HOME` unless the task needs the file to be visible to other Android apps.

## Example
- Situation: python -m venv under /sdcard fails with a symlink or permission error.
- Without the skill: Runs `chmod -R 777`, which has no effect on shared storage.
- With the skill: Explains that shared storage has no Unix modes, symlinks, or executable bit, moves the repository and venv under `$HOME`, and keeps only exchange files on shared storage.

## Safety
`termux-setup-storage` changes user-visible links and shows an Android dialog: ask first. Never create, move, or delete files in shared storage without approval, and never run `chmod` or `chown` loops against it.

## Verification
Check only the requested path, with a harmless read the user chose. A write test needs approval and a throwaway filename in a directory the user named.

## Handoffs
- `termux-environment` when Android version or the native/proot side is unknown.
- `proot-boundaries` when the failure is only inside proot.
- `termux-backup` when the user wants an archive written to shared storage.
- `git-credentials` when keys were placed on shared storage.

## Report
Which path class the failing path belongs to, which of the rules above applies, and the single recommended change (a permission grant, a bind, or moving the file under `$HOME`).
