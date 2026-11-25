---
name: decodie-flag-stale
description: >-
  Fast CI-friendly check for entries whose source files have changed since last
  verification. Compares entry source files against git diff without reading
  source code. Flags stale entries in index.json. Use in CI pipelines or before
  releases to detect outdated documentation.
license: MIT
metadata:
  author: owenbush
  version: "1.0"
---

# Decodie — Flag Stale Mode

Fast, CI-friendly counterpart to verify mode. For every entry with a `verified_sha`, check whether any of its source files have changed since that SHA, and flip `stale: true` on entries that have. Does not read source files or recompute anchor hashes — only diffs filenames against git history.

This mode **modifies `.decodie/index.json` only**.

## Activation

Takes no arguments. Always operates on the full index.

## Setup

1. Confirm `.decodie/` exists. If not: "No `.decodie/` directory found — nothing to check." Stop.
2. Confirm git repository:
   ```bash
   git rev-parse --git-dir
   ```
   If not: "Not a git repository — `flag-stale` requires git history. Run verify mode instead." Stop.
3. Read `.decodie/index.json`. If empty: "No entries to check." Stop.

## Detection Process

For each entry:

1. **Skip entries with no `verified_sha`.** Report as `unverified`.
2. **Skip entries with no `sources`** (and no `references[].file` fallback). Report as `no-sources`.
3. **Compute changed files:**
   ```bash
   git diff --name-only <verified_sha>..HEAD
   ```
   If the SHA is unknown to git (history rewritten), treat as stale.
4. **Compare** changed files against entry's source files. If any match, the entry is stale.
5. **Update:**
   - Newly stale → set `stale: true`. Leave `verified_sha` unchanged.
   - Already stale → no change (still counted).
   - No source files in diff → leave `stale` as-is. Do **not** flip stale back to fresh — only verify mode can do that.

Write updates back to `index.json`.

## Reporting

```
Decodie flag-stale
  Newly stale:  N entries
  Already stale: M entries
  Fresh:        F entries
  Unverified:   U entries (no verified_sha -- run verify mode)
  No sources:   K entries
```

If newly stale, list them:

```
Newly stale:
  - entry-1711540000-a1b2 -- src/lib/foo.ts
  - entry-1711540123-c3d4 -- src/lib/bar.ts, src/lib/baz.ts
```

## Important Notes

- **One-way flag.** Only flips `stale` to `true`. Clearing requires verify mode.
- **No source file reads.** Based purely on `git diff --name-only`. This is what makes it fast enough for CI.
- **No exit-code policy.** Whether stale entries block a PR is a per-repo decision.
- **No git history rewriting.** Only read-only git commands.
