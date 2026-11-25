---
name: pr-review-expert
description: Structured PR/code review with blast radius analysis, security scanning, breaking change detection, and test coverage delta. Use when reviewing PRs, doing code reviews, or before merging changes.
---

# PR Review Expert

**Category:** Code Review / Quality Assurance

## Overview

Systematic code review that goes beyond style nits. Performs blast radius analysis, security scanning, breaking change detection, and test coverage delta calculation. Produces a reviewer-ready report with a 30+ item checklist.

## When to Use

- Before merging any PR that touches shared libraries, APIs, or DB schema
- When a PR is large (>200 lines changed)
- Security-sensitive code paths (auth, payments, PII handling)
- After an incident — review similar code proactively

## Workflow

### Step 1 — Gather Context

Identify what changed:
```bash
rtk git diff --name-only main...HEAD
rtk git diff --stat main...HEAD
rtk git log --oneline main...HEAD
```

### Step 2 — Blast Radius Analysis

For each changed file, identify:

1. **Direct dependents** — who imports this file?
```bash
# Find all files importing a changed module
rtk grep -r "from ['\"].*changed-module['\"]" src/ --include="*.ts" -l
rtk grep -r "import.*changed-module" src/ --include="*.py" -l
```

2. **Service boundaries** — does this change cross a service?
```bash
rtk git diff --name-only main...HEAD | cut -d/ -f1-2 | sort -u
```

3. **Shared contracts** — types, interfaces, schemas
```bash
rtk git diff --name-only main...HEAD | rtk grep -E "types/|interfaces/|schemas/|models/"
```

**Severity classification:**
- **CRITICAL** — shared library, DB model, auth middleware, API contract
- **HIGH** — service used by >3 others, shared config, env vars
- **MEDIUM** — single service internal change, utility function
- **LOW** — UI component, test file, docs

### Step 3 — Security Scan

Check diff for common vulnerability patterns:

| Category | Pattern | Severity |
|----------|---------|----------|
| SQL Injection | Raw string interpolation in queries | 🔴 CRITICAL |
| Hardcoded secrets | `password = "..."`, API keys in code | 🔴 CRITICAL |
| XSS vectors | `dangerouslySetInnerHTML`, `innerHTML =` | 🔴 CRITICAL |
| Auth bypass | Missing auth checks on endpoints | 🔴 CRITICAL |
| eval/exec | `eval()`, `exec()`, `subprocess.call(shell=True)` | 🔴 CRITICAL |
| Insecure hash | `md5()`, `sha1()` for security purposes | 🟡 HIGH |
| Path traversal | User input in file paths | 🟡 HIGH |
| Prototype pollution | `__proto__`, `constructor[` | 🟡 HIGH |

### Step 4 — Test Coverage Delta

```bash
# Count source vs test files changed
rtk git diff --name-only main...HEAD | rtk grep -vE "\.test\.|\.spec\.|__tests__" | wc -l  # source
rtk git diff --name-only main...HEAD | rtk grep -E "\.test\.|\.spec\.|__tests__" | wc -l   # tests
```

**Coverage rules:**
- New function without tests → flag
- Deleted tests without deleted code → flag
- Auth/payments paths → require thorough coverage

### Step 5 — Breaking Change Detection

**API contracts:**
- Removed/renamed endpoints
- Changed request/response schema
- Removed TypeScript exported types/interfaces

**DB schema:**
- `DROP TABLE`, `DROP COLUMN`, `ALTER...NOT NULL` without default
- Missing down migration / rollback

**Config/env vars:**
- New `process.env.*` references (may be missing in prod)
- Removed env vars (could break running instances)

### Step 6 — Performance Impact

- N+1 query patterns (DB calls inside loops)
- Heavy new dependencies added
- Unbounded loops on potentially large datasets
- Missing `await` (accidentally sequential promises)

## Complete Review Checklist

```markdown
### Scope & Context
- [ ] PR title accurately describes the change
- [ ] Description explains WHY, not just WHAT
- [ ] No unrelated changes (scope creep)
- [ ] Breaking changes documented

### Blast Radius
- [ ] Identified all dependents of changed modules
- [ ] Cross-service dependencies checked
- [ ] Shared types/interfaces reviewed for breakage
- [ ] New env vars documented in .env.example
- [ ] DB migrations are reversible

### Security
- [ ] No hardcoded secrets or API keys
- [ ] SQL queries use parameterized inputs
- [ ] User inputs validated/sanitized
- [ ] Auth checks on all new endpoints
- [ ] No XSS vectors
- [ ] No sensitive data in logs

### Testing
- [ ] New functions have unit tests
- [ ] Edge cases covered (empty, null, boundary)
- [ ] Error paths tested
- [ ] No tests deleted without reason

### Performance
- [ ] No N+1 query patterns
- [ ] DB indexes for new query patterns
- [ ] No unbounded loops on large datasets
- [ ] Async operations correctly awaited

### Code Quality
- [ ] No dead code or unused imports
- [ ] Error handling present
- [ ] Consistent with existing patterns
- [ ] No unresolved TODOs
```

## Output Format

```
## Code Review: [Title]

Blast Radius: HIGH — changes lib/auth used by 5 services
Security: 1 finding (medium severity)
Tests: Coverage delta +2%
Breaking Changes: None detected

--- MUST FIX (Blocking) ---
1. [File:Line] Issue description. Fix: [suggestion]

--- SHOULD FIX (Non-blocking) ---
2. [File:Line] Issue description.

--- SUGGESTIONS ---
3. [File:Line] Optimization opportunity.

--- LOOKS GOOD ---
- [Positive observations]
```

## Best Practices

1. Read the linked ticket before looking at code
2. Check CI status before reviewing
3. Prioritize blast radius and security over style
4. Label each comment: "must:", "should:", "nit:", "question:"
5. Batch all comments in one review round
6. Acknowledge good patterns, not just problems
