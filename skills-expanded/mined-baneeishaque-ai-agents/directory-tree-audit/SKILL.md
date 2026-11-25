---
name: directory-tree-audit
description: >-
  Recursively audits a directory tree, counts items per folder, and flags those
  exceeding a configurable threshold — provides the raw structural data for
  organization decisions.
category: General-Utility
---

# Directory Tree Audit (v1)

A domain-agnostic base skill that walks a directory tree, counts direct children
per folder, and flags folders whose item count exceeds a configurable threshold.
Produces deterministic JSON output consumed by higher-level composer skills
(e.g., the 8±2 human-scanability principle).

***

## Composition Rationale

This skill owns a single reusable primitive: **recursive directory item
counting**. It was extracted as its own base skill because the deterministic
"walk + count + threshold" operation is reused by multiple domains — cleanup
audits, backup scope analysis, and migration tools. Inlining this logic into
any single domain skill would split the SSOT and force each consumer to
maintain its own copy.

***

## 1. Environment & Dependencies

- **Python 3.12+** — required runtime. Standard library only (`os`, `json`,
  `argparse`, `sys`). No `pip` dependencies.
- **Verify**: `python3 --version` (must show ≥3.12).

***

## 2. Protocol

1. **Identify the target directory** — the root from which to walk.
2. **Choose a threshold** — the item count above which a folder is considered
   "overstuffed." Default: 10.
3. **Run the audit script**:

   ```bash
   python3 .agents/skills/general/directory-tree-audit/scripts/audit-folder-depths.py \
       --root <target-dir> \
       --threshold 10 \
       --json
   ```

4. **Consume the JSON output** — each entry reports the folder's path, item
   count, sub-directory count, file count, and a `flagged` boolean.
5. **Interpret flagged entries** — folders with `flagged: true` exceed the
   threshold and may need sub-grouping (delegated to a composer skill).

***

## 3. Script Reference

**`scripts/audit-folder-depths.py`** — the sole script in this skill.

| Argument | Required | Default | Description |
| :--- | :--- | :--- | :--- |
| `--root` | Yes | — | Root directory to audit (absolute or relative path). |
| `--threshold` | No | `10` | Item count threshold for `flagged`. |
| `--json` | No | `true` | Output format (always JSON; flag present for explicitness). |

**Exit codes**:

- `0` — success, valid JSON written to stdout.
- `1` — error (root not found / not a directory), error JSON written to stdout.

**Output schema** (stdout):

```json
[
  {
    "path": "/relative/path",
    "item_count": 12,
    "dir_count": 3,
    "file_count": 9,
    "flagged": true
  }
]
```

Empty tree → `[]`. Single-folder root → single-entry array.

**Error output**:

```json
{"error": "root not found or not a directory: <path>"}
```
