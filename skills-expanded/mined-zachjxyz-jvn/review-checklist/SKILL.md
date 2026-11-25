---
name: review-checklist
description: Code review standards and checklist for the code-reviewer agent
user-invocable: false
---

# Code Review Checklist

Use this checklist when reviewing implementation changes.

## Correctness
- [ ] Logic matches specification requirements
- [ ] Edge cases handled (null, empty, boundary values)
- [ ] Error paths return appropriate responses
- [ ] No off-by-one errors in loops/pagination

## Type Safety
- [ ] No `any` types
- [ ] No `@ts-ignore` or `@ts-expect-error`
- [ ] Drizzle query types properly inferred (not manually typed)
- [ ] API response types match contract

## Security
- [ ] No secrets or credentials in source code
- [ ] Auth checks on all protected routes and server actions
- [ ] User input validated at system boundaries
- [ ] SQL injection prevented (Drizzle parameterized queries)
- [ ] XSS prevented (no `dangerouslySetInnerHTML` without sanitization)

## Performance
- [ ] No N+1 query patterns
- [ ] Indexes on columns used in WHERE, JOIN, ORDER BY
- [ ] Independent data fetches use `Promise.all()`
- [ ] Heavy components use `next/dynamic` for code splitting
- [ ] Suspense boundaries wrap async server components

## Testing
- [ ] Tests written BEFORE implementation (TDD)
- [ ] Happy path covered
- [ ] Error cases covered
- [ ] Edge cases covered
- [ ] Integration tests for API routes

## Maintainability
- [ ] Files under ~200 lines (split if larger)
- [ ] Descriptive variable and function names
- [ ] Early returns for guard clauses
- [ ] No dead code (unused imports, variables, functions)
- [ ] No commented-out code
