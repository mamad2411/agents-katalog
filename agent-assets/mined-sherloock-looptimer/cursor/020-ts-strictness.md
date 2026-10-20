---
description: TypeScript strictness and boundary validation expectations.
globs: "app/**/*.ts, app/**/*.tsx, components/**/*.ts, components/**/*.tsx, actions/**/*.ts, lib/**/*.ts, hooks/**/*.ts, utils/**/*.ts, schema/**/*.ts, types/**/*.ts"
alwaysApply: false
---

## TypeScript strictness (critical)
- Treat the codebase as strict TypeScript; keep type-safety high.
- Prefer `unknown` over `any`, then narrow using type guards.
- Define proper types/interfaces for complex objects (timers, intervals, loops, presets).
- Avoid magic string unions in implementation; prefer `as const` objects or enums for finite states.

## Validation at boundaries
- Use Zod for runtime validation at boundaries (API routes, forms, server actions).
