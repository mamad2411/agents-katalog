---
name: json-group-stats
description: >-
  Base — group JSON objects by a specified field and emit per-group counts or
  grouped records. Domain-agnostic.
category: Data-Processing
---

# JSON Group Stats (v1) — Base Primitive

This is the **base** skill. It reads a JSON array from stdin, groups the
elements by a specified field, and emits a JSON array of per-group counts or
grouped records. The primitive is domain-agnostic — any workflow that needs
to group structured data by a key can compose this skill.

***

## Composition Rationale

This skill is a standalone base — it does NOT compose any other skill. It is
consumed by:

- [`onedrive-flat-folder-split-by-size`](../onedrive-flat-folder-split-by-size/SKILL.md) —
  shells out to `scripts/group-stats.py --group-by key --output counts` to
  compute per-group file counts for OneDrive threshold checking.

***

## Description

### In scope

- Read a JSON array from stdin (each element is a flat dict).
- Group elements by the value of a specified field.
- Emit a JSON array of `{"key": ..., "count": N}` entries (counts mode) or
  `{"key": ..., "count": N, "items": [...]}` entries (groups mode).
- Optional `--min-items` filter to exclude groups below a threshold.
- Deterministic output — groups are sorted alphabetically by key.

### Out of scope

- Recursive or nested grouping (single-level group-by only).
- Aggregation or transformation of grouped items beyond counting.
- Reading from files — stdin stream only.
- Writing to files — stdout only.

***

## 1. Environment & Dependencies

### 1.1 Runtime

- **Python 3.12+** — standard library only (`argparse`, `collections`, `json`,
  `sys`). No external packages.

  ```bash
  python3 --version  # Must be >= 3.12
  ```

### 1.2 Verification

  ```bash
  python3 -c 'import sys; assert sys.version_info >= (3, 12), "Python 3.12+ required"; print("OK")'
  ```

***

## 2. CLI Contract

Located at [`scripts/group-stats.py`](./scripts/group-stats.py).

```bash
python3 .agents/skills/json-group-stats/scripts/group-stats.py \
    --group-by key \
    [--output counts|groups] \
    [--min-items N] \
    < input.json
```

### 2.1 Arguments

| Argument | Required | Default | Purpose |
| :--- | :--- | :--- | :--- |
| `--group-by` | Yes | — | Field name to group by. |
| `--output` | No | `counts` | `counts` — emit `{"key", "count"}` per group; `groups` — emit `{"key", "count", "items"}`. |
| `--min-items` | No | None | Only include groups with ≥ N items. |

### 2.2 Output Format

**Counts mode** (`--output counts`):

```json
[
  {"key": "2025-11", "count": 273},
  {"key": "2025-12", "count": 1375}
]
```

**Groups mode** (`--output groups`):

```json
[
  {
    "key": "2025-11",
    "count": 273,
    "items": [
      {"filename": "Screenshot 2025-11-14 at 20.42.45.png", "abspath": "/path/...", "key": "2025-11"},
      ...
    ]
  }
]
```

### 2.3 Exit Codes

| Code | Meaning |
| :--- | :--- |
| 0 | Success — output written to stdout. |
| 1 | Error — empty input, invalid JSON, no matching group-by field. |

***

## 3. Protocol

### 3.1 Step 1 — Verify Environment

```bash
python3 --version
```

### 3.2 Step 2 — Run the Script

```bash
python3 .agents/skills/json-group-stats/scripts/group-stats.py \
    --group-by key \
    --output counts \
    < /tmp/files.json
```

### 3.3 Step 3 — Consume Output

Pipe the output JSON into a consuming script or redirect to a file:

```bash
python3 .agents/skills/json-group-stats/scripts/group-stats.py \
    --group-by severity \
    --output counts \
    < /tmp/log-entries.json \
    > /tmp/severity-counts.json
```

***

## 4. Edge Cases & Constraints

- **Empty input array**: The script prints an error to stderr and exits 1.
- **Non-dict elements**: Skipped with a warning on stderr.
- **Missing group-by field**: The element is skipped; a count of skipped
  elements is printed to stderr.
- **No elements match**: The script exits 1 with an error on stderr.
- **--min-items filter eliminates all groups**: The script exits 0 with an
  empty array `[]` and a note on stderr.
- **Non-string key values**: Converted to string via `str()` for grouping.
- **Large inputs**: The entire array is held in memory. For very large
  streams (>100k elements), consider splitting.

***

## 5. Prohibited Actions

- The Agent MUST NOT re-implement the group-by-count loop inline when this
  skill is available — the script is the SSOT.
- The Agent MUST NOT use this skill for recursive or multi-field grouping —
  use multiple passes if needed.
- The Agent MUST NOT modify the input data — the script is read-only.

***

## 6. Script Reference

[`scripts/group-stats.py`](./scripts/group-stats.py) performs:

1. Read stdin and parse as a JSON array.
2. Validate structure — must be a list of dicts.
3. Group by `item[--group-by]` using `defaultdict(list)`.
4. Optionally filter by `--min-items`.
5. Sort groups alphabetically by key.
6. Emit JSON array to stdout (counts or groups mode).

***

## 7. Composition by Higher-Level Skills

| Composer Skill | Composition Mechanism |
| :--- | :--- |
| [`onedrive-flat-folder-split-by-size`](../onedrive-flat-folder-split-by-size/SKILL.md) | Pipes a JSON array of file records into this script with `--group-by key --output counts` to obtain per-group file counts for OneDrive threshold checking. Consumes the counts array to determine whether any file group exceeds the 5000-file preview limit. |

***

## 8. Related Skills

- [`json-batch-file-move`](../json-batch-file-move/SKILL.md) — downstream
  consumer; takes a JSON array with abspath+key and moves files into
  subfolders named by key.
- [`file-glob-sort-by-regex-capture`](../file-glob-sort-by-regex-capture/SKILL.md) —
  upstream producer; generates JSON Lines with abspath+key that feeds into
  this skill via the OneDrive composer.
- [`onedrive-flat-folder-split-by-size`](../onedrive-flat-folder-split-by-size/SKILL.md) —
  composer that orchestrates all three bases.
