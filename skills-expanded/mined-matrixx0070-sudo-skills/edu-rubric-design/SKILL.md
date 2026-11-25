---
name: edu-rubric-design
version: 1.0.0
description: Design a grading rubric with clear criteria and distinct performance-level descriptors.
author: matrixx0070
tags: [education, rubric, grading, assessment, criteria]
capabilities: []
---

## When to use

Use this to build a rubric for grading open-ended work — essays, projects, presentations, code — where you need consistent, defensible scoring across submissions or graders. Produces criteria rows and level descriptors that make "good" observable.

**Not for:** auto-scored quizzes with fixed answers (use edu-quiz-builder), the assignment prompt itself, or planning the lesson (use edu-lesson-plan).

## Method

1. Anchor to objectives. List what the task is meant to demonstrate; each criterion must trace to an objective. Decision point: drop any criterion that grades effort or neatness unrelated to the objective.
2. Choose criteria. Pick 3-6 distinct, non-overlapping dimensions (e.g., thesis, evidence, structure, mechanics). Merge overlapping ones.
3. Choose the scale. Set performance levels (default 4: Exemplary / Proficient / Developing / Beginning). Decide analytic (score each criterion) vs. holistic (one overall judgment); default analytic for feedback value.
4. Write level descriptors. For each criterion × level, describe observable evidence, not adjectives. "Cites 3+ relevant sources" beats "good use of sources." Descriptors must be mutually exclusive so a grader can pick one.
5. Weight and total. Assign points or weights per criterion reflecting importance; state how they sum to the final score.
6. Calibrate. Test the rubric against one strong and one weak sample; adjust any descriptor two graders could read differently.

## Example

Task: persuasive essay. Criterion "Evidence" across 4 levels — Exemplary: "3+ credible sources, each tied to a claim"; Proficient: "2-3 sources, mostly tied to claims"; Developing: "1-2 sources, loosely connected"; Beginning: "no or irrelevant sources." Other criteria: Thesis, Organization, Mechanics. Weights: Thesis 30%, Evidence 30%, Organization 25%, Mechanics 15%. Calibration on a B-grade sample flagged that "Organization/Proficient" and "Developing" overlapped, so descriptors were sharpened.

## Pitfalls

- Descriptors made of adjectives ("excellent," "adequate") with no observable evidence, so grading stays subjective.
- Overlapping levels a grader can't cleanly choose between, killing inter-rater reliability.
- Criteria that double-count the same trait, inflating or deflating scores.
- Grading effort, length, or neatness that the objectives never asked for.

## Output format

```
Task: <...> | Objectives assessed: <list> | Type: analytic/holistic

Rubric:
| Criterion (weight) | Exemplary | Proficient | Developing | Beginning |
| Thesis (30%)       | <observable> | <observable> | ... | ... |

Scoring: <how criteria sum to final grade>
Calibration notes: <adjustments after sample test>
```
