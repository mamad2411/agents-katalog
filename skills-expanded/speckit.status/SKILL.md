---
name: speckit.status
description: Progress Dashboard - Calculate phase and task progress from tasks.md with evidence and risk visibility.
---

## Mission
Produce a read-only, reproducible progress report from the feature task list.

## Inputs and Outputs
- Read `.agents/specs/[feature]/tasks.md`, `spec.md`, `plan.md`, and linked evidence when available.
- Output a console dashboard plus pending, blocked, overdue, and unverified task lists. Never mutate tasks.md.

## Protocol
### 1. Parse and Validate
- Accept `- [ ]`, `- [x]`, and `- [X]`; detect duplicate IDs, missing phase headings, dependencies, and task paths. Report malformed structure instead of guessing.
### 2. Calculate
- Group tasks by phase and user story; calculate completed, pending, blocked, and total counts and percentages. Treat blocked or unverified tasks as incomplete and reconcile totals.
### 3. Evidence and Risk
- Link tests, review, build, or acceptance evidence for completed tasks. Surface blocked dependencies, stale claims, missing paths, and absent acceptance evidence.
### 4. Report
- Render a stable timestamped dashboard with phase bars, totals, next actions, blockers, and evidence gaps. Diagnose unreadable or empty task files without fabricating progress.

## Completion Gate
Every parsed task is counted exactly once, phase totals reconcile globally, and all non-complete risks are listed.

## Guard Rails
- Read-only: do not edit tasks.md, checkboxes, specs, or implementation files.
- Do not claim delivery from a checkbox alone; distinguish claimed completion from verified evidence.