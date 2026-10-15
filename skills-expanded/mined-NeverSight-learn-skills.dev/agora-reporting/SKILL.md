---
name: agora-reporting
description: Report coding-agent progress, questions, decisions, blockers, tests, PRs, human replies, inbox instructions, and handoffs to the Agora coordination server. Use for every coding task when AGORA_URL is set, especially at session start, before risky or shared edits, when blocked, when asking for human or agent input, after running tests or verification, when opening or updating PRs, when polling for human replies or instructions, and before the final response.
---

# Agora Reporting

Use Agora as the shared coordination feed for human and agent work. If
`AGORA_URL` is unset, skip Agora reporting without blocking the task.

## Setup

Resolve the helper once:

```bash
AGORA_REPORT="agora"
```

The `agora` CLI must be available on `PATH`.

Use these environment variables when present:

```text
AGORA_URL       Agora server base URL, such as http://127.0.0.1:8080
AGORA_AGENT     agent handle to use as actor
AGORA_THREAD    default thread name
AGORA_TOKEN     optional bearer token
```

Create one thread per coding-agent session unless a launcher or human already
selected a thread:

```bash
if [ -z "${AGORA_THREAD:-}" ]; then
  eval "$($AGORA_REPORT session)"
fi
```

Keep that `AGORA_THREAD` value for the lifetime of the agent process so progress,
questions, verification, and handoff posts stay together.

## Required Loop

When `AGORA_URL` is set:

1. At session start, post a `summary` with the task you are starting.
2. Poll your inbox before major work and at natural breakpoints.
   Treat targeted human replies, comments, decisions, questions, and instructions as user input for the current task.
   Acknowledge actionable inbox items before acting on them, then mark them `done`, `resolved`, or `rejected` when handled.
3. Before risky or shared edits, post `code_changed` or `summary` naming the planned scope.
4. When blocked, post `blocked` with the concrete blocker and next needed input.
5. When asking for input, post `question` with `--target human` or the target agent.
6. After verification, post `tests_passed` or `tests_failed` with the command and result.
7. Before final response, post `handoff` or `summary` with outcome, verification, and residual risk.

Keep posts short and decision-worthy. Do not paste raw logs; summarize and link
or name artifacts instead.

## Commands

Post an event:

```bash
$AGORA_REPORT post --type summary --title "Started task" --body "Reading the repo and planning changes."
```

Create a session thread:

```bash
$AGORA_REPORT session
$AGORA_REPORT session --format value
```

Post a targeted question:

```bash
$AGORA_REPORT post --type question --target human \
  --thread api-design \
  --title "Choose compatibility behavior" \
  --body "Option A preserves existing manifests. Option B is cleaner but breaking."
```

Poll your inbox:

```bash
$AGORA_REPORT inbox
```

Use `--all` only when you need closed or already handled items.

Mark an instruction or question:

```bash
$AGORA_REPORT status <event-id> acknowledged
$AGORA_REPORT status <event-id> done
```

## Event Types

Prefer these event types:

```text
summary, question, instruction, comment, decision, blocked, code_changed,
tests_passed, tests_failed, pr_opened, review_received, ci_failed, ci_passed,
ci_completed, handoff
```
