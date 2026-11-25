---
name: firm-hypothesis-test-plan
description: Writes your leading hypotheses about the client's problem so that each can fail, with the assumption it rests on, a rival explanation that fits the same facts, the observation that would tell them apart, the check with its owner and date, and the result that would change your view. Use for "run firm-hypothesis-test-plan", "test my hypothesis about this client", "I think I already know the answer", "what would prove me wrong", "rival explanations for this problem", "key assumptions check", "plan the first week of checks", part of the Claude for Consultants · Team in Claude Pack by 90n.
---

# Hypothesis Test Plan

## When To Use
By the second call you have a theory, and it is probably a good one. That is the risk. Working alone, nobody asks you what else would explain the same facts, and the theory hardens into the proposal. Run this before options exist, to write down what you believe in a form that could turn out wrong, and what would show it.

## When Not To Use
To split the question into parts first, build the Issue Tree. To stress a recommendation you have already chosen, use Recommendation Pre-Mortem; this skill tests your reading of the problem before any option is on the table.

## Inputs
- Your issue tree, or the problem statement and your current view in a few lines
- The facts so far, from your call record
- Who at the client could supply data or a second view, by role
If you have none of this, I start from your view in your own words and mark the plan as a first draft built on assumptions.

## Approach
Three techniques are used. A hypothesis must be a claim that can be disproven; a statement that cannot be wrong is only a fact (practitioner guide to hypothesis-led problem solving). The Key Assumptions Check and the Analysis of Competing Hypotheses come from "A Tradecraft Primer: Structured Analytic Techniques for Improving Intelligence Analysis" (US Government, 2009): list what must be true, and judge evidence by whether it separates rival explanations. The failure it prevents is collecting ten facts that fit your theory and every other theory equally well.

## Workflow
1. Ask, in one go: what do you currently believe is going on, and what is your strongest reason? Which facts is that built on? Who at the client would see it differently?
2. Write each leading hypothesis, three at most, so that it can fail: "[cause] explains [effect], and if so we would see [observation]". If no observation could contradict it, rewrite it until one could.
3. Run the key assumptions check on each: list what must be true for it to hold, and mark each assumption supported by a fact, plausible but unchecked, or simply taken on trust. Keep the two or three whose failure would sink the hypothesis.
4. Give each hypothesis a rival explanation that fits the same known facts. A real rival, the one a sceptical client lead would raise, not a straw one that is easy to knock down.
5. Find the observation that would tell the two apart: something expected under one and not the other. Evidence that fits both is set aside as not telling, however much of it there is.
6. Turn each telling observation into a check with a method, an owner by role, a date and a cost in time. Then write in advance which result would change your view. A check with no such result is decoration.

## Output Format
```markdown
# Hypothesis Test Plan
Problem: [root question] · Written: [date] · Your current view: [one line]
## Hypotheses and rivals
| # | Hypothesis (can fail) | Rests on (assumption, status) | Rival explanation | Observation that separates them |
|---|---|---|---|---|
| 1 | [cause explains effect] | [assumption: supported / unchecked / on trust] | [rival] | [expected under one, not the other] |
## Checks
| # | Check | Method | Owner (role) | By | Result that would change my view |
|---|---|---|---|---|---|
| 1 | [check] | [data / conversation / document / trial] | [role] | [date] | [result] |
## Evidence set aside as not telling
- [Fact that fits both the hypothesis and its rival]
## Decision
[You] decide by [date] which checks to run before proposing and which to write into the first phase of work; [client role] agrees any check that needs their data or people.
```

## Done When
- Each hypothesis names an observation that could contradict it
- Each has a rival that fits the known facts and an observation that separates the two
- Each check has an owner by role, a date and a result that would change your view

## Quality Bar
- Supporting and contrary evidence are held to the same standard
- The plan tests a claim; it never diagnoses you or the client as biased
- Questions for a client colleague are neutral, and I never draft their answer
- No probability or figure appears unless you supplied it
- Hypotheses stay hypotheses until a check comes back; I invent no finding, and the view you take to the client is yours.

## Next
Run firm-stakeholder-interview-plan (Stakeholder Interview Plan) to plan whom to hear, separately, before your view settles.

## About the makers

This pack is made by 90n ([90n.ai](https://90n.ai)): AI-native ways of working and tools for Product, Marketing and HR teams, built by ex-McKinsey founders. We map where time and money leak, redesign the work around AI and stay until your people run it themselves, and we run our own company on Claude. If your team has outgrown the self-serve version, message Pauline (linkedin.com/in/paulinebertry).
