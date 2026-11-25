---
name: risk-register
description: "Write a risk register with a few real risks, owners, and responses, not a copied list of generic fears. Use when the user mentions risk register, project risks, log a risk, risk review, or asks for a risk register. Project delivery skill by Yasir Jilani."
license: MIT
compatibility: Agent Skills standard. No network access, extra packages, or credentials required.
metadata:
  author: Yasir Jilani
  version: "1.0.0"
  domain: delivery
---

<!-- GENERATED FILE - edits here are overwritten by scripts/generate.py.
     Edit the 'risk-register' entry in source/, then run:
       python3 scripts/generate.py && python3 scripts/validate.py
     See CONTRIBUTING.md. -->

# Risk Register

Write a risk register with a few real risks, owners, and responses, not a copied list of generic fears.

## When to use this skill

Use this skill when the user:

- risk register
- project risks
- log a risk
- risk review

## When not to use this skill

- The user wants a different domain's specialist skill.
- The task requires a licensed professional to decide, and the user only needs a referral note rather than a draft.
- The request asks you to deceive, evade a control, or hide material facts.

## Professional boundary

Delivery plans are commitments only when owners and dates are real. Do not fabricate status to make a report look healthy.

## Operating boundaries

- Use only information the user provides or files they explicitly ask you to read. Do not invent metrics, laws, citations, prices, credentials, or clinical facts.
- Do not ask for passwords, API keys, tokens, seed phrases, one-time codes, or payment card data.
- Do not send data to an external service, install packages, or add network calls as part of this skill.
- Separate facts, assumptions, and recommendations. If a required input is missing, state the assumption or ask one focused question.
- If the user asks you to deceive a person, evade a control, forge a record, or cause harm, stop. Offer a legitimate alternative.
- Work product that affects money, employment, health, safety, or legal rights is a draft for a qualified human to review before it is used.

## Inputs to collect

- The risks the team can describe
- Likelihood and impact in their scale
- Current responses
- Owners

## Workflow


### 1. Step 1

Write risks as events that could happen, with a cause they believe.
### 2. Step 2

Score only on their scale. If they have no scale, use a simple high-medium-low and label it.
### 3. Step 3

Prefer a response that reduces the risk over a response that only watches it, when they can act.
### 4. Step 4

Give each open risk an owner and a review date.
### 5. Step 5

Close risks that have passed or been accepted.
### 6. Step 6

Do not add generic risks like 'resource risk' with no scenario.

## Output

Deliver a **risk register**.

- Purpose of this risk register, in two sentences.
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

Owen Blake, delivery lead at Harbor Goods in Airdrie, needs a risk register by 30 September 2026. A register contains 'resources' and 'communication' and nothing a sponsor can act on.

### Example data

```text
From: Owen Blake, delivery lead
Organization: Harbor Goods, Airdrie
Date: 14 September 2026
Needed by: 30 September 2026

A register contains 'resources' and 'communication' and nothing a sponsor can act on.

The risks the team can describe: Milestone 3 handover is open. No score in the file
Likelihood and impact in their scale: Change request 118, last reviewed 14 September 2026. No owner named since
Current responses: RAID item 12 and one other, both unconfirmed as of 14 September 2026
Owners: Owen Blake, delivery lead
```

### Example outcome

**Risk register**
To: Owen Blake, delivery lead, Harbor Goods
Date: 14 September 2026 · Needed by: 30 September 2026

**Decision**
A shorter register of specific events, each with an owner and a response.

**What the file supports**

| Input | Value | Status |
| --- | --- | --- |
| The risks the team can describe | Milestone 3 handover is open. No score in the file | Needs confirmation |
| Likelihood and impact in their scale | Change request 118, last reviewed 14 September 2026. No owner named since | Carried into the draft |
| Current responses | RAID item 12 and one other, both unconfirmed as of 14 September 2026 | Carried into the draft |
| Owners | Owen Blake, delivery lead | Needs confirmation |

**How this draft was built**

**1. Write risks as events that could happen, with a cause they believe**

**2. Score only on their scale. If they have no scale, use a simple high-medium-low and label it**

**3. Prefer a response that reduces the risk over a response that only watches it, when they can act**

**4. Give each open risk an owner and a review date**

**5. Close risks that have passed or been accepted**

**Deliberately not done**
- Generic risks with no scenario.
- A register with no responses.
- Scores with no scale.

**Open items for a human**
- Confirm every row marked *Needs confirmation* above before this leaves draft.
- Anything absent from the file stayed absent. No figure, date, or name was supplied from outside it.

Next: Owen Blake by 30 September 2026. This is a draft, not a sign-off.

## Anti-patterns

- Generic risks with no scenario
- A register with no responses
- Scores with no scale

## Related skills

- `raid-log`
- `risk-assessment`
