---
name: jev-model-router
description: Use before delegating a substantial task to a subagent or a separate `codex exec` run (implementing, fixing, reviewing, planning), to ask jev-model-router which model and reasoning effort should do it, and after the work has been checked, to report whether it passed. Skip it for quick lookups and for work you do yourself in this turn.
---

# Routing delegated work through jev-model-router

jev-model-router estimates, per task, the cheapest model and effort likely to succeed, and learns
from what you report back. It never runs anything itself: you ask, you run, you report.

The `jev-model-router` MCP server gives you two tools.

## 1. Before you delegate: `route`

Call `route` with the task written as you would brief the agent that does it. Add what you
know: `stage` (plan, implement, review...), `files`, and on a retry `attempt`, `gate_output`
(the tail of the failing test or review) and `failed` (the model or `model@effort` that
failed it, as the previous `route` returned it).

When the user has said which models may do the work (or may not), pass it on every
`route` call as `models` / `exclude`: globs over model ids and tier names, such as
`["anthropic/*", "*gpt-6*"]`. The router only chooses among what they leave.

The answer has `model`, `effort`, `runner`, `success` (the router's estimate) and a
`decision_id`. Keep the `decision_id`. If it has a `why`, the router fell back to its
default (for instance the judge could not be reached): mention it to the user.

If `route` fails with HTTP 503 `jev_unavailable`, the router is set to refuse when its judge
cannot be reached: tell the user, and use the default model rather than guessing one.

`estimated_cost_usd` compares the tiers with each other; it is not a budget for the task.
`cost_basis` says whether it priced the whole task by its cache-aware shape (`task_shape`)
or as one call (`one_call`).
If it has `unsure`, the judge could not tell whether the task needs the requirements it
names, and the router held the choice to a model rated good at them (`raised_from` is what
it would have picked otherwise). Follow the choice as usual; there is nothing to report.

## 2. Run it on what was chosen

The answer's `run` says how.

- `run: "subagent"`: delegating to a subagent that takes a model and reasoning effort: give it the
  returned `model` and `effort` as they are. Otherwise, for a self-contained task, run it from the
  repository root:

  ```bash
  codex exec -m <model> -c model_reasoning_effort="<effort>" "<the brief>"
  ```

  Leave out the `-c` when `effort` is null.
- `run: "delegate"`: the tier runs on another agent's CLI, on that agent's subscription.
  1. Write the brief to a file, as you would brief a subagent: it starts with none of your context.
  2. Run `command_line` followed by ` --brief-file '<that file>'` in the shell with
     `sandbox_permissions: "require_escalated"`: it needs the network and writes the router's log.
     Give the call a `timeout_ms` long enough for the task (30 minutes: `1800000`).
  3. It may edit files and run commands in this project (`workspace-write`). Add
     `--access read-only` for a review or an investigation. Add `--access full` only when the user
     asked for it.
  4. stdout is the other agent's final message: check its work as you would a subagent's.
     Exit 0: report `pass` or `fail` from your check. Exit 3: it hit a rate limit and already
     reported `rate_limited`; do not report again, route again. Exit 2 or 4: report `error` with
     the reason it printed on stderr. Its tokens are already logged: leave `usage` out.
- `run: "unavailable"`: this session cannot run that tier. Use the default and report `error` with
  that reason.

`delegate` answers appear only when the user turned delegation on (`JEV_MODEL_ROUTER_DELEGATE=1`).

## 3. After the work is checked: `report_outcome`

Once the task's own check has run (tests, build, your review of the result), report it once
with the `decision_id`:

- `pass` / `fail`: what the check said. This is the label the router learns from, so report
  what the check said, not how the work looked.
- `rate_limited`: the model refused for quota or rate limits.
- `error`: the run broke for a reason that says nothing about the model (tool crash,
  interruption, the choice could not be followed).

If you know the run's tokens, pass `usage`: `prompt_tokens` and `completion_tokens`, and
`cached_tokens` and `cache_write_tokens` when the runner reports them. They tell the router
how much of a task's input its cache served. Most runs will not know them: leave out what
you do not know rather than guessing.
`prompt_tokens` is the whole input with cached and cache-write tokens included; if the
runner reports fresh input separately from cache reads/writes, add them together.

On `fail`, route the retry with `attempt`, `gate_output` and `failed` filled in: the router
never offers a choice it rates below the one that failed.

## If the tools fail

If the jev-model-router tools are missing, the server did not start, usually because it found no
config: the user must set `JEV_MODEL_ROUTER_CONFIG` to their jev-model-router config file (see the
project README, "Use it from Claude Code or Codex"). Carry on with the default model; do not
block the task on routing.
