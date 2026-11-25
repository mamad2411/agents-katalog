---
name: ralph-loop
displayName: Run and supervise OpenCode task loops
description: Run and supervise bounded OpenCode loops for a user-defined task, including task contracts, verification, retries, progress monitoring, stall detection, and safe stopping. Use when the user asks OpenCode to keep working on a task until a stated outcome is verified. For GitHub issue queues, use ralph-loop-implement as the specialization.
version: 1.0.0
tags: [automation, opencode, unattended, monitoring]
---

# Ralph loop

A Ralph loop gives fresh OpenCode attempts the same task contract until the
outcome passes verification or the retry limit is reached. The loop is a
supervised executor, not permission to expand the user's task.

## Build the task contract

Before starting, turn the request into four concrete fields:

- **Goal:** the outcome OpenCode must produce.
- **Scope:** the files, systems, and side effects the user authorized.
- **Verification:** observable checks that distinguish done from incomplete.
- **Stop conditions:** success, the attempt limit, a confirmed stall, or a need
  for authority the user has not granted.

Use the repository's own instructions and test commands. Ask the user only when
a missing choice would materially change the outcome. Show the task contract
before launch. Starting the loop can modify files or external state, so start
only after the user has asked you to run it.

## Run attempts

Prefer one attempt for the first run. Default to at most two attempts unless the
user chooses another limit.

For each attempt:

1. Start a fresh `opencode run` process with the full task contract. Include
   facts from earlier failed attempts, but no transcript archaeology.
2. Capture the complete output in a per-attempt log and expose a stable
   `current.log` path for the active attempt.
3. When OpenCode exits, run the verification from outside the implementer.
4. Stop on success. On failure, make the next prompt name the failed check and
   the relevant output. Stop at the attempt limit and report the remaining gap.

Do not treat a zero exit code or OpenCode saying "done" as verification.

If a project already provides a Ralph runner, use its command, state, and log
paths instead of inventing a second loop around it. A specialization may define
how work is selected, verified, retried, and recorded.

For a task without a project runner, store the task contract in
`.ralph-task/task.md` and use this attempt shape. Increment `attempt` for each
retry.

```bash
mkdir -p .ralph-task/logs
attempt=1
log=".ralph-task/logs/attempt-${attempt}.log"
ln -sfn "logs/attempt-${attempt}.log" .ralph-task/current.log
timeout "${RALPH_RUN_TIMEOUT:-3600}" opencode run "$(cat .ralph-task/task.md)" 2>&1 | tee "$log"
rc=${PIPESTATUS[0]}
unlink .ralph-task/current.log
```

Run this in Bash so `PIPESTATUS` reports OpenCode's exit code rather than
`tee`'s. The supervisor owns task-file creation, verification, retry prompts,
and cleanup. A project runner may use different state paths.

## Place the long-running process

Choose one execution mode. Starting the same attempt in two modes runs it twice.

- When `${HERDR_ENV:-}` is `1`, run the attempt in its own Herdr pane.
- Otherwise, use the supervising harness's managed long-running shell session.
- In OpenCode without Herdr, there is no native persistent monitor for an
  arbitrary process. Use another terminal/process supervisor whose events stay
  visible to the operator. If none is available, tell the user the stall watch
  cannot be armed and ask where the process should live.

An OpenCode `task(background: true)` watches a child agent session, not an
arbitrary outer process. A detached `&` or `nohup` process is also not an armed
watch because later events do not reach the supervising agent.

Tell the user which mode you used. Keep the turn active until the loop ends.

## Arm the stall watch

Arm a second, push-visible watch in the same turn as the attempt. It must emit
events while the attempt is running and outlive the attempt timeout.

| Harness | Armed watch | Parked or unsupported |
|---|---|---|
| Claude Code | `Monitor(command: ..., persistent: true)` | `Bash(run_in_background: true)` |
| Codex | a managed shell session held by its session handle | detached `&` |
| OpenCode | Herdr or another visible external supervisor | `&`, `nohup`, or a background subagent |

Watch transcript progress, not process age. A live parent process or fresh
heartbeat can remain healthy-looking while the model stream is stuck.

```bash
prev=-1; flat=0
while true; do
  if [ ! -e .ralph-task/current.log ]; then
    echo "ENDED"
    break
  fi
  cur=$(wc -l < .ralph-task/current.log 2>/dev/null || echo 0)
  if [ "$cur" -eq "$prev" ]; then
    flat=$((flat+1))
    if [ "$flat" -eq 2 ]; then
      echo "STALL? transcript flat at ${cur} lines for ~4m | last: $(tail -c 220 .ralph-task/current.log 2>/dev/null | tr '\n' ' ')"
    elif [ "$flat" -eq 8 ]; then
      echo "STALL CONFIRMED flat at ${cur} lines for ~16m"
    fi
  else
    if [ "$flat" -ge 2 ]; then echo "recovered at ${cur} lines"; fi
    flat=0
  fi
  prev=$cur
  sleep 120
done
```

Adapt only the completion condition and transcript path to the runner. Relay
`STALL?`, `STALL CONFIRMED`, recovery, and `ENDED` events as they arrive. Two
flat checks are a warning. Eight are a confirmed stall. On confirmation, show
the transcript tail and ask before killing the attempt unless the user already
authorized automatic stall recovery.

## Use Herdr when available

Run the loop in one sibling pane and the watcher in another. Record every pane
and tab ID created for the run. Keep the caller's original IDs separate.

```bash
herdr pane split --current --direction right --cwd "$PWD" --no-focus
herdr pane run <loop-pane-id> "<loop-command>"
```

Herdr supplies visibility, not stall detection. A hung OpenCode process still
looks busy, so keep the transcript watch armed.

After `ENDED`, confirm the process exited, then close the watcher and loop panes
by their recorded IDs. Leave pre-existing panes and any active successor alone.

## Rotate between independent work items

For a batch with several independent items, give each item a fresh OpenCode
process. Under Herdr, rotate the supervising agent's tab between items when its
context has accumulated details that do not help with the next item. Rotate only
after the current item and its watcher have ended.

Brief the successor with the next task contract, completed work and verification,
branch and working-tree state, unpushed commits, environment constraints, known
bad data, and the predecessor tab ID. Start the successor before closing the
predecessor tab. The successor closes that recorded tab as its first action.

## Report the result

On success, report the attempts used, changed state, and verification. On stop,
report the last useful transcript output, failed verification, and whether any
partial changes remain. Never silently turn a bounded loop into an unlimited
retry cycle.
