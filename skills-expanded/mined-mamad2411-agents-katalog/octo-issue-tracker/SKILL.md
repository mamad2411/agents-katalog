---
name: octo-issue-tracker
description: Use this skill to triage GitHub issues — surface stale issues, propose labels, identify blockers, list PRs awaiting review, and draft responses. Triggers on "issues", "backlog", "triage", "PRs to review", "stale".
---

# octo-issue-tracker — triage GitHub issues

You help track and triage GitHub issues for this project.

When invoked, use the GitHub MCP server if available (fall back to `gh issue list` / `gh pr list` via Bash). Then report:

1. **Stale issues** — open for 30+ days with no activity. Suggest: close as stale, ping owner, or re-prioritize.
2. **Untriaged** — issues with no labels and no assignee. Suggest concrete labels based on title/body.
3. **Blockers** — labeled `blocker` / `release-blocker` / similar. Surface owner and current status.
4. **PRs awaiting review** — open >24h with no review activity. List reviewers who could unblock.
5. **Conflicting work** — issues/PRs touching the same files (use GitHub's PR file lists).

For each item, propose **one concrete next action** (close, label, ping <user>, draft a response, request review from <user>). Never close issues or merge PRs without explicit user confirmation. Quote the issue/PR URL in every recommendation so the user can act in one click.

## OCTO-### IDs

To cross-reference with the `scenario-tester` skill, maintain an `.octo/ISSUES.md` file at the repo root mapping each tracked issue to a stable local ID:

```markdown
# OCTO Issues

## OCTO-001 — [bug] Payment retry double-debits
GitHub: https://github.com/owner/repo/issues/42
Status: open · Severity: high · Linked test: tests/scenarios/payment-flow.md#S4

## OCTO-002 — [feat] CSV import for users
GitHub: https://github.com/owner/repo/issues/57
Status: in-progress · Severity: medium
```

When `scenario-tester` requests issue creation for a failing test, create the entry here with a new OCTO-### ID and (if the GitHub MCP is configured) create the corresponding GitHub issue.
