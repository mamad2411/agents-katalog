---
name: backlog-sync
description: Mirror docs/backlog (epics, features, stories, tasks, sprints) to GitHub Issues, sub-issues and milestones - drafts first, shows you the exact content, and publishes only after you approve that draft.
argument-hint: "[EP-nnn | FE-nnn | SP-nn | all]"
disable-model-invocation: true
---

Mirror the backlog to GitHub Issues for scope: $ARGUMENTS (default `all`).

Follow these steps in order. Never combine steps 2 and 4 in one turn.

1. Dispatch the `backlog-manager` agent with mode `draft` and the scope.
2. Show the owner the full content of `docs/backlog/.sync/draft.md`: every title, body, label, milestone and link, plus the sha256. Ask whether to publish it.
3. Stop and wait for the owner's answer. Approval must come in a new message, after the owner has seen the draft. If they ask for changes, edit the backlog docs and go back to step 1.
4. Once approved, dispatch `backlog-manager` with mode `apply <sha256>`. Report the created and updated issue numbers, with links.
