---
name: ops-scorecard
description: "Build an operations scorecard of a few measures that predict pain, with owners and a review cadence. Use when the user mentions ops scorecard, operations KPIs, weekly ops metrics, service scorecard, or asks for a operations scorecard. Operations skill by Yasir Jilani."
license: MIT
compatibility: Agent Skills standard. No network access, extra packages, or credentials required.
metadata:
  author: Yasir Jilani
  version: "1.0.0"
  domain: operations
---

<!-- GENERATED FILE - edits here are overwritten by scripts/generate.py.
     Edit the 'ops-scorecard' entry in source/, then run:
       python3 scripts/generate.py && python3 scripts/validate.py
     See CONTRIBUTING.md. -->

# Operations Scorecard

Build an operations scorecard of a few measures that predict pain, with owners and a review cadence.

## When to use this skill

Use this skill when the user:

- ops scorecard
- operations KPIs
- weekly ops metrics
- service scorecard

## When not to use this skill

- The user wants a different domain's specialist skill.
- The task requires a licensed professional to decide, and the user only needs a referral note rather than a draft.
- The request asks you to deceive, evade a control, or hide material facts.

## Professional boundary

Operating procedures should be usable by the team that will run them. Do not add surveillance of employees beyond what the user explicitly asks to document as policy.

## Operating boundaries

- Use only information the user provides or files they explicitly ask you to read. Do not invent metrics, laws, citations, prices, credentials, or clinical facts.
- Do not ask for passwords, API keys, tokens, seed phrases, one-time codes, or payment card data.
- Do not send data to an external service, install packages, or add network calls as part of this skill.
- Separate facts, assumptions, and recommendations. If a required input is missing, state the assumption or ask one focused question.
- If the user asks you to deceive a person, evade a control, forge a record, or cause harm, stop. Offer a legitimate alternative.
- Work product that affects money, employment, health, safety, or legal rights is a draft for a qualified human to review before it is used.

## Inputs to collect

- The pains to reduce
- Measures they can collect weekly
- Owners
- The review forum

## Workflow


### 1. Step 1

Choose measures that move before customers escalate, if they have such signals.
### 2. Step 2

Cap the scorecard. More than seven numbers will not be reviewed.
### 3. Step 3

Define each measure.
### 4. Step 4

Pair a volume measure with a quality or aging measure so speed cannot hide rework.
### 5. Step 5

Assign an owner and a threshold that triggers a conversation, not an automatic blame.
### 6. Step 6

Retire a measure that never changes a decision.

## Output

Deliver a **operations scorecard**.

- Purpose of this operations scorecard, in two sentences.
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

Diane Cho, operations manager at Harbor Goods in Airdrie, needs an operations scorecard by 30 September 2026. A team tracks tickets closed and ignores reopen rate.

### Example data

```text
From: Diane Cho, operations manager
Organization: Harbor Goods, Airdrie
Date: 14 September 2026
Needed by: 30 September 2026

A team tracks tickets closed and ignores reopen rate.

The pains to reduce: Tuesday shift, recorded 14 September 2026. No supporting file attached
Measures they can collect weekly: Tuesday shift. Stated in the ask, not documented anywhere else
Owners: Diane Cho, operations manager
The review forum: Tuesday shift, recorded 14 September 2026. No supporting file attached
```

### Example outcome

**Operations scorecard**
Harbor Goods · 14 September 2026 · Due 30 September 2026

**Decision**
Pairs closed tickets with reopens and names the review forum.

| Item | Figure in the file | Call | Why |
| --- | --- | --- | --- |
| Kite Freight | plan 160, actual 85 | Use | Both sides of the comparison are in the file |
| Lumen Ledger | score 71 | Report, do not benchmark | One score is a reading, not a baseline |
| Missing export | Not in the file | Stop | The cell stays blank until the export arrives |

**How these calls were made**

1. Choose measures that move before customers escalate, if they have such signals
2. Cap the scorecard. More than seven numbers will not be reviewed
3. Define each measure
4. Pair a volume measure with a quality or aging measure so speed cannot hide rework
5. Assign an owner and a threshold that triggers a conversation, not an automatic blame

**Deliberately not done**
- A 40-metric scorecard.
- A speed metric with no quality pair.
- Thresholds used only to punish.

**Open items**
- The missing export is the binding constraint. No figure was estimated to fill its place.
- Any row marked *Report, do not benchmark* needs a second period before it can carry a trend.

Next: Diane Cho attaches the missing export, or the cell stays blank. Due 30 September 2026.

## Anti-patterns

- A 40-metric scorecard
- A speed metric with no quality pair
- Thresholds used only to punish

## Related skills

- `kpi-tree-finance`
- `sla-design`
