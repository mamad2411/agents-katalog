---
name: test-pilot-loop
description: >
  Test-pilot any running app through computer use. Trigger when a build completes,
  user says "test pilot this", "test my app", "quick flight", "run a flight check",
  or "check the UX". Tests with three knowledge tiers (knows nothing, has manual,
  has PRD) and reports UX findings with a Tier Gap Ratio.
version: 1.0.0
tools: browser, exec
tags:
  - testing
  - ux
  - quality
  - automation
  - computer-use
---

# Test Pilot Loop — OpenClaw Skill

AI that doesn't just write code — it flies the product first.

Test any running app through computer use. Find confusion, frustration, and friction — not just bugs.

## When to Activate

- User says "test pilot this", "test my app", "quick flight", "flight check", "check the UX"
- A build completes and the user wants validation
- User says "is my app usable?" or "can someone figure this out?"
- Cron triggers after a build event

## Before Testing

Ask the user (if not already provided):
1. **Where is the app?** (URL, app name, window title, simulator)
2. **What was just built?** (one sentence)
3. **What should a user be able to do?** (the core task)

If the user provides a PRD or README path, read it for Runs 2 and 3.

## Two Modes

### Quick Flight (~5 min)
One test as a cold user who knows nothing.

### Full Test Pilot Loop (~15–20 min)
Three sequential tests with different knowledge tiers. Compare results.

---

## Quick Flight

1. Open the app (browser URL or find window via desktop control)
2. You have **no prior knowledge** of this app except its name
3. Try to complete the task the user described
4. Narrate what you see, try, and what confuses you
5. Count every action (click, type, scroll, navigate) as one step
6. Write the report:

```
QUICK FLIGHT REPORT
═══════════════════
App: [name or URL]
Feature tested: [what was built]
Task attempted: [what you tried to do]

COMPLETED: YES / NO / PARTIALLY
If NO: [where you got stuck and why]

STEPS: [count]   WRONG TURNS: [count]

WHAT WORKED WELL:
• [clear, natural moments]

WHAT CONFUSED ME:
• [where, what, why]

WHAT I'D CHANGE:
• [specific suggestion]

BUGS FOUND:
• [what happened vs expected]

INTERFACE CHECK:
  Layout clear:         YES / MOSTLY / NO
  Labels make sense:    YES / MOSTLY / NO
  Feedback after taps:  YES / SOMETIMES / NEVER
  Know what to do next: YES / SOMETIMES / NO

ONE-SENTENCE SUMMARY:
"[The single most important thing to fix.]"
```

---

## Full Test Pilot Loop

Run three tests sequentially. Reset the app before each run.

**Run 1 — Cold User (knows nothing):**
You have no prior knowledge of this project. Find the app, attempt the task, count every step, note every moment of confusion. If you can't figure it out after 8 confused steps, report abandonment.

**Run 2 — Guided User (has the manual only):**
You have read the user manual or README. You have NOT seen the PRD. Follow the documented instructions. Note every place where the docs are wrong, incomplete, or use different words than the app. If no manual exists, skip this run.

**Run 3 — Insider (has the full PRD):**
You have the full Product Requirements Document. You know every intended feature and acceptance criterion. Test whether the app delivers what was specified. If no PRD exists, skip this run.

### Full Report

```
TEST PILOT REPORT
═════════════════
App: [name or URL]
Feature: [what was built]
Task: [what was tested]
Tiers completed: [1 / 2 / 3]

┌─────────────────────────────────────────────────┐
│              RUN 1       RUN 2       RUN 3       │
│              COLD        GUIDED      INSIDER     │
├─────────────────────────────────────────────────┤
│ Completed:   [Y/N]      [Y/N]       [Y/N]       │
│ Steps:       [count]    [count]     [count]      │
│ Wrong turns: [count]    [count]     [count]      │
│ Confusion:   [count]    [count]     [count]      │
└─────────────────────────────────────────────────┘

TIER GAP RATIO: [Cold steps] / [Insider steps] = [X]x
  ≤ 1.5x = ⭐ Excellent    ≤ 2.0x = 🟢 Good
  ≤ 3.0x = 🟡 Acceptable   > 3.0x = 🔴 Poor

COLD USER FINDINGS:
  Confused at: [where, what, why]
  Would give up at: [exact point]
  Would have helped: [suggestion]

GUIDED USER FINDINGS:
  Manual accuracy issues: [wrong/outdated instructions, terminology mismatches]

INSIDER FINDINGS:
  PRD compliance: [X]%
  Requirements not met: [list]

BUGS FOUND:
  • [what happened vs expected]

FIX THESE (priority order):
  1. [most important — what and why]
  2. [next]
  3. [next]

VERDICT: PASS ✅ / NEEDS WORK ⚠️ / FAIL ❌
```

---

## After Testing

1. Send the report to the user
2. If a coding agent is running: save the report to `FLIGHT_PLAN.md` or `test-pilot-report.md`
3. If user says "fix it": write the FIX THESE section to the shared project file

## Retest Loop

When user says "retest", "test again", or "check the fixes":
1. Re-run the tests that previously found issues
2. Compare new results to previous
3. Report whether the Tier Gap Ratio improved
4. Continue looping until PASS

### Persistent Looping with Dual-Patrol

For continuous build-test-fix cycles (overnight runs, multi-iteration development), combine this skill with the **Dual-Patrol Model** from the full Test Pilot Loop framework. Both the orchestrator (Cowork Opus) and the coding agent patrol a shared `FLIGHT_PLAN.md` file independently — no direct terminal control needed. The orchestrator writes feedback and `NEXT_ACTION` instructions; the coding agent picks them up, fixes, rebuilds, and signals "ready for retest." See [TEST_PILOT_LOOP.md — The Dual-Patrol Model](https://github.com/suhuandds/test-pilot-loop/blob/main/TEST_PILOT_LOOP.md#the-dual-patrol-model) for setup details.

## Rules

1. Always test through computer use, not by reading source code
2. Never skip the cold user test — it's the most valuable
3. Always count steps. Steps are the universal measurement.
4. If you can't access the app, tell the user immediately
5. Never invent features that aren't there. Report what you see.
6. Be honest about confusion — your confusion IS the feedback
7. If a run exceeds 20 steps without completing the task, report abandonment
8. Reset the app between tier runs for a fresh experience

---

*Test Pilot Loop Skill v1.0*
*By Huan Su — github.com/suhuandds/test-pilot-loop*
