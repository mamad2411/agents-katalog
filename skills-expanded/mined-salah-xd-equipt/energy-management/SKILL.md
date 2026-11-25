---
name: energy-management
description: "Maps energy levels to task types for optimized daily scheduling with peak performance time blocks and recovery periods."
allowed-tools: Read Write Glob
metadata:
  author: Salah-XD
  version: "1.0"
---

# Energy Management

## When to Use This Skill

Use this skill when you need to:
- Map personal energy patterns to optimize when you do which tasks
- Design a daily schedule based on energy levels rather than arbitrary time slots
- Identify energy drains and build recovery rituals into the workday
- Maximize output without burnout by working WITH your biology

**DO NOT** use this skill for morning routines (use morning-routine-builder), task prioritization, or health/wellness planning. This is for aligning work tasks with natural energy cycles.

---

## Core Principle

TIME MANAGEMENT IS A LIE — YOU CANNOT MANAGE TIME, ONLY ENERGY. MATCHING HIGH-ENERGY TASKS TO HIGH-ENERGY WINDOWS MULTIPLIES OUTPUT WITHOUT ADDING HOURS.

---

## Phase 1: Energy Audit

Map the user's natural energy patterns.

### Required Inputs

| Input | What to Ask | Default |
|-------|------------|---------|
| **Wake time** | "What time do you typically wake up?" | 6:30 AM |
| **Work hours** | "What are your typical work hours?" | 8 AM - 6 PM |
| **Peak time** | "When do you feel most alert and focused?" | Mid-morning |
| **Crash time** | "When do you hit an energy low?" | After lunch |
| **Task types** | "List your main work activities (creative, analytical, admin, calls, etc.)" | No default |
| **Current pain** | "When do you feel least productive?" | Afternoon |

### Energy Mapping Exercise

Ask the user to rate energy levels 1-5 for each 2-hour block:

```
## Energy Map

| Time Block | Energy (1-5) | Current Task Type | Ideal Task Type |
|-----------|-------------|------------------|-----------------|
| 6-8 AM | [X] | [What they do now] | [What they should do] |
| 8-10 AM | [X] | [Current] | [Ideal] |
| 10 AM-12 PM | [X] | [Current] | [Ideal] |
| 12-2 PM | [X] | [Current] | [Ideal] |
| 2-4 PM | [X] | [Current] | [Ideal] |
| 4-6 PM | [X] | [Current] | [Ideal] |
```

**GATE: Confirm energy map before designing the optimized schedule.**

---

## Phase 2: Task-Energy Matching

Categorize tasks by energy requirement and match to energy windows.

### Task Energy Categories

```
## Task Classification

### Peak Energy Tasks (Energy 4-5 required)
- Strategic thinking and planning
- Creative work (writing, designing, building)
- Complex problem solving
- Important client conversations
- Learning new skills

### Moderate Energy Tasks (Energy 2-3 required)
- Client calls and meetings
- Collaboration and feedback
- Research and analysis
- Project management
- Decision-making

### Low Energy Tasks (Energy 1-2 sufficient)
- Email and inbox processing
- Administrative tasks
- Data entry and filing
- Social media scheduling
- Routine follow-ups
```

### Optimized Schedule Template

```
## Energy-Optimized Daily Schedule

| Time | Energy Level | Task Category | Specific Tasks |
|------|-------------|--------------|----------------|
| [Peak window] | HIGH (4-5) | Creative / Strategic | [User's highest-value tasks] |
| [Moderate window] | MODERATE (3) | Collaborative / Analytical | [Meetings, calls, reviews] |
| [Low window] | LOW (1-2) | Administrative / Routine | [Email, admin, scheduling] |
| [Recovery window] | RECHARGE | Break / Movement | [Walk, rest, nourishment] |
```

**GATE: Present the optimized schedule for feedback.**

---

## Phase 3: Energy Protection

Build systems to protect peak energy and manage dips.

### Energy Drains to Eliminate

Help the user identify and address common energy killers:

```
## Energy Drain Audit

| Drain | Impact (1-5) | Solution |
|-------|-------------|----------|
| Checking email first thing | [X] | Delay email until after peak work block |
| Back-to-back meetings | [X] | Insert 15-min buffers between meetings |
| Decision fatigue | [X] | Batch decisions, create defaults for recurring choices |
| Context switching | [X] | Batch similar tasks, use time blocks |
| Poor nutrition/hydration | [X] | Prep snacks, set water reminders |
| No breaks | [X] | Schedule 10-min breaks every 90 minutes |
```

### Recovery Rituals

Design 3-5 minute recovery activities between energy blocks:
- 5-minute walk (physical reset)
- Breathing exercise (nervous system reset)
- Hydration + snack (fuel reset)
- Music or silence (sensory reset)

### Peak Protection Rules

- No meetings during peak energy windows
- Phone on do-not-disturb during creative blocks
- Email and Slack closed during deep work
- "Office hours" for questions — do not be available all day

---

## Phase 4: Sustain

Build long-term energy management habits.

### Weekly Energy Review

5 questions to ask every Sunday:

1. Which days did I feel most productive? What was different?
2. Did I protect my peak energy windows this week?
3. What drained my energy the most?
4. Did I take enough recovery breaks?
5. What adjustment do I need for next week?

### Seasonal Adjustments

Energy patterns shift with seasons, workload, and life changes:
- Re-map energy levels quarterly
- Adjust schedules during high-stress periods (launch weeks, tax season)
- Accept that some weeks will be low-energy — reduce expectations, do not push through

### Energy Score Tracker

```
## Weekly Energy Score

| Day | Morning | Midday | Afternoon | Evening | Overall |
|-----|---------|--------|-----------|---------|---------|
| Mon | [1-5] | [1-5] | [1-5] | [1-5] | [Avg] |
```

Track for 2 weeks to validate the energy map and refine the schedule.

---

## Anti-Patterns

- **Scheduling creative work during energy lows** — you cannot force creativity at 3 PM if your brain peaks at 9 AM.
- **No recovery time** — running at peak energy all day leads to burnout. Build in recharge blocks.
- **Fighting your biology** — if you are not a morning person, do not force a 5 AM creative block. Work with your rhythm.
- **Ignoring energy data** — tracking energy for a week gives you actionable data. Guessing gives you a bad schedule.
- **Packing every minute** — the best schedule has white space. Over-optimization creates rigidity.

---

## Recovery

- **User's energy is low all day:** Check sleep, nutrition, exercise, and stress levels first. No schedule optimization fixes chronic exhaustion.
- **User cannot protect peak time (meetings scheduled by others):** Block peak hours on the calendar as "Focus Time" before others can book them.
- **User's energy pattern is unpredictable:** Use a flexible system — do the highest-energy task available whenever a high-energy window opens, rather than a fixed schedule.
- **User pushes through energy dips:** Reframe breaks as productivity tools, not laziness. A 10-minute break at 2 PM produces better output at 2:30 than powering through.
- **User does not believe in energy management:** Track for 5 days. The data will show productivity differences between peak and low windows.
