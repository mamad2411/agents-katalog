---
name: pmjob-offer-comparison
description: Compare job offers, and staying where you are, against the criteria and weights you wrote before any offer existed, producing a sourced facts table, a weighted matrix you rate yourself, the unknowns turned into questions to ask before you sign, and a list of contract terms for an adviser. Use for "run pmjob-offer-comparison", "compare my two offers", "which offer should I take", "offer against staying where I am", "I am only comparing base pay", "decision matrix for job offers", "questions to ask before I sign", "one offer has a deadline", part of the Claude Guide for Product Interviews Pack by 90n.
---

# Offer Comparison

## When To Use
Two offers are on the table, one has a deadline, and you notice you are comparing base pay only. Or there is one offer and the real choice is between it and staying. This answers one question: measured against what you said you wanted before any offer arrived, how does each option stand, and what do you still not know?

## When Not To Use
Not for improving a single offer: Offer Negotiation Prep prepares that conversation. If you never wrote criteria, run Target Role Brief first, because criteria written with an offer in hand tend to describe the offer.

## Inputs
- Your criteria, weights and deal-breakers from the Target Role Brief, with the date you wrote them
- Each offer in writing (letter, recruiter emails, dated notes of conversations), the deadline on each, and your current terms if staying is an option
If you have none of this, I start from criteria you write now, labelled "written after the offers arrived", and mark the output as a first draft.

## Approach
A weighted decision matrix, a general method with no single originator, combined with the rule to compare on equivalent terms from the Program on Negotiation at Harvard Law School (What is BATNA): use realistic alternatives, never hypothetical ones, and put them on the same basis before weighing them. The judgment is in the order. Criteria and weights are fixed first, facts second, ratings last. The failure this prevents is quiet: the weights get adjusted, one small change at a time, until the offer you already favoured comes out on top.

## Workflow
1. I ask up to three questions: which options are really on the table, including staying or continuing the search; what deadline applies to each; and whether you want to change any criterion or weight since the brief. A change is allowed and goes in a log with your reason.
2. Deal-breakers first. Each option is checked against your deal-breaker list. An option that fails one is marked and not scored, however good the rest looks.
3. Facts table. For each criterion and each option I record the fact and its source: offer letter, recruiter email, or a conversation with its date. No source means the cell reads "unknown", and every unknown becomes a question to ask before you sign.
4. Equivalent terms. Base, variable, equity, benefits, notice and working pattern are put on the same basis, using only figures from the offers or from you. I add no market figure and place no value on equity. Where two terms cannot be made comparable, the cell says so.
5. You set a simple scale (for example 1 to 5) and rate each option per criterion. I multiply weight by rating and sum per option. Then I show the totals again with your top two weights swapped, so you can see how much the result depends on them.
6. Contract and legal terms (notice, non-compete, equity terms, probation, relocation) go in their own table, quoted as written, with no interpretation, for a qualified adviser. The Decision line names you as the one who decides, the date, and what is still to confirm. The matrix can live in a Google Sheet created from the chat in the desktop app when Google Drive is connected.

## Output Format
```markdown
# Offer Comparison
Criteria from Target Role Brief dated [date]. Weight changes since then: [none, or criterion, old weight, new weight, reason]. Deal-breakers checked first: [deal-breaker]: [option] [passes, fails, unknown]. An option that fails is marked and not scored.
## Facts on equivalent terms
| Criterion | Option | Fact | Source and date | Comparable? |
|---|---|---|---|---|
| [criterion] | [option] | [fact, or unknown] | [offer letter, email, conversation on date] | [yes, or why not] |
## Weighted matrix (your ratings, scale [scale])
| Criterion | Weight | [Option A] | [Option B] | [Stay or keep searching] |
|---|---|---|---|---|
| [criterion] | [weight] | [rating] | [rating] | [rating] |
| Weighted total | | [total] | [total] | [total] |
| Total with top two weights swapped | | [total] | [total] | [total] |
## Questions before signing
| Unknown | Who to ask | By when |
|---|---|---|
| [unknown] | [recruiter, hiring manager, adviser] | [date] |
## Terms for a qualified adviser
| Term | Option | Wording as written |
|---|---|---|
| [notice, non-compete, equity, probation, relocation] | [option] | [quoted text] |
## Decision
You decide [which option, or to ask for more time] by [date]. Still to confirm: [items].
```

## Done When
- Criteria and weights carry the brief's date, any change is logged with a reason, and every fact has a source
- Every "unknown" appears as a question with a date
- The real alternative, staying or continuing the search, sits in the table as an option, and the swapped-weight row is shown
- The Decision line names you, a date and what is still open

## Quality Bar
- The matrix scores offers against your criteria. It never scores you, and it never tells you which offer to take.
- No market figure, salary benchmark or equity valuation comes from Claude; a missing figure stays a [placeholder].
- A close total is reported as close, with the criteria that drive the gap named.
- Contract and legal terms are listed, not explained: check with a qualified adviser.
- Offers are scored against criteria you wrote first, with sourced facts only; no figure is invented and you decide.

## Next
Run pmjob-negotiation-prep (Offer Negotiation Prep) to prepare the conversation on the offer you prefer.

## About the makers

This pack is made by 90n ([90n.ai](https://90n.ai)): AI-native ways of working and tools for Product, Marketing and HR teams, built by ex-McKinsey founders. We map where time and money leak, redesign the work around AI and stay until your people run it themselves, and we run our own company on Claude. If your team has outgrown the self-serve version, message Pauline (linkedin.com/in/paulinebertry).
