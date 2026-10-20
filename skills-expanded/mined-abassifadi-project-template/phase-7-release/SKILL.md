---
name: phase-7-release
description: Phase 7 of the development cycle. Releases a verified milestone — production readiness (monitoring, alerts, runbook, rollback), version number and changelog, release notes, deployment through the CI/CD pipeline, and post-release checks.
disable-model-invocation: true
argument-hint: "[version, e.g. 1.0.0 — omit to propose one]"
---

# Phase 7 — Release

Precondition: `docs/release/VERIFY-<milestone>.md` exists with `Decision: GO`. If not, stop and tell the user to run `/phase-6-verify`.

## Steps

```
Release progress:
- [ ] 1. Production readiness
- [ ] 2. Version and changelog
- [ ] 3. Deploy (with user approval)
- [ ] 4. Post-release check
- [ ] 5. Close the loop
```

**1. Readiness.** Use the `planning-observability` skill to make sure production has:
- a health check endpoint
- structured logs
- the key metrics
- alerts on the spec's availability and latency targets

Then write a short `docs/release/RUNBOOK.md` covering:
- how to deploy
- how to roll back
- where the logs and dashboards are
- what to do for each alert

Confirm the CI/CD pipeline can deploy to production (`setting-up-ci-cd`). Any database migrations must be backward compatible with the currently deployed version.

**2. Version and changelog.**
- Choose a semantic version (MAJOR.MINOR.PATCH): MAJOR for breaking changes, MINOR for features, PATCH for fixes. The first public release is usually `1.0.0`, or `0.x` while things are still unstable.
- Generate `CHANGELOG.md` entries from the Conventional Commits since the last tag, grouped into Added, Changed, Fixed, and Security.
- Write user-facing release notes in plain language.

**3. Deploy.**
- Show the user the version, the changelog, and the rollback plan, then **wait for explicit approval**.
- After approval: tag the release (`vX.Y.Z`) and deploy through the pipeline. Never deploy manually from a laptop.
- Prefer a gradual rollout (canary or a feature flag) when the platform supports it.

**4. Post-release.**
- Watch the health checks, error rate, and latency for the first period after the release.
- If they get worse, roll back first and investigate afterwards (`debugging-systematically`).

**5. Close the loop.**
- Mark the milestone released in BACKLOG.md.
- Move any follow-ups into the backlog.
- Ask the user whether to start the next milestone (`/phase-5-build`) or plan new features (`/phase-1-spec` to update the spec).
