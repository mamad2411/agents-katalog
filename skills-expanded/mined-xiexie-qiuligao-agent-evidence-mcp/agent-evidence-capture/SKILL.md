---
name: agent-evidence-capture
description: Capture screenshots, short recordings, and milestone evidence during long-running agent tasks. Use when an agent is asked to perform multi-step browser, desktop, QA, troubleshooting, deployment, or admin workflows where the user wants checkpoint artifacts, progress evidence, error snapshots, or a final timeline of what happened.
---

# Task Evidence Capture

Create a session before a long-running task when the user asks for screenshots, recordings, progress evidence, reviewable checkpoints, or a visible audit trail.

## Follow This Workflow

1. Start a session with a task-oriented name.
2. Capture an initial checkpoint when the starting state matters.
3. Capture a checkpoint whenever a major state change happens.
4. Capture an extra checkpoint when an error, warning, or unexpected dialog appears.
5. Prefer screenshots by default.
6. Use short recordings only when motion or transient UI behavior matters.
7. End the session with a summary of artifact paths and key milestones.

## Prefer These Labels

Use short, searchable labels:

- `initial-state`
- `page-loaded`
- `form-filled`
- `submitted`
- `error-dialog`
- `retry-started`
- `success`
- `final-result`

## Prefer These Behaviors

Prefer checkpoint capture over raw screenshot capture when the image documents progress.

Avoid repeated screenshots of nearly identical states unless:

- the user explicitly asks for dense logging
- the UI changes rapidly and evidence matters
- a failure sequence needs to be preserved

Store artifacts in the session directory unless the user gives a specific destination.

Include concise reasons with checkpoints so later summaries are readable.

## Use Recording Sparingly

Use recording only when:

- the user explicitly asks for recording
- drag-and-drop or animation behavior matters
- a bug cannot be explained with still images
- the task needs a short demo clip at the end

Prefer short recordings around milestones instead of recording the entire task.

## End Cleanly

At the end of the task, report:

- the session id
- the artifact directory
- the most important checkpoints
- any recording paths that were created



