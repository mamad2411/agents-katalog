---
name: production-readiness-review
description: Reviews whether a feature branch is ready to run in production. It checks the deployment platform, data durability and backups, schema migrations, configuration and secrets, transport security, build and dependencies, observability, scaling and rollback, and produces a traffic-light report and a change list. Use it whenever the user asks if something is production ready, before a first deploy or a release, for a go-live checklist, deployment review, operational readiness, or when "production changes" left for later need to be addressed.
---

# Production readiness review

Most production failures come from assumptions nobody checked. Start by turning assumptions into facts.

## 1. Ask about the target

Ask in one round, with recommended options first. Skip what the repo already answers.

| Question | Why it matters |
| --- | --- |
| Where does it run (VPS, container, PaaS, serverless)? Is the disk persistent across deploys? | Data loss when state is stored on local disk |
| Is there a reverse proxy or load balancer? Which address does the app see? | Client IP for rate limits, trusted proxy settings |
| Is HTTPS terminated before the app? | Secure cookies, HSTS |
| How many instances? | In-memory state, stores that allow one writer, shared secrets |
| How are secrets and environment variables set? | Missing or weak secrets, the production mode of the runtime or framework |
| Where do logs go? Is there alerting? | Silent failures |
| How is it deployed and rolled back? Is there CI? | Broken builds, untested merges |

## 2. Review each area

| Area | Check |
| --- | --- |
| Data | Source of truth, backups and restore test, operations that delete data (confirmation, backup first) |
| Schema | Version marker, migrations for existing databases, a test that starts from the previous schema |
| Configuration | Every variable documented, validated at startup, safe defaults, failure messages |
| Transport and session security | HTTPS, HSTS, `Secure` cookies, trusted proxies, CORS scope |
| Build and dependencies | Runtime needs only production dependencies; generated assets built at build time; a dependency audit (for example `npm audit --omit=dev`, `pip-audit`, `composer audit`); engine versions tested |
| Observability | Logs enabled, errors logged with cause, audit events, no secrets in logs |
| Scale | In-memory limits and caches, concurrent writers, expensive operations (for example password hashing, reports) |
| Operations | Start, stop, health check, rollback, runbook for the top failures |

For heavy branches, run `red-team-review` with production-focused missions (operations, data durability, security in deployment) instead of reviewing alone.

## 3. Report and triage

Write `.scratchpad/<slug>/production-readiness-report.md` with `traffic-light-findings`:

- Facts confirmed by the user and assumptions still open.
- Findings per area.
- A "where to look first when it fails" table, with the first suspect for each symptom.

Then run `triage-findings-list` to merge it with other open reports, and ask which changes to apply.
