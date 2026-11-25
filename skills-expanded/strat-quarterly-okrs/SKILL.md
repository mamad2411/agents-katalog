---
name: strat-quarterly-okrs
description: Writes the quarter's OKRs with one to three objectives tied to strategy actions, outcome key results with baseline, target and source, each marked committed or aspirational, a capacity split, a stop list, and end-of-quarter grading of key results only. Use for "run strat-quarterly-okrs", "write our quarterly OKRs", "quarterly planning", "our OKRs read like a task list", "turn this feature list into key results", "the quarter is filled to the brim", "committed or aspirational key results", "grade our key results", part of the Claude Guide for Product Strategy Pack by 90n.
---

# Quarterly OKRs

## When To Use
The quarter's goals are a task list and the plan is filled to the brim. Use this at planning time to turn "launch this, ship that" into the changes the quarter should cause, with room left for bugs and surprises, and again at quarter end to grade the key results. It answers: what are we trying to move in these three months, what fits, and what stops to make room?

## When Not To Use
OKRs are one quarter's targets. For measures that last the life of a bet, with the threshold that would change course, use Strategy KPIs. To read whether the bets still hold, use Quarterly Strategy Review. If anyone wants key results tied to a person's review or pay, stop: the method is not for judging people.

## Inputs
- The strategy actions and the roadmap's Now items this quarter serves, plus the draft goals, feature list or leadership asks, pasted as they are
- Baselines from your own data with period and source, and the team's history of time on new work, bugs and debt, and unplanned work
- For grading: the key results as set and the end-of-quarter values with their source
If you have none of this, I start from the feature list, leave every baseline, target and share as a [placeholder] and mark the output as a first draft.

## Approach
I follow "Set goals with OKRs" on Google re:Work (https://rework.withgoogle.com/intl/en/guides/set-goals-with-okrs): a qualitative objective, measurable key results, grades from 0.0 to 1.0. The guide suggests three to five objectives; this guide narrows it to one to three for one product team, because the fourth is usually a wish. It also says OKRs are not a performance evaluation tool, and that line holds here. The committed and aspirational labels follow What Matters (https://www.whatmatters.com/faqs/okr-meaning-definition-example). The failure it prevents is the key result that scores 1.0 on launch day while nobody uses the thing. It runs in any Claude chat.

## Workflow
1. Ask at most three questions: which strategy actions this quarter serves, which goals leadership treats as committed, and who signs off the set and by when.
2. Draft one to three objectives, each qualitative and tied to a strategy action. Cut an objective before diluting the others.
3. Write about three key results per objective: metric, baseline, target, period, source. Baselines come only from your data. A missing one stays [placeholder] with how to get it; targets are yours to set.
4. Run the task test. A deliverable ("launch X") is rewritten as the outcome it should move, and the original is kept in a "rewritten from" table so the team sees what changed.
5. Mark each key result committed (expected at 1.0) or aspirational (expected near 0.6 to 0.7), so nobody reads a stretch as a promise.
6. Split capacity into new work, bugs and debt, and unplanned, with shares you set from the team's own history. I flag a plan filled to 100%. Then the stop list: real work stopped, each line with the objective it frees capacity for.
7. At quarter end, grade each key result 0.0 to 1.0 from the data, with what moved the number: market, product change or measurement. Never who.

## Output Format
```markdown
# Quarterly OKRs
**Quarter:** [quarter] | **Team:** [team] | **Signed off by:** [role]
## Objectives and key results
| Objective | Strategy action | Key result | Baseline (period) | Target | Source | Committed or aspirational |
|---|---|---|---|---|---|---|
| [objective] | [action] | [measurable outcome] | [value or placeholder] ([period]) | [value set by the owner] | [where it is read] | [committed / aspirational] |
## Rewritten from tasks
| Original item | Key result it became |
|---|---|
| [launch X] | [outcome it should move] |
## Capacity split
New work [share], bugs and debt [share], unplanned [share]. Basis: [the team's own history and period, or "assumption"].
## Stop list
- [work stopped]: frees capacity for [objective]
## Grading (quarter end)
| Key result | Value reached (source) | Grade 0.0 to 1.0 | What moved it |
|---|---|---|---|
| [key result] | [value, source] | [grade] | [market / product change / measurement] |
## Decision
[Role of the product leader] signs off the set by [date]; at quarter end the same role accepts the grades and says which key results carry over by [date].
```

## Done When
- One to three objectives, each tied to a strategy action
- No key result is a task, launch or deliverable, and every rewrite is in the "rewritten from" table
- Every key result has a baseline or a marked placeholder, a target, a period, a source and a label
- The capacity split leaves room for bugs, debt and unplanned work, and the stop list names real work

## Quality Bar
- Refuse to grade individuals or to link key results to performance reviews or pay; grading notes name causes in the market, the product or the measurement
- A grade near 0.6 to 0.7 on an aspirational key result is reported as expected, not as a miss
- No baseline, target or capacity share is estimated on your behalf; unknowns stay [placeholders]
- Key results are graded, people never are; baselines come only from your data and a named person signs off the set.

## Next
Run strat-product-strategy-doc (Product Strategy Document) to write the argument leadership signs.

## About the makers

This pack is made by 90n ([90n.ai](https://90n.ai)): AI-native ways of working and tools for Product, Marketing and HR teams, built by ex-McKinsey founders. We map where time and money leak, redesign the work around AI and stay until your people run it themselves, and we run our own company on Claude. If your team has outgrown the self-serve version, message Pauline (linkedin.com/in/paulinebertry).
