---
name: devflow-router
description: Routes requests that start with "/devflow" to the build, debug or plan workflow of the devflow plugin. Use only when the user types /devflow or names devflow.
---

# devflow router

Use this skill only when the user invokes /devflow. For any other request, do nothing and let the agent answer normally.

## Memory

If `.devflow/context.md` exists, show the user a one-line summary and ask whether to use it.
Ask before writing to `.devflow/context.md`, and show what will be saved.

## Workflows

| Signal | Workflow |
|---|---|
| error, bug, fix | DEBUG |
| plan, design | PLAN |
| everything else | BUILD |

Stop and report after each workflow; the user decides whether to continue.
