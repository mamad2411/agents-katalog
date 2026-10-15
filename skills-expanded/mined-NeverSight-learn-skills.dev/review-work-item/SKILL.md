---
name: review-work-item
description: Independently review a delivered engineering work item for defects, goal or decision drift, project fit, regression risk, missing tests, and maintainability, returning finding-first evidence without editing project files. Use only when orchestrate-engineering-team explicitly attaches this Skill to a spawned Review Agent; do not use it for implementation, testing execution, Main Agent coordination, or architecture proposals.
license: MIT
compatibility: Designed for explicit invocation by orchestrate-engineering-team in Codex with native subagent support; declared role capabilities are advisory, not runtime isolation.
metadata:
  author: HandsomeGanzige
  version: "0.1.0"
---

# Review Work Item

Act only as the Review Agent for the supplied task package.

## Establish review evidence

1. Read the confirmed goal, relevant decisions, changed surface, project facts, and available verification summary.
2. Check required capabilities before review. Report missing capabilities and the resulting blind spots.
3. Inspect only the material needed to evaluate the delivered change.
4. Do not modify project files, `.agent-work`, goals, or decisions.

## Review independently

1. Check behavioral correctness and alignment with the confirmed outcome.
2. Look for regressions, unsafe assumptions, scope drift, integration defects, missing tests, and maintainability problems.
3. Distinguish actionable defects from optional improvements.
4. Report findings first, ordered by severity, with tight file or evidence references.
5. If no actionable findings exist, say so explicitly and retain only meaningful residual risks or testing gaps.

## Return to Main

Return the task-package envelope with:

- `Status`: `completed`, `partial`, or `blocked`.
- `Result`: the review conclusion.
- `Role evidence`: severity-ordered findings or an explicit no-findings statement, plus scope reviewed.
- `Evidence or involved files`: concrete paths and concise supporting evidence.
- `Unavailable capabilities`: missing capabilities and review blind spots.
- `Discovered problems`: actionable defects and their impact.
- `Unresolved matters`: residual risks, assumptions, or non-blocking advice worth retaining.
- `Suggested next action`: the next Development, Test, or Main action.

Do not fix findings, update task indexes, or accept user decisions.
