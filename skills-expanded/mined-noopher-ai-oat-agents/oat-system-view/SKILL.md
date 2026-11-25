---
name: oat-system-view
description: Read the whole fleet's state from the workflow log, the store, and each session's liveness, and tell a stuck Run from a slow one. Use before reporting on any Run you are not the meta-agent of.
---

# Oat System View

## The read-only accessors, and what each one answers

- `oat-agents log runs --repo REPO` — which Runs belong to this repository, and whether each is
  still open. Always pass `--repo` from a console; without it, a Run outside this repository can
  show up in the answer.
- `oat-agents log show --run R --format json` — the full chronology: launches, exits, inbox
  deliveries, decisions, review verdicts. `--agent`, `--event`, `--since`, and `--limit` narrow
  it. **This is where you read what the inbox carried**, instead of touching the inbox.
- `oat-agents log agents --run R` — one row per agent that has appeared in the Run's log.
- `oat-agents goal show --run R` — the exact text the Run was fired with. When a Run's work
  looks wrong, check it against what was actually asked before concluding anything.
- `oat-agents checklist show --run R` — the Run's checklist, which items are checked, and
  under `progress` where the Dispatches linked to each item stand (`active`, `queued`,
  `ended`, or `no_dispatch`).
- `oat-agents dispatch show --dispatch D --run R` — the store's record of one Dispatch plus
  whether its session is still alive.
- `oat-agents dispatch read --dispatch D --run R --source auto --limit 50` — the text on an
  agent's terminal. The last resort: it is long and unstructured. Exhaust the log first.

## Where a Run's commands run

Every Run records, when it is fired, whether its roles get execution environments (pods) and
why: an `exec_profile_selected` event names the profile; an `exec_profile_none` event says there
is none, and its `warning` names the roles that asked for one and will run on the host instead.
Every role launched without the environment it asked for adds an `env_skipped` event for its
Dispatch. Read them with `oat-agents log show --run R --event exec_profile_none` (or
`exec_profile_selected`, `env_skipped`), and read the environments themselves with:

- `oat-agents dispatch show --dispatch D --run R` — `env_id` and `image_id` when the Dispatch
  got a pod, `env_skipped` when it asked for one and ran on the host.
- `oat-agents env status` — every registered environment: its pod, namespace, image and run.
- `oat-agents env evidence --worktree PATH` — which commands already ran against the code as it
  stands, and in which image.

A role that asked for a pod and ran on the host is worth telling the operator about: its
verification ran somewhere nothing recorded, so a report that cites it proves less than it
seems to.

## Telling a stuck Run from a slow one

A `run wait` that times out returns a liveness report for every still-active Dispatch. Two
states matter:

**`stalled`.** Neither the agent nor its session has written anything. That is an agent that
stopped taking turns, not a slow one — no delivery is coming to restart it on its own. Confirm
it on a second observation before saying so.

**`waiting`.** The agent is silent but its session is not, so it is blocked on something.
`outstanding` names what, when the backend's transcript exposes it. A silence that has
outlasted the kind of work it is doing is worth a look, but is not on its own a verdict that
anything is wrong — a long-running command and one that will never return look identical until
you read what it actually is.

A `needs-human` event marks an open question with no answer yet; it stays open until a matching
`answered` event retires it. This is the cheapest kind to miss and the most expensive to leave
open: nothing times out on its own, and the Run can sit there indefinitely. Read the timestamp
of the last `needs-human` event before deciding whether it is still fresh.

## Things that look like problems and are not

- A Run with no active Dispatches and no `run_closed` entry is usually finished but not yet
  cleaned up, not stuck.
- A Run whose last event is an `inbox_timeout` is at a checkpoint, which is what the timeout is
  for, not a failure.

## What you must never run

Each of these takes something from a Run that it cannot get back:

- `run wait`, `run ack`, `run reply` — a Run's inbox is delivered once, to its own meta-agent.
  Consuming a delivery leaves that meta-agent waiting forever for a message it will never be
  told about. There is no recovery. Read the log instead.
- `dispatch release` — ends someone's terminal; with `--remove-worktree` it deletes the only
  copy of their work.
- Firing any role into a Run you do not own — that Run's meta-agent can neither read nor settle
  an agent it did not launch.
