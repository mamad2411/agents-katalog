---
name: weekly-planning-workflow
description: 4-step (of a 7-step series) structured weekly planning methodology — connects Google Calendar first, brain-dumps everything, asks Claude to ask questions before planning, then requests specific time-blocked calendar blocks with buffers
---

# Weekly Planning with Claude

A structured approach to turning a messy brain dump into a real, time-blocked weekly plan. Captured from a 7-step carousel series; steps 1–4 are documented here (steps 5–7 were not visible in the source batch).

## The 4-Step Workflow

### Step 1 — Connect and Verify Calendar Access
Before typing any planning prompt, connect Google Calendar and verify Claude can actually read this week's events. A plan built on incomplete calendar data will double-book or miss conflicts.

### Step 2 — Brain Dump Everything
Write every deadline, half-finished task, and lingering commitment in one long, messy paragraph. Don't organize yet — the mess is the input. Include:
- Hard deadlines
- Work-in-progress items
- Commitments that have been postponed
- Anything uncertain or half-committed

### Step 3 — Ask Claude to Ask Questions First
Before Claude produces any plan, explicitly tell it to ask you questions. Force it to surface:
- Your energy levels for the week (which days are high/medium/low)
- Hard deadlines that cannot move
- What genuinely cannot be rescheduled
- What's optional vs. required

Don't let Claude jump to a plan before surfacing constraints — the questions reveal what the plan has to work around.

### Step 4 — Request Real Calendar Blocks
Ask for actual calendar blocks with:
- Specific start time (e.g. "9:00 AM", not "morning")
- Specific finish time
- Buffer time between blocks (e.g. 15 minutes minimum)

Vague time slots are not a plan. Require specificity before accepting the output.

## Prompts (copy-paste)

**Step 1:**
Connect Google Calendar and verify you can see my events for this week before I give you any planning prompt.

**Step 2:**
Here is everything I'm carrying this week: [brain dump — one long paragraph, no organizing yet]

**Step 3:**
Before you make any plan, ask me questions. Surface my energy levels for each day, any hard deadlines that cannot move, and what is optional vs. required.

**Step 4:**
Now give me a calendar plan with specific start and finish times for each block, and at least 15 minutes of buffer between blocks.

## Related skills

- `advisory-board` — sanity-check week priorities against a personal board of advisors
- `night-shift-workflow` — for recurring tasks that run unattended during off-hours
- `quarterly-okr-architect` — for ensuring the week's blocks serve quarterly goals
- `overwhelm-to-action-prompts` — companion prompts for when the brain dump itself is overwhelming
