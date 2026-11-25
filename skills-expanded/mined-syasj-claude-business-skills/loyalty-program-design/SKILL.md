---
name: loyalty-program-design
description: "Draft a loyalty program structure that rewards the behavior the brand actually wants to drive. Use when the user mentions loyalty program, rewards program, points program, customer loyalty retail, or asks for a loyalty program brief. Retail and commerce skill by Yasir Jilani."
license: MIT
compatibility: Agent Skills standard. No network access, extra packages, or credentials required.
metadata:
  author: Yasir Jilani
  version: "1.0.0"
  domain: retail
---

<!-- GENERATED FILE - edits here are overwritten by scripts/generate.py.
     Edit the 'loyalty-program-design' entry in source/, then run:
       python3 scripts/generate.py && python3 scripts/validate.py
     See CONTRIBUTING.md. -->

# Loyalty Program Design

Draft a loyalty program structure that rewards the behavior the brand actually wants to drive.

## When to use this skill

Use this skill when the user:

- loyalty program
- rewards program
- points program
- customer loyalty retail

## When not to use this skill

- The user wants a different domain's specialist skill.
- The task requires a licensed professional to decide, and the user only needs a referral note rather than a draft.
- The request asks you to deceive, evade a control, or hide material facts.

## Professional boundary

Do not invent inventory, prices, or reviews. Do not write deceptive promotions.

## Operating boundaries

- Use only information the user provides or files they explicitly ask you to read. Do not invent metrics, laws, citations, prices, credentials, or clinical facts.
- Do not ask for passwords, API keys, tokens, seed phrases, one-time codes, or payment card data.
- Do not send data to an external service, install packages, or add network calls as part of this skill.
- Separate facts, assumptions, and recommendations. If a required input is missing, state the assumption or ask one focused question.
- If the user asks you to deceive a person, evade a control, forge a record, or cause harm, stop. Offer a legitimate alternative.
- Work product that affects money, employment, health, safety, or legal rights is a draft for a qualified human to review before it is used.

## Inputs to collect

- What behavior they want to reward
- Their margin
- Tech they have
- Competitors they named

## Workflow


### 1. Step 1

Define the earn rule from the behavior they want, not from the points chart that sounds nice.
### 2. Step 2

State the redemption value in real dollars so they can check the margin math.
### 3. Step 3

A high earn rate with a blocked redemption is a fraud risk. Do not design that.
### 4. Step 4

Cap liability exposure if they name a max outstanding balance.
### 5. Step 5

Name what happens to points on a return.
### 6. Step 6

This is a draft structure. They need legal review before launch.

## Output

Deliver a **loyalty program brief**.

- Purpose of this loyalty program brief, in two sentences.
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

Diane Cho, store lead at Harbor Goods in Airdrie, needs a loyalty program brief by 30 September 2026. A program offers 10% back in points but the redemption minimum is higher than the average order, so few members ever cash out.

### Example data

```text
From: Diane Cho, store lead
Organization: Harbor Goods, Airdrie
Date: 14 September 2026
Needed by: 30 September 2026

A program offers 10% back in points but the redemption minimum is higher than the average order, so few members ever cash out.

What behavior they want to reward: Returns desk log, last reviewed 14 September 2026. No owner named since
Their margin: End-cap display 3, last reviewed 14 September 2026. No owner named since
Tech they have: End-cap display 3. Partly documented: the what is written down, the who is not
Competitors they named: two deals cited from memory. Neither has a written loss reason
```

### Example outcome

**Loyalty program brief**
To: Diane Cho, store lead, Harbor Goods
Date: 14 September 2026 · Needed by: 30 September 2026

**Decision**
Sets a redemption minimum below the average order and discloses the liability cap.

**What the file supports**

| Input | Value | Status |
| --- | --- | --- |
| What behavior they want to reward | Returns desk log, last reviewed 14 September 2026. No owner named since | Needs confirmation |
| Their margin | End-cap display 3, last reviewed 14 September 2026. No owner named since | Carried into the draft |
| Tech they have | End-cap display 3. Partly documented: the what is written down, the who is not | Carried into the draft |
| Competitors they named | two deals cited from memory. Neither has a written loss reason | Needs confirmation |

**How this draft was built**

**1. Define the earn rule from the behavior they want, not from the points chart that sounds nice**

**2. State the redemption value in real dollars so they can check the margin math**

**3. A high earn rate with a blocked redemption is a fraud risk. Do not design that**

**4. Cap liability exposure if they name a max outstanding balance**

**5. Name what happens to points on a return**

**Deliberately not done**
- An earn rate that creates liability they cannot pay.
- Blocked redemption that misleads members.
- No return policy for points.

**Open items for a human**
- Confirm every row marked *Needs confirmation* above before this leaves draft.
- Anything absent from the file stayed absent. No figure, date, or name was supplied from outside it.

Next: Diane Cho by 30 September 2026. This is a draft, not a sign-off.

## Anti-patterns

- An earn rate that creates liability they cannot pay
- Blocked redemption that misleads members
- No return policy for points

## Related skills

- `promotion-review`
- `customer-health-score`
