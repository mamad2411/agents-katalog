---
name: components-composition-patterns
description: React composition patterns that scale — compound components, render props, context providers, lifting state. Use when refactoring boolean-prop-heavy components or designing flexible, reusable component APIs (incl. React 19)
---

# React Composition Patterns

Composition patterns for building flexible, maintainable React components. Avoid
boolean prop proliferation by using compound components, lifting state, and
composing internals. These patterns make codebases easier for both humans and AI
agents to work with as they scale.

## Rule Categories by Priority

| Priority | Category                | Impact | Prefix          | Reference                               |
| -------- | ----------------------- | ------ | --------------- | --------------------------------------- |
| 1        | Component Architecture  | HIGH   | `architecture-` | `references/component-architecture.md`  |
| 2        | State Management        | MEDIUM | `state-`        | `references/state-management.md`        |
| 3        | Implementation Patterns | MEDIUM | `patterns-`     | `references/implementation-patterns.md` |
| 4        | React 19 APIs           | MEDIUM | `react19-`      | `references/react19-apis.md`            |

## References

Each file is loaded on demand — read one only when the task needs that depth (progressive disclosure).

- `references/component-architecture.md` — avoiding boolean-prop proliferation and structuring compound components with shared context · read when a component has accumulated boolean modes or you're designing a flexible multi-part component API.
- `references/state-management.md` — lifting state into providers, generic context interfaces for dependency injection, decoupling state from UI · read when sibling components need shared state, or you want the same UI to work across different state implementations.
- `references/implementation-patterns.md` — explicit variant components over boolean modes, and children over render props · read when choosing between variant components vs. props, or between `children` and `renderX` callbacks.
- `references/react19-apis.md` — `ref` as a regular prop (no `forwardRef`) and `use()` instead of `useContext()` · read when targeting React 19+ and refactoring refs or context usage.
