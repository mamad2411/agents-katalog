---
name: workflow-refactor
description: Workflow for behavior-preserving restructuring, from local cleanup through complex refactors.
disable-model-invocation: true
---

# Code Refactoring Workflow

Use this workflow for clear, small, localized refactors and complex behavior-preserving restructuring. The approved plan records the behavior and contracts to preserve, scope, risks, documentation impact, and verification needed for the work. Every run produces the standard durable plan, implementation report, and review pass artifacts.

The main agent orchestrates this workflow and owns user communication and closeout. Follow the shared scaffolding in `AGENTS.md` — **Workflow Delegation**, **Standard Artifacts**, and **Shared Stop Conditions**.

## Steps

1. **Plan and approve.** Spawn `planner` with the request and this workflow's planning requirements. The plan records current behavior and contracts to preserve, boundaries, baseline and post-refactor verification, behavior-drift and rollback risks, and documentation impact. The main agent obtains explicit user approval before implementation. If the work reveals behavior change, stop and request user direction; do not switch workflows automatically.
2. **Establish the baseline and refactor in green steps.** After plan approval, spawn `implementer` with the approved plan. Apply `$refactor` and the test-strategy guidance from `$tdd`. Run focused tests before restructuring; add characterization tests when behavior to preserve is uncovered. Make one small behavior-preserving change at a time and rerun focused tests after each meaningful step. The implementer records its TDD, baseline, documentation, and verification evidence in `.agents/implementation-reports/implementation_YYYYMMDD_<name>.md`.
3. **Review independently.** Spawn `code-reviewer` with the approved plan, implementation report, touched files, tests, and verification evidence. The reviewer checks behavior drift, scope creep, missed tests, unnecessary abstraction, code smells, and documentation staleness. Missing or stale required documentation is a `BLOCK`. Each review pass is recorded under `.agents/code-reviews/review_YYYYMMDD_<name>_pass_N.md`.
4. **Resolve and verify.** On `BLOCK`, send only the concrete findings back to `implementer`, preserve the approved plan, rerun focused checks, and repeat review until `APPROVE` or a Shared Stop Condition triggers. Treat `WARNING` as actionable when tied to the plan, behavior drift, or a meaningful test gap. Run broader final verification whenever shared behavior, API contracts, persistence, auth, security, or user-facing workflows are touched.

In the final response, identify the artifact paths, independent reviewer verdict, and main-agent closeout review. Report the preserved behavior, structural improvement, exact verification results, residual risks, and omissions.
