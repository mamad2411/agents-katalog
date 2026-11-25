---
name: decodie-verify
description: >-
  Verify that learning entries still match the source code they reference.
  Resolves content-based anchors, stamps confirmed entries with the current
  commit SHA, and marks mismatches as stale. Use to maintain entry accuracy
  after code changes.
license: MIT
metadata:
  author: owenbush
  version: "1.0"
---

# Decodie — Verify Mode

Confirm that every learning entry in `.decodie/index.json` still matches the source code it references, mark mismatches as stale, and stamp confirmed entries with the current commit SHA.

This mode **modifies `.decodie/index.json` only**. It never modifies session files, source code, or anything outside `.decodie/`.

## Activation

Parse the optional path argument:
- If no path provided, verify **all entries**.
- If a path is provided, verify only entries whose `sources` (or `references[].file`) overlap that path. For a directory, an entry is in scope if any source file starts with that directory.
- If the path does not exist, report the error and stop.

## Setup

1. Confirm `.decodie/` exists. If not: "No `.decodie/` directory found — nothing to verify." Stop.
2. Read `.decodie/index.json`. If empty: "No entries to verify." Stop.
3. Determine **current commit SHA**:
   ```bash
   git rev-parse HEAD
   ```
   If not a git repo, warn and continue (anchor checks still run, but `verified_sha` cannot be set).

## Verification Process

For each entry in scope:

1. **Resolve source files.** Prefer `sources`; fall back to unique `references[].file` values. If falling back, **backfill** the `sources` field.

2. **Check each reference** `{ file, anchor, anchor_hash }`:
   - File missing → reference fails.
   - File exists → search for literal `anchor` string. If found, recompute SHA-256 hash and confirm first 8 hex chars match `anchor_hash`.

3. **Decide outcome:**
   - All references resolve → `stale: false`, `verified_sha` = HEAD SHA.
   - Any reference fails → `stale: true`, leave `verified_sha` unchanged.

4. **Write back** to `index.json`. Preserve all other fields and sort order.

## Reporting

```
Decodie verify
  Verified:  N entries (verified_sha -> <short-sha>)
  Stale:     M entries
  Skipped:   K entries (out of scope)
  Backfilled sources on: B entries
```

If stale entries exist, list them:

```
Stale entries:
  - entry-1711540000-a1b2 -- references/0: src/lib/foo.ts (anchor not found)
  - entry-1711540123-c3d4 -- references/1: src/lib/bar.ts (file missing)
```

## Important Notes

- **Append-only for entry content.** Only `sources`, `verified_sha`, and `stale` may be updated.
- **Idempotent.** Running twice with no changes is a no-op.
- **Path is a filter.** Out-of-scope entries are skipped, not cleared.
- **No git history rewriting.** Only reads HEAD via `git rev-parse`.
