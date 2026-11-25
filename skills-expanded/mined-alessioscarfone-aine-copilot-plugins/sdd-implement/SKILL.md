---
name: sdd-implement
description: 'Write code, modify files, run tests, and mark tasks done to implement a change from its spec. Use when executing development tasks defined in a change spec, building a feature, coding this up, making the changes, or developing from a spec. Do not use for proposing new changes, designing architecture, or verifying completed work.'
---

> [!IMPORTANT]
> This skill is designed to be used with the **sdd-team:sdd-dev.agent** agent.
> Switch to it in the agent selector before invoking this skill for the full interactive experience.
> If you are already using **sdd-team:sdd-dev.agent**, proceed with the workflow below.

Implement tasks from a change.

**Input**: Optionally specify a change name (e.g., `/sdd-implement add-auth`). If omitted, check if it can be inferred from conversation context. If vague or ambiguous you MUST prompt for available changes.

Before writing, read the shared project documents for context:
- {ARTIFACT_MAIN_FOLDER}/{SHARED_SUBFOLDER}/prd.md — product requirements, user journeys, functional requirements
- {ARTIFACT_MAIN_FOLDER}/{SHARED_SUBFOLDER}/architecture.md — tech stack, architectural decisions, naming conventions
- {ARTIFACT_MAIN_FOLDER}/{SHARED_SUBFOLDER}/ux.md — UX design decisions, component inventory (if exists)

**Steps**

1. **Select the change**

   If a name is provided, use it. Otherwise:
   - Infer from conversation context if the user mentioned a change
   - Auto-select if only one active change exists
   - If ambiguous, list directories in `{ARTIFACT_MAIN_FOLDER}/{CHANGE_SUBFOLDER}/` (excluding `archive`) and use the **AskUserQuestion tool** to let the user select

   Always announce: "Using change: <name>" and how to override (e.g., `/sdd-implement <other>`).

2. **Inspect the change directory**
   List files in `{ARTIFACT_MAIN_FOLDER}/{CHANGE_SUBFOLDER}/<name>/` to understand which artifacts are present:
   - `proposal.md` — what & why
   - `design.md` — how
   - `tasks.md` — implementation steps
   - `specs/` — capability specs (if any)

3. **Read all change context**

   Read `{ARTIFACT_MAIN_FOLDER}/{CHANGE_SUBFOLDER}/<name>/tasks.md` first to get the task list and progress.

   Also read all available artifacts:
   - `proposal.md` — change scope and goals
   - `design.md` — technical approach and decisions
   - `specs/` — capability specifications (if any)

   **Handle task states:**
   - If `tasks.md` is missing: show message, suggest using `/sdd-propose` first
   - If all tasks are marked `[x]`: congratulate, suggest archiving
   - Otherwise: proceed to implementation

4. **Show current progress**

   Display:
   - Progress: "N/M tasks complete"
   - Remaining tasks overview

5. **Implement tasks (loop until done or blocked)**

   **Before starting the first task**, follow the **`sdd-tracker` skill** — set change `status` to `in-progress` and changelog entry "Implementation started on YYYY-MM-DD".

   For each pending task:
   - Show which task is being worked on
   - Make the code changes required
   - Keep changes minimal and focused
   - Mark task complete in the tasks file: `- [ ]` → `- [x]`
   - Continue to next task

   **Pause if:**
   - Task is unclear → ask for clarification
   - Implementation reveals a design issue → suggest updating artifacts
   - Error or blocker encountered → report and wait for guidance
   - User interrupts

6. **On completion or pause, show status**

   Display:
   - Tasks completed this session
   - Overall progress: "N/M tasks complete"
   - If all done: follow the **`sdd-tracker` skill** — set change `status` to `done` and changelog entry "Implementation completed on YYYY-MM-DD".
   - If paused: explain why and wait for guidance

**Output During Implementation**

```
## Implementing: <change-name> (schema: <schema-name>)

Working on task 3/7: <task description>
[...implementation happening...]
✓ Task complete

Working on task 4/7: <task description>
[...implementation happening...]
✓ Task complete
```

**Output On Completion**

```
## Implementation Complete

**Change:** <change-name>
**Schema:** <schema-name>
**Progress:** 7/7 tasks complete ✓

### Completed This Session
- [x] Task 1
- [x] Task 2
...

All tasks complete!. Proceed with verify
```

**Output On Pause (Issue Encountered)**

```
## Implementation Paused

**Change:** <change-name>
**Schema:** <schema-name>
**Progress:** 4/7 tasks complete

### Issue Encountered
<description of the issue>

**Options:**
1. <option 1>
2. <option 2>
3. Other approach

What would you like to do?
```

7. **Proceed with verify**

After update tasks and sdd-tracker, run **`/sdd-verify <change-name>`** skill to confirm implementation matches the spec.

**Guardrails**
{SKILL_ASSETS_NOTICE}
- Keep going through tasks until done or blocked
- Always read context files before starting (from the apply instructions output)
- If task is ambiguous, pause and ask before implementing
- If implementation reveals issues, pause and suggest artifact updates
- Keep code changes minimal and scoped to each task
- Update task checkbox immediately after completing each task
- Pause on errors, blockers, or unclear requirements - Do not guess
- Use contextFiles from CLI output, Do not assume specific file names

**Fluid Workflow Integration**

This skill supports the "actions on a change" model:

- **Can be invoked anytime**: Before all artifacts are done (if tasks exist), after partial implementation, interleaved with other actions
- **Allows artifact updates**: If implementation reveals design issues, suggest updating artifacts - not phase-locked, work fluidly
