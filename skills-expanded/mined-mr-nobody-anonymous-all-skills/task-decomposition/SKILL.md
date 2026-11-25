---
name: task-decomposition
description: Break a large project or vague goal into concrete, ordered, completable subtasks with dependencies and estimates.
category: productivity
aliases:
- break-down
- subtasks
- wbs
- work-breakdown
- project-decompose
triggers:
- break this into smaller tasks
- decompose this
- how do I start this project
- break down this project
- what are the steps
- subtasks
- work breakdown
keywords:
- break
- decompose
- subtasks
- steps
- project
- plan
- split
- chunk
- smaller
dependencies: []
risk: low
version: 1.0.0
source: custom
enabled: true
author: Mr-Nobody-Anonymous
tags:
- break
- decompose
- decomposition
- productivity
- steps
- subtasks
compatibility:
  claude-code: '>=1.0'
  skillhub: '*'
  cursor: '>=0.40'
  codex: '*'
network_access: false
filesystem_access: read
credential_access: false
destructive_operations: false
---

# Task Decomposition

## Purpose

Take a large, vague, or intimidating piece of work and produce a concrete list of subtasks —
ordered, completable, with dependencies and rough sizes — that the user can actually start on.

## When to Use

- User has a project, goal, or large task and doesn't know where to start
- User explicitly asks to break something down
- User has a deadline and needs a path to it
- The output of another skill (e.g. `planning`) needs concrete next moves

## When NOT to Use

- The "task" is too vague to decompose (route to `planning` first)
- The user has no real commitment to doing the work (route to `unlazy`)
- The task is a single, small, concrete action (just do it)

## Capabilities

- Hierarchical breakdown (project → milestones → tasks → actions)
- Dependency mapping (what blocks what)
- Size estimates (S / M / L or time)
- Identify the *first* actionable subtask
- Suggest parallelism where possible

## Inputs

- The project / goal / task
- Deadline (if any)
- Resources / constraints (time, people, money)
- Definition of "done"

## Workflow

1. **Define done.** Ask: "What does 'finished' look like?" If the user can't say, the project isn't clear enough yet.
2. **Identify milestones.** 3–7 major waypoints between start and done.
3. **Decompose milestones into tasks.** Each task fits a single work session (1–4 hours).
4. **Decompose tasks into actions.** Each action is 5–60 minutes and completable in one sitting.
5. **Map dependencies.** For each action, what must happen first?
6. **Identify the critical path.** The longest dependency chain. That's the deadline-driving work.
7. **Pick the very first action.** A single verb phrase the user can do in the next hour.

## Tools

- Plain text / paper
- Task tracker (optional)
- Whiteboard or mind map (optional)

## Examples

**User:** "Break down building a portfolio website."
**Response:**
1. Define: "Done" = 3 case studies + about + contact, deployed.
2. Milestones: research, design, build, deploy.
3. Tasks: write copy, choose template, customize, write case studies, deploy.
4. First action: "List 3 sites I admire and write 2 sentences about why."

## Safety

- Don't overload users with 50-step plans — they become another source of overwhelm
- Prefer 5–10 actions at the top level, drill down only as needed

## Source

Custom skill, written for this library.

## Notes

Pairs with:
- `planning` (when the goal itself is unclear)
- `focus` (to design sessions for each subtask)
- `prioritization` (when there are too many parallel threads)