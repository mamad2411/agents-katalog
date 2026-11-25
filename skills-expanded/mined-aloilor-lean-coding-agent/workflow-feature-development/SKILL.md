---
name: workflow-feature-development
description: Workflow for feature and change requests, from small changes through complex externally observable behavior.
disable-model-invocation: true
---

# Feature Development Workflow

Use this workflow for clear, small changes and complex or cross-cutting features. The approved plan records the requirements, scope, constraints, acceptance criteria, risks, and verification needed for the work. Every run produces the standard durable plan, implementation report, and review pass artifacts.

The main agent orchestrates this workflow and owns user communication and closeout. Follow the shared scaffolding in `AGENTS.md` — **Workflow Delegation**, **Standard Artifacts**, and **Shared Stop Conditions**.

## Steps

1. **Plan and approve.** Spawn `planner` with the request and this workflow's planning requirements. The plan covers behavior, scenarios, non-goals, contracts, constraints, acceptance criteria, implementation approach, risks, and verification. The main agent obtains explicit user approval of the plan before implementation.
2. **Implement test-first.** After plan approval, spawn `implementer` with the approved plan. Apply `$tdd`; drive each behavior through RED, GREEN, and REFACTOR. The implementer records its TDD and verification evidence in `.agents/implementation-reports/implementation_YYYYMMDD_<name>.md`.
3. **Review independently.** Spawn `code-reviewer` with the approved plan, implementation report, touched files, tests, and verification evidence. The reviewer checks correctness, security, test-first evidence, SOLID, DRY, YAGNI, KISS, and code smells, then records each pass under `.agents/code-reviews/review_YYYYMMDD_<name>_pass_N.md` and returns `APPROVE`, `WARNING`, or `BLOCK`.
4. **Resolve and verify.** On `BLOCK`, send only the concrete findings back to `implementer`, preserve the approved plan, rerun the relevant checks, and repeat review until `APPROVE` or a Shared Stop Condition triggers. Treat `WARNING` as actionable when tied to the plan, a likely bug, security/privacy, or a meaningful test gap.
5. **Close out.** Run the relevant focused and broader verification for the change, with broader checks whenever it touches shared behavior, API contracts, persistence, auth, security, or user-facing workflows. Inspect the final diff and report residual risks and omissions.

In the final response, identify the artifact paths, independent reviewer verdict, and main-agent closeout review. Report the implemented behavior, exact verification results, residual risks, and omissions.
