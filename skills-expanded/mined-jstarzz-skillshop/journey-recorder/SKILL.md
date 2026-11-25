---
name: journey-recorder
description: "Record human or agent interactions as structured semantic journeys with browser, network and assertion evidence. Use when record workflow, capture QA session, turn use into tests."
license: MIT
compatibility: "Agent Skills compatible hosts; optimized for coding agents with repository and test/tool access."
metadata:
  category: "qa"
  version: "0.1.0"
  maintainer: "SkillShop maintainers"
  maturity: "draft"
---

# Journey Recorder

Record human or agent interactions as structured semantic journeys with browser, network and assertion evidence.

## Activate when

- record workflow
- capture QA session
- turn use into tests

## Focus

- Primary mission: Record human or agent interactions as structured semantic journeys with browser, network and assertion evidence.
- Use project/runtime evidence; this skill is a workflow, not a role-play persona.
- If another skill owns a deeper specialist concern, hand off instead of duplicating its entire workflow.

## Workflow

1. Declare the journey goal, actor, environment, starting state and preconditions.
2. Record semantic actions using route, accessible role/name, stable test id, domain action and state transition; coordinates are evidence only, never the canonical target.
3. Capture relevant screenshots, accessibility/DOM snapshots, console exceptions and network requests/responses/timings when tooling provides them.
4. Redact passwords, session cookies, Authorization headers, private API keys, full payment-card data and other secrets before persistence.
5. Mark dynamic values such as IDs, CSRF tokens, timestamps, transaction references and generated names so later compilation can extract/parameterize them.
6. Annotate business assertions after meaningful actions: record created, balance updated, permission denied, receipt visible—not just 'button clicked'.
7. Normalize the recording into `references/semantic-journey.schema.json`.
8. Version the semantic journey separately from generated target-specific tests so the canonical intent survives UI implementation changes.

## Deliverables

- Test charter or cases
- Defects with reproducible evidence
- Coverage gaps and regression candidates
- A result that directly satisfies: Record human or agent interactions as structured semantic journeys with browser, network and assertion evidence.

## Common failure modes

- Testing only the happy path
- Calling automated scanning 'manual QA'
- Brittle coordinate-only recordings with no semantic assertions
- Hiding uncertainty instead of stating what was not inspected, reproduced, measured, or verified.

## Composition

Use `skill-router` when this task needs multiple specialties. Prefer composition over copying another skill's workflow into this one.

## Exit criteria

- The requested decision, change, test, or review is supported by concrete evidence.
- Important residual risks, limitations, and unknowns are explicit.
- The output is specific enough for another engineer or agent to act on without reconstructing hidden reasoning.
