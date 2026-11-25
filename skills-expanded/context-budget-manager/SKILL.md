---
name: context-budget-manager
description: Keeps agent sessions lean — decide what to load into context vs. reference by path, summarize-and-restart before quality degrades, enforce progressive disclosure in skills, and run a session hygiene checklist. Use when the user says "the session is getting long", "the agent is getting dumber", "context is bloated", "should I start a new chat", or when planning how much material a task loads. Don't use for cleaning persistent memory files — that's memory-hygiene.
version: 1.0.0
author: Gen AI Hub
license: MIT
metadata:
  hermes:
    tags: [Agent Mastery, Context, Sessions, Efficiency, Hygiene]
    related_skills: [memory-hygiene, model-cost-optimizer]
---

# Context Budget Manager

Context is a budget, not a backpack: every token loaded competes with the tokens doing the actual work, and a stuffed session gets slower, dumber, and pricier all at once. This skill is the discipline of loading the minimum that lets the task succeed — reference the rest by path, restart before degradation instead of after, and keep skills disclosing progressively. The standard: at any moment you can say what's in context and why each piece earns its place.

## When to Use

- Kicking off a task that touches many files, docs, or datasets — decide the load plan first.
- Mid-session symptoms: repeated questions, forgotten instructions, drifting quality, ballooning per-message cost.
- Authoring or reviewing a skill's structure (progressive disclosure is a context decision).
- Handing a long-running task across sessions and the handoff needs to survive the restart.
- **Not for:** pruning long-term memory/notes files (`memory-hygiene`), or cutting cost by changing model tier (`model-cost-optimizer`).

## Quick Reference

| Decision | Rule of thumb |
|---|---|
| Load vs. reference | Load only what THIS step reads or edits; everything else is a path + one-line note |
| Big file (>300 lines) | Read the relevant section by offset/heading, never the whole file "for context" |
| Search results | Keep the conclusion + file paths; drop the raw dumps |
| Restart trigger | Any 2 of: repeated instructions, forgotten constraints, >70% context used, phase complete |
| Skill structure | Hot path first and under ~40 lines; edge cases at the bottom; heavy reference in separate files |
| Handoff size | Restart summary ≤30 lines — state, not story |
| Active skills | Only the skills this task triggers; park the rest |

## Procedure

1. **Plan the load before loading** — list what the task needs as two columns: LOAD (files/sections this step will actually read or edit) and REFERENCE (paths with a one-line description, loaded only if a step demands them). If the LOAD column exceeds ~5 items, the task probably needs phases — split it.
2. **Load surgically** — open big files by section (headings, line offsets, targeted grep) instead of whole-file reads. After any broad search, keep conclusions and paths; do not re-quote file bodies into the conversation. Success: each loaded item maps to a step that used it.
3. **Watch for degradation** — check the restart triggers in the table at natural breakpoints (phase ends, every ~10 exchanges). Two triggers hit = restart now; finishing "just one more thing" in a degraded session is how wrong edits ship.
4. **Summarize-and-restart** — write a handoff of ≤30 lines: goal, decisions made (with reasons), current state (files touched, what's verified), and next 3 actions with exact paths. Persist it to a file (e.g. `HANDOFF.md` or the task ticket) — not just the chat — then start the fresh session from it. Success: the new session resumes without re-reading the old transcript.
5. **Enforce progressive disclosure in skills** — when writing or reviewing a skill: description carries the trigger; hot path in the first ~40 lines; edge cases at the bottom; bulky reference material (schemas, long examples) in sibling files the skill points to, loaded only on need. A skill that front-loads 200 lines taxes every session that touches it.
6. **Run the session hygiene checklist** — at session start: (a) load plan written? (b) memory/notes loaded are current (see `memory-hygiene`)? (c) only skills relevant to this task active? During: (d) no raw data dumps kept after conclusions are drawn? (e) restart triggers checked at breakpoints? At end: (f) durable facts written to files, not left in the transcript?
7. **Deliver the plan** — for any multi-file task, present the filled template below before loading anything, so the user can veto or add items while the budget is still intact. Success: work starts with an approved plan, not an accidental one.

## Output Template

```
## Context plan: <task> — <date>
Budget stance: LOAD <n> items / REFERENCE <m> items

LOAD (reads/edits this phase):
- <path or section> — <why this step needs it>

REFERENCE (path only, load on demand):
- <path> — <one-line description>

Restart triggers armed: repeated-instructions | forgotten-constraint | ~70% full | phase-end
Handoff file: <path> (written before any restart)
```

## Pitfalls

- **"Load everything for context"** — whole repos or full docs read in "to be safe," burning the budget before work starts. Recovery: dump nothing retroactively-useful; restart with a surgical load plan and reference the rest by path. Safety comes from the plan, not the payload.
- **Restarting too late** — quality visibly degraded three exchanges ago, and now the handoff summary is written by a degraded session. Recovery: restart anyway, but verify the handoff against the actual files (not the transcript's claims) before trusting it; the checklist's fixed triggers exist so next time the call isn't a judgment call.
- **Handoff as story, not state** — the summary narrates the journey ("first we tried X, then...") and the new session inherits noise. Recovery: rewrite as state — decisions, current file status, next actions with paths. If a line doesn't change what the next session does, cut it.
- **Skill bloat taxing every session** — a skill front-loads every edge case and example, costing 300 lines on load. Recovery: restructure — hot path up top, edge cases below, reference tables into sibling files; re-run the repo validator after restructuring.
- **Losing durable facts in the restart** — a decision lived only in the abandoned transcript. Recovery: reconstruct from files/diffs, then adopt the rule: any decision worth keeping gets written to a file the moment it's made (that's also `memory-hygiene` territory).
- **Every skill active in every session** — a dozen loaded skills tax the budget before the first message. Recovery: park skills the task can't trigger; if a skill self-triggers too eagerly, its description needs a tighter "Don't use for" clause — route that to `skill-author-coach`.

## Verification

- [ ] Load plan exists and every loaded item was used by a step
- [ ] No whole-file reads where a section read sufficed; no raw search dumps retained
- [ ] Restart triggers checked at each phase boundary; restarts happened at ≤2 triggers, not after visible degradation
- [ ] Handoff (≤30 lines, state-not-story) written to a file before any restart
- [ ] New session resumed from the handoff without re-reading the old transcript
- [ ] Only task-relevant skills were active for the session
- [ ] Durable decisions persisted outside the transcript by session end
