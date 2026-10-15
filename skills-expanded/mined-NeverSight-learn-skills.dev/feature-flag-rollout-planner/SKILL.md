---
name: feature-flag-rollout-planner
description: Vendor-neutral skill to generate a staged feature-flag rollout plan (phases, metrics, guardrails, rollback criteria) from feature context and risk inputs.
---

## When to invoke
- You are planning a safe rollout for a risky change.
- You want a consistent rollout template for engineering and product teams.

## Inputs needed
- Feature context: name, description, target users.
- Risk profile: data migrations, performance risk, external dependencies.
- Success metrics and guardrail metrics.
- Optional stakeholders and comms channels.

## Workflow
1. Validate inputs and normalize percentages/dates.
2. Propose rollout phases (internal, 1%, 10%, 50%, 100%) and duration.
3. For each phase, define:
   - enablement criteria
   - monitoring checklist
   - guardrails and rollback triggers
4. Produce comms checklist and ownership.

## Output format
Markdown rollout plan with:
- Overview
- Phased rollout table
- Monitoring and dashboards
- Rollback plan
- Communications checklist

## Guardrails
- If metrics are not provided, output placeholders instead of guessing.
- Include a default rollback trigger for error-rate regression.

## Reference code
- `plan_rollout.py` reads a JSON feature brief and writes Markdown rollout plan.
