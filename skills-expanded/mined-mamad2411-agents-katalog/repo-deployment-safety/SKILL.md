---
name: repo-deployment-safety
description: Reviews deployment, rollback, artifact publishing, package publishing, environment promotion, and production-adjacent commands for safety. Use when commands or file changes may release, deploy, roll back, publish, or mutate external systems.
---

# Repo Deployment Safety

Use this skill when a task may deploy, release, roll back, publish artifacts, promote environments, or change externally visible delivery state.

## When to Use This Skill

Use this skill for:

- deploy commands
- rollback commands
- release commands
- package publishing
- container image publishing
- artifact promotion
- infrastructure promotion
- deployment config edits
- production-like environment changes

## Required Behavior

Before deploying, releasing, publishing, or rolling back:

1. Identify target environment.
2. Identify exact command or change.
3. Identify expected effect.
4. Identify blast radius.
5. Identify rollback or recovery path.
6. Identify validation after the action.
7. Ask for explicit approval.

## Workflows

Use:

- `workflows/deployment-plan-review-workflow.md`
- `workflows/rollback-plan-review-workflow.md`

## Resources

Use:

- `resources/deployment-risk-matrix.md`

## Scripts

This skill owns:

```text
scripts/deployment-command-guard.py
```

The root-level `hooks.json` calls this script before `run_command`.
