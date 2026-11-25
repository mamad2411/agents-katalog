---
name: json-diff-leaf
description: Generic recursive leaf-value diff of two JSON files. Outputs deterministic, machine-readable JSON change list.
category: Base-Primitive
---

# JSON Diff Leaf — Base Primitive

> **Skill ID:** `json-diff-leaf`<br>
> **Version:** 1.0.0<br>
> **Standard:** [Agent Skills (agentskills.io)](https://agentskills.io)

## Description

A domain-agnostic base primitive that recursively compares two JSON files and outputs a structured JSON array of every
leaf-value difference. It detects **added**, **removed**, **changed**, **type-changed**, and **reordered** values. Array
comparisons use set semantics (order-independent) — only genuine additions/removals are reported; pure reordering is
flagged separately.

Output is pure machine-readable JSON — no human-friendly formatting, timestamp heuristics, or conclusions. Those belong
in the `json-diff-cli` composer.

## Composition Rationale

This skill owns exactly one operation: "read two JSON files, walk their structure recursively, and report every leaf-
value difference as a structured change object." The recursive leaf-walk + diff algorithm is a generic primitive that
multiple domains could reuse — schema validators, config watchers, TOML/YAML comparison tools (after parsing to dict),
and the `json-diff-cli` composer.

Known composers that depend on this base skill's public contract (stdout JSON array, integer exit code):

| Composer | Composition Mechanism |
| --- | --- |
| [`json-diff-cli`](../json-diff-cli/SKILL.md) | Calls `scripts/json-diff-leaf.py --file1 <a> --file2 <b>` via subprocess; consumes the JSON array stdout to produce human-readable formatted output with timestamp formatting, set-based list diff, and a conclusion. |

## Environment & Dependencies

| Requirement | Minimum |
| --- | --- |
| Python | 3.11+ (stdlib only: `json`, `argparse`, `pathlib`, `typing`) |
| OS | Linux, macOS, Windows |

No external packages required.

## Script Reference

### `scripts/json-diff-leaf.py`

The single executable script packaged with this skill.

**Usage:**

```bash
python3 scripts/json-diff-leaf.py \
  --file1 <path> \
  --file2 <path>
```

**Output:** A JSON array printed to stdout. Each element is a change object:

```json
{"path": "a.b.c", "kind": "added|removed|changed|type-changed|reordered",
 "old_value": …, "new_value": …}
```

The `path` field uses dot-separated keys (e.g., `chrome.storage.local.whitelist`). Array indices are NOT tracked — array
changes are reported at the array's path with set semantics.

**Exit codes:**

| Code | Meaning |
| --- | --- |
| 0 | Success (differences may or may not exist) |
| 1 | Error (file not found, invalid JSON, etc.) |

**Change kinds:**

| Kind | Meaning | Fields populated |
| --- | --- | --- |
| `added` | Key exists only in file 2 | `new_value` |
| `removed` | Key exists only in file 1 | `old_value` |
| `changed` | Scalar value differs | `old_value`, `new_value` |
| `type-changed` | Value type differs (e.g., string → number) | `old_value` (type name), `new_value` (type name) |
| `reordered` | Array items are the same set but different order | `old_value`, `new_value` |

## Verification

```bash
echo '{"a":1,"b":[1,2]}' > /tmp/_left.json
echo '{"a":2,"b":[2,1]}' > /tmp/_right.json
python3 scripts/json-diff-leaf.py --file1 /tmp/_left.json --file2 /tmp/_right.json
```

Expected output — two change objects: `a` changed from 1 to 2, `b` reordered:

```json
[
  {"path": "a", "kind": "changed", "old_value": 1, "new_value": 2},
  {"path": "b", "kind": "reordered", "old_value": [1, 2], "new_value": [2, 1]}
]
```

## Composition by Higher-Level Skills

| Composer | Composition Mechanism |
| --- | --- |
| [`json-diff-cli`](../json-diff-cli/SKILL.md) | Calls `scripts/json-diff-leaf.py --file1 <a> --file2 <b>` via `subprocess.run`; consumes the JSON array stdout for human-readable enrichment. |

## Related Skills

| Skill | Relationship |
| --- | --- |
| [`json-content-compare-ignore-keys`](../json-content-compare-ignore-keys/SKILL.md) | Hash-based JSON snapshot comparison with key-ignore support — complementary use case (pass/fail gate vs. exploratory diff). |
| [`json-deep-sort`](../json-deep-sort/SKILL.md) | Sorts JSON arrays and dict keys in-place — useful as a pre-normalization step before feeding JSON into this diff primitive. |
