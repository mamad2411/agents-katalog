---
name: "issue-operator"
description: "Create, update, deduplicate, comment on, and close GitHub issues for confirmed findings while keeping local audit logs synchronized. Use when a user asks to manage findings through GitHub issues, reconcile issue state, close resolved findings with evidence, or as part of $full-test-suite."
---

# Issue Operator

Own the GitHub issue lifecycle for confirmed findings tracked in `project-audit-findings.md`.

## Workflow

1. Read the local findings log and identify confirmed findings only.
2. Use `../_shared-project-ops/scripts/project_ops_state.py show-findings --path project-audit-findings.md` when deterministic parsing helps.
3. Prefer `python3 scripts/gh_issue_helper.py sync --repo-root . --findings-path project-audit-findings.md --report-path full-test-suite-report.md` for deterministic GitHub issue sync.
4. Search GitHub for each finding ID before creating a new issue.
5. Create or update issues using the shared template.
6. Add comments when verification or resolution state changes.
7. Close issues only after the local findings log records fix and verification evidence.

## Rules

- Never create issues for hypotheses.
- The local findings log remains the operational source of truth.
- If `gh` is unavailable, record the blocker locally and continue with local tracking.
- Merge duplicates when multiple findings map to one root cause.
- When invoked as a nested step inside `$full-test-suite`, do not run `gh_issue_helper.py sync` or direct `gh` commands yourself. Reconcile only the local findings/report state and let the outer suite `sync-issues` action own all networked GitHub synchronization.

## References

- GitHub issue template: `../_shared-project-ops/references/github-issue-template.md`
- Close comment template: `../_shared-project-ops/references/close-comment-template.md`
- Dedupe rules: `../_shared-project-ops/references/dedupe-rules.md`
- Finding format: `../_shared-project-ops/references/finding-format.md`
- State CLI: `../_shared-project-ops/references/state-cli.md`
- GH helper: `references/gh-helper.md`
