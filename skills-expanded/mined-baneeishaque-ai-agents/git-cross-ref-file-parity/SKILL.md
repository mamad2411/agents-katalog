---
name: git-cross-ref-file-parity
description: Compare the diff introduced for a specific file by any two git refs (commit vs stash, commit vs commit, stash vs stash) and report IDENTICAL or DIFFERENT with a diff-of-diffs on divergence.
category: Git & Repository Management
---

# Git Cross-Ref File Parity Skill (v1)

> **Skill ID:** `git-cross-ref-file-parity`<br>
> **Version:** 1.0.0<br>
> **Standard:** [Agent Skills (agentskills.io)](https://agentskills.io)

## Description

Given two git refs of potentially different types (commit SHA, stash, branch
tip), extract the diff each ref introduces for a specific file and compare them
byte-for-byte. Reports **IDENTICAL** or **DIFFERENT**; on divergence prints a
unified diff-of-diffs so the caller can immediately see what changed.

### Canonical use case

> "I have a commit and a stash. Both touch `AGENTS.md`. Are the changes the same?"

```bash
python3 .agents/skills/git-cross-ref-file-parity/scripts/compare-file-diff.py \
    --repo   /path/to/repo \
    --commit 5612f696278fbf78e00517bbd792ff5c34d2508e \
    --stash  before-nginx-on-agents-md \
    --file   AGENTS.md
```

## When to Apply

- Verifying a stash can be safely dropped because a commit already captured
  its changes to a specific file.
- Confirming two branches introduce identical changes to a shared config file.
- Auditing whether a cherry-pick reproduced exactly the same file delta as the
  original commit.
- Any parity question of the form "do ref A and ref B make the same change to
  file X?"

Do NOT apply when:
- You need a full commit metadata audit → use
  [`git-commit-comparison-audit`](../git-commit-comparison-audit/SKILL.md).
- You need to classify or dispose of stashes → use
  [`git-stash-triage`](../git-stash-triage/SKILL.md).

## Prerequisites

| Requirement | Verification |
| :--- | :--- |
| Git 2.x+ | `git --version` |
| Python 3.9+ | `python3 --version` |
| Script present | `ls .agents/skills/git-cross-ref-file-parity/scripts/compare-file-diff.py` |

---

## Operational Logic

### Step 1 — Gather inputs

Collect from the user:

| Input | Example |
| :--- | :--- |
| Repository path | `/Users/<user>/lab-data/my-repo` |
| Commit SHA or ref | `5612f696278fbf78e00517bbd792ff5c34d2508e` |
| Stash ref or human name | `before-nginx-on-agents-md` or `stash@{2}` |
| File path (repo-relative) | `AGENTS.md` |

If either side is not a stash, use `--ref-a` / `--ref-b` instead of
`--commit` / `--stash`.

### Step 2 — Run the script

```bash
# Commit vs stash (most common):
python3 .agents/skills/git-cross-ref-file-parity/scripts/compare-file-diff.py \
    --repo   <repo-path> \
    --commit <SHA> \
    --stash  <stash-name-or-ref> \
    --file   <file-path>

# Two commits / branches:
python3 .agents/skills/git-cross-ref-file-parity/scripts/compare-file-diff.py \
    --repo  <repo-path> \
    --ref-a <sha-or-branch-A> \
    --ref-b <sha-or-branch-B> \
    --file  <file-path>

# Always show raw diffs (useful for manual inspection):
python3 ... --show-diff
```

### Step 3 — Interpret output

| Result | Meaning | Recommended action |
| :--- | :--- | :--- |
| ✅ IDENTICAL | Both refs introduce the exact same change to the file | Stash can be safely dropped (if stash-vs-commit); cherry-pick verified |
| ❌ DIFFERENT | Diffs diverge | Inspect the diff-of-diffs output; decide which side to keep |

On **DIFFERENT**: the script prints a unified diff of side-A's normalised diff
vs side-B's normalised diff, making it easy to spot added/removed lines.

### Step 4 — Act on result

- **IDENTICAL + commit already merged**: offer to drop the stash via
  [`git-stash-triage`](../git-stash-triage/SKILL.md) (never auto-drop).
- **DIFFERENT**: present the divergence to the user before any destructive action.

---

## Ref Resolution Rules

| `--` argument | Base ref | Tip ref | Rationale |
| :--- | :--- | :--- | :--- |
| `--commit <SHA>` | `<SHA>^` | `<SHA>` | Standard parent-to-child diff |
| `--stash <ref>` | `stash^1` | `stash^0` | Stash base is the commit before `git stash push` |
| `--ref-a` / `--ref-b` | `<ref>^` | `<ref>` | Same as commit |

**Stash name resolution**: if `--stash` is not a `stash@{N}` pattern, the
script scans `git stash list` for the first entry containing the given string
and uses its `stash@{N}` ref. An unambiguous substring of the stash message
is sufficient (e.g., `before-nginx`).

---

## Script Reference

### `scripts/compare-file-diff.py`

| Flag | Required | Description |
| :--- | :--- | :--- |
| `--repo DIR` | No (default `.`) | Repository root |
| `--file PATH` | **Yes** | File path relative to repo root |
| `--commit SHA` | Pair A | Commit SHA or ref |
| `--stash REF-OR-NAME` | Pair A | Stash ref or human name |
| `--ref-a REF` | Pair B | First generic ref |
| `--ref-b REF` | Pair B | Second generic ref |
| `--show-diff` | No | Always print both raw diffs |

**Exit codes**: `0` = IDENTICAL · `1` = DIFFERENT · `2` = Error

---

## Related Skills

| Skill | When to use instead |
| :--- | :--- |
| [`git-commit-comparison-audit`](../git-commit-comparison-audit/SKILL.md) | Full commit metadata + Why/What narrative across all files |
| [`git-stash-triage`](../git-stash-triage/SKILL.md) | Classify, inspect, and dispose of stashes |
| [`git-commit-metadata-extraction`](../git-commit-metadata-extraction/SKILL.md) | Extract full commit metadata as a primitive |
| [`git-ref-content-audit`](../git-ref-content-audit/SKILL.md) | Bulk per-file *content* parity across every file in a ref (including a stash's untracked tree) — answers "is Ref-A fully superseded by Ref-B?" rather than "do A and B introduce the same single-file delta?" |
