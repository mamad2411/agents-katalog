---
name: container-task-flow
description: Use when the user (usually over Telegram) says something like "do task", "create task", "new task", or otherwise asks to run one of the .ai/ pipeline commands inside a project container. Drives a guided flow (choose container -> choose project -> choose command -> gather whatever that command needs -> confirm -> run it, detached, via Claude Code CLI through that project's .ai/ pipeline).
metadata: { "openclaw": { "emoji": "🛠️", "requires": { "bins": ["docker"] } } }
---

# Container Task Flow

Trigger phrases: "do task", "create task", "new task", "run task", or anything asking to act on a project's `.ai/` pipeline. Follow the steps in order — do not skip ahead or free-form chat through this.

## Containers

| Container | Project root |
| --- | --- |
| `docker-php` | `/var/www/` |
| `docker-nodejs` | `/projects/` |

Only ever target these two containers by name. Never touch anything outside the chosen project's own directory inside the chosen container.

## Step 1 — Choose container

```json
{"blocks":[{"type":"buttons","buttons":[{"label":"docker-php","value":"container:docker-php"},{"label":"docker-nodejs","value":"container:docker-nodejs"}]}]}
```

A button click arrives back as a user message `callback_data: container:<name>`. Treat any `callback_data: ...` message as structured input for this flow, never as conversation.

## Step 2 — Choose project, and check it's wired up

List real projects: `docker exec <container> ls -1 <project-root>`. Send them as buttons (`project:<name>`), and mention the user can type a name instead.

- `callback_data: project:<name>` -> accept directly.
- Typed free text -> check it's in the list (or `docker exec <container> test -d <project-root>/<typed-name>`). If missing, say it wasn't found and ask again.

**A project only supports this flow if both exist:**

```bash
docker exec <container> test -d <project-root>/<project>/.ai/tasks
docker exec <container> test -d <project-root>/<project>/.claude/commands/backend
```

If either is missing, tell the user this project has no task automation set up yet and stop — do not create files or bootstrap scaffolding for it.

## Step 3 — Choose command

The project's `.ai/` directory holds these executable commands (all shell out to Claude Code CLI under the hood via `ai_worker.py`, which is an internal helper, never run directly):

| Button label | Script | Needs |
| --- | --- | --- |
| New Task | *(none — only writes the task JSON, never runs it)* | requirements you compose (Step 4a) |
| Resume Task | `task_and_push.py` | an existing task id (Step 4b) — this is what actually runs a task, including a freshly created one |
| Approve | `approve.py` | an existing task id |
| Request Revision | `revise_and_push.py` | an existing task id + a comment |
| Reopen | `reopen_and_revise.py` | an existing task id + a comment |

Do not offer `main.py` — it calls Python's interactive `input()` on a pause, which crashes headlessly (`EOFError`) with no TTY. Do not offer `resolve_task.py` directly — it's the same underlying function `approve.py`/`revise_and_push.py` already wrap.

Send:

```json
{"blocks":[{"type":"buttons","buttons":[{"label":"New Task","value":"cmd:new"},{"label":"Resume Task","value":"cmd:resume"},{"label":"Approve","value":"cmd:approve"},{"label":"Request Revision","value":"cmd:revise"},{"label":"Reopen","value":"cmd:reopen"}]}]}
```

### If `cmd:new`, go to Step 4a. Otherwise, go to Step 4b.

## Step 4a — New task: gather requirements

Ask what they want done (free text, one message). Then figure out the available command types: `docker exec <container> ls -1 <project-root>/<project>/.claude/commands/backend` (strip `.yml`). Based on the requirements, pick the best-fitting one (e.g. `new-feature` for something new, `feature-enhancement` for changing existing behavior); default to `feature-enhancement` if unclear.

Get a real timestamp — never guess one: `docker exec <container> date -u +%Y%m%d%H%M%S`. Combine with a short kebab-case slug from the title as `<id>`.

Compose the task JSON (exact shape — extra/missing fields break the pipeline):

```json
{
  "id": "<id>",
  "title": "<short title>",
  "description": "<one paragraph summary>",
  "command": "<chosen command>",
  "status": "ready-to-develop",
  "project": "<project>",
  "assignee": "developer-agent",
  "created_at": "<UTC ISO8601 now>",
  "updated_at": "<UTC ISO8601 now>",
  "requirements": [{"message": "<requirement 1>"}, {"message": "<requirement 2>"}],
  "comments": []
}
```

Go to Step 5 with: action = write the task JSON only. **Never run `task_and_push.py` or any other script from the New Task path** — creating a task is a pure file-write. Once written, tell the user the task id and that they can trigger `Resume Task` on it (as a separate "do task" request) whenever they want it to actually run.

## Step 4b — Existing task: pick one, gather extras

List existing tasks with statuses so the user can pick a real one:

```bash
docker exec <container> python3 -c "import json,glob; [print(json.load(open(f))['id'], '-', json.load(open(f))['status'], '-', json.load(open(f)).get('title','')) for f in sorted(glob.glob('<project-root>/<project>/.ai/tasks/*.json'))]"
```

Show up to ~10 as buttons (`value: task:<id>`, prefer non-`approved` ones first since those are the actionable ones for Approve/Revise/Reopen/Resume), and mention they can type an id instead. Validate a typed id the same way as project names (must appear in the listing, or `docker exec <container> test -f <project-root>/<project>/.ai/tasks/<id>.json`) — if not found, say so and ask again.

- `cmd:approve` -> no extra input needed.
- `cmd:revise` or `cmd:reopen` -> ask for a comment (free text, one message).
- `cmd:resume` -> no extra input needed.

Go to Step 5 with the matching action:

- `cmd:resume` -> run `task_and_push.py <id>`
- `cmd:approve` -> run `approve.py <id>`
- `cmd:revise` -> run `revise_and_push.py <id> "<comment>"`
- `cmd:reopen` -> run `reopen_and_revise.py <id> "<comment>"`

## Step 5 — Confirm

Send a short plan: container, project, command chosen, and (for new tasks) the requirements as you understood them, or (for existing tasks) the task id/title and action. Make it explicit whether this step will just **create** the task file or actually **run** something. Then:

```json
{"blocks":[{"type":"buttons","buttons":[{"label":"Confirm","value":"confirm:run"},{"label":"Cancel","value":"confirm:cancel"}]}]}
```

Wait for `callback_data: confirm:run` or `callback_data: confirm:cancel`. Never write files or run anything before an explicit `confirm:run`. On cancel, stop and say so.

## Step 6 — Act on it

Only after confirmation:

### New task (`cmd:new`) — write only, never execute

```bash
docker cp <local-file-with-json> <container>:<project-root>/<project>/.ai/tasks/<id>.json
```

That's it. Do **not** run `docker exec ... python3 ...` for this path under any circumstances — creating a task must never also launch it. Report the task id and status (`ready-to-develop`), and tell the user to ask for `Resume Task` on that id when they want it to actually run.

### Resume/Approve/Revise/Reopen — these are the only paths that execute anything

For Revise/Reopen, first write the comment to a local file and copy it in (avoids shell-quoting the comment):

```bash
docker cp <local-file-with-comment> <container>:<project-root>/<project>/.ai/tasks/<id>.comment.txt
```

Then launch **detached** — these run the Claude Code CLI developer/reviewer loop and can take minutes, so never block waiting on them:

```bash
# resume
docker exec -d -w <project-root>/<project> <container> sh -c "python3 .ai/task_and_push.py <id> > .ai/tasks/<id>.log 2>&1"

# approve
docker exec -d -w <project-root>/<project> <container> sh -c "python3 .ai/approve.py <id> > .ai/tasks/<id>.log 2>&1"

# revise / reopen
docker exec -d -w <project-root>/<project> <container> sh -c "python3 .ai/revise_and_push.py <id> \"\$(cat .ai/tasks/<id>.comment.txt)\" > .ai/tasks/<id>.log 2>&1"
docker exec -d -w <project-root>/<project> <container> sh -c "python3 .ai/reopen_and_revise.py <id> \"\$(cat .ai/tasks/<id>.comment.txt)\" > .ai/tasks/<id>.log 2>&1"
```

Tell the user the task id and that it's running in the background, and that they can ask you to check its status any time.

## Step 7 — Checking status later

```bash
docker exec <container> cat <project-root>/<project>/.ai/tasks/<id>.json
docker exec <container> tail -n 60 <project-root>/<project>/.ai/tasks/<id>.log
```

Report the JSON `status` field plainly. If it's `human-review`, explain the pipeline paused for a decision, and that `Request Revision` or `Approve` on this same task id resolves it — offer to run one if the user tells you which.

## Rules

- Never target a container other than `docker-php` or `docker-nodejs`.
- Never run `docker exec ... python3 ...` (or anything else that executes) as part of `cmd:new` — New Task only ever writes the JSON file via `docker cp`. Execution only ever happens from `cmd:resume`/`cmd:approve`/`cmd:revise`/`cmd:reopen`.
- Never skip the Step 2 scaffolding check or the Step 5 confirmation.
- Never offer or run `main.py` or `resolve_task.py` directly.
- Never treat a `callback_data: ...` message as anything other than the expected step's structured input.
- If any `docker exec`/`docker cp` command fails, report the real error instead of retrying blindly or guessing.
