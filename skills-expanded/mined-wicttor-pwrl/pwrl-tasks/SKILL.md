---
name: pwrl-tasks
description: "Slice implementation plans into granular, executable task files. Use when: breaking down plans from pwrl-plan; creating actionable tasks for pwrl-work; need detailed task files in docs/tasks/to-do."
argument-hint: "[Path to plan file, or leave blank to find latest plan]"
---

# PWRL Tasks

Slice a plan into granular, executable task files for `/pwrl-work`.

## Interaction Method

- Use platform's `ask_user_question`, `ask_user`, `ask_user_input`, `vscode/askQuestions` or any available extension/tool for user interaction for all decisions
- Ask one question at a time
- Use multiple-choice questions when possible
- If input is empty, ask: "What plan would you like to slice into tasks? Provide a plan file path or leave blank to auto-discover the latest plan."
- Provide clear recovery suggestions when errors occur

## Purpose

- Create ready-to-execute work items in `docs/tasks/to-do/`
- Preserve unit IDs and dependencies from the plan
- Enrich tasks with implementation steps, tests, and acceptance criteria

## Usage

```bash
/pwrl-tasks
/pwrl-tasks docs/plans/2026-05-01-001-auth.md
```

## Input

Plan document path, or blank to auto-discover the latest plan in `docs/plans/`.

## Support Files

- `references/task-template.md` — Canonical task structure (body + frontmatter)
- `references/index-template.md` — Canonical `docs/tasks/INDEX.md` structure
- `references/dependency-resolution.md` — Dependency modeling and validation guidance
- `references/examples.md` — Examples of good tasks and indexes
- `references/github-issues-integration.md` — Optional GitHub Issues sync rules

## Workflow

### Phase 0: Select Interaction Mode

Before locating the plan, ask the user to choose their engagement level for this slicing workflow. Use the platform's `ask_user_question` extension (or equivalent) to present the following three options:

**Question:** "How would you like to proceed with this task slicing?"

**Options:**

- **Detailed (Step-by-Step)** — Show each generated task file to the user before writing; pause for ambiguous dependency resolutions; require explicit approval before updating the index. Maximum control. Best for complex plans where dependency resolution is non-obvious.
- **Smart (Risk-gated automation)** — Write all task files automatically; pause only for ambiguous dependency resolutions (e.g., a unit that references a missing unit-id) and for the index update. v1 simplification: behaves like Yolo with a single confirmation prompt at workflow start.
- **Yolo (Full Automation)** — Write all task files automatically; auto-resolve dependencies with conservative defaults (e.g., assume a missing dependency is a future unit, do not block on it); auto-update the index. Fastest. Best for routine plans and trusted plan templates.

Store the selection in the orchestrator context for use by Phases 2 and 3:

```yaml
interactionMode: detailed | smart | yolo
```

> **Note:** A future enhancement could read the mode from `.pwrlrc.json` so users who always want Yolo don't get re-prompted. Out of scope for plan 2026-06-29-001 — see `docs/learnings/pattern/interaction-mode-three-mode-propagation-2026-06-29.md` §"Future Refinements".

### Interaction Mode Propagation

The `interactionMode` value is set in Phase 0 and consumed by Phases 2 and 3:

- **Phase 2 (Generate Task Files):**
  - **Detailed:** Show each generated task file to the user before writing; pause for ambiguous dependency resolutions.
  - **Smart:** Write all task files automatically; pause only for ambiguous dependency resolutions.
  - **Yolo:** Write all task files automatically; auto-resolve dependencies with conservative defaults.
- **Phase 3 (Generate Index and Report):**
  - **Detailed:** Show the proposed index update to the user before writing; require explicit approval.
  - **Smart:** Write the index automatically; report the diff afterward.
  - **Yolo:** Write the index automatically; no diff preview.

### Phase 1: Locate and Read the Plan

1. If a path is provided, read that plan; otherwise scan `docs/plans/` for the latest active/draft plan.
2. If no plan exists, ask the user to create one with `/pwrl-plan` or provide a path.
3. Extract implementation units (`U1`, `U2`, ...) plus any dependencies and test scenarios.
4. Read `docs/learnings/INDEX.md` and map relevant learnings to each unit (or mark a learning gap).

### Phase 2: Generate Task Files

1. For each unit, create `docs/tasks/to-do/YYYY-MM-DD-uX-<slug>.md`.
2. Use `references/task-template.md` as the canonical task structure and keep tasks self-contained.
3. Ensure task frontmatter includes (at minimum):

   ```yaml
   ---
   unit-id: U1
   plan: docs/plans/YYYY-MM-DD-NNN-name.md
   status: to-do
   dependencies: [U2]
   files: [path/to/file.ts]
   learnings: [docs/learnings/pattern/example.md]
   ---
   ```

4. Ensure task body includes: goal, context, steps, edge cases, testing, acceptance criteria, and references.
5. If a unit has no relevant learning, add an explicit step to document one via `/pwrl-learnings`.

### Phase 3: Generate Index and Report

1. Create/update `docs/tasks/INDEX.md` using `references/index-template.md`.
2. Validate dependencies (see `references/dependency-resolution.md` for guidance).
3. Report created tasks, critical path, and recommended starting tasks.

## Output

- Task files created under `docs/tasks/to-do/`
- A task index at `docs/tasks/INDEX.md` reflecting statuses and dependencies

**Quality Gate Validation:** Run `/pwrl-phase-checkpoint tasks 3 [artifact-path]` to validate all tasks generated and dependencies resolved. See [pwrl-phase-checkpoint](../pwrl-phase-checkpoint/SKILL.md) for validation rules.

## Best Practices

- Keep each task independently executable (with dependencies noted)
- Preserve stable unit IDs from the plan; never renumber
- Prefer linking to existing codebase patterns over inventing new conventions
- If GitHub Issues sync is enabled, follow `references/github-issues-integration.md`

## Rules

- Never delete or overwrite existing tasks without explicit user confirmation.
- Use repository-relative paths only in tasks and indexes.
- If dependency information is ambiguous, ask before encoding it into tasks.
