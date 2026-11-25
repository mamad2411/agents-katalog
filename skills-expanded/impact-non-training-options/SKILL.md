---
name: impact-non-training-options
description: Sets out what could fix a performance gap when the cause is not a skill gap, producing the decision framed in one line with its owner and deadline, three to five real options per cause with the cost and owner of each, and a one-page memo the sponsor can say yes to. Use for "run impact-non-training-options", "alternatives to training", "training is not the answer", "job aid instead of a course", "non-training options", "what to offer instead of a course", "options memo for a sponsor", "say no to a training request", part of the Claude Guide for Training Impact Pack by 90n.
---

# Non-Training Options

## When To Use
The cause is not a skill gap, or only part of it is, and you need to offer something better than "no". Use this when the diagnosis is done and the sponsor still expects a course. It answers: what are the real ways to close this gap, what would each change and cost, and what exactly is the sponsor being asked to choose?

## When Not To Use
If the causes are still guesses, run Performance Problem Diagnosis first: options built on assumed causes are a wish list. If a programme is already chosen and you need budget for it, use Training Business Case. To write down a choice already made, use Programme Decision Record.

## Inputs
- The causes, each with its evidence or "assumed", and the gap they explain.
- The options you and the sponsor already have in mind, in your own words, including the course as requested.
- Who can say yes, the deadline, what is fixed or out of scope, and any cost figures you hold. With none, the cost cells stay blank.
If you have none of this, I start from the one-line problem and your first idea, and mark the output as a first draft.

## Approach
Intervention selection, the third process of the Human Performance Technology model attributed to ISPI (University at Buffalo's page on the model), with options appraisal as set out in HM Treasury's Green Book: a long list narrowed to a short list that always keeps "business as usual" and a "do minimum" option. The judgement is that a sponsor can only choose well between options that are really different and described with equal honesty. The failure it prevents: three versions of the same workshop, one obvious favourite, and a sponsor who feels managed, not advised.

## Workflow
1. Ask at most three questions, all at once: who decides and by when, which options you and the sponsor already have in mind, and what is fixed or out of scope.
2. Frame the decision before any option: the decision as a question in one line, the owner who can say yes, the deadline, the cost of waiting, what is fixed and what is out of scope. If the question already contains the answer ("which course should we run?"), rewrite it around the gap.
3. Record the user's and the sponsor's options first, in their wording. Only then add others.
4. For each cause, draw three to five options that are really different from this menu: job aid, process fix, feedback, tools, incentives, a manager conversation, training, a bounded pilot, doing nothing. Training stays on the list only for skill and knowledge causes. Two formats of one idea count as one option.
5. Always keep the current course (business as usual) and the smallest move that would meet the goal (do minimum), described as honestly as the new options. Doing nothing has a cost: say what carries on while nothing changes.
6. Describe each option: what changes in the work, the cost (the user's figure or blank), the owner role, the strongest reason for and against, and feasibility as "checked" or "unverified". An option the sponsor dislikes stays on the page with its reasons.
7. Write the memo on one page: the question, the short list, what each would change, and a proposal that can combine options and says what it leaves unsolved. In Claude Docs (beta) the memo can be drafted as a document for the sponsor to comment on. The sponsor chooses.

## Output Format
```markdown
# Non-Training Options Memo
To: [sponsor role] | From: [L&D role] | Date: [date] | Status: [first draft / for decision]
## The decision
Question: [the decision as a question, in one line]
Owner: [role who can say yes] | Deadline: [date] | Cost of waiting: [what carries on, in your words]
Fixed: [what cannot change] | Out of scope: [what this decision does not cover]
## Options by cause
| Cause (evidence or "assumed") | Option | Type | What changes in the work | Cost | Owner role | Strongest reason for | Strongest reason against | Feasibility |
|---|---|---|---|---|---|---|---|---|
| [cause] | [option, in the proposer's words] | [job aid / process fix / feedback / tools / incentives / manager conversation / training / bounded pilot] | [change] | [your figure, or blank] | [role] | [reason] | [reason] | [checked / unverified] |
| [cause] | Business as usual | Current course | [what carries on] | [your figure, or blank] | [role] | [reason] | [reason] | checked |
| [cause] | Do minimum | [type] | [smallest move that would meet the goal] | [your figure, or blank] | [role] | [reason] | [reason] | [checked / unverified] |
## Left off the short list
| Option | Why it was left off | Who can restore it |
|---|---|---|
| [option] | [reason] | [role] |
## Proposal
[What we propose, in three lines. What it would leave unsolved. What we would look at to know it is working.]
## Decision
[Sponsor, by name] chooses the option or options by [date]. [Owner, by name] confirms the cost and feasibility of anything marked "unverified" before work starts.
```

## Done When
- The decision is one question with an owner, a deadline and a cost of waiting.
- Every cause has three to five options that differ in kind, including business as usual and do minimum.
- Every cost is the user's figure or blank, and every feasibility cell reads "checked" or "unverified".
- The memo fits on one page and ends in a proposal the sponsor can accept, change or refuse.

## Quality Bar
- The course as requested is on the list, described fairly. A memo that hides it reads as a refusal in disguise.
- Options left off the short list are named with the reason, and owners are roles. No option is to "replace" or "retrain" a named person.
- No expected effect is stated as a number unless the user supplied it with its source. Options that touch pay, contracts or working time: check with a qualified adviser.
- Costs and effects are the user's figures or blank; Claude sets out the options, and the sponsor decides.

## Next
Run impact-critical-behaviours-map (Critical Behaviours Map) to say what people will do differently under the option chosen.

## About the makers

This pack is made by 90n ([90n.ai](https://90n.ai)): AI-native ways of working and tools for Product, Marketing and HR teams, built by ex-McKinsey founders. We map where time and money leak, redesign the work around AI and stay until your people run it themselves, and we run our own company on Claude. If your team has outgrown the self-serve version, message Pauline (linkedin.com/in/paulinebertry).
