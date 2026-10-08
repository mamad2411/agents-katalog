---
name: code-review
description: Comprehensive code review for quality, security, performance, and maintainability.
---

# Code Review

Thorough code review covering all quality dimensions.

## Review Checklist

### Correctness
1. Does the code do what it claims?
2. Are edge cases handled (null, empty, boundary)?
3. Are error paths covered?
4. Are concurrency issues addressed?

### Security
1. Input validated and sanitized?
2. Output encoded for the right context?
3. Auth checks present where needed?
4. No secrets in code or logs?
5. No SQL injection / XSS / SSRF vectors?

### Performance
1. N+1 queries eliminated?
2. Appropriate data structures used?
3. No unnecessary allocations?
4. Caching applied where beneficial?
5. No blocking I/O on hot paths?

### Maintainability
1. Naming is clear and consistent?
2. Functions are small and focused?
3. No dead code or commented-out blocks?
4. Complex logic is explained (comments/README)?
5. Tests cover the new behavior?

### API Design
1. Consistent with existing API patterns?
2. Backward compatible (or versioned)?
3. Error responses follow existing conventions?
4. Documentation updated?

## Review Process
1. **Skim**: Read the entire diff for context
2. **Understand**: Grasp the intent of the change
3. **Deep Dive**: Focus on security-critical and complex sections
4. **Test**: Verify tests exist and are meaningful
5. **Feedback**: Be specific, constructive, and kind

## Feedback Format
```
[SEVERITY] file:line — Description
Suggestion: Specific fix or approach
```
Severity levels: BLOCKER, MAJOR, MINOR, NIT
