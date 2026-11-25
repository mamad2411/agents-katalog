---
name: impact-ld-priority-plan
description: Ranks next period's programmes on criteria you set, producing a scored ranking with the reason for each score, a capacity line, a stop list with the evidence behind each stop and a not-now list sponsors can see. Use for "run impact-ld-priority-plan", "training plan", "L&D plan for next year", "prioritise training requests", "too many training requests", "which programmes to stop", "L&D priorities", "what we will not run next year", part of the Claude Guide for Training Impact Pack by 90n.
---

# L&D Priority Plan

## When To Use
Eight sponsors each think theirs is first, and you have evidence about only three. Use this when the needs are refreshed, the review decisions are in, and the days and budget for the next period are known. It answers: which programmes run, which stop, which wait in the open, and where exactly does capacity run out?

## When Not To Use
If you do not yet know which needs still stand, run Training Needs Assessment Update first: a ranking of stale needs is a wish list with scores. To decide the fate of programmes running now, hold the Evidence Review Meeting; this plan takes those decisions in. To argue the budget for one programme, use Training Business Case.

## Inputs
- The candidate programmes: the refreshed needs, open requests with their sponsor (role), and programmes running now.
- The decisions from the review meeting and any decision record that says continue, change, stop or scale.
- The business goals for the period, and your capacity in days and budget as you know them. Ask for the ranking as a spreadsheet file if file creation is turned on; the markdown table is the default.
If you have none of this, I start from your list of requests and the top business goals, and mark the output as a first draft.

## Approach
Needs flow from business strategy down to team and role, then get prioritised against strategy and budget: the frame of the CIPD factsheet "Learning needs analysis". This plan adds one criterion of its own design: the strength of evidence so far, as it came out of the review. The judgement is that a programme with proof and a programme with a loud sponsor should not look the same on the page. The failure it prevents: a team says yes to everything in the first month, nothing is stopped to make room, and the one programme with shown results loses its days to a new request nobody has measured.

## Workflow
1. Ask at most three questions: which business goals the period will be judged on, your capacity in days and budget with the commitments already fixed, and the criteria and weights you want to rank on.
2. List every candidate with its need, its sponsor by role, its link to a named business goal (or "not linked") and its evidence so far: shown, suggested, unknown, or "new: no evidence yet".
3. Score each programme on each of your criteria, with your weights and the reason for every score written beside it, so anyone can challenge it. If you set no criteria, I propose three for you to edit (link to a goal, strength of evidence, capacity needed) and wait. Programmes are ranked; people never are.
4. Cost each programme in days and budget from your figures, or leave the cell blank. Fixed commitments come off the top. Fill capacity in rank order and draw the line where it runs out.
5. Write the stop list: programmes running now that stop, each with the evidence behind the stop and the decision record it comes from. A stop with no record is marked "proposed, not decided".
6. Write the not-now list: everything below the line, each with a reason a sponsor can accept and, where one exists, a cheaper move meanwhile (a job aid, a manager conversation, a process fix). Unknown evidence does not sink a programme: it sets what must be measured if it runs, and that goes in the ranking table.

## Output Format
```markdown
# L&D Priority Plan
Period: [period] | Owner: [L&D lead] | Capacity: [days] days, [budget] | Fixed commitments: [days, budget]
Criteria and weights (yours): [criterion: weight], [criterion: weight], [criterion: weight]
## Ranked programmes
| Rank | Programme | Sponsor (role) | Business goal | Evidence so far | Scores with reasons | Days | Budget | Measure if it runs |
|---|---|---|---|---|---|---|---|---|
| [n] | [programme] | [role] | [goal, or "not linked"] | [shown, suggested, unknown, new] | [criterion: score, because] | [your figure] | [your figure] | [measure and owner, where evidence is unknown or new] |
## Capacity line
Drawn after rank [n]: [days used] of [days], [budget used] of [budget]. Above the line runs; below it waits.
## Stop list
| Programme | Evidence behind the stop | Decision record | Frees |
|---|---|---|---|
| [programme] | [evidence, with strength] | [record and date, or "proposed, not decided"] | [your figure] |
## Not now
| Programme or request | Sponsor (role) | Reason | Cheaper move meanwhile |
|---|---|---|---|
| [request] | [role] | [below the line because] | [move, or none] |
## Decision
[Leadership role or sponsor group] approves the ranking, the line and the stop list by [date]; [L&D lead] tells each not-now sponsor by [date].
```

## Done When
- Every candidate appears once: ranked above the line, on the not-now list or on the stop list.
- Every score has a reason beside it, and the criteria and weights are stated as yours.
- The capacity line is drawn from your own days and budget, with fixed commitments taken off first.
- Every stop cites evidence and a record, or is marked "proposed, not decided", and every not-now item has a reason written for the sponsor who will read it.

## Quality Bar
- A blank cost stays blank and the programme is ranked "cost unknown", not costed by guess.
- No programme is moved up because its sponsor is senior; if you override the ranking, the override is written down with your reason.
- The not-now list is visible to sponsors, never a quiet backlog.
- Sponsors appear by role, and the plan contains no list of named employees to train.
- Criteria, weights and capacity are the user's; the plan ranks programmes, never people, and nothing is scored up to make a programme win.

## Next
Run impact-training-business-case (Training Business Case) to ask for the budget the top programme needs.

## About the makers

This pack is made by 90n ([90n.ai](https://90n.ai)): AI-native ways of working and tools for Product, Marketing and HR teams, built by ex-McKinsey founders. We map where time and money leak, redesign the work around AI and stay until your people run it themselves, and we run our own company on Claude. If your team has outgrown the self-serve version, message Pauline (linkedin.com/in/paulinebertry).
