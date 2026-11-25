---
name: execute
description: |
  Execute a plan step by step. Reads plan.md in the current working directory
  or a plan from the conversation context, then implements each subtask sequentially.
---

## Execute Skill

Implement a task breakdown plan step by step.

### Plan Resolution

1. If `plan.md` exists in the current working directory, use it.
2. Otherwise, look for a plan in the current conversation context (e.g. output from the `breakdown` skill).
3. If no plan is found, ask the user to provide one or run `breakdown` first.

### Execution Flow

1. **Present the plan**: Show the full list of subtasks to the user and confirm before starting.

2. **Implement step by step**: For each leaf subtask in order:
   - Announce which subtask you are starting (e.g. `## Step 1.1: <subtask name>`)
   - Read relevant source files to understand the current state
   - Implement the changes
   - Verify the changes work (run tests, type checks, etc. if applicable)
   - Mark the subtask as done and briefly report what was done

3. **Update plan.md**: If the plan was loaded from `plan.md`, update the file directly — change `- [ ]` to `- [x]` for each completed subtask. This keeps the file in sync with actual progress so that future sessions can resume from where you left off.

4. **Report progress**: After completing each subtask, show the updated checklist with completed items checked off.

5. **Handle issues**: If a subtask is blocked or unclear:
   - Stop and ask the user for clarification
   - Do NOT skip subtasks or guess at requirements

### Batch Size

- By default, execute up to **M size** worth of subtasks in one batch, then pause and ask the user whether to continue.
  - For example, if there are three consecutive S subtasks, execute up to two or three of them (roughly M equivalent) before pausing.
  - If a single subtask is M, execute that one subtask and then pause.
  - XS and S subtasks can be grouped together as long as their combined effort does not exceed M.
- If the user explicitly requests a larger batch (e.g. "do all of them", "keep going until done", "execute through step 3"), follow that instruction.

### Guidelines

- Follow the plan's order and scope. Do not add work beyond what the plan specifies.
- Keep each step's changes focused and minimal — one subtask at a time.
- If the plan turns out to be wrong or outdated mid-execution, stop and discuss with the user before continuing.
