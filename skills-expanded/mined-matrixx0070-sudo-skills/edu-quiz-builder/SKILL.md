---
name: edu-quiz-builder
version: 1.0.0
description: Build a quiz or assessment with an answer key, deliberate difficulty spread, and objective alignment.
author: matrixx0070
tags: [education, assessment, quiz, answer-key, difficulty]
capabilities: []
---

## When to use

Use this to create a graded or practice assessment: a set of items tied to objectives, with a full answer key and a controlled easy/medium/hard mix. Covers multiple choice, short answer, and problem items.

**Not for:** designing the grading criteria for open work (use edu-rubric-design), the whole course plan (use edu-curriculum-design), or a live tutoring dialogue (use edu-tutor-session).

## Method

1. Anchor to objectives. List the objectives being tested and how many items each gets. Decision point: if an objective has zero items, add one or drop it from scope.
2. Choose item types by cognitive level. Recall → MCQ/fill-in; application → problems; analysis → short answer or scenario. Match type to what you're measuring.
3. Set difficulty spread. Target a deliberate mix (default ~30% easy, 50% medium, 20% hard) and tag each item. Decision point: adjust the ratio for a diagnostic (more easy) vs. a mastery check (more hard).
4. Write items cleanly. One idea per item; for MCQ, make distractors plausible and reflect real misconceptions; avoid "all of the above" and grammar tells.
5. Build the answer key. Give the correct answer plus a one-line rationale for every item; for MCQ, note why each distractor is wrong where useful.
6. Review for fairness. Remove trick wording, double negatives, and cultural/prior-knowledge bias unrelated to the objective.

## Example

Objective: "Apply the order of operations." 5 items. Easy (MCQ): "3 + 4 × 2 = ?" → 11 (distractor 14 catches left-to-right error). Medium (problem): "Evaluate 2 × (5 − 3)² " → 8. Hard (short answer): "A student computed 6 ÷ 2 × 3 = 1. Find and explain their error." Key gives answers, the distractor rationale, and the misconception each hard item targets. Spread: 2 easy, 2 medium, 1 hard.

## Pitfalls

- All items at one difficulty, so the quiz can't separate mastery levels.
- MCQ distractors that are obviously wrong, letting learners guess correctly.
- No rationale in the key, making the quiz useless for feedback and reteaching.
- Testing reading tricks or trivia instead of the stated objective.

## Output format

```
Quiz: <topic> | Objectives tested: <list> | Items: <n>

Questions:
1. [Obj X | Easy | MCQ] <stem>
   a) ... b) ... c) ... d) ...

Answer key:
1. <answer> — <rationale; distractor notes>

Difficulty spread: Easy <n> / Medium <n> / Hard <n>
Coverage: <items per objective>
```
