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

Runtime scratch belongs under ignored local state such as `.claude/saga/` or a
deployment-specific cache. Do not commit raw API responses or validator JSON.

## Accepting a saga handoff

When promoting on behalf of a saga-tracked item, `saga`'s `/work` mints an **offer** (an ack
token + a gate-or-auto payload) at or after merge via `plugins/saga/scripts/deploy_handoff.py
offer`. Ownership is not considered transferred until `deploy` explicitly **acknowledges (ack)**
it — an offer alone is never read as "done".

1. Read the offer before promoting:

   ```bash
   python3 plugins/saga/scripts/deploy_handoff.py read --saga-id <saga-id>
   ```

2. Record the write-once ack once you take the item:

   ```bash
   python3 plugins/saga/scripts/deploy_handoff.py accept \
     --saga-id <saga-id> --token <token-from-offer> \
     --by <identity> --evidence <durable-evidence-e.g.-PR-or-tag-url>
   ```

   A double-accept, an accept without a matching offer, or a stale (superseded) token is refused.

3. **Apply the gate-or-auto rule before promoting** — do not decide gate-vs-auto by convention.
   Read the payload from the offer (`deploy_handoff.py read`); the rule below is implemented
   mechanically as `authorize_promotion` in `plugins/saga/scripts/deploy_handoff.py`. The payload
   is `gate` or `auto`, captured once at saga intent time and carried unmodified with the offer:
   - `gate` **always** blocks pending explicit operator confirmation. A `gate` payload is never
     silently overridden to auto-fire, regardless of environment.
   - `auto` authorizes unattended promotion for `nonprod` only; `staging` and `production` always
     require explicit confirmation regardless of payload.
4. An unacknowledged offer reads `handed-off-unacknowledged` on
   `deploy_handoff.py reconcile --saga-id <saga-id>` (or `--all` for a sweep) — treat that as a
   dropped baton, not a clean state, and accept it before proceeding.

This ack contract is scoped to the saga -> deploy edge and does not change tag-promotion
mechanics, environment model, or the confirmation requirements in "Deployment Workflow" above.

## Script Helpers

- `plugins/deploy/scripts/mint_tag.py`: build and optionally push policy tags.
- `plugins/deploy/scripts/query_deployments.py`: show status and drift.
- `plugins/deploy/scripts/preview_release_notes.py`: summarize candidate changes.
- `plugins/saga/scripts/deploy_handoff.py`: read/accept a saga's deploy-handoff offer via its
  `read`/`accept`/`reconcile` CLI verbs; its `authorize_promotion` function implements the
  gate-or-auto rule (see "Accepting a saga handoff" above).
