# Skill: Code Review

## When to Use
Activate when reviewing code for quality, security, performance, or maintainability.
This includes pull request reviews, pre-commit checks, and "is this good enough to ship?" decisions.

## Process

### 1. Understand the Intent
Before judging the code, understand what it's trying to do.
- Read the commit message, PR description, or task context
- Identify the scope: new feature, bug fix, refactor, or optimization
- Note what's in scope for review and what isn't

### 2. Check Correctness
Does the code do what it claims to do?
- Trace the main execution path manually
- Identify edge cases: null inputs, empty collections, boundary values, concurrent access
- Check error handling: are failures caught, reported, and recoverable?
- Verify the code matches the stated requirements, not just "looks right"

### 3. Check Security
Look for common vulnerabilities appropriate to the context:
- Input validation at system boundaries (user input, API responses, file reads)
- Injection risks: SQL, command, XSS, path traversal
- Authentication and authorization: is every endpoint/action properly gated?
- Secrets: no hardcoded keys, tokens, or credentials
- Dependencies: any known vulnerabilities in added packages?

### 4. Check Maintainability
Will the next developer understand this in 6 months?
- Naming: do variables, functions, and classes reveal intent?
- Complexity: can any function be split for clarity?
- Duplication: is there copy-paste code that should be abstracted?
- Tests: are the important paths covered? Are tests testing behavior, not implementation?

### 5. Check Performance (if relevant)
Only flag performance issues that matter at the expected scale.
- N+1 queries, unbounded loops, unnecessary allocations
- Missing indexes on queried columns
- Large payloads or responses that should be paginated

## Output Format

```
## Code Review: [File or PR name]

**Scope:** [What was changed and why]

**Critical Issues** (must fix before merge)
- [Issue with file:line reference and specific fix]

**Improvements** (should fix, not blocking)
- [Suggestion with reasoning]

**Nitpicks** (optional, take or leave)
- [Minor style or preference items]

**What's Good**
- [Specific things done well -- reinforce good patterns]
```

## Rules
- Always read the full diff before commenting. Don't review line-by-line in isolation.
- Lead with critical issues. Don't bury security problems under style nitpicks.
- Every criticism must include a specific suggestion. "This is bad" is not a review.
- Praise good patterns explicitly. Reinforcement shapes future code quality.
- Don't bikeshed. If it works and it's readable, move on.
