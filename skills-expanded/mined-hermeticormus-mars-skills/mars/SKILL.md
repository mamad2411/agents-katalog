---
name: mars
description: Production-readiness audit for the five mortal sins of vibe-coded MVPs (data model drift, happy path delusion, observability void, unit economics buried in code, environment confusion). Rates findings by severity and returns a verdict. Use before launch or when asked for a Mars audit / production-readiness check.
license: MIT
---

# Mars: production code audit

Mars is the god of war against sloppy code. Point it at a codebase to find the production sins before real users do. Not here to validate feelings; here to find what breaks at 3 AM. The code either meets the standard or it does not, and Mars says which.

Mars is the broad production-readiness sweep across all five categories. For a security-specific deep audit with fixes applied, see [`vibe-proof-skills`](https://github.com/HermeticOrmus/vibe-proof-skills).

## The five mortal sins

### 1. Data model drift

Schema, types, and frontend disagree on the shape of the data. Hunt for: types that do not match the DB schema, optional-vs-required mismatches, enums not in the database, dates as strings parsed inconsistently, IDs as numbers in some places and strings in others, missing foreign keys, orphaned-data possibilities.

### 2. Happy path delusion

Only works when every input and dependency behaves. Hunt for: no error boundaries, try/catch that swallows errors, API calls without timeouts, missing null checks, no retry logic, frontend-only validation, no rate limiting, missing input sanitization, SQL injection and XSS vectors.

### 3. Observability void

Nothing to read when it breaks. Hunt for: `console.log` instead of structured logging, no request ID correlation, no performance timing, no error tracking, no health checks, no DB connection or queue monitoring, silent failures returning 200.

### 4. Unit economics buried in code

Hidden per-request cost. Hunt for: unbounded queries (no LIMIT), N+1 patterns, missing pagination, uncompressed large payloads, no caching, sync operations that should be async, missing indexes, full table scans behind the ORM.

### 5. Environment confusion

Code does not know which environment it runs in. Hunt for: hardcoded URLs and API keys, missing env-var validation, no `.env.example`, secrets in git history, prod DB reachable from dev, missing environment-specific config, debug code in production.

## Severity scale

- **CRITICAL**: data loss or security breach. Blocks production.
- **SEVERE**: production outage. Blocks launch.
- **MODERATE**: degraded experience. Fix soon.
- **MINOR**: compounding technical debt.

## Audit protocol

1. Scan the codebase. Leave no file unturned.
2. Categorize each finding under one of the five mortal sins.
3. Rate each finding on the severity scale.
4. Give a `file:line` reference for every finding.
5. Recommend a concrete fix, not a direction.
6. Order the fixes by severity, then blast radius.

## Output format

```markdown
# MARS AUDIT REPORT
**Project**: {project_name}
**Date**: {date}
**Verdict**: {PRODUCTION_READY | NEEDS_HARDENING | DEPLOY_AT_YOUR_PERIL}

## Summary
{One honest paragraph}

## Critical issues ({count})
## Severe issues ({count})
## Moderate issues ({count})
## Minor issues ({count})

## Priority order
1. {First fix}
2. {Second fix}

## Verdict
{Final assessment and next step}
```

The verdict line is the load-bearing output. `PRODUCTION_READY` means no critical or severe findings. `NEEDS_HARDENING` means severe but no critical. `DEPLOY_AT_YOUR_PERIL` means at least one open critical finding.

---

See full content at https://github.com/HermeticOrmus/mars-skills.
