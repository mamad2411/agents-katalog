---
name: pr-status
description: >-
  Report mergeability and review/CI status for GitHub pull requests in a compact
  dashboard. Use when checking whether a PR is mergeable, blocked, or ready to
  merge; when asked for "PR status", "review status", "is it mergeable", "what's
  blocking this PR", "are my PRs ready", or to check CI/check status across one
  or many PRs and repos. Read-only: does not merge, approve, or resolve comments.
---

# PR Status

Answer "where does this PR stand?" for one PR, a whole repo, or every PR you own, in a single compact readout: state, **mergeability**, **review** decision, and **CI** checks. Read-only.

Run the bundled script: it parses every ref form, queries GitHub, and prints the dashboard. It needs only `gh` (authenticated) and `jq`, and works from **any** directory (no checkout required; it always passes `--repo`).

```bash
bash scripts/pr-status.sh <ref> [<ref> ...]   # specific PRs
bash scripts/pr-status.sh --repo owner/repo   # every open PR in a repo
bash scripts/pr-status.sh --mine              # your open PRs across all repos
bash scripts/pr-status.sh --author LOGIN      # someone else's open PRs
bash scripts/pr-status.sh <ref> --comments    # also dump review summaries + inline comments
```

A `<ref>` is any of: a PR URL, `owner/repo#123`, `owner/repo/123`, or a bare `#123`/`123` (only when the cwd is that repo). Mix as many as you like in one call; combine with `--mine`/`--repo`.

## Reading the result and what to do next

The script prints a human verdict per PR. Map it to the next action, but do **not** act unless the user asked; this skill reports:

| Verdict | Means | Next step |
|---|---|---|
| `READY` / CLEAN | all gates green | mergeable now |
| `BLOCKED` | branch protection unmet (usually a required approval) | needs a reviewer to approve; offer to request reviewers or ping |
| `UNSTABLE` | a non-required check is failing/pending | inspect the named red/⏳ checks |
| `BEHIND` | base branch advanced | update/rebase the branch |
| `CONFLICTS` / DIRTY | merge conflicts | hand off to the `merge-resolver` skill |
| `DRAFT` | still a draft | mark ready first |
| `UNKNOWN` | GitHub still computing | wait a moment and re-run; do not report a conclusion |

The `checks:` line shows `N✓ N✗ N⏳`; any ✗/⏳ are listed by name so you can name what's red without a second query. The `review:` line shows the overall decision plus each reviewer's latest state.

## Branches

- **Just status** (default): run the script, summarise the table. For many PRs, lead with the headline (e.g. "3 of 4 mergeable; #315 blocked on review").
- **Status + what reviewers said**: add `--comments`. Summarise the verdicts and any change requests; if the user wants to *act on* them, hand off to the `address-review` skill (this skill only reads).

## Boundaries

- Read-only. Never merge, approve, request changes, resolve threads, or push from this skill.
- Reports the current snapshot. For "tell me when it's approved", re-run on an interval rather than claiming a future state.
- For deep per-comment triage and replies use `address-review`; for conflict resolution use `merge-resolver`; for creating/editing PRs use `github-cli`.
