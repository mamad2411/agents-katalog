---
name: pmjob-take-home
description: Builds a Take-Home Assignment Plan that restates the brief, lists the questions to send before you start (expected hours, what is assessed, the AI rule), sets a time box you choose, lays out the submission with an assumptions and limits page, and adds a note of what you used AI for in line with what the employer allows. Use for "run pmjob-take-home", "plan my take-home", "product take-home assignment", "design challenge plan", "how long should a take-home take", "can I use AI on the take-home", "structure my case study submission", "take-home with no time limit", part of the Claude Guide for Product Interviews Pack by 90n.
---

# Take-Home Assignment Plan

## When To Use
The take-home says "spend as long as you need" and you are about to give it a week. Use this the day the brief arrives, before you open a blank document, to decide how much time it gets, what the reader needs to see and what the employer allows on AI. It answers: what is the smallest submission that shows how I think?

## When Not To Use
This applies the AI rule to one assignment; if you do not yet know the employer's rule for the whole process, start with Candidate AI Use Plan. For practice on questions nobody set you, use Product Sense Case. A piece you chose yourself to show how you work with AI is AI Work Sample.

## Inputs
- The assignment brief, pasted in full, with the deadline and anything the recruiter wrote around it
- The employer's AI rule for this stage and where it is written (the brief, an email, your Candidate AI Use Plan)
- The hours you can honestly give it this week
If you have none of this, I start from your description of the task and mark the output as a first draft.

## Approach
Scope and time box first: decide the hours and the shape of the answer before producing anything. The AI rule is read before that, as in Anthropic's Guidance on Candidates' AI Usage, which sets take-homes for its own hiring as done without AI unless the employer says otherwise. Silence is not permission, so an unstated rule becomes a question. The failure this prevents is thirty polished screens, no stated assumption, and a review call where you cannot say what you chose not to do.

## Workflow
1. Ask at most three questions: what the brief and the recruiter say about AI on this assignment, and where; how many hours you will give it in total; and who reviews it and whether a review call follows, if you know.
2. Settle the AI rule first. If AI is forbidden or not confirmed, this plan covers only the restated brief, the questions, the time box and the structure, and I do not touch the content. If it is allowed, the plan records what you will use it for.
3. Restate the brief in three lines: what is asked, for whom, and what a good submission would let the reader decide. Anything you cannot restate is a question, not an assumption to bury.
4. List the questions to send before starting, as points you send yourself: expected hours, what is being assessed, format and length, who reviews it, whether there is a review call, the AI rule. If the brief reads like unpaid production work on the employer's live product, I flag it and add a question for the recruiter; on the legal side, check with a qualified adviser.
5. Set the time box: your total, split across understand, decide, produce and check. One public employer guide describes its design challenge as an evening or two of work; that is one employer, not a standard, so the number is yours. When the box is spent you cut scope and say so, you do not add hours.
6. Lay out the submission in this order: the answer first, then the reasoning and the trade-offs, then the work, then an assumptions and limits page (what you assumed, what you did not do in the time, what would come next). Reviewers read the reasoning behind the screens and ask why on the call. Then write the AI use note, one or two lines, to attach wherever any AI was used. Claude Docs can hold the write-up and Claude Slides the deck, only where the employer allows AI.

## Output Format
```markdown
# Take-Home Assignment Plan
**Role:** [role] · **Due:** [date] · **AI rule:** [allowed for [what] / forbidden / not stated] · **Where written:** [source, date]
## The brief in three lines
[What is asked] · [For whom] · [What a good submission lets the reader decide]
## Questions to send first
1. [Expected hours, what is assessed, format and length, reviewer, review call, AI rule] · sent [date] · answer [ ]
## Time box
Total [hours you set] · understand [ ] · decide [ ] · produce [ ] · check [ ] · stop rule [what you cut first when the box is spent]
## Submission structure
| Part | What goes in | Length |
|---|---|---|
| The answer | [your recommendation in a few lines] | [ ] |
| Reasoning and trade-offs | [options considered, what you chose and what it costs] | [ ] |
| The work | [ ] | [ ] |
| Assumptions and limits | [assumed / not done in the time / what would come next] | [ ] |
## AI use note
[What you used AI for and what you did yourself, or "No AI was used on this assignment."]
## Decision
You decide the total hours, what to cut if the box runs out and whether to submit as planned, by [date].
```

## Done When
- The AI rule cell names a source, or the question about it has been sent
- The time box has a total and a stop rule you set, and the submission opens with the answer and closes with assumptions and limits
- An AI use note exists and matches what happened

## Quality Bar
- No norm for hours is invented; the only number in the time box is yours
- Where AI is forbidden or unconfirmed, I decline to produce any content of the assignment and say why in one line
- Cut scope is named on the limits page, never hidden
- Follow the employer's stated rule on AI for this assignment and say what you used; where AI is not allowed, the work is yours alone.

## Next
Run pmjob-round-debrief (Interview Round Debrief) to capture what happened after the review.

## About the makers

This pack is made by 90n ([90n.ai](https://90n.ai)): AI-native ways of working and tools for Product, Marketing and HR teams, built by ex-McKinsey founders. We map where time and money leak, redesign the work around AI and stay until your people run it themselves, and we run our own company on Claude. If your team has outgrown the self-serve version, message Pauline (linkedin.com/in/paulinebertry).
