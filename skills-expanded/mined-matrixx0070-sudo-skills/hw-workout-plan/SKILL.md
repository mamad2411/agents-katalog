---
name: hw-workout-plan
version: 1.0.0
description: Build a progressive, goal-appropriate workout plan matched to experience level using general fitness principles.
author: matrixx0070
tags: [fitness, workout, training, exercise, progression]
capabilities: []
---

This is general wellness information, not medical diagnosis or treatment. Consult a licensed healthcare professional before starting a new exercise program, especially with injuries, heart/joint conditions, pregnancy, or if you are new to intense exercise.

## When to use

Use this when someone states a training goal (strength, muscle, endurance, general fitness, fat loss), their experience level, available days/equipment, and wants a structured, progressive plan.

**Not for:** rehab or return-to-play after injury or surgery, sport-specific competitive programming for elite athletes, or anyone with acute pain or a flagged medical condition — refer to a physical therapist or physician.

## Method

1. Collect inputs: goal, experience (beginner/intermediate/advanced), days/week, equipment, session length, injuries/limitations.
2. Choose a split. Decision point: 2-3 days → full-body; 4 days → upper/lower; 5-6 days → push/pull/legs or body-part split.
3. Select movement patterns each session: squat, hinge, horizontal push/pull, vertical push/pull, carry/core. Prefer compounds first.
4. Set volume/intensity by goal: strength → lower reps (3-6), higher load; hypertrophy → 6-12 reps; endurance → 12-20+ reps. Beginners start at the low end of sets (2-3).
5. Decision point: if equipment or injury blocks a lift, substitute the same pattern (e.g., barbell squat → goblet squat or leg press).
6. Define progression: add reps within a range, then add load (double progression); include a lighter/deload week roughly every 4-6 weeks.
7. Add warm-up, mobility, and 48h between training the same muscle hard.

## Example

Goal: muscle, beginner, 3 days, dumbbells only, 45 min. Full-body A/B alternating. Day A: goblet squat 3x8-12, DB bench 3x8-12, one-arm row 3x8-12, RDL 3x8-12, plank 3x30s. Progression: hit top of range two sessions → add weight. Deload week 6.

## Pitfalls

- Copying an advanced split for a beginner — too much volume, poor recovery, burnout.
- No progression rule, so weights never change and gains stall.
- Skipping warm-ups and deloads, inviting overuse injury.
- Ignoring stated equipment/time — a gym program for someone with two dumbbells fails on day one.

## Output format

```
GOAL: <goal> | LEVEL: <level> | SPLIT: <split>, <days>/week
ASSUMPTIONS: <missing inputs / substitutions>

DAY <n> — <focus>
- <exercise>: <sets>x<reps>  (sub: <alt>)
- ...
Warm-up: <note> | Rest: <note>

PROGRESSION: <rule> | DELOAD: every <n> weeks
NOTE: General wellness info, not medical advice — clear new programs with a clinician if you have any condition or injury.
```
