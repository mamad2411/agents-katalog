---
name: lawstu-bar-prep-questions
version: 1.0.0
description: Drill bar-style questions — MBE multiple choice and essay prompts with structured feedback on why each distractor is wrong.
author: matrixx0070
tags: [law-student, bar-exam, mbe, essays, practice-questions]
capabilities: []
---

## When to use

Reach for this during bar review, or 2L/3L, when you want reps on MBE-format multiple choice and MEE/essay prompts. The skill poses questions in bar format, then — after you answer — explains the call, why the right choice wins, and why each distractor is engineered to tempt you.

**Not for:** taking the actual bar exam or any proctored assessment (that would be misconduct). It is a *practice* drill: you answer first, feedback follows. It will not sit an exam for you. Not for open reasoning drills (see `lawstu-socratic-drill`) or timed issue simulation (see `lawstu-exam-forecast`).

## Method

1. **Pick subject and format.** MBE (7 subjects) or essay/MEE. Decision point: drill your weakest MBE subject by percentage, not by comfort.
2. **Answer before feedback.** Commit to a letter or write the essay skeleton first — no peeking.
3. **Get the full explanation.** The skill states the tested rule, why the correct answer applies, and a one-line reason each wrong option fails (misstated rule, wrong element, right rule/wrong facts).
4. **Log the miss pattern.** Track *why* you missed — rule gap, misread call, or trap distractor. Decision point: three misses on one rule → back to `lawstu-flashcards`.
5. **Time your reps.** MBE budget ≈ 1.8 min/question; essays on the real clock.
6. **Cycle by subject** until per-subject accuracy clears your target.

## Example

MBE on the parol evidence rule. You pick the answer that "sounds most lawyerly." Feedback: correct choice turns on the writing being *fully* integrated; your pick applied the rule to a partially integrated contract (right rule, wrong trigger fact) — the classic distractor. You log it under "integration triggers."

## Pitfalls

- Reading the explanation before committing — kills the diagnostic signal.
- Grading only right/wrong, never the *why* behind the miss.
- Drilling strong subjects because they feel good.
- Untimed practice that collapses under real exam pace.

## Output format

```
Subject | format (MBE/essay) | timed?
Q: [stem + call]
Your answer: [committed first]
Feedback:
  correct: [letter] — [tested rule]
  distractors: A/B/C/D — why each fails
Miss log: rule gap | misread call | trap distractor
Accuracy this set: __/__
```

## Reference

- **Bar-exam frameworks:** MBE (200 MC, 7 subjects), MEE (essays), MPT (skills task); UBE aggregates them.
- **IRAC** governs essay scoring — issue-spotting breadth plus two-sided application (`lawstu-irac-practice`).
- **Case-brief / outline** rule banks are the raw material bar questions test (`lawstu-outline-builder`).
