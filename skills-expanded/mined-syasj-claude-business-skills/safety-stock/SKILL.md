---
name: safety-stock
description: "Review safety stock for a few items so cash is not trapped in a habit. Use when the user mentions safety stock review, inventory too high, buffer stock, stock cover, or asks for a safety stock review. Supply chain skill by Yasir Jilani."
license: MIT
compatibility: Agent Skills standard. No network access, extra packages, or credentials required.
metadata:
  author: Yasir Jilani
  version: "1.0.0"
  domain: supply-chain
---

<!-- GENERATED FILE - edits here are overwritten by scripts/generate.py.
     Edit the 'safety-stock' entry in source/, then run:
       python3 scripts/generate.py && python3 scripts/validate.py
     See CONTRIBUTING.md. -->

# Safety Stock Review

Review safety stock for a few items so cash is not trapped in a habit.

## When to use this skill

Use this skill when the user:

- safety stock review
- inventory too high
- buffer stock
- stock cover

## When not to use this skill

- The user wants a different domain's specialist skill.
- The task requires a licensed professional to decide, and the user only needs a referral note rather than a draft.
- The request asks you to deceive, evade a control, or hide material facts.

## Professional boundary

Inventory and supplier recommendations depend on the user's lead times and service targets. Do not invent supplier performance.

## Operating boundaries

- Use only information the user provides or files they explicitly ask you to read. Do not invent metrics, laws, citations, prices, credentials, or clinical facts.
- Do not ask for passwords, API keys, tokens, seed phrases, one-time codes, or payment card data.
- Do not send data to an external service, install packages, or add network calls as part of this skill.
- Separate facts, assumptions, and recommendations. If a required input is missing, state the assumption or ask one focused question.
- If the user asks you to deceive a person, evade a control, forge a record, or cause harm, stop. Offer a legitimate alternative.
- Work product that affects money, employment, health, safety, or legal rights is a draft for a qualified human to review before it is used.

## Inputs to collect

- Current cover
- Lead time
- Stockout history they have
- Service target

## Workflow


### 1. Step 1

Rank items by cash tied up and by stockout pain, using their data.
### 2. Step 2

Identify cover that exceeds their own rule.
### 3. Step 3

Ask what uncertainty the extra cover buys. If nobody knows, it is a candidate to reduce.
### 4. Step 4

Do not cut stock that covers a known supply risk they named.
### 5. Step 5

Recommend a pilot reduction with a stockout check.
### 6. Step 6

Revisit after one lead time.

## Output

Deliver a **safety stock review**.

- Purpose of this safety stock review, in two sentences.
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

Diane Cho, supply lead at Harbor Goods in Airdrie, needs a safety stock review by 30 September 2026. Every item is set to 90 days because the spreadsheet default says so.

### Example data

```text
From: Diane Cho, supply lead
Organization: Harbor Goods, Airdrie
Date: 14 September 2026
Needed by: 30 September 2026

Every item is set to 90 days because the spreadsheet default says so.

Current cover: Redline Parts and one other, both unconfirmed as of 14 September 2026
Lead time: 28 days
Stockout history they have: Redline Parts, last reviewed 14 September 2026. No owner named since
Service target: 120
```

### Example outcome

**Safety stock review**
To: Diane Cho, supply lead, Harbor Goods
Date: 14 September 2026 · Needed by: 30 September 2026

**Decision**
Pilots a reduction on items with no risk story and leaves named risks alone.

**What the file supports**

| Input | Value | Status |
| --- | --- | --- |
| Current cover | Redline Parts and one other, both unconfirmed as of 14 September 2026 | Needs confirmation |
| Lead time | 28 days | Carried into the draft |
| Stockout history they have | Redline Parts, last reviewed 14 September 2026. No owner named since | Carried into the draft |
| Service target | 120 | Needs confirmation |

**How this draft was built**

**1. Rank items by cash tied up and by stockout pain, using their data**

**2. Identify cover that exceeds their own rule**

**3. Ask what uncertainty the extra cover buys. If nobody knows, it is a candidate to reduce**

**4. Do not cut stock that covers a known supply risk they named**

**5. Recommend a pilot reduction with a stockout check**

**Deliberately not done**
- A blanket cut.
- Cutting stock that covers a known risk.
- No stockout check.

**Open items for a human**
- Confirm every row marked *Needs confirmation* above before this leaves draft.
- Anything absent from the file stayed absent. No figure, date, or name was supplied from outside it.

Next: Diane Cho by 30 September 2026. This is a draft, not a sign-off.

## Anti-patterns

- A blanket cut
- Cutting stock that covers a known risk
- No stockout check

## Related skills

- `inventory-policy`
- `working-capital`
