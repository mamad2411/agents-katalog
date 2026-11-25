---
name: code-review
description: Generate a focused code review checklist based on language, framework, and change type. Outputs specific items to check, not generic advice.
argument-hint: [language/framework, change description, risk level]
allowed-tools: Read, Write
---

# Code Review Checklist Generator

Generate a targeted code review checklist from the change context. No boilerplate — every item should be specific to the language, framework, and type of change being reviewed.

## Process

1. **Parse change context.** Identify language, framework, change type (new feature, bug fix, refactor, performance).
2. **Assess risk.** Database migration? Auth changes? Payment flow? Flag high-risk areas.
3. **Generate language-specific checks.** Memory management (C/C++), null safety (Kotlin), async correctness (JavaScript/Python).
4. **Add framework-specific checks.** React hooks dependencies, Django ORM N+1 queries, SQL injection in raw queries.
5. **Include security checks.** Input validation, auth bypass, data exposure.
6. **Check performance impact.** O(n²) loops, unindexed queries, missing pagination.
7. **Verify tests.** Coverage for new code, edge cases, integration tests.
8. **Structure as actionable checklist.** Group by category, priority order.

## Output Format

### Code Review Checklist: [Change Title]

**Language:** [Python/JavaScript/Java/Go/etc.]  
**Framework:** [Django/React/Spring Boot/etc.]  
**Change Type:** [New Feature/Bug Fix/Refactor/Performance]  
**Risk Level:** [Low/Medium/High/Critical]

---

## Critical Issues (Must Fix)

### Security
- [ ] **SQL Injection:** Raw SQL queries use parameterized statements, not string concatenation
- [ ] **XSS:** User input is escaped before rendering in HTML
- [ ] **Auth bypass:** New endpoints require authentication decorators/middleware
- [ ] **Sensitive data:** Passwords/tokens not logged or exposed in error messages
- [ ] **CSRF protection:** POST/PUT/DELETE requests include CSRF token

### Data Integrity
- [ ] **Database migration:** Migration is reversible (has down migration)
- [ ] **Foreign keys:** ON DELETE behavior specified (CASCADE/RESTRICT/SET NULL)
- [ ] **Null handling:** Required fields have NOT NULL constraints
- [ ] **Data validation:** Input validation at API boundary, not just client side

### Correctness
- [ ] **Edge cases handled:** Empty arrays, null values, zero/negative numbers
- [ ] **Error handling:** Exceptions caught and logged, user sees meaningful error
- [ ] **Race conditions:** Concurrent access handled (locks, transactions, idempotency)

---

## High Priority

### Performance
- [ ] **N+1 queries:** Django/ORM queries use select_related/prefetch_related
- [ ] **Pagination:** List endpoints return max 100 items, support pagination
- [ ] **Indexes:** New WHERE/JOIN columns have database indexes
- [ ] **Caching:** Expensive operations cached (API calls, complex queries)

### Code Quality
- [ ] **No magic numbers:** Constants extracted to named variables
- [ ] **Function length:** Functions under 50 lines (break up if longer)
- [ ] **Naming:** Variable/function names are descriptive, not abbreviated
- [ ] **DRY:** No copy-pasted code blocks (extract to shared function)

### Testing
- [ ] **Unit tests:** New functions have tests covering happy path + 2-3 edge cases
- [ ] **Integration tests:** New API endpoints have integration tests
- [ ] **Test coverage:** New code has ≥80% coverage (check with coverage tool)
- [ ] **Test quality:** Tests assert behavior, not implementation details

---

## Medium Priority

### Framework-Specific (React)
- [ ] **Hook dependencies:** useEffect/useCallback dependency arrays are complete
- [ ] **Key prop:** Lists use unique, stable keys (not array index)
- [ ] **State updates:** setState uses functional form when depending on previous state
- [ ] **Memoization:** Expensive computations wrapped in useMemo

### Framework-Specific (Django)
- [ ] **QuerySet evaluation:** Avoid query evaluation in loops (use values_list)
- [ ] **Model validation:** clean() method validates business logic
- [ ] **Signal receivers:** Signals are idempotent (handle duplicate calls)
- [ ] **Migration dependencies:** Migration lists dependencies on other migrations

### Observability
- [ ] **Logging:** Errors logged with context (user ID, request ID, stack trace)
- [ ] **Metrics:** New feature has success/failure metrics
- [ ] **Monitoring:** Database queries logged if duration > 1s

---

## Low Priority

### Style & Conventions
- [ ] **Linting passes:** No linter warnings introduced
- [ ] **Formatting:** Code formatted with project formatter (Black/Prettier/etc.)
- [ ] **Imports:** Unused imports removed
- [ ] **Comments:** Complex logic has explanatory comments (why, not what)

### Documentation
- [ ] **API docs:** New endpoints documented in OpenAPI/Swagger
- [ ] **README:** Updated if setup process changes
- [ ] **Changelog:** Entry added for user-facing changes

---

## Risk-Specific Checks

### If Database Migration:
- [ ] Migration tested on staging data
- [ ] Data backfill script tested for large tables
- [ ] Index creation uses CONCURRENTLY (PostgreSQL)
- [ ] Estimated migration duration documented

### If Payment/Financial:
- [ ] Idempotency key prevents duplicate charges
- [ ] Currency handling uses DECIMAL, not FLOAT
- [ ] Amount validation prevents negative/zero values
- [ ] Refund logic tested

### If Authentication:
- [ ] Password reset tokens expire
- [ ] Session timeout configured
- [ ] Failed login attempts rate-limited
- [ ] Two-factor auth not bypassed

---

## How to Use This Checklist

1. **Read the code.** Understand what it does before checking boxes.
2. **Check Critical first.** Stop review if critical issues found.
3. **High Priority next.** Request changes if multiple High items fail.
4. **Medium/Low are suggestions.** Author can push back with rationale.
4. **Not every item applies.** Skip irrelevant checks, but note why.
5. **Add custom items.** If you spot issues not on list, add them.

## Rules

- Checklist must be specific to the language and framework (React checks for React PRs, Django checks for Django PRs).
- Group by risk level: Critical > High > Medium > Low.
- Critical items are blockers — PR should not merge if these fail.
- Include realistic examples in brackets [like this] when useful.
- If change involves high-risk areas (auth, payments, migrations), include dedicated risk sections.
- Every checkbox must be actionable ("Check for X") not vague ("Code is good").
- Maximum 40 checklist items — more than that is noise.
- If change type is unclear, list questions to clarify before generating checklist.
