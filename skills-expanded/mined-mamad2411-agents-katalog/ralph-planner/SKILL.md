---
name: ralph-planner
description: 自动拆分大任务，不用你一步步指挥，自主排流程。Use when you need to break down complex tasks into executable steps. Triggers on "plan", "break down", "organize tasks", "create plan".
---

> ⚠️ **此 skill 已标记为 OpenCode 遗产**。Reasonix 中请用 `writing-plans` + `executing-plans` 替代任务规划。

# Ralph Planner

Autonomous task decomposition and planning engine.

## Core Principle

Break any complex goal into small, executable, verifiable tasks. Order them by dependencies. Then execute them one by one.

## Planning Process

### Phase 1: Understand the Goal
- Extract the end goal from user's request
- Define clear completion criteria (what does "done" look like?)
- Identify constraints and requirements

### Phase 2: Decompose
Break the goal into tasks following these rules:
- Each task must be completable in ONE iteration
- Each task must have verifiable acceptance criteria
- Each task should produce a tangible output (file, function, test)
- If a task needs more than 3 sentences to describe, split it further

### Phase 3: Order by Dependencies
```
Level 0: No dependencies (can start immediately)
Level 1: Depends on Level 0 tasks
Level 2: Depends on Level 1 tasks
...
```

Typical dependency order:
1. Schema/database changes
2. Core logic/backend
3. API endpoints
4. Frontend components
5. Integration tests

### Phase 4: Create Task List
Format:
```
## Tasks
- [ ] Task 1: [description]
  - AC: [acceptance criteria]
  - Depends: [none]
- [ ] Task 2: [description]
  - AC: [acceptance criteria]
  - Depends: [Task 1]
```

## Execution Rules

1. After creating the plan, immediately start executing the first task
2. Complete each task before moving to the next
3. If a task fails, try alternative approaches before moving on
4. Update the task list as you go (mark completed tasks)
5. If you discover new tasks during execution, add them to the plan

## Task Sizing Guidelines

| Too Big (split these) | Right Size |
|----------------------|------------|
| "Build the entire dashboard" | "Create dashboard data query" |
| "Add authentication" | "Add login API endpoint" |
| "Refactor the API" | "Refactor single endpoint" |
| "Write tests" | "Write tests for one module" |

## Progress Format
```
📋 Plan: [Goal]
📊 Progress: [3/7 tasks done]
⏳ Current: [Task 4: description]
🔄 Next: [Task 5: description]
```
