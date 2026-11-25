---
name: implement
description: "Implement a piece of work based on a spec or set of tickets."
---

Implement the work described by the user in the spec or tickets.

Before editing, record the starting commit SHA with `git rev-parse HEAD` and inspect the working tree. Keep unrelated existing changes outside this task.

Use $tdd for code behavior changes, choosing appropriate existing boundaries and honoring any already agreed ones. Load a referenced skill by reading its SKILL.md if this host has no Skill tool.

Run checks relevant to the change and the repository’s required gates. Broaden or repeat checks when failures, new changes, or wider impact justify it.

Continue through implementation, relevant checks, and fixes within the authorized scope. Stop for a user decision only when it affects behavior, scope, material resources, or permission. Once ready, use $code-review in working-tree mode against the recorded starting SHA. Include the task's committed, staged, unstaged, and relevant untracked files. Pass the spec or the agreed acceptance criteria from the conversation.

Address accepted findings and rerun the affected checks. Commit only when the user's request authorizes a commit, including prior authorization in this session. A commit must contain only this task's files. Report the checks, review scope, and any unresolved findings.
