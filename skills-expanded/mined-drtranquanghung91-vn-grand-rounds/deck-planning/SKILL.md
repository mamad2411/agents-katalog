---
name: deck-planning
description: Use when a confirmed brief exists for a medical presentation and the storyline, slide-by-slide outline or time budget has not been written or approved yet, or when an outline needs restructuring.
---

# Deck planning

## Overview

Turn `brief.md` into `plan.md`: one message per slide, in an order that answers the
audience's questions before they ask them. The plan is a contract. The builder builds what
it says, the researcher sources what it lists, and the user approves it before either
starts.

## Method

1. Write the **core message** from the brief as one sentence. Every slide must serve it or
   be cut.
2. Pick the recipe for the deck type in `recipes.md` and adapt it to the time budget:
   about one content slide per minute, title and closing not counted.
3. Write each slide's title as an **assertion**, a full sentence stating that slide's
   conclusion: "Recurrence-free survival improved from 70% to 82% at 24 months", not
   "Results". Section words alone are not titles.
4. For each slide choose the **visual** that carries the evidence, using
   `visual-grammar.md`. Text-only slides need a reason.
5. List the **claims** each slide needs (numbers, facts, recommendations) in words. These
   become the researcher's work list. Do not write numbers you have not sourced: write
   "HR for RFS with 95% CI" and let stage 4 fill it.
6. Put detail that the audience doesn't need to *see* in the speaker notes column, not on
   the slide.

## Output: `plan.md`

```markdown
# Plan: <title>
Core message: <one sentence>
Budget: <n> content slides for <m> minutes (+ title, closing)

| # | Assertion title | Visual | Claims needed | Notes for presenter | Time |
|---|-----------------|--------|---------------|---------------------|------|
| 1 | <title slide>   | title layout | – | opening line | 0:30 |
| 2 | … | trial schema (rebuilt SVG) | eligibility; arms and doses; randomisation ratio; primary endpoint | … | 1:00 |

Appendix / backup slides: <optional>
Open questions for the user: <only if any>
```

Then show the plan to the user and ask for approval in one line. Changes go back into
`plan.md`. Nothing downstream starts until the user says yes.

## Quality bar

- Titles read as a story when read alone, top to bottom.
- No two consecutive slides use the same visual type unless the content is a series.
- Every number the talk depends on appears in some slide's "Claims needed".
- Limitations, conflicts of interest and what is still unknown have a slide when the deck
  type is journal club, guideline update or conference.
- Case decks: the timeline comes before the discussion; teaching points are tied to
  references.
