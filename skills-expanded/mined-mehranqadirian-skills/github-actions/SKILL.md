---
name: github-actions
description: Writes, reviews and debugs GitHub Actions workflows. Use whenever the user edits a file under .github/workflows, asks to set up CI or deployment on GitHub, wants to speed up or secure a pipeline, sees a workflow fail or never start, or asks about permissions, secrets, caching, matrices or pull_request_target, even if they only say "add CI to my repo". Lints workflows for script injection, unpinned actions and broad permissions before suggesting changes.
---

# github-actions

Write CI that is fast, least-privilege and hard to abuse. The linter is line based and dependency free, so it runs anywhere, including Termux.

```
github-actions/
├── SKILL.md
├── scripts/
│   └── lint_workflow.py      script injection, pull_request_target, permissions, unpinned actions, leaks
└── references/
    └── hardening.md          safe starter workflow, injection fix, pinning, secrets, speed, debugging
```

## When to use

- Creating a first workflow for tests, lint, build or release
- Reviewing a workflow before merging, especially from a fork
- A workflow is slow, flaky, never triggers or fails only in CI
- Questions about permissions, secrets, OIDC, caching, matrices

## Workflow

1. **Lint first**: `python3 scripts/lint_workflow.py .github/workflows` (a file or a folder). Errors must be fixed; warnings are likely risks; add `--strict` to fail on warnings.
2. **Fix by severity**: script injection and `pull_request_target` with a PR checkout first, then moving-branch actions, then missing `permissions:`, then pinning and timeouts.
3. **Use the starter** in `references/hardening.md` when creating a workflow: least-privilege `permissions`, `concurrency`, `timeout-minutes`, dependency cache.
4. **Explain each change** briefly with its reason, for example: "titles are attacker-controlled text, so they go through `env:`".
5. **For failures**, ask for the failing step's log, the trigger event and the branch, then use the debugging list in the reference. Typical causes: wrong path, YAML indentation, missing tool on the runner, secret not available to forks.
6. **Verify**: a workflow cannot be fully tested locally. Say so, suggest pushing to a branch and reading the run, and name what would confirm success.

## Rules

- Never put untrusted `github.event.*` fields directly into `run:`; route them through `env:`
- Never run untrusted pull request code under `pull_request_target`
- Default to `permissions: contents: read` and grant more per job
- Pin third-party actions to a commit SHA; follow moving branches never
- Do not print secrets, and rotate any that appeared in logs
- A push that changes workflow files needs a token with the `workflow` scope; if the push is rejected for that reason, run `gh auth refresh -s workflow`

## What to report back

| Field | Content |
|-------|---------|
| Findings | rule, line, severity, why it matters |
| Changed workflow | diff or full file with comments on the key changes |
| Not verified | behavior only visible in a real run |
| Follow ups | Dependabot for actions, environments with reviewers, OIDC |

## Related skills

- `docker-basics`: container builds and image scanning in CI
- `secrets-hygiene`: scan the repo for credentials in CI
- `code-review`: review the change that touches the pipeline
