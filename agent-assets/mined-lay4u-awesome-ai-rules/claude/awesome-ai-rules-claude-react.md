# React + TypeScript Project Rules

## Scope
- Applies to React applications and component libraries using TypeScript.
- Optimize for composability, testability, and clear component boundaries.

## Core Stack
- React with TypeScript is required.
- Tailwind CSS is the default styling system.
- Routing must use either:
  - React Router v7, or
  - TanStack Router
- Storybook is required for component documentation.

## Component Structure
- Each component file should follow this order:
  1. imports
  2. `Props` interface/type
  3. component implementation
  4. named export
- Prefer one component per file unless tightly coupled primitives are trivial.
- Use named exports; avoid default exports.

## Props and Types
- Every component must have explicit prop typing.
- Use `interface` for public props by default.
- Keep props minimal and explicit; avoid `any`.
- Use discriminated unions for variant-heavy components.

## State Management
- Local UI state: `useState` (or `useReducer` when transitions are complex).
- Global/shared client state: Zustand.
- Do not use global state for ephemeral local concerns.
- Keep async data fetching concerns separate from UI-only state.

## Styling Rules
- Tailwind utility classes are preferred for styling.
- Inline styles are not allowed except dynamic CSS variables when unavoidable.
- CSS Modules are not allowed.
- Shared visual primitives should be wrapped in reusable components.

## Routing Conventions
- Route definitions should be centralized and strongly typed.
- Use route-level data loading patterns provided by the selected router.
- Keep route components thin; delegate business logic to hooks/services.

## Testing Standards
- Every component must have tests using React Testing Library.
- Test files use `*.test.tsx`.
- Cover at least:
  - render baseline
  - critical interactions
  - accessibility-relevant behavior (labels, roles, keyboard where applicable)
- Assert user-visible outcomes, not implementation details.

## Storybook Standards
- Every shared/reusable component must include stories.
- Provide at least:
  - default state
  - key variants
  - edge/empty/loading/error states when relevant
- Keep stories aligned with production props and realistic data.

## File Layout Guidance
- Example feature structure:
  - `components/` for reusable UI
  - `features/<name>/` for domain-specific UI + hooks + tests
  - `routes/` for route entry components
  - `state/` for Zustand stores

## Definition of Done
- Typecheck and lint pass.
- Component tests exist and pass for new/changed UI.
- Storybook stories are added/updated for reusable components.
- Styling follows Tailwind-first, no inline styles, no CSS modules.
