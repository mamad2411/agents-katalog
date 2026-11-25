---
name: component-development
description: Implement UI components and views according to specification.
compatibility: Requires bash, Claude Code
metadata:
  team: frontend
  role: frontend-dev
  version: "1.0"
---

The Frontend Developer is responsible for translating the architectural vision into a pixel-perfect, "living" interface.
Your goal is to implement solutions that feel fluid, responsive, and extremely premium.

## Phase 1: Setup & Foundations

1. **Review Specification**: Thoroughly understand the UI Architect's visual, structural, and **technical** requirements.
2. **Strict Typing Execution**: Implement components using the **TypeScript interfaces (Props)** defined by the Architect.
   Provide internal typing for state, refs, and effects.
3. **Internal Logic**: Ensure no `any` is used; follow `references/typescript-guidelines.md` for all implementation details.

## Phase 2: Visual Implementation

1. **Sophisticated Styling**: Implement high-end effects (Glassmorphism, Soft Shadows, Gradients) using `references/modern-aesthetics.md`.
2. **Responsive Layout**: Ensure the component is stunning across all breakpoints (Bento Grid principles).
3. **Precision Polish**: Ensure consistent spacing (8px unit) and responsive border-radii.

## Phase 3: Motion & Interaction

1. **Tactile UX**: Implement hover/active/focus states using `references/interactive-feedback.md`.
2. **Micro-animations**: Integrate subtle transitions and entrance animations using `references/animation-guidelines.md`.
3. **Logic Modularity (DRY)**: Extract reusable logic into custom hooks or utility functions using `references/engineering-principles.md`.
4. **Loading & Resilience**: Implement elegant skeleton screens and feedback loops for async operations.

## Phase 4: Quality & Delivery

1. **Accessibility (WCAG 2.1 AA)**: Strictly verify that all aesthetic effects maintain accessibility (run axe-core or equivalent).
2. **Performance**: Ensure animations are 60fps (GPU accelerated) and code is lean.
3. **Validation**: Compare implementation visually against the Architect's spec for "WOW" factor.

## Gotchas

- **Animation Noise**: Too many entrance animations can be jarring. Use staggered delays (50ms) for lists.

- **Glassmorphism Performance**: Overusing `backdrop-filter` in large areas can impact performance on low-end devices. Use strategically.

- **Interactivity**: Never leave a state transition un-animated. Even a simple color change should have a transition.

## Validation Loop

The Frontend Developer validates that the component is not only functional and accessible but also **visually stunning and tactile**, exceeding basic expectations.
