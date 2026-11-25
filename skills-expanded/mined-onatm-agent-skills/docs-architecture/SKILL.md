---
name: docs-architecture
description: Maintain system and domain architecture docs such as `docs/ARCHITECTURE.md`, `web-architecture.md`, or `api-architecture.md`. Use when topology, shared patterns, cross-component flows, deployment model, or ownership boundaries change.
---

# Docs Architecture

Maintain architecture-level docs without drifting into component internals or feature copy. Keep root and domain architecture docs aligned with the current topology and the docs they index.

## Resource Map

- Use `assets/doc-starters/architecture-doc.md` when creating or substantially rewriting `docs/ARCHITECTURE.md` or a domain architecture doc such as `web-architecture.md`.
- Read `references/architecture-example.md` when you need a worked example of the expected level of abstraction.

## When to Use

- New system boundary, pipeline stage, deployment model, or ownership boundary
- Changes to shared patterns used across multiple services or features
- Updates to architecture index docs that link to `docs/designs/` or `docs/features/`
- Domain architecture docs describing reusable patterns, topology, or trust boundaries

## Do Not Use

- Component or service implementation detail that belongs in `docs-components-design`
- Feature behavior, user flows, or product narrative that belongs in `docs-feature-design`

## Workflow

1. Identify the target architecture doc and its scope.
- Root architecture doc for the whole system
- Domain architecture doc for a shared surface such as web, API, or data

2. Update only architecture-level content.
- System or domain boundaries
- Shared principles and patterns
- Cross-component data or control flow
- Runtime, deployment, trust boundaries, and ownership

3. Keep architecture docs as index docs.
- Link to related `docs/designs/` and `docs/features/` docs
- Summarize shared behavior instead of duplicating component internals

4. Verify truth-bearing details.
- Active components and boundaries match the current code
- Flows, contracts, and ownership are still accurate
- Security and operations notes reflect the live system

5. Trim stale detail.
- Remove implementation walkthroughs that belong in component docs
- Remove feature-level behavior copy that belongs in feature docs

## Writing Rules

- Focus on topology, boundaries, and shared patterns
- Explain why the system is shaped this way, not every internal step
- Prefer concise diagrams and links over long prose dumps
- Treat the doc as an index and coordination surface, not a full implementation manual

## Quality Checklist

- The doc clearly states its scope and boundaries
- Shared patterns and cross-component flows are current
- Links to related design and feature docs are synchronized
- Component-level internals are linked out instead of duplicated
- Security, operations, and ownership notes reflect current behavior
