---
name: firm-recommendation-memo
description: Writes your recommendation on the client's decision as a one-page memo, answer first, with the decision it answers and who decides, the options rejected and why, the costs accepted, the evidence and assumptions as known on the date, what would change it, conditions before action, first steps with owners and a review date, marked proposed until the client's decider decides. Use for "run firm-recommendation-memo", "write my recommendation", "put my advice on one page", "recommendation memo for the client", "what do I actually advise", "answer first memo", "record why I recommend this option", part of the Claude for Consultants · Team in Claude Pack by 90n.
---

# Recommendation Memo

## When To Use
You have the tree, the options, the table and the tests. The client does not want to read them; they want to know what you think and how sure you are. Run this to state your position plainly, with your name on it, and with the reasoning recorded as it stood on the day so it can be judged fairly later.

## When Not To Use
If your contact needs a neutral page to argue internally, use Client Decision Brief; it recommends nothing. To summarise a proposal for its signer, use Proposal Executive Summary. This memo is your advice on their decision, not a sales document.

## Inputs
- The problem statement with its decider, and the options with the trade-off table
- Your pre-mortem and your sensitivity verdict
- The first steps you would advise and who would own them
If you have none of this, I start from your recommendation in two sentences and mark the memo as a first draft with the reasoning sections open. Claude Docs suits a memo you will keep editing; any chat works.

## Approach
Two forms are joined. Answer first, from Barbara Minto's pyramid (barbaraminto.com): the recommendation leads and each line beneath supports the one above. And the decision record of Michael Nygard ("Documenting Architecture Decisions", 2011): context, decision, status, consequences, kept as written. Status is what matters here. A recommendation is proposed until the client's decider acts, and writing it as settled is how advisers end up owning a choice that was never theirs. The failure it prevents is advice nobody can reconstruct six months on.

## Workflow
1. Ask, in one go: what do you recommend, in one sentence? Who decides at the client, and has anything been decided yet? What would you want reviewed, and when?
2. Write the top three lines: the recommendation, the decision it answers, and the decider by role with the date. If you cannot, the thinking is not finished, and I will say which piece is missing.
3. Set the status: proposed (default), conditional on a named condition, or final only if the decider has said so in words you can quote. Silence is never recorded as agreement.
4. Record the options rejected, each with the reason in one line, and the costs your recommendation accepts. A memo that admits no cost is not believed.
5. Write the evidence and assumptions as known on this date, each with its source, and "what would change this" taken from your sensitivity verdict. Leave earlier drafts intact; changes are added with a date, not written over.
6. Add conditions to meet before acting (approvals, a specialist's check), first steps with an owner by role and a date, and a review date with the signals that would reopen the choice. Legal, tax or regulatory conditions: check with a qualified adviser.

## Output Format
```markdown
# Recommendation Memo
To: [client decider role] · From: [your name] · Date: [date] · Status: [proposed / conditional on [condition] / final, per [role] on [date]]
## Recommendation
[One sentence.] It answers: [the decision question]. [Decider role] decides by [date].
- Because: [reason] · Evidence: [source]
## Options not recommended, and costs accepted
| Option | Why not, in one line |
|---|---|
| [option, including current course and in house] | [reason] |
- Accepted cost: [cost or risk, and who bears it]
## Known on this date, and what would change this
- [Evidence or assumption] · [source] · [fact / estimate / assumption]
- Would change this: [from the sensitivity verdict, in one or two sentences]
## Before acting, and first steps
| Condition or step | Owner (role) | By |
|---|---|---|
| [condition or step] | [role] | [date] |
Review on [date], or sooner if [signal].
## Decision
[Client decider role] accepts, amends or declines this recommendation by [date]; [you] sign it and send it yourself.
```

## Done When
- The recommendation, the decision and the decider are in the first three lines
- The status is proposed, conditional or final, and "final" quotes the decider
- Rejected options and accepted costs are both listed
- "What would change this" and a review date are present

## Quality Bar
- One page; the supporting analysis is referenced, not pasted in
- Facts, estimates and assumptions are labelled as such
- No fee, scope or sales line appears; this is advice, not a proposal
- Earlier dated versions are kept, never rewritten after the outcome is known
- I arrange your reasoning and add no evidence of my own; the recommendation is yours, under your name, and the decision is the client's.

## Next
Run firm-good-better-best-options (Good-Better-Best Options) to turn the recommended route into ways the client can buy the work.

## About the makers

This pack is made by 90n ([90n.ai](https://90n.ai)): AI-native ways of working and tools for Product, Marketing and HR teams, built by ex-McKinsey founders. We map where time and money leak, redesign the work around AI and stay until your people run it themselves, and we run our own company on Claude. If your team has outgrown the self-serve version, message Pauline (linkedin.com/in/paulinebertry).
