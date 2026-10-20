---
name: development-lifecycle
description: "Klasik SDLC ve Ajansal Geliştirme Yaşam Döngüsü (ADLC) için rehber: planlama, tasarım, uygulama, test ve dağıtım aşamalarını kapsar."
---

# Development Lifecycle (SDLC ↔ ADLC)

## Overview

Run work as a **defined process**, not ad-hoc expert calls. This skill maps each lifecycle
phase to the concrete skill / agent / slash-command to use, and helps choose between the
classic **SDLC** (human-driven) and the **ADLC** (agent-driven) for a task.

Pick a lane, then execute phase by phase. Skip phases deliberately, never accidentally.

## Choosing SDLC vs ADLC

- **SDLC** — human owns each phase; agents assist. Default for high-risk, regulated, or
  ambiguous work where a human gate per phase is required.
- **ADLC** — agents own execution across phases; human steers via eval/approval. Default for
  well-scoped, repeatable work where the PRD and skills are clear.
- They share the same spine. The big difference: in ADLC, **planning/PRD/skills evolve
  dynamically** and sub-agents run phases in parallel; in SDLC phases are sequential gates.

## SDLC — phase → what to use

| Phase | Use |
| :--- | :--- |
| Planning | `dev-planning-and-task-breakdown`, `dev-writing-plans`, `pm-sprint-plan`, `pm-outcome-roadmap` · agent `spec-planner` |
| Requirements | `pm-create-prd`, `dev-to-prd`, `pm-user-stories`, `dev-idea-refine` · agent `spec-analyst` |
| System Design | `dev-dotnet-architecture-selection`, `dev-system-design-scaling`, `dev-api-and-interface-design` · agent `spec-architect`, `backend-architect` · rule `architecture.md` |
| Implementation | `dev-executing-plans`, `dev-incremental-implementation`, `dev-tdd`, `dev-low-level-design` · agent `spec-developer` + language pros · cmd `/mutfak-bootstrap` |
| Testing & QA | `dev-test-driven-development`, `dev-qa` · agent `spec-tester`, `qa-expert`, `test-automator` · cmd `/mutfak-test-all` |
| Deployment | `dev-ci-cd-and-automation`, `dev-shipping-and-launch` · agent `deployment-engineer` · cmd `/mutfak-deploy` |
| Maintenance | `dev-deprecation-and-migration` · agent `legacy-modernizer`, `debugger` · cmd `/mutfak-fix-issue` |
| Evaluation | `dev-observability-and-instrumentation` · agent `performance-engineer`, `spec-validator` · cmd `/mutfak-review` |

## ADLC — phase → what to use

| Phase | Use |
| :--- | :--- |
| Goal Definition | `dev-define-goal`, `dev-idea-refine`, `dev-brainstorming` |
| Build PRD | `pm-create-prd`, `dev-to-prd`, `dev-notion-spec-to-implementation` |
| Write Skills | `dev-skill-creator`, `dev-write-a-skill`, `dev-plugin-creator` + **capability-gaps** rule (grow the central library, don't solve once) |
| Orchestrate Agents | **`mutfak-spec-workflow` chain**, `tech-lead-orchestrator`, `agent-organizer`, `dev-subagent-driven-development`, `dev-dispatching-parallel-agents` |
| Autonomous Coding | `dev-subagent-driven-development`, `dev-agents-sdk`, `dev-executing-plans` · agent `spec-developer` |
| Autonomous Testing | `dev-test-driven-development`, `test-automator`, `spec-tester` |
| Eval & Observability | `dev-verification-before-completion`, `ali-eval`/`ali-self-eval`, `ali-observability-designer` · agent `spec-reviewer`, `spec-validator` |
| Deployment (auto CI/CD) | `dev-ci-cd-and-automation` · agent `deployment-engineer` |
| Monitoring & Feedback | `dev-observability-and-instrumentation`, `dev-sentry`, `ali-self-improving-agent` · agent `performance-engineer` |

## The spec-workflow spine (ready-made process)

For non-trivial features, drive the whole lifecycle with the `mutfak-spec-workflow` agents:

```
spec-analyst → spec-architect → spec-planner → spec-developer
            → spec-tester → spec-reviewer → spec-validator   (spec-orchestrator coordinates)
```

This is the SDLC executed agentically — each agent owns one phase with quality gates between.

## Workflow

1. **Classify** the task: risk, clarity, repeatability → choose SDLC or ADLC lane.
2. **Enter at the right phase** (don't redo settled phases; don't skip unsettled ones).
3. For each phase, invoke the mapped skill/agent/command above.
4. **Gate between phases:** verify exit criteria (PRD signed off, tests green, review clean)
   before advancing. In ADLC, the human gate is the *Eval & Observability* phase.
5. **Close the loop:** Monitoring & Feedback findings re-enter Planning/Goal as new work.

## Gotchas

- **Process theater** — running every phase for a one-line fix; scale the lifecycle to the task.
- **Skipping gates** — advancing with red tests or an unsigned PRD propagates rework downstream.
- **ADLC without skills** — orchestrating agents before the needed skills exist; write skills first
  (capability-gaps), or the agents improvise inconsistently.
- **No feedback loop** — shipping without Monitoring/Eval means drift goes unnoticed.

## Related

- Process rule (project): `.claude/rules/process.md`.
- New capability mid-process: `.claude/rules/capability-gaps.md`.
- Design altitude: `dev-low-level-design`, `dev-system-design-scaling`, `dev-dotnet-architecture-selection`.
