---
name: workflow-conventions
description: Workflow structure, environment variable patterns, planning rules, and development flow for this project. Relevant when creating, editing, or debugging workflows.
user-invocable: false
---

## Workflow Structure

Every workflow directory must follow this layout:

```
workflows/
  {workflow-name}/
    README.md          # What it does, inputs/outputs, how to run
    main.py            # Entry point
    .env.example       # Workflow-specific env var overrides (optional)
    tests/             # Workflow-specific tests (optional for simple scripts)
```

Dependencies are managed in the root `requirements.txt`, not per-workflow.

## Deployment Targets

Every workflow must be runnable locally first. Modal is an optional additional deployment layer. Specify the target in the plan and CATALOG.md.

| Target | How to Run | Notes |
|--------|-----------|-------|
| Local | `python workflows/{name}/main.py` | Always supported — the baseline for every workflow |
| Local + Modal | Local run + `modal deploy workflows/{name}/main.py` | Adds Modal deployment on top of local. Use for scheduled, GPU, or API-deployed functions |

## Modal Modes

When a workflow targets Modal, it must also declare its **Modal mode(s)** in the plan and CATALOG.md. A single Modal function cannot be both a web endpoint and a scheduled/manual function — use separate entry points when combining modes.

| Mode | Entry Point | Trigger |
|------|-------------|---------|
| **Webhook** | `run_modal()` with `@modal.fastapi_endpoint` | HTTP POST with bearer token |
| **Scheduled** | `run_scheduled()` with `schedule=modal.Cron(...)` | Automatic cron + Modal dashboard "Run now" |
| **Manual** | `run_manual()` as plain `@app.function` | Modal dashboard "Run now" or `modal run` CLI |

Modes can be combined (e.g., `webhook + scheduled`). All entry points share the same `run()` core logic and `image`.

## Environment Variables

Env vars use a two-tier loading system:

1. **Root `.env`** (project root) — loaded first. Shared vars across workflows.
2. **Workflow `.env`** (`workflows/{name}/.env`) — loaded second with `override=True`. Workflow-specific overrides.

## Planning

- Save plans to `.agent/plans/{workflow-name}.md`
- Plans are independent — no sequencing, no cross-workflow dependencies
- Each plan must include:
  - What the workflow does (inputs, outputs, side effects)
  - Dependencies and services needed
  - Deployment target (Local, or Local + Modal)
  - Validation steps to verify it works
  - Complexity indicator:
    - **Simple** - Single-pass executable, low risk
    - **Medium** - May need iteration, some complexity
    - **Complex** - Break into sub-tasks before executing
- Use `.agent/plans/_template.md` as a starting point

## Development Flow

1. **Scaffold** — Run `/new-workflow` to create the directory and plan template
2. **Plan** — Fill in the plan at `.agent/plans/{workflow-name}.md`
3. **Build** — Run `/build` to execute the plan
4. **Validate** — Test the workflow runs correctly
5. **Ship** — Deploy to target (Modal, cron, etc.)

## Progress Tracking

See `CATALOG.md` for the status of all workflows. Updated when a workflow is completed.
