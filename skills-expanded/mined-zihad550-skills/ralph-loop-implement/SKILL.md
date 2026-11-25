---
name: ralph-loop-implement
displayName: Drain a GitHub issue queue with Ralph
description: Run and supervise the Ralph GitHub issue-queue specialization, which sends ready and unblocked issues to OpenCode's implement-issue command, verifies closure, and parks failed issues. Use for starting, stopping, checking, or diagnosing the repository's ralph issue loop. For arbitrary user-defined tasks, use ralph-loop.
version: 2.0.0
tags: [github, issues, automation, opencode, unattended]
---

# Ralph issue loop

Read and apply [`ralph-loop`](../ralph-loop/SKILL.md) first. It owns task-loop
supervision, process placement, transcript stall detection, bounded retries,
Herdr cleanup, and reporting. This skill defines only the GitHub issue-queue
specialization.

The repository's `ralph` command selects the lowest-numbered open issue with the
agent-ready label and zero open blockers. It passes that issue to a fresh
`opencode run` process with `/implement-issue`, then checks whether the issue
closed. The existing runner is the loop. Start it directly rather than wrapping
it in another generic loop.

Ralph can change code, commit, and close issues. Start it only when the user asks
to work the queue.

## Preflight the queue

```bash
ralph --check
```

Read the exact frontier back to the user. Stop before launch when it is empty.
Do not relabel or reprioritize issues to fill it.

Check these queue-specific risks:

- Compare suspicious issue titles with git history. A stale open issue consumes
  an attempt even when its work already shipped.
- Flag a dirty working tree. An implementer commit may include unrelated staged
  work, so offer to commit or stash it first.
- Check `.ralph.env` when the repository needs nonstandard verification. The
  available settings live in `ralph.env.example`.

Preflight is complete when the user has seen the frontier and any dirty-tree or
stale-issue risk.

## Start Ralph

```bash
ralph --once       # one issue, preferred for the first run
ralph              # drain the frontier
```

Use the execution-mode rules from `ralph-loop`. Under Herdr, the loop command
belongs in its own pane. In other managed harnesses, run it as the long-running
call. Start exactly one copy per checkout.

Arm the base skill's stall watch with these Ralph paths and completion check:

```bash
cd /path/to/repo
prev=-1; flat=0
while true; do
  st=$(jq -r '.status // "unknown"' .ralph/state.json 2>/dev/null || echo unknown)
  if [ "$st" != "running" ]; then
    echo "ENDED status=$st done=$(jq -c '.done' .ralph/state.json 2>/dev/null) parked=$(jq -c '.parked' .ralph/state.json 2>/dev/null)"
    tail -n 3 .ralph/ralph.log 2>/dev/null
    break
  fi
  cur=$(wc -l < .ralph/current.log 2>/dev/null || echo 0)
  if [ "$cur" -eq "$prev" ]; then
    flat=$((flat+1))
    if [ "$flat" -eq 2 ]; then
      echo "STALL? transcript flat at ${cur} lines for ~4m | last: $(tail -c 220 .ralph/current.log 2>/dev/null | tr '\n' ' ')"
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

Keep the watch alive across every issue in a draining run. Ralph's default
`RALPH_RUN_TIMEOUT` is 3600 seconds, so a one-hour watch expires too early for a
second issue.

## Read Ralph state

```bash
ralph --status         # state, timeline, heartbeat, and 40 transcript lines
ralph --status 100     # deeper transcript tail
```

| Path | Meaning |
|---|---|
| `.ralph/state.json` | status, current issue and attempt, `done`, `parked`, frontier |
| `.ralph/ralph.log` | append-only queue timeline |
| `.ralph/heartbeat` | Ralph liveness plus transcript `lines=` count |
| `.ralph/current.log` | symlink to the active attempt transcript |
| `.ralph/logs/` | complete transcript for every attempt |

Interpret queue outcomes as follows:

- A growing `lines=` count means OpenCode is progressing.
- `parked: #N` means the issue remained open after
  `RALPH_MAX_ATTEMPTS`. Read its attempt logs and issue comments.
- A growing `done` list with a dirty tree means an issue closed while changes
  remain uncommitted. Flag the partial state.
- `rc=124` plus a transcript that was silent for most of the timeout means a
  hang. Output written until the timeout means the attempt was genuinely slow.
  Recommend a larger timeout only for the second case.

## Queue concurrency

Ralph enforces one loop per checkout with `.ralph/lock.d`. If it reports
`already running`, inspect `ralph --status`; the runner clears dead-process locks
itself.

Separate checkouts may run independently. For parallel workers on one
repository, use one worktree per worker and enable claiming:

```bash
git worktree add ../repo-b -b ralph-b
RALPH_CLAIM=1 ralph
```

Claiming assigns an issue before work and drops assigned issues from other
workers' frontiers. A failed attempt releases the issue. A parked issue keeps
its assignee. Single loops do not need claiming.

Coordinate shared resources such as development-server ports across worktrees.

## Stop and boundaries

Use `Ctrl-C` or signal the PID recorded in `state.json`. Ralph records
`status: interrupted` and retains its state.

The issue specialization has these fixed boundaries:

- It uses at most `RALPH_MAX_ATTEMPTS`, then parks the issue and continues.
- It commits on the current branch. It does not push, create a PR, or create a
  branch.
- It reads labels, priority, and GitHub's native blocker relationships. It does
  not change queue ordering.
- It supports GitHub. Another tracker needs a different frontier adapter.
