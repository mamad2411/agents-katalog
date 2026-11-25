---
name: acct-sales-forecast
description: Builds your sales forecast with deals placed in commit, best case or pipeline by a rule you write, the proof cited per deal, totals from your CRM only, the changes since last week with a reason for each and what is missing to move a deal up. Use for "run acct-sales-forecast", "sales forecast", "forecast call prep", "what should I commit this quarter", "commit best case pipeline", "prepare my forecast for my manager", "forecast categories", "defend my number", part of the Claude for Account Executives Pack by 90n.
---

# Sales Forecast

## When To Use
Your forecast rests on a feeling and your manager marks it down. Deals move from one category to another and nobody can say why. Run this before your forecast call. It answers: which deals can you call for the period, on which written proof, and what changed since last week?

## When Not To Use
If your deals are not qualified or your stages no longer mean anything, start with Pipeline Review. To tell your manager about the week, use Weekly Manager Update.

## Inputs
- Your CRM export for the period: deal, amount, close date, stage. Salesforce in Claude (beta) reads it directly; any CRM works by export or copy and paste.
- Last week's forecast, for the changes.
- The evidence per deal: emails, call notes, your latest Pipeline Review.
If you have none of this, I start from a list of your deals for the period with their amounts and mark the output as a first draft, categories to confirm.

## Approach
Forecast categories with evidence per deal. The names commit, best case and pipeline are the standard forecast category names in Salesforce Help; the rule that puts a deal in each one is yours, written down. A probability-weighted pipeline gives an impression of precision that hides missing evidence, so nothing here is weighted unless you supply the weights and ask for it. A category is a claim, and each claim sits next to its proof.

## Workflow
1. I ask at most three questions: what is your written rule for each category (for example, commit means a written commitment from the signer on amount and date), which period does the forecast cover, and where is last week's forecast.
2. I apply your rules to each deal and cite the proof that places it (email of [date], call notes of [date]). With no proof the deal moves down a category or stays out of the forecast.
3. Amounts and close dates come only from the CRM export or from you. I total each category and present no weighted figure as a truth.
4. Changes since last week: each movement (in, out, category change, date moved, amount changed) gets its reason: new proof, date pushed by the customer, deal lost.
5. For each best case deal, the proof missing to move it to commit, and who can obtain it by when.
6. Risks on commit deals: a dependency, a tight date, a signer you have not met, a paper process nobody has described.
7. If your rule and your manager's differ, I show the deals the difference touches, so the call is about the rule and not about your optimism.

## Output Format
```markdown
# Sales Forecast
Period: [period] · Source: [CRM export of date] · Prepared: [date]
Rules (yours): commit = [rule] · best case = [rule] · pipeline = [rule]
## Deals by category
| Deal | Amount (CRM) | Close date (CRM) | Category | Proof (source, date) |
|---|---|---|---|---|
| [deal] | [amount] | [date] | [commit / best case / pipeline] | [proof] |
Totals (CRM): commit [sum] · best case [sum] · pipeline [sum]
## Changes since last week
| Deal | Movement | Reason |
|---|---|---|
| [deal] | [movement] | [reason] |
## To move up to commit
| Best case deal | Missing proof | Who obtains it, by when |
|---|---|---|
| [deal] | [proof] | [name, date] |
## Risks on commit deals
- [deal]: [risk]
## Decision
[You] call [commit only / commit and best case] on [date]; [manager name] confirms or challenges it on the forecast call.
```

## Done When
- Every deal in a category cites a dated written proof.
- Every amount matches the CRM export or a figure you gave.
- Every change since last week has a reason.
- The rules for the three categories are written at the top, in your words.

## Quality Bar
- No probability percentage is presented as a truth.
- No comparison between sellers and no ranking of people.
- A deal with a missing signer or an unknown paper process is not commit by default; you decide, with the gap in view.
- The table can go to Google Sheets through the desktop Output picker when Google Drive is connected.
- Figures come from your CRM only: no amount, probability or win rate is invented.

## Next
Run acct-stalled-deals (Stalled Deals Review) to deal with the deals that fell out of the forecast for lack of movement.

## About the makers

This pack is made by 90n ([90n.ai](https://90n.ai)): AI-native ways of working and tools for Product, Marketing and HR teams, built by ex-McKinsey founders. We map where time and money leak, redesign the work around AI and stay until your people run it themselves, and we run our own company on Claude. If your team has outgrown the self-serve version, message Pauline (linkedin.com/in/paulinebertry).
