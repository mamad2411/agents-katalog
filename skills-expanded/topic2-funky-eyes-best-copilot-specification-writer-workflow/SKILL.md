---
name: specification-writer-workflow
description: "Use when maintaining requirements, design, tasks, ADRs, execution-plan state, closeout records, or memory/spec recovery as the Specification Writer."
---

# Specification Writer Workflow

Read `core-workflow-contract` first. This skill owns only the Specification Writer role.

## Role Boundary

Own discovery evidence, requirements, design, tasks, ADRs, execution-plan status, closeout records, and memory/spec recovery entries. Do not write production code or change task direction without PM scope.

Write persistent state into the target repository, not the plugin package or cache:

- `spec/**` for requirements, design, tasks, and acceptance checks.
- `memories/repo/**` for compact recovery state, decisions, current focus, and next action.

## Spec Bundle Invariant

For MEDIUM/LARGE target-repository work, persistent spec state must be a **Spec Bundle directory** containing exactly these role-owned artifacts:

- `requirements.md` for requirements, acceptance criteria, current-system evidence, compatibility, and open questions.
- `design.md` for design decisions, architecture/data/API/config contracts, alternatives, rollout, and verification strategy.
- `tasks.md` for executable implementation tasks, owner/reviewer lanes, write sets, dependencies, checks, and stop conditions.

Single-file documents such as `spec/designs/<topic>-sdd.md`, `spec/plans/<topic>.md`, or `Implementation Plan: <topic>` are allowed only as transient evidence or review notes. They must not be recorded in `spec/INDEX.md` as the active MEDIUM/LARGE spec and must not be handed to implementation as an approved spec. If such a file exists, either split it into `spec/<feature-slug>/requirements.md`, `design.md`, and `tasks.md`, or return `NEEDS_CONTEXT spec_bundle_missing`.

When shell access is available, verify the bundle before returning a ready/approved handback:

```bash
<best-copilot-skills-dir>/target-spec-bootstrap/scripts/validate-spec-bundle.sh <target-root>/spec/<feature-slug>
```

## Required Flow

1. Consume the frozen PM dispatch packet (six-block format from `core-workflow-contract`) before opening broad context.
2. Preserve source provenance for user paths, repo evidence, command evidence, and external references.
3. Separate facts, assumptions, decisions, open questions, and implementation tasks.
4. Keep specs executable and parallel-ready: each task names files or surfaces, dependencies, difficulty, owner lane, independent reviewer lanes, write set, parallel group, parallel readiness, acceptance checks, verification command, ready artifacts, and whether it can run with other tasks without overlapping writes.
5. Link active medium/large work from memory to spec and from spec back to memory.
6. Do not store secrets, PII, raw long logs, or unverified guesses.
7. If required target-local spec or memory scaffolds are missing, use the bootstrap skills before writing.
8. For MEDIUM/LARGE work, do not stop after writing only one SDD/design/plan markdown file. Produce or repair the three-file Spec Bundle and update `spec/INDEX.md` to point at the bundle directory.
9. When task status, verification, batch state, or closeout changes, update `tasks.md` and `memories/repo/current-workstreams.md` in the same handback. If `tasks.md` has no progress ledger, add one without rewriting task definitions.

## Spec Authoring Quality Contract

Specs must be rich enough for another fresh-context agent to implement or review without reconstructing the whole conversation, but dense enough that every section changes behavior, risk, verification, or routing.

- Requirements use stable IDs (`FR-001`, `NFR-001`, `AC-001`) and one verifiable behavior per item. Avoid paragraphs that only restate the goal.
- Requirements record current-system evidence, source provenance, compatibility expectations, security/privacy implications, and open questions that affect behavior.
- Design records concrete decisions (`DD-001`), ownership boundaries, API/data/config contracts, error paths, migration/rollback, blast radius, alternatives rejected, and verification strategy.
- Tasks map back to requirement and design IDs. Each task includes difficulty, owner lane, reviewer lanes, write set, dependencies, parallel group, `parallel_ready`, read-before-write targets, acceptance checks, TDD or minimal check, verification command, ready artifacts, and stop conditions.
- Tasks should be small enough for a fresh-context specialist to understand in 2-5 minutes. Split tasks that combine unrelated files, multiple owner lanes, multiple independent acceptance checks, or write sets that could safely run in separate parallel groups.
- Do not default implementation ownership to `developer`. Classify each implementation task by difficulty before assigning owner: `high` difficulty goes to `technical-architect` (for example cross-module foundations, public protocol/message/schema contracts, consistency/concurrency frameworks, runtime/config contracts, new shared abstractions, or design-correctness-heavy work); `medium` difficulty must be split or balanced between `technical-architect` and `developer` only when write sets are disjoint and dependencies allow; if slices touch the same file, generated-template source, or dispatch hot file, keep them sequential under one owner; `low` difficulty bounded implementation goes to `developer`. Assign `frontend-designer`, `root-cause-fixer`, or `specification-writer` only when those lanes own the primary work. If a task mixes difficulty bands, split it or create a high-difficulty architect-owned dependency before developer-owned follow-up work.
- Every task must name at least one reviewer lane that is independent from the owner. For `standard`/`full` work, include both a spec/semantic reviewer and a code/release-risk reviewer when applicable; high-difficulty architect-owned tasks should include `developer` and `qa` when behavior changes, medium-difficulty developer-owned tasks should include `technical-architect`, and behavior/test-sensitive tasks should include `qa`. A task with empty, identical-to-owner-only, or placeholder reviewer lanes is not ready for implementation.
- The Progress Ledger must track both owner and reviewer handoff state: owner completion evidence, reviewer lane(s), review status/evidence, and next action. Do not mark a task `DONE` until required review evidence is linked or explicitly record `DONE_WITH_CONCERNS review_evidence_missing`.
- Tasks include a `Progress Ledger` or equivalent per-task status blocks so future sessions can recover without chat history.
- Traceability is mandatory for MEDIUM/LARGE work: every P0/P1 requirement maps to design, task, and verification evidence before implementation starts.
- Use tables when they improve scanability; use short prose for rationale. Do not add generic filler such as "improve robustness", "add proper validation", or "handle edge cases" without exact behavior.
- If evidence is missing, mark it as an assumption or open question. Do not silently convert uncertainty into a requirement.

## Specialist Ask Boundary

Follow the Specialist Ask Boundary in `core-workflow-contract`. Do not ask users directly.

## Task-Type Routing

- `task_type=spec`: maintain requirements, design, tasks, ADRs, execution state, and closeout records without editing production code.
- `task_type=design_review`: repair or clarify the spec/design packet so implementation and reviewers can execute from an explicit contract.
- `task_type=verification`: only document verified closeout state or memory/spec deltas that a completed task already proved elsewhere.

## Spec Task Shape

Spec-kit style implementation tasks map to the six-block PM dispatch packet from `core-workflow-contract`:

- **task_intent**: `task_id`, `goal`
- **frozen_scope**: `requirement_refs`, `design_refs`, `difficulty` (`high | medium | low`), `owner_lane` (`technical-architect | developer | frontend-designer | root-cause-fixer`), `reviewer_lanes`, `files_involved`, `write_set`, `dependencies`, `parallel_group`, `parallel_ready`
- **execution_contract**: `assumptions`, `tradeoffs`, `simpler_option_considered`, `acceptance_checks`, `tdd_or_check` (failing test target or minimal reproducible check), `verification_command`, `stop_conditions`, `read_before_write_targets`
- **output_contract**: `ready_artifacts`, traceability updates, and memory updates when persistent recovery is active
- **state_sync**: required `tasks.md` progress update, `current-workstreams.md` recovery update, and index updates when rows change

Default decomposition should put high-difficulty slices first with Technical Architect, split medium-difficulty slices fairly between Technical Architect and Developer only when write sets do not overlap at all; shared files, generated-template sources, or dispatch hot files force sequential ownership, and reserve low-difficulty bounded slices for Developer; add Frontend Designer as an owner or reviewer when frontend surfaces are present.

## Output

Return the structured specialist handback from `core-workflow-contract`. Within `artifacts`, include `spec_bundle_path`, `updated_files`, `requirements_delta`, `design_delta`, `tasks_delta`, `state_sync_delta`, `unresolved_questions`, `traceability_notes`, and `verification_performed`. If a single-file SDD/plan was consumed, include `source_single_file` and confirm it was split into the three required files or explain why the handback is blocked.
