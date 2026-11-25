---
name: req-scope
description: >
  Decompose a ready REQ into atomic, sequenced, AI-ready TASKs with
  explicit dependencies and owned acceptance criteria. Use when the user
  says scope, break down the requirement, create tasks, see the build as
  steps, or runs /ultimate-sdd:scope.
license: MIT
metadata:
  author: andrewr303
  version: "2.0"
---

Turn a ready REQ into independently verifiable outcome slices. Scope is planning, not implementation.

**Supporting files:** `references/spec-quality.md`, `references/readiness.md`, `references/model.md`, `references/handoff.md`, `templates/task-template.md`, `templates/artifact-review.md`.

## Steps

### 1. Load and gate

Follow **Planning context loading** in `references/spec-quality.md`: target instructions, validated `docs/plan/config.json` via `sdd.py config`, `workflow.md`, catalog/platform/relevant CTX, and upstream project/brief/EPIC/REQ. Read linked CHANGE/deltas/truth, optional REQ/CHANGE design sidecars, and **all existing tasks** for this REQ before slicing.

Refuse Scope if readiness <4 or a build-blocker remains; send the concrete gaps to `req-specify`. Check dependency, lifecycle, authorization, and review gates separately from the number. In auto permission mode **NEVER call AskUserQuestion**; report unresolved choices rather than guessing permission. Do not re-open a done/cancelled REQ or rewrite active/done work to make room for a plan.

### 2. Slice by observable outcome

Apply **Vertical task slices** in `references/spec-quality.md`. Each TASK delivers one observable, independently verifiable outcome across only the relevant layers, including its own tests and needed docs. There is no fixed task count and no default schema/core/UI/tests/docs sequence.

An enabling infrastructure TASK needs all four: its own observable parent AC/check, a reason it cannot be bundled, a true prerequisite, and a named consumer. Reject scaffolding-only untestable tasks. A migration with verifiable forward/rollback preservation may qualify; empty tables for unspecified future use do not.

Map every parent AC to exactly one active owner through `ac: [AC-n]`. Copy full original Given/When/Then text verbatim, not a shortened paraphrase. Cross-reference other tasks' criteria without sharing ownership. Do not invent AC: if the slice needs missing behavior/checks, refine the REQ first.

On re-scope preserve existing IDs, bodies, active/done tasks, and evidence. Do not append a second owner for completed work. Add only unowned authorized outcomes with new IDs; any ownership transfer or revision of an existing contract needs explicit authorization and a stale-evidence assessment, not an overwrite.

### 3. Sequence and write

Use `templates/task-template.md` at `docs/plan/tasks/REQ-<n>/TASK-<k>-<slug>.md`. Scan within the REQ for the next append-only TASK ID; cite it externally as `REQ-n/TASK-k`.

Fill Goal, slice kind (`vertical` or justified `enabling`), Context, owned file scope/integration seams, Steps, owned AC, Verify, and empty Send-back/evidence. Prefer extending actual existing files over inventing abstractions.

- Effective `parallelism: serial` → serialize. `disjoint` permits concurrency only after proving no file overlap, dependency, or integration conflict; otherwise serialize with the reason recorded.
- Keep `blocked_by` / `blocks` mutual and acyclic, within this REQ. Name provider/consumer seams and any unavoidable shared files. Patch only authorized dependency links on existing work; flag conflicts with active tasks rather than rescheduling them silently.
- New TASKs are `ready` only when their gates/dependencies permit; otherwise `blocked` for dependencies or `planned` pending unresolved planning gates. Preserve existing lifecycle states.
- Each slice includes its tests and relevant docs in Steps, not separate default chores. Record the effective TDD policy for the later implementer; do not run TDD here.
- Verify lists actual config `test_commands` argv arrays, workflow/repo-evidenced methods, or authorized reproducible observations, with cwd, prerequisites, source, and expected outcomes. Empty config is not permission to invent tooling. Never add git mutation instructions or execute these commands during Scope.

### 4. Review the set and finalize

Apply **Planning artifact review** in `references/spec-quality.md` using `templates/artifact-review.md` to the **TASK set plus parent REQ**. Check outcome boundaries, exact single ownership, verbatim AC, tests/docs, dependencies, and file conflicts. Pending or material findings are not a pass; return REQ-contract gaps to Specify rather than expanding the TASKs.

Follow **Finalize and derive Next** there: run `plan.py board --root <root> --write`, `validate --root <root>`, and `next --root <root> --json`. Show the actual task list, blockers, ownership/serialization decisions, review state, and derived Next. Never hardcode "load TASK-1" or claim planning checks prove implementation. Stop before Load/code.
