---
name: typescript-advance
description: Use this skill to implement expert-level TypeScript patterns like generics, discriminated unions, and branded types. Trigger this WHENEVER the user wants to model complex business logic, eliminate "impossible states", or refactor "any"-heavy legacy code into type-safe architectures.
license: MIT
compatibility: Designed for any Agent Skills-compliant client (e.g. Claude Code)
metadata:
  version: "1.1"
  triggers:
    - "advanced typescript"
    - "typescript generics"
    - "discriminated unions"
    - "model impossible states"
    - "typescript best practices"
---

# Advanced TypeScript Skill

This skill provides a systematic approach to writing type-safe, maintainable, and expressive TypeScript code. It focuses on using the compiler to eliminate entire classes of bugs by modeling data accurately.

## Core Principles
1. **Stop using `any`**: Use `unknown` or generics instead. `any` is a trap that bypasses type checking.
2. **Model Impossible States as Impossible**: Use Discriminated Unions to ensure that an object can only exist in valid states.
3. **Generics for Reusability**: Design components and functions that adapt to data while maintaining strict type boundaries.
4. **Exhaustiveness Checking**: Use the `never` type to ensure that every possible case in a union is handled.

## Workflow
Progress:
- [ ] **Architecture**: Choose between `interface` and `type` (Extensibility vs. Composability).
- [ ] **Defense**: Implement type guards and assertion functions for dynamic data.
- [ ] **Transformation**: Leverage utility types (`Pick`, `Omit`, `Partial`) to reduce boilerplate.
- [ ] **Validation**: Ensure no `any` leaks into the final implementation.

## Gotchas
- **Deep Recursion**: Extremely complex recursive types (like deep path pickers) can slow down the TS compiler or hit the recursion limit.
- **Narrowing Pitfalls**: Remember that `typeof null === 'object'`. Always check for nullity before narrowing objects.
- **Discriminated Union Requirements**: Every member of the union MUST share the same literal property (the "discriminant") to be narrowed correctly.
- **Generic Constraints**: Be careful with "too open" generics. Use `extends` to provide the compiler with enough context to be useful.

## Reference Documentation
For detailed patterns and examples:
- [Best Practices & Patterns](./references/best-practices.md)
- [Project Configuration](./references/config.md)

## Success Criteria
- No `any` types are used in new code.
- Discriminated unions are used for complex state management (e.g., API responses).
- Generics include proper constraints (`extends`) where applicable.

