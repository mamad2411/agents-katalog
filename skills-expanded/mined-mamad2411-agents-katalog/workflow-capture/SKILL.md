---
name: workflow-capture
description: Maintain a durable, tagged journal of a complex workflow so it can later be distilled into a reusable skill. Use this whenever beginning a complex, multi-step workflow (design work, automation build, CAD, RAG pipeline, website work, or anything non-trivial you might want to repeat), even if the user does not say "capture" or "log". If the work has sequencing, corrections, or hard-won discoveries worth keeping, start a worklog. Also use on resume to read an existing worklog after a context reset.
---

# Workflow Capture

Maintain an append-only journal that survives compaction and `/clear`, capturing the signal (decisions, sequencing, corrections, dead ends) that should become a skill. Do not log keystrokes; the transcript already does that at the wrong altitude. Capture why, not just what.

## At session start

1. Determine the active workflow slug (kebab-case, e.g. `figma-site-redesign`).
2. Look for `_worklogs/YYYY-MM-DD-<slug>/WORKLOG.md`.
   - If it exists, read it fully before doing anything. It is your memory.
   - If not, create the directory and a new WORKLOG.md with a one-line header naming the workflow and date.

## Tag schema

Every entry carries exactly one tag:

- DECISION: what was done and why -> a procedure step
- SEQUENCE: X must precede Y -> ordered steps or preconditions
- CORRECTION: user overrode you -> a hard rule
- DEADEND: tried X, failed because Y -> a "do not do this" warning
- CONVENTION: naming, structure, params, defaults -> reference material
- DISCOVERY: tool quirk, API limit, gotcha -> environment notes
- CHECKPOINT: state snapshot before clear or compaction -> resume anchor

## Entry format

Append, never rewrite history.

```
## [YYYY-MM-DD HH:MM] TAG
One-line summary.
Optional result and fix or lesson.
Tags: comma, separated, keywords
```

## When to append

Append an entry the moment one of these happens:
- The user corrects or overrides something (CORRECTION).
- An approach fails and you switch (DEADEND).
- A non-obvious ordering constraint appears (SEQUENCE).
- You set a reusable convention (CONVENTION).
- A tool behaves unexpectedly (DISCOVERY).

Keep entries short. The lesson matters, not the prose.

## Checkpoint and resume

Before any compaction or `/clear`, write a CHECKPOINT entry: current state, open threads, next intended action. On resume in a fresh window, read the worklog and continue from the last CHECKPOINT plus accumulated tags.

## Why this matters

The context window is volatile and mostly noise. A durable tagged journal is the only thing that lets a workflow survive a context reset and later become a skill that makes the next run cheaper and more correct.
