---
name: kpi-tree-finance
description: "Break a financial outcome into drivers the operator can influence, and stop at metrics someone owns. Use when the user mentions KPI tree, driver tree, what drives margin, finance metrics tree, or asks for a finance KPI tree. Finance skill by Yasir Jilani."
license: MIT
compatibility: Agent Skills standard. No network access, extra packages, or credentials required.
metadata:
  author: Yasir Jilani
  version: "1.0.0"
  domain: finance
---

<!-- GENERATED FILE - edits here are overwritten by scripts/generate.py.
     Edit the 'kpi-tree-finance' entry in source/, then run:
       python3 scripts/generate.py && python3 scripts/validate.py
     See CONTRIBUTING.md. -->

# Finance KPI Tree

Break a financial outcome into drivers the operator can influence, and stop at metrics someone owns.

## When to use this skill

Use this skill when the user:

- KPI tree
- driver tree
- what drives margin
- finance metrics tree

## When not to use this skill

- The user wants a different domain's specialist skill.
- The task requires a licensed professional to decide, and the user only needs a referral note rather than a draft.
- The request asks you to deceive, evade a control, or hide material facts.

## Professional boundary

This is not investment, tax, or financial advice. Do not invent rates of return, tax rates, or valuation multiples. A qualified finance professional must review any decision that moves money.

## Operating boundaries

- Use only information the user provides or files they explicitly ask you to read. Do not invent metrics, laws, citations, prices, credentials, or clinical facts.
- Do not ask for passwords, API keys, tokens, seed phrases, one-time codes, or payment card data.
- Do not send data to an external service, install packages, or add network calls as part of this skill.
- Separate facts, assumptions, and recommendations. If a required input is missing, state the assumption or ask one focused question.
- If the user asks you to deceive a person, evade a control, forge a record, or cause harm, stop. Offer a legitimate alternative.
- Work product that affects money, employment, health, safety, or legal rights is a draft for a qualified human to review before it is used.

## Inputs to collect

- The top outcome
- The operating levers the team controls
- Metrics they can actually extract
- Owners

## Workflow


### 1. Start at the outcome

Cash, contribution, or revenue quality. One top node.
### 2. Decompose mathematically

Each level should explain the level above. If a metric does not connect, cut it.
### 3. Stop at ownership

A driver with no owner is a decoration. Name the owner or stop decomposing.
### 4. Mark leading versus lagging

The tree should show what the team can see before the month closes.
### 5. Note data gaps

A missing driver is a measurement task, not a fake number.
### 6. Tie to the scorecard

Recommend which nodes appear weekly and which appear monthly.

## Output

Deliver a **finance KPI tree**.

- Purpose of this finance KPI tree, in two sentences.
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

Mara Chen, founder at Northline Studio in Calgary, needs a finance KPI tree by 30 September 2026. A COO wants to know which weekly numbers explain monthly gross margin.

### Example data

```text
From: Mara Chen, founder
Organization: Northline Studio, Calgary
Date: 14 September 2026
Needed by: 30 September 2026

A COO wants to know which weekly numbers explain monthly gross margin.

The top outcome: A COO wants to know which weekly numbers explain monthly gross margin. Stated once, in the ask. Not written down anywhere else
The operating levers the team controls: two people on shift, one off
Metrics they can actually extract: plan 150, actual 85
Owners: Mara Chen, founder
```

### Example outcome

**Finance kpi tree**
To: Mara Chen, founder, Northline Studio
Date: 14 September 2026 · Needed by: 30 September 2026

**Decision**
A tree from gross margin to a few owned drivers, with data gaps called out and a weekly subset named.

**What the file supports**

| Input | Value | Status |
| --- | --- | --- |
| The top outcome | A COO wants to know which weekly numbers explain monthly gross margin. Stated once, in the ask. Not written down anywhere else | Needs confirmation |
| The operating levers the team controls | two people on shift, one off | Carried into the draft |
| Metrics they can actually extract | plan 150, actual 85 | Carried into the draft |
| Owners | Mara Chen, founder | Needs confirmation |

**How this draft was built**

**1. Start at the outcome**  
Cash, contribution, or revenue quality. One top node.

**2. Decompose mathematically**  
Each level should explain the level above. If a metric does not connect, cut it.

**3. Stop at ownership**  
A driver with no owner is a decoration. Name the owner or stop decomposing.

**4. Mark leading versus lagging**  
The tree should show what the team can see before the month closes.

**5. Note data gaps**  
A missing driver is a measurement task, not a fake number.

**Deliberately not done**
- A mind map of every metric the company has ever tracked.
- Drivers that do not add up to the parent.
- No owners.

**Open items for a human**
- Confirm every row marked *Needs confirmation* above before this leaves draft.
- Anything absent from the file stayed absent. No figure, date, or name was supplied from outside it.

Next: Mara Chen by 30 September 2026. This is a draft, not a sign-off.

## Anti-patterns

- A mind map of every metric the company has ever tracked.
- Drivers that do not add up to the parent.
- No owners.

## Related skills

- `north-star-metric`
- `management-reporting-pack`
- `metric-definition`
