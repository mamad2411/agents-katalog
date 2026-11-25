---
name: lawstu-study-plan
version: 1.0.0
description: Build a realistic semester or bar-review study plan — backward-planned from exams, balanced across courses, with spaced review baked in.
author: matrixx0070
tags: [law-student, study-plan, scheduling, time-management, spaced-repetition]
capabilities: []
---

## When to use

Reach for this at the start of a semester or bar-review cycle when you need a week-by-week plan that survives contact with reality — reading, briefing, outlining, and practice spread so nothing piles up in finals week. The skill builds the schedule with you around your real constraints.

**Not for:** doing the studying itself, or forecasting specific exam issues (see `lawstu-exam-forecast`). It plans; it does not complete assignments or write anything you submit. Not for a single study session's agenda (see `lawstu-session`).

## Method

1. **Set the anchors.** List every exam/assignment deadline and work backward. Decision point: fixed dates dominate; build the plan around them, not around wishful weekly totals.
2. **Inventory the load.** Courses, weekly reading pages, and your realistic available hours (job, commute, life). Be honest — an over-packed plan fails week two.
3. **Layer the phases.** Weeks 1-10: read + brief + rolling outline. Weeks 11-13: outline compression + practice questions. Finals: timed simulation + spaced review.
4. **Balance across courses.** Rotate so no single course starves; heavier-credit or weaker subjects get more blocks.
5. **Bake in spaced review.** Schedule flashcard/recall sessions at expanding intervals, not one cram block.
6. **Add slack and a weekly review.** One buffer block per week and a Sunday reset to re-plan from actuals.

## Example

Four courses, finals in a two-week window. Backward plan: outlines *done* by T-14, so weeks 11-13 are pure practice. Contracts (your weakest) gets two blocks weekly to others' one. Every Sunday you compare planned vs. actual and shift the buffer block to whatever slipped — the plan bends instead of breaking.

## Pitfalls

- Front-loading nothing and cramming outlines into finals week.
- Planning peak-motivation hours you never actually have.
- No spaced review, so recall decays before the exam.
- A rigid plan with no buffer; one bad week cascades.

## Output format

```
Term/cycle | anchors (all deadlines)
Weekly capacity: __ realistic hours
Phase map:
  wks 1-10: read/brief/outline
  wks 11-13: compress + practice
  finals: simulate + spaced review
Per-course allocation: [blocks/week, weighted]
Spaced-review schedule: intervals
Weekly buffer + Sunday review:
```

## Reference

- **Backward planning:** anchor on exam dates; outlines complete before practice phase.
- **Spaced repetition** pairs with `lawstu-flashcards` for durable recall.
- **Bar framing:** the same phase structure scales to a 8-10 week bar-review calendar (`lawstu-bar-prep-questions`).
