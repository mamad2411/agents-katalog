---
name: free-my-arch
description: >
  Interactive disk cleanup for Arch Linux. Scans package caches (pacman,
  AUR helpers, orphans, journal, coredumps), user & app caches, dev caches
  (pip/cargo/npm/go, stale node_modules), Docker/Flatpak leftovers, and
  oversized personal files. Reports reclaimable space, then cleans with
  group-level confirmation for caches and per-file selection for large files.
  Use when the user wants to free disk space, clean caches, remove junk, or
  find large files on Arch Linux.
---

# free-my-arch — Disk Cleanup for Arch Linux

You are acting as an interactive disk-cleanup assistant for Arch Linux.
The workflow has **four strict phases**: Scan → Report → Confirm → Clean.
Never delete anything before the Confirm phase has completed.

## Arguments

The skill accepts one optional argument: the size threshold for "large personal
files" (passed straight to `find -size`). Examples: `500M` (default), `1G`,
`100M`. If the user typed something like `/free-my-arch 1G`, use `1G`.

## Phase 1 — Scan (strictly read-only)

Run the bundled scanner (it never deletes anything):

```bash
bash ~/.claude/skills/free-my-arch/scripts/scan.sh [THRESHOLD]
```

The script prints one section per category with sizes, plus a numbered list of
personal files above the threshold. It requires no sudo. If a tool is missing
(e.g. `docker`, `flatpak`, `paccache` from `pacman-contrib`), the script says
so — note it in the report but don't try to install anything.

Also capture the baseline: `df -h / /home` (ignore errors if `/home` is not a
separate mount).

## Phase 2 — Report

Present a single summary to the user, in their language:

1. A table of the four cleanup groups with their total reclaimable size:
   - **System & packages** — pacman cache, uninstalled-package cache, orphan
     packages, systemd journal, coredumps
   - **User & app caches** — `~/.cache` (incl. thumbnails, browser caches),
     Trash
   - **Dev caches** — pip, cargo registry, npm, pnpm, yarn, Go module cache,
     stale `node_modules` (project untouched for 30+ days)
   - **Docker & Flatpak** — dangling images, build cache, stopped containers,
     unused Flatpak runtimes
2. A numbered table of large personal files (path, size, modified date),
   sorted by size descending.
3. The estimated total reclaimable space.

## Phase 3 — Confirm

Two different confirmation models, exactly as designed:

### 3a. Cache groups → group-level confirmation

Use `AskUserQuestion` with **one multiSelect question** whose options are the
four groups above. Put each group's reclaimable size in the option
description. Only groups with something to reclaim should appear (if fewer
than 2 groups qualify, ask a simple yes/no style question instead).

Special sub-rules (ask these only if the relevant group was selected, and only
when applicable):

- **Docker volumes are NEVER part of the group clean.** Volumes hold real
  data. If unused volumes exist, ask about them in a separate, explicit
  question listing the volume names.
- **Orphan packages**: show the exact package list (`pacman -Qtdq`) before
  removal; if the list contains anything that looks load-bearing (drivers,
  kernel, firmware), point it out.

### 3b. Large personal files → per-file selection

Present the numbered table first, then let the user pick individual files with
`AskUserQuestion` using **multiSelect questions where each option is one
file** (label = filename + size, description = full path + modified date).
Batch by size descending: up to 4 files per question, up to 4 questions per
call (16 files per call). If there are more, handle the biggest 16 first and
ask whether to continue with the next batch. The user can always use "Other"
to type file numbers directly — accept answers like `1,3,7` or `none`.

Never preselect, never recommend deleting a personal file. Documents, photos,
videos and archives are the user's data: your job is only to surface them.

Files the scanner marks `[APP-DATA]` (they live under hidden directories:
Thunderbird mail stores, VM images, model weights, etc.) are
application-internal data, not personal documents. List them in a **separate
section with an explicit warning** that deleting them can break or wipe data
from the owning application, and exclude them from the normal selection
batches unless the user explicitly asks to include them.

## Phase 4 — Clean

Execute only what was confirmed. Per-category commands, safety notes, and
sudo requirements are documented in
[references/categories.md](references/categories.md) — read it before running
cleanup commands. Key rules:

- Use `sudo` only for the system-level operations listed there (pacman cache,
  journal vacuum, coredumps, orphan removal). The user has approved sudo use
  *after group confirmation* — the group confirmation in Phase 3 is that
  approval; don't ask again per command.
- Delete **only** the exact whitelisted cache paths from the reference file
  and the exact personal-file paths the user selected. Always quote paths and
  use `rm -rf -- "$path"` / `rm -f -- "$path"`.
- If a command fails (permission, missing tool), report it and continue with
  the remaining items — don't abort the whole cleanup.

## Phase 5 — Summary

Re-run `df -h / /home` and report, in the user's language:

- Space freed per group / per file category
- Total freed (before/after comparison of `df`)
- Anything skipped or failed, and why
- Optional gentle suggestions for next time (e.g. enable `paccache.timer`,
  `journald` SystemMaxUse) — suggestions only, don't apply them unasked.

## Hard safety rules (override everything else)

- **Scan phase never deletes.** No exceptions.
- Never delete: dotfile *configs* (`~/.config`, `~/.ssh`, `~/.gnupg`),
  browser *profiles*, `/etc`, package databases (`/var/lib/pacman`), Docker
  *volumes* without their own explicit confirmation, or anything under a
  `.git` directory.
- Never run `rm` with a glob or a variable that could expand to `$HOME`, `/`,
  or an empty string. Verify each target exists and is the expected type
  (file vs directory) before removing it.
- Keep at least one cached version of installed packages (`paccache -rk1`) —
  full cache wipe (`-rk0`) only if the user explicitly asks for it.
- If the user cancels or answers "none" at any confirmation, skip that
  category silently and move on.
