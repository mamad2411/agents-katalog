---
name: eng-task-management
description: Update the Mermaid task diagram and project tracker tickets when engineering tasks change status. Use when a task is starting, completing, or getting blocked — to keep the project's eng-roadmap.md diagram and the tracker in sync.
alwaysApply: false
---

# Eng Task Management

The source of truth for task status is `eng-roadmap.md` in each project folder. Both frontend and backend engineers track tasks through this file.

Keeps two things in sync whenever a task changes status:
1. The Mermaid flowchart in the project's `eng-roadmap.md`
2. The corresponding ticket in the project tracker (Jira, Linear, GitHub Issues, etc.)

---

## Task Diagram States

All task nodes use `style` directives. Four states:

| State | When to use | Mermaid style |
|-------|-------------|---------------|
| Default (no style) | Not yet started, unblocked | *(no style directive)* |
| Blocked | Cannot start — has unmet dependencies | `fill:#ffe0e0,stroke:#ffaaaa,color:#000000` |
| In Progress | Actively being worked on | `fill:#fffde0,stroke:#ffeeaa,color:#000000` |
| Complete | Done | `fill:#e0f5e0,stroke:#aaddaa,color:#000000` |

Only unblocked (default) or in-progress tasks may transition to In Progress or Complete. Blocked tasks must be unblocked first.

---

## Auto-Unblock Rule

Whenever a task is marked **Complete**, check every task that directly depends on it (downstream neighbors in the diagram). For each dependent that is currently **Blocked**, check whether *all* of its direct prerequisites are now Complete. If so, remove its red style so it returns to the default (unblocked) state.

## Auto-Block Rule

Whenever a task is added or a new dependency edge is introduced, re-evaluate the blocked state of all affected downstream tasks. Any task that now has at least one prerequisite that is not yet Complete should be marked Blocked (red) if it isn't already.

---

## Project Tracker Integration

Configure your project tracker here:

- **Instance:** `[YOUR_INSTANCE]` (e.g., `yourcompany.atlassian.net` for Jira, `linear.app` for Linear)
- **Find tickets:** `[YOUR_QUERY]` (e.g., Jira JQL: `parent = <EPIC_KEY>`, Linear: filter by project)
- **Transition to Done:** `[YOUR_DONE_TRANSITION_ID]` (e.g., Jira transition ID `31`)
- **Transition to In Progress:** `[YOUR_IN_PROGRESS_TRANSITION_ID]`
- **Transition to Blocked:** `[YOUR_BLOCKED_TRANSITION_ID]`

### Workflow: task completes

1. In `eng-roadmap.md`, mark the node Complete (green)
2. Apply auto-unblock rule to dependents
3. Transition the corresponding tracker ticket to Done
4. Commit and push

### Workflow: task starts

1. In `eng-roadmap.md`, mark the node In Progress (yellow)
2. Transition the tracker ticket to In Progress

### Workflow: task gets blocked

1. In `eng-roadmap.md`, mark the node Blocked (red)
2. Apply auto-block rule to downstream tasks
3. Transition the tracker ticket to Blocked

---

## Finding the Right Ticket

Match the ticket summary to the diagram node label. If ticket keys aren't embedded in the diagram, search by epic/project in your tracker.
