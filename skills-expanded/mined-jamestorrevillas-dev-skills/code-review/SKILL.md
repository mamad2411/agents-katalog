---
name: code-review
description: Use this skill when performing code reviews, security audits, architecture reviews, vulnerability analysis, or evaluating code quality. Trigger on keywords: code review, review, audit, security, vulnerability, OWASP, SQL injection, XSS, architecture review, refactor suggestion, quality check, static analysis.
---

# Code Review

## Review Philosophy

Review the code, not the person. The goal is to ship better software, not to win arguments. Every comment should make the codebase better or help the author learn — preferably both.

---

## Feedback Categories

Always tag review comments to set expectations:

| Tag | Meaning | Must Fix? |
|---|---|---|
| `BLOCKER` | Breaks functionality, security risk, violates standards | Yes |
| `WARNING` | Technical debt, potential issue, should be addressed | Recommended |
| `SUGGESTION` | Optional improvement, alternative approach | No |
| `QUESTION` | Asking for clarification or understanding | No |
| `NITPICK` | Minor style or preference | Author decides |
| `PRAISE` | Acknowledge good work | N/A |

---

## Code Quality Checklist

### Correctness
- [ ] Does the code do what the ticket/story requires?
- [ ] Are edge cases handled? (null, empty, boundary values)
- [ ] Is error handling present and meaningful?
- [ ] Are async operations awaited properly?
- [ ] Are there any obvious race conditions?

### Readability
- [ ] Are variable and function names descriptive?
- [ ] Is the code self-documenting (minimal need for comments)?
- [ ] Are complex sections commented with the "why"?
- [ ] Is there dead code or commented-out code that should be removed?
- [ ] Is function length reasonable (< 40 lines as a guideline)?

### Architecture
- [ ] Does this follow the existing patterns in the codebase?
- [ ] Is there unnecessary coupling between modules?
- [ ] Is the change in the right layer (controller vs service vs repository)?
- [ ] Would this be hard to test? (if yes, it needs refactoring)
- [ ] Is this solving the right problem at the right level?

### Performance
- [ ] Are there N+1 query problems (loops that trigger individual DB queries)?
- [ ] Are expensive operations cached where appropriate?
- [ ] Is pagination implemented for list endpoints?
- [ ] Are there unnecessary re-renders (frontend)?

### Tests
- [ ] Are tests included for new behavior?
- [ ] Do tests cover the happy path AND error paths?
- [ ] Are tests testing behavior, not implementation details?

---

## Security Review (OWASP Top 10)

Apply a security persona when reviewing code that touches auth, data access, or user input.

### Input Validation
- [ ] Is all user input validated and sanitized before use?
- [ ] Are parameterized queries / ORMs used? (never raw string concatenation in SQL)
- [ ] Is output encoded before rendering to prevent XSS?

### Authentication & Authorization
- [ ] Are protected endpoints properly authenticated?
- [ ] Is authorization checked at the right level (not just frontend)?
- [ ] Are JWTs validated properly (signature, expiry, issuer)?
- [ ] Is there rate limiting on auth endpoints?

### Sensitive Data
- [ ] Are secrets/credentials in environment variables, not hardcoded?
- [ ] Is sensitive data (passwords, tokens) hashed or encrypted at rest?
- [ ] Is sensitive data excluded from logs?
- [ ] Does the API return only the data the client needs (no over-fetching)?

### Dependencies
- [ ] Are new dependencies well-maintained and trusted?
- [ ] Is the dependency necessary, or can it be avoided?
- [ ] Are there known vulnerabilities in the added version?

---

## Architecture Review

When reviewing architectural decisions:

### Questions to Ask
1. **Scalability** — Will this work at 10x current load?
2. **Maintainability** — Will a new developer understand this in 6 months?
3. **Testability** — Can this be unit tested without complex setup?
4. **Reversibility** — How hard is it to undo this decision?
5. **Consistency** — Does this align with how the rest of the system works?

### Red Flags
- God classes / functions (doing too many things)
- Deep inheritance hierarchies
- Hardcoded configuration values
- Direct cross-module database access
- Synchronous calls to external services without timeout/retry
- Missing abstractions that make testing impossible

---

## Review Comment Examples

### Good Comment (Specific + Constructive)
```
BLOCKER: This SQL query is vulnerable to injection. User input is concatenated 
directly into the query string. Use parameterized queries instead:

// Instead of:
db.query(`SELECT * FROM users WHERE id = ${userId}`)

// Use:
db.query('SELECT * FROM users WHERE id = $1', [userId])
```

### Bad Comment (Vague + Unhelpful)
```
This doesn't look right.
```

---

## Self-Review Checklist (Before Submitting a PR)

Run through this before requesting review:
- [ ] I've reviewed my own diff line by line
- [ ] Tests are passing locally
- [ ] No debug logs or commented-out code left in
- [ ] No hardcoded secrets or environment-specific values
- [ ] PR description clearly explains what, why, and how
- [ ] Scope is focused — no unrelated changes snuck in
