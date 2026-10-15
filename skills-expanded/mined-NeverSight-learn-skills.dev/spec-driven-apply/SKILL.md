---
name: spec-driven-apply
description: Implement the tasks in a spec-driven change. Works through incomplete tasks one by one, marking each complete as it goes.
version: 0.1.0
---

You are helping the user implement a spec-driven change.

## Steps

1. **Select the change** — run `node {{SKILL_DIR}}/scripts/spec-driven.js modify` to list active changes. Ask which change to apply. If already specified, use it.

2. **Load context** — read all artifacts:
   - `.spec-driven/changes/<name>/proposal.md` — what and why; note the **Unchanged Behavior** section — these behaviors must not be broken during implementation
   - `.spec-driven/changes/<name>/specs/` — delta spec files (mirror of main specs/ structure)
   - `.spec-driven/changes/<name>/design.md` — approach and decisions
   - `.spec-driven/changes/<name>/tasks.md` — the checklist
   - `.spec-driven/changes/<name>/questions.md` — open and resolved questions
   Also read:
   - `.spec-driven/config.yaml` — project context; treat `rules` as binding constraints; if `fileMatch` entries are present, apply matching rules when editing files whose paths match the glob pattern
   - `.spec-driven/specs/INDEX.md` — identifies all existing spec files
   - Every spec file in INDEX.md that is relevant to this change — read full content to understand current requirements before writing code

3. **Check task status** — run:
   ```
   node {{SKILL_DIR}}/scripts/spec-driven.js apply <name>
   ```
   Show the user the task summary (total, complete, remaining).

4. **Check for open questions** — read `questions.md` and scan for `- [ ] Q:` entries:
   - If any open questions are found, list each one and **stop** — do not proceed to implementation
   - Ask the user to resolve the questions (edit questions.md directly or use `/spec-driven-modify`)
   - Only continue once all questions are resolved (moved to `## Resolved` with an `A:` answer)

5. **Implement tasks** — work through each `- [ ]` task in order:
   - Read relevant code before making changes
   - Implement the task
   - Verify the change does not violate any **Unchanged Behavior** listed in proposal.md
   - For `## Testing` tasks: actually run the tests (lint, unit tests) and confirm they pass before marking complete
   - Mark it complete in tasks.md by changing `- [ ]` to `- [x]`
   - Briefly confirm what was done before moving to the next task

6. **Update delta specs** — after all tasks are done, re-read each file in `changes/<name>/specs/` and verify it accurately reflects what was actually implemented:
   - If the implementation diverged from the original plan, update the affected files
   - If additional spec files need to be created or modified, do so now

7. **On completion** — when all tasks are done and delta spec is accurate:
   - Run `node {{SKILL_DIR}}/scripts/spec-driven.js apply <name>` again to confirm 0 remaining
   - Suggest running `/spec-driven-verify <name>` to verify the implementation

## Rules
- Read existing code before modifying it
- Complete tasks in order unless there is a clear dependency reason to skip
- Mark tasks complete immediately after implementing them, not in bulk at the end
- If a task is ambiguous, read proposal.md and design.md before asking the user
- Do not implement tasks that are already marked `- [x]`
