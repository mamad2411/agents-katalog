---
name: maintaining-github-repos
description: >-
  Use when answering org-level or repo-level GitHub maintenance questions about
  repository inventory, branch health, PR backlog, or safe cleanup follow-up.
argument-hint: "org|repo|branches|prs|cleanup"
disable-model-invocation: true
---

# Maintaining GitHub Repos

This is a prompt-driven reference skill. Use it to surface GitHub maintenance signals and safe follow-up actions without forcing a single workflow.

## When to Use

Trigger conditions:

- User asks for org-level repository hygiene or cleanup signals
- User asks for repo-level branch inventory or stale branch checks
- User asks for repo-level PR backlog or pending-review checks
- User asks what cleanup actions are safe for repos, branches, or PRs

Not this skill:

- Does not force a single cleanup workflow or mandatory first command
- Does not assume org-wide cleanup when the user only asked about one repo
- Does not execute destructive actions without an explicit approval step

## Routing

Use the prompt to choose only the relevant reference pages:

| User intent | Reference |
| --- | --- |
| Org-wide stale, empty, scratch, archived, or high-branch-count repo signals | `references/org-level-signals.md` |
| Repo branch counts, merged vs remaining, stale branches, or branch drift | `references/repo-level-branch-signals.md` |
| Repo PR aging, review backlog, or blocked PR follow-up | `references/repo-level-pr-signals.md` |
| Repo archive/delete follow-up | `references/repo-level-actions.md` |
| Branch cleanup follow-up | `references/branch-level-actions.md` |
| PR nudges, rebase, draft, or close decisions | `references/pr-level-actions.md` |

Answer the requested subset directly. Add adjacent checks as recommendations, not as a forced sequence.

## Prompt Obligations

When the prompt supplies facts, surface the relevant signals without inventing missing data. The required repo-level signals are:

- total branch count
- merged branches vs remaining branches
- branches inactive for more than 5 days
- PRs pending for more than 48 hours

Use `gh` and `git` command patterns from the references when live inspection is needed, but keep the response prompt-driven rather than script-driven.

## Optional Helper

For org-level repo cleanup candidate analysis, the existing helper remains available:

```bash
python3 skills/maintaining-github-repos/scripts/analyze_repos.py --org accelerate-data --dry-run
```

Use it when the user wants a bulk org inventory or cleanup preview. Do not assume every invocation of this skill starts with that script.

## Live GitHub Prerequisite

For real repository review or cleanup work, require live GitHub state before answering branch or PR hygiene questions as if they are current.

- Verify that `gh` is installed before attempting GitHub inspection.
- Verify that `gh auth status` succeeds before relying on GitHub state.
- Stop and report the blocker if `gh` is missing or unauthenticated.
- Do not pretend branch or PR state is current when live GitHub inspection is unavailable.

## Safety Rails

- Repo archive/delete actions require a preview before mutation and exact-scope confirmation before `--execute`.
- Branch cleanup requires the exact local and/or remote candidate set before deletion.
- Never treat the default branch as a cleanup candidate.
- PR cleanup must account for merged, approved, blocked, and abandoned states before recommending close or draft actions.
- Inspection, counting, and signal-reporting requests do not require a fixed workflow or confirmation gate.

## Destructive Action Boundary

If the user moves from inspection into repo cleanup, keep the helper behavior explicit:

- Preview first with `--dry-run`
- Confirm the exact destructive scope
- Use only supported execution scopes from the current preview set
- Stop if the requested destructive subset is broader than the helper supports

## Dependencies

- `gh` CLI for GitHub inspection and cleanup actions
- `git` for local and remote branch state checks
- Python 3 for `skills/maintaining-github-repos/scripts/analyze_repos.py`
