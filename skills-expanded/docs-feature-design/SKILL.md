---
name: docs-feature-design
description: Maintain feature docs that explain user-visible behavior, goals, flows, and business rules without implementation detail. Use when feature scope, user workflows, or product behavior changes.
---

# Docs Feature Design

Maintain docs that explain what a feature does and why it matters, not how it is implemented. A single component or service may support multiple features, so keep technical design out of feature docs and link it separately when needed.

## Resource Map

- Use `assets/doc-starters/feature-doc.md` when creating or substantially rewriting a doc in `docs/features/`.
- Read `references/feature-example.md` when you need a worked example of the expected behavior-focused depth.

## When to Use

- New feature definition or major feature revision
- Changes to user-visible behavior, primary flows, goals, rules, or constraints
- Updates to product scope, supported actors, or expected outcomes
- Feature docs that should stay understandable without reading implementation details

## Do Not Use

- API, schema, runtime, deployment, or internal control-flow detail that belongs in `docs-components-design`
- System topology or domain architecture that belongs in `docs-architecture`

## Workflow

1. Identify the feature, audience, and existing doc path.
- Default location is `docs/features/`
- Reuse an existing feature doc when one already exists

2. Capture behavior-level content only.
- User problem and goals
- Primary actors and entry points
- Main flows, states, and business rules
- User-visible edge cases, constraints, and outcomes
- Non-Goals, Audience / Actors, and Open Questions are optional — omit them when they don't add value for the feature
- "User-Facing Behavior" (flat bullet list) is a valid simpler alternative to formal numbered Primary Flows for straightforward features

3. Move technical detail out.
- If the draft starts describing APIs, schema, queues, retries, deployment, or internal implementation, link or create the relevant component design doc instead

4. Keep cross-links aligned.
- Link to relevant architecture and component docs
- Do not duplicate their content inside the feature doc

5. Verify the doc against the current product behavior.
- The described flows and rules match what the feature actually does
- The audience can understand the feature without technical context

## Writing Rules

- Speak about what the feature does, not how it is implemented
- Multiple features can map to one component or service; keep the feature doc centered on one user-facing capability
- Use product language, user states, and business rules
- Do not include API sections, schema sections, deployment notes, or implementation plans

## Quality Checklist

- The doc explains the user problem, goals, and primary flows
- Business rules and user-visible edge cases are clear
- Technical implementation detail is absent
- Links to relevant component or architecture docs are present when needed
- A non-implementer could understand the feature from the doc alone
