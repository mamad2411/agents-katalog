---
name: emergency-save
description: Emergency workflow for preserving work before the user must leave immediately.
---

# Emergency Save

## Purpose

This skill is activated when the user must leave immediately due to an emergency, interruption, power outage, disaster, or any unexpected event.

The objective is **preserving work**, not completing work.

---

## Triggers

Examples:

- /safe
- /emergency
- "撤退"
- "緊急"
- "停電了"
- "Fire"
- "Earthquake"
- "Need to leave now"

---

## Priority

This skill has the highest execution priority.

Immediately interrupt all non-critical tasks.

Do not wait for long-running operations.

---

## Procedure

1. Stop accepting new work.

2. Cancel any long-running operation whenever possible.

Examples:

- build
- test
- install
- AI generation
- indexing
- search

3. Record current working state.

Include:

- Current task
- Completed work
- Remaining work
- Files modified
- Known issues

4. Save the agent memory.

5. Stage all modified files.

```
git add .
```

6. Create a commit.

Example:

```
git commit -m "emergency-save"
```

7. Push the current branch.

```
git push origin HEAD
```

---

## Never

Never:

- merge
- rebase
- pull
- squash
- clean history
- resolve conflicts

Those actions can be performed after the user returns.

---

## Success Output

Return only:

Emergency save completed.

If something failed, clearly report the step that failed.