---
name: workflow-bug-fixing
description: Workflow for bugs, failing tests, CI failures, runtime errors, and regressions, from local repairs through consequential investigations.
disable-model-invocation: true
---

# Bug Fixing Workflow

Use this workflow for bugs and failures. Every run produces a user-approved plan, an implementation report, and review-pass artifacts. The plan records the symptom, evidence, likely root cause, impact, proposed repair, verification, and non-goals in proportion to the failure's consequences.

Create an incident report only on request; offer one for an outage, data loss, or security exposure.

The main agent orchestrates this workflow and owns user communication, repair approval, and closeout; `bug-diagnostician` owns investigation. Follow the shared scaffolding in `AGENTS.md` — **Workflow Delegation**, **Standard Artifacts**, and **Shared Stop Conditions**.

## Steps

1. **Investigate and plan.** Spawn `planner` with the request and this workflow's planning requirements. After it signals grill completion, spawn `bug-diagnostician` to inspect the relevant code, callers, tests, project context, and documentation and return its investigation, drafting `docs/incidents/incident_YYYYMMDD_<name>.md` only if requested. Return that investigation to the same planner to incorporate its evidence and the repair contract into the plan.
2. **Approve the repair plan.** The main agent presents the completed plan with the symptom, evidence or likely root cause, proposed repair, impact, and verification plan. Obtain explicit user approval of the plan before changing production or test code; this approval authorizes only the repair described in that plan.
3. **Reproduce and fix test-first.** After plan approval, spawn `implementer` with the approved plan and any incident report. Apply `$tdd`; prefer an existing failing test, otherwise add the smallest focused regression test and observe RED. Make the smallest root-cause change that turns the regression test GREEN, then refactor only while green. Record the TDD and verification evidence in `.agents/implementation-reports/implementation_YYYYMMDD_<name>.md`.
4. **Review independently.** Spawn `code-reviewer` with the approved plan, implementation report, changed files, tests, verification evidence, and any incident report. The reviewer checks root-cause correctness, regression coverage, security, scope, and code smells, records each pass under `.agents/code-reviews/review_YYYYMMDD_<name>_pass_N.md`, and on `APPROVE` finalizes any incident report from confirmed evidence.
5. **Resolve and verify.** On `BLOCK`, send only the concrete findings back to `implementer`, preserve the approved plan, rerun the focused regression test, and repeat review until `APPROVE` or a Shared Stop Condition triggers. Treat `WARNING` as actionable when tied to the repair plan, a likely bug, security/privacy, or a meaningful test gap. Run relevant broader checks, inspect the final diff, and perform the main-agent closeout review.

If the repair expands into feature-level behavior or contract work, stop and request user direction; do not switch workflows automatically.

In the final response, identify the artifact paths, independent reviewer verdict, and main-agent closeout review. Report the confirmed root cause, repair, exact verification results, residual risks, and omissions.
