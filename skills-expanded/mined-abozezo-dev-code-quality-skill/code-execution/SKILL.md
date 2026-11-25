---
name: code-execution-skill
description: |
  Guides implementation work through an explicit planning, execution/building,
  verification, and review workflow with documented handoffs. Reuses the
  existing code-verify-and-clean-skill for verification and review.
  Use when: planning a code change, implementing an approved plan, building an
  application, coordinating quality gates, or preparing a change for handoff.
allowed-tools:
  - Read
  - Write
  - Grep
  - Glob
  - Bash
  - WebFetch
  - Browser
---

# Code Execution Skill

Deliver code changes through four ordered stages: **planning**, **execution/building**, **verification**, and **review**. A stage may begin only when it receives the required handoff artifact from the preceding stage, and it must produce the artifact required by the next stage.

## Shared Quality Skill

Stages 3 and 4 both use the existing [`skills/code-verify-and-clean-skill/`](../code-verify-and-clean-skill/) skill. **Do not move, copy, rewrite, or otherwise modify that skill as part of this workflow.** Treat it as the shared source of truth for verification, cleanup, security, templates, and reporting.

## Workflow and Handoffs

| Stage | Required input | Required work | Required output / handoff |
| --- | --- | --- | --- |
| 1. Planning | Change request and relevant repository context | Define scope, affected files, implementation approach, risks, acceptance criteria, and commands/checks to run. Resolve open questions before implementation. | **Approved plan** |
| 2. Execution / Building | Approved plan | Implement only the approved scope, make focused changes, and run the applicable build or generation steps. Record files changed, decisions, and any deviations from the plan. | **Implementation summary** |
| 3. Verification | Implementation summary and changed code | Use `skills/code-verify-and-clean-skill/` to run its linting, tests, runtime checks, security checks, and reporting workflow. Capture commands, outcomes, failures, and remaining risks. | **Verification results** |
| 4. Review | Implementation summary and verification results | Use `skills/code-verify-and-clean-skill/` to assess structural-cleanup standards and security-review guidance, complete its review template, and confirm verification evidence is sufficient for the change. | **Final review findings** |

## Stage 1 — Planning

Create an approved plan before editing implementation files. It must include:

- Goal and non-goals.
- Affected files/components and expected change sequence.
- Risks, dependencies, and rollback considerations.
- Clear acceptance criteria.
- Expected build, test, lint, runtime, and security checks.

**Handoff:** The approved plan is the only authorization for execution/building. If scope changes materially, update and re-approve the plan before continuing.

## Stage 2 — Execution / Building

Implement the approved plan in small, coherent changes. Build or generate artifacts as appropriate for the repository, and keep implementation notes accurate.

The implementation summary must state:

- The approved-plan items completed and any approved deviations.
- Files changed and the purpose of each change.
- Build/generation commands run and their outcomes.
- Known limitations, deferred work, or risks to pass to verification.

**Handoff:** Supply the implementation summary and changed code to verification.

## Stage 3 — Verification

Verification must use the existing [`skills/code-verify-and-clean-skill/`](../code-verify-and-clean-skill/) without moving or rewriting it. Follow that skill's established workflow for:

1. **Linting and static checks** — run applicable formatters, linters, type checks, and compilation/build checks.
2. **Tests** — execute relevant unit, integration, and other repository-native test suites.
3. **Runtime checks** — when applicable, run the application and use its DevTools/browser guidance to inspect behavior, console output, and network requests.
4. **Security checks** — apply its security-verification guidance for input handling, exposure risks, dependencies, and other relevant attack surfaces.
5. **Reporting** — follow its reporting workflow and record findings and evidence using its supplied reporting assets where applicable.

Verification results must include the exact commands/checks, pass/fail status, pertinent output or evidence, unresolved findings, and an explicit recommendation to proceed or return to execution/building.

**Handoff:** Pass the verification results, together with the implementation summary, to review. Any blocking verification failure returns the change to Stage 2.

## Stage 4 — Review

Review must also use the existing [`skills/code-verify-and-clean-skill/`](../code-verify-and-clean-skill/) without moving or rewriting it. Review the implementation and verification evidence against that skill's:

- **Structural-cleanup standards** for modularity, duplication, dead code, clarity, and maintainability.
- **Security-review guidance** for vulnerabilities, unsafe handling, secret exposure, and residual risk.
- **Review template** in `assets/review-template.md` to make findings consistent and actionable.
- **Verification evidence** from Stage 3, confirming that checks are relevant, complete, and sufficient for the claimed behavior.

Final review findings must identify approved items, blocking issues, non-blocking follow-ups, residual risks, and the final disposition: approve, approve with follow-ups, or return to execution/building.

## Completion Rule

A change is complete only after final review findings have been produced and the final disposition is approval (with any follow-ups explicitly recorded). Preserve all four handoff artifacts with the change record:

1. Approved plan
2. Implementation summary
3. Verification results
4. Final review findings
