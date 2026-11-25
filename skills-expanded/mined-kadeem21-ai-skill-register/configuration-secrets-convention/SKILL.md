---
name: configuration-secrets-convention
description: Establish config loading hierarchy, startup validation, and secrets handling with no secrets committed to repository. Use for secure environment portability.
---

# Configuration and Secrets Convention

## Goal
Make configuration safe and deterministic across environments.

## Workflow
1. Read `../_shared/PROTOCOL.md` and align with task objective.
2. Read `../_shared/skill-usage-policy.md` and apply activation/escalation rules.
3. Collect repository evidence from source-of-truth files before proposing edits.
4. Produce required artifact for this skill.
5. Add explicit verify step and fail condition.
6. Stop and escalate if verify fails after two hypothesis changes.
7. Finish with summary from `../_shared/artifact-summary-template.md`.

## Required Output
Config hierarchy: default -> env -> local override, plus `.env.example` policy.

## Verify Gate
Startup validation must fail fast on missing required settings.

## Safety Rules
- Fail closed for risky work: architecture, refactor, release, config, or dependency changes.
- Do not exceed change budget without explicit escalation note.
- Do not repeat failing command without changing approach.
