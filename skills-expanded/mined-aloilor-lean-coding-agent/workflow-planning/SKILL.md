---
name: workflow-planning
description: Orchestration workflow for planning requested work without implementing it.
disable-model-invocation: true
---

# Planning Workflow

Use this workflow when the user wants to explore and approve a plan before work starts. It can cover feature work, bug fixes, refactoring, or another scoped change. It ends with an approved plan and does not implement the work.

The main agent orchestrates this workflow and owns user communication. Follow the shared scaffolding in `AGENTS.md` — **Workflow Delegation**, **Standard Artifacts**, and **Shared Stop Conditions**.

## Steps

1. **Prepare the plan.** Spawn `planner` with the request and the planning requirements. The planner runs `$lean-grill-with-docs`, examines relevant project context, and drafts `.agents/plans/plan_YYYYMMDD_<name>.md`. Relay material questions to the user and return answers to the planner.
2. **Review and approve the plan.** Present the completed plan to the user and obtain explicit approval. Send requested revisions to the same planner and present the updated plan.
3. **Stop at the plan.** Once approved, return the plan as the durable handoff for a later task. Do not spawn implementation or review agents and do not begin implementation.

The plan should match the request's scope and include relevant decisions, boundaries, non-goals, acceptance criteria, implementation approach, risks, and verification expectations. Avoid detailed technical design unless requested or required by documented architecture. For bug-related plans, distinguish evidence from hypotheses and identify any diagnosis that remains necessary before repair.

In the final response, link the approved plan and summarize its scope, key decisions, acceptance criteria, risks, and verification expectations.
