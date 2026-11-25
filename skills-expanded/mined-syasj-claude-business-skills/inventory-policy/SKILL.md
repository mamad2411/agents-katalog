---
name: inventory-policy
description: "Set an inventory policy from service target, lead time, and demand variability they can show. Use when the user mentions inventory policy, safety stock, min max, inventory target, or asks for a inventory policy note. Supply chain skill by Yasir Jilani."
license: MIT
compatibility: Agent Skills standard. No network access, extra packages, or credentials required.
metadata:
  author: Yasir Jilani
  version: "1.0.0"
  domain: supply-chain
---

<!-- GENERATED FILE - edits here are overwritten by scripts/generate.py.
     Edit the 'inventory-policy' entry in source/, then run:
       python3 scripts/generate.py && python3 scripts/validate.py
     See CONTRIBUTING.md. -->

# Inventory Policy

Set an inventory policy from service target, lead time, and demand variability they can show.

## When to use this skill

Use this skill when the user:

- inventory policy
- safety stock
- min max
- inventory target

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

- Service target
- Lead time
- Demand variability if known
- Cost of a miss they described

## Workflow


### 1. Step 1

Define the item and the service target in their words.
### 2. Step 2

Use their lead time. A generic lead time is labeled a guess.
### 3. Step 3

If variability is unknown, say the safety stock is incomplete rather than inventing a formula result.
### 4. Step 4

Separate cycle stock from safety stock.
### 5. Step 5

Name who may override the target.
### 6. Step 6

Review the policy when lead time changes.

## Output

Deliver a **inventory policy note**.

- Purpose of this inventory policy note, in two sentences.
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

Diane Cho, supply lead at Harbor Goods in Airdrie, needs an inventory policy note by 30 September 2026. A buyer wants six weeks of safety stock because it feels safe, with a two-week lead time.

### Example data

```text
From: Diane Cho, supply lead
Organization: Harbor Goods, Airdrie
Date: 14 September 2026
Needed by: 30 September 2026

A buyer wants six weeks of safety stock because it feels safe, with a two-week lead time.

Service target: 160
Lead time: 28 days
Demand variability if known: 40 in the last period. No prior period attached, so no trend
Cost of a miss they described: CAD 36 direct. Overhead not in this line
```

### Example outcome

**Inventory policy note**
To: Diane Cho, supply lead, Harbor Goods
Date: 14 September 2026 · Needed by: 30 September 2026

**Decision**
Asks for the service target and variability before accepting six weeks.

**What the file supports**

| Input | Value | Status |
| --- | --- | --- |
| Service target | 160 | Needs confirmation |
| Lead time | 28 days | Carried into the draft |
| Demand variability if known | 40 in the last period. No prior period attached, so no trend | Carried into the draft |
| Cost of a miss they described | CAD 36 direct. Overhead not in this line | Needs confirmation |

**How this draft was built**

**1. Define the item and the service target in their words**

**2. Use their lead time. A generic lead time is labeled a guess**

**3. If variability is unknown, say the safety stock is incomplete rather than inventing a formula result**

**4. Separate cycle stock from safety stock**

**5. Name who may override the target**

**Deliberately not done**
- An invented safety-stock percentage.
- A policy with no owner.
- Mixing cycle and safety stock.

**Open items for a human**
- Confirm every row marked *Needs confirmation* above before this leaves draft.
- Anything absent from the file stayed absent. No figure, date, or name was supplied from outside it.

Next: Diane Cho by 30 September 2026. This is a draft, not a sign-off.

## Anti-patterns

- An invented safety-stock percentage
- A policy with no owner
- Mixing cycle and safety stock

## Related skills

- `safety-stock`
- `working-capital`
