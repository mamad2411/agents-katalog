---
name: "mindforge-pr-branch"
description: "Create a clean PR branch by filtering out .planning/ commits — ready for code review"
---


<objective>
Create a clean branch suitable for pull requests by filtering out .planning/ commits
from the current branch. Reviewers see only code changes, not MindForge planning artifacts.

This solves the problem of PR diffs being cluttered with PLAN.md, SUMMARY.md, STATE.md
changes that are irrelevant to code review.
</objective>

<execution_context>
@.agent/workflows/mindforge-pr-branch.md
</execution_context>

<process>
Execute the pr-branch workflow from @.agent/workflows/mindforge-pr-branch.md end-to-end.
</process>
