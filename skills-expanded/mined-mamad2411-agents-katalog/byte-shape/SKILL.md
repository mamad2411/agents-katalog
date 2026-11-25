---
name: byte-shape
description: Shape a Your ByteDance / Byte OS project into product positioning, MVP scope, non-goals, user flows, UX structure, technical direction, metrics, OKRs, and an initial roadmap. Use after byte-start or byte-research, or when the user asks to define what the product should be before implementation.
---

# Byte Shape

Shape turns the foundation into a product that can be planned and built. It should reduce ambiguity, not expand it.

## Inputs

Read:

```text
.byte-os/BYTE.md
.byte-os/OKRS.md
.byte-os/RESEARCH.md
.byte-os/COMPETITORS.md
.byte-os/USER_ASSUMPTIONS.md
.byte-os/DECISIONS.md
```

If Byte OS state is missing, run or recommend `byte-start`.

## Workflow

Run a project-group shaping pass:

- Product Manager: positioning, MVP, non-goals, priority.
- UX Researcher: core jobs, scenarios, user journey.
- Product Designer: information architecture, screens, flows, interaction model.
- Tech Lead: architecture direction, integrations, data model risks.
- Growth Analyst: activation, retention, monetization, referral surfaces.
- QA Engineer: edge cases and acceptance criteria.
- Product Director: final product tradeoffs.

Use the Your ByteDance style: make context visible, be candid about weak assumptions, and tie scope decisions to measurable impact.

Use actual subagents only when explicitly authorized. Otherwise synthesize roles inline.

## Decisions To Make

Define:

- Product promise in one sentence
- Primary user and secondary users
- First core workflow
- MVP scope
- Explicit non-goals
- Feature priority
- Key screens or surfaces
- Data objects
- Integrations
- Metrics
- Objective and Key Results alignment
- Risks
- Version 0 delivery boundary

## Artifacts

Write or update:

```text
.byte-os/PRODUCT_SPEC.md
.byte-os/UX_SPEC.md
.byte-os/TECH_SPEC.md
.byte-os/ROADMAP.md
.byte-os/OKRS.md
.byte-os/STATUS.md
.byte-os/DECISIONS.md
```

`PRODUCT_SPEC.md` must include:

- Positioning
- Target users
- Problems and jobs to be done
- MVP
- Non-goals
- Requirements
- Acceptance criteria

`UX_SPEC.md` must include:

- Core user journey
- Screen or page list
- Navigation model
- Empty, loading, error, and success states
- First-run experience

`TECH_SPEC.md` must include:

- Proposed architecture
- Data model
- APIs or integrations
- Implementation risks
- Testing strategy

`ROADMAP.md` must include:

- v0 deliverable
- v1 improvements
- Later opportunities

Update `STATUS.md`:

```text
Stage: shaped
Next recommended command: byte-plan
```

## Completion Criteria

The step is complete when a team can create executable plans without asking what the product is supposed to do.
