---
name: react-frontend-catalog
description: Index of the decomposed React/Next.js frontend skill catalog (component patterns, hooks, state, performance, forms, error boundaries, animation, accessibility). Use to find which specific skill applies instead of loading one large frontend-patterns doc.
metadata:
  origin: decomposed from frontend-patterns + frontend-a11y (2026-08-26)
allowed-tools: Read, Edit, Grep, Glob
---

# React frontend skill catalog

Originally two large skills (`frontend-patterns`, `frontend-a11y`) covering everything from
component composition to reduced-motion in one file each. Split into focused skills so each loads
only what's relevant to the task at hand.

## Component & state patterns

- `react-component-composition` — composition over inheritance, compound components, render props
- `react-custom-hooks` — toggle/query/debounce hooks, stable-callback traps
- `react-state-context-reducer` — Context + useReducer for multi-field state
- `react-forms` — controlled forms with useState validation
- `react-error-boundaries` — class-based ErrorBoundary with retry

## Performance & polish

- `react-performance` — memoization, code splitting, list virtualization
- `react-animation` — Framer Motion list/modal transitions

## Accessibility

- `a11y-forms` — label/id, required-field, error-message wiring
- `a11y-semantics-aria` — semantic HTML vs ARIA, aria-label/labelledby/describedby/live/expanded
- `a11y-keyboard-nav` — keyboard handlers for custom non-native widgets
- `a11y-focus-management` — modal focus move-in/restore-out
- `a11y-media-motion` — prefers-reduced-motion hook

## How to pick

Match the task, not the file that used to contain it — e.g. building a modal touches
`a11y-focus-management` (focus) and possibly `react-animation` (transitions) and
`a11y-media-motion` (respecting reduced motion), not one monolithic "modal" skill. Cross-links
between the related skills above point to the adjacent piece.
