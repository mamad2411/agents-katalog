---
allowed-tools: Read,Glob,Grep,Bash,Edit,Write
description: Turn a PRD into a phased implementation plan using tracer-bullet vertical slices, saved to ./plans/
argument-hint: [path/to/prd.md or 'in context']
model: opus
---

# Purpose

Convert a PRD (Product Requirements Document) into a phased implementation plan organized as tracer-bullet vertical slices. Each phase cuts through ALL integration layers end-to-end. Output is a Markdown file saved to `./plans/`. Follow the Instructions and Workflow sections below.

## Variables

PRD_SOURCE: $ARGUMENTS

## Instructions

- The PRD should already be in conversation context OR the user provides a file path via PRD_SOURCE. If neither, ask the user to paste the PRD or provide a path.
- Explore the codebase to understand current architecture, existing patterns, and integration layers before planning.
- Identify durable architectural decisions first — things unlikely to change across phases: route structures, DB schema shape, key data models, auth approach, third-party service boundaries.
- Break the PRD into tracer-bullet phases. Each phase is a thin VERTICAL slice through every layer (schema, API, UI, tests) — NOT a horizontal slice of one layer.
- Each slice must be demoable or verifiable on its own.
- Prefer many thin slices over few thick ones.
- Do NOT include specific file names, function names, or implementation details likely to change as later phases are built.
- DO include durable decisions: route paths, schema shapes, data model names.
- Present the proposed breakdown to the user and ask: does the granularity feel right? Should any phases be merged or split?
- Iterate until the user approves the breakdown.
- Only after approval, write the plan file to `./plans/` using the Plan Template.
- ULTRATHINK about the vertical slice boundaries — each phase should be independently valuable.

## Workflow

1. If PRD_SOURCE is a file path, read it. If PRD_SOURCE is 'in context' or empty, confirm the PRD is already in conversation. If not available, ask the user.
2. Explore the codebase — start with README.md, then scan key directories to understand architecture, patterns, and integration layers.
3. Identify durable architectural decisions that apply across all phases (routes, schema, models, auth, external services).
4. Draft vertical slices — break the PRD into tracer-bullet phases where each phase cuts end-to-end through every layer.
5. Present the proposed phase breakdown to the user as a numbered list showing each phase's title and which user stories it covers. Ask if granularity is right and if any phases should be merged or split.
6. Iterate on the breakdown until the user approves.
7. Create `./plans/` directory if it doesn't exist.
8. Write the plan file as `./plans/<feature-name>.md` using the Plan Template below.

### Plan Template

```md
# Plan: <Feature Name>

> Source PRD: <brief identifier or link>

## Architectural decisions

Durable decisions that apply across all phases:

- **Routes**: ...
- **Schema**: ...
- **Key models**: ...
- (add/remove sections as appropriate)

---

## Phase 1: <Title>

**User stories**: <list from PRD>

### What to build

A concise description of this vertical slice. Describe the end-to-end behavior, not layer-by-layer implementation.

### Acceptance criteria

- [ ] Criterion 1
- [ ] Criterion 2
- [ ] Criterion 3

---

## Phase 2: <Title>

**User stories**: <list from PRD>

### What to build

...

### Acceptance criteria

- [ ] ...

<!-- Repeat for each phase -->
```

## Report

Return the path to the created plan file and a summary list of the phases with their titles.