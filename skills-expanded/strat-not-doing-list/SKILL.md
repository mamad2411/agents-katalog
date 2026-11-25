---
name: strat-not-doing-list
description: Drafts a Not-Doing List that tests each live request, segment and pet project against the chosen strategy and writes the "we will not" lines with the reason, what saying no costs, who hears it, the short answer to give and the condition that would reopen it. Use for "run strat-not-doing-list", "everything is still a priority", "what will we not do", "draft the not-doing list", "test these requests against the strategy", "how do I say no to this request", "what would reopen this", part of the Claude Guide for Product Strategy Pack by 90n.
---

# Not-Doing List

## When To Use
The strategy was "agreed" and everything is still a priority. Every request that was live before the choice is live after it, because nobody wrote down what the choice turns away. Use this once the option and its bets are set, to answer: what will we not do, what does that cost, and what do we say to the people who asked?

## When Not To Use
Without a chosen option there is nothing to test against: run Strategic Options and the Decision Matrix first. For placing or cutting single roadmap items by horizon, use the Product Roadmap (Now, Next, Later), which keeps its own "not on the roadmap" section. This list comes before the roadmap and covers requests, segments and projects.

## Inputs
- The chosen option and its bets
- Everything live: requests, segments served, pet projects, half-started work, promises already made
- Capacity for the horizon as the user states it, and any cost of saying no the user can source
If you have none of this, I start from the chosen option in one sentence and the five requests you hear most, and mark the output as a first draft.

## Approach
Michael Porter argues in "What is strategy?" (Harvard Business Review, 1996, on hbr.org) that strategy requires trade-offs: choosing what not to do. The test table that applies the idea to a product is this guide's practice. The judgment sits in the neutral items, the work that does not conflict with the strategy and still takes people away from it. The failure it prevents is the "will not" list made only of things nobody wanted anyway, which costs nothing, upsets nobody and changes nothing.

## Workflow
1. Ask at most three questions: which option was chosen and what its bets are, what is live today, and which promises have already been made to customers or leaders.
2. Collect everything live and list it by need or theme, never by who asked. Merge duplicates so one need is one line.
3. Test each line against the chosen option and its bets: serves it, conflicts with it, or is neutral but takes capacity. Neutral items are where the list is won or lost, so each one gets a named capacity cost from the user or the word "unknown".
4. Write a "we will not" line only where someone wanted the thing. For each: the reason in the strategy's own words, what saying no costs (the user supplies any figure, with its source), and who hears it, as a role.
5. Draft the short answer to give: two sentences a product person can say out loud, naming the reason and the reopening condition, with no apology and no "not now" that sounds like a date.
6. Write the condition that would reopen each line as an observable change, never "if priorities change". Where a line conflicts with a promise already made, mark it as a question for the owner. This list does not keep the register of promises: dated commitments, with the role that made each, are listed in the Product Roadmap (Now, Next, Later).

## Output Format
```markdown
# Not-Doing List
**Chosen option:** [option] | **Horizon:** [period] | **Owner:** [role] | **Tested on:** [date]
## Test of everything live
| Item (by need or theme) | Type | Test result | Why |
|---|---|---|---|
| [item] | [request / segment / pet project / half-started work] | [serves / conflicts / neutral but takes capacity] | [link to the option or a bet] |
## We will not
| We will not | Reason, in the strategy's words | What saying no costs | Who hears it (role) | Short answer to give | Reopens if |
|---|---|---|---|---|---|
| [line someone wanted] | [reason] | [cost, with source, or "assumption"] | [role] | [two sentences] | [observable change] |
## Conflicts with a promise already made
- [line]: conflicts with [promise, made to role or segment]. Question for the owner: keep, renegotiate or end? The dated commitment itself is listed in the Product Roadmap (Now, Next, Later).
## Kept, and why
- [Item]: serves [option or bet]
## Decision
[Role of the strategy owner] approves each "we will not" line and rules on each flagged conflict by [date]; [role] gives the short answers by [date].
```

## Done When
- Every live item has a test result and a reason
- Every "we will not" line is something a real requester wanted
- Each line has a cost, a hearer by role, a short answer and a reopening condition
- Every line that conflicts with a promise already made is a question for the owner, with a pointer to the roadmap

## Quality Bar
- Requests are listed by need and theme, never ranked or labelled by who asked
- No invented cost: a figure has a source or the word assumption
- Reopening conditions are observable; "if priorities change" is rejected
- The reason quotes the chosen option or a bet, not a general principle
- Contract points in a promise already made: check with a qualified adviser
- Claude tests the list against the strategy; a named person owns every "we will not" line and the cost of saying it.

## Next
Run strat-scenario-planning (Scenario Planning Model) to see how the chosen option holds under base, upside and downside.

## About the makers

This pack is made by 90n ([90n.ai](https://90n.ai)): AI-native ways of working and tools for Product, Marketing and HR teams, built by ex-McKinsey founders. We map where time and money leak, redesign the work around AI and stay until your people run it themselves, and we run our own company on Claude. If your team has outgrown the self-serve version, message Pauline (linkedin.com/in/paulinebertry).
