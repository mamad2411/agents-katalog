---
name: git-clean-filter-renormalize-backfill
description: Industrial protocol for backfilling stored Git blobs through a newly-installed clean filter via `git add --renormalize`, with a true-byte-drift guard that excludes only files whose working-tree content has actually changed (not files showing phantom-modified after filter install).
category: Git-Hygiene
---

# Git Clean-Filter Renormalize Backfill (v1)

When a Git clean filter is added AFTER files matching its `.gitattributes`
pattern were already committed, the previously-stored blobs were never run
through the filter. They remain in their pre-filter form (typically minified
JSON, mixed line-endings, non-canonical formatting) until each file is
touched again.

The fix is `git add --renormalize -- <pathspec>`, which re-runs the clean
filter on every tracked file matching the pathspec and re-stages the result.
This skill wraps that mechanic with the **two guardrails** that make it safe
to perform as a single atomic backfill commit:

1. **True-byte-drift detection** — files whose working-tree content has
   actually changed are EXCLUDED from the batch. Status `M` from
   `git status` is NOT sufficient: when the clean filter is freshly
   installed, every matching file appears modified because
   `clean(working_tree) != stored_blob`. Only files whose raw working-tree
   bytes differ from the index blob are truly dirty.
2. **Post-backfill audit** — verify every targeted blob is now in its
   post-filter form. The audit is filter-agnostic; the default heuristic
   (line count >= 3) is tuned for the JSON-pretty case and is overridable.

***

## 1. When to use this skill

- Right after installing any new clean filter (jq-pretty, prettier, secret
  scrub, LFS migration, line-ending normalization, etc.) where existing
  tracked content predates the filter.
- After migrating a `.gitattributes` to a stricter encoding / formatting
  policy.
- After fixing a buggy clean filter — `git add --renormalize` re-applies the
  corrected version.

## 2. Environment & Dependencies

- `git` >= 2.25 (for `--pathspec-from-file` / `--pathspec-file-nul`).
- `python3` >= 3.12 (stdlib only — no external packages).
- The clean filter itself must already be configured and reachable from this
  repository (`git config --get filter.<name>.clean`). This skill does NOT
  install filters; it only backfills.

## 3. Operational Logic

### 3.1 Pre-flight

- Stage a safety stash via
  [`git-pre-execution-safety-stash`](../git-pre-execution-safety-stash/SKILL.md).
- Confirm the filter exists: `git config --get filter.<name>.clean`.
- Confirm `.gitattributes` lists at least one pattern matched to that filter.

### 3.2 Audit BEFORE

Run [`scripts/audit_filtered_blobs.py`](scripts/audit_filtered_blobs.py)
with the same pathspec(s) as in `.gitattributes`. Record the
`pretty / minified` counts as the baseline.

### 3.3 Renormalize

[`scripts/renormalize_filtered_files.py`](scripts/renormalize_filtered_files.py)
enumerates tracked matches, compares raw working-tree bytes to the index
blob, skips true-drift files, runs `git add --renormalize` on the remainder
via `--pathspec-from-file=- --pathspec-file-nul`.

### 3.4 Commit (atomic, formatting-only)

Per [`git-atomic-commit-construction`](../git-atomic-commit-construction/SKILL.md):
the staged change MUST contain ONLY blob renormalization — no content edits.
This is why §3.3's dirty-skip guard is mandatory.

### 3.5 Audit AFTER

Re-run `audit_filtered_blobs.py`. The `minified` count should drop to the
number of files skipped in §3.3. Those will be picked up automatically on
their next normal `git add` (once their live edits are committed).

### 3.6 Stash restoration & drop

`git stash apply`, audit, then drop only after confirming no content was lost.

***

## 4. Scripts

| Script | Purpose | Tier |
| --- | --- | --- |
| [`scripts/renormalize_filtered_files.py`](scripts/renormalize_filtered_files.py) | True-byte-drift-guarded `git add --renormalize` driver | Python 3.12+ stdlib |
| [`scripts/audit_filtered_blobs.py`](scripts/audit_filtered_blobs.py) | Per-pattern pretty/minified blob-line classifier | Python 3.12+ stdlib |

Both ship executable; stdlib only. Per
[`scripting-language-selection-rules.md`](../../../ai-agent-rules/scripting-language-selection-rules.md)
Section 1, Python 3.12+ is the Tier 1 default.

## 5. Composition by Higher-Level Skills

| Composer | Domain |
| --- | --- |
| [`git-jq-pretty-json-filter`](../git-jq-pretty-json-filter/SKILL.md) | Pretty-printing minified JSON via a `jq` clean filter |

Any future filter-installation skill (LFS migration, prettier,
secret-scrub, line-ending normalization) SHOULD compose this skill for
backfill rather than reimplementing the renormalize + dirty-skip + audit
triad.

## 6. SSOT Compliance

- Atomic-commit discipline: [`git-atomic-commit-construction`](../git-atomic-commit-construction/SKILL.md).
- Safety-stash discipline: [`git-pre-execution-safety-stash`](../git-pre-execution-safety-stash/SKILL.md).
- Scripting tier: [`scripting-language-selection-rules.md`](../../../ai-agent-rules/scripting-language-selection-rules.md).
- Script-over-instruction: [`script-over-instruction-decomposition`](../script-over-instruction-decomposition/SKILL.md).

## 7. Traceability

Originated in a session on a private VS Code configurations repository
where ~545 JSON files had been committed minified before the jq-pretty
filter was installed. The true-byte-drift guard emerged as a correction
to a v0 design that used `git status --porcelain` and would have skipped
100% of files (filter install marks every matching file as
phantom-modified).
