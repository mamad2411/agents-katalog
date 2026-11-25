---
name: ai-task-master
description: Schedule and manage automated task execution. Use this to run prompts or workflows later or on a recurring schedule without user interaction.
---

# AI Task Master

AI Task Master enables scheduling of autonomous actions. It should be used whenever a user wants something to happen in the future or repeatedly without being present.

---

## When to Use

Use this skill when the user:

- Wants something to run **later**
- Wants something to run **on a schedule**
- Describes a task as recurring (e.g. “every day”, “weekly”, “every 2 hours”)
- Uses phrases like:
  - “remind me”
  - “run later”
  - “schedule”
  - “every day / week / hour”

---

## When NOT to Use

Do NOT use this skill when:

- The task should happen **immediately**
- The task requires **user interaction**
- The instruction is **unclear or incomplete**
  - Instead: help the user refine the task into a clear, self-contained instruction

---

## Core Behavior

- Executes tasks **without user interaction** at a future time
- Does **not ask questions or confirmations**
- Assumes no user is present at runtime
- Tasks must be **fully self-contained**
- AI Task Master schedules execution but does not interpret intent

---

## Command Interface

The command structure is:
```bash
node skill.js [--action <create|list|delete|run>] [--task "<name>"] [--session "<name>"] [--prompt "<instruction>"] [--when "<schedule>"]
```

### Flags
#### `--action` 
Defines the operation to perform. Valid options include:
- `create` *(default)* — schedule a new task
- `list` — display existing tasks
- `delete` — remove a task
- `run` — execute a task immediately

**Notes:**
- May be omitted when creating a task (defaults to `create`)
- Required for `list`, `delete`, and `run`

#### `--task` *(optional)*
Defines the 'name' or 'id' of the scheduled task. If not provided it will be auto-generated.

#### `--session` *(optional)*
Defines the user-agent session that should be used for the automation (if supported by agent).
(Defaults to `scheduled-automations`)

#### `--prompt`
Defines the prompt that will be given to the AI agent when the task runs.

**Prompt Requirements:**
- Must be non-interactive
- Must be clear and complete
- Must persist output (file, log, etc.)

**Good Examples Prompts:**
- "Add a sage piece of wisdom to ~/lifetips.md"
- "prose run morning-brief.prose"
- "Scan email for failure alerts and save a timeline to off-hour-alerts-summary_DDMMYYYY.md"

**Example BAD Prompts:**
- "Help me {anything}" - _The prompt will run non-interactively._
- "Research {something}" - _The task will vanish when complete; the prompt should incude writing a file with findings for human review._

**Rule:** Never schedule vague instructions. Always resolve them into executable commands first.

#### `--when`
Describes when the task should run.

- **Valid Syntax**
  - Relative (future) Time
    - `2m`, `3h`, `1d`
    - `in 2h`
  - Time Today
    - `14:30`
    - `at 14:30`
  - Date + Time
    - `2026-03-21@09:00`
    - `on 2026-03-21@09:00`
  - Daily
    - `daily:09:00`
  - Weekly
    - `weekly:mon@08:00`
    - `weekly:mon,wed,fri@15:30`

**NOTE:**
  - If no 'daily' or 'weekly' prefix is provided → the task is treated as a one-time futureexecution

---

### Example Commands

#### List all tasks

```bash
# --list is shorthand for --action list
node skill.js --action list
```
or
```bash
# --list is shorthand for --action list
node skill.js --list
```

#### Create a task

```bash
# Use default values for action, task, session
node skill.js --prompt "<instruction>" --when "<schedule>"
```
or

```bash
# Use explicit values for all options
node skill.js --action create --task "<name>" -session "<session-name>" --prompt "<instruction>" --when "<schedule>"
```

#### Delete a task

```bash
node skill.js --action delete --task "<name>"
```
or
```bash
# --delete <taskname> is shorthand for --action delete --task <taskname>
node skill.js --delete <taskname>
```
#### Run an existing scheduled task now

```bash
node skill.js --action run --task "<name>"
```
or
```bash
# --run <taskname> is shorthand for --action run --task <taskname>
node skill.js --run <taskname>
```

---

## Workflow Integration (Critical)

AI Task Master does NOT decide what to run — it only schedules execution.

If the user refers to a workflow or named process - you MUST convert it into an explicit executable command.

### Example

User:
> Run the job search every morning at 8

Correct:

```bash
node skill.js --task "job-search" \
  --prompt "prose run projects/job-search/find-jobs.prose" \
  --when "daily:08:00"
```

Incorrect:

```bash
node skill.js --task "job-search" \
  --prompt "run job search" \
  --when "daily:08:00"
```

---

## Output Expectations
Tasks scheduled with this skill should:
- Prefer writing to files or logs
- Avoid conversational output
- Ensure results are persisted

---

## Heuristics
Use this skill if:
- The task happens **in the future**
- The task **repeats**
- The user cannot or will not be present

Do NOT use this skill if:
- The task should happen now

---

## Summary
AI Task Master schedules reliable, autonomous execution of tasks and workflows in the future or on a recurring basis.