---
name: edu-curriculum-design
version: 1.0.0
description: Design a course curriculum with measurable learning objectives, a logical unit sequence, and aligned assessments.
author: matrixx0070
tags: [education, curriculum, instructional-design, objectives, sequencing]
capabilities: []
---

## When to use

Use this when you need to turn a subject and audience into a full course: what learners will be able to do, in what order they learn it, and how each unit builds on the last. Best for multi-week or multi-module courses where sequence and coverage matter.

**Not for:** a single class session (use edu-lesson-plan), writing one assessment (use edu-quiz-builder), or explaining one concept (use edu-explainer).

## Method

1. Define the learner and end state. Confirm audience, prior knowledge, time budget, and the terminal outcome — what a graduate can do. Decision point: if prior knowledge is unknown, assume the stated minimum prerequisite and label it.
2. Write terminal objectives. Draft 3-6 course-level objectives using measurable verbs (Bloom's: analyze, apply, evaluate). Ban vague verbs like "understand" or "know."
3. Decompose into units. Break each terminal objective into unit-level enabling objectives. Decision point: if a unit has more than ~4 objectives, split it.
4. Sequence. Order units by dependency (prerequisites first), then by cognitive load (concrete before abstract, simple before complex).
5. Align assessment. Map at least one assessment or checkpoint to every objective. Flag any objective with no assessment (orphan) or any assessment testing no objective.
6. Add pacing. Assign time per unit against the budget; flag overload.

## Example

Course: "Intro to SQL for analysts," 6 weeks, learners know spreadsheets. Terminal objective: "Write multi-table queries to answer a business question." Units: (1) SELECT/WHERE, (2) sorting/filtering, (3) JOINs, (4) aggregation/GROUP BY, (5) subqueries, (6) capstone. JOINs (3) must precede aggregation-across-tables (4). Each unit ends with a graded exercise; the capstone assesses the terminal objective. Week 5 looked overloaded (3 hard objectives) so subqueries split across two sessions.

## Pitfalls

- Objectives that use unmeasurable verbs ("understand," "be aware of") so mastery can't be checked.
- Sequencing by topic familiarity instead of prerequisite dependency, leaving learners stuck.
- Objectives with no matching assessment, or assessments that test untaught material.
- Cramming coverage past the time budget instead of cutting scope.

## Output format

```
Course: <title> | Audience: <who> | Prereqs: <...> | Duration: <...>

Terminal objectives:
1. <measurable verb + outcome>

Unit map:
| Unit | Enabling objectives | Depends on | Assessment | Time |

Sequence rationale: <why this order>
Coverage/alignment gaps: <orphan objectives or assessments>
Assumptions: <prior knowledge, time>
```
