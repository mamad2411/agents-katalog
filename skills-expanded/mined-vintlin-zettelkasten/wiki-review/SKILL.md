---
name: wiki-review
description: Review unresolved items emitted by `wiki-generation` and convert them into concrete next actions.
---

# Wiki Review

Use this skill for unresolved generation items and for explicit review tasks about theme concepts, argument boundaries, or entrance-note shape.
Do not use it for routine uncertainty or whole-repo auditing.
When the task is about a theme concept or a possible new parent question, use `wiki-rank` first, then use this skill to decide the structural move.

## Read First

- `references/review-rules.md`

## Input And Output

- Input: review blocks, usually from `outputs/processing/<source-id>-report.md`
- Output: actionable review results in the format defined by `references/review-rules.md`

## Workflow

1. Read the review blocks.
   Inspect only the affected notes and the minimum extra context needed to decide.
   If the user is reviewing a theme concept rather than a generation leftover, inspect the theme note, the directly related argument notes, and only the minimum permanent notes needed to understand the concept.

2. Confirm the issue is still real.
   Drop items that are already resolved or have no workflow impact.

3. Classify and decide.
   For each valid item:
   - classify the issue
   - decide the next action
   - name the affected files
   - state the reason briefly

   For theme / argument review, first reduce the concept, then decide structure:
   - what is the concept behind this theme or proposed new theme
   - what are its irreducible generators
   - how is it different from adjacent existing themes or parent questions
   - what boundary naturally follows from that concept explanation
   - what argument range belongs inside that boundary, and what should stay outside

   Then stress-test the resulting structure with four short questions:
   - generation: can this theme or argument still regenerate the notes beneath it, or has it become a loose bucket?
   - minimality: if two adjacent arguments were merged, would anything important actually be lost?
   - independence: can two arguments vary independently in real cases, or are they mostly the same generator in different words?
   - predictive coverage: does this parent help place new notes cleanly, or does every new note still require ad hoc judgment?

   Use these checks only to sharpen the decision. Do not turn review output into a long essay or ranking writeup.

4. Output actionable results.
   Make the next move explicit: update, create, defer, or ask for judgment.

## Hard Rules

- Do not turn open-ended curiosity into review work.
- Do not expand into repository-wide linting.
- Keep outputs concrete enough for the next agent to act without reinterpretation.

## Scope Boundary

- Use `wiki-review` for unresolved generation leftovers.
- Use `wiki-links` for broader repository inspection.
