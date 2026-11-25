---
name: angular-enterprise-architecture
description: Use when designing, reviewing, refactoring, or enforcing Angular application architecture with isolated lazy features, eager core/layout, reusable ui/pattern architecture building blocks, one-way dependency graphs, eslint-plugin-boundaries rules, or folder placement decisions. This skill takes precedence over angular-developer when architecture rules conflict with general Angular advice.
---

# Angular Enterprise Architecture

Use this skill for Angular architecture decisions before applying general Angular implementation guidance. If this skill conflicts with `angular-developer`, this skill wins for architecture, dependency direction, folder placement, and lazy/eager boundaries.

## Always Apply

- Keep the eager app minimal: `main.ts`, `app.*`, `core/`, and `layout/`.
- Implement every user-facing business flow as a lazy `feature/<feature-name>/`, even if the app currently has only one feature.
- Keep sibling lazy features isolated. A feature must not import implementation from another feature.
- Preserve a one-way dependency graph: more specific blocks may depend on simpler/shared blocks, never the reverse.
- Share by extracting one level up, not by importing sideways.
- Do not use `feature-shared`. A normal parent feature folder covers sharing between its own lazy sub-features.
- Implement automatic validation with the latest project-compatible `eslint-plugin-boundaries` flat config. Use the references in this skill as the starting point, then verify against the current JS Boundaries docs/package version before finalizing.

## Reference Routing

- For architecture and folder structure, including what to implement in each folder, read [placement.md](references/placement.md).
- For preserving the one-way dependency graph, lazy loading, and lazy feature isolation while sharing code, read [extract-one-level-up.md](references/extract-one-level-up.md).
- For standardized architecture building block definitions, folder structure, and dependency rules, read [building-blocks.md](references/building-blocks.md).
- For adding a new architecture building block and matching ESLint boundary type, read [adding-building-blocks.md](references/adding-building-blocks.md).
- For implementing or adapting ESLint enforcement, read [eslint.config.boundaries.js](references/eslint.config.boundaries.js). The provided config targets an Angular CLI polyrepo with multiple apps and libraries under `projects/`; for a single-app workspace it can be simplified and many `basePattern` entries can be omitted.

Terminology: use `architecture building block` for the concept, `folder` for its implementation location, and `ESLint boundary type` for the matching `eslint-plugin-boundaries` enforcement entry.
