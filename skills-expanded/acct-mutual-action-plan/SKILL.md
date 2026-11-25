---
name: acct-mutual-action-plan
description: Drafts a mutual action plan with the dated steps on both sides from the customer's yes to signature and start, an owner per step by role, the dependencies, each step marked proposed or agreed and a cover note that invites the customer to change it. Use for "run acct-mutual-action-plan", "mutual action plan", "close plan with the customer", "mutual success plan", "the customer said yes and nothing moves", "steps to signature", "who owns legal and procurement", "the deal keeps slipping", part of the Claude for Account Executives Pack by 90n.
---

# Mutual Action Plan

## When To Use
The customer says yes and the deal slips month after month. Nobody wrote down what has to happen on their side before signature: technical validation, security, legal, procurement. Run this once you have agreement in principle. It answers: which steps, owned by whom and by when, must be done to start on the date the customer wants?

## When Not To Use
With no agreement in principle the plan will read as pressure: go back to Negotiation Plan or Discovery Call Questions. To organise your own time, use Weekly Sales Plan.

## Inputs
- The start date the customer wants, in their words, with its source and why it matters to them.
- What you know about their process: who validates the technical side, security, legal and procurement, and who signs (your Stakeholder Map if you have it).
- Your own steps: final proposal, contract, preparing the start.
If you have none of this, I start from the standard steps with no dates, mark each as an assumption to check with the customer, and mark the output as a first draft.

## Approach
A mutual action plan is a closing practice, described here generically: both sides write the steps to signature together, each with an owner and a date. It gives a shape to what the MEDDPICC method calls the paper process, the steps that take a deal from decision to signature (meddicc.com). It starts from the customer's date, not from your quarter end, which is what makes it acceptable. Sent as a timetable it reads as pressure; built with the customer it surfaces the procurement step nobody mentioned until week five.

## Workflow
1. I ask at most three questions: which start date did the customer give and where, who on their side validates each step, and which steps have they already accepted.
2. I work back from the start date: kick-off, signature, contract review, procurement or supplier setup, security or data checks, technical validation, budget approval. I add any step the customer named, and leave none out because it feels awkward to ask about.
3. Each step gets an owner on the customer side and one on yours, by job role (or "unknown"), a date, and what it needs from the other side. I never guess a person's name.
4. Dependencies: what blocks what (legal waits for the final proposal). A date that ignores a dependency is flagged.
5. The arithmetic of time: where the steps cannot fit before the start date, I say so and show the earliest realistic start. I do not squeeze the dates.
6. Status: "agreed" only if the customer accepted it, with the source; otherwise "proposed". Every step with no owner or no date becomes a question for your contact. Contract clauses are not drafted here.
7. I draft the cover note: the plan is offered as a proposal, with a question that invites the customer to correct it. You rewrite it and send it yourself. It shares well as a page in Claude Docs.

## Output Format
```markdown
# Mutual Action Plan
Deal: [name] · Start date the customer wants: [date], because [their reason], source: [source] · Status: proposed, to agree
## Steps from yes to start
| Step | Customer owner (job role) | Your owner | Done by | Depends on | Status |
|---|---|---|---|---|---|
| Technical validation | [role or unknown] | [name] | [date] | [step] | proposed / agreed |
| Security or data check | [role] | [name] | [date] | [step] | proposed / agreed |
| Legal review | [role] | [name] | [date] | [step] | proposed / agreed |
| Procurement | [role] | [name] | [date] | [step] | proposed / agreed |
| Signature | [role] | [name] | [date] | [step] | proposed / agreed |
| Start | [role] | [name] | [date] | [step] | proposed / agreed |
## Gaps and questions
- [Step with no owner or date]: [question for your contact]
- Earliest realistic start if the dates do not fit: [date]
## Cover note (draft)
[Three or four lines inviting the customer to correct the plan]
## Decision
[Customer role] and [you] agree the plan, or change the start date, on the call of [date].
```

## Done When
- Every step has two owners (or "unknown"), a date and a status.
- No step reads "agreed" without a trace of the customer's agreement.
- Dependencies are noted and no date contradicts them.
- The cover note invites the customer to correct the plan.

## Quality Bar
- The plan starts from the customer's date, never from your quarter target.
- Customer steps are written in their process words, not your sales stages.
- Your own steps are in it too; mutual means you carry dates as well.
- Contract, procurement and data points: check with a qualified adviser.
- Proposed to the customer, never imposed: no step is marked agreed without their word, and you send it.

## Next
Run acct-pipeline-review (Pipeline Review) to put this deal back among all the others, at the stage its evidence supports.

## About the makers

This pack is made by 90n ([90n.ai](https://90n.ai)): AI-native ways of working and tools for Product, Marketing and HR teams, built by ex-McKinsey founders. We map where time and money leak, redesign the work around AI and stay until your people run it themselves, and we run our own company on Claude. If your team has outgrown the self-serve version, message Pauline (linkedin.com/in/paulinebertry).
