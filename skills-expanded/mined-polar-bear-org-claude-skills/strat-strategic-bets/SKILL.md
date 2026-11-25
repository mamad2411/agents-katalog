---
name: strat-strategic-bets
description: Writes the Strategic Bets for the chosen option as three to five conditions that would have to be true, each with the evidence today, the test or early signal, a kill criterion and date set in advance, and an owner by role. Use for "run strat-strategic-bets", "what would have to be true", "write the bets behind our strategy", "what would prove this strategy wrong", "set kill criteria before the results", "early signals for the strategy", "which bet does the strategy lean on most", part of the Claude Guide for Product Strategy Pack by 90n.
---

# Strategic Bets

## When To Use
The strategy is chosen and nobody has written what would prove it wrong. Six months later the first weak result arrives, there is no agreed signal to read it against, and direction changes with whoever is most worried. Use this straight after the choice to answer: what are we betting on, and what result, by what date, would make us stop?

## When Not To Use
Bets belong to a chosen option. If no option is chosen yet and you are still explaining a problem, use the Hypothesis Board. If you need full metric definitions, baselines and guardrails for each bet, that is Strategy KPIs; here a bet gets one signal and one kill line.

## Inputs
- The chosen option in a sentence, and the horizon it covers
- The evidence behind the choice: interview themes, usage data, the matrix and its low-confidence scores
- Who owns the strategy by role, and which roles can watch a signal
If you have none of this, I start from the chosen option in one sentence and mark every bet "assumed" in a first draft.

## Approach
The question "what would have to be true?" comes from Lafley, Martin, Rivkin and Siggelkow, "Bringing science to the art of strategy" (Harvard Business Review, 2012, on hbr.org). It moves the room from arguing about what is true to naming the conditions the choice depends on. The bet table built around the question is this guide's own practice. The judgment is writing a condition tight enough to fail. The failure it prevents is the bet nobody can lose, "customers will value this", which is still "holding" on the day the strategy is quietly dropped.

## Workflow
1. Ask at most three questions: which option was chosen and over what horizon, what evidence stands behind it, and who owns the strategy by role.
2. For the chosen option only, ask what would have to be true about customers, the product, the economics and competitors for it to be a good choice. List the conditions without debating whether they hold yet.
3. Cut to three to five bets, each one condition that could turn out false inside the horizon. Run the looseness test on every line: if no result could show it false, rewrite it until one could.
4. Record the evidence today for each bet: "seen", with the interview or data source, or "assumed". What customers did counts as seen. What the team believes does not.
5. Order the bets by importance and evidence: how much the strategy depends on the bet, and how little has been seen. The bet the strategy leans on most with the least behind it goes first.
6. For each bet write the test or the early signal to watch, where it is read, a kill criterion and a date. The user sets every threshold, and all of it is written before any result arrives.
7. Give each bet an owner by role who watches the signal and raises it. The owner watches a signal; a broken bet is information about the strategy, not about the role.

## Output Format
```markdown
# Strategic Bets
**Chosen option:** [option] | **Horizon:** [period] | **Strategy owner:** [role] | **Written on:** [date, before results]
## Bets
| # | What would have to be true | About | Evidence today | Dependence | Test or early signal | Read where | Kill criterion | Kill date | Owner (role) |
|---|---|---|---|---|---|---|---|---|---|
| 1 | [condition that could turn out false] | [customers / product / economics / competitors] | [seen, with source / assumed] | [high / medium] | [test or signal] | [report, query or call set] | [result that ends the bet; threshold set by the owner] | [date] | [role] |
## Order of attention
1. Bet [#]: [why the strategy leans on it and what has not been seen yet]
## Conditions dropped by the looseness test
- [Condition]: [why no result could show it false, and the rewrite or the reason it was cut]
## Decision
[Role of the strategy owner] confirms the bets, the kill criteria and the dates by [date], before the first result is read.
```

## Done When
- Every bet belongs to the chosen option and could turn out false inside the horizon
- There are three to five bets, ordered by dependence and evidence
- Each bet is marked seen, with its source, or assumed
- Each bet has a signal, a place it is read, a kill criterion, a date and an owner by role
- The table is dated before any result

## Quality Bar
- A bet is one condition; a line joined by "and" is split
- Thresholds come from the user, never from a benchmark supplied from memory
- Bets are conditions, not failure stories and not metric definitions
- A broken bet is never read as a person's failure
- Kill criteria and dates are set by the owner before results arrive; evidence is what customers did or it is marked assumed.

## Next
Run strat-not-doing-list (Not-Doing List) to test every live request against the chosen option and these bets.

## About the makers

This pack is made by 90n ([90n.ai](https://90n.ai)): AI-native ways of working and tools for Product, Marketing and HR teams, built by ex-McKinsey founders. We map where time and money leak, redesign the work around AI and stay until your people run it themselves, and we run our own company on Claude. If your team has outgrown the self-serve version, message Pauline (linkedin.com/in/paulinebertry).
