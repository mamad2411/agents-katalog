---
name: react-patterns
description: Use when implementing or reviewing React components, hooks, composition, state placement, rendering, or React performance.
---

# React Patterns

## Boundaries

Use only after React is confirmed. Use frontend guidance for broader UX and
TypeScript guidance for advanced type or tooling problems.

## Operating Loop

1. Detect React version, rendering environment, compiler use, framework conventions,
   state libraries, and test setup.
2. Identify ownership of state, effects, async data, and errors.
3. Prefer composition and colocated state; extract only when reuse or complexity
   justifies it.
4. Keep effects synchronized with external systems rather than using them for derived
   state.
5. Profile before performance optimization and verify user-visible behavior.

## Decision Rules

- Follow the Rules of Hooks and preserve stable ownership boundaries.
- Choose local, lifted, contextual, server, or global state from actual scope.
- Treat memoization as a targeted optimization, especially when a compiler is active.
- Provide error recovery and preserve user input where practical.
- Test behavior and accessibility rather than component internals.

## Optional Reference

Load [legacy-guide.md](references/legacy-guide.md) for a compact pattern catalog after
confirming its assumptions match the repository.
