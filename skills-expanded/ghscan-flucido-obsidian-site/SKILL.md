---
title: Skill — Evening Reflection
created: 2026-07-10
updated: 2026-07-10
type: skill
tags: [shared, agents, skill, daily, evening]
loads_by: orchestrator
---

# Skill: Evening Reflection

> Reconcile the day's work, populate end-of-day state transfer, and sync state
> for next-morning pickup. MANDATORY — skipping creates context debt.

## When to Use

Every business day, at the end of the session.

## Inputs

- Today's `Daily/YYYY-MM-DD.md` (start with the morning plan)
- `Work/LTC/pipeline.md`, `Work/WFC/pipeline.md` (current state)
- `Work/Shared/Ops/morning-standup.md` (today's priorities)
- Any artifacts created/modified today (grep for today's date in `log.md`)

## Outputs

- EOD state transfer goes to `Work/Shared/Ops/evening-reflection.md` only — the daily note is a morning sprint and does NOT get an EOD section (per [[Work/Shared/Ops/templates/daily-note]] sprint format)
- Updated `Work/Shared/Ops/evening-reflection.md` (today's entry)
- Updated `MEMORY.md` (date bumped, decisions added, risk register refreshed)
- Updated `Work/Shared/master-priority-queue.md` if major stage movement
- Append entries to `log.md` for file changes
- Append to `Work/Shared/Ops/issues-fixes-log.md` if any errors or near-misses
- Evening wrap-up (in-session summary; email if Gmail available)

## Process

### Step 1: Reconcile (5 min)
- [ ] Compare completed vs. planned actions from today's morning note
- [ ] Mark each item: completed / partial / slipped
- [ ] Note items started but not finished (with new target date)

### Step 2: Populate EOD entry in evening-reflection dashboard (10 min)
Fill in `Work/Shared/Ops/evening-reflection.md` for today. **The daily note does NOT get an EOD section** — it's a morning sprint only. Tomorrow's §1 ("What did we do yesterday?") pulls from this entry. Use the standard EOD structure:
- **Completed Today** — concrete list with file paths
- **Carrying Forward** — explicit owner + next action + new due date
- **Tomorrow's First Attention** — top 3 items for next-day pickup
- **Key Decisions** — anything that changed trajectory
- **Corrections / Notes** — anything Frank or another agent should know

### Step 3: Populate evening-reflection dashboard (5 min)
Fill in `Work/Shared/Ops/evening-reflection.md`:
- **What Shipped Today** (table: org, item, outcome, confidence)
- **What Slipped** (table: org, item, reason, new target)
- **Pipeline Movement** (any stage changes today)
- **Wins** (concrete, with file:line or evidence)
- **Learnings** (one or two, with prevention rules)
- **Metrics Snapshot** (today vs. session total)
- **Tomorrow's First Attention** (table: priority, org, item, why first)
- **State Transfer Notes** (handoff to next session)
- **Shutdown Checklist** (what got done, what didn't)
- **Incidents** (any new entries for `issues-fixes-log.md`)

### Step 4: Roll forward (5 min)
- [ ] For every incomplete item: assign explicit owner and next action
- [ ] Set or update due dates
- [ ] Add to tomorrow's priority candidate list
- [ ] Carry any HIGH risks to next-day first-attention

### Step 5: Sync state (5 min)
- [ ] Update MEMORY.md (Current State, Latest Decisions, Risk Register)
- [ ] Append to `log.md` for every file changed
- [ ] Append to `issues-fixes-log.md` if any incidents
- [ ] Verify all daily note sections complete (no "TODO" placeholders left)

### Step 6: Close (2 min)
- [ ] Log shutdown completion
- [ ] Preview tomorrow's top 3 outcomes (in-session)
- [ ] Note anything Frank should see first thing

### Step 7: Publish wrap-up (2 min)
- [ ] If Gmail API available: send evening wrap-up
  - Subject: `Evening Wrap-Up — [WEEKDAY] [M/D]`
  - Body: full daily note (plain text) + EOD state transfer
- [ ] If Gmail blocked: present in-session summary

## Validation

- [ ] EOD state transfer fully populated (no empty fields)
- [ ] evening-reflection.md entry for today
- [ ] MEMORY.md date bumped
- [ ] log.md updated for today's changes
- [ ] No silent carry-forward — every slipped item has explicit owner + new due date

## Mandatory (Hard Rule)

**Do not skip the EOD state transfer.** It is the single source of truth for
next-morning pickup. Skipping creates "context debt" — the next morning's session
will not know where Frank left off.

## Common Failures to Avoid

- **Silent completion** — claim an item done without evidence. If it ran in
  user-time and is unconfirmed, say "unknown — Frank to confirm."
- **Date confusion** — make sure EOD date = today's date, not yesterday's.
- **Skipping the rollover** — every slipped item MUST get a new due date.
- **Forgetting the log** — every file write needs a `log.md` entry.
- **Leaving EOD placeholders empty** — they get filled NOW, not tomorrow.
