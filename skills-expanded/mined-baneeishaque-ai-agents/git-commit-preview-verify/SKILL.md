---
name: git-commit-preview-verify
description: Verify whether commits listed in a commit-preview markdown file have been executed against git history, with optional cleanup.
category: Git & Repository Management
---

# Git Commit Preview Verify Skill

> **Skill ID:** `git-commit-preview-verify`<br>
> **Version:** 1.0.0<br>
> **Standard:** [Agent Skills (agentskills.io)](https://agentskills.io)

## Description

Provides a deterministic, domain-agnostic primitive for verifying
whether the commits listed in a commit-preview markdown file have been
executed against git history. It parses the standard §2d preview format
produced by [`git-atomic-commit-construction`](../../../../git-atomic-commit-construction/SKILL.md),
cross-references each `Commit N:` title against `git log --oneline`, and
reports each arranged commit as `done` or `pending`.

The primitive supports human-readable text output and machine-readable
JSON, plus an optional `--cleanup` gate that deletes the preview file
ONLY when every listed commit is verified as executed — so a partially
executed plan never loses its handoff artifact.

## Environment & Dependencies

| Requirement | Minimum |
| --- | --- |
| Git | 2.x |
| Python | 3.10+ |

Verify:

```bash
git --version
python3 --version
```

## When to Apply

Apply this skill when:

- A user points to an existing `scratch/commit-preview.md` and asks "is
  this done?" or "check if these commits were made".
- Resuming a session that previously generated a commit preview but may
  not have executed all commits.
- Auditing whether a planned commit sequence was fully executed.
- Cleaning up a stale preview file after all commits are confirmed
  executed.

Do NOT apply when:

- The preview has not been written yet — use
  [`git-atomic-commit-construction`](../../../../git-atomic-commit-construction/SKILL.md)
  §2d to generate it first.
- The user wants to verify individual commit content — use
  [`git-commit-metadata-extraction`](../../../../git-commit-metadata-extraction/SKILL.md).
- The user wants to split or rewrite existing commits — use
  [`git-history-refinement`](../../../../git-history-refinement/SKILL.md).

## Scripts (Public CLI Contract)

The deterministic Tier-A primitive is
[`scripts/verify-commit-preview.py`](scripts/verify-commit-preview.py)
per `script-over-instruction-decomposition`. It is read-only by default
and never mutates the working tree unless `--cleanup` is passed with all
commits done.

```bash
python3 scripts/verify-commit-preview.py --preview <path> [--repo <path>] [--format text|json] [--cleanup]
```

| Flag | Meaning |
| --- | --- |
| `--preview PATH` | Path to the commit-preview markdown file (required) |
| `--repo PATH` | Git repository root (default: auto-detect from CWD) |
| `--format text\|json` | Output format (default: `text`) |
| `--window N` | `git log` window size in commits (default: 50) |
| `--cleanup` | Delete the preview file only when ALL commits are done |

### Examples

```bash
# Text report (default)
python3 scripts/verify-commit-preview.py --preview scratch/commit-preview.md

# Machine-readable JSON
python3 scripts/verify-commit-preview.py --preview scratch/commit-preview.md --format json

# Verify, then delete the preview (only fires when all commits done)
python3 scripts/verify-commit-preview.py --preview scratch/commit-preview.md --cleanup
```

### Exit Codes

| Code | Meaning |
| --- | --- |
| 0 | All commits verified as executed |
| 1 | One or more commits not found in git log |
| 2 | Preview file not found or unreadable |
| 3 | Not inside a git repository (and `--repo` not provided / invalid) |
| 4 | Preview file contains no parseable commit entries |

### Input / Output Format

The parser accepts the §2d preview's `Commit N:` section headers at any
heading level (`## Commit 1: <title>` or `### Commit 1: <title>`). For
each entry it records `{ index, title, status, sha }`. `status` is
`done` when the title matches a line of `git log --oneline -<window>`
(returning that line's SHA), otherwise `pending` with a null SHA.

Text output:

```text
Commit Preview Verification
==========================
Preview: scratch/commit-preview.md
Repository: /Users/dk/lab-data/ai-suite

 #  Status   SHA       Title
 1  done     febd2a47  docs(gists-ai-prompts): add commit preview instruction log entries

Result: 5/5 commits executed
```

JSON output:

```json
{
  "preview_file": "scratch/commit-preview.md",
  "repo": "/Users/dk/lab-data/ai-suite",
  "total": 5,
  "done": 5,
  "pending": 0,
  "commits": [
    { "index": 1, "title": "docs(gists-ai-prompts): ...", "status": "done", "sha": "febd2a47" }
  ]
}
```

### Cleanup Semantics

- `--cleanup` deletes the preview file and prints `Cleaned up: <path>`
  ONLY when `pending == 0`.
- If any commit is pending, cleanup is refused with a warning and the
  exit code is 1 — the preview MUST be retained for the next session.

## Composition by Higher-Level Skills

| Composer | Composition Mechanism |
| --- | --- |
| [`git-atomic-commit-construction`](../../../../git-atomic-commit-construction/SKILL.md) | Invoked in §2d.2 for post-execution verification of arranged commits and preview cleanup |

## Related Skills

- [`git-atomic-commit-construction`](../../../../git-atomic-commit-construction/SKILL.md)
  — the composer that generates the preview this skill verifies.
- [`git-commit-metadata-extraction`](../../../../git-commit-metadata-extraction/SKILL.md)
  — for extracting individual commit metadata.
- [`git-hunk-staging-primitives`](../../../../git-hunk-staging-primitives/SKILL.md)
  — sibling base skill for hunk-based staging during commit construction.
- [`repo-scratch-output-capture`](../../../../repo-scratch-output-capture/SKILL.md)
  — for managing the `scratch/` directory where previews live.

## Traceability

- **Created**: 2026-08-11
- **Source**: Observed workflow gap — user pointed to an existing
  `scratch/commit-preview.md`, agent verified commits manually via
  `git log`, then deleted the file; none of that was documented.
- **Extracted from**: [`git-atomic-commit-construction`](../../../../git-atomic-commit-construction/SKILL.md)
  §2d — post-execution preview verification was not documented.
