---
name: incremental-task-tree
description: Breaks down large tasks into a hierarchical task tree (level-by-level), limits work scope to small directories/packages, verifies feasibility upfront, and executes work in user-reviewed milestone chunks. Use when the user requests "incremental review", "work in small steps", "limited directory scope", "step-by-step milestones", or explicit tree-based task breakdown.
---

# Incremental Task Tree Workflows

Limits work to a single small directory or package at a time and requests user review in manageable milestone chunks using a level-by-level task tree breakdown.

## When to Use

* User explicitly asks to work in small steps, limit modifications to small directories, or do incremental reviews.
* User requests a large task to be broken down into milestone chunks with confirmation steps.
* Trigger keywords: "incremental mode", "work in small steps", "milestone chunks", "step by step review", "tree breakdown".
* Do NOT trigger for large autonomous tasks unless specifically requested by the user.

## Core Rules

1. **Scoped Directory Boundary**: Limit active changes to a single small directory or package at a time. Avoid large, multi-package edits in a single step unless it is a simple, easily reviewable refactor.
2. **Upfront Feasibility & Deferred Expansion**: Always verify feasibility and compatibility across top-level task splits upfront before execution begins. Defer full exploration and detailed sub-task breakdown of lower branches until reaching that specific branch's execution phase.
3. **User Confirmation in Chunks**: Group fine-grained, deterministic tasks into logical milestones and obtain user approval before executing each chunk.

## Task Tree Decomposition Process

### Step 1: Top-Level Tree Splitting

* Deconstruct the user prompt into high-level tasks.
* Evaluate the size and scope of each split task.
* Order the tasks by the best order of execution (dependencies first / contracts first / etc. as appropriate in the scenario).
* Perform an upfront feasibility and cross-task compatibility check for all tasks before starting work.

### Step 2: Recursive Sub-Task Expansion

* Select active task branches sequentially from start to end.
* If a task is too large or spans broad boundaries, split it further.
* Continue splitting until each leaf task is concise, deterministic, and isolated to a single small package or straightforward refactor.

### Step 3: Milestone Grouping & Review Request

* Combine concise leaf tasks into logical **Milestones**.
* Present the Milestone outline and scope to the user.
* Wait for explicit user confirmation before executing any code modifications.

### Step 4: Execution & Milestone Delivery

* Execute tasks in the approved Milestone in strict sequential order.
* Present results, affected directories, and diff summaries to the user upon completing the Milestone.
* Request review and confirmation before expanding or executing the next Milestone.
