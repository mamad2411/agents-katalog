---
name: work-discipline
description: "Execution discipline for implementing planned work: when to enter plan mode, how to timebox exploration, subagent strategy, verify-as-you-go, and when to stop and re-plan. Apply while implementing any phase or non-trivial change."
---

# Skill: Work Discipline

## Purpose
Behavioral guardrails for while you're actively implementing. This complements planning skills (what to build) and verification skills (did it work) with guidance on how to work.

## 1. Plan Mode Defaults

- Enter plan mode for any non-trivial task (3+ steps or architectural decisions)
- If something goes sideways mid-implementation, **stop and re-plan** — don't keep pushing a broken approach
- Use plan mode for verification steps too, not just building
- Write detailed specs upfront to reduce ambiguity

## 2. Subagent Strategy

- Use subagents liberally to keep the main context window clean
- Offload research, exploration, and parallel analysis to subagents
- One task per subagent for focused execution
- For complex problems, throw more compute at it via subagents rather than cramming everything into one context
- Waiting on subagents for more than a few minutes? Arm a stall watchdog first (the "Arm the watchdog" step in `/autopilot` and `/orchestrator`). Silence must have a deadline; a hung agent otherwise blocks the lead forever

## 3. Verify As You Go

- Never declare a task complete without proving it works
- Run tests, check logs, demonstrate correctness after each meaningful change
- Diff behavior between main and your changes when relevant
- Ask yourself: "Would this pass code review without revision?"
- This is lighter than `/verify` — just the habit of checking your own work before moving on

## 4. Simplicity and Minimal Impact

- Make every change as simple as possible — impact minimal code
- For non-trivial changes, pause and ask "is there a more elegant way?"
- If a fix feels hacky, step back — knowing everything you know now, implement the clean solution
- Skip this for simple, obvious fixes — don't over-engineer
- Changes should only touch what's necessary — avoid introducing unrelated modifications

## 5. Bug Fixing

- When given a bug report, gather evidence first: read the error, check the code, understand the cause
- Point at logs, errors, failing tests — then resolve them
- Fix root causes, not symptoms. No temporary workarounds masquerading as fixes
- Don't shotgun-fix by trying multiple things at once — change one thing, test, iterate

## 6. Re-Plan Trigger

If any of these happen, stop coding and re-enter plan mode:
- The plan's assumptions no longer match what you're seeing in the code
- You've discovered a dependency the plan didn't account for
- A task is turning out 3x more complex than expected
- You're about to make changes outside the current phase scope
