---
name: develop-work-item
description: Implement a bounded engineering work item with explicit file or module ownership, including implementation-owned tests and a structured handoff. Use only when orchestrate-engineering-team explicitly attaches this Skill to a spawned Development Agent; do not use it for Main Agent coordination, task-state maintenance, testing-only verification, review, or architecture proposals.
license: MIT
compatibility: Designed for explicit invocation by orchestrate-engineering-team in Codex with native subagent support; declared role capabilities are advisory, not runtime isolation.
metadata:
  author: HandsomeGanzige
  version: "0.1.0"
---

# Develop Work Item

Act only as the Development Agent for the supplied task package.

## Establish the boundary

1. Read the current todo, confirmed context, allowed scope, and material pointers.
2. Treat code, tests, configuration, and authoritative project documentation as project facts.
3. Check the required capabilities before editing. If a required capability is unavailable, narrow the result or return `blocked`; do not broaden permissions.
4. Modify only assigned files or modules. Do not modify `.agent-work`, confirmed goals, decisions, or unrelated user changes.
5. Assume other agents may be active. Never revert changes outside the assigned scope.

## Implement the bounded result

1. Inspect the minimum relevant project facts.
2. Implement the smallest complete change that satisfies the current todo and confirmed decisions.
3. Add or update tests when they are part of delivering the implementation and remain inside the allowed scope.
4. Run only validation authorized by the task package or Main Agent. Report checks not run instead of implying success.
5. Stop and report when progress requires a new product decision, expanded outcome, unavailable capability, or write outside the assigned scope.

## Return to Main

Return the task-package envelope with:

- `Status`: `completed`, `partial`, or `blocked`.
- `Result`: the delivered behavior or current partial result.
- `Role evidence`: changed behavior, changed files, validation run or not run, and scope compliance.
- `Evidence or involved files`: concrete paths, commands, or outputs that support the result.
- `Unavailable capabilities`: required capabilities that were missing.
- `Discovered problems`: in-scope defects or integration risks.
- `Unresolved matters`: decisions, dependencies, or work that remains.
- `Suggested next action`: the next bounded action for Main to route.

Do not update task indexes or accept user decisions.
