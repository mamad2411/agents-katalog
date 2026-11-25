---
name: scheduler
description: Create and manage cron-driven prompt tasks for a project. Use when the user wants something to run later or on a recurring schedule, or to inspect why a scheduled task did not run.
license: AGPL-3.0
---

# Scheduled Tasks

A schedule task is a stored prompt plus a time rule. Tasks live in the global
registry `~/.agents/cron/tasks.json`, each bound to the project it was created
in (`projectDir`); run records and Task Sessions stay in that project's
`.agents/cron/`. Each run opens its own isolated Pi Task Session. Execution is
owned by an external scheduler that invokes `agents-cron run-due`, so Pi never
runs tasks in the background by itself. Mention the cron entry when the user
expects unattended runs.

**Not a task.** A standing, message-driven role — serve this inbox, judge what
arrives, keep watching until I say stop — has no time rule that could express
it. That is a pod, and agents-pod owns it: `spawn_pod`, woken by its admission
owner — `intake` when a Listener or inbox feeds it, `external` for an outside
wake, `self` for a goal that reaches done — and never by the clock. Use a task
only when the trigger is a time; when an ask carries both signals, the two axes
below decide which unit owns which half (agents-pod ADR 0005, amended by ADR
0033: the cron side owns when work starts, the pod side owns keeping it alive).

## Install

The CLI is the npm package `agents-cron` and needs Node `>= 22.19`:
`npm install -g agents-cron`. In Pi, install the whole package instead —
extension, tool, and this skill — with `pi install npm:agents-cron`.

## Drive the store

In Pi, use the `schedule_task` tool or the `/loop`, `/remind`, and `/schedule`
commands. The tool is exposed with `deferred` exposure: it is not declared to
the model up front, so find it with `tool_search` (for example
`tool_search("schedule task")`) before the first call; the extension already
keeps `tool_search` active for this.

In any other harness, shell out to the CLI, which reads and writes the same
store with the same rules:

```bash
agents-cron list [--limit <n>] [--json]  # bare `agents-cron` does the same: this project first, then others
agents-cron show <taskId> [--json]       # one task in full, prompt included
agents-cron runs <taskId> [--limit <n>]  # its run history, newest first — why it failed
agents-cron add --prompt "<text>" (--at <iso> | --every <duration> | --cron "<expr>") [options]
agents-cron set <taskId> [options]       # reconfigure: --model --thinking --agent --cwd --tools --name --notify
agents-cron enable <taskId> | disable <taskId> | remove <taskId>
agents-cron clear                         # remove every task bound to the current project
agents-cron export [--out <file>] [--all] [taskId...]   # definitions as JSON; import starts disabled
agents-cron import <file> [--dry-run]
agents-cron run <taskId>                  # run it now, without disturbing the schedule
agents-cron run-due [--all]                # what cron calls; executes whatever is due
agents-cron prune [--keep <n>]            # all projects unless --project; default keep 20
agents-cron dashboard [--port <n>]
agents-cron dashboard start|stop|status   # detached: survives Pi, stop reclaims it
agents-cron test-notify [--channel <id>]
```

The CLI answers machine-readably: bare invocation prints the task list, each
mutation ends with a `next: agents-cron …` line, truncation is stated with the
true total, empty results exit `0` with a plain sentence, and anything
unparseable is refused — `error: <code>: <message>` on stderr, exit `2` for
bad input, `3` for a broken environment, `1` for a failed run. Read `--json`
when you need the record rather than the line.

Every surface — this CLI, the `schedule_task` tool, the `/schedule` commands,
and the dashboard — prints a task and a run through one shared formatter, so
the same task reads identically wherever you look: an interval is `every 30m`
(never `every 1800000ms`), a timestamp is compact ISO (`2026-09-01T10:00:00Z`,
or `never`), and a task line ends with its latest outcome (`never run`, or
`last error at …`). Do not reformat those fields in your own prose; quote the
line. Two locks are two words: `lock_busy` is another instance executing in
this directory (normal; `run-due` skips and exits `0`), and
`registry_lock_busy` is a refused write to the machine-wide registry (exit
`3`, nothing saved).

IDs resolve across the whole registry, so these commands manage any task from
any directory. One global crontab line (`agents-cron run-due --all`) drives
every project; a per-project line still runs only that project.

A task's model is configurable per task: pin `--model <id>` and `--thinking
<level>` (off, minimal, low, medium, high, xhigh, max) on `add`, or change
them later with `set` — an empty value (`--model=`) clears the override back
to the project and user defaults. In Pi, the same fields are trailing flags
on `/loop`, `/remind`, and `/schedule add`, or `/schedule set <id>` flags
afterwards (a value of `-` clears).

The dashboard is a read-only local web view (`127.0.0.1:7383` by default) of
tasks, run history, and per-run summaries, errors, and session records — the
quickest way to see why a task did not run.

Runs can also push notifications through `.agents/cron/config.json` channels —
SMTP email (QQ/Foxmail-style), webhook (including the Feishu group-bot format
`"format": "feishu"`; the bot's keyword must be `task`, and signature
security is not supported), and `system` desktop notifications (macOS
Notification Center via osascript, Linux via notify-send — zero setup, ideal
for local-only reminders) — error-only by default, and a task may override
the level (`--notify always`) and route itself to specific channels
(`--to feishu` in Pi, `--notify-to feishu,mail` on the CLI). A project may
also set a default route: `"defaultTo": ["feishu"]` applies to every task
that names no channels of its own. First-time setup is guided: run
`agents-cron setup-notify` with the user; it opens the mail and Feishu
consoles, captures the SMTP 授权码 and webhook URL, writes config.json plus
`.agents/cron/notify.env` (secrets never enter config.json), wires the shell,
and live-tests each channel. Verify an existing setup with
`agents-cron test-notify`. Channels are never forced: a run worth announcing
with none configured only gets a one-line stderr reminder (in the cron log).

When the user wants to perceive a task's output, resolve its notification
before creating it: read the task project's `.agents/cron/config.json`; if
`notifications.defaultTo` names channels, route to them without asking; if
channels exist but no default does, ask which ones (list their ids); if there
are no channels yet, offer `agents-cron setup-notify` or a `system` channel.
Tasks created so the user can see the result should carry `--notify always`
(reminders included — the default level announces only failures). Confirm the
chosen routing back to the user with the task id and next run time.

If `agents-cron` is not on `PATH`, call the installed binary directly:
`"$HOME/.pi/agent/npm/node_modules/.bin/agents-cron"` for a global install or
`.pi/npm/node_modules/.bin/agents-cron` for a project install.

## When the work belongs to a pod

Some asks carry two signals at once, and a schedule is only half of the answer:

> 「每天早上 9:00 汇总 GitHub CI 失败，产出一份报告，直到我明确说停」

`每天 9:00` is a time rule (yours); `直到我说停` is a role that must stay alive
(`spawn_pod`, agents-pod). Read two axes before creating anything —
**trigger** (`time` · `message` · `role alive`) × **work** (`stateless per
firing` · `needs memory across firings`) — and only three shapes come out:

| axes | shape |
| --- | --- |
| time + stateless | this skill alone: one task whose prompt does the work and keeps nothing |
| time + memory | the task owns the clock and **hands over** to a pod (`spawn_pod`): its prompt appends one Inbox Item to the inbox the pod's Listener watches (bind it with `agents-pod listener add --inbox <file> --pod <podId>`; the pod's admission is `intake`), or calls `agents-pod wake <podId>` when no input batch has to be queued (`admission: external`). The work lives in the pod, never in the task's prompt |
| message / role alive | not a task: that is `spawn_pod` in agents-pod — `intake` when a Listener or inbox feeds it, `self` only for a goal that reaches done |

Hand over as an Inbox Item when a per-firing input has to be queued — the batch
is ordered and the pod owes exactly one wake-up per batch; use `agents-pod wake`
when nothing has to be queued (the pod still keeps its own memory across
firings). State the split in one line, naming every unit the ask has and the
pod's admission (`intake` or `external`), before the first tool call. Never
write the role into the task prompt (a task ends; a role does not), and never
put a time rule inside the pod's goal: agents-pod's spawn refuses a recognised
clock phrase (09:00, 每天, 每 30 分钟, 9 点, every 30 minutes, daily) when the
pod's admission is `self` or unstated, and a pod re-armed by a clock is the wake
storm this split exists to prevent (agents-pod ADR 0030, ADR 0033).

## Agents

Tasks run through an agent adapter: `pi` (default), `claude` (Claude Code,
driven headless via `claude --print`), or `codex` (driven headless via
`codex exec`). Pin one per task with `--agent` on `add`,
`run`, and `run-due`, or the task's `agent` field in the registry. A Claude Code run
needs the `claude` CLI on `PATH` (`AGENTS_CRON_CLAUDE_BIN` under cron) and
treats the task's `tools` list as an allowlist, because headless runs cannot
approve permission prompts. A Codex run needs the `codex` CLI on `PATH`
(`AGENTS_CRON_CODEX_BIN` under cron); its sandbox depends on the task's
`tools`: none runs read-only, any runs workspace-write. `thinking` is ignored
on both.

## Rules

- Use `once` with an ISO timestamp, `interval` with a duration of at least 1
  minute such as `30m`, or `cron` with a 5- or 6-field expression or a nickname
  (`@daily`, `@hourly`, `@weekly`, `@monthly`, `@yearly`, `@annually`).
- `/loop` and `/schedule add` accept a duration, a nickname, or a quoted cron
  expression (quote it whenever it contains spaces).
- Deleting and clearing tasks requires interactive confirmation in Pi; creating
  a task does not.
- Resolve notifications when creating a task the user wants to hear about:
  apply `notifications.defaultTo` if set, else ask from the configured
  channels, else offer `setup-notify` or a `system` channel; add
  `--notify always --to <ids>` (Pi) or `--notify always --notify-to <ids>`
  (CLI) to the created task.
- Tasks contain prompts for Pi; they never contain arbitrary shell commands.
- Do not create duplicate tasks when an existing task already represents the
  same request.
- Ask the user to clarify any missing or ambiguous timing; never guess a
  schedule.
- Explain the task ID and next run time after creating a task.
- A Task Session is separate from this session and its results are never
  injected here. Inspect them with the `runs` action or `agents-cron list`,
  read a task's prompt with the `show` action or `agents-cron show <id>`, and
  tell the user they can open one with `pi --session <path>`.
