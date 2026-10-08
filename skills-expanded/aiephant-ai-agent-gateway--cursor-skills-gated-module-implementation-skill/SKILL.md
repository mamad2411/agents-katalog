---
name: gated-module-implementation
description: Plan-first, one-time human plan approval; batched execution in either Gated (human confirms between batches) or Auto-loop (continuous run after plan approval); strict task-state updates; automatic 3-round code review. Use for "audit then implement" or "plan first, then execute". Say "auto-loop" or "frad-dotclaude" for Auto-loop mode.
---

# Gated Module Implementation

## Overview

- **(1) Plan + (2) Audit:** Write the implementation plan, run three rounds of plan audit, fix gaps.
- **(3) Human — Plan only:** **Only one** human gate: approve the plan before any task runs. No human approval between code review rounds (those are automatic).
- **(4) Execute in order by batch:** Tasks (e.g. 1–10) run **in order**. Behavior depends on **Execution mode** (below).
- **(5) Automatic 3-round review:** After all tasks and tests pass, run **exactly 3 rounds** of code review automatically: round 1 → fix Critical/Important → round 2 → fix → round 3. No human confirmation between rounds.

Unit tests: full coverage. E2E: pass. Test report: generated. No skipped tests.

### Execution mode

| Mode | When to use | Phase 4 behavior |
|------|-------------|------------------|
| **Gated** (default) | User does not ask for auto-run. | After each batch: report → **wait for human confirmation** ("continue" / "go") → next batch. |
| **Auto-loop** | User says "auto-loop", "frad-dotclaude mode", "audit then implement and run everything automatically", or equivalent. | After plan approval: run **all batches in sequence** with no human between batches. After each batch: report and update task state, then **immediately** proceed to next batch until all tasks done → then Phase 5. |

**Announce at start:** "I'm using the gated-module-implementation skill for this module." If Auto-loop: also say "Auto-loop mode: I will run all execution batches continuously after plan approval."

---

## Phase 1: Plan (Required Before Any Code)

1. **Clarify scope and dependencies**
   - Identify the module boundary, upstream/downstream services, and shared contracts (API, DB, events).
   - Document in a short "Context & Dependencies" section (can live in the plan file or a linked doc).

2. **Write the implementation plan**
   - **REQUIRED SUB-SKILL:** Use [writing-plans](../writing-plans/SKILL.md).
   - Save the plan to the **correct project** `plan/` path (see writing-plans for the table).
   - Plan must include explicit tasks for: unit tests (full coverage), E2E tests (fully runnable), and test report generation. No "skip tests" or "TODO tests."

3. **Deliverable**
   - One plan file at `<project>/plan/YYYY-MM-DD-<feature-name>.md` with header, goal, architecture, and bite-sized tasks including test steps.

---

## Phase 2: Three Rounds of Audit

Run **three** audit rounds on the **plan** (and any linked context). Do not proceed to execution until all three are done and issues are addressed.

### Round 1 — Completeness & Scope

- [ ] Goal and acceptance criteria are clear and testable.
- [ ] All touched files (create/modify/test) are listed with exact paths.
- [ ] Dependencies on other modules/APIs/DB are documented; no hidden coupling.
- [ ] Edge cases and error paths are covered in tasks or tests.

**Output:** Short checklist result; list any gaps. Fix the plan if gaps found.

### Round 2 — Dependencies & Interfaces

- [ ] API contracts (request/response, status codes) are specified where the module touches boundaries.
- [ ] DB schema changes (if any) are stated; migrations are in the task list.
- [ ] Integration points (policy-service, gateway, SaaS, data-warehouse) respect project boundaries (see `.cursor/rules/project.mdc`).

**Output:** Short checklist result; list any conflicts or missing interface specs. Update plan if needed.

### Round 3 — Test Strategy & Rollout

- [ ] Unit test tasks exist for all new/edited behavior; plan states "full coverage" (or equivalent) and no skipped tests.
- [ ] E2E test tasks exist and are runnable (commands and expected pass condition stated).
- [ ] A task generates a test report (e.g. coverage report, E2E summary); artifact path or command documented.
- [ ] Rollback or feature-flag approach is considered if relevant.

**Output:** Short checklist result; list any missing test or report steps. Update plan until satisfied.

After Round 3, present a one-paragraph **Audit Summary** (all three rounds) and say: **"Plan ready for human review. Please confirm before execution."**

---

## Phase 3: Human Review — Plan Approval Only (Once)

**Only one human review is required: approve the plan before any task execution.** No human approval is needed before or between code review rounds (those are automatic). In **Auto-loop** mode, there is **no** human confirmation between Phase 4 batches — only this single plan approval.

### Single checkpoint — Approve plan (before first task)

- Present: plan path, goal, audit summary, and any open risks.
- **Do not start Phase 4 until the human explicitly confirms** (e.g. "approved" / "go ahead" / "execute").
- If the human requests plan changes, update the plan and optionally re-run the relevant audit round(s), then ask for confirmation again.

### Between execution batches (Gated mode only)

- **Gated mode:** After each batch (e.g. tasks 1–3 done): report what was done, show verification, **wait for human confirmation** before starting the next batch (e.g. 4–6). Tasks run in order; between batches you need "continue" / "go".
- **Auto-loop mode:** Do **not** wait for human between batches. After each batch: report and update task state, then proceed immediately to the next batch until all tasks are done.

---

## Phase 4: Execute the Plan (Tasks in Order, Batch by Batch)

1. **REQUIRED SUB-SKILL:** Use [executing-plans](../executing-plans/SKILL.md).
2. Execute **all tasks in order** (e.g. Task 1 → 2 → … → 10). Work in batches (e.g. first 3, then next 3, then rest). Behavior by mode:
   - **Gated:** After each batch: report → **wait for human confirmation** → next batch. Continue until all tasks are done.
   - **Auto-loop:** After plan approval: run batch 1 → report and update task state → **immediately** batch 2 → report → … → last batch. Do **not** stop for human between batches. Only after **all** tasks are done (and tests pass, report generated) proceed to Phase 5.

3. **Task state discipline (mandatory — do not forget):**
   - **Before starting a task:** Mark it `in_progress` (e.g. TodoWrite or plan checklist).
   - **Immediately after completing a task:** Mark it `completed`.
   - **Before each batch report:** Verify every task in that batch is marked `completed`; if any is still `in_progress` or unchecked, update it first.
   - *Rationale:* Forgetting to update task state loses track of progress and makes batch reporting inaccurate; always update state when starting and finishing a task.
   - **Per-batch self-check before "Ready for feedback":** All tasks in this batch are marked `completed`; no task left in `in_progress`.

4. **Testing requirements (non-negotiable):**
   - **Unit tests:** Achieve full coverage for new/changed code; do not skip or disable tests.
   - **E2E tests:** All E2E tests must run and pass; document the exact run command and result.
   - **Test report:** Generate and attach or link the test report (e.g. coverage HTML, E2E summary). If the project has a standard place (e.g. `coverage/`, `test-results/`), put it there and mention the path.

5. If execution is blocked (e.g. test failure, missing dep), stop and ask; do not skip tests to "unblock."

---

## Phase 5: Automatic 3-Round Code Review (No Human Between Rounds)

**Multi-round review** means run exactly **3** review rounds automatically: round 1 → fix Critical/Important → round 2 → fix → round 3. No human confirmation between rounds; all three rounds run automatically without inserting a human gate in the middle.

1. After **all** plan tasks are complete and tests pass with report generated:
   - **REQUIRED SUB-SKILL:** Use [requesting-code-review](../requesting-code-review/SKILL.md).
2. **Round 1:** Dispatch the code-reviewer (plan + scope, correct BASE_SHA/HEAD_SHA). Fix all Critical and Important issues; re-run unit and E2E tests; regenerate test report if needed.
3. **Round 2:** Dispatch the code-reviewer again (BASE_SHA = previous HEAD_SHA, HEAD_SHA = current HEAD). Fix all Critical and Important issues; re-run tests and update report if needed.
4. **Round 3:** Dispatch the code-reviewer again (BASE_SHA = previous HEAD_SHA, HEAD_SHA = current HEAD). After round 3, consider the module done (fix any remaining Critical/Important from the report as needed).
5. Do not stop to ask human between rounds — run all three rounds automatically.

---

## Workflow Summary

| Phase | Action | Gate (Gated) | Gate (Auto-loop) |
|-------|--------|--------------|-------------------|
| 1 | Clarify deps + write plan (writing-plans) | Plan saved | Plan saved |
| 2 | Audit Round 1–3 (plan audit) | Checklist pass | Checklist pass |
| 3 | **Human: approve plan once** | Explicit approval to execute | Explicit approval to execute |
| 4 | Execute batch 1; **update task state** each start/complete | Report; human confirms | Report; no stop |
| 4 | Execute batch 2, … remaining | Report; human confirms each | Continue to next batch |
| 4 | All tasks done; unit + E2E pass; report generated | — | No human between batches |
| 5 | **Automatic** code review: round 1 → fix → round 2 → fix → round 3 | 3 rounds, no human | 3 rounds, no human |

---

## Red Lines

- **Do not** start Phase 4 without human approval of the plan (once).
- **Gated mode only:** Do **not** start the next execution batch without human confirmation after the previous batch. **Auto-loop mode:** After plan approval, you may run all batches continuously without human between batches.
- **Do not** skip or disable unit or E2E tests; no "skip" in test config for this module.
- **Do not** forget to mark tasks `in_progress` when starting and `completed` when finishing; verify batch task states before each report.
- **Do not** stop to ask human between code review rounds — run all 3 rounds automatically.
- **Do not** consider the module complete without a generated test report and **all 3** code review rounds completed.

---

## References

- Plan path rules and task format: [writing-plans](../writing-plans/SKILL.md)
- Execution batching and checkpoints: [executing-plans](../executing-plans/SKILL.md)
- Code review dispatch and template: [requesting-code-review](../requesting-code-review/SKILL.md)
- Project boundaries (four engines): `.cursor/rules/project.mdc`
