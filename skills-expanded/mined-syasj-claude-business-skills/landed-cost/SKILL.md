---
name: landed-cost
description: "Build a landed-cost view from cost elements the user can support, so a buy decision sees the full cash cost. Use when the user mentions landed cost, total delivered cost, import cost stack, should we source this, or asks for a landed cost note. Supply chain skill by Yasir Jilani."
license: MIT
compatibility: Agent Skills standard. No network access, extra packages, or credentials required.
metadata:
  author: Yasir Jilani
  version: "1.0.0"
  domain: supply-chain
---

<!-- GENERATED FILE - edits here are overwritten by scripts/generate.py.
     Edit the 'landed-cost' entry in source/, then run:
       python3 scripts/generate.py && python3 scripts/validate.py
     See CONTRIBUTING.md. -->

# Landed Cost Review

Build a landed-cost view from cost elements the user can support, so a buy decision sees the full cash cost.

## When to use this skill

Use this skill when the user:

- landed cost
- total delivered cost
- import cost stack
- should we source this

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

- Invoice cost
- Freight, duty, and fees they know
- Volume
- The alternative source

## Workflow


### 1. Step 1

List only cost elements they can support. Mark unknowns.
### 2. Step 2

Show cost per unit at the volume they named.
### 3. Step 3

Compare with the alternative on the same elements.
### 4. Step 4

Note cash timing if duties or freight are paid earlier.
### 5. Step 5

Do not invent a duty rate.
### 6. Step 6

Recommend a buy, a question, or a hold until the unknown cost is filled.

## Output

Deliver a **landed cost note**.

- Purpose of this landed cost note, in two sentences.
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

Diane Cho, supply lead at Harbor Goods in Airdrie, needs a landed cost note by 30 September 2026. A cheaper invoice price is recommended, and nobody added international freight.

### Example data

```text
From: Diane Cho, supply lead
Organization: Harbor Goods, Airdrie
Date: 14 September 2026
Needed by: 30 September 2026

A cheaper invoice price is recommended, and nobody added international freight.

Invoice cost: CAD 44 direct. Overhead not in this line
Freight, duty, and fees they know: CAD 180, from their sheet, not a guess
Volume: 70 in the last period. No prior period attached, so no trend
The alternative source: note from Diane Cho, 14 September 2026. No outside report
```

### Example outcome

**Landed cost note**
To: Diane Cho, supply lead, Harbor Goods
Date: 14 September 2026 · Needed by: 30 September 2026

**Decision**
Holds the recommendation until freight is included or explicitly unknown.

**What the file supports**

| Input | Value | Status |
| --- | --- | --- |
| Invoice cost | CAD 44 direct. Overhead not in this line | Needs confirmation |
| Freight, duty, and fees they know | CAD 180, from their sheet, not a guess | Carried into the draft |
| Volume | 70 in the last period. No prior period attached, so no trend | Carried into the draft |
| The alternative source | note from Diane Cho, 14 September 2026. No outside report | Needs confirmation |

**How this draft was built**

**1. List only cost elements they can support. Mark unknowns**

**2. Show cost per unit at the volume they named**

**3. Compare with the alternative on the same elements**

**4. Note cash timing if duties or freight are paid earlier**

**5. Do not invent a duty rate**

**Deliberately not done**
- An invented duty rate.
- A unit cost that ignores freight.
- A comparison that omits the alternative's freight.

**Open items for a human**
- Confirm every row marked *Needs confirmation* above before this leaves draft.
- Anything absent from the file stayed absent. No figure, date, or name was supplied from outside it.

Next: Diane Cho by 30 September 2026. This is a draft, not a sign-off.

## Anti-patterns

- An invented duty rate
- A unit cost that ignores freight
- A comparison that omits the alternative's freight

## Related skills

- `pricing-margin-bridge`
- `supplier-scorecard`
