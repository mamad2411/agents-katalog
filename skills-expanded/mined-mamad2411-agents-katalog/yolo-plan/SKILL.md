---
name: yolo-plan
description: Use when you have a goal or brief and need to break it into executable, testable tasks. Produces a committed plan.md. Triggers on "make a plan", "break this into tasks", or as the planning step of yolo-feature.
---

# yolo-plan

Turn a goal into an ordered set of small, testable tasks. One task = one commit.

## Inputs
- The brief (`workspace/features/<slug>/brief.md`) and, if present, `…/research.md`.

## Procedure
1. Decompose the goal into tasks small enough that each is one focused commit (roughly 2–5 steps of work).
2. For each task define: a kebab-case `id`, `title`, `description`, the `files` it touches, a `test_spec` (the tests to write/update — required for non-scaffolding tasks), `relevant_tests` (paths to *existing* tests that already cover the touched code — the contract to keep green; the executor loads these into context, since the measured TDD win is knowing *which* tests to check, not the ritual), a one-line `verification`, and `depends_on` (task ids).
3. Discover the project's `lint_commands` and `test_commands` from its config (package.json scripts, Makefile, pyproject, etc.) and record them — yolo-verify reuses them.
4. Order tasks by dependency.

## Output
Write `workspace/features/<slug>/plan.md` as YAML:

```yaml
tasks:
  - id: add-csv-export
    title: "Add CSV export endpoint"
    description: "..."
    files: ["src/export.ts"]
    test_spec: "src/export.test.ts: happy-path export + empty-dataset"
    relevant_tests: ["src/reports.test.ts"]   # existing tests covering this area — keep green
    verification: "GET /export returns text/csv"
    depends_on: []
lint_commands: ["eslint ."]
test_commands: ["npm test"]
```

Commit the plan (`yolo: plan <slug>`).

## Execution contract (consumed downstream)
- Each task is implemented test-first — its `relevant_tests` (existing contract) and `test_spec` (new tests) are loaded into the executor's context — and committed with the trailer `YOLO-Task: <id>` (`<id>` matches the task's `id` field; see `.claude/yolo/conventions.md`).
- Present the plan for approval before any code is written — this IS the **plan gate**, the first of YOLO's two confirmations (`.claude/yolo/conventions.md` *The two gates*). Lead with the **key findings/assumptions from research** the plan rests on (a wrong assumption is the costliest thing to catch late — research-review is higher-leverage than diff-review), then the tasks. Skip only if the user pre-consented ("just go").

## Constraints
- No status files; status is derived from git. You only write `plan.md`.
