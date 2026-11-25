---
name: git-ref-content-audit
description: Bulk per-file blob-equality audit between two Git refs (commit, branch, tag, or stash including its untracked tree at stash^3) — classify every Ref-A file as IDENTICAL / DIFFERENT / MISSING against Ref-B, with a verdict line indicating full / partial / non-supersession.
category: Git & Repository Management
---

# Git Ref Content Audit Skill (v1)

> **Skill ID:** `git-ref-content-audit`<br>
> **Version:** 1.0.0<br>
> **Standard:** [Agent Skills (agentskills.io)](https://agentskills.io)

## Description

Given two Git refs `A` and `B`, enumerate every file accessible under Ref A
and classify each path against Ref B by **blob hash equality**:

| Status      | Meaning                                                       |
|-------------|---------------------------------------------------------------|
| `IDENTICAL` | Ref-A and Ref-B both have the path, blobs are byte-identical. |
| `DIFFERENT` | Both refs have the path, blobs differ.                        |
| `MISSING`   | Ref A has the path, Ref B does not.                           |

For **stash** refs, the audit automatically includes the stash's **untracked
tree** (`<stash>^3`) — without which untracked-but-stashed files would be
invisible to the comparison. This is critical for safety stashes created with
`git stash push -u`.

Produces a verdict line:

- `✅ FULLY SUPERSEDED` — zero MISSING, zero DIFFERENT
- `⚠️ PARTIALLY SUPERSEDED` — zero MISSING, ≥ 1 DIFFERENT (likely later refinements)
- `❌ NOT SUPERSEDED` — ≥ 1 MISSING (manual disposition required)

### Canonical use case

> "Before dropping a safety stash, prove every file it captured is already
> represented byte-identically in `HEAD` (or evolved with deliberate later
> refinements)."

```bash
python3 .agents/skills/git-ref-content-audit/scripts/audit-ref-content.py \
    --repo /path/to/repo \
    --stash "safety: 3-layer indent-override skill stack commits" \
    --ref-b HEAD \
    --show-diffs
```

## When to Apply

- **Safety-stash supersession check** before `git stash drop` (the
  `git-pre-execution-safety-stash` Phase 3 verify-and-release step uses
  `stash apply` no-op; this audit is a stronger per-file blob check).
- Verifying a long-lived feature branch's content has been fully absorbed
  by a successor branch before retiring the source.
- Auditing whether a cherry-pick / rebase preserved every file's content,
  not just diff parity (catches mid-flight refinements that
  patch-id parity would miss).
- Confirming a backup branch is no longer needed because every file lives
  on the canonical branch.

Do NOT apply when:
- You need **single-file diff parity** (does change A introduce the same
  delta as change B?) — use
  [`git-cross-ref-file-parity`](../git-cross-ref-file-parity/SKILL.md).
- You need **commit-level divergence** between two branches (unique
  commits, message audit) — use
  [`git-divergence-audit`](../git-divergence-audit/SKILL.md).
- You need to **triage and dispose** of unknown stashes — use
  [`git-stash-triage`](../git-stash-triage/SKILL.md); this audit can be
  invoked from inside that triage to confirm bucket-A (already-applied).

## Prerequisites

| Requirement | Minimum |
|---|---|
| Git         | 2.x+    |
| Python      | 3.9+    |
| Access      | Read access to the target repository |

## Step-by-Step Procedure

### 1. Resolve Ref A

- **Commit / branch / tag**: pass via `--ref-a <ref>`.
- **Stash by index**: pass via `--stash 0` → `stash@{0}`.
- **Stash by message substring**: pass via `--stash "<substring>"` — must
  resolve to exactly one entry (ambiguity is rejected with the full match list).

### 2. Resolve Ref B

Defaults to `HEAD`. Override with `--ref-b <ref>` for arbitrary destinations.

### 3. Enumerate Ref-A files

The script automatically:

- For commits / branches / tags: walks the full tree via `git ls-tree -r`.
- For stashes: takes the union of
  - tracked changes (`diff-tree` between the stash commit and its first parent `<stash>^1`), and
  - untracked tree (`git ls-tree -r <stash>^3`), if present.

Pass `--no-untracked` to skip the stash untracked tree (rarely needed).

### 4. Classify each path

For each enumerated path:

```text
ref_a_blob = git rev-parse <ref-a>:<path>
ref_b_blob = git rev-parse <ref-b>:<path>
```

Status: `IDENTICAL` if both hashes are 40-char and equal; `MISSING` if
`ref_b_blob` is empty; otherwise `DIFFERENT`.

### 5. Inspect divergences (optional)

Pass `--show-diffs` to print a unified `git diff <ref-a>:<path>
<ref-b>:<path>` for every `DIFFERENT` file. Use this when the verdict is
`⚠️ PARTIALLY SUPERSEDED` and you must judge whether the HEAD-side
divergence is a deliberate refinement (safe) or a missing change
(blocking).

### 6. Render verdict

The script prints a verdict line plus per-status buckets. JSON output
(`--json`) provides the same data programmatically:

```json
{
  "ref_a": "stash@{0}",
  "ref_b": "HEAD",
  "files": [
    {"path": "AGENTS.md", "status": "DIFFERENT",
     "ref_a_blob": "680dc67...", "ref_b_blob": "0a36ad7..."}
  ]
}
```

### 7. Decide disposition

| Verdict | Action |
|---|---|
| ✅ FULLY SUPERSEDED | Ref-A is safe to drop / delete after explicit user authorization (per [`git-operation-rules.md` §5](../../../ai-agent-rules/git-operation-rules.md) for stashes). |
| ⚠️ PARTIALLY SUPERSEDED | Re-run with `--show-diffs`; classify each divergence as "later refinement" (safe) or "missing change" (must re-apply). User authorization required before disposing of Ref-A. |
| ❌ NOT SUPERSEDED | Do NOT dispose of Ref-A. Promote missing files to commits (via [`git-stash-triage`](../git-stash-triage/SKILL.md) → Bucket B/C) or leave the ref in place. |

## Script Reference

`scripts/audit-ref-content.py`

| Flag | Description |
|---|---|
| `--repo` (required) | Path to the Git repository. |
| `--ref-a` *or* `--stash` (required) | Ref A: a Git ref OR a stash specifier. `--stash` accepts `stash@{N}`, a numeric index, or a message substring. |
| `--ref-b` | Ref B (default `HEAD`). |
| `--no-untracked` | When Ref-A is a stash, skip the untracked tree (`<stash>^3`). |
| `--show-diffs` | Print a unified diff for every DIFFERENT file. |
| `--json` | Emit machine-readable JSON instead of the text report. |

**Exit codes:**

| Exit | Meaning |
|---|---|
| 0    | All Ref-A paths present in Ref-B (IDENTICAL or DIFFERENT). |
| 1    | At least one Ref-A path MISSING in Ref-B. |
| 2    | Usage / git error. |

## Related Skills

- **[Git Cross-Ref File Parity](../git-cross-ref-file-parity/SKILL.md)** —
  single-file *diff* parity (does the change introduced by A match the change
  introduced by B?). This skill answers the multi-file *content* parity question
  instead.
- **[Git Pre-Execution Safety Stash](../git-pre-execution-safety-stash/SKILL.md)** —
  the canonical creator of safety stashes; recommend using this audit as a
  stronger Phase 3 verify-and-release check than `stash apply` no-op alone.
- **[Git Stash Triage](../git-stash-triage/SKILL.md)** — classifies unknown
  stashes for disposition; use this audit to confirm Bucket A (already-applied)
  via per-file blob equality before drop.
- **[Git Divergence Audit](../git-divergence-audit/SKILL.md)** — commit-level
  divergence between branches; complementary, not substitutive.

## Common Pitfalls

| Pitfall | Solution |
|---|---|
| Stash created with `-u` but untracked files appear missing in audit | The script auto-includes `<stash>^3`; ensure you didn't pass `--no-untracked`. |
| Stash name substring matches multiple stashes | Script rejects with the full match list — disambiguate by index or longer substring. |
| `DIFFERENT` files trigger drop hesitation when they are deliberate later refinements | Re-run with `--show-diffs` and judge per-file; partial supersession is normal for evolving documentation / configs. |
| Trying to audit working-tree (not a ref) | Refs only. Use `git stash push` first, then audit the stash; or commit, then audit `HEAD`. |
| Empty 0-byte placeholder files appear as `MISSING` in Ref-B | This is correct behavior — verify content via `git cat-file -s <ref-a>:<path>` to confirm the source was an unintentional empty file. |
