---
name: vscode-bookmarks-merge
description: >-
  Base — merge two .vscode/bookmarks.json files: merge by file path,
  deduplicate by (line, column), sort bookmarks by line, sort file entries
  by path. Domain-agnostic JSON merge primitive.
category: VS Code / IDE Configuration
---

# VS Code Bookmarks Merge Skill (v1)

> **Skill ID:** `vscode-bookmarks-merge`<br>
> **Version:** 1.0.0<br>
> **Standard:** [Agent Skills (agentskills.io)](https://agentskills.io)

## Composition Rationale

This skill is a **base skill**: it owns a single generic primitive — merging
two VS Code `.vscode/bookmarks.json` files by file path, deduplicating
bookmarks by (line, column), sorting bookmarks by line, and sorting file
entries by path. The layering test (*"Could a different domain ever need the
same merge-and-dedupe-by-path primitive?"*) is YES: cross-repo bookmark
migration, bookmark consolidation across workspace splits, team bookmark
sync, and similar JSON-structured file merges all need this shape.

Known composers and consumers:

- [`vscode-bookmarks-cross-repo-migrate`](../vscode-bookmarks-cross-repo-migrate/SKILL.md) —
  discovers moved files across repos, remaps paths, then shells out to this
  skill's script to perform the actual merge.

Bidirectional discoverability: the composer links back here in its
`## Composition Rationale` section.

## Description

### In scope

- Read two `.vscode/bookmarks.json` files from disk.
- Merge entries by `path`: if the same file path exists in both source and
  target, combine their `bookmarks` arrays.
- Deduplicate bookmarks by (line, column): two bookmarks on the same line
  and column are considered identical.
- Sort bookmarks by line number (ascending), then by column (ascending).
- Sort file entries by `path` (alphabetical, case-insensitive).
- Write the merged result to stdout as a valid `.vscode/bookmarks.json`
  document.
- Support `--dry-run` flag to print the merged result without writing.

### Out of scope

- Path remapping or relocation — use the composer skill instead.
- Detecting whether referenced files still exist on disk — pure JSON merge.
- Cleaning up the source file after merge — handled by the composer.
- Any bookmark format other than the VS Code `bookmarks.json` schema
  (`{"files": [{"path": "...", "bookmarks": [...]}]}`).

## When to Apply

Apply this skill when:

- You have two `.vscode/bookmarks.json` files and need to merge them.
- You are migrating bookmarks from one repo to another and have already
  determined the new paths.
- You need to consolidate bookmarks from multiple workspaces.
- You are splitting a repo and need to keep only the relevant bookmarks.

Do NOT apply when:

- You need path remapping (use the composer instead).
- The JSON format is different from VS Code's bookmark schema.
- You just need to edit a single bookmark file directly.

## Prerequisites

| Requirement | Minimum |
|---|---|
| Python | 3.12+ |

---

## 1. Environment & Dependencies

### 1.1 Runtime

- **Python 3.12+** — standard library only (`json`, `sys`, `argparse`,
  `pathlib`). No external packages.

  ```bash
  python3 --version  # Must be >= 3.12
  ```

### 1.2 Verification

  ```bash
  python3 -c 'import sys; assert sys.version_info >= (3, 12), "Python 3.12+ required"; print("OK")'
  ```

---

## 2. CLI Contract

Located at [`scripts/merge-bookmarks.py`](./scripts/merge-bookmarks.py).

```bash
python3 .agents/skills/vscode-bookmarks-merge/scripts/merge-bookmarks.py \
    --source <source-bookmarks.json> \
    --target <target-bookmarks.json> \
    [--output <output.json>] \
    [--dry-run]
```

### 2.1 Arguments

| Argument | Required | Default | Purpose |
| :--- | :--- | :--- | :--- |
| `--source` | Yes | — | Path to the source bookmarks JSON file (entries to merge FROM). |
| `--target` | Yes | — | Path to the target bookmarks JSON file (entries to merge INTO). |
| `--output` | No | stdout | Path to write the merged result. |
| `--dry-run` | No | — | Print merged result to stdout only (no file written). |

### 2.2 Input Format

Both files must follow the VS Code `.vscode/bookmarks.json` format:

```json
{
  "files": [
    {
      "path": "some/file.md",
      "bookmarks": [
        {"line": 10, "column": 0, "label": "some label"}
      ]
    }
  ]
}
```

### 2.3 Output Format

Same schema as input. The merged result contains:

- All file entries from both source and target.
- For entries with the same `path`: combined `bookmarks` arrays, deduplicated
  by (line, column), sorted by line (ascending), column (ascending).
- File entries sorted alphabetically by `path` (case-insensitive).

### 2.4 Exit Codes

| Code | Meaning |
| :--- | :--- |
| 0 | Merge completed successfully. |
| 1 | Input parsing error (invalid JSON, missing fields). |
| 2 | Source or target file not found. |

---

## 3. Protocol

### 3.1 Step 1 — Verify Environment

```bash
python3 --version
```

### 3.2 Step 2 — Dry-Run Merge

```bash
python3 .agents/skills/vscode-bookmarks-merge/scripts/merge-bookmarks.py \
    --source /path/to/source/bookmarks.json \
    --target /path/to/target/bookmarks.json \
    --dry-run
```

Review the output to confirm the merge looks correct.

### 3.3 Step 3 — Execute Merge

```bash
python3 .agents/skills/vscode-bookmarks-merge/scripts/merge-bookmarks.py \
    --source /path/to/source/bookmarks.json \
    --target /path/to/target/bookmarks.json \
    --output /path/to/target/bookmarks.json
```

### 3.4 Step 4 — Verify Result

```bash
python3 -c "
import json
with open('/path/to/target/bookmarks.json') as f:
    data = json.load(f)
print(f'{len(data[\"files\"])} file entries, {sum(len(e[\"bookmarks\"]) for e in data[\"files\"])} total bookmarks')
"
```

---

## 4. Merge Logic (Detailed)

### 4.1 Algorithm

1. Parse both JSON files into dictionaries.
2. Build a lookup map keyed by `path` (lowercase for case-insensitive match)
   from the target file's `files` array.
3. For each entry in the source file:
   - If the path already exists in the target lookup, append the source
     entry's bookmarks to the target entry's bookmarks.
   - If the path is new, add the entire source entry to the merged list.
4. Deduplicate each entry's bookmarks: two bookmarks are duplicates if they
   share the same `line` and `column` values. The first occurrence is kept;
   subsequent duplicates are discarded.
5. Sort bookmarks by `line` (ascending), then `column` (ascending).
6. Sort file entries by `path` (case-insensitive alphabetical).
7. Output the merged result.

### 4.2 Deduplication Rule

- Two bookmarks are identical iff they have the same `line` AND `column`.
- The `label` field is NOT considered during deduplication — if two bookmarks
  are on the same line and column but have different labels, the first
  (from target, then source) is kept.

---

## 5. Edge Cases & Constraints

- **Missing `files` key**: If either file lacks a `files` key, treat it as
  an empty array.
- **Empty bookmarks array**: Entries with an empty `bookmarks` array are
  preserved in the output (they may be intentional placeholders).
- **Missing bookmark fields**: If a bookmark is missing `line` or `column`,
  it is included but not deduplicable (every such bookmark is kept).
- **---dry-run vs --output exclusive**: If `--dry-run` is set, `--output` is
  ignored.

---

## 6. Prohibited Actions

- The Agent MUST NOT re-implement the merge-dedupe-sort algorithm inline when
  this skill is available — the script is the SSOT.
- The Agent MUST NOT modify source or target files directly — only the
  script's `--output` or `--dry-run` mechanisms write output.
- The Agent MUST NOT add, remove, or alter bookmark `label` values — the
  merge is structural only.

---

## 7. Script Reference

[`scripts/merge-bookmarks.py`](./scripts/merge-bookmarks.py) performs:

1. Parse `--source`, `--target`, `--output`, `--dry-run` via `argparse`.
2. Read and parse both JSON files.
3. Validate the `{"files": [...]}` schema (tolerate missing `files` key).
4. Build a path-keyed dict from target entries (case-insensitive key).
5. Iterate source entries: merge bookmarks into matching target entry or
   add as new entry.
6. Deduplicate bookmarks within each entry by (line, column).
7. Sort bookmarks by (line, column) and file entries by path.
8. Emit the merged result to stdout or `--output` path.

---

## 8. Composition by Higher-Level Skills

| Composer Skill | Composition Mechanism |
| :--- | :--- |
| [`vscode-bookmarks-cross-repo-migrate`](../vscode-bookmarks-cross-repo-migrate/SKILL.md) | Shells out to `scripts/merge-bookmarks.py` with `--source` and `--target` after discovering and remapping paths; consumes the merged JSON from stdout or the written output file. |

---

## Related Skills

- [`vscode-bookmarks-cross-repo-migrate`](../vscode-bookmarks-cross-repo-migrate/SKILL.md) —
  composer that handles path remapping and cross-repo discovery.
- [`json-deep-sort`](../json-deep-sort/SKILL.md) — alternative if you need
  deep key-sorting of arbitrary JSON rather than the specific bookmarks
  schema.
- [`json-diff-cli`](../json-diff-cli/SKILL.md) — for diffing two bookmark
  files before deciding to merge.
- [`json-content-compare-ignore-keys`](../json-content-compare-ignore-keys/SKILL.md) —
  compare bookmark files while ignoring path or label variations.

---

## 10. Traceability

- **Created**: 2026-07-14
- **Source**: cross-repo VS Code bookmark migration from `oleovista-acers` to `ai-suite`.
- **Design rationale**: The merge primitive was extracted as a base skill
  because the same merge-by-path + deduplicate-by-(line,column) algorithm
  is needed whenever two bookmark files need consolidation, regardless of
  the remapping domain.
