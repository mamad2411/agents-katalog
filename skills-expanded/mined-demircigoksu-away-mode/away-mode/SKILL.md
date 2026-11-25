---
name: away-mode
description: Finish every job in a task file autonomously while the user is away from the keyboard (asleep, in a meeting, travelling), asking nothing and verifying every step. Use when the user hands over a task list and says they will be away, offline, asleep, or unreachable. Triggers "I'm going to sleep", "you have full authority", "handle it while I'm out", "don't ask me anything", "finish this overnight", "work while I'm asleep", "autonomous run", "unattended".
---

# Away Mode: finish the work while nobody is at the keyboard

## Purpose

Take a task file, complete every job in it, **prove** each one with an
independent check, and leave one handoff report. Asking questions is
forbidden. Deciding is mandatory.

## Variables (resolved fresh on every run)

Derive these from the user's message and the task file. None of them is fixed,
and none of them is worth stopping for.

| Variable | Meaning | Default when absent |
|---|---|---|
| `TASK_FILE` | The task list (tasks.md, todo.md, backlog.md, sprint.md, a Notion or Drive page, or the message itself) | Search connected folders for `task*.md`, `todo*.md`, `backlog*.md`, `sprint*.md`; if exactly one candidate, use it |
| `TASK_COUNT` | How many jobs (7, 3, 12, "all of them") | Count the top-level items in the file |
| `AWAY_MODE` | Where the user is: asleep / busy / mobile / just "away" | `away` (assume no interaction) |
| `AWAY_WINDOW` | How long they are gone (overnight, two hours, unknown) | Unknown: build the run so it can continue indefinitely |
| `PROJECT_ROOT` | Where the work happens | The task file's folder |
| `VERIFY_TARGETS` | What must be proven: server, database, API, build, tests, live page | Derive from the task file; at least one end-to-end check is mandatory |
| `RESUME_POLICY` | What happens if the session dies | Scheduled task that picks up where it stopped |

`TASK_COUNT` is not a target, it is a **checksum**. If the file yields a
different number than the user said, note the difference in the report and
proceed with the file's number.

## The run

### 0. Gather context (do not ask)

1. Find `TASK_FILE` and read all of it. If you cannot: search connected
   folders, the device bridge (`device_bash` / a local filesystem MCP), and
   uploaded files. Still nothing? Apply the "no file" protocol in
   `references/variable-resolution.md`: write the jobs from the user's message
   into a task file yourself, then work from that.
2. Read the project's own context: `README`, `CLAUDE.md`, `AGENTS.md`,
   `docker-compose.yml`, `.env.example`, the migrations folder, deploy scripts.
   A repo's own conventions outrank your habits.
3. Read persistent memory if the session has it. The user's stack, servers and
   preferences may already be on file.
4. If a `progress.json` from an earlier session exists, **resume from it**.

### 1. Set up the state file

Create `PROJECT_ROOT/.away-mode/progress.json` (schema:
`assets/progress.schema.json`). One entry per job: `id, title, status,
verification, evidence, assumptions, notes`.

This file is the single source of truth. Update it the moment a job closes; if
the session drops, the next run continues from here.

At the same time open a visible task list (`TaskCreate`): one item per job,
plus a final "end-to-end verification" and "handoff report".

### 2. One loop per job

Full version in `references/work-loop.md`. In short:

```
READ  ->  PLAN  ->  APPLY  ->  VERIFY  ->  RECORD EVIDENCE  ->  WRITE STATE
                       ^                        |
                       +------- fix <-----------+     (3 rounds max)
```

- **APPLY**: change files where they live. Edit the user's files in place
  (`sed -i`, a short read-modify-write script), never by retyping content from
  tool output, which may have been truncated.
- **VERIFY**: do not claim, prove. "The code ran" is not proof; run something
  that reads the result back.
- A job that still fails after 3 fix rounds is marked `blocked` with what was
  tried and why, and **the run moves on**. One job never stops the flow.

### 3. Server and database verification (mandatory)

A job is not done until the **persistent state on the server** has changed.
For each job run whatever applies and keep the output as evidence:

- Schema change: did the migration actually run (`alembic current`,
  `prisma migrate status`, `\d table`, an `information_schema` query).
- Data change: `SELECT` the row count and a sample row, before and after.
- API: call the live endpoint and keep the body (a 200 is not enough, read it).
- App: is the container up, is the log clean (`docker compose ps`,
  `logs --tail`).
- Cache/CDN: is the change actually being served.

Commands and details: `references/verification.md`. Back up before writing:
`references/verification.md#backups`.

Prefer the repo's own deploy and status tooling over raw commands. That path is
the tested one, and ad hoc scripts can trip the user's security software.

### 4. Do not ask. Decide, then record the decision

While `AWAY_MODE` is on, `AskUserQuestion` is not used. When something is
ambiguous:

1. Take the task file's wording literally.
2. Copy the pattern already in the project (same naming, same layer).
3. Choose the reversible option.
4. Write the choice into `progress.json` -> `assumptions` as one sentence, and
   surface it in the report.

**One exception: irreversible work.** Unless the task file explicitly permits
it, do not run these; prepare them and leave them for approval: deleting
production data, `DROP`/`TRUNCATE`, one-way migrations, sending mail or
messages to the outside world, payments, DNS or domain changes, force pushes,
overwriting without a backup. Write the script, produce the dry-run output, and
put it in the report as "one command, with your approval".

### 5. Keep the run alive (the user is still away)

If the work is long or the session may be interrupted, keep it going:

- For long steps, schedule your own return (`send_later` / `ScheduleWakeup`).
- If the session can close entirely, create a scheduled task that **resumes
  from the state file**; write the prompt so it stands alone and embed the
  `progress.json` path in it. Do not use in-session cron tools, they die with
  the session.
- When everything is done, delete the scheduled task.

Template prompt: `references/resume-trigger.md`.

### 6. Handoff report

When the run ends (or the user comes back), leave exactly one report:
`PROJECT_ROOT/HANDOFF.md`, template `assets/handoff-template.md`.

It contains: a job-by-job status table, **evidence** for each job (command plus
the critical output), the decisions and assumptions you made, what is blocked
and why, irreversible work waiting for approval, and a "three things to do when
you wake up" list.

Deliver it as a file (`SendUserFile`, plus write it into the connected folder)
and give a five-line summary in chat. No essays, tables and evidence.

## Definition of done

Per job: `status = done` **and** `evidence` is non-empty **and** the
verification ran where the change has to be true (the server, not only your
laptop). If any of the three is missing, the job is not `done`.

## References

- `references/variable-resolution.md` - finding the variables, and what to do when there is no task file
- `references/work-loop.md` - the per-job loop, error handling, blocked jobs
- `references/verification.md` - server/DB/API checks and backups
- `references/resume-trigger.md` - surviving a dropped session
- `assets/task-file-template.md` - the task file template to hand the user
- `assets/progress.schema.json` - state file schema
- `assets/handoff-template.md` - report template
