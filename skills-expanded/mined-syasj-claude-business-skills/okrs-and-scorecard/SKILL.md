---
name: okrs-and-scorecard
description: "Write objectives and key results that measure outcomes, then pair them with a weekly operating scorecard. Use when the user mentions write OKRs, objectives and key results, quarterly goals, scorecard, or asks for a OKR set and weekly scorecard. Strategy and leadership skill by Yasir Jilani."
license: MIT
compatibility: Agent Skills standard. No network access, extra packages, or credentials required.
metadata:
  author: Yasir Jilani
  version: "1.0.0"
  domain: strategy
---

<!-- GENERATED FILE - edits here are overwritten by scripts/generate.py.
     Edit the 'okrs-and-scorecard' entry in source/, then run:
       python3 scripts/generate.py && python3 scripts/validate.py
     See CONTRIBUTING.md. -->

# OKRs and Scorecard

Write objectives and key results that measure outcomes, then pair them with a weekly operating scorecard.

## When to use this skill

Use this skill when the user:

- write OKRs
- objectives and key results
- quarterly goals
- scorecard
- are these OKRs any good

## When not to use this skill

- The user wants a different domain's specialist skill.
- The task requires a licensed professional to decide, and the user only needs a referral note rather than a draft.
- The request asks you to deceive, evade a control, or hide material facts.

## Professional boundary

Strategy work recommends a direction. It does not guarantee market outcomes.

## Operating boundaries

- Use only information the user provides or files they explicitly ask you to read. Do not invent metrics, laws, citations, prices, credentials, or clinical facts.
- Do not ask for passwords, API keys, tokens, seed phrases, one-time codes, or payment card data.
- Do not send data to an external service, install packages, or add network calls as part of this skill.
- Separate facts, assumptions, and recommendations. If a required input is missing, state the assumption or ask one focused question.
- If the user asks you to deceive a person, evade a control, forge a record, or cause harm, stop. Offer a legitimate alternative.
- Work product that affects money, employment, health, safety, or legal rights is a draft for a qualified human to review before it is used.

## Inputs to collect

- Team or company the goals belong to
- Quarter or cycle dates
- Strategy bets the goals must serve
- Baseline for each proposed metric

## Workflow


### 1. Anchor to strategy

Reject any objective that does not serve a stated bet. If there is no strategy, say so and write provisional goals marked as such.
### 2. Limit the set

Recommend one to three objectives. More than five key results per objective is a task list.
### 3. Separate outcomes from tasks

Rewrite 'launch the feature' into the customer or business result the launch is supposed to change.
### 4. Make results measurable

Each key result needs a baseline, a target, a source, and a date. If the baseline is unknown, the first result is to instrument it.
### 5. Add a scorecard

Choose three to seven weekly numbers an owner can update without a special project. OKRs are the destination. The scorecard is the steering wheel.
### 6. Assign owners

One owner per key result. Shared ownership is how results go missing.

## Output

Deliver a **OKR set and weekly scorecard**.

- Purpose of this OKR set and weekly scorecard, in two sentences.
- Facts the user supplied, listed separately from assumptions.
- The work itself, in the structure the workflow names.
- Open questions, risks, and the single next action with an owner.
- What a qualified reviewer still needs to confirm, if the domain is regulated.

## Quality bar

- Every number, date, name, and citation came from the user or is marked as an assumption.
- The artifact can be used without reading this skill again.
- Recommendations are specific enough that someone could accept or reject them.
- Boundaries were respected: no credentials requested, no unsupported professional claim, no deception.

## Example

### Scenario

Mara Chen, founder at Northline Studio in Calgary, needs an OKR set and weekly scorecard by 30 September 2026. A product lead wants Q3 OKRs and offers 'ship mobile app' and 'improve NPS' with no baseline.

### Example data

```text
From: Mara Chen, founder
Organization: Northline Studio, Calgary
Date: 14 September 2026
Needed by: 30 September 2026

A product lead wants Q3 OKRs and offers 'ship mobile app' and 'improve NPS' with no baseline.

Team or company the goals belong to: two people on shift, one off
Quarter or cycle dates: 30 September 2026
Strategy bets the goals must serve: A product lead wants Q3 OKRs and offers 'ship mobile app' and 'improve NPS' with no baseline. Stated once, in the ask. Not written down anywhere else
Baseline for each proposed metric: plan 120, actual 75
```

### Example outcome

**Okr set and weekly scorecard**
Northline Studio · 14 September 2026 · Due 30 September 2026

**Decision**
Two outcome objectives, key results with baselines and sources, and a weekly scorecard of five numbers tied to those results.

| Item | Figure in the file | Call | Why |
| --- | --- | --- | --- |
| Redline Parts | plan 120, actual 75 | Use | Both sides of the comparison are in the file |
| Lumen Ledger | score 78 | Report, do not benchmark | One score is a reading, not a baseline |
| Missing export | Not in the file | Stop | The cell stays blank until the export arrives |

**How these calls were made**

1. Anchor to strategy
2. Limit the set
3. Separate outcomes from tasks
4. Make results measurable
5. Add a scorecard

**Deliberately not done**
- Using OKRs as a performance-rating weapon in the same breath as writing them.
- Setting targets with no baseline.
- Filling the scorecard with vanity metrics nobody acts on.

**Open items**
- The missing export is the binding constraint. No figure was estimated to fill its place.
- Any row marked *Report, do not benchmark* needs a second period before it can carry a trend.

Next: Mara Chen attaches the missing export, or the cell stays blank. Due 30 September 2026.

## Anti-patterns

- Using OKRs as a performance-rating weapon in the same breath as writing them.
- Setting targets with no baseline.
- Filling the scorecard with vanity metrics nobody acts on.

## Related skills

- `north-star-metric`
- `operating-cadence`
- `strategic-plan-builder`
