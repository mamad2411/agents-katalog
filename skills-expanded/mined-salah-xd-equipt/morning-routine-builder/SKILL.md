---
name: morning-routine-builder
description: "Designs personalized morning routines for entrepreneurs with time blocks, habits, and productivity triggers tailored to energy levels and business goals."
allowed-tools: Read Write Glob
metadata:
  author: Salah-XD
  version: "1.0"
---

# Morning Routine Builder

## When to Use This Skill

Use this skill when you need to:
- Design a structured morning routine optimized for entrepreneurial productivity
- Map habits and rituals to specific time blocks based on energy science
- Build a repeatable morning system that supports business and personal goals
- Reset a broken morning routine that is costing you focus and output

**DO NOT** use this skill for full daily scheduling, evening routines, or general time management. This is specifically for the first 1-3 hours after waking.

---

## Core Principle

A MORNING ROUTINE IS NOT A WISHLIST OF HABITS — IT IS A SEQUENCED SYSTEM WHERE EACH BLOCK PRIMES THE NEXT, BUILDING MOMENTUM TOWARD YOUR MOST IMPORTANT WORK.

---

## Phase 1: Assessment

Before designing anything, gather the inputs that shape the routine. No assessment, no routine.

### Required Inputs

Ask the user for each of these. If they do not provide one, use the default.

| Input | What to Ask | Default |
|-------|------------|---------|
| **Wake time** | "What time do you wake up (or want to wake up)?" | 6:00 AM |
| **First obligation** | "What time does your first meeting, commitment, or work block start?" | 9:00 AM |
| **Top business goal** | "What is your #1 business priority right now?" | Revenue growth |
| **Energy pattern** | "Are you sharpest immediately after waking, or do you need 30-60 min to ramp up?" | Ramp-up needed |
| **Current routine** | "Describe what you currently do in the first 2 hours after waking." | No consistent routine |
| **Non-negotiables** | "Any habits you MUST keep (coffee ritual, kids' school drop-off, exercise)?" | None specified |

**GATE: Present the assessment summary and get confirmation before designing the routine.**

---

## Phase 2: Design

Build the routine using time blocks that follow circadian and productivity science.

### Block Categories

Every morning routine draws from these five categories. Not all are required — sequence depends on the user's profile.

1. **Priming Block (5-15 min)** — hydration, light exposure, breathwork, or journaling to shift from sleep to alert state
2. **Movement Block (15-45 min)** — exercise, stretching, or walking to elevate energy baseline
3. **Focus Block (30-90 min)** — deep work on the most important business task before distractions arrive
4. **Learning Block (10-30 min)** — reading, podcast, or skill development
5. **Admin Block (10-20 min)** — inbox triage, daily planning, reviewing priorities

### Sequencing Rules

- Priming ALWAYS comes first — never start with email or social media
- Focus Block should land during the user's peak alertness window
- Movement before Focus if the user needs ramp-up time; Movement after Focus if they wake sharp
- Admin Block is ALWAYS last — it is a transition to the workday, not a morning activity
- Build in 5-minute buffers between blocks for transitions

### Routine Template

Present the designed routine in this format:

```
## Your Morning Routine

**Wake:** 6:00 AM
**Routine ends:** 8:30 AM
**Total routine time:** 2 hours 30 minutes

| Time | Block | Activity | Duration | Why |
|------|-------|----------|----------|-----|
| 6:00 | Priming | Glass of water + 5 min journaling | 15 min | Hydration and mental clarity |
| 6:15 | Movement | 30-min run or bodyweight workout | 30 min | Energy baseline elevation |
| 6:45 | Buffer | Shower + get ready | 15 min | Transition |
| 7:00 | Focus | Deep work on [top priority] | 60 min | Highest-value task in peak window |
| 8:00 | Learning | Read industry book (20 pages) | 20 min | Compound knowledge growth |
| 8:20 | Admin | Review calendar + triage inbox | 10 min | Transition to workday |
```

**GATE: Present the routine and wait for user feedback before finalizing.**

---

## Phase 3: Reinforcement

After the routine is approved, provide implementation support.

### Habit Triggers

For each block, define a specific trigger that initiates the habit:

- **Environmental trigger:** Place water bottle on nightstand (Priming)
- **Completion trigger:** "After I finish my workout, I immediately sit at my desk" (Movement → Focus)
- **Time trigger:** Phone alarm labeled with the block name

### Accountability System

Provide a simple 7-day tracking template:

```
## Week 1 Tracker

| Day | Priming | Movement | Focus | Learning | Admin | Notes |
|-----|---------|----------|-------|----------|-------|-------|
| Mon | [ ] | [ ] | [ ] | [ ] | [ ] | |
| Tue | [ ] | [ ] | [ ] | [ ] | [ ] | |
...
```

### Ramp-Up Plan

If the routine is a big change, provide a phased approach:
- **Week 1:** Implement Priming + one other block only
- **Week 2:** Add the Focus Block
- **Week 3:** Full routine
- **Week 4:** Evaluate and adjust timing

---

## Phase 4: Optimize

Deliver final refinements and long-term sustainability guidance.

### Weekend Variation

Design a modified weekend version that keeps momentum without rigidity. Typically: same Priming block, flexible timing on everything else, Focus Block becomes optional.

### Red Flags to Watch

- If the routine takes longer than 3 hours, it will collapse — cut blocks
- If the Focus Block keeps getting skipped, it is in the wrong time slot
- If the user dreads the routine, remove the block they resist most and add it back later

### Quarterly Review Prompt

Provide 5 questions for the user to reassess the routine every 90 days based on changing business priorities and energy patterns.

---

## Anti-Patterns

- **Overloading the routine** — cramming 10 habits into 90 minutes guarantees failure. Maximum 5 blocks.
- **Starting with email** — checking inbox first surrenders your agenda to other people's priorities.
- **Copying someone else's routine** — what works for a CEO with a chef and no kids will not work for a solopreneur with school drop-off.
- **No triggers** — habits without environmental or completion triggers rely on willpower, which depletes.
- **Rigid weekends** — forcing the same routine 7 days a week causes burnout and rebellion.

---

## Recovery

- **User has no morning time:** Compress to a 20-minute micro-routine: 5 min priming, 15 min focus. Something beats nothing.
- **User tried routines before and quit:** Ask what broke. Design around the failure point, not despite it.
- **User works night shifts:** Reframe as "first 2 hours after waking" regardless of clock time. Same principles apply.
- **User cannot wake earlier:** Do not push wake time. Work with the time between waking and first obligation.
- **User has young children:** Build routine around kid-dependent windows. Priming during feeding, Focus during nap or before kids wake.
