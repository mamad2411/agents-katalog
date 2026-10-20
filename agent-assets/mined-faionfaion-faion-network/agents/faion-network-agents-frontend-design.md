# Frontend Design

## Summary

**One-sentence:** Run a multi-phase workflow that produces 3-5 distinct UI design variants, picks one by taste, and ships components colocated with stories and tests.

**One-paragraph:** Solopreneur-scale UI projects move from fixed requirements (type, style, tech) to 3-5 distinct design variants differing in navigation pattern and information density, rendered to screenshots for comparison, selected by human taste, defined as design tokens before components, scaffolded with Storybook on pinned versions, and delivered as components colocated with stories and tests. Output is a frontend spec + token system + component library scaffolded in Storybook.

**Ефективно для:**

- Greenfield UI projects where the visual direction is open.
- Redesigns where stakeholders need to compare distinct directions rather than iterate one.
- Token + component-library decisions made before any production component lands.
- Solopreneur or small-team contexts without a dedicated design system team.

## Applies If (ALL must hold)

- Project ships a UI with non-trivial component count (>=20 components).
- Visual direction is undecided or being deliberately revisited.
- Tech stack supports Storybook (React/Vue/Svelte/Angular/Web Components).
- Engineer has authority to pick design direction (no enforced design system to inherit).

## Skip If (ANY kills it)

- Existing design system locks all visual decisions — no design phase needed.
- Project is a one-page marketing site — variant generation overhead exceeds value.
- Team has a dedicated design crew — handoff workflow differs.
- Component count <=5 — direct build is faster than the workflow.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Brief: app type, style direction, tech stack (React/Vue/etc) | doc | product |
| Component inventory (estimated count + key flows) | list | tech-lead |
| Storybook version + framework adapter pinned | config | platform |
| Screenshot tooling (Playwright or Chromatic) for variant render | tool | platform |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| [[design-tokens]] | Tokens are defined before components. |
| [[ui-component-library]] | Component library structure follows separately. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 testable rules (3-5 distinct variants, screenshot before decide, tokens before components, Storybook pinned versions, colocate story+test+component) | 900 |
| `content/02-output-contract.xml` | essential | JSON Schema for frontend spec + valid/invalid examples | 900 |
| `content/03-failure-modes.xml` | essential | 4 antipatterns with symptom/root-cause/fix | 800 |
| `content/04-procedure.xml` | essential | 6-step procedure: fix-requirements → variants → screenshots → select → tokens → scaffold | 800 |
| `content/05-examples.xml` | essential | Worked example: SaaS dashboard variant comparison | 700 |
| `content/06-decision-tree.xml` | essential | Routing tree → rule from 01-core-rules.xml | 500 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `variant_generation` | opus | Generating truly distinct variants requires deep visual synthesis. |
| `screenshot_render` | sonnet | Mechanical: run Playwright against each variant. |
| `token_extraction` | sonnet | Extract values from chosen variant for token system. |
| `storybook_scaffold` | sonnet | Storybook setup with pinned versions + addons. |

## Templates

| File | Purpose |
|------|---------|
| `templates/frontend-spec.md` | Frontend design spec skeleton: brief, variant set, chosen variant, tokens, Storybook pin, planned components. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/render-variants.sh` | Playwright/Chromatic script to render variant screenshots | Wave 3 of procedure: screenshot all variants |
| `scripts/validate-frontend-design.py` | Validate the frontend spec artefact against 02-output-contract schema | Pre-publish gate / pre-commit |

## Related

- [[design-tokens]]
- [[ui-component-library]]
- [[tailwind-architecture]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps project scope, design ownership, and component count to a rule from `01-core-rules.xml`, telling the agent whether to run the full design workflow or skip when the design direction is fixed by inheritance. Walk it on every fresh invocation; do not memo-ise outcomes across distinct engagements.
