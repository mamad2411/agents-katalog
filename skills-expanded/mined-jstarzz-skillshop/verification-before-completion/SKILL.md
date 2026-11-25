---
name: verification-before-completion
description: "Gate completion claims behind fresh evidence that directly proves the claimed outcome. Use when before saying done, before PR or release, after final code change."
license: MIT
compatibility: "Agent Skills compatible hosts; optimized for coding agents with repository and test/tool access."
metadata:
  category: "meta"
  version: "0.1.0"
  maintainer: "SkillShop maintainers"
  maturity: "draft"
---

# Verification Before Completion

Gate completion claims behind fresh evidence that directly proves the claimed outcome.

## Activate when

- before saying done
- before PR or release
- after final code change

## Focus

- Primary mission: Gate completion claims behind fresh evidence that directly proves the claimed outcome.
- Use project/runtime evidence; this skill is a workflow, not a role-play persona.
- If another skill owns a deeper specialist concern, hand off instead of duplicating its entire workflow.

## Workflow

1. Write the exact claim you are about to make: fixed, passing, deployed, safe, compatible, fast, or complete.
2. Choose the fresh command, test, runtime check, diff inspection or external observation that could falsify that exact claim.
3. Run it after the final relevant change; stale evidence does not count.
4. Read the complete output including exit status, skipped tests, warnings, partial runs and scope limitations.
5. Check evidence scope: a unit test cannot prove a deployment, a build cannot prove a user journey, and one benchmark cannot prove sustained capacity.
6. If direct proof is unavailable, downgrade the wording and state what remains unverified.
7. Only then make the completion claim and include the evidence.

## Deliverables

- Evidence-based output for the skill's mission
- Explicit assumptions and unknowns
- Clear downstream actions
- A result that directly satisfies: Gate completion claims behind fresh evidence that directly proves the claimed outcome.

## Common failure modes

- Loading every available skill 'just in case'
- Replacing evidence with conversational confidence
- Producing a giant narrative when a compact reusable artifact would do
- Hiding uncertainty instead of stating what was not inspected, reproduced, measured, or verified.

## Composition

Use `skill-router` when this task needs multiple specialties. Prefer composition over copying another skill's workflow into this one.

## Exit criteria

- The requested decision, change, test, or review is supported by concrete evidence.
- Important residual risks, limitations, and unknowns are explicit.
- The output is specific enough for another engineer or agent to act on without reconstructing hidden reasoning.
