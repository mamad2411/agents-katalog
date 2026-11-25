---
name: prioritize
description: Pick the ops tasks genuinely worth doing next (at most 3) from active plans and backlog for autonomous execution, weighing impact, feasibility, and project goals.
---

# Ops Prioritize

Given a project's active plans, backlog, and goals, select the tasks genuinely worth executing now — at most 3. The output is a ranked shortlist with execution order — this skill does NOT execute them.

## Context Required

You need the full project overview loaded (`charter.md`, MEMORY.md, state, backlog, active plans) plus any newly identified work items from `find-tasks`.

The project's goals are in `charter.md` (a repo set up before it existed keeps them in MEMORY.md): weigh impact against them.

## Selection Criteria

Score each candidate task on these dimensions:

### Impact (weight: high)

How much does completing this task move the project toward its goals?

- **High**: directly advances a primary goal, unblocks other work, or fills a critical knowledge gap
- **Medium**: advances a secondary goal, improves project quality, or creates useful reference material
- **Low**: nice-to-have, minor cleanup, or distant from current priorities

### Feasibility (weight: high)

Can an autonomous agent complete this task without human input or real-world actions?

- **High**: pure research, writing, analysis, or knowledge management — all inputs are available
- **Medium**: mostly feasible, but may need assumptions about preferences or priorities
- **Low**: requires external information the agent can't access, real-world actions, or significant subjective judgment

Tasks with low feasibility should be skipped — they'll end up in the follow-up file anyway.

### Independence (only for tasks meant to run in parallel)

Tasks that will run one after another need not be independent. If the caller wants to run two in parallel, they must be:

- Tasks that modify the same files are NOT independent
- Tasks where one's output is the other's input are NOT independent
- Tasks touching different backlog areas, state files, or reference topics are usually independent

## Process

### Step 1: Inventory

List all candidate tasks from:

1. **Active plans** in `plans/` — these are already approved work, except an autopilot cycle record (`*autopilot-cycle*`), which is autopilot's record, not a plan
2. **Backlog items** — particularly those marked as high priority or quick wins; where the repo's CLAUDE.md has an `## Autopilot` section, not `backlog/ideas.md` or an item marked `(code item)`, which are autopilot's to route or build
3. **Newly identified items** from the latest `find-tasks` run

For each, note: description, source file, estimated effort, and which files it would touch.

### Step 2: Score

Rate each candidate on impact and feasibility. Discard anything with low feasibility.

### Step 3: Select

Pick the tasks with the highest combined impact × feasibility that are worth the user's review time — at most 3, and fewer, or none, when that is all the candidates justify. A cosmetic or speculative item doesn't earn a slot because one is free.

If active plans exist, prioritize them — they represent work the user already approved. Backlog items and newly identified work fill remaining slots.

### Step 4: Prepare

For each selected task, prepare an execution brief:

```markdown
## Selected Tasks

### Task 1: [Title]
- **Source**: [active plan file or backlog file + item]
- **What**: [1-2 sentence description of what the sub-agent should do]
- **Scope**: [which files will be created/modified]
- **Effort**: light / medium / heavy
- **Plan exists**: yes/no — if no, the sub-agent should create one first

### Task 2: [Title]
...
```

If a selected task doesn't have an existing plan file, note that the sub-agent should create one as its first step (following `plan` format).

### Step 5: Order

Determine execution order. Preferences:

1. Tasks with existing plans go first (less setup overhead)
2. If a task might inform another, put it first

## Rules

- **Never select more than 3** — better to complete a focused batch and reassess
- **Skip tasks that need a real-world action** — `ops:work-autonomously` lists them
- **Work carrying an `ASKED (decide <id>` marker** — not ready while that to-decide question is open and has `blocks` set; ready once it is answered, and applying the answer is part of the task
- **Respect the user's priorities** — if the charter, MEMORY.md or state files indicate urgency on a topic, weight those tasks higher
