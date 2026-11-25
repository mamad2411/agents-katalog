---
name: refactor
description: 'Surgical code refactoring to improve maintainability without changing behavior. Covers extracting functions, renaming variables, breaking down god functions, improving type safety, eliminating code smells, and applying design patterns. Less drastic than repo-rebuilder; use for gradual improvements.'
---

# Refactor

## Overview

Improve code structure and readability without changing external behavior. Refactoring is gradual evolution, not revolution.

## When to Use

- Code is hard to understand or maintain
- Functions/classes are too large
- Code smells need addressing
- Adding features is difficult due to code structure
- User asks "clean up this code", "refactor this", "improve this"

---

## Refactoring Principles

### The Golden Rules

1. **Behavior is preserved** — Refactoring doesn't change what code does
2. **Small steps** — Make tiny changes, test after each
3. **Version control** — Commit before and after each safe state
4. **Tests are essential** — Without tests, you're editing, not refactoring
5. **One thing at a time** — Don't mix refactoring with features

### When NOT to Refactor

- Code that works and won't change again
- Critical production code without tests (add tests first)
- Under a tight deadline
- "Just because" — need a clear purpose

---

## Safe Refactoring Process

```
1. PREPARE
   - Ensure tests exist (write them if missing)
   - Commit current state
   - Create feature branch

2. IDENTIFY
   - Find the code smell to address
   - Understand what the code does
   - Plan the refactoring

3. REFACTOR (small steps)
   - Make one small change
   - Run tests
   - Commit if tests pass
   - Repeat

4. VERIFY
   - All tests pass
   - Manual testing if needed
   - Performance unchanged or improved

5. CLEAN UP
   - Update comments
   - Update documentation
   - Final commit
```

---

## Refactoring Checklist

### Code Quality
- [ ] Functions are small (< 50 lines)
- [ ] Functions do one thing
- [ ] No duplicated code
- [ ] Descriptive names
- [ ] No magic numbers/strings
- [ ] Dead code removed

### Structure
- [ ] Related code is together
- [ ] Clear module boundaries
- [ ] Dependencies flow in one direction
- [ ] No circular dependencies

### Type Safety
- [ ] Types defined for all public APIs
- [ ] No `any` types without justification
- [ ] Nullable types explicitly marked

### Testing
- [ ] Refactored code is tested
- [ ] Tests cover edge cases
- [ ] All tests pass

---

## References

> For detailed code smells catalog (10 patterns with examples), design patterns (Strategy, Chain of Responsibility), extract method examples, type safety introduction, and the complete refactoring operations table, see:
> `references/code-smells-catalog.md`
