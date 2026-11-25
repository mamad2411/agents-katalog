---
name: system-map-module-map-generator
description: Generate concise module map with responsibilities, dependencies, and data flow, including a Mermaid diagram. Use for onboarding and architecture reviews.
---

# System Map and Module Map Generator

## Goal
Provide 10-minute project comprehension artifact.

## Workflow
1. Read `../_shared/PROTOCOL.md` and align with task objective.
2. Read `../_shared/skill-usage-policy.md` and apply activation/escalation rules.
3. Collect repository evidence from source-of-truth files before proposing edits.
4. Produce required artifact for this skill.
5. Add explicit verify step and fail condition.
6. Stop and escalate if verify fails after two hypothesis changes.
7. Finish with summary from `../_shared/artifact-summary-template.md`.

## Required Output
`SYSTEM_MAP.md` using `../_shared/system-map-template.md`.

## Verify Gate
Map includes all top-level modules and at least one end-to-end data flow.

## Safety Rules
- Fail closed for risky work: architecture, refactor, release, config, or dependency changes.
- Do not exceed change budget without explicit escalation note.
- Do not repeat failing command without changing approach.
