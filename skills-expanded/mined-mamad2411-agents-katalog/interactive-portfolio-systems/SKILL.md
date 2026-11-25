---
name: interactive-portfolio-systems
description: Build interactive personal portfolio sections for AI/ML work using no-build React, plain JavaScript, and CSS. Use when Codex is asked to add filters, galleries, case-study panels, project explorers, skill matrices, evidence dashboards, or interactive portfolio storytelling.
---

# Interactive Portfolio Systems

Use this skill to turn a static portfolio into an interactive, evidence-backed product experience without adding a build system.

## Workflow

1. Keep data in small arrays near the relevant component in `src/app.js`.
2. Make the first interaction obvious from structure, not explanatory text.
3. Prefer controls that reveal stronger evidence: filters, segmented views, expandable case studies, scorecards, timelines, or project matrices.
4. Store UI state with plain React hooks from the vendored React runtime.
5. Keep interactions accessible with semantic buttons, labels, focus states, and ARIA only where needed.
6. Add stable layout constraints so labels, hover states, and dynamic content cannot shift the page.
7. Verify mobile tap targets, keyboard navigation, reduced motion, and no horizontal overflow.

## AI/ML Portfolio Patterns

- Project cards should show problem, method, stack, result or validation plan, and status.
- Use evidence labels such as `Prototype`, `Research`, `Evaluation`, `Deployment`, or `Roadmap`.
- Make retrieval, OCR, computer vision, and optimization work legible through diagrams, metrics, pipeline steps, or concise capability chips.
- Do not overstate model quality. Label inferred or planned outcomes clearly.

## No-Build Constraints

- Do not add npm, bundlers, JSX transforms, or external runtime dependencies.
- Use `React.createElement`, browser APIs, and CSS custom properties.
- Keep animation and interaction code understandable enough to maintain in one file.

