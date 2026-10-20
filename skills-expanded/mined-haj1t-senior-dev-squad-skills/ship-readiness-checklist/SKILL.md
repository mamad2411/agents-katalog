---
name: ship-readiness-checklist
description: "Final gate: tests pass, lint/build clean, env documented, migrations safe, rollback possible. Use when verifying a release is ready to ship."
---

# Ship Readiness Checklist

## Overview

The final gate before any code reaches production. One question: **"Is this ready to ship?"** Every item must be green. If any item is RED, the release is blocked.

**Core principle:** SHIPPING IS NOT THE GOAL. SHIPPING SAFELY IS THE GOAL.

## The Iron Law

```
IF YOU WOULDN'T WANT TO BE PAGED ABOUT THIS AT 3 AM, IT'S NOT READY
```

Trust your discomfort. If something feels wrong, fix it before shipping.

## The 7 Gates

### Gate 1: Code Quality
```
☐ Unit, integration, E2E tests pass (CI green)
☐ Bug fix has regression test
☐ FAIL if: Any test suite is red
```

### Gate 2: Build
```
☐ Build succeeds (dev + production)
☐ Docker image builds
☐ FAIL if: Build fails in any environment
```

### Gate 3: Security
```
☐ No secrets committed (scanner confirms)
☐ Input validation + auth on all endpoints
☐ npm audit passes (no critical/high)
☐ FAIL if: Any critical security finding
```

### Gate 4: Operations
```
☐ Env vars documented in .env.example
☐ New vars added to production secret manager
☐ Rollback plan documented and tested
☐ FAIL if: No rollback plan
```

### Gate 5: Database
```
☐ All migrations additive + reversible
☐ Migration tested against staging data
☐ FAIL if: Migration deletes data or has no rollback
```

### Gate 6: Frontend
```
☐ Core Web Vitals meet targets
☐ All states handled (loading, empty, error, success)
☐ Responsive + accessible
```

### Gate 7: Release
```
☐ Release notes written
☐ Version bumped (semver)
☐ Post-release monitoring plan in place
☐ Rollback trigger criteria documented
```

## Quick Summary

| Area | Status | Notes |
|------|--------|-------|
| 🔬 Tests | ✅ | All passing |
| 🔧 Build | ✅ | Production build OK |
| 🔒 Security | ✅ | No findings |
| ⚙️ Ops | ✅ | Rollback tested |
| 🗄️ DB | ✅ | Migration additive |
| Overall | ✅ SHIP | |

## The Red Line

If you would be uncomfortable waking up at 3 AM because of this deployment, it is not ready. Fix what makes you uncomfortable, then ship.

## When to Use

**Use this when:**
- A PR is ready to merge and you need a final gate review
- Before any production deployment, scheduled or emergency
- When handing off a release to another team member or on-call engineer

**Use this ESPECIALLY when:**
- A database migration is part of the release
- The change touches authentication, payments, or data pipelines
- It is a Friday afternoon or holiday-adjacent deployment

**Don't skip when:**
- "It's a tiny hotfix" (hotfixes have caused the worst incidents)
- "CI is green, that's enough" (CI does not cover rollback plans or env documentation)
- "We deploy this service every week" (familiarity breeds skipped checks)

## Red Flags — STOP and Follow Process

If you catch yourself thinking:
- "The rollback is just reverting the commit — no need to document it"
- "Tests are green, everything else can be done post-deploy"
- "It's an internal service, security review isn't necessary"
- "The migration is small, staging isn't worth it"
- "We can add monitoring after we see how it behaves in prod"
- "The env vars haven't changed, no need to check .env.example"
- "We need to ship tonight — we'll skip Gate 4 and 5"

**ALL of these mean: STOP. Return to the relevant phase.**

## Common Rationalizations

| Excuse | Reality |
|--------|---------|
| "Rollback is just `git revert`" | Schema migrations cannot be reversed by a revert. Always test rollback separately. |
| "Monitoring can wait until after deploy" | You will learn it is broken when users start filing tickets. |
| "It passed staging, that's sufficient" | Staging only proves the happy path. You need rollback criteria and triggers documented. |
| "Security scan is slow, skip it this once" | That one time is when the critical CVE ships to production. |
| "The team knows what changed, notes aren't needed" | The on-call engineer at 2 AM does not. Write release notes every time. |

## Your Human Partner's Signals You're Doing It Wrong

**Watch for these redirections:**
- "Do we have a rollback plan?" — Gate 4 was not completed or not communicated
- "Why is this env var missing in production?" — Gate 4 env documentation was skipped
- "How long until we can roll back the migration?" — Database rollback was not tested
- "Who approved this for Friday?" — Gate 7 stakeholder notification was skipped
- "Where are the release notes?" — Gate 7 was treated as optional

**When you see these:** STOP. Return to the relevant gate and complete it before proceeding.

## Verification

- [ ] All 7 gates checked — no gate is marked skipped without documented justification
- [ ] CI is green on the exact commit being deployed (not an earlier commit)
- [ ] Rollback steps written out in plain language and tested against staging
- [ ] Rollback trigger criteria defined (error rate %, latency threshold, alert name)
- [ ] All new environment variables present in `.env.example` with descriptions
- [ ] New secrets added to the production secret manager, not committed to git
- [ ] Database migration tested against a copy of production data or realistic staging volume
- [ ] Migration is additive and has a tested down-migration
- [ ] Health check endpoint responds correctly after staging deployment
- [ ] Release notes written and stakeholders notified
- [ ] Post-release monitoring window defined (who watches, for how long, what alerts)

## Related Skills

- **devops-release-engineer** — use for the full CI/CD pipeline and containerization setup that feeds into this checklist
- **security-reviewer** — use for Gate 3 when a deeper security review is required beyond automated scanning
- **test-engineer** — use to ensure test coverage is adequate before Gates 1 and 2 are assessed
- **edge-case-hunter** — use before the release if business logic changed, to verify failure paths are covered
- **architecture-planner** — use when the release introduces new services or infrastructure dependencies
