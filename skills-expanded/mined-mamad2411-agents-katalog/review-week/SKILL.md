---
name: review-week
description: End of week review and scoring
---

# Weekly Review Skill

Score the week, identify patterns, log history. Run Friday afternoon or Sunday before planning the next week.

## Commands

- `/review-week` — Review and score the week

## Setup

Reads the same memory files as `/plan-week`. See [`plan-week/SETUP.md`](../plan-week/SETUP.md) for setup.

---

## Workflow

### Step 1: Load Context

Read:
- `weekly-plan.md` — this week's tasks and priorities
- `weekly-history.md` — prior weeks (for trend analysis)
- `career-strategy.md` — current strategic priorities

### Step 2: Score the Week

- Count completed `[x]` vs total tasks per priority level
- Calculate overall completion percentage
- Score each priority: P1 %, P2 %, P3 %

### Step 3: Ask for Task Updates

Present unchecked tasks and ask:
> "These are still unchecked. Which actually got done? Which should carry forward? Which should we drop?"

Update checkboxes based on answers.

### Step 4: Analyze Patterns

If `weekly-history.md` has prior weeks:
- Completion trend (improving? declining?)
- Which priority level gets neglected most
- Are carry-forwards becoming chronic?
- Overcommitment signal — planning 15, finishing 8?

### Step 5: Anti-Procrastination Flags

- **P1 hit rate < 80%** — flag prominently
- **Same task 3+ weeks as carry-forward** — stale task alert
- **Overcommitment** — if consistently completing < 60%, suggest planning fewer tasks next week

### Step 6: Update Files

Fill in the "End of Week Score" section of `weekly-plan.md`:
```
- P1 completion: X/Y tasks
- P2 completion: X/Y tasks
- P3 completion: X/Y tasks
- Overall: Z%
```

Append a summary block to `weekly-history.md`:
```markdown
## Week of [Date Range]
- **Focus:** [week focus statement]
- **Planned:** X tasks across Y priorities
- **Completed:** X/Y (Z%)
- **P1 hit rate:** X/Y (Z%)
- **Key wins:** [1-2 bullets]
- **Missed:** [what didn't get done and why]
- **Carry forward:** [tasks moving to next week]
```

### Step 7: Seed Next Week

Ask: "Any early thoughts for next week's priorities?" and note them.

### Step 8: Present Scorecard

```
WEEK SCORECARD: [Date Range]
P1: 3/3 (100%)  ||||||||||
P2: 2/3 (67%)   |||||||
P3: 1/2 (50%)   |||||
Overall: 6/8 (75%)

Trend: [up/down/flat] from last week (was X%)
```

Be honest. Don't sugarcoat a bad week. The point is signal, not comfort.
