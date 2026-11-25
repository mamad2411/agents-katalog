---
name: edu-lesson-plan
version: 1.0.0
description: Write a single lesson plan with objectives, timed activities, materials, and an aligned assessment.
author: matrixx0070
tags: [education, lesson-plan, instruction, activities, assessment]
capabilities: []
---

## When to use

Use this to plan one class session or self-study block: what learners will achieve, the minute-by-minute flow of activities, and how you check they got it. Works for classroom, one-on-one, or async lessons.

**Not for:** designing a whole course sequence (use edu-curriculum-design), building a standalone quiz (use edu-quiz-builder), or a live adaptive tutoring conversation (use edu-tutor-session).

## Method

1. Set the objective. Write 1-3 measurable objectives for this session only — what learners can do by the end. Decision point: if you have more than 3, the lesson is overloaded; cut or split.
2. Hook. Plan a 2-5 minute opener that activates prior knowledge or creates a question worth answering.
3. Instruction (I do). Present the new concept with a worked example. Keep direct instruction short — chunk it.
4. Guided practice (we do). Learners try with support; you circulate and correct. Decision point: if most struggle, reteach before moving on.
5. Independent practice (you do). Learners apply it alone.
6. Assessment / exit check. A quick check aligned to each objective (exit ticket, one problem, thumbs). This is the proof, not a vibe.
7. Time-box. Assign minutes to every step; ensure they sum to the session length. Add a differentiation note (support + stretch).

## Example

Topic: fractions equivalence, 45 min, grade 5. Objective: "Generate equivalent fractions by multiplying numerator and denominator." Hook (5): "Is 1/2 the same as 2/4? Prove it with a pizza drawing." I do (10): model 1/2 = 2/4 = 3/6. We do (12): class solves 3 together. You do (13): 6 problems solo. Exit ticket (5): "Write two fractions equal to 3/4." Stretch: simplify back down. Support: fraction tiles provided.

## Pitfalls

- Objectives too broad to check in one session ("understand fractions").
- Front-loading long lecture with no practice, so misconceptions surface too late.
- Skipping the exit check, so you assume learning happened without evidence.
- Activities whose minutes don't sum to the session length — the plan overruns.

## Output format

```
Lesson: <topic> | Level: <...> | Duration: <n min>

Objectives (measurable): 1. ...
Materials: <...>

Timed flow:
| Min | Segment | Activity | Purpose |
| 5   | Hook    | ...      | ...     |

Assessment / exit check: <aligned to each objective>
Differentiation: Support: <...> | Stretch: <...>
```
