---
name: keep-going
description: Hand a task to claude-limit-runner so it survives usage limits — it runs headless, and when a 5-hour or weekly limit blocks it, waits for the reset and resumes the same session automatically. Use when the user says "keep going", "keep working on this", "don't stop when you hit the limit", "run this overnight", "pick this back up after the limit resets", or wants to check on / stop a run already in progress.
---

# keep-going

Starts, checks, or stops a `claude-limit-runner` background run. The runner is a
shell script — this skill is a thin front door to it, nothing more. All the logic
lives in the script.

## Preflight

Confirm the runner is installed:

```bash
command -v claude-limit-runner
```

If it is missing, tell the user to run `install.sh` from the claude-limit-runner
repo, and stop. Do not try to reimplement the behaviour inline.

## Choosing what to do

Read the user's argument:

| They said | Do this |
|---|---|
| a task description | **Start** a new detached run for that task |
| `off`, `stop`, `cancel` | **Stop** the current run |
| `status`, `check`, nothing at all | **Report** current status |
| `logs`, `what's it doing` | **Tail** the log |
| `here`, `this session`, `take over` | **Hand off** the current session (see below) |

## Start a run

Run it from the user's current working directory so the task has the right context:

```bash
claude-limit-runner on "<the task, stated concretely>" \
  --done-when '<shell command that exits 0 only when truly finished>' \
  [-- <any claude flags they asked for>]
```

### Always try to supply --done-when

**The most common way a long run fails is not a usage limit — it is Claude
stopping early.** On a long task list a model does part of the work and signs off.
Without `--done-when` the runner believes it and exits reporting success. This has
really happened: two overnight runs stopped roughly two-thirds through and were
logged as completed.

So before starting, work out a *mechanical* completion condition — something a
shell command can verify:

| The task involves | A checkable done-condition |
|---|---|
| a plan file with checkboxes | `! grep -q "^- \[ \]" docs/plan.md` |
| several plan files | `! grep -rq "^- \[ \]" docs/plans/` |
| code that must pass gates | `npm test && npx tsc --noEmit` |
| a deploy | `curl -sf https://the-site/ > /dev/null` |
| a build artifact | `test -f dist/bundle.js` |
| a written handoff | `grep -q "$(date +%F)" docs/HANDOFF.md` |

Combine with `&&` when several must hold. Prefer conditions the *task itself*
maintains — asking the plan to tick its own checkboxes and then grepping for
unticked ones is the most reliable pattern.

If the work has no checkable condition, say so plainly and offer to add one — for
example, ask the task to tick checkboxes in a plan file, then check those. Starting
a long run with no done-condition is worth flagging as a real risk, not glossing
over.

### Permissions

Headless Claude cannot show a permission prompt, so anything that would normally
ask is silently refused. If the task needs to edit files, pass a permission mode
after `--` (e.g. `-- --permission-mode acceptEdits`). If the user has not said
which they want, ask rather than choosing for them. If a run reports permission
denials in its log, that is the cause.

Write the task as a complete, self-contained instruction — the runner starts a fresh
Claude session that cannot see this conversation. Include the paths, the goal, and
what "done" looks like. If the user's request is vague ("keep going on that thing"),
restate what you understand the task to be and confirm before starting.

Only pass flags after `--` if the user actually asked for them (a specific model, a
permission mode, a budget cap). Do not add flags of your own.

Then report back: the pid, the log path, and how to stop it.

## Hand off the current session

When the user wants *this* conversation continued rather than a new task, pass the
current session id and fork it, so the runner works from a copy of this session's
context instead of fighting over the live one:

```bash
claude-limit-runner on --resume "<current session id>" --fork-session "<what to continue doing>"
```

The current session id is in the session's own metadata. If you cannot determine it
reliably, say so and start a normal run with a written-out task instead — do not
guess a session id.

## Stop, status, logs

```bash
claude-limit-runner off
claude-limit-runner status
claude-limit-runner logs        # add -f to follow
```

Summarise `status` output in a sentence or two rather than dumping it verbatim:
whether it is running, which iteration it is on, and when it next checks for the
limit lifting.

## Notes to pass on when relevant

- The runner holds the Mac awake with `caffeinate` while it waits. It cannot wake a
  machine that is already asleep, and it cannot keep a laptop awake with the lid
  closed on battery. For an overnight run: lid open, plugged in.
- Defaults: gives up after 20 Claude invocations or 8 hours of total waiting. Mention
  `--max-iterations` / `--max-wait` if the user wants a longer run.
- One run at a time. Starting a second refuses until the first is stopped.
- Resuming defaults to `--resume-mode summary`: each leg is a fresh session carrying
  a written brief (task + commits so far + what is still owed). This is much cheaper
  than replaying the transcript. Use `--resume-mode fork` only when in-session
  continuity genuinely matters, and warn that it costs significantly more.
- `--notify` fires on every state transition. Worth suggesting for overnight runs so
  the user is not relying on noticing it themselves.
- `status` re-runs the done-check and shows recent commits, so it answers "is it
  actually done" rather than "is the process alive".
