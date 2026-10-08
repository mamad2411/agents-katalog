---
name: line-design
description: "Design a conveyor line for a recurring job: stages as bays, named handoffs, briefs each bay can follow, and a step test before the schedule is turned on."
license: MIT
metadata:
  title: "Line Design"
  category: "Station"
  author: "StarNet"
---

A line is standing work the station runs unwatched: a job lands in the INBOX, rides the belts through BAYS, and leaves at the OUTBOX. Each bay is one agent doing one step from one brief. A line scheduled untested fails at 3 a.m. with nobody there — so the design ends with a test, never with the schedule.

You design and verify; the Commander builds. station.layout is read-only: bays, belts, briefs and schedules are placed in REFIT (Build mode) through the Workflow panel.

## Method
1. **Read the floor first (station.layout).** The lines that exist, whether routing is live, whether automation is stopped (E-STOP), bays on no line, who holds which workstation. Extend an existing line before proposing a new one.
2. **Name the job and the finished output in one sentence each.** "Every weekday: this week's research on X in, a 200-word sourced brief out." If the output is vague, the line has nothing to converge on.
3. **Cut the stages.** A stage earns a bay only when it needs a different skill, different gear, or an independent check. Common shapes: RESEARCHER → WRITER → REVIEWER, or ENGINEER → TESTER. The LINE BUDGET caps stages after the first (6 by default); fewer bays cost less.
4. **Name each handoff before any brief.** For every belt, state what crosses it — "bullet notes with links", "a 200-word draft". That phrase goes in the bay's HANDS OFF field, and the next brief is written against it. A handoff you cannot name is a seam you have not found.
5. **Write each brief as a standing order for arriving work.** The DOES field (up to 2000 characters): what the bay receives, what it does, the output shape, and what to do when the input is thin — say so, never invent.
6. **Add a loop only with a real verdict.** A reviewer bay before a LOOP gate ends its output with `VERDICT: approved` or `VERDICT: revise` plus what to fix; the gate reads only the last three non-empty lines. Set max tries and an escalation lane (a FIXER bay) so a draft that never passes still goes somewhere.
7. **Check gear per bay.** Each bay's agent needs an assigned workstation in that room (no workstation, no compute) plus the props its step uses — a DISH for web, an INTEL CAB for files. station.layout with `line` set shows each bay's tools.
8. **Hand the Commander a build sheet.** One row per bay: role, agent, DOES, HANDS OFF, gear. Then gates, OUTBOX, and the INBOX trigger (schedule, channel, watched folder or webhook).
9. **Test cheapest first.** The test controls are the Commander's to press; ask in this order. WATCH IT is free — a crate rides the belts and each machine says what it would do. Then TEST THIS STEP on bay 1 with a realistic test job (one real run, real cost), carrying each output forward bay by bay — or STEP THROUGH, which pauses at every handoff and delivers nothing. RUN ONE REAL JOB last: end to end, into the OUTBOX. Fix the brief behind any bad output and retest that bay.
10. **Only then schedule it.** The schedule is saved on the INBOX and fires only while scheduling is on (TURN SCHEDULING ON). routine.create schedules one agent, not a line.

## Rules
- **Never report a line as working from its design.** Working means a test output, read by you, at every bay.
- **Quote station.layout's status and "how it runs" sentence as given.** Say so when routing is not live or starts are paused; one blocking error anywhere stops every line.
- **A bay never checks its own work.**
- Real test runs count against the LINE BUDGET; state the cost before asking for more than one.

## Done means
station.layout shows the line with no blockers and a last run on every step, the end-to-end job reached the OUTBOX, and the Commander saw that output before scheduling was turned on.

## Output
The build sheet, each bay's test result and cost, what changed after testing, and anything still blocking.

*Needs the ORCHESTRATOR (station.layout), which every run the Commander starts carries. The Commander builds, tests and schedules the line in REFIT.*
