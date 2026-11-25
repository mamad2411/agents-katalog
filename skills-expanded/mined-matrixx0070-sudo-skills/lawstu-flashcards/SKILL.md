---
name: lawstu-flashcards
version: 1.0.0
description: Build active-recall flashcards for rules, elements, and case holdings — atomic cards with clean prompts for spaced repetition.
author: matrixx0070
tags: [law-student, flashcards, active-recall, spaced-repetition, memorization]
capabilities: []
---

## When to use

Reach for this when you need durable recall of black-letter rules, element lists, exceptions, and key holdings. The skill turns your outline and briefs into atomic, one-fact cards you can drill in any spaced-repetition system.

**Not for:** conceptual understanding or application skill (use `lawstu-socratic-drill` and `lawstu-irac-practice` — flashcards memorize, they do not teach reasoning). It builds study cards from material *you* provide; it will not generate answers to graded assignments. Not for building the outline itself (see `lawstu-outline-builder`).

## Method

1. **Source from your own outline.** Cards are only as good as the rules you have already synthesized. Decision point: if a rule is fuzzy in your outline, fix it there first — do not memorize a wrong card.
2. **Make each card atomic** — one fact, one prompt. Split multi-element rules into a "name the elements" card plus one card per tricky element.
3. **Prefer active prompts.** "Elements of adverse possession?" beats "Adverse possession is…". Front asks, back answers tersely.
4. **Add cloze deletions** for element lists and thresholds ("Statute of Frauds covers contracts over $___").
5. **Tag by course and doctrine** so you can drill a single topic before its exam.
6. **Include a case-holding deck** — front: case name + one-line facts; back: holding + rule. Keep holdings to one sentence.

## Example

Rule card — Front: "Hearsay definition (FRE 801)?" Back: "Out-of-court statement offered to prove the truth of the matter asserted." Then a cloze: "Hearsay is inadmissible unless ___ (an exception applies)." Then an application-adjacent card: "Statement offered only to show notice — hearsay? → No, not for its truth."

## Pitfalls

- Overloaded cards (a whole doctrine on one back) — you memorize the shape, not the content.
- Verbatim casebook prose that you recognize but cannot produce.
- No application cards, so you know rules but freeze on facts.
- Never re-drilling; recall decays without spaced review.

## Output format

```
Course | doctrine tag
Rule cards:
  Q: [active prompt] | A: [terse rule]
Cloze cards:
  [sentence with ___ blanks]
Case-holding deck:
  Front: case + 1-line facts | Back: holding + rule
Drill schedule: today / +1d / +3d / +7d
```

## Reference

- **Case-brief format** feeds the holding deck (`lawstu-case-brief`).
- **IRAC:** flashcards fortify the Rule element of IRAC; pair with application drills.
- **Bar framing:** element and exception cards map onto MBE-tested rules; a course deck extends into a bar deck (`lawstu-bar-prep-questions`).
