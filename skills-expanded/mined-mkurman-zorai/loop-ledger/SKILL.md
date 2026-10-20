---
name: loop-ledger
description: Scaffold a J-Space-style 5-state task ledger (Goal/Core/Verified/Open/Next) for long multi-step tasks and goal runs. Use when starting loop-tier work that spans multiple tools, files, sessions, or subagents, or when resuming such work after a pause or handoff. Pairs with the loop-ledger-verification-task guideline.
tags: [productivity, task-management, goal-runs, state]
---

# Loop Ledger

A five-section persistent artifact that lets a task survive tool-call seams, context switches, compression, and restarts without re-deriving state.

## When to use

- Loop-tier work: multi-file, multi-tool, multi-session, goal-run, or subagent-coordinated tasks.
- Not for fast single-step work — overhead exceeds value there.

## Scaffold

Create `threads/<thread_id>/artifacts/specs/ledger.md`:

```markdown
# Ledger: <one-line task name>

## Goal
<One sentence: the deliverable, not the activity.>

## Core
<Anchors established exactly once, broadcast to every branch/child:>
- Paths: <repo dirs, key files>
- Names/IDs: <goal_run_id, thread_id, session IDs, task IDs>
- Constraints: <hard requirements, acceptance criteria>
- Style/conventions: <language, format, coding conventions in force>

## Verified
<Append-only. One line per claim:>
- <claim> | verifier: <cmd/test/review + exit code> | covers: <scope> | not: <gap>

## Open
<Unresolved questions/blockers with owner or next probe.>

## Next
<Exactly ONE next action, executable cold without further context.>
```

## Maintenance rules

1. **Core is broadcast-once.** Subagent descriptions, child task briefs, and resume turns reference Core entries verbatim instead of paraphrasing. New anchors get added to Core and re-broadcast, never forked privately.
2. **Verified entries carry their verifier and coverage.** A claim without verifier + coverage + gap does not belong here.
3. **Next is replaced, never accumulated.** If it can't be executed cold, make it more specific first.
4. **On resume** (pause/handoff/restart): read the ledger before anything else, confirm Goal still matches the original request, then execute Next.
5. **Checkpoints at seams:** after each tool chain boundary, file switch, or subagent return, refresh against the ledger before acting.

## Completion

The task is done when combined `Verified` coverage matches `Goal` scope (gaps explicitly accepted), `Open` is empty or deferred with stated reason, and the final report cites verifier + coverage per claim.

Source: adapted from J-Space Cognition Suite V3.6 mechanisms (capability-realization report, Tiger3807861189, 2026) — runtime-agnostic subset: 5-state ledger, verifier binding, failure inheritance, broadcast-once anchors. First-person grammar and first-turn persona anchoring intentionally excluded as model-specific overfits.
