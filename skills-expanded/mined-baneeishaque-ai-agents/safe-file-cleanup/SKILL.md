---
name: safe-file-cleanup
description: Base primitive — safely remove files and directories using the system trash/recycle bin when available, with verification and exit-code contract.
category: General
---

# safe-file-cleanup (v1)

> **Name:** safe-file-cleanup<br>
> **Description:** Base primitive — safely remove files/directories via system trash when available, with verification
and exit-code contract.<br>
> **Category:** General

## Description

Generic base primitive for removing files and directories from disk.
When a trash/recycle-bin command is available, paths are moved there instead
of being permanently deleted. The primitive verifies removal and reports
per-path status via JSON Lines.

## Composition Rationale

This skill is a standalone base primitive. It does not compose any other
skill. It is consumed by:

- [`opencode-session-log-cleanup`](../../../opencode/opencode-session-log-cleanup/SKILL.md) — shells out to
`scripts/safe_cleanup.py` with discovered session-log paths; consumes the exit code and per-path JSON Lines output to
confirm cleanup.

## Related Skills

- [`file-glob-sort-by-mtime`](../file-glob-sort-by-mtime/SKILL.md) — sibling base primitive for mtime-ordered file
discovery.

## Environment & Dependencies

| Requirement | Version | Notes |
| ------------- | --------- | ------- |
| Python | 3.12+ | Stdlib only — no pip dependencies |
| `trash` CLI | any | Optional but preferred on macOS; install via `brew install trash` or `npm install -g trash-cli` |
| `gio` CLI | any | Optional alternative on Linux GVFS desktops |

## CLI Contract

| Argument | Required | Description |
| ---------- | ---------- | ------------- |
| `paths` | Yes | One or more files or directories to remove |
| `--remove-empty-parents` | No | Remove empty parent directories after successful deletions |
| `--json` | No | Emit JSON Lines output |

**Output:** JSON Lines to stdout — one object per path with keys `path`,
`status` (`removed`, `skipped`, `failed`), and `message`.

*Exit codes:*

- `0` — all paths removed successfully
- `1` — partial failure (some removed, some failed)
- `2` — complete failure (no paths removed)

## Protocol

1. Resolve each `path` argument to an absolute path.
2. Detect an available trash command (`trash`, then `gio`).
3. For each path:
   - If it does not exist, emit `skipped`.
   - Otherwise, attempt removal via the detected trash command (or stdlib
     fallback when no trash command is available).
   - Verify the path no longer exists.
   - Emit `removed` or `failed` with a descriptive message.
4. If `--remove-empty-parents` is set and any path was removed, walk up
   from each removed path and delete empty directories until a non-empty
   ancestor is encountered.
5. Set the exit code per the contract above.

## Edge Cases

- **No trash command available**: falls back to `os.remove` /
  `shutil.rmtree`. A message indicating the fallback is emitted per path.
- **Path does not exist**: emitted as `skipped`; does not affect the exit
  code.
- **Permission denied**: emitted as `failed`; contributes to partial or
  complete failure.
- **Parent removal race**: `os.rmdir` failures during
  `--remove-empty-parents` are silently swallowed — a non-empty or
  concurrently-created parent is not an error.

## Script Reference

`scripts/safe_cleanup.py`:

1. Parses `paths`, `--remove-empty-parents`, and `--json` via `argparse`.
2. Calls `find_trash_command()` to prefer `trash`, then `gio`.
3. Iterates paths, calling `remove_path()` and `verify_removed()`.
4. Optionally calls `remove_empty_parents()`.
5. Prints JSON Lines or human-readable lines and exits with the contract
   exit code.

## Composition by Higher-Level Skills

| Composer | Composition Mechanism |
| --- | --- |
| [`opencode-session-log-cleanup`](../../../opencode/opencode-session-log-cleanup/SKILL.md) | Calls `scripts/safe_cleanup.py <paths> [--remove-empty-parents]`; consumes exit code and JSON Lines output to confirm cleanup. |
