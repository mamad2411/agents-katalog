---
name: using-itsolpowers
description: "Route ITSOL work to the smallest skills by stage, authority, domain, and risk."
---
# Using ITSOL Powers

Choose the smallest sufficient context. Skill descriptions are the routing index; load bodies and references only when needed.

## Route

1. **Bounded administration:** repository inspection/status, `.itsol.md` setup, or a local commit of an already verified slice. Reuse prior evidence; do not create plans, delegation, review, QA, or a new completion gate. Push, release, deployment, and other external effects remain separately authorized.
2. **Engineering:** classify the current stage—initiative, intake, requirements, planning, implementation, debugging, migration, review, QA, or current-tech research—before loading skills.
3. Load `itsol-workflow-mode` only when planning, implementation, bugfix, delegation, or mode transition needs authority. It owns the seven workflow fields and their canonical states; do not redefine them downstream.
Workflow state is `governed` | `autonomous-planned` | `direct`: `workflow_mode`, `mode_source`, `decision_authority`, `scope`, `artifact_state` (`draft` | `approved` | `ready-for-execution` | `not-required`), `execution_mode` (`pending` | `inline` | `subagents` | `auto`), and `protected_constraints`.

## Primary process

- broad multi-phase outcome → `itsol-initiative-delivery`
- unclear request → `itsol-task-intake`
- requirements/plan → `itsol-functional-planning` + `itsol-requirements-review`
- feature/refactor → `itsol-feature-implementation`
- bug/regression → `itsol-bug-debugging`
- rewrite/toolchain migration → `application-technology-migration`
- code/PR review → `itsol-code-review-workflow`
- browser dogfood → `agent-browser-dogfood-workflow`
- QA handoff → `itsol-qa-handoff`
- delegation packet → `itsol-subagent-workflow`
- budget/stop/completion → `itsol-execution-policy`
- version/API research → `itsol-current-tech-context`

Use `itsol-self-review` before handoff. Load `itsol-tdd-workflow` only when the user explicitly requests test-first development. Use Codex setup/doctor only for explicit role setup or diagnosis.

## Domain selection

Read candidate descriptions, then add only touched surfaces. Prefer the implementation, debugging, or review variant matching the stage. Load `itsol-current-tech-context` when a claim depends on a runtime, framework, SDK, package, generator, or external API. Do not preload family checklists.

## Execution and profiles

Load `itsol-execution-policy` when resource, delegation, review, stop, or completion state matters; load `itsol-subagent-workflow` only after delegation is authorized. Only the main agent delegates; children never delegate. Keep writers disjoint and accept `completed` only after evidence validation; preserve `partial`, `blocked`, and `failed`.

Context profile precedence is explicit task, `ITSOLPOWERS_CONTEXT_PROFILE`, validated runtime capability, then `compatibility`; invalid input fails closed. Provider name alone never selects `frontier`. Profiles never weaken workflow authority, repository restrictions, protected actions, deterministic contracts, honest incomplete status, or nested-delegation prohibition. `frontier` uses risk-proportionate verification; `compatibility` states verification, response, and review evidence explicitly. Neither requires TDD or fan-out for small work.

## Verification

Choose permitted checks for changed behavior and material risk, starting with relevant existing checks. TDD and RED/GREEN are opt-in; their absence is not a blocker and needs no exception. Add lasting tests only for meaningful behavior, contracts, or regressions that existing coverage cannot protect. Avoid tests per function, mock-call counts, private structure, trivial assertions, and duplicate coverage. Preserve behavioral/security coverage; revise obsolete implementation-detail assertions instead of freezing production structure to satisfy them. Small mechanical edits need no new tests. Do not scaffold a framework or add coverage quotas without agreed scope. Broaden checks only for a concrete risk; scratch diagnostics need not become permanent test files.

## Complete authorized work

Within the resolved authority, scope, and stop limits, continue until every `done_when` criterion has evidence. For implementation, complete the change, run permitted focused checks, and fix failures caused by the change. A progress update or proposed next step does not complete the task. While awaiting an answer, command, or child result, continue independent work; wait for results before dependent work or final acceptance. Stop when the requested result and checks are complete. Repeat successful checks or review only after a relevant change, failure, unresolved concern, or policy requirement. If a required gate, decision, or limit blocks continuation, report the incomplete result and exact blocker.

## User communication

Communicate in the user's language. Minimize reading effort.

- Lead with the result, recommendation, or decision needed.
- Use short sentences, active voice, familiar words, and consistent terminology.
- Keep one idea per sentence and one topic per paragraph.
- Explain unfamiliar technical terms briefly.
- Use bullets for parallel items and numbered steps for procedures. Give one action per step.
- Keep progress updates to 1–2 sentences. Keep routine final replies to one short paragraph or 3–5 bullets.
- Preserve required evidence, uncertainty, constraints, and material risks. Preserve code, commands, identifiers, and quotations exactly.
- Provide more detail when the task or user requires it. Remove repetition, generic praise, and unnecessary background.

These defaults apply to conversation. Preserve required response formats and complete artifact content. Brevity must not reduce task scope, verification, or deliverable completeness.

## Contract and handoff

State outcome, constraints/authority, observable `done_when`, and focused evidence. Return `completed`, `partial`, `blocked`, or `failed` with achieved evidence, unverified gaps, blockers, and next action. Report changed/inspected files, commands and observed results, assumptions, coverage gaps, risks, integration dependencies, and the next review target. A commit request never authorizes push, publish, release, or deploy.
