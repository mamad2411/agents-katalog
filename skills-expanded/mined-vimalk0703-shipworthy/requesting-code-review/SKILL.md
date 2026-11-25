---
name: requesting-code-review
description: Invoke the code-reviewer agent with git-based commit ranges to get structured feedback on code quality, architecture compliance, and correctness.
invoke_when: Use when requesting a code review after completing a feature, before merging a branch, or when the user asks for a review of their code.
---

# Requesting Code Review

## When to Request

- After completing all tasks in a plan
- Before creating a pull request
- After significant refactoring
- When unsure about an approach

## How to Request

### 1. Determine the Review Scope

Use git to identify what changed:
```bash
git diff main...HEAD --stat        # files changed
git log main..HEAD --oneline       # commits to review
```

### 2. Dispatch the Code Reviewer Agent

Launch the `code-reviewer` agent with:
- The commit range or diff to review
- The architecture.md constraints
- The original plan/spec (if applicable)
- Specific concerns you want addressed

### 3. Review Checklist

The code reviewer evaluates:
- **Plan alignment** — does the code match the spec?
- **Architecture compliance** — does it follow Mandatory Rules?
- **Code quality** — naming, structure, readability
- **Error handling** — proper patterns, no silent failures
- **Security** — input validation, auth checks, no secrets
- **Testing** — coverage, meaningful assertions, edge cases
- **Performance** — no obvious bottlenecks, proper queries
- **Type safety** — no `any`, proper types, null handling

### 4. Issue Severity

Issues are flagged as:
- **Critical** — must fix before merge (bugs, security issues, broken tests)
- **Important** — should fix (architecture violations, missing tests)
- **Suggestion** — nice to have (naming improvements, refactoring ideas)
