---
name: aflow-operate
description: Operate a running Aflow stack from a terminal session on the operator's behalf — talk to a Helmsman, start and watch skill runs, read a run's tasks and payloads, resolve or decline a gate, read the plan board, debug a stuck run, judge an output. Use when the operator asks you to drive, watch, unblock or evaluate work in Aflow (local edition or hosted), whatever the work is about. Not for a commissioned change.
---

# Operating Aflow from a session

**Not for you if your task arrived as a commission or review brief** (Commission Change,
Local Code Review, "Make the change", a `host.harness.run` task): then you are the coding
agent the loop started, and the brief is the whole job. This skill is for the session that
sits beside the operator and drives the platform.

You act with the operator's own posture on their machine, as the loop's agents do
(`docs/dev/driving-work-through-the-loop.md`, "What a commission runs under"): you may
read anything the operator can read, start and watch runs, write to the board, decline a
gate with a reason, restart the operator's own stack when it is idle. Four acts stay the operator's, and you never take them on their behalf: approving a
gate (a push approval, a merge card, a write approval, an override), merging a pull request
by hand, widening egress, write policy or confinement, and renewing a credential. Arming a
schedule that acts on its own (a resident, a shepherd) is theirs too. When one of those is
the next step, say so and stop.

## Where everything is

| Thing         | Where                                                                                                                                                                                                                                 |
| ------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| API           | `http://localhost:3000/v1` on the dev stack (`yarn start`); the appliance and the hosted product answer the same routes on their own host                                                                                             |
| Auth          | `mcp.local.json` at the checkout root (copy `apps/aflow-mcp/mcp.local.json.example`); holds `apiKey`, `tenantId`, `sessionToken` — **never print the file**                                                                           |
| Bearer token  | `node -e 'const c=require("./mcp.local.json");process.stdout.write(c.apiKey)'`                                                                                                                                                        |
| Space         | every space-scoped call takes `spaceId`; find it with the MCP `space_list`, or `GET /v1/spaces`                                                                                                                                       |
| MCP server    | `aflow-local` (`yarn dev:mcp`, port 3100): `auth_status`, `space_list`, `catalog`, `run_operation`, `start_session`, `watch_session`, `watch_run`, `inspect_session`, `retry_session`, `fetch_payload` — CLAUDE.md "Local MCP server" |
| Postgres      | `DATABASE_URL` in `.env` (print the key name only); one schema per tenant, `t_<tenantId without dashes>`                                                                                                                              |
| Runs          | `workflow_runs` keyed by `run_id` (not `id`); `workflow_run_tasks` by `run_id` + `task_id`, with `output_ref` / `input_ref` / `failure_reason`                                                                                        |
| Conversations | `sessions`; `step_executions` by `session_id`, with `operation_id`, `status`, `error_ref`                                                                                                                                             |
| Board         | `plan_nodes` (`status`, `position`, `goal`, `criteria`, `note`, `outcome`, `revision`); `agent_schedules`                                                                                                                             |
| Payloads      | `GET /v1/payloads?ref=<url-encoded ref>&spaceId=…`; `inline:<base64>` refs decode locally                                                                                                                                             |

The MCP is the first choice when it is connected: it carries the catalog and the schemas,
and `start_session` / `watch_session` return a `continuation` to call verbatim when they
time out. The REST calls below are the fallback when the MCP is not connected, and the
shape the scripts use.

## Driving a Helmsman

The Helmsman is the space's agent. A conversation with it is a session; you send a message,
it runs, it pauses on `user_input` with its reply, or on a `workflow_run` while a skill it
started is in flight. [scripts/hm.sh](scripts/hm.sh) wraps the four calls (`new`, `send`, `status`,
`last`); pass **absolute** file paths and **full** session ids.

- New conversation: `POST /v1/sessions?spaceId=…` with
  `{ mode: "mcp", target: { kind: "platform-role", systemRole: "cybernetic-helmsman" }, input: { input: "<text>" } }` → `sessionId`.
- Reply: read `GET /v1/sessions/:id?spaceId=…`; when `status` is `PAUSED` and
  `requiredInput` is present, `POST /v1/sessions/:id/resume?spaceId=…` with
  `{ stepExecutionId: requiredInput.stepExecutionId, input: { input: "<text>" } }`. The
  input is keyed `input` — keyed by variable id it delivers an empty turn.
- Its last reply: `GET /v1/sessions/:id/chat-history?spaceId=…`, field `decision.message`,
  or `modelOutput` when the decision carries no message. `messages` holds only what the
  latest turn sent to the model, so the newest reply is not among them.
- A session blocked on a `workflow_run` cannot take a message; it queues until the run ends.
- A session that `FAILED` on a transient provider error: `POST /v1/sessions/:id/retry?spaceId=…` with `{}`.

Write the brief as a note to a capable colleague: the goal, what is already settled, the
ids it needs, what to report back, and "then hold". The Helmsman reads the board and its
memory; it does not read your terminal.

## Watching

Never wait in the foreground. Start a watcher in the background that exits on the event,
and act when it fires: `scripts/watch-run.sh <runId> <spaceId>` ends when a run is terminal
or paused; `scripts/watch-session.sh <sessionId> <spaceId>` ends when a conversation pauses
after having run. A watcher that expires on its own timer is not an event — re-arm it.

A run's tasks tell the story: `GET /v1/spaces/:spaceId/workflow-runs/:runId`, or the
`workflow_run_tasks` rows ordered by `started_at`. A `paused` run with `paused_reason`
`task_paused` is a gate; its `paused_payload_ref` holds the prompt and the allowed
resolutions.

## Gates

A gate is a question to a person. Read it before you touch it: the decision step's output
(`decide-push`, or the task the pause names) says why it asked, and the review's output
holds the verdict and the findings. Then:

- **Decline** when the run's own record says the premise is wrong — a review that did not
  return a verdict, a major finding the gate's reason does not mention, a receipt gone
  stale: `POST /v1/spaces/:spaceId/workflow-runs/:runId/resume` with
  `{ pauseVersion: <from the run>, resolution: { mode: "reject", comment: "<why, with the record>" } }`.
  Declining pushes nothing and wakes the conversation that owns the run with your reason.
- **Approve** is the operator's click. Give them the link to the session and what the
  record says, and stop.

## Judging an output

Read what the platform recorded, not what an agent said about it. A review's verdict and
findings are on the review task's `output_ref` (`verdict`, `findings[]` with `severity`,
`file`, `line`, `claim`, `evidence`). A commission's patch and summary are on its result. A
Helmsman's claim about a run ("the restart", "the flaky projection") is a hypothesis; the
run's tasks, the executor's log and the process table are the evidence. When they disagree,
correct the Helmsman with the record, and record the real cause where the next session
will read it (a plan node's note or learnings, or memory).

## Debugging a stuck run

`docs/dev/debugging-runs.md` is the full playbook. The cases that recur:

- **Nothing fires, schedules silent, runs frozen, `/health` ok** — the orchestrator is
  gone. Run `pgrep -f aflow-orchestrator`. The dev supervisor restarts it after a crash (a
  non-zero exit) within 2–30 s, but not after a SIGTERM, which ends it cleanly. A Postgres
  connection drop does not end it: it replaces its database client and reconnects on the
  next query. Restart the stack when nothing is mid-check.
- **Commissions return in seconds with an empty patch; reviews end without a verdict** —
  the coding provider's usage limit, shared by every harness on the machine. Wait for the
  window, then republish the branch as it stands.
- **A push refused for a "check receipt this executor did not issue"** — the host executor
  restarted between the check and the approval. Publish the branch again as it stands;
  the approval must be given again. Do not restart the stack while a gate waits on a person.
- **A session paused with an empty prompt** — a `human.chat.ask` that failed validation;
  answer the conversation directly with what it needed.
- **A check killed by an executor shutdown reads as failed** — it was interrupted; look at
  the executor's log around the time before believing the failure.
- **Two sessions publishing one branch at once** — the machine is overloaded and timing
  tests flake; let one finish.

## Keeping this skill honest

Facts here rot: route paths, the resume body shapes, table and column names, the MCP tool
list, the executor's failure texts. A change that moves one of them updates this file in
the same pull request (CLAUDE.md, "Documentation practices"). Nothing checks it; the next
session that follows a stale line is the check, so when a line here is wrong, fix the line
before you work around it. Machine-specific facts — paths, space ids, session ids,
branch names — do not belong here; they belong in the session's own notes.
