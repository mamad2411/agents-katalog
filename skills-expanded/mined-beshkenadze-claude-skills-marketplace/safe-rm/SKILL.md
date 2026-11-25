---
name: safe-rm
description: Use safe-rm script instead of rm -rf. Prevents accidental deletion of protected system, config, and project paths.
version: 1.0.0
---

# Safe RM

## Overview

Wrapper around `rm -rf` with safety checks. Use this instead of direct `rm -rf` commands.

## When to Use

- Deleting directories or files recursively
- Any `rm -rf` or `rm -r` operation
- Cleaning up temporary files/folders

## Usage

```bash
# Dry-run (default) - shows what would be deleted
safe-rm /path/to/delete

# Actually delete (if path is not protected)
safe-rm --force /path/to/delete
safe-rm -f /path/to/delete
```

## Protected Paths

The script blocks deletion of:

**System:** `/`, `/bin`, `/boot`, `/dev`, `/etc`, `/lib`, `/opt`, `/proc`, `/root`, `/sbin`, `/sys`, `/usr`, `/var`, `/home`, `/Users`

**Home config:** `~`, `~/.ssh`, `~/.gnupg`, `~/.config`, `~/.local`, `~/.claude`, `~/.zshrc`, `~/.bashrc`

**Project:** `.git`, git repository root

## Exit Codes

- `0` — success (or dry-run completed)
- `1` — path is protected
- `2` — path does not exist

## Instructions for Claude

1. **NEVER use `rm -rf` directly** — always use `safe-rm` script
2. Run without `--force` first to preview what will be deleted
3. If path is protected, inform user and do not proceed
4. Only use `--force` after confirming dry-run output is correct
