---
name: json-diff-cli
description: Human-readable JSON leaf diff with timestamp formatting, set-based list diff, and summary conclusion. Composes the json-diff-leaf base primitive.
category: Data Processing
---

# JSON Diff CLI — Composer

> **Skill ID:** `json-diff-cli`<br>
> **Version:** 1.0.0<br>
> **Standard:** [Agent Skills (agentskills.io)](https://agentskills.io)

## Description

A human-readable CLI for comparing two JSON files. Calls the [`json-diff-leaf`](../json-diff-leaf/SKILL.md) base
primitive to obtain the structured diff, then enriches the output with:

- **Timestamp formatting** — epoch-millisecond values are converted to human-readable UTC dates (e.g., `2025-12-14
12:11:22 UTC`) so you can instantly see which file is newer.
- **Set-based list diff** — array items are compared as sets; only the added and removed elements are shown as a bullet
list, not the entire array. Pure reordering is flagged separately.
- **File attribution** — every change is tagged with `[filename]` so you know exactly which side the addition/removal
belongs to.
- **Conclusion** — a summary sentence describing the overall relationship (superset, subset) and flagging which file has
the newer timestamp.

## Composition Rationale

This skill is a **composer**: it does NOT re-implement recursive leaf-value diff logic. It delegates the structured
comparison entirely to the [`json-diff-leaf`](../json-diff-leaf/SKILL.md) base primitive. The domain-specific value this
composer adds is:

1. **Human-readable output formatting** — the base outputs machine JSON; this skill renders it for a terminal user.
2. **Timestamp heuristics** — detecting epoch-ms timestamps by path name and rendering them as dates.
3. **Set-based list presentation** — showing only added/removed items as a clean bullet list instead of raw JSON arrays.
4. **Summary conclusion** — computing superset/subset relationships and timestamp ordering.

The base script is resolved via a relative path anchored to the composer's own location (`$(dirname)/../../json-diff-
leaf/scripts/json-diff-leaf.py`), ensuring the pipeline works regardless of the caller's `cwd`.

## Environment & Dependencies

| Requirement | Minimum |
| --- | --- |
| Python | 3.11+ (stdlib only: `json`, `subprocess`, `argparse`, `datetime`, `pathlib`, `typing`) |
| Base skill | [`json-diff-leaf`](../json-diff-leaf/SKILL.md) must be present at the expected relative path |
| OS | Linux, macOS, Windows |

No external packages required.

## Script Reference

### `scripts/json-diff-cli.py`

**Usage:**

```bash
python3 scripts/json-diff-cli.py <file1> <file2>
```

Both arguments are positional paths to JSON files.

**Exit codes:**

| Code | Meaning |
| --- | --- |
| 0 | Success (files may be identical or differ) |
| 1 | Error (missing base script, file not found, invalid JSON, base subprocess failure) |

**Output example:**

```text
CHANGED  chrome.storage.local.last-update
  [file1.json] 1765714282850 (2025-12-14 12:11:22 UTC)
  [file2.json] 1781679716289 (2026-06-17 07:01:56 UTC)

ADDED  chrome.storage.local.whitelist
  [file2.json] added items:
    - github.com
    - www.figma.com
    - app.zoom.us

─── CONCLUSION ───
file2.json has 1 key(s) added (chrome.storage.local.whitelist); 1 value(s) changed (chrome.storage.local.last-update). file2.json is a superset of file1.json. (chrome.storage.local.last-update: file2.json is newer — 1781679716289 (2026-06-17 07:01:56 UTC) > 1765714282850 (2025-12-14 12:11:22 UTC))
```

## Verification

```bash
echo '{"a":1,"t":1765714282850}' > /tmp/_old.json
echo '{"a":2,"t":1781679716289,"b":"new"}' > /tmp/_new.json
python3 scripts/json-diff-cli.py /tmp/_old.json /tmp/_new.json
```

## Related Skills

| Skill | Relationship |
| --- | --- |
| [`json-diff-leaf`](../json-diff-leaf/SKILL.md) | Base primitive — this composer shells out to its script for the structured diff. |
| [`json-content-compare-ignore-keys`](../json-content-compare-ignore-keys/SKILL.md) | Hash-based snapshot comparison (complementary use case: pass/fail gate vs. exploratory diff). |
| [`json-deep-sort`](../json-deep-sort/SKILL.md) | Pre-normalization step before diffing. |
| [`folder-comparison`](../folder-comparison/SKILL.md) | Directory-level comparison — broader scope, less depth-per-file. |
| [`near-duplicate-file-comparison`](../near-duplicate-file-comparison/SKILL.md) | Eight-dimension forensic rubric for source file comparison. |
