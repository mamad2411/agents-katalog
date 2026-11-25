---
name: openspeq-plan
description: Plan a change with openspeq by staging repo-native specs, deltas, and decision logs before implementation.
---

# openspeq-plan

Use this skill when a user asks for a feature, refactor, migration, or bug fix that should be specified before implementation.

## Goal

Create a scoped planning workspace under `specs/_plans/<plan-name>/` and connect it to permanent specs.

## Inputs

- target repository root
- change request
- affected areas of the codebase

## Steps

1. Read the target repo's `specs/mission.md`.
2. Search existing permanent specs and `specs/decision-log.md` for overlapping behavior or prior decisions.
3. Inspect the code that will be affected.
4. Ask clarifying questions only if the change remains ambiguous after inspection.
5. Create `specs/_plans/<plan-name>/` with:
   - `plan.md` from `templates/plan-template.md`
   - `decision-log.md` when tradeoffs matter
   - one or more staged deltas using `templates/delta-template.md`
6. Keep deltas small and scenario-driven.
7. Identify validation commands before implementation starts.

## Recommended anchors

- MECE Partitioning for task breakdown
- Five Whys for bug analysis
- BDD / scenario language for behavior specs
- ADR promotion only for durable decisions; when a decision will constrain future architecture, use `/adr` rather than leaving it only in plan-level prose

## Constraints

- No vendor-specific prompt syntax in durable files.
- Prefer explicit verification commands over vague assurances.
- Scope the plan tightly enough that code and spec changes can be reviewed together.

## Outputs

- staged plan folder
- plan document
- staged spec deltas
- optional plan-level decision log
