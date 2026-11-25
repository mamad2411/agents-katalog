---
name: divide-task
description: Divide a specced pastiche task into sub-task GitHub issues with autonomy and dependency labels, mirror them into `_dev/TODO.md`, and update the parent issue. Use after `grill-to-spec` completes for a task, or when the user invokes `/divide-task`.
---

# divide-task

Harness conventions: `_dev/docs/harness.md`. Requires: task spec written, task `[WIP]`, feature branch checked out.

## Workflow

1. **Derive sub-tasks from the spec.** Each sub-task is one implementation step, sized for a single overnight session. Number them `N.1, N.2, …` where `N` is the task's TODO number.

2. **Analyze each sub-task:**
   - **Autonomy** — purely mechanical, mergeable without human judgment → `autonomous-ready`; otherwise → `decision-needed`. When in doubt, `decision-needed`.
   - **Dependencies** — which sub-tasks must land first. Independent sub-tasks that touch disjoint files/logic may run in parallel; note the execution order.

3. **Review with the user** before creating anything: list sub-tasks, labels, and dependency order. Adjust until approved.

4. **Create child issues.** For each sub-task:
   - Title `[N.x] <name>`; body: one-paragraph scope + pointer to the spec path; same milestone as the parent; autonomy label.
   - For blocked ones: create `blocked-by-<blocker-issue-number>` labels on demand (`gh label create`) and apply them. Blockers must be created first so their issue numbers exist.
   - Link each as a sub-issue of the parent (GitHub sub-issue, or a task-list in the parent body if unavailable).

5. **Mirror into `_dev/TODO.md`.** Under the task line, add an indented checklist: `  - [ ] **N.x** <name> (#<issue>)`.

6. **Update the parent issue.** Add the sub-issue links and the spec reference.

## Label lifecycle (for whoever completes a sub-task)

When a blocking sub-task closes, remove its `blocked-by-<its-number>` label from every issue carrying it, and tick the sub-task checkbox in TODO.md.
