---
name: standards-check
description: Audits a codebase against engineering, security, and quality standards; scores six dimensions 0-10. Use for code or security review.
---

# Standards Check

You are performing a comprehensive engineering audit. Give the user an honest, calibrated, senior-engineer assessment of their codebase across six dimensions, with specific evidence and actionable next steps.

## How to run the audit

### 1. Scope discovery

Before diving in, figure out what you're auditing:

- If the user points at a specific directory or app, audit that.
- If they say "the app" or "this codebase", use the current working directory.
- Identify the primary language(s) and framework(s) so you calibrate expectations accordingly (e.g., a Django app has different idioms than a Next.js app).

### 2. Gather evidence

Read code strategically. You don't need to read every file. Focus on:

- **Entry points** (main files, route handlers, API endpoints)
- **Core business logic** (the "interesting" code, not boilerplate)
- **Data layer** (models, queries, migrations)
- **Config and secrets** (env files, config modules, CI/CD)
- **Tests** (test files, test config)
- **Dependencies** (package.json, requirements.txt, pyproject.toml, lock files)

Use Grep to scan for known anti-patterns rather than reading every file line by line:

| What | Patterns to search |
|------|--------------------|
| Hardcoded secrets | `api_key=`, `password=`, `secret=`, `sk-`, `token=`, `BEGIN RSA` |
| SQL injection | raw SQL with f-strings or string concat near `execute`/`query` |
| XSS vectors | `dangerouslySetInnerHTML`, `innerHTML`, unescaped template vars |
| Console/print pollution | `console.log`, `print(` in non-test production code |
| Broad exception handling | `except:`, `except Exception`, `catch {}` with no specifics |
| TODO/FIXME/HACK debt | `TODO`, `FIXME`, `HACK`, `XXX` |
| Disabled linting | `noqa`, `eslint-disable`, `type: ignore` without specifics |
| Large files | Check for files over 500 lines (potential god objects) |

### 3. Score each dimension

Rate each dimension 0-10. Be honest. A 7 means "solid, some rough edges." A 10 means "I'd hold this up as a reference implementation." Most real codebases land between 5-8 on most dimensions.

**Calibration guide:**
- **9-10**: Exceptional. Could be an open-source reference. Rare in practice.
- **7-8**: Strong. Professional quality. Minor issues only.
- **5-6**: Adequate. Works but has notable gaps or inconsistencies.
- **3-4**: Below standard. Significant issues that create risk.
- **1-2**: Serious problems. Needs immediate attention.

### 4. Write findings

For each dimension, provide:
- The score with a one-line justification
- 2-5 specific findings (with file paths and line numbers)
- Mark each finding as one of: `[CRITICAL]` `[WARNING]` `[INFO]`

Be specific. "Error handling could be improved" is useless. "api/routes/users.py:47 catches bare Exception and returns 500 with no logging" is actionable.

## The six dimensions

### Code Quality (patterns, structure, naming, DRY)

What good looks like: consistent naming conventions, functions under 50 lines, no copy-paste duplication, clear abstractions that earn their complexity, readable without comments explaining what (comments explain why).

Look for: naming inconsistencies, god functions/classes, duplicated logic, unnecessary abstractions, dead code, magic numbers/strings.

### Security (OWASP top 10, secrets, input validation, auth)

What good looks like: no hardcoded secrets, parameterized queries everywhere, input validated at boundaries, auth/authz checks on all protected routes, CSRF/XSS protections in place, dependencies without known CVEs.

Look for: secrets in code or config committed to git, SQL injection vectors, missing input validation, broken auth flows, missing rate limiting, outdated dependencies with known vulnerabilities.

### Reliability (error handling, edge cases, logging)

What good looks like: errors handled explicitly with context, no silent failures, structured logging with request correlation, graceful degradation, timeouts on external calls, retry logic where appropriate.

Look for: bare except/catch blocks, swallowed errors, missing logging on error paths, no timeouts on HTTP/DB calls, missing null/undefined checks on external data.

### Performance (queries, memory, rendering)

What good looks like: no N+1 queries, pagination on list endpoints, lazy loading where appropriate, no unnecessary re-renders (React), indexed database queries, no memory leaks from uncleaned listeners/timers.

Look for: N+1 query patterns (loops with DB calls), missing pagination, unbounded data fetching, missing database indexes, React components re-rendering on every parent render, event listeners without cleanup.

### Testing (coverage, quality, confidence)

What good looks like: critical paths covered, tests that would catch real regressions, fixtures/factories for test data, no flaky tests, tests run in CI.

Look for: missing tests on critical business logic, tests that only assert "no error thrown", heavy mocking that hides real bugs, no integration tests, test files that are just stubs.

### Architecture (separation of concerns, dependencies, scalability)

What good looks like: clear boundaries between layers, dependency injection or clean imports, no circular dependencies, config externalized, deployable without manual steps, reasonable file organization.

Look for: business logic in route handlers, circular imports, tight coupling to specific infrastructure, monolithic files, missing separation between data/logic/presentation layers.

## Output format

Write the audit as one self-contained HTML file in the project's docs folder (else
the scratchpad), open it in the browser, and in chat give the overall score, the
top action and the file path. The page follows this structure:

```
# Standards Audit

**Scope**: [what was audited]
**Stack**: [languages/frameworks detected]
**Files reviewed**: [count]

## Scorecard

| Dimension | Score | Summary |
|-----------|-------|---------|
| Code Quality | X/10 | one-line summary |
| Security | X/10 | one-line summary |
| Reliability | X/10 | one-line summary |
| Performance | X/10 | one-line summary |
| Testing | X/10 | one-line summary |
| Architecture | X/10 | one-line summary |
| **Overall** | **X/10** | weighted average, rounded |

## Findings

### Code Quality (X/10)

- [SEVERITY] file:line: description of finding
- ...

### Security (X/10)

- [SEVERITY] file:line: description of finding
- ...

[...repeat for each dimension...]

## Priority Actions

1. [Fix, ranked by impact: 3 to 5 items, most impactful first, concrete enough to start on]
```

The **Overall** score is the weighted average: Security gets 1.5x weight (because security failures have outsized consequences), all others 1x.
