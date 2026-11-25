---
name: acct-deal-review
description: Writes a one-page deal review brief as the pre-read for your weekly review of one deal, with the overview, impact, people by role, decision, competition, what is known with its proof and what is not known yet, a pre-mortem and the help and decisions you ask for. Use for "run acct-deal-review", "deal review", "prepare my deal review", "opportunity review", "deal review template", "pre-read for my manager on this deal", "deal inspection", "pre-mortem on this deal", part of the Claude for Account Executives Pack by 90n.
---

# Deal Review Brief

## When To Use
Your deal reviews are status updates and the plan for the deal never changes. Run this the day before the weekly review of one deal with your manager. It answers: what should happen next on this deal, and what do you need from the person across the table to make it happen?

## When Not To Use
For the whole week across all deals, use Weekly Manager Update. For a first qualification of a deal nobody has examined, run MEDDPICC Qualification. After the customer has decided, run Win/Loss Review.

## Inputs
- Your MEDDPICC Qualification Note, or your notes and the CRM record for the deal.
- Last week's review actions and what became of each.
- Where you need support: access, a price ruling, a resource, a second opinion.
If you have none of this, I start from the deal in one paragraph and mark the output as a first draft with most cells reading "not known yet". It works well as a page in Claude Docs.

## Approach
The format follows Insight Partners' public guidance on running effective deal reviews (insightpartners.com): weekly, one manager and one seller, an overview sent ahead, then impact, people, decision and competition, starting from last week's actions, with room to say "I do not know yet". To that I add a pre-mortem (Harvard Business Review, September 2007): assume the deal was lost three months from now and list why. The question in the room is "what should happen next?", not "what is happening?". The brief reviews the deal, never the seller.

## Workflow
1. I ask at most three questions: which deal, what happened to last week's actions, and where you need your manager's help.
2. Last week's actions first: each one done, not done or changed, with the reason. Commitments that slip unseen are how reviews stop mattering.
3. The overview, for sending ahead: what the account does and your relationship with it, the amount, stage and close date from the CRM, the next step, and where you need support.
4. Four sections, each split into "known, with proof" and "not known yet". Impact: metrics and pain, and the cost of not solving it in the customer's figures. People: the economic buyer, the champion role and others by role, with dated actions. Decision: criteria and process, with owners and dates. Competition: other vendors, in-house options and doing nothing.
5. "Not known yet" is a full answer. Each one gets the step that will find out and the date, so it is a plan and not a gap to defend.
6. The pre-mortem: if this deal is lost in three months, why? Three to five causes about the deal (a role never met, a criterion you do not meet, a step in the paper process), each with the action that reduces it and an owner.
7. The asks: the decisions and help you need, each with a date. I cut to one page.

## Output Format
```markdown
# Deal Review Brief
Deal: [name] · Amount, stage, close date (CRM): [values] · Review: [date] with [manager name]
## Last week's actions
| Action | Done / not done / changed | Why |
|---|---|---|
| [action] | [status] | [reason] |
## Overview (pre-read)
[Account and relationship in two lines] · Next step: [who, what, date] · Support needed: [where]
## Known and not known yet
| Section | Known, with proof (source, date) | Not known yet | Step to find out, by when |
|---|---|---|---|
| Impact | [fact] | [gap] | [step, date] |
| People (by role) | [fact] | [gap] | [step, date] |
| Decision / Competition | [fact] | [gap] | [step, date] |
## Pre-mortem: lost in three months, why?
| Cause | Action that reduces it | Owner | Date |
|---|---|---|---|
| [cause about the deal] | [action] | [name] | [date] |
Asks: [decision or help needed] by [date]
## Decision
[Manager name] and [you] agree in the review of [date] what happens next on this deal and who does it.
```

## Done When
- Last week's actions are each accounted for.
- Every "known" cell has a proof with its source, and every "not known yet" has a step and a date.
- The pre-mortem lists three to five causes with an action and an owner each, and the brief fits one page and ends with dated asks.

## Quality Bar
- Amount, stage and close date come from the CRM, unchanged.
- No deal score and no probability.
- Pre-mortem causes are about the deal and its steps, never about a person on either side.
- The brief reviews the deal, never the seller: nothing in it rates anyone, and nothing unproven is written as known.

## Next
Run acct-win-loss-review (Win/Loss Review) once the customer has decided, to learn what counted.

## About the makers

This pack is made by 90n ([90n.ai](https://90n.ai)): AI-native ways of working and tools for Product, Marketing and HR teams, built by ex-McKinsey founders. We map where time and money leak, redesign the work around AI and stay until your people run it themselves, and we run our own company on Claude. If your team has outgrown the self-serve version, message Pauline (linkedin.com/in/paulinebertry).
