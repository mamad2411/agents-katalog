---
name: task-prioritization
description: "Creates task prioritization frameworks using Eisenhower matrix, ICE scoring, or MoSCoW method to help entrepreneurs focus on highest-impact work."
allowed-tools: Read Write Glob
metadata:
  author: Salah-XD
  version: "1.0"
---

# Task Prioritization

## When to Use This Skill

Use this skill when you need to:
- Prioritize a backlog of tasks using a proven framework
- Decide what to work on first when everything feels urgent
- Create a repeatable prioritization system for weekly or daily planning
- Score and rank business tasks by impact, effort, and urgency

**DO NOT** use this skill for project management setup, full weekly scheduling, or delegation workflows. This is for ranking and ordering tasks by priority.

---

## Core Principle

PRIORITIZATION IS NOT ABOUT DOING MORE — IT IS ABOUT IDENTIFYING THE FEW TASKS THAT MOVE THE BUSINESS FORWARD AND ELIMINATING OR DEFERRING EVERYTHING ELSE.

---

## Phase 1: Gather

Collect the raw task list and context before applying any framework.

### Required Inputs

| Input | What to Ask | Default |
|-------|------------|---------|
| **Task list** | "List every task on your plate right now — brain dump, no filtering." | No default — must be provided |
| **Time horizon** | "Are we prioritizing for today, this week, or this quarter?" | This week |
| **Framework preference** | "Preference: Eisenhower Matrix, ICE Scoring, or MoSCoW? Or want me to recommend?" | Recommend based on context |
| **Top business goal** | "What is your single most important business goal right now?" | Revenue growth |
| **Available hours** | "How many focused work hours do you realistically have in this time period?" | 20 hours/week |

### Framework Selection Logic

- **Eisenhower Matrix** — best for daily/weekly prioritization when tasks vary wildly in urgency and importance
- **ICE Scoring** — best for growth tasks, feature backlogs, or marketing experiments where impact matters most
- **MoSCoW** — best for project scoping or quarterly planning where you need clear must-have vs. nice-to-have categories

**GATE: Confirm the task list, time horizon, and framework before proceeding.**

---

## Phase 2: Categorize

Apply the chosen framework to every task on the list.

### Eisenhower Matrix

Sort each task into one of four quadrants:

```
## Eisenhower Matrix

| Quadrant | Label | Action | Tasks |
|----------|-------|--------|-------|
| Q1 | Urgent + Important | DO FIRST | [tasks] |
| Q2 | Not Urgent + Important | SCHEDULE | [tasks] |
| Q3 | Urgent + Not Important | DELEGATE | [tasks] |
| Q4 | Not Urgent + Not Important | ELIMINATE | [tasks] |
```

Rule: If more than 30% of tasks land in Q1, the user is in reactive mode. Flag this.

### ICE Scoring

Score each task 1-10 on three dimensions and calculate the average:

```
## ICE Scores

| Task | Impact (1-10) | Confidence (1-10) | Ease (1-10) | ICE Score | Rank |
|------|--------------|-------------------|-------------|-----------|------|
| [task] | 8 | 7 | 5 | 6.7 | 1 |
```

Rule: Explain each score briefly. Do not assign scores without rationale.

### MoSCoW Method

Categorize each task into one of four groups:

```
## MoSCoW Prioritization

**Must Have** — business fails or goal is missed without these
- [tasks]

**Should Have** — important but workarounds exist
- [tasks]

**Could Have** — nice improvements, do if time permits
- [tasks]

**Won't Have (this period)** — explicitly deferred
- [tasks]
```

Rule: Must Haves should not exceed 60% of available hours. If they do, something needs to move down.

**GATE: Present the categorized/scored list and get user confirmation before creating the action plan.**

---

## Phase 3: Action Plan

Convert the prioritized list into an executable sequence.

### Ordered Task List

Present the final priority order with time estimates:

```
## This Week — Priority Order

| # | Task | Framework Result | Est. Time | Day |
|---|------|-----------------|-----------|-----|
| 1 | [task] | Q1 / ICE 8.3 / Must Have | 2 hours | Monday |
| 2 | [task] | Q2 / ICE 7.0 / Must Have | 3 hours | Monday-Tuesday |
```

### Time Budget Check

Compare total estimated hours against available hours. If tasks exceed capacity:
- Flag the gap explicitly ("You have 20 hours but 32 hours of Must Haves")
- Recommend which tasks to defer, delegate, or shrink in scope

### Daily Top 3

If the time horizon is weekly, break it into daily top-3 lists:

```
**Monday:** 1. [task] 2. [task] 3. [task]
**Tuesday:** 1. [task] 2. [task] 3. [task]
```

---

## Phase 4: System

Help the user build a repeatable prioritization habit.

### Weekly Prioritization Ritual

Recommend a recurring 30-minute block (e.g., Sunday evening or Monday morning) where the user:
1. Brain dumps all tasks
2. Applies the chosen framework
3. Sets the week's top 5
4. Blocks focus time on the calendar for top 3

### Review Questions

Provide 5 end-of-week review questions to refine the system over time.

---

## Anti-Patterns

- **Prioritizing by deadline only** — urgent is not the same as important. Deadline-driven prioritization keeps you reactive.
- **Scoring without rationale** — ICE scores without explanation are arbitrary. Every score needs a one-line justification.
- **Everything is Must Have** — if 80% of tasks are Must Haves, the framework is not being used honestly. Push back.
- **Ignoring Q2 tasks** — important but not urgent work (strategy, systems, relationships) is where leverage lives.
- **Re-prioritizing daily** — constant re-sorting is procrastination in disguise. Prioritize once, execute all week.

---

## Recovery

- **User cannot decide between two tasks:** Ask "If you could only complete ONE of these before Friday, which moves the business further?" Force the binary choice.
- **All tasks feel urgent:** Ask when each task actually has consequences if delayed. Most "urgent" tasks have soft deadlines.
- **User has no clear business goal:** Pause prioritization. Help them identify a 90-day goal first — priorities cannot exist without a destination.
- **Task list is overwhelming (30+ items):** Group related tasks into projects first, then prioritize at the project level before task level.
- **User resists eliminating tasks:** Reframe: "You are not deleting them. You are choosing not to do them THIS week." Create a parking lot list.
