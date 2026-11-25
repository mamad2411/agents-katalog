---
name: metrics
description: |
  Flow metrics and analysis for Infiquetra project boards using GitHub timeline events.
  Provides cycle time, throughput, WIP age, per-status time breakdowns, and interpretation
  guidance across Operations, Asgard, and CAMPPS.
when_to_use: |
  Use this skill when the user wants to:

  Cycle time analysis:
  - "how long are issues taking", "what's our cycle time", "how fast are we delivering"
  - "cycle time report", "are we hitting our cycle time targets"
  - "how long did this capability take", "how long has issue #42 been active"

  Throughput analysis:
  - "how many capabilities did we complete last week", "weekly delivery rate"
  - "throughput this month", "how many items reached Ready to close"

  WIP age and aging work:
  - "how old are our active items", "what's stale", "aging work items"

  Flow health:
  - "how's our flow", "where's the bottleneck", "which status is slowest"
---

# SDLC Metrics

Flow metrics for Infiquetra's GitHub Projects boards. Metrics use GitHub timeline events
for Status changes. Deployment state is intentionally separate from workflow Status; use
deployment records and deployment fields for environment promotion questions.

## Script Location

```bash
$INFIQUETRA_SDLC_PATH/../infiquetra-claude-plugins/plugins/mission-control/scripts/sdlc_manager.py
```

If `$INFIQUETRA_SDLC_PATH` is unset, use `~/workspace/infiquetra/infiquetra-sdlc` as the default base path.
Always run the script with `python3`.

## Metric Boundaries

| Board | Active start | Terminal status |
|-------|--------------|-----------------|
| Operations / Asgard / CAMPPS | `Active` stage | `Ready to close` |

> **How the start boundary is actually detected.** `_cycle_start_statuses` in
> `scripts/sdlc_manager.py` returns the literal option name `Active`, and the
> timeline query it feeds (`QUERY_GET_ISSUE_TIMELINE`) captures only the option
> *name* of a single-select change — it records no field name or id, so it cannot
> tell a `Stage` change from a `Status` change. `Active` is a live `Stage` option
> on all three boards and is not a `Status` option at all, so the start boundary is
> whichever field first carried an option named `Active`. That is close to the
> boundary this table declares, but it is matched by name rather than by field.
> Making the field explicit is outside issue #1020, whose scope is the cached
> census and the prose describing it.


Legacy (read-only history): the retired `Mount Olympus` board used its own active-start status
with `Done`/`Closed`/`Cancelled` terminals, and its timeline may include `In Progress`,
`In Development`, or `Deployed`. The CLI reads those values for historical continuity only;
new cards use the active boards above.

## Core Operations

### Cycle Time

```bash
python3 sdlc_manager.py metrics cycle-time --project campps
python3 sdlc_manager.py metrics cycle-time --project asgard --days 14
python3 sdlc_manager.py metrics cycle-time --project campps --type capability
```

Cycle time is calculated from the first active-start status to a terminal status.

### Throughput

```bash
python3 sdlc_manager.py metrics throughput --project campps
python3 sdlc_manager.py metrics throughput --project asgard --weeks 8
```

Throughput counts items that reached a terminal workflow status during the reporting window.

### WIP Age

```bash
python3 sdlc_manager.py metrics wip-age --project campps
python3 sdlc_manager.py metrics wip-age --project operations
```

WIP age shows current items in active statuses and flags entries over the configured thresholds.

### Per-Status Time Breakdown

```bash
python3 sdlc_manager.py metrics column-time --project campps --number 42
```

Use this to diagnose where one card spent time.

## Targets

### Cycle Time Targets (P85)

| Issue Type | P85 Target | Notes |
|------------|------------|-------|
| Capability | < 5 days | Active ownership through terminal status |
| Enhancement | < 2 days | Smaller scope |
| Defect | < 1 day | Highest urgency |
| Exploration | < 3 days | Timeboxed research |
| Context Update | < 1 day | Documentation or context maintenance |

### WIP Age Thresholds

| Board | Status | Flag if age > |
|-------|--------|---------------|
| Operations / Asgard / CAMPPS | every non-terminal Status | 3 days |

One threshold, every board, every Status that is not terminal. This is what
`_active_age_thresholds` in `scripts/sdlc_manager.py` computes: the stage-flow
statuses minus the terminal ones, each at three days. There is no per-board
split and no longer threshold for any board.

## Natural Language Examples

**"What's our cycle time for capabilities this month?"**
-> `metrics cycle-time --project campps --type capability --days 30`

**"How many items did Asgard complete recently?"**
-> `metrics throughput --project asgard --weeks 4`

**"How old are our active items?"**
-> `metrics wip-age --project campps`

**"How long has issue #42 been active?"**
-> `metrics column-time --project campps --number 42`

## Interpreting Results

### When Cycle Time Is Over Target

1. Run `metrics column-time` on slow items to find the status consuming the most time.
2. Check WIP age for active or review bottlenecks.
3. Look for `blocked` or `Needs clarification` state.
4. Check how many cards sit in the `Active` stage at once; no limit is enforced, so a
   pile-up there is a judgement call, not a gate.
5. Separate deployment delay from work status; deployment evidence belongs to deployment fields.

### When Throughput Is Low

1. Check how much work sits in the `Active` stage at once.
2. Look for aging items that are not moving to review or verification.
3. Check whether `Ready for Planning` is empty or poorly shaped.
4. Confirm the board is the right one: raw intent should not be counted as initiative execution.

### When WIP Age Is High

1. Identify the specific cards and ask what decision, context, or reviewer is missing.
2. Move truly blocked cards to the right pause state.
3. Swarm or split work that is too large.

## Reference Documents

- `references/metrics-targets.md` - Complete targets, definitions, and interpretation guide
- `skills/board/references/kanban-workflow.md` - Board workflow, stages, and statuses
