---
name: strat-north-star-metric
description: Builds a north star metric tree for the product with two or three candidates tested against customer value, the strategy and leading the business result, the exact definition of the chosen metric, three to five input metrics with definition, data source and owning team, and a counter-metric per input. Use for "run strat-north-star-metric", "pick our north star metric", "north star framework", "which number is the strategy meant to move", "input metrics", "metric tree", "we ship a lot and cannot show impact", "is revenue a north star", part of the Claude Guide for Product Strategy Pack by 90n.
---

# North Star Metric

## When To Use
The team ships a lot and cannot say which number the strategy is meant to move, so every dashboard review turns into a debate about which chart matters. Use it once an option is chosen and its bets are written. It answers: which one number shows that customers get the value the strategy promises, and which few inputs can teams move?

## When Not To Use
If you need to know whether each bet is working, run Strategy KPIs: that sheet holds one row set per bet with a review date, while this tree is one metric for the product and stays stable across strategy cycles. If you only need today's state with no number picked, run Product Health Read. With no chosen option, a north star freezes today's habits into a number; run Strategic Options first.

## Inputs
- The chosen option and its bets, and the moment a customer gets value from the product
- The metrics you track today, with where each one comes from
- The candidates the team or leadership has already floated
If you have none of this, I start from a description of the value moment and mark the output as a first draft. With a read-only analytics connector on, I read event names and definitions from your analytics instead of asking you to type them; it works the same in a plain chat with an export.

## Approach
The method is the North Star Framework from the Amplitude North Star Playbook (https://amplitude.com/books/north-star): one metric that reflects customer value, moved through a handful of named inputs teams can act on. The judgment is in the three tests, and most candidates fail the third. The failure it prevents: registered users or revenue picked as the star, which keep climbing for two quarters while customers quietly stop getting value, so the strategy looks healthy until the renewals arrive.

## Workflow
1. Ask at most three questions: what the value moment is for the customer, which data sources you trust today, and who approves the north star (by role).
2. List two or three candidates. Rate each pass, partial or fail, with a reason, on three tests: it expresses the value customers get, it represents the strategy (the chosen option and its bets, so a metric the rejected options would move just as well is a partial), and it leads business results instead of trailing them.
3. Reject revenue and vanity counts, such as registered users or actives with no value action, and say why in one line each. They stay in the table as rejected so the argument is not reopened.
4. Write the exact definition of the leading candidate: what counts, the time window, what is excluded. If two people could compute it and get different answers, it is not finished.
5. Break it into three to five inputs a team can act on. Breadth, depth, frequency and efficiency is a starting heuristic, not a rule; an input that is another team's outcome is dropped.
6. For each input, write the definition, the data source and the owning team. Where data is missing, write "not yet measurable" and the tracking change needed; never fill in a value.
7. Add one counter-metric per input so gaming it does not hurt customers, for example [activation speed] guarded by [support contacts per new account]. You set each threshold.

## Output Format
```markdown
# North Star Metric Tree
Product: [name] | Chosen option: [name] | Approver: [role] | Draft status: [first draft or reviewed]
## Candidates
| Candidate | Customer value | Represents the strategy | Leads business results | Verdict |
|---|---|---|---|---|
| [metric] | [pass, partial or fail, with reason] | [pass, partial or fail, with reason] | [pass, partial or fail, with reason] | [proposed or rejected] |
| [revenue or vanity count] | [reason] | [reason] | [reason] | [rejected, why] |
## North star
[Name]. Counts: [what counts]. Window: [time window]. Excluded: [what is left out]. Source: [where it is computed]
## Input metrics
| Input | Definition | Data source | Owning team | Counter-metric and threshold |
|---|---|---|---|---|
| [input] | [definition] | [source or "not yet measurable"] | [team] | [guard, threshold set by the owner] |
## Still to check
- [Data source to confirm, or customer evidence for the value moment still to gather]
## Decision
[Role who approves] approves the north star and its inputs by [date]; [owning team] confirms each data source by [date].
```

## Done When
- The proposed north star passes all three tests, or each partial is explained
- Revenue and vanity counts are named as rejected, with the reason
- There are three to five inputs, each with a definition, a source, an owning team and a counter-metric whose threshold you set

## Quality Bar
- Metrics are aggregate; owners are teams, never a person, and no per-user or per-employee metric appears in the tree.
- The value moment rests on what real customers did; where that evidence is missing, the line reads "assumed" and goes to the check list.
- Inputs are things a team can move, not another team's result, and the definition is exact enough that two analysts compute the same number.
- The tree is for the product and outlives one strategy cycle; a bet's measures belong on the KPI sheet and may point at an input, never redefine it.
- No invented baselines; a named person approves the north star, Claude never picks it alone.

## Next
Run strat-strategy-kpis (Strategy KPIs) to define the measures, baselines and change-course thresholds for each bet.

## About the makers

This pack is made by 90n ([90n.ai](https://90n.ai)): AI-native ways of working and tools for Product, Marketing and HR teams, built by ex-McKinsey founders. We map where time and money leak, redesign the work around AI and stay until your people run it themselves, and we run our own company on Claude. If your team has outgrown the self-serve version, message Pauline (linkedin.com/in/paulinebertry).
