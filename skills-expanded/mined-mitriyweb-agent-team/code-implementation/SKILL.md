---
name: code-implementation
description: Implement UI components and frontend logic according to UI_SPEC.md.
compatibility: Requires bash, Claude Code
metadata:
  team: frontend
  role: developer
  version: "1.0"
tags:
---

The Frontend Developer is responsible for building accessible, responsive, and performant UI components using the project's specified framework and styling approach.

## Phase 1: Technical Foundations

1. **Review Specification**: Thoroughly understand the Architect's visual and structural requirements (`UI_SPEC.md`).
2. **Environment Check**: Verify `FRONTEND_FRAMEWORK` and `CSS_APPROACH` before writing code.
3. **Strict Typing**: Implement components using TypeScript interfaces for props and internal state.

## Phase 2: Implementation (A11y & Design)

1. **Build Components**: Implement components using the specified framework.
2. **Styling**: Apply styles using the defined `CSS_APPROACH` and design tokens.
3. **Accessibility**: Ensure semantic HTML and proper ARIA attributes for WCAG 2.1 AA compliance.
4. **Responsiveness**: Verify UI behavior across mobile, tablet, and desktop viewports.

## Phase 3: Reliability & Verification

1. **Unit Tests**: Write unit tests for complex UI logic if required by the plan.
2. **Linting**: Ensure code passes `bun run lint` and `bun run check`.

## Phase 4: Delivery

1. **Architect Review**: Request review from `fe-architect`.
2. **Iteration**: Fix visual and functional bugs reported by `fe-reviewer`, `fe-qa`, or `fe-aqa`.

## Gotchas

- **Framework Choice**: Always check environment variables; never assume a framework.

- **A11y**: Accessibility is a first-class citizen; don't skip it.

- **Performance**: Avoid unnecessary re-renders or large unoptimized assets.

## Validation Loop

The Frontend Developer validates that the UI is not only functional and pixel-perfect but also accessible and performant.
