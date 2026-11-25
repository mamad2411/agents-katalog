---
name: json-content-compare-ignore-keys
description: Compare JSON file content while ignoring specified keys
    (e.g., auto-timestamps). Outputs deterministic hash of sorted,
    filtered JSON. Exit 0 = matches stored snapshot, 1 = mismatch.
category: Base-Primitive
---

# JSON Content Compare Ignore Keys — Base Primitive

> **Skill ID:** `json-content-compare-ignore-keys`<br>
> **Version:** 1.0.0<br>
> **Standard:** [Agent Skills (agentskills.io)](https://agentskills.io)

## Description

A generic, domain-agnostic primitive for comparing a JSON file against a
stored baseline while ignoring specified keys (e.g., auto-timestamps,
nonces, machine-specific paths). On first invocation it computes and stores
a snapshot. On subsequent invocations it compares the current file's
(ignored-keys-removed, sorted) hash against the snapshot and exits
**0 = MATCH** (only ignored keys changed or nothing changed) or
**1 = MISMATCH** (structural / semantic change detected).

Deterministic, idempotent, stdin-free by design — operates on one file
path per invocation so compositors can call it in a loop.

## Composition Rationale

This skill is a **standalone base primitive**. It owns exactly one
operation: "read JSON, strip keys, hash, compare." Any domain that needs
to distinguish trivial auto-timestamp churn from real content changes
in a JSON config file can compose this skill.

Known composers that depend on this skill's public contract (stdout hash
line, integer exit code):

| Composer | Invocation Pattern |
| --- | --- |
| [`claude-config-change-gate`](../claude-config-change-gate/SKILL.md) | `python3 .../json-content-compare-ignore-keys.py --file known_marketplaces.json --ignore-keys lastUpdated` |

## Environment

| Requirement | Minimum |
| --- | --- |
| Python | 3.12+ (stdlib only: `json`, `hashlib`, `argparse`, `pathlib`) |
| OS | Linux, macOS, Windows (POSIX shell not required — direct Python invocation) |

## Script Reference

### `scripts/json-content-compare-ignore-keys.py`

The single executable script packaged with this skill.

**Usage:**

```bash
python3 json-content-compare-ignore-keys.py \
  --file <path> \
  --ignore-keys <key> [--ignore-keys <key2> ...] \
  [--snapshot-dir <dir>]
```

| Argument | Required | Default | Description |
| --- | --- | --- | --- |
| `--file <path>` | Yes | — | Path to the JSON file to compare |
| `--ignore-keys <key>` | No | `[]` | Key name(s) to remove before hashing (repeatable) |
| `--snapshot-dir <dir>` | No | parent of `--file` | Where to store / read the `.snapshot` file |

**Exit codes:**

| Code | Meaning |
| --- | --- |
| 0 | MATCH — hash equals stored snapshot (only ignored keys differ or nothing changed) |
| 1 | MISMATCH — hash differs from stored snapshot (structural / semantic change) |

**First-run behavior:** If no `.snapshot` file exists, the script stores
the current (ignored-keys-removed, sorted) hash and exits 0. This seeds
the baseline.

**Snapshot format:** Single line containing the 64-character SHA-256 hex
digest, followed by `\n`.

## Related Skills

| Skill | Relationship |
| --- | --- |
| [`json-deep-sort`](../json-deep-sort/SKILL.md) | Sorts JSON arrays and dict keys in-place — complementary if the input JSON needs pre-normalization before this comparator runs. |
| [`git-jq-pretty-json-filter`](../git-jq-pretty-json-filter/SKILL.md) | Installs a `jq`-based pretty-print clean filter — useful when the JSON file is minified on disk. |

## Verification

Confirm the script exits correctly on MATCH vs MISMATCH:

```bash
# Create two structurally identical files differing only by ignored key
echo '{"a":1,"t":"2024-01-01"}' > /tmp/_a.json
echo '{"a":1,"t":"2024-06-13"}' > /tmp/_b.json

# First run — seeds snapshot
python3 scripts/json-content-compare-ignore-keys.py \
  --file /tmp/_a.json --ignore-keys t \
  && echo "exit 0 (seeded)" || echo "exit 1"

# Second run — same structure, different timestamp → MATCH
python3 scripts/json-content-compare-ignore-keys.py \
  --file /tmp/_b.json --ignore-keys t \
  && echo "exit 0 (MATCH)" || echo "exit 1 (MISMATCH)"

# Third run — different value → MISMATCH
echo '{"a":2,"t":"2024-06-13"}' > /tmp/_c.json
python3 scripts/json-content-compare-ignore-keys.py \
  --file /tmp/_c.json --ignore-keys t \
  && echo "exit 0 (MATCH)" || echo "exit 1 (MISMATCH)"
```

Expected output: first two exit 0, third exits 1.
