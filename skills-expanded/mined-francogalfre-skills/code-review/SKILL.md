---
name: code-review
description: Reviews code for bugs, security vulnerabilities, performance issues, and readability problems. Use when the user says "review this code", "check my code", "what's wrong with this", "code review", "audit this file", or pastes code and asks for feedback. Works with any language but optimized for TypeScript, JavaScript, React, and Node.js.
---

# Code Review

Performs structured code reviews across four dimensions: correctness, security,
performance, and readability. Produces actionable findings with severity levels
and concrete fix suggestions — not vague observations.

---

## Required Details

| Detail | Example |
|---|---|
| **Code to review** | Paste or file path |
| **Language / framework** | TypeScript, React, Node.js |
| **Context** | What does this code do? |
| **Focus area** | All / security only / performance only |

---

## Instructions

### Step 1 — Scan across four dimensions

**Correctness**
- Logic errors, off-by-one, wrong conditions
- Unhandled edge cases (null, empty array, 0, negative)
- Async issues: missing `await`, unhandled promise rejections
- Race conditions or state mutations

**Security**
- Unsanitized user input used in queries, HTML, or shell commands
- Secrets or credentials in code
- Missing auth/permission checks
- Insecure defaults (no HTTPS, weak crypto, open CORS)

**Performance**
- Expensive operations inside loops or render functions
- Missing memoization where it matters (`useMemo`, `useCallback`, `React.memo`)
- N+1 query patterns
- Unnecessary re-renders or large bundle imports

**Readability**
- Magic numbers or strings without named constants
- Functions doing more than one thing
- Names that don't communicate intent
- Dead code or commented-out blocks

### Step 2 — Assign severity to each finding

| Severity | Meaning |
|---|---|
| 🔴 Critical | Bug or security hole — must fix before merge |
| 🟠 High | Likely to cause problems in production |
| 🟡 Medium | Should fix — degrades quality or maintainability |
| 🔵 Low | Nice to fix — style, naming, minor improvement |

### Step 3 — Format each finding

```
[severity] Category — Short title

Problem: [what is wrong and why it matters]
Line: [line number or code snippet]
Fix:
```[language]
[corrected code]
```
```

---

## Non-Negotiable Acceptance Criteria

- [ ] Every finding has a severity level
- [ ] Every finding has a concrete fix — not just "consider improving this"
- [ ] Critical and High findings are listed first
- [ ] No findings about style preferences unless they affect readability significantly
- [ ] If code has no issues in a category, state it explicitly — don't omit the category

---

## Output Format

~~~
## Code Review

### Summary
[2-3 sentences: overall quality, main concerns, safe to merge or not]

### Findings

[findings ordered by severity — Critical first]

### Verdict
- [ ] Needs changes before merge
- [ ] Approved with suggestions
- [ ] Approved
~~~