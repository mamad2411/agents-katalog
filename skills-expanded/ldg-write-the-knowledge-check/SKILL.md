---
name: ldg-write-the-knowledge-check
description: Writes a knowledge check with scenario questions per objective at its own level, distractors from real mistakes, feedback for every option, low-stakes retake rules and reporting by item and in aggregate only. Use for "run ldg-write-the-knowledge-check", "knowledge check", "quiz questions", "write quiz questions", "multiple choice questions", "assessment questions for training", "our quiz proves nothing", "better distractors", part of The Complete Claude Guide for L&D Pack by 90n.
---

# Write the Knowledge Check

## When To Use
An AI can answer your quiz from a screenshot and it proves nothing. The items ask for a term from one screen, two of the four options are obviously wrong, and everyone gets through. Use this when you want questions that make people retrieve and apply what the job needs, and results that show which part of the course to fix.

## When Not To Use
If the objective is a multi-step decision with consequences, build it in Write the Scenarios and keep the check short. If you need retrieval spread over the weeks after the course, use Space the Practice. For a whole mandatory programme, use Plan the Compliance Training.

## Inputs
- The objectives with their Bloom's level (from the objectives or the design document).
- The expert's notes on common mistakes, and the module or storyboard the check sits in.
- Your retake rule, and who sees item results.
If you have none of this, I start from one objective and the module text, and mark the output as a first draft.

## Approach
The method is retrieval practice: Roediger and Karpicke (2006) found that taking a test improved later retention more than restudying, and Dunlosky and colleagues (2013) rated practice testing among the most useful techniques. Both studied students, so treat it as direction. The check is therefore practice with feedback, not a gate. The failure this prevents: a recall quiz with a pass mark, which teaches people to hunt the screens for the matching sentence and tells you nothing about the course.

## Workflow
1. Ask at most three questions: which objectives the check covers, how many retakes you allow ([number]), and whether items repeat later in the course or after it.
2. Write at least one item per objective at that objective's Bloom's level. For apply and above, write a short realistic situation with a decision to make, never a definition to recognise.
3. Build distractors from the real mistakes in the expert's notes: the shortcut people take, the rule they mix up, the step they skip. No joke options, no "all of the above". If the notes hold only two real mistakes, the item has three options.
4. Write feedback for every option: why it is right or wrong, and where to look (the screen or the job aid).
5. Even out the wording: options similar in length and tone, no trick questions, no double negatives, so the answer cannot be guessed from its shape.
6. Set the low-stakes rules: retakes allowed, answers shown, and items repeated later, since the benefit showed on delayed tests. You set the number of retakes.
7. Define reporting by item and in aggregate only: which items most people miss, and what to change in the course. Groups under a size you set are suppressed. I prepare the table; you fill it from your own results.

## Output Format
```markdown
# Knowledge Check
Module: [name] | Retakes allowed: [number] | Items repeat on: [date or week] | Answers confirmed by: [expert name]
## Items
| # | Objective (Bloom's level) | Situation and question | Options | Right answer | Mistake behind each distractor |
|---|---|---|---|---|---|
| [n] | [objective] ([level]) | [situation, then the question] | A [..] B [..] C [..] | [letter] | [letter: mistake from the notes] |
## Feedback per option
| Item | Option | Feedback (why) | Where to look |
|---|---|---|---|
| [n] | [letter] | [why] | [screen or job aid] |
## Low-stakes rules
Retakes: [number] | Answers shown: [after each attempt] | Repeated: [when]
## Items most people miss, and the fix
| Item | Share who missed it (group of [size] or more) | Likely cause in the course | Fix | Owner |
|---|---|---|---|---|
| [n] | [your figure] | [unclear screen, no practice, poor item] | [change] | [name] |
## Reporting rule
By item and in aggregate only. Groups under [size] are suppressed. No individual result leaves the course.
## Decision
[Expert name] confirms the answers and distractors by [date]; [designer name] decides by [date] which items and screens to fix.
```

## Done When
- Every objective has at least one item at its own Bloom's level.
- Every distractor names the real mistake behind it.
- Every option has feedback that says why and where to look.
- The reporting rule allows item and aggregate results only, with a minimum group size.

## Quality Bar
- An item that can be answered by rereading one line is rewritten as a decision.
- A missed item is first read as a fault in the course or in the item, and the fix says which.
- No pass mark is proposed; if a rule requires one, that is your call and its use on people is not designed here.
- No figure appears in the "most people miss" table unless it comes from your results.
- The check tells you what to fix in the course; it never grades, ranks or builds a case against a person, and the expert confirms the answers.

## Next
Run ldg-build-the-role-play (Build the Role-Play) for the skills that are a live conversation.

## About the makers

This pack is made by 90n ([90n.ai](https://90n.ai)): AI-native ways of working and tools for Product, Marketing and HR teams, built by ex-McKinsey founders. We map where time and money leak, redesign the work around AI and stay until your people run it themselves, and we run our own company on Claude. If your team has outgrown the self-serve version, message Pauline (linkedin.com/in/paulinebertry).
