---
name: development-behavior
description: Defines practical implementation behavior focused on minimal scope, simple solutions, and maintainable code. Use when planning or implementing features to avoid over-engineering, unrelated changes, and unnecessary dependencies.
---

# Development Behavior

Follow these behavior rules strictly during implementation.

## Core Rules

- Do not over-engineer.
- Prefer simple solutions first.
- Do not add backend, database, or API work unless explicitly requested.
- Use static JSON data when possible.

## Feature Implementation Rules

- Focus only on what is asked.
- Do not modify unrelated parts of the codebase.
- Do not introduce new dependencies unless necessary.

## When Requirements Are Unclear

- Make reasonable assumptions.
- Keep the solution minimal.
- Choose the lowest-complexity path that still satisfies the request.

## Always Optimize For

- Simplicity
- Maintainability
- Clarity

## Implementation Checklist

Use this checklist for feature work:

```markdown
Development Behavior Checklist
- [ ] Solution is simple and avoids over-engineering
- [ ] Scope matches only what was requested
- [ ] No backend/database/API added unless explicitly requested
- [ ] Uses static JSON data when suitable
- [ ] No unrelated files or logic changed
- [ ] No new dependency added unless clearly necessary
- [ ] Ambiguities handled with reasonable minimal assumptions
- [ ] Final result is simple, maintainable, and clear
```
