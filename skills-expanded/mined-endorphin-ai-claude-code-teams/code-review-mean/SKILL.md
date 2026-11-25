---
name: code-review-mean
description: "Code review for MEAN stack apps. Use when reviewing backend (Express + MongoDB) and frontend (React) code for quality, security, architecture compliance, performance, and best practices."
---

# Code Review Mean

## Purpose

Review MEAN stack code (Express + MongoDB backend and React frontend) for quality, security, architecture compliance, and best practices. Produce structured review verdicts that either approve the code or send it back to developers with specific, actionable feedback.

## Key Patterns

### Review Dimensions
1. **Architecture Compliance** — Does code match architect designs? Models match DB schema? Controllers match API contracts? Components match React design?
2. **Security** — No exposed secrets, proper auth checks, input validation, XSS prevention
3. **Error Handling** — All errors caught, proper status codes, user-friendly messages
4. **Performance** — Indexed queries, pagination, no N+1 queries, React memoization where needed
5. **Code Quality** — Consistent patterns, DRY, proper naming, no dead code
6. **Best Practices** — MEAN-specific patterns followed (Mongoose middleware, Express middleware chain, React hooks rules)

### Backend Review Checklist
- Models have validators, indexes, timestamps, toJSON transform
- Controllers use asyncHandler wrapper
- Routes apply auth + validation middleware correctly
- Error handler catches Mongoose errors (ValidationError, CastError, 11000)
- Passwords hashed with bcrypt, select: false on schema
- JWT properly signed and verified
- No raw user input in queries (injection prevention)
- Environment variables used for secrets

### Frontend Review Checklist
- Functional components with hooks only
- API calls go through services/api.js, not raw axios/fetch
- Loading states on all async operations
- Error states with retry on all data fetches
- Auth context wraps the app, ProtectedRoute guards private pages
- No prop drilling deeper than 2 levels
- Keys on all list-rendered elements
- Responsive design works on mobile

### Issue Severity
- **Critical** — Must fix: security vulnerability, data loss risk, broken functionality, auth bypass
- **Warning** — Should fix: performance issue, poor UX, missing error handling, code smell
- **Info** — Nice to have: style improvement, alternative approach

### Verdict Logic
- **PASS** — Zero critical issues. Warnings noted but don't block.
- **FAIL** — One or more critical issues. Code goes back to developers with fix instructions.

## Conventions

- Review BOTH backend and frontend in a single pass
- Every issue must be actionable — say what's wrong AND how to fix it
- Reference specific files and code patterns
- Don't nitpick style if functionality is correct
- If same issue in multiple files, report once with "also in: file1, file2"
- Maximum 2 review loops — after 2 rounds, remaining warnings ship as tech debt
- Include machine-readable JSON verdict block at end of output

## Knowledge Strategy

- **Patterns to capture:** Common issues in MEAN apps, security vulnerabilities specific to Node.js/MongoDB/React
- **Examples to collect:** Good review verdicts, patterns that consistently cause issues
- **Update permission:** Agents may freely add/update files in `references/`. Changes to `SKILL.md` or `scripts/` require user approval.
