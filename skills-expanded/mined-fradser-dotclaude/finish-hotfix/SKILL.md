---
name: finish-hotfix
allowed-tools: ["Bash(git:*)", "Read", "Write"]
description: Finalizes a hotfix and merges it into main and develop using git-flow, then prunes stale branches and worktrees. This skill should be used when the user asks to "finish a hotfix", "merge hotfix branch", "complete hotfix", "git flow hotfix finish", or wants to finalize a hotfix.
model: haiku
argument-hint: "[version]"
user-invocable: true
disable-model-invocation: true
---

## Workflow Execution

**Launch a general-purpose agent** that executes the finish-hotfix workflow.

Follow the pipeline in `../../references/gitflow-finish-pipeline.md`:
- **Workflow Type**: `hotfix`
- **Arguments**: `$ARGUMENTS`
