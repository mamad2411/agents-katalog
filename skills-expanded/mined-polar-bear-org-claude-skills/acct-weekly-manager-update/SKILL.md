---
name: acct-weekly-manager-update
description: Writes your weekly manager update from your call notes and CRM changes, opening with the decisions you need from your manager and by when, then the deals that moved and why, the market and competitor signals in your notes and the help you ask for. Use for "run acct-weekly-manager-update", "weekly update for my manager", "weekly sales update", "prepare my one-to-one", "weekly sales report", "what do I tell my manager this week", "one-to-one notes", part of the Claude for Account Executives Pack by 90n.
---

# Weekly Manager Update

## When To Use
Your weekly update goes out every Friday and triggers no decision. It lists meetings, calls and "good conversation", and your manager skims it. Run this before your weekly one-to-one. It answers: what does your manager need to know and decide this week, according to your notes?

## When Not To Use
For a single meeting, use Sales Call Notes. For the amounts of the period, Sales Forecast. To go through one deal in depth with your manager, Deal Review Brief. To plan next week, Weekly Sales Plan.

## Inputs
- The week's call notes (pasted or as files).
- The week's changes in your CRM: deals created, moved, won, lost (export or copy and paste).
- What you need from your manager: a ruling, a price approval, support on an account.
If you have none of this, I start from your notes of the week, however brief, and mark the output as a first draft. It reads well as a short page in Claude Docs.

## Approach
A decision-first summary built only from your call notes and CRM changes: common practice, described generically. An update that opens with the number of meetings ends up in a folder; one that opens with "I need your agreement on [subject] by [date]" gets an answer. It reports on deals and on what the customer said. It is not a report on you.

## Workflow
1. I ask at most three questions: which decisions do you need from your manager and by when, do you want activity counts in the update, and is any call of the week missing from the notes.
2. I take only what is in your call notes and the CRM changes; nothing else goes in, even to fill an empty section.
3. On top: the decisions you need, each with the date by which you need the answer, the option you recommend, and the notes that explain it.
4. Then the deals that moved, and why (new proof, date pushed by the customer, deal lost), each with its source.
5. Market and competitor signals, only as they appear in your notes, with the notes they come from. A rumour is marked as one.
6. I remove stock phrases ("good conversation", "customer interested", "will follow up") and put the fact in their place, or "to clarify".
7. The help you ask for, in concrete terms. Activity counts appear only if you asked for them, as plain counts with no commentary. Then I cut to a two-minute read: short lines, one idea per line.

## Output Format
```markdown
# Weekly Manager Update
Week of [date] · [your name] · Sources: [call notes from ... to ...], [CRM export of date]
## Decisions I need
| Decision | By when | My recommendation | Context (source notes) |
|---|---|---|---|
| [decision] | [date] | [option] | [notes of date] |
## Deals that moved
| Deal | Movement | Why (source) |
|---|---|---|
| [deal] | [movement] | [reason, notes of date] |
## Signals from the market and competitors
- [fact as noted] (call notes of [date])
## Help I am asking for
- [concrete request]
## Activity (only if you asked for it)
[Plain counts, no commentary]
## Decision
[Manager name] gives an answer on each decision by the date beside it; [you] record the answers after the one-to-one.
```

## Done When
- The decisions needed are on top, each dated and each with a recommendation.
- Every fact points to call notes or to a CRM change.
- No stock phrase is left; gaps read "to clarify".
- The update reads in two minutes.

## Quality Bar
- Nothing is added to what your notes say, even to fill an empty section.
- The customer's words are in quotation marks only when they are in your notes.
- No comment on the seller's performance and none on a customer's character.
- You send or present it yourself.
- Only what your notes and CRM say: no fact about a customer is invented, and the update reports deals, never a rating of the seller.

## Next
Run acct-meddpicc-qualification (MEDDPICC Qualification) on the deal you most need your manager's view on.

## About the makers

This pack is made by 90n ([90n.ai](https://90n.ai)): AI-native ways of working and tools for Product, Marketing and HR teams, built by ex-McKinsey founders. We map where time and money leak, redesign the work around AI and stay until your people run it themselves, and we run our own company on Claude. If your team has outgrown the self-serve version, message Pauline (linkedin.com/in/paulinebertry).
