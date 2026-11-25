---
name: code-review
description: "Apply when reviewing code, giving feedback, or checking a PR. Covers: what to look for, how to give constructive feedback, security checklist, and common code smells. Trigger for: review, PR, pull request, code quality, feedback, refactor."
---

# CODE REVIEW — What to Look For

## Security Checklist (check first)
- [ ] No hardcoded secrets, tokens, passwords
- [ ] Input validated before use (Pydantic/Zod)
- [ ] SQL queries parameterized (no string concat)
- [ ] Auth checks on all new endpoints
- [ ] No sensitive data logged
- [ ] Dependencies not introducing vulnerabilities

## Correctness
- [ ] Edge cases handled (empty input, null, large numbers)
- [ ] Error handling — what happens when it fails?
- [ ] Race conditions (shared state, concurrent writes)
- [ ] Off-by-one errors in loops and slices
- [ ] Async/await used correctly (no missing await)

## Code Quality Signals
```python
# 🚩 Red flags to call out:
# 1. Function > 50 lines → suggest decomposition
# 2. Nesting > 3 levels → suggest early returns
# 3. Magic numbers/strings → suggest constants
# 4. Duplicate code (3+ times) → suggest extraction
# 5. Boolean parameter → suggest enum or two functions
# 6. God class/function → suggest SOLID split

# ✅ Positive signals to acknowledge:
# - Clear variable names
# - Well-placed comments (why, not what)
# - Tests included
# - Handles failure cases
```

## How to Give Feedback
```
# Levels of feedback (be explicit about severity):
# [BLOCK] Security issue or incorrect behavior — must fix
# [IMPORTANT] Performance, maintainability — should fix
# [SUGGESTION] Style, minor improvement — optional

# Format:
# ❌ "This is wrong"
# ✅ "[IMPORTANT] This N+1 query will be slow at scale.
#    Consider: JOIN users on user_id instead. Here's an example: ..."
```

## Common Code Smells
```
- "util.py" or "helpers.py" — vague catch-all modules
- Functions named "process", "handle", "do" — not descriptive
- `except Exception: pass` — silently swallowing errors
- Long parameter lists (> 4 args) → use dataclass/TypedDict
- Returning None on error instead of raising exception
- print() for logging
- TODO comments without issue number or date
```

## What NOT to Block On
- Personal style preferences (use linter instead)
- Naming conventions (if they're consistent)
- "I would have done it differently" without clear benefit
- Minor refactors unrelated to the PR scope
