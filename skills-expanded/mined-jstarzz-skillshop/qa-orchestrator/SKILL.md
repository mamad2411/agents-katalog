---
name: qa-orchestrator
description: "Plan and coordinate the right mix of exploratory, manual, automated, visual, API, data, accessibility, device and performance testing. Use when QA plan, release testing, choose test types."
license: MIT
compatibility: "Agent Skills compatible hosts; optimized for coding agents with repository and test/tool access."
metadata:
  category: "qa"
  version: "0.1.0"
  maintainer: "SkillShop maintainers"
  maturity: "draft"
---

# Qa Orchestrator

Plan and coordinate the right mix of exploratory, manual, automated, visual, API, data, accessibility, device and performance testing.

## Activate when

- QA plan
- release testing
- choose test types

## Focus

- Primary mission: Plan and coordinate the right mix of exploratory, manual, automated, visual, API, data, accessibility, device and performance testing.
- Use project/runtime evidence; this skill is a workflow, not a role-play persona.
- If another skill owns a deeper specialist concern, hand off instead of duplicating its entire workflow.

## Workflow

1. Read requirements, changed surfaces, business-critical journeys and known risk areas.
2. Classify each behavior by the cheapest test layer that can reliably prove it: unit, integration, API/contract, browser E2E, manual, visual, accessibility, device or performance.
3. Use exploratory/manual QA for discovery and human judgment; use automation for stable repeated regression value.
4. Select specialty skills only where applicable rather than running every QA dimension on every change.
5. Define test data, identities/roles, environment, devices/browsers and reset strategy.
6. Prioritize high-value/destructive flows such as payments, permissions, data mutation, onboarding and recovery.
7. Define evidence and exit criteria for pass/fail/blocker status.
8. Produce the QA matrix and route individual work to the selected skills.

## Deliverables

- Test charter or cases
- Defects with reproducible evidence
- Coverage gaps and regression candidates
- A result that directly satisfies: Plan and coordinate the right mix of exploratory, manual, automated, visual, API, data, accessibility, device and performance testing.

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
