---
name: pwrl-work
description: Execute implementation work efficiently through 4-phase micro-skill pipeline
argument-hint: "[Task file, plan doc path, or work description. Leave blank to use latest plan/task]"
---

# PWRL Work

Execute implementation work through a deterministic 4-phase pipeline: triage input, prepare environment, implement with test-first discipline, and review code quality.

## Interaction Method

- Use platform's `ask_user_question`, `ask_user`, `ask_user_input`, `vscode/askQuestions` or any available extension/tool for user interaction for all decisions
- Ask one question at a time
- Use multiple-choice questions when possible
- If input is empty, ask: "What work would you like to execute? Provide a task file path, plan file, or describe the work to be done."
- Provide clear recovery suggestions when errors occur

## Purpose

Transform task files, plans, or prompts into completed working code through systematic execution:

- **Triage Input** — Classify and validate input (task file, plan file, bare prompt, or latest task)
- **Prepare Environment** — Repository verification, ambiguity resolution, branch setup, verification commands
- **Execute Implementation** — Test-first implementation with incremental verification and quality gates
- **Review & Verify** — Code review, scope check, diff quality, documentation

## Usage

```bash
/pwrl-work
/pwrl-work docs/tasks/to-do/2026-06-11-U2-email-validation.md
/pwrl-work docs/plans/2026-06-11-003-skill-architecture.md
/pwrl-work "add email validation to user signup"
```

## Architecture

**Direct sequence of 4 micro-skills with deterministic artifact flow:**

```
Input
  ↓
Phase 0: pwrl-work-triage
  ├ Input: task file, plan file, bare prompt, or empty
  ├ Output: triage artifact (unit_id, files, acceptance_criteria, dependencies)
  ↓
Phase 1: pwrl-work-prepare
  ├ Input: triage artifact
  ├ Processing: repo verification, ambiguity resolution, branch strategy, verification commands
  ├ Output: prepare artifact (branch, verification_commands, environment state)
  ↓
Phase 2: pwrl-work-execute
  ├ Input: prepare artifact
  ├ Processing: scaffolding, test-first implementation, quality gates
  ├ Output: execute artifact (files changed, tests passing, build/lint status)
  ↓
Phase 3: pwrl-work-review
  ├ Input: execute artifact
  ├ Processing: scope check, diff review, test review, documentation check
  ├ Output: review artifact (approval status, ready_to_ship)
  ↓
COMPLETE
```

Each phase produces an explicit **artifact** (YAML frontmatter + structured data) consumed by the next phase. Enables resumability, traceability, and independent testing.

## Phase Summary

**Phase 0: Triage** — Validate input, classify work, extract requirements, set interaction mode. See [pwrl-work-triage/SKILL.md](../pwrl-work-triage/SKILL.md).

**Phase 1: Prepare** — Verify repository, resolve ambiguities, setup branch and environment. See [pwrl-work-prepare/SKILL.md](../pwrl-work-prepare/SKILL.md).

**Phase 2: Execute** — Implement with test-first discipline, verify quality gates. See [pwrl-work-execute/SKILL.md](../pwrl-work-execute/SKILL.md).

**Phase 3: Review** — Verify scope, review code quality, get approval. See [pwrl-work-review/SKILL.md](../pwrl-work-review/SKILL.md).

### Interaction Mode Propagation

Interaction mode (`detailed | smart | yolo`) is set in Phase 0 (via `pwrl-work-triage` Step 5) and read at the start of each subsequent phase. The mode is stored in the triage artifact's `interactionMode` field and propagated through every downstream phase. Determines whether confirmation steps execute or are skipped.

- **`detailed`** — Pause at every phase transition (Triage → Prepare → Execute → Review); show generated artifacts; require explicit approval to proceed. Best for complex work, unfamiliar codebases, and learning.
- **`smart`** — Phases run automatically; pause only when the next phase produces a HIGH-risk operation (destructive git, irreversible API calls, schema-breaking migrations). v1 simplification: behaves like Yolo with a single confirmation prompt at workflow start. See `docs/learnings/pattern/interaction-mode-three-mode-propagation-2026-06-29.md` §"Future Refinements" for the full risk-classification roadmap.
- **`yolo`** — Every phase runs automatically; only the final review report is shown. Fastest. Best for straightforward, well-understood work and time-sensitive hotfixes.

**Exception:** Error recovery steps always pause the pipeline, regardless of mode. Downstream phases that still assume a legacy two-value enum must treat any value other than `detailed` as `yolo` until upgraded; `smart` is new as of 2026-06-29.

---

## Quality Criteria

- Requirements from task/plan fully implemented
- Behavior changes covered by tests
- Tests pass after each logical unit
- Code follows project patterns and conventions
- No debug code, console.logs, or commented code left behind
- Scope stayed tight (no unrelated changes)

## Rules

- **Clarify ambiguities upfront** — Don't proceed if approach is unclear
- **Verify incrementally** — Run checks frequently, catch issues early
- **Test-first discipline** — Write tests before implementing
- **One scope at a time** — Complete and review each unit separately
- **No scope creep** — Get approval before expanding beyond task
- **Quality gates** — All checks must pass before marking ready

## Error Handling & Recovery

For comprehensive error scenarios, recovery strategies, and escalation rules, see [references/error-handling.md](references/error-handling.md).

## Support Files

- `pwrl-work-triage/references/triage-input-protocol.md` — Phase 0 specification
- `pwrl-work-prepare/references/prepare-environment-protocol.md` — Phase 1 specification
- `pwrl-work-execute/references/execute-implementation-protocol.md` — Phase 2 specification
- `pwrl-work-review/references/review-quality-protocol.md` — Phase 3 specification

## When to Use

- Use when executing a clear task from a task file
- Use when extracting and executing units from a plan
- Use for well-defined work with clear acceptance criteria
- For exploratory work without clear requirements, use `/pwrl-plan` first
