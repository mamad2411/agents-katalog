---
name: react-patterns-error-loading-states
description: "Treat non-happy paths as features: skeleton loaders, typed errors, retry affordances, useful empties."
---
# Design error, loading, and empty states first

> Treat non-happy paths as features: skeleton loaders, typed errors, retry affordances, useful empties.

**Track:** 🎨 Frontend Engineering · **Domain:** React Patterns · **Level:** foundation · **~20 min**

**Who this is for:** Frontend Engineers, Full-Stack Developers, Design Engineers, UI Developers

## When to Use This Skill

Treat non-happy paths as features: skeleton loaders, typed errors, retry affordances, useful empties.
Use it whenever a matching task appears in conversation — the agent loads these instructions on demand.

## Steps

1. For every data section, spec loading, error, empty, and partial states upfront
2. Use skeletons matching final layout to avoid shift on load
3. Differentiate recoverable errors (retry button) from fatal ones (support link)
4. Write empty states as invitations: what this shows + how to populate it
5. Surface partial failures inline instead of failing the whole page
6. Add boundary components at route and widget level, logging with context

## Common Pitfalls

- Infinite spinner hiding a thrown error
- Empty tables with zero guidance

## Commands

**Install with skills CLI**
```bash
npx skills add aniruddhaadak80/skills --skill react-patterns-error-loading-states
```

**Install globally**
```bash
npx skills add aniruddhaadak80/skills --skill react-patterns-error-loading-states -g
```

---

Part of [aniruddhaadak80/skills](https://github.com/aniruddhaadak80/skills) · Browse all at https://skills.sh/aniruddhaadak80/skills