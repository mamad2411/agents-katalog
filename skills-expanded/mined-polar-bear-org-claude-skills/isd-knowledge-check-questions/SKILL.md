---
name: isd-knowledge-check-questions
description: Drafts knowledge check questions written to the assessment blueprint, each one a short decision with distractors taken from real mistakes, feedback for every option, an item-writing rule check and an item review table for the expert. Use for "run isd-knowledge-check-questions", "write quiz questions for this course", "an AI can pass our quiz from a screenshot", "questions that ask for a decision", "fix these multiple-choice questions", "distractors from real mistakes", "check my questions against item-writing rules", "feedback for every answer option", part of the Claude for Instructional Designers Pack by 90n.
---

# Knowledge Check Questions

## When To Use
An AI can pass your quiz from a screenshot, so it proves nothing. The items ask for a term from one slide, the wrong options are silly, and the longest answer is the right one. Use this to write items that ask for the decision the job asks for, and that tell you which part of the course to fix.

## When Not To Use
If nobody has decided how many items each objective gets or what a result is used for, run Assessment Blueprint first: this skill writes, it does not plan. If the objective is a chain of linked decisions with consequences, write it in Branching Scenario Script and keep the check short.

## Inputs
- The blueprint rows (objective, level, evidence type, number of items) and the storyboard or module the check sits in.
- The expert's notes on the common mistakes.
- Your retake rule and the smallest group size you report on.
If you have none of this, I write one item per objective from the module text, and mark the set as a first draft.

## Approach
Retrieval practice: Roediger and Karpicke (2006, Psychological Science) found that taking a test improved later retention more than restudying. So a check is practice first, and its results are for fixing the course. The items follow the common rules of multiple-choice writing, applied one by one. The failure this prevents: an item anyone can get right from its wording alone, because the right answer is the longest, the only grammatical fit, or "all of the above". No rule makes a quiz proof against a tool; a decision built on real mistakes at least asks for what the job asks for.

## Workflow
1. Ask up to three questions: which blueprint rows this set covers, your retake rule and whether items repeat later, and the smallest group size you report on.
2. Write each item to its row, at the row's level. For apply and above, a short realistic situation with a decision ("A customer says X. What do you do next?"), never a definition. Recall items only where the blueprint asks for recall.
3. Take the distractors from the expert's notes: the shortcut, the rule people mix up, the step they skip. Each distractor names the mistake behind it. If the notes give two real mistakes, the item has three options; I do not invent a fourth.
4. Write feedback for every option: why it is right or wrong, and the screen or job aid it points back to.
5. Run the rule check on each item: one clear problem in the stem; the stem makes sense with the options covered; no negatives or absolutes; options parallel in length and grammar; one best answer; no "all of the above" or "none of the above"; every distractor plausible. A failed rule is fixed, or flagged for you.
6. Set the low-stakes rules: retakes, answers shown after an attempt, items repeated later. Reporting is by item and in aggregate, with groups under your size left out. Any pass mark is the organisation's and is written `[pass mark, set by whom]`; I propose none.
7. Hand the expert the item review table. Where the notes do not settle an answer I write `[to confirm with the expert]` and the item stays out of the course until it is confirmed.

## Output Format
```markdown
# Knowledge Check Questions
Course: [name] | Blueprint version: [n or "none, first draft"] | Retakes: [rule you set] | Items repeat: [where or when]
## Items
| Item | Blueprint row and level | Stem (situation and question) | Options | Best answer | Mistake behind each distractor |
|---|---|---|---|---|---|
| Q1 | [objective, level] | [situation, then the question] | A [..] B [..] C [..] | [letter] | [B: mistake, C: mistake] |
## Feedback
| Item | Option | Feedback (why) | Points back to |
|---|---|---|---|
| Q1 | A | [why] | [screen or job aid] |
## Rule check
| Item | Stem: one problem, stands alone | No negatives or absolutes | Options parallel | One best answer | No "all" or "none of the above" | Distractors plausible | Action |
|---|---|---|---|---|---|---|---|
| Q1 | [met or not] | [met or not] | [met or not] | [met or not] | [met or not] | [met or not] | [none, fixed, or flagged] |
## Item review for the expert
| Item | Answer confirmed | Distractors are real mistakes | Change asked | Date |
|---|---|---|---|---|
| Q1 | [yes, no] | [yes, no] | [change] | [date] |
## Rules and reporting
Low stakes: [retakes, answers shown after an attempt]. Reporting by item and in aggregate; groups under [size you set] are left out. Pass mark: [pass mark, set by whom].
## Decision
The expert, by role, confirms every answer and distractor by [date]. The designer decides which items go in and which are rewritten, by [date]. What a result is used for stays with the person named in the blueprint.
```

## Done When
- Every item carries its blueprint row and sits at that row's level.
- Every distractor names the real mistake behind it, and every option has feedback that says why.
- The rule check is filled in for every item, and the reporting line allows results by item and in aggregate only.

## Quality Bar
- An item answerable by rereading one line of a slide is rewritten as a decision; the right answer is not the longest option, and its position varies.
- Names and cases in a stem are fictional; nothing is written as a real incident.
- I do not design a ranking, a list of who missed what, or a report on one person. If a result could affect someone's job, that is for the organisation: check with a qualified adviser.
- Claude drafts the items; the expert confirms every answer, and results fix the course, never grade a learner.

## Next
Run isd-job-aid-template (Job Aid Template) for what people should look up, not remember.

## About the makers

This pack is made by 90n ([90n.ai](https://90n.ai)): AI-native ways of working and tools for Product, Marketing and HR teams, built by ex-McKinsey founders. We map where time and money leak, redesign the work around AI and stay until your people run it themselves, and we run our own company on Claude. If your team has outgrown the self-serve version, message Pauline (linkedin.com/in/paulinebertry).
