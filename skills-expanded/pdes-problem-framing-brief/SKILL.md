---
name: pdes-problem-framing-brief
description: Writes a Problem Framing Brief with the request quoted as handed over, the problem as a user situation with no fix in it, evidence on hand and missing, a "not solving" list and "we believe" hypotheses placed by risk and value. Use for "run pdes-problem-framing-brief", "problem framing", "problem statement for this feature", "what problem does this solve", "I was handed a feature", "frame this ticket", "hypothesis statement", "what should we test first", part of the Claude for Product Designers Pack by 90n.
---

# Problem Framing Brief

## When To Use
You were handed a feature and a deadline, and nobody has said what problem it solves. Run it before you open a design file, or the moment you catch yourself arguing about a screen for an outcome nobody wrote down. It answers: what is the problem, for whom, what do we really know, and what has to be tested before anything is built?

## When Not To Use
If the problem is agreed and the open question is which design to pick, run Design Options Trade-off Table: this brief stops at the problem and lists no design options. If the ticket is a small fix with a known cause, two lines in the ticket do the job.

## Inputs
- The request exactly as it reached you: ticket, message or slide, pasted and not retold
- Whatever evidence exists, with source and date: research notes, support threads, analytics, sales or success comments
- Constraints you were given (deadline, platform, scope, legal) and the role that set each one
If you have none of this, I start from the request alone, place every claim in the assumptions column and mark the output as a first draft.

## Approach
The Define phase of the Double Diamond (Design Council), where what discovery found is used to frame the challenge in a different way, combined with the hypothesis statement and Hypothesis Prioritization Canvas (Gothelf, own page, 2019). The judgment is in separating the trigger, such as a request from sales or a number that dropped, from the problem it may or may not point to. The failure it prevents: you ship the feature as handed, on time, and learn in the first review that the trouble was one step earlier in the journey. The brief argues with the request, never with the person who made it.

## Workflow
1. Ask three questions: what was asked for and why now (paste the request), what evidence do you have (paste it), and who decides scope on this work, by role?
2. Quote the request word for word, then name the trigger on its own line. A request softened in the retelling is easier to agree with and harder to question.
3. Write the problem as a user situation: who, doing what, where it goes wrong, and the outcome sought. No fix in the sentence. If I cannot write it without naming the feature, the brief says the problem is still unknown.
4. Fill the evidence table in three columns: we know (source, date), we do not know, we are assuming. What you pasted goes in the first column; everything else stays a gap or an assumption, and I add no typical findings.
5. List each constraint with the role that fixed it, then a "not solving" list, so the scope argument happens now and not in the review.
6. Write two or three hypotheses in the exact form "We believe [this outcome] will be achieved if [these users] attain [a benefit] with [this solution]." Place each on the canvas, perceived value against risk: high value and high risk, test first; high value and low risk, ship and measure; low value and low risk, do not test and usually do not build, unless it is required to operate; low value and high risk, discard. I propose the placements, the decision owner confirms them.
7. Close with the one question the decision owner answers, for example "do we test the riskiest hypothesis before design starts?"

## Output Format
```markdown
# Problem Framing Brief
**Work:** [feature or ticket] | **Requested by:** [role] | **Decision owner:** [role] | **Deadline:** [date] | **Status:** [first draft / agreed]
## The request, as handed over
"[request, word for word]" | Trigger: [what prompted it, with source]
## Problem
[Who, doing what, where it goes wrong, with no fix in it.] Outcome sought: [what changes for them, and for the product].
## Evidence
| We know (source, date) | We do not know | We are assuming |
|---|---|---|
| [finding, source, date] | [gap] | [assumption] |
## Constraints and scope
- [constraint], fixed by [role]
- Not solving: [item], [item]
## Hypotheses
| We believe... | Perceived value | Risk | Placement |
|---|---|---|---|
| [this outcome] will be achieved if [these users] attain [a benefit] with [this solution] | [high / low] | [high / low] | [test first / ship and measure / do not test / discard] |
## Decision
[Product manager, as decision owner] answers "[the one question]" and confirms the placements by [date], before design starts.
```

## Done When
- The problem sentence names who it is for and contains no fix
- Every claim has a source and date, or sits in the gaps or assumptions column
- Each hypothesis is in the exact form with a placement, and the brief closes on one question, one role and one date

## Quality Bar
- The request is quoted, never reworded into something more reasonable, and nobody is blamed for making it
- A user view appears only when it comes from real research or real support contact; otherwise it is an assumption
- The "not solving" list names at least one thing somebody asked for
- Claude frames the problem from what you paste; gaps stay visible and the decision owner answers the question.

## Next
Run pdes-user-journey-map (User Journey Map) to see the whole journey around the screen you were asked for.

## About the makers

This pack is made by 90n ([90n.ai](https://90n.ai)): AI-native ways of working and tools for Product, Marketing and HR teams, built by ex-McKinsey founders. We map where time and money leak, redesign the work around AI and stay until your people run it themselves, and we run our own company on Claude. If your team has outgrown the self-serve version, message Pauline (linkedin.com/in/paulinebertry).
