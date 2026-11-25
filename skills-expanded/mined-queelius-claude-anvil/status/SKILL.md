---
name: status
description: >-
  Show the current state of a research-agent run from .research/: liveness,
  cycles and budget, sub-problem and hypothesis statuses, eval trend, current
  focus, and branches. Read-only.
---

# Research Status

Show the current state of a research-agent run. Read-only: this skill never modifies `.research/` or relaunches the agent.

## Step 1: Locate the Run

`.research/goal.md` marks a research run (Glob tool). If absent, tell the user there is no research run here and suggest `/research-agent:research`.

## Step 2: Read the Structured Files

Read (Read tool), degrading gracefully on partial runs:

1. `.research/goal.md`: the goal is the body; the frontmatter `eval` is the eval script (null means self-evaluation).
2. `.research/run.json`: `status`, `heartbeat`, `stale_after_minutes`, `launched`, `budget`, `policy`. The run is **live** when `status` is `running` or `stopping` and the heartbeat is less than `stale_after_minutes` old (compare against `date -u +%Y-%m-%dT%H:%M:%SZ`). `running` with a stale heartbeat means the agent is gone: the run was interrupted.
3. `.research/state.md` YAML frontmatter: `cycle`, `current_focus`, and the `subproblems` / `hypotheses` lists (count by `status`).
4. `.research/cycles.jsonl`: one record per cycle; the last 5 give recent activity.
5. `.research/scores.jsonl`: one record per eval run; the source of the eval trend.

**Legacy fallback** (a run from an older plugin version: no run.json, state.md without frontmatter, or no cycles.jsonl): take counts from the prose `- status:` lines of state.md, cycles from the `### Cycle N` entries of log.md (`tail -200 .research/log.md` for long logs), report liveness as "unknown (legacy run)", and use the default policy (pivot after 3, conclude after 5). When state.md is missing, report "initialized, no cycles yet" and skip the sub-problem and hypothesis sections.

## Step 3: Inventory Artifacts

Use Glob to count:

- `attempts/*/notes.md`: total attempts; list the most recent 3 with their slugs and the first line of their notes
- `findings/*`: confirmed results promoted out of attempts/
- `synthesis.md`: present means the run (or branch) has concluded; note this prominently
- `branches/*/`: for each branch, read the same structured files under its run root (run.json liveness and worktree, state.md `cycle` and `current_focus`, synthesis.md presence)

## Step 4: Format the Report

```markdown
# Research Status: {one-line goal}

## Goal
{goal body, trimmed if very long}

## Run state
- Status: running (heartbeat {M} min ago) | stopping (stop requested) | interrupted (stale heartbeat) | concluded
- Cycles: {cycle} / {budget.max_cycles or "unbounded"}
- Elapsed this launch: {hours} / {budget.max_hours or "unbounded"}
- Current focus: {current_focus.id}: {its text} ({current_focus.why})
- Eval: {eval path or "self-evaluation"}

## Sub-problems
| Status | Count |
|--------|-------|
| open | N |
| in-progress | N |
| resolved | N |
| abandoned | N |
| unresolved (terminal) | N |

## Hypotheses
| Status | Count |
|--------|-------|
| untested | N |
| confirmed | N |
| refuted | N |
| inconclusive | N |

## Recent activity
- {ts} Cycle N: {hypothesis id} via {modality} -> {result}, then {decision}
- ... (last 5 cycles)

## Eval trend
- Latest score: X (or "self-evaluation")
- Best score: Y
- Trend over last 5 eval runs: improving | flat | declining

## Branches
- {name}: {status}, {cycle} cycles, focus: {current focus}, worktree: {path or "none"}, concluded: yes|no
- (omit this section when no branches exist)

## Attempts inventory
- {N} attempts total
- {M} findings promoted
- Most recent attempts:
  - attempts/{NNN}-{slug}: {one-line note}
```

## Step 5: Suggest Next Actions

- Concluded (`synthesis.md` present): point the user to `.research/synthesis.md`
- Live and progressing: nothing to do; check back later, or `/research-agent:synthesize` to wrap up early
- Interrupted (stale heartbeat, or a legacy run whose session ended): suggest `/research-agent:resume`
- Stalled (the last `policy.conclude_after` cycles in cycles.jsonl have no `pass` result, or the eval trend is flat or declining): suggest `/research-agent:synthesize` to lock in current results, or `/research-agent:branch` to try a competing strategy
- Fewer than 3 cycles: note that it is too early to judge the trend
