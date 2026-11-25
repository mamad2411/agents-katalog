---
name: strat-one-page-strategy
description: Cuts a signed product strategy to one page for the teams who act on it, adding no new content, with the challenge and policy in one line, the actions, what we will not do, what it means for each team by role, a say-no test on three real requests and a repeat-from-memory test. Use for "run strat-one-page-strategy", "strategy on one page", "one page strategy for the teams", "nobody can repeat our strategy", "teams cannot say no with the strategy", "what does the strategy mean for my team", "test the strategy on real requests", "share the signed strategy with teams", part of the Claude Guide for Product Strategy Pack by 90n.
---

# One-Page Strategy

## When To Use
Leaders signed the strategy, and teams still cannot repeat it or use it to turn down a request. The document sits in a folder; on a Tuesday, with a request on the table, nobody opens it. Use this to cut the signed strategy to the one page a team works from. It answers: can someone who was not in the room say what we are doing, and say no with it?

## When Not To Use
If the strategy is not signed, stop: this page is never a shortcut to a strategy, so run Product Strategy Document first. If the strategy has just changed and teams need to hear what and why, Strategy Change Note announces that; this page states the standing strategy.

## Inputs
- The signed Product Strategy, in full, with who signed it and when
- Three real requests the teams received recently, as they were worded
- The teams who act on the strategy, by role
If you have none of this, I start from the signed strategy alone, leave the say-no test as [three requests to add] and mark the output as a first draft.

## Approach
Two public disciplines hold the page together. Bottom line up front, from US Army Regulation 25-50 (https://armypubs.army.mil/epubs/DR_pubs/DR_a/ARN42124-AR_25-50-007-WEB-13.pdf), puts the main point in the first sentence. The A3 report in the Lean Enterprise Institute lexicon (https://www.lean.org/lexicon-terms/a3-report/) keeps the whole story on a single sheet. The two tests are this guide's own practice. The failure this prevents is the summary that quietly improves on the strategy: a neater phrase or a new priority slips in, and now there are two strategies. In Claude Docs the page is one shared document. It works the same in a plain chat.

## Workflow
1. Ask at most three questions: who signed the strategy and on what date, which teams (by role) will work from this page, and the word limit for the repeat-from-memory test. If the strategy is not signed, I stop here and say so.
2. Write line one: the challenge and the policy in one sentence, main point first, taken from the document's own top line.
3. Copy the actions and the "we will not" lines from the document. Shorten them, but keep the meaning word for word where a choice is stated. Each line keeps a pointer to the line of the document it comes from.
4. Write what it means for each team, by role: what starts, what stops, what does not change. If the document does not say, the cell reads "not stated in the signed strategy" and goes to the owner. I do not fill it.
5. Run the say-no test: answer each of the three real requests using only the page, and name the line used. If the page cannot decide a request, flag it to the document's owner. The page is not patched to make the test pass.
6. Run the repeat-from-memory test: line one and the "we will not" lines within your word limit, no jargon. Then the trace check: every line on the page maps to a line of the signed document, and anything that does not is removed.

## Output Format
```markdown
# One-Page Strategy
**Cut from:** [signed strategy, date signed] | **Signed by:** [role] | **For:** [teams, by role]
## The strategy in one line
[Challenge], so we will [policy].
## What we are doing
- [action, shortened] (signed strategy: [section, line])
## What we will not do
- We will not [request, segment or bet], because [reason] (signed strategy: [section, line])
## What it means for each team
| Team (role) | Starts | Stops | Does not change |
|---|---|---|---|
| [role] | [work] | [work] | [work] |
## Say-no test
| Real request | Answer from the page | Line used | Could the page decide? |
|---|---|---|---|
| [request as worded] | [yes / no / not now, in one sentence] | [line] | [yes / no: flagged to the owner] |
## Repeat-from-memory test
[Line one and the "we will not" lines in [word limit] words, no jargon.]
## Decision
[Role of the owner of the signed strategy] approves the page for the teams and rules on each flagged request by [date].
```

## Done When
- The whole strategy fits on one page and line one carries the challenge and the policy
- Every line maps to a line of the signed document
- Three real requests are answered from the page, or flagged to the owner
- The memory version fits the word limit you set

## Quality Bar
- No new priority, phrase or number that the signed document does not hold
- Requests in the say-no test are real ones, pasted by you, never made up
- Teams appear by role; the tests check the page, never the people reading it
- The page adds nothing the signed strategy does not say; when a real request cannot be answered from it, the owner decides, not Claude.

## Next
Run strat-product-strategy-deck (Product Strategy Deck) to present the same strategy in a room and ask for the endorsement.

## About the makers

This pack is made by 90n ([90n.ai](https://90n.ai)): AI-native ways of working and tools for Product, Marketing and HR teams, built by ex-McKinsey founders. We map where time and money leak, redesign the work around AI and stay until your people run it themselves, and we run our own company on Claude. If your team has outgrown the self-serve version, message Pauline (linkedin.com/in/paulinebertry).
