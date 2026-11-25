---
name: file-glob-sort-by-mtime
description: Base primitive — find the newest file matching a glob pattern by modification time, output JSON Lines with path, mtime, size
category: General
---

# File Glob Sort by mtime (v1)

## Scope & Intent

**In scope:**
- List files in a directory matching a glob pattern
- Sort results by modification time descending (newest first)
- Output JSON Lines with `path`, `mtime` (nanoseconds), `size` (bytes)
- Limit result count via `--limit`

**Out of scope:**
- Recursive vs non-recursive control (always recursive `rglob`)
- Symlink following (uses `Path.stat()` — does not cross symlinks)
- File content inspection or filtering

## Environment & Dependencies

| Requirement | Version | Notes |
|-------------|---------|-------|
| Python | 3.12+ | Stdlib only — no pip dependencies |

## CLI Contract

| Argument | Required | Description |
|----------|----------|-------------|
| `--dir` | Yes | Directory to search (resolved relative to CWD) |
| `--glob` | Yes | Glob pattern (e.g. `*.yaml`) |
| `--limit` | No | Max results (0 = unlimited, default) |

**Output:** JSON Lines to stdout — one JSON object per file.

**Exit codes:**
- `0` — success (may emit zero lines if no files match)
- `1` — directory not found or inaccessible

## Protocol

1. Verify `--dir` exists and is readable.
2. Run `python3 scripts/sort-by-mtime.py --dir <path> --glob <pattern> [--limit N]`
3. Consume JSON Lines output.

## Edge Cases

- **No files match**: emits zero lines, exits 0
- **Permission denied**: silently skips inaccessible files
- **Large directories**: processes all matches in memory before sorting — use `--limit` for bounded output

## Prohibited Actions

- Do NOT re-implement the sort logic in a caller script; pipe from this script instead.
- Do NOT parse unordered directory listings yourself — always use this script for mtime-based ordering.

## Script Reference

`sort-by-mtime.py`:
1. Resolves `--dir` to absolute path
2. Uses `Path.rglob(args.glob)` to find all matches recursively
3. Calls `.stat()` on each match to get `st_mtime_ns` and `st_size`
4. Sorts descending by mtime
5. Applies `--limit` if specified
6. Prints JSON Lines

## Composition by Higher-Level Skills

- `opencode-current-session-id` — uses this skill to find the newest `.yaml` file in `.opencode/logs/`

## Related Skills

- [`file-glob-sort-by-regex-capture`](../../../file-glob-sort-by-regex-capture/SKILL.md) — sibling base; sorts by regex capture instead of mtime
- [`text-lines-sort-by-length`](../../text-lines-sort-by-length/SKILL.md) — sorts text lines by length (different domain, same pattern)
- [`opencode-installed-plugin-lookup`](../../opencode/opencode-installed-plugin-lookup/SKILL.md) — related — plugin registry probe; may order log files from the logger convention
