---
name: frontend-design-system-orchestrator
description: "Orchestrates the frontend development lifecycle: from UI/UX design and design system tokens to component scaffolding, security scanning, and visual validation. Ensures consistent, accessible, and performant user interfaces. Keywords: frontend-design, ui-ux, tailwind, react, design-system, component-scaffolding, visual-validation."
version: 1
created: "2024-05-22"
updated: "2024-05-22"
---

# Frontend Design System Orchestrator - Consistent UI Development

This skill manages the transition from design concepts to production-ready frontend components. It ensures that every UI element is consistent with the design system, secure, accessible, and visually correct.

## When to Use
Use this skill when:
- Building a new product's UI/UX.
- Developing a reusable component library.
- Implementing a new design system.
- Auditing an existing frontend for visual and security issues.

## The Orchestrated Workflow
This skill executes the following phases in sequence:

### Phase 1: Design & Foundations
1. **UI/UX Design**: Invoke `ui-ux-designer` to create wireframes, design tokens, and user flows.
2. **Design System Setup**: Invoke `tailwind-design-system` to establish the tokenized styling, component libraries, and responsive patterns.

### Phase 2: Component Development
3. **Component Scaffolding**: Invoke `frontend-developer` to build React components using TypeScript, hooks, and the established design tokens.
4. **State Management**: Invoke `react-state-management` to manage global and server state effectively.

### Phase 3: Security & Quality
5. **Security Scanning**: Invoke `frontend-security-coder` to check for XSS vulnerabilities and client-side security issues.
6. **Visual Validation**: Invoke `ui-visual-validator` to verify that the final implementation matches the design specifications and accessibility standards.

## Freedom Calibration & Constraints
- **Constraint Level: Medium**
  - **Rigidity**: The sequence of Design $\rightarrow$ Tokens $\rightarrow$ Components $\rightarrow$ Validation is mandatory.
  - **Freedom**: The specific UI components and layout choices are left to the designer and developer's collaboration.

## Critical Anti-Patterns (NEVER List)
| Anti-Pattern | Description | Alternative / Solution |
| :--- | :--- | :--- |
| **NEVER** hardcode colors | Hardcoding hex codes bypasses the design system. | Always use design tokens from `tailwind-design-system`. |
| **NEVER** skip visual validation | UI "looks" correct but may have accessibility or alignment issues. | Always run `ui-visual-validator`. |
| **NEVER** ignore client-side security | Trusting user input on the frontend leads to XSS. | Invoke `frontend-security-coder` for every new component. |

## Verification
1. A design system with tokens and components is established.
2. New features are built using the established system.
3. Components pass security and visual validation checks.
4. Accessibility standards are met across all new UI.
