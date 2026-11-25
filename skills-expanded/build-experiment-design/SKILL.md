---
name: build-experiment-design
description: Plans a controlled experiment for the version engineers build and run on real traffic, producing a hypothesis, one primary metric with guardrails, a sample and duration check from your own numbers and a decision rule written before launch. Use for "run build-experiment-design", "plan the A/B test for the built version", "will the built feature move the number", "is our traffic big enough for a test", "how long should the experiment run", "write the decision rule before launch", "what are our guardrail metrics", part of the Claude for Product Builders Pack by 90n.
---

# Experiment Design Plan

## When To Use
This plan is for the version engineers build and run on real traffic. It is never for the prototype: something shown to five users cannot be A/B tested. Use it when the decision was "build" and the next argument is whether the built version will move the number. It answers: can a fair test settle that, and what will we do with each possible result?

## When Not To Use
If all you have is a prototype, run Five-User Usability Test Plan instead; five sessions find problems, they do not measure a change. If traffic cannot reach the sample this check asks for, do not run a weak test: say so and go back to sessions with real users.

## Inputs
- The change as engineering will build it, and the current experience it is compared with
- The metric that should move, with its current value and its spread, from your own data
- Weekly users who would reach the changed screen, from your own data
If you have none of this, I start from the change and the metric and mark the output as a first draft for later, with the sample check left open.

## Approach
Online controlled experiments as set out by Kohavi, Longbotham, Sommerfield and Henne in "Controlled experiments on the web: survey and practical guide", 2009 (ai.stanford.edu/~ronnyk/2009controlledExperimentsOnTheWebSurvey.pdf). The judgment is agreeing the one metric that decides, and the rule for each outcome, before anyone sees data. The failure it prevents: a test read twenty ways afterwards until some metric shows a winner.

## Workflow
1. Ask three questions: is there an engineer-built version, or a date for one, and who runs the test; which single metric would settle the argument; and how many users reach the change each week. If nothing is built yet, carry on and mark the plan as a draft for later.
2. Write the hypothesis: "If we [change], then [primary metric] will [direction] for [users], because [reason]." One primary metric only, the paper's overall evaluation criterion. Every other metric is a guardrail or a diagnostic.
3. Name the guardrails: metrics that must not get worse. You set the threshold that stops the test; I do not propose one.
4. Run the sample check with the paper's rule of thumb: users per variant n = 16 x variance / (smallest change worth detecting) squared, at 95% confidence and 80% power. Variance and the smallest change come from your numbers. If traffic cannot reach n in a reasonable window, the plan says so and names another method.
5. Set the duration in whole weeks, long enough for primacy and newness effects to fade. Plan an A/A test first to check the split and the logging, then a gradual ramp-up with guardrails watched at each step. List what an engineer or analyst must confirm before launch: the variance, the eligible traffic, the logging and the split.
6. Write the decision rule for each outcome before launch: a gain with guardrails held, no detectable change, a guardrail breached. Add the line that a test says what changed, not why.

## Output Format
```markdown
# Experiment Design Plan
For the engineer-built version on real traffic. Not for the prototype. Status: [ready / draft for later, nothing built yet]. Question: [what this settles] | Owner: [role] | Written on: [date, before launch]
## Hypothesis
If we [change], then [primary metric] will [direction] for [users], because [reason].
Variants: A (control): [current experience] | B: [the built change] | Built and run by: [engineering team, by role]
## Metrics
| Role | Metric (definition) | Current value (period) | Stop threshold |
|---|---|---|---|
| Primary | [numerator / denominator / period] | [from your data] | n/a |
| Guardrail | [metric] | [from your data] | [set by you] |
## Sample, duration and setup
Variance: [from your data] | Smallest change worth detecting: [set by you] | Users per variant: [n from the formula] | Weekly eligible users: [from your data] | Duration: [whole weeks] | Feasible: [yes / no, and the other method] | A/A test: [dates] | Ramp-up: [steps] | Guardrails watched by: [role] | Numbers confirmed by: [engineer or analyst, by role]
## Decision rule
| Result on the primary metric | Action |
|---|---|
| [gain, guardrails held] | [keep B] |
| [no detectable change] | [keep A or change it] |
| [guardrail breached] | [stop, keep A] |
## Decision
The [product lead, by role] approves this plan and rule by [date, before launch]; the [named role] makes the call on the result by [date].
```

## Done When
- The first lines say it runs on the engineer-built version and real traffic
- One primary metric is named; the rest are marked guardrail or diagnostic
- The sample check uses your numbers, or is marked not feasible with another method
- The decision rule covers a gain, no change and a guardrail breach

## Quality Bar
- No invented variance, traffic or effect size; missing numbers stay in [brackets]. A result short of the sample is inconclusive, not a trend.
- An engineer or analyst confirms the numbers and the setup; the builder does not run the test alone.
- Results are read in aggregate: no per-user outcomes, no scoring of users or team members, small segments suppressed at the minimum you set. Consent and privacy rules for testing on users: check with a qualified adviser.
- The experiment runs on the version engineers built, never on the prototype; a named person makes the call on the rule set before launch.

## Next
Run build-routine-skill (Build Routine Skill) to turn the steps you repeated on this idea into a routine for the next one.

## About the makers

This pack is made by 90n ([90n.ai](https://90n.ai)): AI-native ways of working and tools for Product, Marketing and HR teams, built by ex-McKinsey founders. We map where time and money leak, redesign the work around AI and stay until your people run it themselves, and we run our own company on Claude. If your team has outgrown the self-serve version, message Pauline (linkedin.com/in/paulinebertry).
