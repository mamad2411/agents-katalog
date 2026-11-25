---
name: itsol-task-intake
description: "Classify task mode and risk, then route the smallest ITSOL process and domain skill set."
---

# ITSOL Task Intake

Classify work before changing code. Resolve `itsol-workflow-mode` before functional, bugfix, planning, implementation, or delegation gates.

## Intake

1. Inspect the request, repository context, and applicable `.itsol.md` policy.
2. Record all seven fields: `workflow_mode`, `mode_source`, `decision_authority`, `scope`, `artifact_state`, `execution_mode`, and `protected_constraints`. Missing, inconsistent, or restriction-conflicting state is `blocked`.
3. Classify the task: requirements, feature, bug, planning, review, self-review, QA, deployment, incident, data, security, or mixed.
4. Identify user-visible outcome, affected systems, risk, security/data impact, ambiguity, and current-tech research needs.
5. Route the smallest process and domain set; use `itsol-repo-memory` first when `.itsol.md` exists.
6. Functional work: load `itsol-functional-planning` and `itsol-requirements-review`; preserve mode semantics—governed keeps discovery/plans/review/approval/execution gates, autonomous-planned creates and reviews plans then uses `Ready for execution`, direct omits persistent plans and planning gates.
7. Bugfixes retain evidence and regression verification in every mode; defer Fix Plan gates to `itsol-workflow-mode` and `itsol-bug-debugging`.
8. Keep protected-action authority separate and propagate complete state through handoffs and packets.

Do not modify files, spawn nested subagents, or invoke external agent CLIs from intake.

## Execution policy

Load `itsol-execution-policy` after workflow mode whenever resource, stop, delegation, or completion state matters. It owns budgets and evidence validation; never use `maxTurns` or termination as completion. Preserve `partial`, `blocked`, and `failed`.

## Focused references

- [01-overview.md](./references/01-overview.md) — task types, process, and subagent routing.
- [02-etap-2-doprecyzowanie-brakow.md](./references/02-etap-2-doprecyzowanie-brakow.md) — ambiguity, impact, help, and status.
- [03-definicja-gotowosci-zadania-do-implementacji.md](./references/03-definicja-gotowosci-zadania-do-implementacji.md) — readiness definition and junior/mid standard.
