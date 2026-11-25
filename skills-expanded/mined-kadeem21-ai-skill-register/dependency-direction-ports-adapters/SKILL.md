---
name: dependency-direction-ports-adapters
description: Introduce ports and adapters with clear dependency direction so domain logic stays isolated from integrations. Use during architecture refactor or new subsystem design.
---

# Dependency Direction and Ports/Adapters

## Goal
Keep integrations replaceable and domain logic pure.

## Workflow
1. Read `../_shared/PROTOCOL.md` and align with task objective.
2. Read `../_shared/skill-usage-policy.md` and apply activation/escalation rules.
3. Collect repository evidence from source-of-truth files before proposing edits.
4. Produce required artifact for this skill.
5. Add explicit verify step and fail condition.
6. Stop and escalate if verify fails after two hypothesis changes.
7. Finish with summary from `../_shared/artifact-summary-template.md`.

## Required Output
Port list (interfaces), adapter list (implementations), and placement rules.

## Verify Gate
Confirm domain modules reference only ports, not adapter implementations.

## Safety Rules
- Fail closed for risky work: architecture, refactor, release, config, or dependency changes.
- Do not exceed change budget without explicit escalation note.
- Do not repeat failing command without changing approach.
