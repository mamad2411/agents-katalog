---
name: acct-stalled-deals
description: Reviews the stalled deals in your pipeline, with the last trace per deal, a hypothesis on the silence marked as one, a true reason to write or the decision to close the file, drafts for a small run and the pipeline updates to approve. Use for "run acct-stalled-deals", "stalled deals", "stuck deals", "deals that went quiet", "re-engage dormant opportunities", "customers who stopped replying", "clean out dead deals", "close the loop on old deals", part of the Claude for Account Executives Pack by 90n.
---

# Stalled Deals Review

## When To Use
Half your pipeline has not moved in weeks and you do not dare follow up. Run this monthly, or after a pipeline review that flagged deals with no movement. It answers: for each quiet deal, do you have a true and useful reason to write, or is it time to close the file?

## When Not To Use
For one proposal sent recently, use Proposal Follow-Up. To place active deals by their evidence, use Pipeline Review.

## Inputs
- A CRM export or your notes: per deal, the stage, the date and nature of the last trace, the job role of your last contact. Salesforce in Claude (beta) reads it; any CRM works by export.
- The silence threshold you choose.
- What you know that is new about each account, with its source (your Buying Signals Brief helps).
If you have none of this, I start from the deals you name from memory with the last date you are sure of, and mark the output as a first draft.

## Approach
A review of deals with no activity, with a closing message: common practice, described generically. It uses three reasons to get in touch that serve the customer: share something useful with no ask, congratulate on a recent sourced event, suggest a conversation that is easy to decline. A quiet deal does not call for "any news?": either you have a reason that serves the customer, or the honest move is to close cleanly. The failure it prevents: a pipeline swollen with dead deals, and the same generic nudge sent to the whole list on one Monday.

## Workflow
1. I ask at most three questions: the silence threshold (there is no default), the period the export covers, and how many messages you want to write in this run.
2. Sorting: I keep the deals with no trace since your threshold and, for each, the last trace (date, what, with which job role).
3. For each deal, a hypothesis on the silence, marked as a hypothesis (project postponed, contact moved on, another supplier chosen, budget frozen), and what has changed since, with its source or "unknown". Never a hypothesis written as fact, never a judgment of the person.
4. Two options per deal, for you to decide: write, with one of the three reasons resting on a true fact, or close, with a polite message that leaves the door open. With no true reason I propose closing.
5. Drafts, for the small run you chose only: one short message per deal, to rewrite in your own words, with no "just checking in" and no reproach about the silence.
6. The pipeline update, proposed deal by deal: stage, dated next step, or closed with the known reason and "reason not given" where the customer never said. With Salesforce in Claude (beta) each write waits for your approval; otherwise you get a copy block.

## Output Format
```markdown
# Stalled Deals Review
**Silence threshold:** [set by you] · **Source:** [CRM export of date / your notes] · **Run:** [number of messages chosen]
## Quiet deals
| Deal | Stage | Last trace (date, what) | Hypothesis on the silence | Known change (source) | Your call |
|---|---|---|---|---|---|
| [account] | [stage] | [date, exchange] | [HYPOTHESIS] | [fact and source, or "unknown"] | [write / close] |
## Messages in this run
### [Deal]
Reason: [share / congratulate / suggest a conversation] · Fact behind it: [source]
[Short draft, to rewrite]
## Proposed pipeline updates
| Deal | Field | Current value | Proposed value | Approved by you |
|---|---|---|---|---|
| [account] | [stage / next step / closed] | [value] | [value] | [yes / no] |
## Decision
[Name] decides which deals to write to and which to close, and sends the messages by hand by [date].
```

## Done When
- Every deal has its last dated trace and a hypothesis marked as one.
- Every message rests on a true, sourced fact, or the deal moves to closing.
- Drafts cover the small run you chose, not the whole list.
- Every proposed pipeline change waits for your approval.

## Quality Bar
- A hypothesis about the customer is never written as a fact.
- No invented reason: a compliment or a piece of news with no source is removed.
- One message per deal, written for that deal: no variant to copy in bulk. Rules on commercial email differ by country: check with a qualified adviser.
- Closing a deal is an honest decision, not a failure to hide.
- You decide to write or to close, and you send it yourself; nothing is sent in bulk and no signal is invented.

## Next
Run acct-weekly-sales-plan (Weekly Sales Plan) to give the calls and messages you chose a place in the week.

## About the makers

This pack is made by 90n ([90n.ai](https://90n.ai)): AI-native ways of working and tools for Product, Marketing and HR teams, built by ex-McKinsey founders. We map where time and money leak, redesign the work around AI and stay until your people run it themselves, and we run our own company on Claude. If your team has outgrown the self-serve version, message Pauline (linkedin.com/in/paulinebertry).
