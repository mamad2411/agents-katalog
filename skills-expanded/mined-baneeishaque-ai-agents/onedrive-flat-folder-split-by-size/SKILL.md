---
name: onedrive-flat-folder-split-by-size
description: >-
  Composer — orchestrate glob+regex listing, group-size threshold check, and
  batch file move to split OneDrive flat folders exceeding the 5000-file
  web preview limit. Metadata-only.
category: File-Management
---

# OneDrive Flat Folder Split by Size (v1) — Composer

This is the **composer** skill. It orchestrates three atomic base skills to
split a flat folder of OneDrive-synced files into key-named subfolders,
ensuring no subfolder exceeds the OneDrive web preview limit (~5000 files).

**Metadata-only constraint**: This script NEVER opens or reads source file
content. All operations use filesystem metadata only (`os.path`, `glob`,
`shutil.move`). Reading a file in a OneDrive-synced folder triggers a cloud
download — this script avoids that entirely.

***

## Composition Rationale

This skill is a composer — it does NOT re-implement glob+regex listing,
JSON grouping, or batch file moving. It orchestrates three atomic base skills:

1. **[`file-glob-sort-by-regex-capture`](../file-glob-sort-by-regex-capture/SKILL.md)** —
   called FIRST. Shells out to its `scripts/sort-by-capture.py` with
   `--directory`, `--glob`, `--regex` to obtain a JSON Lines listing of all
   matching files with extracted keys.

2. **[`json-group-stats`](../json-group-stats/SKILL.md)** — called SECOND.
   The JSON Lines from step 1 are parsed into a JSON array and piped into
   `scripts/group-stats.py --group-by key --output counts` to compute
   per-group file counts for threshold checking.

3. **[`json-batch-file-move`](../json-batch-file-move/SKILL.md)** — called
   THIRD (unless `--dry-run`). Pipes the JSON array from step 1 into
   `scripts/batch-move-by-key.py --target-dir <directory>` to execute the
   actual file moves.

The composer's value-add over any single base: it enforces the OneDrive
5000-file web preview limit, runs a threshold pre-check with user
confirmation, supports dry-run preview, and holds the metadata-only
operating mode as a permanent invariant.

Bidirectional discoverability: all three bases list this composer in their
respective `## Composition by Higher-Level Skills` tables.

***

## Description

### In scope

- Accept a directory path, glob pattern, regex with capture group, and
  optional threshold.
- **Pipeline**: glob+regex listing → group by key → check group sizes
  against threshold → batch move into `<key>/` subfolders.
- Dry-run mode: report planned groups and sizes without moving.
- Threshold warning: flag groups at/above the limit and prompt before
  proceeding.
- Metadata-only: no file content is ever read.

### Out of scope

- Discovering or installing base scripts — the three base skills must be
  present at the expected relative paths (verified at startup).
- Recursive subdirectory traversal — controlled by the glob pattern.
- Cross-filesystem moves — `shutil.move` on the same volume is metadata-
  only; cross-volume falls back to copy+delete which reads content.

***

## 1. Environment & Dependencies

### 1.1 Runtime

- **Python 3.12+** — standard library only (`argparse`, `json`, `os`,
  `subprocess`, `sys`). No external packages.

  ```bash
  python3 --version  # Must be >= 3.12
  ```

### 1.2 Required Base Skills

The following skills must exist at the expected relative paths (they are
resolved from this script's own directory, NOT from `$PWD`):

| Base Skill | Script Path |
| :--- | :--- |
| `file-glob-sort-by-regex-capture` | `../../file-glob-sort-by-regex-capture/scripts/sort-by-capture.py` |
| `json-group-stats` | `../../json-group-stats/scripts/group-stats.py` |
| `json-batch-file-move` | `../../json-batch-file-move/scripts/batch-move-by-key.py` |

The script verifies all three paths exist at startup and exits 1 with a
clear diagnostic if any is missing.

### 1.3 Verification

  ```bash
  python3 -c 'import sys; assert sys.version_info >= (3, 12), "Python 3.12+ required"; print("OK")'
  ```

***

## 2. CLI Contract

Located at [`scripts/split-flat-folder.py`](./scripts/split-flat-folder.py).

```bash
python3 .agents/skills/onedrive-flat-folder-split-by-size/scripts/split-flat-folder.py \
    --directory "/path/to/flat/folder" \
    --glob "Screenshot*.png" \
    --regex "(20\d{2}-\d{2})" \
    [--threshold 5000] \
    [--dry-run]
```

### 2.1 Arguments

| Argument | Required | Default | Purpose |
| :--- | :--- | :--- | :--- |
| `--directory` | Yes | — | Flat folder to organize (absolute or relative path). |
| `--glob` | Yes | — | Glob pattern for target files (e.g. `Screenshot*.png`). |
| `--regex` | Yes | — | Python regex with exactly one capture group for the grouping key. |
| `--threshold` | No | 5000 | Max files per output subfolder before warning. |
| `--dry-run` | No | — | Report planned groups and sizes; do not move files. |

### 2.2 Output

The script prints progress to stderr and a JSON result array to stdout:

```json
[
  {"abspath": "/path/Screenshot 2025-11-14.png", "key": "2025-11", "status": "moved", "error": null},
  {"abspath": "/path/Screenshot 2025-12-01.png", "key": "2025-12", "status": "moved", "error": null}
]
```

### 2.3 Exit Codes

| Code | Meaning |
| :--- | :--- |
| 0 | Pipeline completed successfully (or dry-run finished). |
| 1 | Directory not found, base script missing, regex matched nothing, or pipeline failure. |

***

## 3. Protocol

### 3.1 Step 1 — Verify Environment

```bash
python3 --version
```

### 3.2 Step 2 — Run a Dry-Run First

```bash
python3 .agents/skills/onedrive-flat-folder-split-by-size/scripts/split-flat-folder.py \
    --directory "/path/to/Screenshots" \
    --glob "Screenshot*.png" \
    --regex "(20\d{2}-\d{2})" \
    --dry-run
```

Review the per-group counts. If any group is at/above 5000, consider a
more specific regex (e.g. grouping by year only, or by year-month-day).

### 3.3 Step 3 — Execute

```bash
python3 .agents/skills/onedrive-flat-folder-split-by-size/scripts/split-flat-folder.py \
    --directory "/path/to/Screenshots" \
    --glob "Screenshot*.png" \
    --regex "(20\d{2}-\d{2})"
```

### 3.4 Step 4 — Verify

```bash
ls "/path/to/Screenshots/2025-11/" | head -5
ls "/path/to/Screenshots/2025-12/" | head -5
```

***

## 4. OneDrive-Specific Mandates

These mandates are invariants of the workflow — they MUST be followed in
every invocation:

1. **Metadata-only**: The script (and all base scripts it calls) MUST NOT
   open, read, or write the content of any source file. Only `os.path`,
   `glob.glob`, `os.stat`, `os.makedirs`, and `shutil.move` are permitted.
   Opening a file for reading triggers OneDrive cloud download.

2. **5000-file threshold**: OneDrive web preview does not display folders
   with more than ~5000 items. The default `--threshold 5000` matches this
   limit. Adjust with `--threshold` if OneDrive changes the limit.

3. **Dry-run before live**: Always run with `--dry-run` first to review
   the planned group sizes before executing moves.

4. **Same-volume moves**: Ensure `--directory` and the target subfolders
   are on the same OneDrive-synced volume. Cross-volume `shutil.move`
   falls back to copy+delete, which reads file content.

***

## 5. Example Invocations

### 5.1 macOS Screenshots (PNG)

```bash
python3 .agents/skills/onedrive-flat-folder-split-by-size/scripts/split-flat-folder.py \
    --directory "/Users/me/Library/CloudStorage/OneDrive/Backups/Macbook-Air-Screenshots" \
    --glob "Screenshot*.png" \
    --regex "(20\d{2}-\d{2})" \
    --dry-run
```

### 5.2 macOS Screen Recordings (MOV)

```bash
python3 .agents/skills/onedrive-flat-folder-split-by-size/scripts/split-flat-folder.py \
    --directory "/Users/me/Library/CloudStorage/OneDrive/Backups/Macbook-Air-Screenshots" \
    --glob "Screen Recording*.mov" \
    --regex "(20\d{2}-\d{2})" \
    --dry-run
```

### 5.3 General Date-Stamped Files

```bash
python3 .agents/skills/onedrive-flat-folder-split-by-size/scripts/split-flat-folder.py \
    --directory "/path/to/downloads" \
    --glob "report-*.pdf" \
    --regex "(20\d{2}-\d{2})" \
    --threshold 5000 \
    --dry-run
```

***

## 6. Prohibited Actions

- The Agent MUST NOT re-implement any of the three base primitives inline.
- The Agent MUST NOT open source files for reading.
- The Agent MUST NOT move files across volumes for OneDrive-synced data.
- The Agent MUST NOT skip the dry-run step before live execution.
- The Agent MUST NOT exceed the OneDrive 5000-file threshold in any output
  subfolder without explicit user approval.

***

## 7. Related Skills

- [`file-glob-sort-by-regex-capture`](../file-glob-sort-by-regex-capture/SKILL.md) —
  upstream base that provides the sorted file listing with extracted keys.
- [`json-group-stats`](../json-group-stats/SKILL.md) — upstream base that
  provides per-group counts for threshold checking.
- [`json-batch-file-move`](../json-batch-file-move/SKILL.md) — downstream
  base that executes the actual file moves.
- [`macos-screenshots-folder-split`](../macos-screenshots-folder-split/SKILL.md) —
  domain-specific composer that wraps this skill with macOS screenshot
  defaults.
