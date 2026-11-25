---
name: ldg-write-the-scenarios
description: Writes decision scenarios built from real mistakes, with options that tempt, a consequence and feedback for every choice, a path map with no dead ends and a list of facts for the expert to confirm. Use for "run ldg-write-the-scenarios", "scenario based learning", "branching scenario", "write a scenario", "decision scenario", "practice not content", "turn the expert's incidents into practice", "they passed the course and still cannot make the call", part of The Complete Claude Guide for L&D Pack by 90n.
---

# Write the Scenarios

## When To Use
New hires completed every module and still cannot make the call on the job. They can recite the rule, then stall the first time a real case does not look like the slide. Use this when the objective is a decision a person makes alone, and you need practice where a wrong choice shows what happens next.

## When Not To Use
If one short question per objective is enough, use Write the Knowledge Check. If the skill is a live conversation between people, use Build the Role-Play. Scenarios are for multi-step decisions made alone, on screen or on paper.

## Inputs
- The objective this practice serves, the learners by role and task, and the format (e-learning, paper, a live discussion).
- The expert's notes on real incidents: what happened, the mistakes people make, the exceptions.
If you have none of this, I start from one objective and one incident you describe in two lines, and mark the output as a first draft.

## Approach
The method is Merrill's First Principles of Instruction (2002 paper): learning is promoted by a real problem, then activation, demonstration, application and integration. So each scenario grows out of one incident that really happened, and the content only appears where the decision needs it. The failure this prevents is the scenario with one sensible answer and three absurd ones: everybody clicks the sensible one, the report shows full marks, and the first hard case at work still goes wrong. Wrong options have to be the mistakes capable people make under pressure.

## Workflow
1. Ask at most three questions: which objective and which incident to build from, how many decision points you want ([number]), and the format and length the build allows.
2. Choose one real incident from the expert's notes and write the setup in the learner's work language: who, where, what is at stake, what they can see. Leave the time pressure in. Characters are fictional and marked so.
3. Put Merrill's order around it. Activate: a question on what the learner has already seen on the job. Demonstrate: a short worked case with the expert's reasoning said aloud. Apply: the scenario. Integrate: a prompt about their own work next week.
4. At each decision point write three or four options: the right call and the real mistakes from the notes. A mistake nobody makes is cut, even if it leaves only three options.
5. For every option write the consequence the learner sees (the reply, the reopened case, the delay) and feedback that says why. Branch only where a mistake changes the outcome; elsewhere show the consequence and let the learner recover.
6. Draw the path map and check it: every branch reaches an end, there are no loops, and the right answer is not always the longest option. Then list every fact, rule and figure used, with its source, for the expert to confirm. I do not fill gaps in the notes with plausible detail.

## Output Format
```markdown
# Decision Scenarios
Objective served: [objective] | Source incident: [note reference] | Format: [format] | Characters are fictional
Setup: [who, where, what is at stake, what the learner can see]
## Around the scenario
| Phase | What the learner gets | Expert reasoning shown |
|---|---|---|
| Activate | [question on what they have already seen] | n/a |
| Demonstrate | [short worked case] | [what the expert noticed, and why] |
| Integrate (after) | [prompt about the learner's own work next week] | n/a |
## Decision points
| Point | Option | Right call or the real mistake behind it | Consequence the learner sees | Feedback (why) | Goes to |
|---|---|---|---|---|---|
| [n] | [option] | [right call, or mistake from the notes] | [what happens] | [why] | [point or end] |
## Path map
| Path | Points passed | Ends at | Checked: ends, no loop |
|---|---|---|---|
| [name] | [n, n, n] | [ending] | [yes or no] |
## Facts for the expert
| Fact, rule or figure | Where it is used | Source | Confirmed |
|---|---|---|---|
| [fact] | [point and option] | [note or document] | [yes, no, changed] |
## Decision
[Expert name] confirms the facts and the mistakes by [date]; [designer name] decides by [date] whether the scenarios go to storyboard.
```

## Done When
- Every wrong option traces to a mistake in the expert's notes.
- Every option has a consequence and feedback that says why.
- The path map shows every path ending, with no loop; every fact sits in the list for the expert, and characters are marked fictional.

## Quality Bar
- The setup reads like a real shift, in the words people use at work.
- The right option is not the longest, the most polite or always in the same position.
- Feedback explains the reasoning; "Correct" or "Try again" alone is rewritten.
- Claude drafts from the expert's real cases; the expert confirms every fact, and a learner's choices are practice, never a record about them.

## Next
Run ldg-storyboard-the-elearning (Storyboard the E-Learning) to put the scenario on screens.

## About the makers

This pack is made by 90n ([90n.ai](https://90n.ai)): AI-native ways of working and tools for Product, Marketing and HR teams, built by ex-McKinsey founders. We map where time and money leak, redesign the work around AI and stay until your people run it themselves, and we run our own company on Claude. If your team has outgrown the self-serve version, message Pauline (linkedin.com/in/paulinebertry).
