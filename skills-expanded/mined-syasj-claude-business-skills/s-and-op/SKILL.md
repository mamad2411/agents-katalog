---
name: s-and-op
description: "Brief an S&OP cycle so demand, supply, and a decision meet in one forum. Use when the user mentions S&OP, SIOP, sales and operations planning, demand supply balance, or asks for a S&OP brief. Supply chain skill by Yasir Jilani."
license: MIT
compatibility: Agent Skills standard. No network access, extra packages, or credentials required.
metadata:
  author: Yasir Jilani
  version: "1.0.0"
  domain: supply-chain
---

<!-- GENERATED FILE - edits here are overwritten by scripts/generate.py.
     Edit the 's-and-op' entry in source/, then run:
       python3 scripts/generate.py && python3 scripts/validate.py
     See CONTRIBUTING.md. -->

# Sales and Operations Planning

Brief an S&OP cycle so demand, supply, and a decision meet in one forum.

## When to use this skill

Use this skill when the user:

- S&OP
- SIOP
- sales and operations planning
- demand supply balance

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

- The demand number
- The supply constraint
- The gap
- The decision needed

## Workflow


### 1. Step 1

Use one set of numbers. Two unofficial forecasts are a finding.
### 2. Step 2

Show the gap in units and in customer impact.
### 3. Options

change demand, add supply, or accept the miss. Recommend one.
### 4. Step 4

Name the decider.
### 5. Step 5

Record assumptions that expire next cycle.
### 6. Step 6

Do not let a side meeting overturn the decision without a note.

## Output

Deliver a **S&OP brief**.

- Purpose of this S&OP brief, in two sentences.
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

Diane Cho, supply lead at Harbor Goods in Airdrie, needs a S&OP brief by 30 September 2026. Sales brings a new forecast to the meeting that supply has not seen.

### Example data

```text
From: Diane Cho, supply lead
Organization: Harbor Goods, Airdrie
Date: 14 September 2026
Needed by: 30 September 2026

Sales brings a new forecast to the meeting that supply has not seen.

The demand number: 20 in the last period. No prior period attached, so no trend
The supply constraint: no extra headcount, and no result that is not in this file
The gap: SKU 1044 cabin filter is missing a source
The decision needed: Sales brings a new forecast to the meeting that supply has not seen
```

### Example outcome

**S&op brief**
To: Diane Cho, supply lead, Harbor Goods
Date: 14 September 2026 · Needed by: 30 September 2026

**Decision**
Stops the decision until both sides use the same number, then records the gap.

**What the file supports**

| Input | Value | Status |
| --- | --- | --- |
| The demand number | 20 in the last period. No prior period attached, so no trend | Needs confirmation |
| The supply constraint | no extra headcount, and no result that is not in this file | Carried into the draft |
| The gap | SKU 1044 cabin filter is missing a source | Carried into the draft |
| The decision needed | Sales brings a new forecast to the meeting that supply has not seen | Needs confirmation |

**How this draft was built**

**1. Use one set of numbers. Two unofficial forecasts are a finding**

**2. Show the gap in units and in customer impact**

**3. Options**  
change demand, add supply, or accept the miss. Recommend one.

**4. Name the decider**

**5. Record assumptions that expire next cycle**

**Deliberately not done**
- Two forecasts.
- A meeting with no decision.
- A side deal that ignores the gap.

**Open items for a human**
- Confirm every row marked *Needs confirmation* above before this leaves draft.
- Anything absent from the file stayed absent. No figure, date, or name was supplied from outside it.

Next: Diane Cho by 30 September 2026. This is a draft, not a sign-off.

## Anti-patterns

- Two forecasts
- A meeting with no decision
- A side deal that ignores the gap

## Related skills

- `demand-plan-review`
- `capacity-plan`
