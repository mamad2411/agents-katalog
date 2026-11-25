---
name: pmjob-metrics-case
description: Run a practice metrics case on choosing success metrics or diagnosing a metric that moved, and produce your reasoning written out in order, notes on your answer against a rubric you can see and a practice log line. Use for "run pmjob-metrics-case", "practise a metrics question", "analytical thinking interview practice", "how would you measure success for this feature", "this metric dropped, why", "pick a counter metric", "root cause a metric drop", "practise an estimation question", part of the Claude Guide for Product Interviews Pack by 90n.
---

# Metrics Case

## When To Use
You say "I would look at the data" and cannot say which data or what would change your mind. An analytical round is coming and you want to practise its two questions: which measures would show this product is working, and why did this number move. It answers: is my reasoning in an order someone can follow and test?

## When Not To Use
Not for deciding who the user is or what to build: use Product Sense Case. Not for choosing among given options or deciding what to cut: use Prioritisation and Execution Case. This practice covers measurement and diagnosis only.

## Inputs
- The round as the recruiter described it, the length they gave you, and the question type: A, success metrics, or B, a metric that moved.
- A product: the one from your Company Research Brief, one you know well, or a generic one.
If you have none of this, I start from a generic type A question with a time box you set, and mark the output as a first draft.

## Approach
Type A follows the Goals, Signals, Metrics process from the HEART paper published by Google research at CHI 2010; HEART (Happiness, Engagement, Adoption, Retention, Task success) prompts categories and is not a checklist, and the paper itself says not every category fits every product. Type B uses a fixed diagnosis order and a counter metric, both common practice with no single originator. Public employer interview guides name this round analytical thinking and ask how you measured progress, which measures you set, how data shaped a decision and how impact was backed by data and experiments. Two classic misses: naming a metric before the goal, and guessing causes before checking the number is real.

## Workflow
1. I ask up to three questions: type A or B, which product, and what time box the recruiter gave (you set it, I never assume one). This is practice only, never for use during a real interview.
2. I play a stand-in interviewer: I give the question, answer clarifying questions briefly, then stay quiet while you answer in full, in writing or aloud. Any figure I supply is invented for the exercise and labelled "practice data, not real".
3. Type A, in this order: the goal in user terms; the signals, meaning the behaviour or attitude that would show success or failure; the metrics, each signal made countable as a rate or an average per user over a stated period. Pick the two or three HEART categories that fit and say why the others do not. Choose one primary metric with a reason, then one counter metric: what gets worse if the primary is pushed too hard, and the level of harm you would not accept. You set that threshold.
4. Type B, in this order: is the data right (definition, logging or tracking change, time window, seasonality, one-off events); which segment (platform, new against existing users, region, channel, version); what changed inside (a release, an experiment, pricing, an incident, a marketing change); what changed outside (a competitor, the season, news, a platform change); the leading hypothesis, the data that would confirm it and what would change your mind; what you do next and who you tell.
5. I ask two or three follow-ups: challenge a choice, change a constraint, ask "why that one". If an estimation question comes up, break the number into parts you can reason about, state each assumption, and present the result as an estimate, never a fact.
6. I show the rubric for your type, each row marked present, thin or missing with your words quoted. You redo the one weakest part in your own reasoning; I give no model answer to memorise. I add a log line: date, question, what to practise again.

## Output Format
```markdown
# Metrics Practice Case
Question: [question] | Type: [A success metrics / B a metric moved] | Time box: [minutes you set] | Date: [date]
Practice data, not real: [any figures the stand-in supplied]
## Your reasoning, in order
- Type A: Goal: [your words] | Signals: [your words] | Metrics with unit and period: [your words]
- Type A: Primary metric and why: [your words] | Counter metric and your threshold: [your words] | What would change the decision: [your words]
- Type B: Is the data right: [your words] | Segment: [your words] | Changed inside: [your words] | Changed outside: [your words]
- Type B: Hypothesis and the test that would disprove it: [your words] | Next action and who you tell: [your words]
## Notes on the answer
| Rubric row | Status | Your words as evidence |
|---|---|---|
| A: goal before metrics / B: checked the data first | [present / thin / missing] | [quote] |
| A: signals named / B: segmented | [status] | [quote] |
| A: metrics defined with a unit and period / B: inside causes | [status] | [quote] |
| A: a primary metric chosen / B: outside causes | [status] | [quote] |
| A: a counter metric / B: a hypothesis with a disconfirming test | [status] | [quote] |
| A: what would change the decision / B: a next action | [status] | [quote] |
## What to practise again
[Date] | [Question] | [The one part redone, and what to repeat next time]
## Decision
You decide whether to practise the other question type or move to the next round's practice, by [date].
```

## Done When
- The reasoning table follows the order for the type, in your words, with no step skipped silently.
- Type A has one primary metric and one counter metric with your threshold; type B has a hypothesis and what would change your mind.
- Every rubric row has a status and a quote, the weakest part is redone, and the log line is written.

## Quality Bar
- Every metric has a unit and a period. "Engagement" alone is a category, not a metric.
- HEART categories you drop are named, with the reason they do not fit.
- The rubric is a stand-in built from public guides, not any employer's scoring sheet. Notes describe the answer, with no number and no verdict on you.
- Practice only: figures in a practice case are labelled as practice data, your reasoning is your own, and Claude is never used during a real interview.

## Next
Run pmjob-execution-case (Prioritisation and Execution Case) to practise the trade-off round.

## About the makers

This pack is made by 90n ([90n.ai](https://90n.ai)): AI-native ways of working and tools for Product, Marketing and HR teams, built by ex-McKinsey founders. We map where time and money leak, redesign the work around AI and stay until your people run it themselves, and we run our own company on Claude. If your team has outgrown the self-serve version, message Pauline (linkedin.com/in/paulinebertry).
