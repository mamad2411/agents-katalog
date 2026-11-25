---
name: macos-screenshots-folder-split
description: >-
  Domain composer — convenience wrapper around onedrive-flat-folder-split-by-size
  with macOS screenshot and screen recording filename defaults and patterns.
category: File-Management
---

# macOS Screenshots Folder Split (v1) — Domain Composer

This is a **domain composer** skill. It wraps the generic
[`onedrive-flat-folder-split-by-size`](../onedrive-flat-folder-split-by-size/SKILL.md)
composer with macOS-specific defaults:

- **Screenshot pattern**: `Screenshot YYYY-MM-DD at HH.MM.SS.png` (and the
  `1` duplicate suffix variant).
- **Recording pattern**: `Screen Recording YYYY-MM-DD at HH.MM.SS.mov`.
- **Two-pass pipeline**: PNG screenshots and MOV recordings are processed
  in separate passes, then a combined summary is printed.
- **Regex**: `(20\d{2}-\d{2})` extracts YYYY-MM from both patterns.
- **Default threshold**: 5000 files (OneDrive web preview limit).

The skill does NOT re-implement any logic — it shells out to
`onedrive-flat-folder-split-by-size` which in turn composes the three
base skills.

***

## Composition Rationale

This skill is a thin domain composer — it does NOT reimplement threshold
checking, batch moves, or JSON grouping. It shells out to
[`onedrive-flat-folder-split-by-size`](../onedrive-flat-folder-split-by-size/SKILL.md)
with macOS-specific glob patterns and the YYYY-MM date regex.

The composer's value-add over calling `onedrive-flat-folder-split-by-size`
directly:

- Hard-coded knowledge of macOS screenshot and recording filename formats.
- Two-pass execution (PNG + MOV) with a single composite summary.
- Correct regex for the YYYY-MM capture from both filename variants.
- Automatic handling of the `1` duplicate suffix edge case
  (`Screenshot ... 1.png`).

***

## Description

### In scope

- Accept a directory path (the macOS Screenshots folder).
- Run the OneDrive flat-folder split pipeline twice:
  1. `--glob "Screenshot*.png"` with date-extraction regex.
  2. `--glob "Screen Recording*.mov"` with date-extraction regex.
- Print a combined summary (files processed, moved, errors).
- Support `--dry-run` and `--threshold` passthrough.

### Out of scope

- Non-macOS screenshot sources (Windows Snipping Tool, Android screenshots,
  etc.) — those need their own glob+regex via the generic composer.
- Subfolder recursion — screenshots are assumed to be in a flat folder.
- File content processing — metadata-only.

***

## 1. Environment & Dependencies

### 1.1 Runtime

- **Python 3.12+** — standard library only (`argparse`, `json`, `os`,
  `subprocess`, `sys`). No external packages.

  ```bash
  python3 --version  # Must be >= 3.12
  ```

### 1.2 Required Upstream Skill

The following composer skill must exist at the expected relative path
(resolved from this script's own directory):

| Skill | Script Path |
| :--- | :--- |
| `onedrive-flat-folder-split-by-size` | `../../onedrive-flat-folder-split-by-size/scripts/split-flat-folder.py` |

This script verifies the path exists at startup and exits 1 with a clear
diagnostic if it is missing.

### 1.3 Verification

  ```bash
  python3 -c 'import sys; assert sys.version_info >= (3, 12), "Python 3.12+ required"; print("OK")'
  ```

***

## 2. CLI Contract

Located at [`scripts/split-screenshots.py`](./scripts/split-screenshots.py).

```bash
python3 .agents/skills/macos-screenshots-folder-split/scripts/split-screenshots.py \
    --directory "/path/to/Screenshots" \
    [--threshold 5000] \
    [--dry-run]
```

### 2.1 Arguments

| Argument | Required | Default | Purpose |
| :--- | :--- | :--- | :--- |
| `--directory` | Yes | — | Path to the macOS Screenshots folder. |
| `--threshold` | No | 5000 | Max files per output subfolder (passthrough to upstream). |
| `--dry-run` | No | — | Report only; do not move files (passthrough to upstream). |

### 2.2 Output

Progress output goes to stderr; JSON result arrays go to stdout:

```json
[
  {"abspath": "/path/Screenshot 2025-11-14 at 20.42.45.png", "key": "2025-11", "status": "moved", "error": null}
]
```

### 2.3 Exit Codes

| Code | Meaning |
| :--- | :--- |
| 0 | All passes completed successfully (or dry-run finished). |
| 1 | Directory not found, upstream script missing, or any pass failed. |

***

## 3. Protocol

### 3.1 Step 1 — Verify Environment

```bash
python3 --version
```

### 3.2 Step 2 — Run a Dry-Run First

```bash
python3 .agents/skills/macos-screenshots-folder-split/scripts/split-screenshots.py \
    --directory "/Users/me/Library/CloudStorage/OneDrive/Backups/Macbook-Air-Screenshots" \
    --dry-run
```

Review the per-group counts for both screenshots and recordings.

### 3.3 Step 3 — Execute

```bash
python3 .agents/skills/macos-screenshots-folder-split/scripts/split-screenshots.py \
    --directory "/Users/me/Library/CloudStorage/OneDrive/Backups/Macbook-Air-Screenshots"
```

### 3.4 Step 4 — Verify

```bash
ls "/path/to/Screenshots/2025-11/" | head -5
ls "/path/to/Screenshots/2025-12/" | head -5
```

***

## 4. macOS Filename Patterns

The script handles these macOS screenshot naming conventions:

| Pattern | Example | Key |
| :--- | :--- | :--- |
| Screenshot + date | `Screenshot 2025-11-14 at 20.42.45.png` | `2025-11` |
| Screenshot + date (duplicate) | `Screenshot 2025-11-14 at 20.42.45 1.png` | `2025-11` |
| Screen Recording | `Screen Recording 2025-12-05 at 22.05.29.mov` | `2025-12` |
| Screen Recording (duplicate) | `Screen Recording 2025-12-05 at 22.05.29 1.mov` | `2025-12` |

The regex `(20\d{2}-\d{2})` captures YYYY-MM from all variants. The glob
patterns `Screenshot*.png` and `Screen Recording*.mov` filter by type.

***

## 5. Prohibited Actions

- The Agent MUST NOT re-implement the OneDrive split pipeline inline.
- The Agent MUST NOT open source files for reading (triggers OneDrive
  download).
- The Agent MUST NOT skip dry-run before live execution.
- The Agent MUST NOT use this skill for non-macOS screenshot folders.

***

## 6. Related Skills

- [`onedrive-flat-folder-split-by-size`](../onedrive-flat-folder-split-by-size/SKILL.md) —
  upstream composer that this skill wraps with macOS defaults.
- [`file-glob-sort-by-regex-capture`](../file-glob-sort-by-regex-capture/SKILL.md) —
  upstream base used by the pipeline for file listing and key extraction.
- [`json-group-stats`](../json-group-stats/SKILL.md) — upstream base for
  per-group threshold checking.
- [`json-batch-file-move`](../json-batch-file-move/SKILL.md) — downstream
  base for batch file moves.
