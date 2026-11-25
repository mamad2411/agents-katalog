---
name: savings-tracking
description: "Track procurement savings against a baseline the user can defend. Use when the user mentions procurement savings, cost avoidance, savings tracking, sourcing savings, or asks for a savings note. Procurement skill by Yasir Jilani."
license: MIT
compatibility: Agent Skills standard. No network access, extra packages, or credentials required.
metadata:
  author: Yasir Jilani
  version: "1.0.0"
  domain: procurement
---

<!-- GENERATED FILE - edits here are overwritten by scripts/generate.py.
     Edit the 'savings-tracking' entry in source/, then run:
       python3 scripts/generate.py && python3 scripts/validate.py
     See CONTRIBUTING.md. -->

# Procurement Savings Tracking

Track procurement savings against a baseline the user can defend.

## When to use this skill

Use this skill when the user:

- procurement savings
- cost avoidance
- savings tracking
- sourcing savings

## When not to use this skill

- The user wants a different domain's specialist skill.
- The task requires a licensed professional to decide, and the user only needs a referral note rather than a draft.
- The request asks you to deceive, evade a control, or hide material facts.

## Professional boundary

Buying decisions follow the organization's authority limits. Do not steer an award to a supplier for a personal benefit, and do not invent bids.

## Operating boundaries

- Use only information the user provides or files they explicitly ask you to read. Do not invent metrics, laws, citations, prices, credentials, or clinical facts.
- Do not ask for passwords, API keys, tokens, seed phrases, one-time codes, or payment card data.
- Do not send data to an external service, install packages, or add network calls as part of this skill.
- Separate facts, assumptions, and recommendations. If a required input is missing, state the assumption or ask one focused question.
- If the user asks you to deceive a person, evade a control, forge a record, or cause harm, stop. Offer a legitimate alternative.
- Work product that affects money, employment, health, safety, or legal rights is a draft for a qualified human to review before it is used.

## Inputs to collect

- The baseline
- The new price
- Volume
- One-time versus run-rate

## Workflow


### 1. Step 1

Define the baseline before claiming savings.
### 2. Step 2

Separate unit-price savings from volume changes.
### 3. Step 3

Mark cost avoidance as avoidance, not as cash, unless cash actually moved.
### 4. Step 4

Note one-time credits separately.
### 5. Step 5

Do not count a budget cut that reduced service as savings unless they want that labeled honestly.
### 6. Step 6

Show the arithmetic.

## Output

Deliver a **savings note**.

- Purpose of this savings note, in two sentences.
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

Diane Cho, buyer at Harbor Goods in Airdrie, needs a savings note by 30 September 2026. A report claims savings because the department stopped the service.

### Example data

```text
From: Diane Cho, buyer
Organization: Harbor Goods, Airdrie
Date: 14 September 2026
Needed by: 30 September 2026

A report claims savings because the department stopped the service.

The baseline: Quote set, 3 vendors, recorded 14 September 2026. No supporting file attached
The new price: CAD 49
Volume: 55 in the last period. No prior period attached, so no trend
One-time versus run-rate: five working days, due 30 September 2026
```

### Example outcome

**Savings note**
To: Diane Cho, buyer, Harbor Goods
Date: 14 September 2026 · Needed by: 30 September 2026

**Decision**
Refuses the savings claim or labels it a service cut.

**What the file supports**

| Input | Value | Status |
| --- | --- | --- |
| The baseline | Quote set, 3 vendors, recorded 14 September 2026. No supporting file attached | Needs confirmation |
| The new price | CAD 49 | Carried into the draft |
| Volume | 55 in the last period. No prior period attached, so no trend | Carried into the draft |
| One-time versus run-rate | five working days, due 30 September 2026 | Needs confirmation |

**How this draft was built**

**1. Define the baseline before claiming savings**

**2. Separate unit-price savings from volume changes**

**3. Mark cost avoidance as avoidance, not as cash, unless cash actually moved**

**4. Note one-time credits separately**

**5. Do not count a budget cut that reduced service as savings unless they want that labeled honestly**

**Deliberately not done**
- Savings with no baseline.
- Avoidance counted as cash.
- A service cut hidden as savings.

**Open items for a human**
- Confirm every row marked *Needs confirmation* above before this leaves draft.
- Anything absent from the file stayed absent. No figure, date, or name was supplied from outside it.

Next: Diane Cho by 30 September 2026. This is a draft, not a sign-off.

## Anti-patterns

- Savings with no baseline
- Avoidance counted as cash
- A service cut hidden as savings

## Related skills

- `cost-reduction-sprint`
- `budget-variance-review`
