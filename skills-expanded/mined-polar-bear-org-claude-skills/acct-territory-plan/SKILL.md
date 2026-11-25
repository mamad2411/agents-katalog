---
name: acct-territory-plan
description: Builds your territory plan for the quarter, with accounts tiered A, B and C from your own numbers, a potential column you fill, objectives per tier, a contact rhythm and a quarter calendar with three to five measures. Use for "run acct-territory-plan", "territory plan", "sales plan for the quarter", "account tiering", "tier my accounts", "plan my book of business", "quarterly territory plan template", "where should I spend my time this quarter", part of the Claude for Account Executives Pack by 90n.
---

# Territory Plan

## When To Use
You are asked for your plan for the quarter and all you have is a list of accounts. Run this at the start of a quarter. It answers: on which accounts do you put your time, for which objectives, and at what rhythm?

## When Not To Use
To work one account in depth, run Account Plan. To place this week's hours, run Weekly Sales Plan. With no figure per account at all, export your CRM first: without numbers a tiering is an impression.

## Inputs
- Your account list with your own revenue or margin per account (CRM export or spreadsheet).
- The objectives your leadership set for the quarter.
- Your estimate of each account's potential, if you have one.
If you have none of this, I start from your account list, leave the number columns empty and mark the output as a first draft. With the desktop Output picker and Google Drive connected the table can go to Google Sheets; any spreadsheet works by copy and paste.

## Approach
Account tiering on the Pareto principle, and objectives written to be specific, measurable, achievable, relevant and time-bound: two common practices, described here generically. The judgment is that today's revenue does not tell the whole story, so a potential column sits beside the ranking. The failure it prevents: a quarter spent on the accounts that call loudest instead of the ones that matter.

## Workflow
1. I ask at most three questions: which criterion ranks your accounts (revenue or margin), where do you put the thresholds between A, B and C, and which objectives did leadership set.
2. I rank the accounts by your criterion, largest first, and compute each account's cumulative share of the total. You set the A, B and C thresholds; I propose no default.
3. I add a potential column that you fill, so a small account with real potential does not vanish into C. Where you move an account up a tier on potential, I note the reason beside it.
4. Per tier I write two objectives: one on a result, and one on activity you control (conversations, meetings, proposals), because a result you do not control needs an activity you do.
5. Per tier you set the contact rhythm; I lay it over a quarter calendar week by week and flag any week that cannot hold it alongside meetings and follow-ups.
6. You choose three to five measures; I tie each one to an objective and drop any measure tied to none.

## Output Format
```markdown
# Territory Plan
Quarter: [quarter, year] · Owner: [name] · Ranking criterion: [revenue or margin]
## Account tiers
| Account | [Revenue or margin] | Cumulative share | Tier (your thresholds) | Potential (you) | Note |
|---|---|---|---|---|---|
| [account] | [your figure] | [computed] | [A, B or C] | [yours] | [reason if moved] |
## Objectives per tier
| Tier | Result objective | Activity objective you control | By |
|---|---|---|---|
| A | [objective] | [objective] | [date] |
## Contact rhythm
| Tier | Actions | Rhythm (set by you) |
|---|---|---|
| A | [actions] | [rhythm] |
## Quarter calendar and measures
| Week | Planned actions | Measure followed |
|---|---|---|
| [week] | [actions] | [measure] |
## Decision
[Manager name] approves the tiers and objectives by [date]; [you] set the date of the first check-in.
```

## Done When
- Every amount comes from your figures, and the A, B and C thresholds are yours.
- The potential column exists, even partly filled.
- Each tier has one result objective and one activity objective, both dated.
- Each measure is tied to an objective.

## Quality Bar
- Tiers apply to accounts, never to people: no ranking of contacts or of sellers.
- The calendar fits a real working week, follow-ups included.
- No benchmark, quota or target appears that you or your leadership did not give.
- Tiers and objectives come from your own numbers only: no figure is invented.

## Next
Run acct-buying-signals (Buying Signals Brief) to find a dated public reason to call your A and B accounts.

## About the makers

This pack is made by 90n ([90n.ai](https://90n.ai)): AI-native ways of working and tools for Product, Marketing and HR teams, built by ex-McKinsey founders. We map where time and money leak, redesign the work around AI and stay until your people run it themselves, and we run our own company on Claude. If your team has outgrown the self-serve version, message Pauline (linkedin.com/in/paulinebertry).
