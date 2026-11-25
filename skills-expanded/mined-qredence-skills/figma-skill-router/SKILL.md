---
name: figma-skill-router
description: "Use when a Figma Design agent must choose one installed Figma skill for a request or design-file context."
---

# Figma Skill Router

Choose exactly one installed Figma skill for the current request. Skip this router when a narrower matching skill is already invoked.

## Routing Rules

1. Read the user goal, requested action, and strongest available context: selection, page, file, library, comments, branch, PRD, code, or none.
2. Choose the narrowest skill whose trigger and supported context match the request.
3. Prefer review skills for verbs such as `audit`, `review`, `check`, or `find`; prefer apply skills for verbs such as `fix`, `apply`, `migrate`, or `standardize`.
4. Route to one skill only. Do not invoke, chain, or mention multiple skills in the same handoff.
5. Ask once only when a missing input prevents a safe route. Otherwise state the scope assumption.

## Capability Gate

Route only to work the current Figma surface can support. For prototype interactions, exports, vector editing, diagrams, data visualizations, external code, analytics, branches, or admin data, prefer a planning or review skill unless the required capability and context are explicitly available in the session.

## Catalogue Index

Use the request noun and verb to choose within the relevant group.

| Area | Installed skills |
| --- | --- |
| Discover and define | `design-brief-generator`, `build-from-prd`, `persona-builder`, `journey-map-builder`, `workshop-facilitator`, `affinity-mapping`, `sticky-synthesis`, `competitive-teardown`, `deck-from-outline` |
| Content and brand | `content-inventory`, `content-tone-review`, `microcopy-generator`, `localization-readiness`, `brand-kit-asset-generator` |
| Layout and construction | `container-layout-normalizer`, `responsive-breakpoint-check`, `spacing-scale-enforcer`, `figma-to-code-component`, `base-ui-primitive-composition`, `shadcn-component-structure`, `cva-variant-generator` |
| Components and libraries | `component-audit`, `component-naming-sync`, `library-health-report`, `follow-ds-guidelines`, `design-tokens-sync`, `legacy-styles-to-variables`, `apply-color-variables`, `color-token-format-normalizer`, `semantic-color-audit`, `shadcn-theme-variables` |
| Review and quality | `accessibility-audit`, `heuristic-evaluation`, `design-crit`, `visual-consistency-check`, `states-completeness-check`, `site-launch-checklist`, `prototype-qa`, `animation-consistency-check` |
| Prototypes and motion | `prototype-from-flow`, `wire-up-interactions`, `variable-driven-prototype`, `motion-spec-generator` |
| Code, changes, and handoff | `code-connect-mapper`, `dev-handoff-prep`, `handoff-summary`, `token-tailwind-theme-sync`, `tailwind-class-order-check`, `design-change-diff`, `branch-review-summary` |
| File operations | `file-cleanup`, `rename-layers-batch`, `naming-convention-enforcer` |
| Collaboration and utilities | `comment-triage`, `plugin-widget-recommender` |

## Tie-Breakers

Use `shadcn-theme-variables` for creating or repairing semantic shadcn theme variables in Figma; use `token-tailwind-theme-sync` when Figma variables are already defined and code theme files need to catch up. Use `component-audit` for one component set and `library-health-report` for a library-wide review. Use `microcopy-generator` to write copy and `content-inventory` to enumerate it. Use `design-crit` for broad design feedback, `heuristic-evaluation` for usability, and `accessibility-audit` for accessibility. Use `journey-map-builder` to map an experience and `prototype-from-flow` to specify a screen flow. For unmatched requests, use `design-brief-generator` for new work or `design-crit` for improvement work.

## Handoff

Return only:

```markdown
Primary skill: `<skill-name>`
Why: <request and matching context in one sentence>
Scope: <selection, page, file, or explicit assumption>
Capability note: <only when relevant>
```

Do not list alternatives, perform the routed work, recommend a dependent skill, or send more than one skill to the same request.