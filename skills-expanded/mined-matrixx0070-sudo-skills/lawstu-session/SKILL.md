---
name: lawstu-session
version: 1.0.0
description: Run a focused study session — set a goal, pick the right drill, work in timed blocks, and close with a recall check and next step.
author: matrixx0070
tags: [law-student, study-session, focus, orchestration, active-recall]
capabilities: []
---

## When to use

Reach for this when you sit down to study and want structure instead of aimless re-reading. The skill runs a single session end-to-end: it clarifies your goal, routes you to the right drill (briefing, IRAC, flashcards, Socratic), keeps you in timed blocks, and closes with a recall check so the time sticks.

**Not for:** planning the whole term (see `lawstu-study-plan`) or replacing the specific drills it routes to — it orchestrates them. It never does the work for you or produces submittable answers; it structures *your* effort. Not for a live cold-call rehearsal alone (see `lawstu-cold-call-prep`).

## Method

1. **Name one goal.** "Understand promissory estoppel well enough to IRAC it," not "study Contracts." Decision point: if the goal needs more than 90 minutes, split it into two sessions.
2. **Pick the mode** that fits the goal: new material → `lawstu-case-brief`; consolidation → `lawstu-outline-builder`; recall → `lawstu-flashcards`; application → `lawstu-irac-practice`; pressure-test → `lawstu-socratic-drill`.
3. **Work in timed blocks** (e.g., 25/5 or 50/10). Phone parked; one doctrine per block.
4. **Active over passive.** Every block ends in output you produced — a rule stated, a hypo answered — not pages re-read.
5. **Recall check.** Close by reciting the session's core rules from memory, no notes. Gaps become the next session's opener.
6. **Log the next step** so tomorrow starts without warm-up friction.

## Example

Goal: apply the hearsay exceptions. Block 1 — flashcards on the exceptions (recall). Block 2 — three short hypos via IRAC practice (application). Close: recite the exceptions cold — you blank on present-sense-impression vs. excited-utterance timing. That distinction becomes tomorrow's first block. One hour, measurable gain.

## Pitfalls

- Re-reading highlights and calling it studying; passive review feels productive and isn't.
- Vague goals you can't tell you achieved.
- No recall check, so you never learn what didn't stick.
- Doctrine-hopping mid-block; context switches shred retention.

## Output format

```
Goal (one, testable) | time budget
Mode routed to: [brief / outline / flashcards / irac / socratic]
Blocks: [doctrine → output produced]
Recall check: rules recited cold | gaps
Next session opener:
```

## Reference

- **Active recall + spaced practice** drive retention; every block yields output.
- **IRAC** is the default application format when the goal is exam readiness (`lawstu-irac-practice`).
- **Case-brief format** structures new-reading blocks (`lawstu-case-brief`).
