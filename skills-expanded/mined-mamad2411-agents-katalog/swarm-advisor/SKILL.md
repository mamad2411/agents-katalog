---
name: swarm-advisor
description: "Advises on multi-agent swarm design using Claude Code's TeammateTool and Task system. Use when the user wants to parallelize work across agents, asks 'should I use a swarm for this?', wants help designing team topology, needs to break a task into parallel workstreams, or is getting started with swarm-orchestration. Assesses whether a swarm is worth the overhead, recommends team size and structure, helps decompose tasks with correct dependencies, and tracks swarm health. Complements the swarm-orchestration skill by adding the 'think before you spawn' layer."
---

# Swarm Advisor

The `swarm-orchestration` skill contains the full technical primitives (Team, Teammate, Task, Inbox, Message). This skill adds the **design layer** — when to use a swarm, how to structure it, and how to avoid common traps.

---

## Is a Swarm Worth It?

Ask first. Swarms have real overhead: spawn cost, coordination messages, inbox polling, cleanup.

**Good fit:**
- 3+ independent workstreams that can run in parallel
- Work that naturally divides: research/implement/test, feature-A/feature-B/feature-C
- Long-running tasks where parallelism saves real time
- Pipeline patterns where stage N feeds stage N+1 with clear handoffs

**Not worth it:**
- Single sequential task → just do it inline
- 2 tasks → use two `Task()` calls without a full team
- Tight interdependencies where agents constantly block each other
- Tasks requiring human judgment mid-way → use GSD interactive mode instead

---

## Team Topology Patterns

### Pattern 1: Parallel Workers (most common)
```
Leader
├── Worker A (area: auth)
├── Worker B (area: API)
└── Worker C (area: tests)
```
Use when: Independent features/modules, parallel research, parallel code review.

### Pattern 2: Pipeline
```
Leader → Researcher → Synthesizer → Implementer → Verifier
```
Use when: Each stage's output feeds the next. Only parallelize within stages.

### Pattern 3: Fan-out / Fan-in
```
Leader spawns N researchers in parallel
Leader waits for all
Leader synthesizes results
```
Use when: Exploring multiple approaches, broad codebase mapping, multi-source research.

### Pattern 4: Self-organizing Queue
```
Leader creates task queue
Workers claim tasks
Workers report back
Leader assigns next task
```
Use when: Many small tasks of unknown count, load balancing needed.

---

## Pre-flight: Task Decomposition

Before spawning anything, help the user decompose the work:

1. **List all tasks** — one sentence each
2. **Mark dependencies** — which tasks must finish before others start?
3. **Group into waves** — tasks with no blocking dependencies = Wave 1, etc.
4. **Assign to agents** — group related tasks per agent to minimize cross-agent state sharing

Present as a table:
```
Wave | Task | Depends on | Agent
-----|------|-----------|------
1    | Research auth patterns | — | researcher
1    | Research API patterns | — | researcher
2    | Implement auth | Wave 1 | implementer-A
2    | Implement API | Wave 1 | implementer-B
3    | Integration tests | Wave 2 | verifier
```

Ask: "Does this decomposition look right? Any tasks missing or misassigned?"

---

## Status Tracking

While a swarm runs, periodically check:

```bash
# Check task statuses
cat ~/.claude/tasks/<team>/*/json 2>/dev/null | grep '"status"'

# Check for stuck agents (no progress in N messages)
cat ~/.claude/teams/<team>/inboxes/<agent>.json
```

Signs of a stuck swarm:
- Tasks stuck `in_progress` for many iterations
- Agents sending `idle_notification` repeatedly
- Inbox messages going unread

Recovery: Send a targeted message to the stuck agent with clarification, or reassign the task.

---

## Shutdown Checklist

Before declaring done:
- All tasks in `completed` status
- Leader has received results from all teammates
- No pending `shutdown_request` messages unacknowledged
- Run cleanup: `TeamDelete` to remove team config

---

## Integration with Other Frameworks

| Use swarm when... | Combined with |
|-------------------|---------------|
| GSD execute-phase has 3+ independent plans | GSD spawns agents via swarm pattern |
| Gepetto section files are independent | Swarm implements sections in parallel |
| Ralph-loop hits a complex multi-part task | Pre-split into swarm, then loop on each part |
