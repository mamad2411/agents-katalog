---
name: react-typescript-patterns
category: frontend
description: Use when writing React + TypeScript components - functional components, explicit typed props, derived state over effects, and no any/unsafe casts
tech_stack: React
---
# React + TypeScript Patterns

## Overview

The compiler is your first test. The recurring defects are `any`/`as` casts that hide type errors, `useEffect` used where a derived value or event handler belongs, and state that should have been derived.

**Core principle:** Type at the source, derive over effect, functional components only.

## Rules

- **Functional components with hooks** — no class components.
- **Explicit, exported props interfaces** next to the component. Never `any`; avoid `as` casts — fix the type at the source.
- **Named exports** for pages/components, one component per file; shared UI lives in the atomic levels (component-composition), page-only wiring next to its page.
- **Derive state** where possible; `useState` for genuinely local state; lift to a hook only when multiple components need it.
- **Effects are a last resort.** Prefer event handlers and derived values. Every `useEffect` has a correct dependency array and a cleanup when it subscribes/allocates.
- **Type all API responses** with interfaces matching the backend JSON — the compiler is your contract test.

## Worked Example

```tsx
// ❌ effect + state to compute something derivable; `any` hides the shape
const [fullName, setFullName] = useState("");
useEffect(() => { setFullName(user.first + " " + user.last); }, [user]);

// ✅ derived value, typed
interface Props { user: User }
export function UserBadge({ user }: Props) {
  const fullName = `${user.first} ${user.last}`;   // derived, no state, no effect
  return <span>{fullName}</span>;
}
```

The derived version has no effect to get wrong, no stale state, and the `User` type flows through.

## Common Mistakes

- `any` or `as` to silence the compiler instead of fixing the type.
- `useEffect` computing a value that could be derived inline.
- State that mirrors a prop.
- Class components.

## Red Flags

- `: any` or `as SomeType` in the diff.
- A `useEffect` whose only job is `setState` from props.
- A missing/incorrect effect dependency array.
