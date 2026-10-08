---
name: frontend-standards
description: Component patterns, state management, styling conventions, and rendering strategies for modern frontend development.
invoke_when: Use when writing React/Next.js components, managing state, styling UI, or making frontend architecture decisions.
---

# Frontend Standards

## Component Patterns

### File Organization
- One component per file
- Co-locate styles, tests, and types with the component
- Name files after the component: `UserProfile.tsx`

### Component Rules
- Prefer function components over class components
- Keep components small — if it exceeds ~150 lines, split it
- Extract custom hooks for reusable logic
- Props interfaces defined above the component

### Server vs Client Components (Next.js App Router)
- Default to server components (no `'use client'`)
- Add `'use client'` ONLY when needed: useState, useEffect, event handlers, browser APIs
- Keep client components as leaf nodes (small, focused)
- Never make a layout or page a client component unless absolutely necessary

## State Management

### Local State
- `useState` for component-specific state
- `useReducer` for complex state logic within a component

### Shared State
- Lift state to the nearest common parent
- Use React Context for truly global state (theme, auth, locale)
- Consider Zustand or Jotai for complex client state
- Server state: use TanStack Query or SWR (not manual fetch + useState)

### Rules
- State should live as close to where it's used as possible
- Avoid prop drilling beyond 2 levels — use Context or composition
- Never store derived data in state (compute it)
- Never mutate state directly — always create new references

## Styling

- Prefer Tailwind CSS or CSS Modules — not inline styles
- Follow the project's established styling approach (check architecture.md)
- Design tokens (colors, spacing, typography) from a single source
- Responsive by default — mobile-first approach

## Data Fetching

- Server components: fetch directly (Next.js) or in loaders
- Client components: use data fetching libraries (TanStack Query, SWR)
- Show loading states for async data
- Handle error states — don't assume fetches succeed
- Implement optimistic updates for better UX on mutations

## Performance

- Use `React.memo` only when profiling shows re-render problems
- Lazy-load routes and heavy components
- Optimize images (next/image, WebP, explicit dimensions)
- Avoid unnecessary re-renders (stable references, proper deps arrays)
