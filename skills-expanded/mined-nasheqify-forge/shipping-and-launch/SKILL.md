---
name: shipping-and-launch
description: >
  Production-launch discipline with pre-launch checklist +
  feature-flag strategy + staged rollout + rollback plan +
  monitoring. Use when deploying to production, preparing a
  release, migrating data / infra, opening beta, or any
  deployment that carries risk.
status: active
invocation:
  primary: user-facing
  secondary: [workflow-step]
  trigger_patterns:
    - "deploy to production"
    - "ship to prod"
    - "production launch"
    - "rollout"
    - "release"
disable-model-invocation: false
---

Read and follow `framework/work-principle.md` before taking up work.
Resolve this reference against the framework root; retain the consumer CWD.


# Skill: shipping-and-launch

## Purpose

Production-launch discipline. The goal is not just deploying —
it's **deploying safely** with active monitoring, a tested
rollback plan, and a clear definition of success. Every launch
should be reversible, observable, and incremental.

Deploy-discipline invariants (pg_dump before a DB deploy, mount
verification before a recreate) are formal skill obligations here, not
just a user convention.

## Source

agent-skills at `eb07f19` (MIT License, © 2025 Addy Osmani); Forge's register of adopted methods.

## Standalone

Distinct from:
- `skills/code_review_board/` — code-quality review before
  deploy, not deploy discipline. shipping-and-launch is the
  post-code-review gate.
- `skills/testing/` — test methodology, not production
  rollout.
- `workflows/runbooks/save/WORKFLOW.md` step 10 (dashboard
  deploy in background) — minimal docs deploy.
  shipping-and-launch is a production-service deploy with
  risk management.

What only this skill delivers:
- Pre-launch checklist (6 categories) as a required gate.
- Feature-flag lifecycle discipline (owner + expiration +
  2-week cleanup).
- Staged-rollout sequence with a threshold table (advance /
  hold / rollback).
- Rollback-plan obligation **before deploy** (not ad-hoc
  post-incident).
- Post-launch verification in the first hour.
- Deploy-discipline invariants (pg_dump before DB-touch,
  mount-verify after machine change) as mechanical
  obligations.

## When to call

- Before the first production deploy of a feature.
- On every significant release for users.
- On data or infrastructure migration.
- On beta or early-access opening.
- On every deploy that carries risk (every deploy).

### Do not call for

- Docs-only deploy via `deploy-docs.sh` — minimal risk; the
  save workflow step 10 is enough.
- Internal-tooling updates without user impact — use
  code_review_board L1.
- Pure bug fixes with clear reproduction — fix workflow + L1
  review is enough (except: a fix that touches the DB →
  deploy discipline active).

## Process

### Phase 1: pre-launch checklist (MUST before deploy)

Before a production deploy starts: read and follow `skills/shipping_and_launch/pre-launch-checklist.md` (six required
categories, every box ticked: code quality, security, performance, accessibility, infrastructure, documentation).

### Phase 1.5: DEPLOY-DISCIPLINE-INVARIANT (NON-NEGOTIABLE)

These two INVARIANTS are **mechanical obligations** before
every production deploy that touches the DB or recreates
containers. They apply to any docker-compose deploy with
persistent data.

#### INVARIANT-1: pg_dump pre-DB-deploy

> On EVERY DB-touching deploy: `pg_dump` as the FIRST command
> before the recreate. No exception, even on "trivial
> migrations" (CHECK constraint add, column rename, etc).

**Required command format:**

```bash
docker compose exec -T <service-name>-db pg_dump -U <user> <dbname> | \
  gzip > ~/backups/<service-name>-pre-deploy-$(date +%Y%m%d-%H%M).sql.gz
```

**Rationale:** 30s pg_dump versus hours of recovery via
re-ingest (when an external source exists) or total data
loss (when not). Lost data is not reproducible. This
invariant has been validated by real incidents where a
"trivial" migration produced total DB loss because the
pg_dump step was skipped.

**When to skip:** **never.** Not even on a nominal
"read-only change". DB touch is DB touch.

#### INVARIANT-2: mount-verify pre-container-recreate

> On a docker-compose recreate after a location / machine
> change: verify the mount sources BEFORE `up -d`.

**Required steps:**
1. `docker inspect <container>` on the running container —
   which bind mounts, which volumes?
2. Check whether `--env-file` or other flags are needed for
   the same mount state.
3. Only then `up -d`.

**Rationale:** implicit defaults ("compose reads .env
automatically") don't apply to `.env.production` — it has to
be passed explicitly, otherwise a different mount appears.

### Phases 2–5: feature flags, staged rollout, monitoring, post-launch verification

When a release uses a feature flag, before the first deploy stage of a rollout and at each advance, hold or rollback
decision, when setting up monitoring before launch, and in the first hour after the launch: read and follow
`skills/shipping_and_launch/rollout.md` (phase 2 feature-flag lifecycle and discipline; phase 3 rollout sequence,
decision thresholds, immediate-rollback triggers; phase 4 what to monitor, error-reporting pattern; phase 5
post-launch verification).

### Phase 6: rollback plan (REQUIRED to write before deploy)

```markdown
## Rollback plan for [feature/release]

### Trigger conditions
- Error rate > 2x baseline
- P95 latency > [X]ms
- User reports of [specific issue]

### Rollback steps
1. Disable the feature flag (when applicable)
   OR
1. Deploy the previous version: `git revert <commit> && git push`
   PLUS on the target host: `docker compose pull && docker compose up -d`
2. Verify: health check + error monitoring
3. Communicate: notify the team

### Database considerations
- Migration [X] has rollback: `alembic downgrade -1`
- Data from the new feature: [preserved / cleaned up]

### Time to rollback
- Feature flag: <1 min
- Redeploy previous version: <5 min
- DB rollback: <15 min (when needed — pg_dump as the recovery source)
```

## Red flags

- Deployment without a rollback plan.
- No monitoring or error reporting in production.
- Big-bang releases (everything at once, no staging).
- Feature flags without expiration or owner.
- Nobody monitors the first hour post-deploy.
- Production config from memory instead of from code.
- "It's Friday afternoon, let's ship".
- DB-touching deploy without pg_dump (INVARIANT
  violation).
- Container recreate without mount verify (INVARIANT
  violation).

## Common rationalizations

| Rationalization | Reality |
|---|---|
| "It works in staging, so it works in production" | Production has different data, traffic patterns, edge cases. Monitor after deploy. |
| "We don't need a feature flag for that" | Every feature benefits from a kill switch. Even "simple" changes can break. |
| "Monitoring is overhead" | Without monitoring you discover problems through user complaints instead of dashboards. |
| "We add monitoring later" | Add it before launch. What you don't see, you can't debug. |
| "Rollback is admitting failure" | Rollback is responsible engineering. Shipping a broken feature is the failure. |
| "The migration is trivial — pg_dump is unnecessary" | Validated by real incident: trivial migration, total DB loss. **Never skip.** |
| "Mount-verify is paranoia, compose reads .env anyway" | Validated by real incident: `.env.production` was not read; a different mount appeared. **Verify.** |

## Contract

### INPUT
- **Required:** Code Review Board PASS
  (`code_review_board` L1 or L2 done) — BEFORE the
  pre-launch checklist.
- **Required:** test suite PASS (every level via the
  `testing` skill; the broad run per `skills/testing/run-strategy.md` §Test selection).
- **Required:** production-environment configuration in
  `.env.production` or equivalent.
- **Optional:** feature-flag definition (when phase 2
  applies).
- **Optional:** rollback-plan template (see phase 6).
- **Context:** `skills/code_review_board/SKILL.md`
  (pre-deploy gate), `skills/security_and_hardening/SKILL.md` (cross-ref
  on security pre-launch). Consumer repos can layer
  additional invariants via their own override files.

### OUTPUT
**DELIVERS:**
- Pre-launch checklist ticked (6 categories +
  INVARIANT-1+2 when DB / container).
- Feature-flag configuration (when applicable).
- Rollback plan documented before deploy.
- Monitoring dashboards set up.
- Post-launch verification (first hour) executed.
- Backup file (pg_dump) on a DB-touching deploy.

**DOES NOT DELIVER:**
- No code changes — deploy skill, not a code skill.
- No code review — `code_review_board` is the
  precondition.
- No test run — `testing` is the precondition.
- No spec update — `retroactive_spec_update` is a separate
  lifecycle.

**ENABLES:**
- Production deploy with confidence (pre-launch gate
  satisfied).
- Fast rollback (plan + backup in place).
- Early issue detection (monitoring + verification).
- Step-by-step rollout (staged instead of big-bang).

### DONE
- Every pre-launch checklist box green.
- INVARIANT-1 (pg_dump) executed when DB touch.
- INVARIANT-2 (mount verify) executed when container
  recreate.
- Feature flag with owner + expiration configured (when
  relevant).
- Rollback plan documented.
- Post-launch verification (first hour) done; every check
  green.
- Cleanup date for the feature flag in the calendar.

### FAIL
- **Retry:** pre-launch checklist has issues → fix, then
  re-check (no deploy without 6/6 categories green). On
  DEPLOY-DISCIPLINE-INVARIANT violation: ABORT, no deploy.
- **Escalate:** the threshold table in phase 3 (`rollout.md`) shows red
  values → immediate rollback per plan. Inform the user.
- **Abort:** INVARIANT violation (no pg_dump on DB touch
  / no mount verify on recreate) → ABORT before deploy.
  Risk too high.

## See also

- `skills/code_review_board/SKILL.md` — pre-deploy code
  gate.
- `skills/testing/SKILL.md` — test suite before deploy.
- `skills/deprecation_and_migration/SKILL.md` —
  deprecation workflow (complementary).
- `skills/_protocols/skill-guardrails.md` — skill
  anti-patterns.
- The user's profile (`<user_repo>/context/user/profile.md`) may add
  further deploy invariants.
