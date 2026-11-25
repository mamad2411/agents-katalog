---
name: isd-course-curriculum-map
description: Lays out a Course Curriculum Map with modules and lessons in order, the objective, practice and check per lesson, a whole-task ladder from simple to hard, two gap lists and the learner's path. Use for "run isd-course-curriculum-map", "map this course", "course outline by lesson", "the lessons do not connect", "which lesson covers which objective", "sequence these lessons", "lessons with no objective", "what order should the lessons go in", part of the Claude for Instructional Designers Pack by 90n.
---

# Course Curriculum Map

## When To Use
The course grew lesson by lesson and nothing connects: lesson four exists because someone sent a deck, and one objective is practised nowhere. Use this when the design is agreed and you need one course laid out at lesson level, to answer which lesson serves which objective, on what case, in what order.

## When Not To Use
The map holds the order, not the reasons: why this strategy and this format live in Course Design Document. It also stops at lessons. For screens, run E-Learning Storyboard Template. A spaced set of short pieces is a different format: run Microlearning Series.

## Inputs
- The agreed objectives and, if you have it, the design per objective (practice and check)
- The current lesson list or outline: titles, what each covers, any existing practice or check
- Two or three real cases for the task, from routine to awkward, ideally from the expert's notes
If you have none of this, I start from a lesson list and one sentence on the task, and mark the output as a first draft.

## Approach
Backward design, as described by the Yale Poorvu Center, means each lesson earns its place through a result and its evidence before any content is chosen. Merrill's First Principles of Instruction (2002, Educational Technology Research and Development, ERIC EJ657839) give the sequence: learning is organised around real problems, and each lesson activates what people already know, demonstrates, has them apply, and asks them to integrate it into their own work. You decide what is cut and what the learner meets first. The failure this prevents is the outline sorted by topic: definitions, then rules, then exceptions, and the learner reaches a real case in the last lesson, when nobody is still paying attention.

## Workflow
1. Ask three questions: which objectives must this course deliver, what lessons exist or are planned, and which real cases can it be built around?
2. Write one row per lesson, inside its module, from the objective outward: objective, practice, check, the whole task it works on. A lesson's current content does not get to define its row.
3. Build the two gap lists. Lessons that serve no objective: I propose cut, merge or move to reference, with a reason the requester can accept. Objectives with no practice or no check: I propose which lesson takes it. You decide each one.
4. Draw the whole-task ladder: a routine case, a case with one complication, an exception. Re-sequence the lessons along it. A topic that only matters in the hard case moves later, even if it sits first in the manual. Then check the four phases inside every lesson: activate, demonstrate, apply, integrate. Flag any lesson with no apply; a lesson with content and no practice is a reading, and the map labels it as one.
5. Lay out the learner's path: the order, what is required before what, and where the course can be left and resumed. Every duration is yours to set; until then it stays `[duration you set]`. Then read the map back as the learner: what do I do first, and when do I first make a decision? If that moment is late, say so at the top.

## Output Format
```markdown
# Course Curriculum Map
## Lessons in order
| Module | Lesson | Objective | Practice | Check | Whole task it works on | Time |
|---|---|---|---|---|---|---|
| [M1] | [L1.1] | [objective #] | [what the learner does] | [check] | [routine case] | [duration you set] |
## Whole-task ladder
| Rung | Case | What is new at this rung | Lessons |
|---|---|---|---|
| [1 Routine / 2 Complication / 3 Exception] | [case] | [the basic steps / the one thing that changes / the rule that breaks] | [L1.1, L1.2] |
## Four phases per lesson
| Lesson | Activate | Demonstrate | Apply | Integrate | Flag |
|---|---|---|---|---|---|
| [L1.1] | [problem they have met] | [worked example] | [practice] | [use on own work] | [none / no apply] |
## Gaps
| Type | Item | Proposal | Your call |
|---|---|---|---|
| Lesson with no objective | [lesson] | [cut / merge with [lesson] / move to reference] | [accept / reject] |
| Objective with no practice or check | [objective #] | [goes in [lesson]] | [accept / reject] |
## Learner's path
| Step | Lesson | Required before it | Can stop and resume here? |
|---|---|---|---|
| 1 | [L1.1] | [nothing] | [yes / no] |
## Decision
[Designer name] decides the cuts, the merges and the first lesson; [sponsor name] and [expert name] accept the map, with its gap list, by [date].
```

## Done When
- Every lesson traces to an objective, and every objective has a practice and a check, or the item sits on the gap list with a proposal
- The order follows the whole-task ladder, not the topic list
- Every lesson has an apply phase or carries a flag

## Quality Bar
- Rows are lessons, not screens and not topics
- A cut is proposed with a reason, never made silently
- Cases come from the expert or from you, and an invented case is marked fictional; durations stay placeholders until you set them from your own builds
- Claude lays out the map and shows the gaps; you decide what is cut and what the learner does first

## Next
Run isd-assessment-blueprint (Assessment Blueprint) to plan the checks before the content is written.

## About the makers

This pack is made by 90n ([90n.ai](https://90n.ai)): AI-native ways of working and tools for Product, Marketing and HR teams, built by ex-McKinsey founders. We map where time and money leak, redesign the work around AI and stay until your people run it themselves, and we run our own company on Claude. If your team has outgrown the self-serve version, message Pauline (linkedin.com/in/paulinebertry).
