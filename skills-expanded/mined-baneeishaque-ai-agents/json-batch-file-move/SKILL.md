---
name: json-batch-file-move
description: >-
  Base — read a JSON array (abspath+key), move files into subfolders named
  by key. Domain-agnostic, metadata-only, no file reads.
category: File-Management
---

# JSON Batch File Move (v1) — Base Primitive

This is the **base** skill. It reads a JSON array from stdin where each
element carries an `abspath` (absolute path to an existing file) and a `key`
(subfolder name). It groups entries by key, creates subdirectories named
after each key, and moves files into their respective folders. The primitive
is domain-agnostic — any workflow that needs to batch-move files according
to a JSON manifest can compose this skill.

**Metadata-only constraint**: The script NEVER opens or reads file content.
Only `os.path.exists`, `os.makedirs`, and `shutil.move` are used. This is
essential for OneDrive-synced folders where read operations trigger download.

***

## Composition Rationale

This skill is a standalone base — it does NOT compose any other skill. It is
consumed by:

- [`onedrive-flat-folder-split-by-size`](../onedrive-flat-folder-split-by-size/SKILL.md) —
  shells out to `scripts/batch-move-by-key.py --target-dir <directory>` and
  pipes a JSON array of file records (abspath+key) via stdin to execute the
  actual file moves.

***

## Description

### In scope

- Read a JSON array from stdin; each element is a dict with `abspath` (str)
  and `key` (str).
- Group entries by `key`.
- Create `key/` subdirectories under a parent target directory.
- Move each file into its respective subdirectory.
- Emit a JSON array of result objects (status per file).
- Support `--dry-run` mode for safe preview.
- Metadata-only — no file content is ever read.

### Out of scope

- Discovering files or extracting keys — the JSON manifest is supplied
  externally (see `file-glob-sort-by-regex-capture` for discovery).
- Sorting or filtering the input — pass-through grouping only.
- Deleting or modifying source files in any way other than `shutil.move`.
- Cross-filesystem moves — `shutil.move` within the same volume is
  metadata-only.

***

## 1. Environment & Dependencies

### 1.1 Runtime

- **Python 3.12+** — standard library only (`argparse`, `collections`, `json`,
  `os`, `shutil`, `sys`). No external packages.

  ```bash
  python3 --version  # Must be >= 3.12
  ```

### 1.2 Verification

  ```bash
  python3 -c 'import sys; assert sys.version_info >= (3, 12), "Python 3.12+ required"; print("OK")'
  ```

***

## 2. CLI Contract

Located at [`scripts/batch-move-by-key.py`](./scripts/batch-move-by-key.py).

```bash
python3 .agents/skills/json-batch-file-move/scripts/batch-move-by-key.py \
    [--target-dir DIR] \
    [--dry-run] \
    < input.json
```

### 2.1 Arguments

| Argument | Required | Default | Purpose |
| :--- | :--- | :--- | :--- |
| `--target-dir` | No | Current working directory | Parent directory under which key subfolders are created. |
| `--dry-run` | No | — | Log planned moves to stderr; do not execute any moves. |

### 2.2 Input Format

A JSON array where each element has:

| Field | Type | Required | Description |
| :--- | :--- | :--- | :--- |
| `abspath` | string | Yes | Absolute path to an existing file. |
| `key` | string | Yes | Subfolder name to move the file into. |

```json
[
  {"abspath": "/path/Screenshot 2025-11-14.png", "key": "2025-11"},
  {"abspath": "/path/Screenshot 2025-12-01.png", "key": "2025-12"}
]
```

### 2.3 Output Format

A JSON array of result objects:

```json
[
  {"abspath": "/path/Screenshot 2025-11-14.png", "key": "2025-11", "status": "moved", "error": null},
  {"abspath": "/path/Screenshot 2025-12-01.png", "key": "2025-12", "status": "moved", "error": null},
  {"abspath": "/path/missing.png", "key": "2025-11", "status": "error", "error": "file does not exist"}
]
```

### 2.4 Exit Codes

| Code | Meaning |
| :--- | :--- |
| 0 | All input entries processed (individual file errors may still exist). |
| 1 | Input parsing failure, target directory missing, or no valid entries. |

***

## 3. Protocol

### 3.1 Step 1 — Verify Environment

```bash
python3 --version
```

### 3.2 Step 2 — Prepare the JSON Manifest

Produce a JSON array with `abspath` and `key` fields (e.g. via
`file-glob-sort-by-regex-capture`):

```bash
python3 .agents/skills/file-glob-sort-by-regex-capture/scripts/sort-by-capture.py \
    --directory "/path/to/files" \
    --glob "*.png" \
    --regex "(2025-\d{2})" \
    > /tmp/manifest.jsonl
```

### 3.3 Step 3 — Run the Move

```bash
# Dry-run first
python3 .agents/skills/json-batch-file-move/scripts/batch-move-by-key.py \
    --target-dir "/path/to/files" \
    --dry-run \
    < /tmp/manifest.json

# Live
python3 .agents/skills/json-batch-file-move/scripts/batch-move-by-key.py \
    --target-dir "/path/to/files" \
    < /tmp/manifest.json
```

### 3.4 Step 4 — Verify Results

Check that files were moved into the expected subdirectories:

```bash
ls "/path/to/files/2025-11/" | head -5
ls "/path/to/files/2025-12/" | head -5
```

***

## 4. Edge Cases & Constraints

- **Missing field**: Entries without `abspath` or `key` are recorded as
  errors in the output but do not halt processing.
- **Non-existent file**: If `os.path.exists(abspath)` returns false, the
  entry is recorded as an error and skipped.
- **Existing destination**: `shutil.move` overwrites the destination if
  a file of the same name already exists in the target folder.
- **--dry-run mode**: Logs each planned `mv` to stderr; output JSON has
  `"status": "dry-run"` for each entry.
- **Cross-volume moves**: `shutil.move` falls back to copy+delete when
  source and destination are on different filesystems, which DOES read
  file content. For OneDrive-synced folders, ensure target-dir is on the
  same volume as the source files.

***

## 5. Prohibited Actions

- The Agent MUST NOT re-implement the group-by-key + batch-move loop inline
  when this skill is available — the script is the SSOT.
- The Agent MUST NOT open or read source file content — only `os.path` and
  `shutil.move` are permitted.
- The Agent MUST NOT use this skill to move files across volumes for
  OneDrive-synced data (triggers content read via copy+delete fallback).

***

## 6. Script Reference

[`scripts/batch-move-by-key.py`](./scripts/batch-move-by-key.py) performs:

1. Parse `--target-dir` and `--dry-run`.
2. Read stdin as a JSON array; validate each element for `abspath` and `key`.
3. Group valid entries by `key` using `defaultdict(list)`.
4. For each group: `os.makedirs(key_dir, exist_ok=True)`.
5. For each file: `shutil.move(abspath, dest)`.
6. Emit a JSON array of result objects to stdout.

***

## 7. Composition by Higher-Level Skills

| Composer Skill | Composition Mechanism |
| :--- | :--- |
| [`onedrive-flat-folder-split-by-size`](../onedrive-flat-folder-split-by-size/SKILL.md) | Pipes a JSON array of file records (abspath+key) into this script with `--target-dir <directory>` to execute the actual file-to-subfolder moves in a OneDrive flat-folder split. |

***

## 8. Related Skills

- [`json-group-stats`](../json-group-stats/SKILL.md) — upstream pre-check;
  groups by key and counts before this script runs.
- [`file-glob-sort-by-regex-capture`](../file-glob-sort-by-regex-capture/SKILL.md) —
  upstream producer that generates the JSON manifest consumed by this skill.
- [`onedrive-flat-folder-split-by-size`](../onedrive-flat-folder-split-by-size/SKILL.md) —
  composer that orchestrates the full pipeline.
