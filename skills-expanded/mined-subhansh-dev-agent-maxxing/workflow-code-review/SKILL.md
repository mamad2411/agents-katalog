---
name: workflow-code-review
description: Run an 8-angle code review with security audit before merging.
---

# Multi-Agent Workflow: Deep Code Review

> Run an 8-angle code review with security audit before merging.

## Skills Used

| Skill | Role |
|-------|------|
| [Deep Code Review](../engineering/deep-code-review/SKILL.md) | 8-angle correctness review |
| [Security Review](../engineering/security-review/SKILL.md) | Security vulnerability audit |
| [Code Simplify](../engineering/code-simplify/SKILL.md) | Cleanup and optimization |
| [Runtime Verify](../engineering/runtime-verify/SKILL.md) | Run the app and observe behavior |
| [Code Review Checklist](../engineering/code-review-checklist/SKILL.md) | Final checklist pass |

## Workflow

### Phase 1: Gather Context

```bash
git diff @{upstream}...HEAD  # Get the diff
git log --oneline -10        # Recent commits
```

### Phase 2: Deep Review (Parallel)

Launch 3 parallel reviews:

**Review 1 — Correctness (8 angles):**
```
Load Deep Code Review skill.
Run all 8 angles: line-by-line, removed-behavior, cross-file, reuse, simplification, efficiency, altitude, conventions.
Return: up to 10 findings ranked by severity.
```

**Review 2 — Security:**
```
Load Security Review skill.
Examine: input validation, auth, crypto, injection, data exposure.
Return: HIGH/MEDIUM findings only with confidence scores.
```

**Review 3 — Cleanup:**
```
Load Code Simplify skill.
Run 4 cleanup angles: reuse, simplification, efficiency, altitude.
Return: actionable fixes.
```

### Phase 3: Runtime Verification

```
Load Runtime Verify skill.
Build the app, run it, drive the changed code paths.
Capture: stdout, screenshots, error messages.
Push on it: try edge cases, wrong inputs, rapid actions.
Verdict: PASS / FAIL / BLOCKED / SKIP
```

### Phase 4: Final Checklist

```
Load Code Review Checklist.
Check: works? readable? safe? performant? maintainable?
Frontend: accessible? responsive? loading states? no CLS?
Backend: migrations reversible? rate limiting? logging?
```

### Phase 5: Report

```markdown
## Review Summary

**Correctness:** 3 findings (1 HIGH, 2 MEDIUM)
**Security:** 1 finding (1 MEDIUM)
**Cleanup:** 2 suggestions
**Runtime:** PASS — all paths verified

### Critical Findings
1. [HIGH] SQL injection in user search — line 42
2. [MEDIUM] Missing error handler in API route — line 87

### Recommendations
- Add input validation before line 42
- Wrap API handler in try/catch
- Consider adding rate limiting
```
