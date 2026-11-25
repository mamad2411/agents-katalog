---
name: procurement-award-note
description: "Write an award note that shows scores, price, and the authority to award. Use when the user mentions award note, source selection, procurement award, bid evaluation, or asks for a award note. Procurement skill by Yasir Jilani."
license: MIT
compatibility: Agent Skills standard. No network access, extra packages, or credentials required.
metadata:
  author: Yasir Jilani
  version: "1.0.0"
  domain: procurement
---

<!-- GENERATED FILE - edits here are overwritten by scripts/generate.py.
     Edit the 'procurement-award-note' entry in source/, then run:
       python3 scripts/generate.py && python3 scripts/validate.py
     See CONTRIBUTING.md. -->

# Award Note

Write an award note that shows scores, price, and the authority to award.

## When to use this skill

Use this skill when the user:

- award note
- source selection
- procurement award
- bid evaluation

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

- The criteria
- The scores and prices they have
- Conflicts
- The approver

## Workflow


### 1. Step 1

Show scores against the published criteria.
### 2. Step 2

Separate price from non-price scores.
### 3. Step 3

Record conflicts and recusals.
### 4. Step 4

Recommend an award only if the evaluation supports it.
### 5. Step 5

Do not change scores to fit a preferred vendor.
### 6. Step 6

Name the approver. This note does not itself sign the contract.

## Output

Deliver a **award note**.

- Purpose of this award note, in two sentences.
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

Diane Cho, buyer at Harbor Goods in Airdrie, needs an award note by 30 September 2026. A low-scoring friend of the buyer is moved to first after evaluation.

### Example data

```text
From: Diane Cho, buyer
Organization: Harbor Goods, Airdrie
Date: 14 September 2026
Needed by: 30 September 2026

A low-scoring friend of the buyer is moved to first after evaluation.

The criteria: their existing list, 6 lines. Two lines have no owner
The scores and prices they have: CAD 120
Conflicts: Quote set, 3 vendors. Stated in the ask, not documented anywhere else
The approver: Diane Cho. They have not signed
```

### Example outcome

**Award note**
To: Diane Cho, buyer, Harbor Goods
Date: 14 September 2026 · Needed by: 30 September 2026

**Decision**
Refuses the move and records the original scores.

**What the file supports**

| Input | Value | Status |
| --- | --- | --- |
| The criteria | their existing list, 6 lines. Two lines have no owner | Needs confirmation |
| The scores and prices they have | CAD 120 | Carried into the draft |
| Conflicts | Quote set, 3 vendors. Stated in the ask, not documented anywhere else | Carried into the draft |
| The approver | Diane Cho. They have not signed | Needs confirmation |

**How this draft was built**

**1. Show scores against the published criteria**

**2. Separate price from non-price scores**

**3. Record conflicts and recusals**

**4. Recommend an award only if the evaluation supports it**

**5. Do not change scores to fit a preferred vendor**

**Deliberately not done**
- Scores changed to fit a favorite.
- A missing conflict.
- An award with no approver.

**Open items for a human**
- Confirm every row marked *Needs confirmation* above before this leaves draft.
- Anything absent from the file stayed absent. No figure, date, or name was supplied from outside it.

Next: Diane Cho by 30 September 2026. This is a draft, not a sign-off.

## Anti-patterns

- Scores changed to fit a favorite
- A missing conflict
- An award with no approver

## Related skills

- `conflict-of-interest`
- `deal-desk-review`
