---
name: strat-market-sizing
description: Builds a TAM, SAM and SOM estimate from top-down and bottom-up sizing as low, base and high, with every input sourced or labelled assumption, the gap between the two methods shown and the share of the reachable market the plan needs. Use for "run strat-market-sizing", "market sizing", "TAM SAM SOM", "how big is this market", "bottom-up market size", "is this market big enough", "where does that number come from", part of the Claude Guide for Product Strategy Pack by 90n.
---

# Market Sizing (TAM, SAM, SOM)

## When To Use
Leadership asks how big this is, and the number must survive "where does that come from?" Use this when a segment, an opportunity or a new bet in the strategy needs a size, to answer: how much demand exists, how much of it can we reach, and how much does the plan need to win?

## When Not To Use
With no published total and no customer counts of your own, a size is a guess in a table: run Lean Canvas to test the bet's logic first. To model how options play out under different conditions, run Scenario Planning Model; to cost the chosen option for the person who funds it, run Business Case.

## Inputs
- Any published market total you trust, with its source and year
- Your own data per segment: reachable customers, price, purchase frequency, sales and onboarding capacity
- The goal and the horizon the plan assumes
If you have none of this, I build the structure with every input as a [placeholder] and mark the output as a first draft. Claude supplies no market figure from memory.

## Approach
TAM, SAM and SOM with two sizing routes, a practitioner convention with no single originator. TAM is the total demand for the problem; SAM is the part reachable with this product, channel and geography; SOM is the part the plan can win in the horizon you set. Two routes that disagree tell you more than one that agrees with itself. With "Code execution and file creation" switched on, the model comes back as an editable spreadsheet; in a plain chat it is a table. The failure it prevents: one confident number copied from a report, which falls over when someone asks what it counts.

## Workflow
1. Ask up to three questions: which problem and segment are being sized, the horizon SOM uses, and the gap between the two routes that counts as too big (you set it).
2. Top-down: start from the published total you supply, with source and year, and narrow it by stated filters (geography, segment, problem fit) to TAM and then SAM. Each filter is its own line, with its own source or the label "assumption".
3. Bottom-up: reachable customers x price x purchase frequency, per segment. Each input comes from your data or is labelled "assumption".
4. Give every input a low, a base and a high value. The output is always a range. If a low and a high are equal, the input has not been questioned yet.
5. Triangulate: where the two routes differ by more than your gap, show both and name the inputs driving the difference. Never average them away.
6. Sanity check: the share of SAM the plan needs to reach its goal, and whether sales and onboarding capacity could reach that many customers in the horizon. Flag any share that needs a leap nobody can explain.

## Output Format
```markdown
# Market Size Estimate (TAM, SAM, SOM)
Problem and segment: [text] | SOM horizon: [period] | Gap threshold: [set by the user]
## Input table
| Input | Route | Low | Base | High | Source and year, or "assumption" |
|---|---|---|---|---|---|
| [published total, then one row per filter] | Top-down | [value] | [value] | [value] | [source, year / assumption] |
| [reachable customers, segment] | Bottom-up | [value] | [value] | [value] | [your data / assumption] |
| [price, purchase frequency] | Bottom-up | [value] | [value] | [value] | [your data / assumption] |
## Estimates
| Level | Top-down (low / base / high) | Bottom-up (low / base / high) | Gap | Inputs driving the gap |
|---|---|---|---|---|
| TAM | [range] | [range] | [gap] | [inputs] |
| SAM | [range] | [range] | [gap] | [inputs] |
| SOM ([horizon]) | [range] | [range] | [gap] | [inputs] |
## Sanity check
- Share of SAM the plan needs: [value, from the goal and the base SAM]; customers to reach in the horizon: [value]; within sales and onboarding capacity: [yes / no, why]
## Decision
The [product leader] decides by [date] which range is shown to leadership, with which caveat, and which assumptions get a source first.
```

## Done When
- Every input has a low, base and high value and a source or the label "assumption"
- Every level is shown as a range from both routes
- Any gap above the threshold is shown with the inputs behind it, not averaged
- The share of SAM the plan depends on is stated

## Quality Bar
- TAM counts demand for the problem, not every organisation that exists.
- Customers are counted in aggregate, never listed by name.
- A range is never collapsed into one figure for a slide.
- No market figure from memory; every input has a source or the word assumption, and a named person decides which figure is shown.

## Next
Run strat-lean-canvas (Lean Canvas) to put the business logic of the sized bet on one page.

## About the makers

This pack is made by 90n ([90n.ai](https://90n.ai)): AI-native ways of working and tools for Product, Marketing and HR teams, built by ex-McKinsey founders. We map where time and money leak, redesign the work around AI and stay until your people run it themselves, and we run our own company on Claude. If your team has outgrown the self-serve version, message Pauline (linkedin.com/in/paulinebertry).
