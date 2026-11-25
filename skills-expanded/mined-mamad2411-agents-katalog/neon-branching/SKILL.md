---
name: neon-branching
description: Neon database branching in CI — branch-per-PR and branch-per-test-run lifecycle, expiry as a cleanup backstop, migration gating against production-shaped data, branch secrets handling, and cost hygiene. Load when writing or reviewing CI workflows for a Neon-backed project.
user-invocable: false
stack: ci/neon-branching
paths:
  - ".github/workflows/**"
  - ".gitlab-ci.yml"
  - ".circleci/config.yml"
  - "**/neon.ts"
  - "**/neon.config.*"
  - "**/*neon*.yml"
---

Full standards in [neon-branching.md](neon-branching.md). Always-on summary.

> **Scope — applies only if this project uses neon-branching.** This layer shares `.circleci/config.yml`, `.github/workflows/**`, `.gitlab-ci.yml` with `circleci`, `github-actions`, `gitlab-ci` in `layers/ci/`, so more than one may load at once and their rules conflict. If the project is not using neon-branching, ignore this layer.
> See `docs/adr/0001-layer-glob-collision-and-dispatcher-routing-policy.md`.

**Scope:** enforceable CI rules only. For the branch-type decision tree and full CLI reference use the official `neon-postgres-branches` skill. For connection strings and migration mechanics see the `neon` layer.

**Branch type:**
- **Normal branch** — migration validation. Copies real row shapes and volumes, which is what makes the test meaningful.
- **Schema-only branch** — when the parent holds PII. Structure without rows.
- Schema-only branches are **independent root branches** — no parent, no shared history. `reset --parent` does not apply to them, so never design a CI flow around resetting one.

**Branch-per-PR lifecycle:**
- Create on PR open; delete on merge **and** on close-without-merge — these are different events, and missing the second is the usual leak
- Name the branch deterministically from the PR number so a re-run reuses instead of duplicating
- Cleanup job runs `if: always()`

**Always set an expiry, even when you have a delete step.** `--expires-at`, or `ttl` in `neon.ts`. The delete step does not run when a job is cancelled or the runner dies — expiry is the only backstop that survives that, and orphaned branches are the most common source of unexpected Neon cost.

**Migration gating:** run migrations on the PR's branch using `DATABASE_URL_UNPOOLED`, against a branch **of production** — never an empty database. An empty DB will not catch a backfill that times out or a `NOT NULL` added to a populated table.

**Secrets:** `NEON_API_KEY` from CI secrets only. Mask the branch connection string; never `echo` it into logs. Never expose the API key to fork PRs — see the `pull_request_target` hazard.

**Never:** share one CI database across parallel jobs · disable scale-to-zero on CI branches · leave cleanup off the failure path.

**Related:** `neon`, `naming-conventions`, `data-governance`, `secret-scanning`.
