---
name: deploy-state
description: |
  Infiquetra deployment state and tag-promotion guidance. Use for /deploy, /deploy-status,
  /deploy-notes, /deploy-hotfix, rollback planning, hotfix promotion, and deployment evidence.
---

# Deploy State

Use this skill for Infiquetra repository deployment work. It is intentionally separate from
`saga` because deployment mutation deserves a hard boundary.

## Source Of Truth

- Link to the Infiquetra context library instead of copying long-lived policy text.
- Search the context library for ADR-0004 before changing deployment behavior.
- Also reference the current CI/CD standards and repository-local workflow files under
  `.github/workflows/`.
- If the target repository does not resolve to `github.com/infiquetra/*`, stop before mutation.

## Environments

Infiquetra tag-promotion environments:

| Environment | Tag Prefix | Purpose |
|-------------|------------|---------|
| `nonprod` | `nonprod-v` | First automated integration environment. |
| `staging` | `staging-v` | Candidate validation before production. |
| `production` | `production-v` | Customer-facing production promotion. |

Rollback tags use `rollback-<environment>-v<version>`. Hotfix tags use the same environment
prefix with an explicit hotfix version such as `production-v1.2.3.1`.

## Deployment Workflow

1. Resolve the repository and reject non-Infiquetra owners.
2. Inspect `.github/workflows/` and classify whether tag-promotion is full, partial, or absent.
3. Infer versions only from policy-safe sources: latest snapshot for nonprod, current nonprod for
   staging, current staging for production.
4. Refuse forward promotion when `unhealthy-v<version>` exists unless the user explicitly chooses
   an audited override after manual verification.
5. Preview the tag, target ref, workflow URL, and release notes.
6. Require explicit confirmation before pushing tags for staging, production, rollback, or hotfix.
7. Push the tag only after checks and approval are clear.
8. Capture the GitHub Actions URL, deployment status, tag, commit SHA, and issue or PR links.

## State Model

Durable evidence belongs in the repository:

- Release notes or deployment notes in repo docs when the repo already has that convention.
- Issue comments through `mission-control` when an SDLC issue exists.
- PR comments when deployment is tied to a PR.

Runtime scratch belongs under ignored local state such as `.gemini/saga/` or a
deployment-specific cache. Do not commit raw API responses or validator JSON.

## Script Helpers

- `plugins/deploy/scripts/mint_tag.py`: build and optionally push policy tags.
- `plugins/deploy/scripts/query_deployments.py`: show status and drift.
- `plugins/deploy/scripts/preview_release_notes.py`: summarize candidate changes.
