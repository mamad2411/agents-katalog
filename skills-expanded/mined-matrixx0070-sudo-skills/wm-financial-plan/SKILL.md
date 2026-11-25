---
name: wm-financial-plan
version: 1.0.0
description: Draft the structure of a comprehensive financial plan — goals, cash flow, net worth, risk, retirement projection, and scenario stress — as advisory support.
author: matrixx0070
tags: [wealth-management, financial-plan, goals, cash-flow, retirement, projection]
capabilities: []
---

## When to use

Reach for this when you are an advisor or paraplanner building the skeleton of a full financial plan and want a disciplined order of operations: gather, quantify goals, project, stress-test, and summarize. Use it to organize a discovery-to-plan workflow, not to produce individualized recommendations.

**Not for:** picking specific securities (wm-investment-proposal), executing trades (wm-portfolio-rebalance), or the review meeting (wm-client-review). This is educational and advisory-support only — projections are illustrations, not guarantees, and not personalized investment or tax advice. Route decisions to a licensed advisor and tax questions to a tax professional.

## Method

1. **Gather the baseline** — net worth (assets, liabilities), income, and expenses. Build a current cash-flow statement before projecting anything.
2. **Quantify goals** — for each goal (retirement, education, home, legacy), capture target amount, target date, and priority. Decision point: if goals collectively exceed capacity, surface the conflict and rank rather than assume all are fundable.
3. **Set assumptions explicitly** — inflation, expected return by asset class, savings rate, retirement age, longevity, and tax drag. Every assumption is stated and labeled as an assumption, so the plan can be re-run when they change.
4. **Project** — model funding trajectories to each goal using the stated assumptions. Show the base case in plain terms (funded / underfunded and by how much).
5. **Stress-test** — run at least a downside scenario (lower returns, earlier retirement, longer life, or a large expense shock) and report how the plan holds up.
6. **Summarize gaps and levers** — for any underfunded goal, describe the levers (save more, spend less, work longer, adjust the goal) as options, not directives.

## Example

A couple wants to retire at 60 and fully fund two college educations. Weak: "You're on track." Strong: "Under base assumptions (3% inflation, 5.5% real return, retire at 60), the retirement goal is ~85% funded and both education goals are fully funded — but a 2%-lower return shaves retirement funding to ~68%. The levers are: retire at 62, raise savings by $900/month, or reduce the target lifestyle by ~10%. Which trade-off fits your priorities?" Assumptions are explicit and the shortfall is expressed as choices.

## Pitfalls

- Burying assumptions so no one can re-run the plan when reality shifts — state every one.
- Presenting a single deterministic projection as certainty; always show a downside case.
- Modeling all goals as fully fundable without testing capacity or forcing prioritization.
- Sliding from illustration into personalized advice; keep levers as options and route decisions to a licensed advisor and a tax professional.

## Output format

```
Client: [name(s)] | Plan date:
Baseline: net worth [assets/liabilities], income, expenses, current cash flow
Goals: [goal | target $ | target date | priority]
Assumptions (labeled): inflation, return by asset class, savings rate, retirement age, longevity, tax drag
Base-case projection: [per goal: funded % / surplus or shortfall]
Stress test: [scenario | impact on each goal]
Gaps & levers: [underfunded goal | options: save more / spend less / work longer / adjust goal]
Disclosures: illustration only, not a guarantee; not personalized investment or tax advice
```

## Reference

CFP Board financial-planning process (establish, gather, analyze, develop, present, implement, monitor). Confirm firm assumption-setting and disclosure standards; projections are hypothetical.
