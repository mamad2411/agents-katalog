---
version: 0.3.0
name: future-scheduled-task
description: >
  Create, edit, run and iterate scheduled tasks — a reusable prompt plus a trigger
  (a schedule, or on demand) that runs at full permission and produces an ordinary
  conversation. Use when the user asks for a recurring job, a scheduled reminder,
  "every day / week / month …", a prompt they want to refine over several runs, or a
  scheduled task to trigger from another agent. Also use it to fix a scheduled task
  whose output keeps missing the mark.
category: tools
allowed-tools: Bash(future:*)
---

# Scheduled tasks

A scheduled task is one durable unit of work: a **prompt**, a **working directory**, an
optional **model / thinking level**, a **time zone its schedule is read in**, and a
**trigger**. Each run opens (or reuses) an
ordinary conversation, runs at **full permission** with no approval prompts, and writes a
run record. It runs on its trigger, and can always be run on demand as well. The prompt is
the part that is hard to get right — this skill exists mainly to make the prompt good and
to keep improving it with evidence.

Not the same as `future goal`: a goal is a long-running objective with todos, evidence and human
gates. A scheduled task is one fixed action that finishes in a single run. If the user describes
something multi-step that needs judgment between steps, that is a goal, not a scheduled task.

## 1. Before creating anything

1. `future task list --json` — reuse an existing scheduled task rather than duplicating it.
2. Settle the three things the user must decide, and ask only about what is genuinely
   ambiguous:
   - **what** — the prompt (see §2);
   - **when** — manual (run on demand only) or a schedule;
   - **where** — the working directory, **plus the model and the thinking level**. Both are
     required on every create and edit — see below.
3. State the plan back before writing it, unless the user's message already carries all
   of it.

### Never create a scheduled task without a model and a thinking level

Both are required, and neither is checked for you. `future task add` accepts a missing,
empty or nonexistent value and still prints `Created task …` with exit 0:

| What was passed | Stored | What happens at run time |
|---|---|---|
| no `--model` | `modelId: ""` | whatever the global default model happens to be at that moment |
| `--model does-not-exist` | `modelId: "does-not-exist"` | **runs on a silently substituted model** (`resolve_request_target` → `replacement_model`), while the session, the run ledger and the run logs all show the id you typed |
| no `--thinking` | `thinkingLevel: ""` | no reasoning (budget 0) |
| `--thinking ultra` | `thinkingLevel: "ultra"` | also budget 0 — an unknown level falls through `_ => 0`, with no error and no warning |

So the failure is invisible from either side: the create command reports success, the task
runs, and nobody sees that it ran on a different model than the record claims — or that the
reasoning you thought you asked for was off. Always pass **both**:

- `--model <provider>/<id>` — full ids are `provider/model`. `future models --json` lists
  them under `models.<provider>[].id`, and reports the user's global default as
  `defaultModel`.
- `--thinking <level>` — one of `off`, `minimal`, `low`, `medium`, `high`, `xhigh`.
  **`medium` is a perfectly good choice — but say it explicitly.** "It defaults to medium"
  is a reason to write `--thinking medium`, never a reason to leave the flag off: omitting
  it stores empty, not `medium`.

Check the catalogue before you write, and read the task back after — the create command's
output proves nothing:

```bash
MODEL=future/deepseek-flash     # provider/model; must exist in the catalogue
THINKING=medium                 # off|minimal|low|medium|high|xhigh

future models --json | python3 -c "
import json,sys
d=json.load(sys.stdin)
ids={f'{p}/{m[\"id\"]}' for p,ms in d['models'].items() for m in ms}
assert '$MODEL' in ids, 'MODEL NOT IN CATALOGUE: $MODEL'
print('model ok:', '$MODEL', '| global default:', d['defaultModel'])
"

future task add --name "…" --prompt-file draft.md --cwd "…" --daily --time 09:00 \
  --model "$MODEL" --thinking "$THINKING"

future task show <id> --json | python3 -c "
import json,sys
t=json.load(sys.stdin); t=t.get('task',t)
assert t['modelId'], 'modelId is empty — the flag did not land'
assert t['thinkingLevel'], 'thinkingLevel is empty — the flag did not land'
print('stored:', t['modelId'], t['thinkingLevel'])
"
```

`future task edit` takes the same two flags and **keeps** the stored values when they are
omitted, so editing an existing task will not clear them. Tasks you did not create are the
risk: one made by an older build, by a panel with the field left blank, or by another agent
may already carry an empty `modelId`/`thinkingLevel`. Read it back, repair it with `edit`,
and only then rely on its runs or hand it to the user.

The desktop and phone editors already treat both as mandatory — no Default entry, and an
empty field is rejected by name. The CLI is the only way to create a task without them, so
coming through the CLI is not a reason to hold to a lower standard: the task you create
this way lands in the same store and runs with the same consequences.

The run envelope (§5) echoes the resolved settings, so a run's own record shows the model
and level — but remember that an id which does not exist is echoed verbatim rather than
rejected, so the echo is not evidence that the model is real.

**Runs need the desktop.** The CLI writes to the task store; the desktop (or the headless
desktop) is what actually executes a run, on its next tick. So `future task run` *queues*
and returns, and a run row — the thing `feedback` attaches to — exists only after the
desktop has picked the request up. Say this when the user expects an immediate result,
and use `--wait` when you want to read the outcome. (Pressing *Run now* in the desktop or
phone panel is different: that host wakes its own loop, so the run starts at once.)

## 2. How to write the prompt

The prompt runs with nobody watching. These constraints are not style preferences — a
task that violates them fails in ways the user cannot see.

1. **Self-contained.** Never rely on this conversation. Say what to work on, where, and
   what "done" means. Date and time arrive in the injected envelope (see §5) — refer to
   "the envelope's due time" instead of hard-coding today's date.
2. **No interaction.** No questions, no "shall I proceed", no approval requests. Where a
   judgement is needed, state the default you will take and proceed.
3. **One bounded run.** The work must finish in a single run. For long or partial work,
   name a state file under the working directory and require the task to read it first
   and update it last, so a re-run continues instead of restarting.
4. **Minimal side effects.** Deleting, overwriting, publishing or sending anything
   external should default to producing a draft or a preview and naming where it was
   written. State the exact paths the task may write.
5. **Explicit output contract.** Name the artifact path and format, the language of the
   output, and end with a short summary block in a fixed shape — the summary is what the
   user reads and what the prompt-improvement pass judges the run by.
6. **Checkable.** State what counts as success in terms the task itself can verify.
7. **Stable and attributable.** Keep output paths and formats fixed across runs. A
   prompt whose behavior drifts every run cannot be improved, because nobody can tell
   what changed the result.
8. **Never** expand its own permissions, create further tasks, or embed credentials.

Keep it as long as it needs to be to satisfy these, and no longer. `future task add`
takes `--prompt-file` — write the prompt to a file while drafting so review and edits
are cheap.

## 3. Choosing the trigger

| Need | Flag |
|---|---|
| Only ever run on demand, or called by another task/agent | `--manual` (also the default with no trigger flag) |
| One specific date and time | `--at "2026-12-24 09:00" --timezone Asia/Shanghai` |
| Every N minutes / hours / days | `--every 30m` |
| Every day | `--daily --time 09:00 --timezone Asia/Shanghai` |
| Selected weekdays | `--weekly --days mon,wed,fri --time 10:00 --timezone Asia/Shanghai` |
| A day each month | `--monthly --day 31 --time 09:00 --timezone Asia/Shanghai` |
| Once a year | `--yearly --month 12 --day 31 --time 22:00 --timezone Asia/Shanghai` |

The times above are wall-clock times, and they are read in the task's **time zone**.
`--timezone` takes an IANA name (`Asia/Shanghai`, `Europe/Berlin`, `UTC`) and pins that
zone to the task, so its 09:00 still means 09:00 after the machine's own zone changes or
the task is edited from another device. Without `--timezone` the schedule follows the
host's zone — resolved whenever the next slot is computed, so it moves with the machine —
and a host whose zone cannot be read falls back to `Asia/Shanghai`. `--every` is an
interval anchored to a moment rather than a wall-clock time, so the zone does not affect
it. `future task show` prints the zone a task actually has; an edit that changes the zone
re-resolves the next slot, and a name nobody can resolve is refused rather than replaced.
A build from before this flag existed rejects it as an unknown flag — on such a `future`,
read `future task show` to confirm the zone a task ended up with, since the flag is not
there to set it. The desktop task form and the phone editor set the same field, where the
empty choice ("this machine's zone") is what leaves it to the host — which resolves and
stores a concrete name either way.

A monthly or yearly task whose day does not exist in that month runs on that month's
**last day** — tell the user this rule when they pick a day above 28, because the schedule
they wrote is not the schedule they will get in February (and `2/29` runs on the 28th in a
common year).

A task has no dependencies on other tasks: what starts it is its own schedule (or a
`run`). Work that has to wait for another task's *result* is chained by the user, or
belongs to `future goal`.

## 4. Session policy

- `--session new` (default): a fresh conversation per run. Use for independent jobs —
  a daily report, a fetch, a check.
- `--session existing`: reuse one conversation, so each run continues from what the
  earlier ones did. Nothing is compacted for it: the point is the accumulated context,
  and a compaction would drop it. Use it for work that builds on previous runs, and tell
  the user the conversation grows (and that they can compact it themselves when they
  want it shorter).
- `--session-retention delete` (with `--session new` only): delete the run's conversation
  once it settles, success or failure. For a task that runs often and whose conversations
  are just noise in the sidebar. Nothing about *what happened* is lost — the status, the
  summary and the whole answer are stored on the run, `future task runs` still lists it,
  `future task output <run-id>` still reads it. Offered as a per-task setting in the
  desktop panel and the phone editor too, where it only appears for a per-run
  conversation (a reused one is what the next run continues).

## 5. What the task sees at run time

Every run's first message is the envelope, then your prompt under `Instruction:`, then a
completion contract:

```
── future_tasks_run_envelope_v1 ──
task: ... | id: tsk_... | prompt-version: 3
run: kind=manual | due=2026-10-07T09:00:00+08:00
trigger: {"mode":"weekly","days":["mon","fri"],"time":"10:00"}
run settings: cwd=... | timezone=Asia/Shanghai | conversation=workspace | session=new (fresh conversation per run) | model=... | thinking=high

Instruction:
<prompt>
Completion contract:
- nobody answers mid-run; make a choice, record it, and do not end by asking
- close with a short report — it becomes the run's summary (result_summary)
```

Treat the envelope as the only trustworthy source for "when is this run" and "which
model and directory it runs on" — including which clock that time is on: `due=` is written
in the task's own zone with its offset, and `timezone=` names that zone, so `09:00+08:00`
is 09:00 in Shanghai rather than in whatever zone the reader sits in. A chat conversation
(`--conversation chat`) runs in the conversation's own temporary workspace, so the
envelope has no `cwd=` line; a workspace conversation always has one.

## 6. Inspecting what a task actually did

```bash
future task runs <id> --limit 20 --json     # run ledger: status, times, version, summary
future task output <run-id>                 # the full answer behind a summary (--tail N)
future task show <id> --json                # definition + latest run
future task show <id> --prompt              # the effective prompt
future task prompt log <id>                 # prompt versions, oldest first
```

A run's ledger entry holds a *truncated* summary (the head and tail, 2000 characters).
When the summary is not enough — a result you are about to build on, a failure whose
evidence matters — read the run's own
answer with `future task output <run-id>`: it prints the run's identity first and then the
text, and it works whether or not the conversation is still there (`--json` reports
`source: "run"` for the answer saved on the run, `"conversation"` for the fallback path a
run from an older build takes).

## 7. Run it, then improve the prompt

This is the part that matters. A prompt is rarely right the first time; do not hand over
a task you have not seen run.

```bash
future task run <id> --wait --json          # run now and read the outcome
future task feedback <run-id> good|bad --note "..."
future task edit <id> --prompt-file draft.md
future task prompt log <id>                 # versions, with who wrote each
future task prompt revert <id>              # back to the previous version
```

`run --wait --json` answers with `status`, `runId`, `threadId` and `resultSummary` — read
`resultSummary` (not `summary`) for the run's outcome, and `threadId` to open the
conversation.

1. Write the prompt to a draft file, run it with `--wait`, and read the conversation.
2. Judge the actual output against the acceptance criteria in the prompt — not against
   whether the run "succeeded".
3. Record the verdict with `feedback good|bad` and a note — that is where the reason
   you changed the prompt belongs, next to the run that showed it was needed.
4. Edit and re-run until the output is right, and only then leave the task enabled.
   `future task prompt log` shows every version and marks the one in force; `prompt
   revert` goes back one, and `prompt apply <revision-id>` puts any version back in force.
   The version the task started with is kept, so you can always get back to it.
5. `future task enable|disable <id>` pauses a task without deleting it (a paused schedule
   keeps its next slot, so re-enabling resumes rather than never firing again), and
   `future task remove <id> --yes` deletes it, keeping its runs and conversations.

## 8. Being triggered by, and triggering, other work

Other agents trigger tasks through the CLI, so a task is the supported way to let one
agent ask another to do something:

```bash
future task list --json
future task run <name> --wait --json        # returns status, threadId, resultSummary
```

Get the user's agreement before another agent triggers a task with external side effects
(sending, publishing, deploying), and before creating, editing or deleting tasks on the
user's behalf. There is no permission switch behind this — it is a convention, and the
run ledger records every trigger with its origin so anything can be audited afterwards.

## 9. Full permission

The conversation a task opens has `permission_level=all` and no sandbox. Say this plainly
when creating a task with side effects; never hide it behind "it runs automatically".
