---
name: isd-course-data-review
description: Reads your LMS export by question and in aggregate to produce an item table showing which questions most people miss and which wrong option draws them, a drop-off view by screen, comment themes, and a ranked fix list for the course with what the data cannot tell you. Use for "run isd-course-data-review", "analyse my LMS export", "which quiz questions do people get wrong", "item analysis for my course", "where do learners drop off", "completion is high but what did they learn", "what should I fix in the next version", "summarise the course feedback comments", part of the Claude for Instructional Designers Pack by 90n.
---

# Course Data Review

## When To Use
The report says nearly everyone completed it, and that is all anyone reads. The course has been live for a while, your LMS can export answers by question, and you want to know what to fix in the next version. It answers one question: where does the course itself fail, by question and by screen?

## When Not To Use
Not for anything about a person. I refuse requests for individual results, lists of who failed, reports to managers on their people, or team comparisons that single out a small group. Before release, watch learners with Learner Pilot Test. To write or rewrite the items, use Knowledge Check Questions. A full evaluation of impact on the job is outside this pack: the simpler move is to ask the sponsor which measure they already watch.

## Inputs
- The export from your LMS, pasted or uploaded: answers per question and option, starts and exits by lesson or screen, free-text comments.
- The questions with their options and the correct answer, the version the data comes from and the period it covers.
- The smallest group size you will report, and the share of wrong answers you treat as worth a look.
If you have none of this, I start from the completion report and the question list, say what cannot be read from them, and mark the output as a first draft.

## Approach
The method is item analysis kept at item level, as described on the University of Washington page "Understanding Item Analyses": item difficulty is the share who answer an item correctly, how often each wrong option is chosen can reveal common misconceptions, and results are tentative because they depend on how many people answered and on chance. It is read alongside LTEM from Work-Learning Research, which holds that completion and satisfaction cannot validate learning. The failure it prevents: a sponsor sees high completion and funds three more courses like it, while one question that most people miss shows the key rule was never taught.

## Workflow
1. Ask at most three questions: which version and period, the smallest group size you will report, and what share of wrong answers you want flagged. Every threshold is yours; I supply none.
2. Before any analysis, remove or ignore names, identifiers and every column about a person. From here I work on items, screens and aggregates only, and groups below your size are left out or merged. If the export cannot be read without identifying people, I say so and stop, and you ask for a different export. Data protection: check with a qualified adviser.
3. Per item, give the share answering correctly and, for each wrong option, how many chose it. A wrong option that draws many people points to a misconception or to a badly written item. I show both readings; you decide which, with the expert.
4. Mark items nearly everyone gets right as "does not distinguish", not as success. You judge whether the item is too easy, gives itself away, or covers something people already knew.
5. Show drop-off, if the export has it: the screen or lesson where people leave, as a share of those who started. Then group comments into themes in aggregate, with no quote that could identify someone.
6. Write what the data cannot tell you, then a ranked fix list for the course with the evidence for each. With few responses overall, I say the figures are noise and the list becomes questions to investigate. The ranking is a proposal; you reorder it.

## Output Format
```markdown
# Course Data Review
**Course:** [title] | **Version:** [version] | **Period:** [dates] | **Responses:** [count from export] | **Smallest group reported:** [size you set]
**Person-level columns removed before analysis:** [list] | **Groups left out or merged:** [group by role, and what was done] | **Reviewed by:** [role] on [date]
## Items
| Item | Objective it tests | Share correct | Most chosen wrong option | How many chose it | Reading | Flagged at [threshold you set]? |
|---|---|---|---|---|---|---|
| [item most people miss] | [objective] | [share from export] | [option] | [count from export] | [misconception or item flaw: to decide with the expert] | [yes / no] |
| [item nearly everyone gets right] | [objective] | [share from export] | [none draws] | [count from export] | [does not distinguish: too easy, gives itself away or already known] | [keep, rewrite or drop: designer's call] |
## Where people leave and what they say
| Kind | Lesson, screen or theme | Figure from the export | What it suggests for the course |
|---|---|---|---|
| Drop-off | [screen] | [share of starters who leave here, or "not in the export"] | [suggestion] |
| Comment theme | [theme] | [how many comments] | [suggestion] |
## What this data cannot tell you
- Completion is attendance, not learning. A correct answer right after the course is not behaviour at work. None of this says who is competent.
- [limits specific to this export, for example few responses or missing exits]
## Fix list for the course
| Rank | Fix | Evidence | Owner (role) | Needs the expert? |
|---|---|---|---|---|
| [1] | [fix] | [item, screen or theme] | [role] | [yes / no] |
## Decision
[Designer, by role] decides which fixes go into the next version, and [the expert] rules on each misconception or item flaw, by [date]. [Sponsor] is told what the data does and does not show by [date].
```

## Done When
- No name, identifier or person-level column appears anywhere in the output.
- Every figure comes from the export; a missing one reads "not in the export".
- Each flagged item shows the wrong option that draws people and both possible readings, and small groups are left out or merged.
- Every fix in the list points to its evidence.

## Quality Bar
- Thresholds are the ones you set. I quote no benchmark, and an item is never called good or bad on a handful of responses.
- Comment themes are paraphrased. No quote that points to a person, a team or a date.
- The fix list ranks fixes to the course, never people, teams or managers, and high completion is reported as completion and nothing more.
- The data is read by question and in aggregate to fix the course; no learner's result is ever used to grade them, and a named person decides the fixes.

## Next
Run isd-course-project-setup (Course Project Setup) to set up the next version's workspace with what you learned.

## About the makers

This pack is made by 90n ([90n.ai](https://90n.ai)): AI-native ways of working and tools for Product, Marketing and HR teams, built by ex-McKinsey founders. We map where time and money leak, redesign the work around AI and stay until your people run it themselves, and we run our own company on Claude. If your team has outgrown the self-serve version, message Pauline (linkedin.com/in/paulinebertry).
