---
name: qbr-customer
description: "Plan a customer quarterly review around their outcomes, not around a product tour. Use when the user mentions QBR, quarterly business review, customer business review, success review, or asks for a customer QBR. Customer experience skill by Yasir Jilani."
license: MIT
compatibility: Agent Skills standard. No network access, extra packages, or credentials required.
metadata:
  author: Yasir Jilani
  version: "1.0.0"
  domain: customer
---

<!-- GENERATED FILE - edits here are overwritten by scripts/generate.py.
     Edit the 'qbr-customer' entry in source/, then run:
       python3 scripts/generate.py && python3 scripts/validate.py
     See CONTRIBUTING.md. -->

# Customer QBR

Plan a customer quarterly review around their outcomes, not around a product tour.

## When to use this skill

Use this skill when the user:

- QBR
- quarterly business review
- customer business review
- success review

## When not to use this skill

- The user wants a different domain's specialist skill.
- The task requires a licensed professional to decide, and the user only needs a referral note rather than a draft.
- The request asks you to deceive, evade a control, or hide material facts.

## Professional boundary

Do not blame the customer. Do not invent policy exceptions. Do not ask a customer for passwords or full payment card numbers.

## Operating boundaries

- Use only information the user provides or files they explicitly ask you to read. Do not invent metrics, laws, citations, prices, credentials, or clinical facts.
- Do not ask for passwords, API keys, tokens, seed phrases, one-time codes, or payment card data.
- Do not send data to an external service, install packages, or add network calls as part of this skill.
- Separate facts, assumptions, and recommendations. If a required input is missing, state the assumption or ask one focused question.
- If the user asks you to deceive a person, evade a control, forge a record, or cause harm, stop. Offer a legitimate alternative.
- Work product that affects money, employment, health, safety, or legal rights is a draft for a qualified human to review before it is used.

## Inputs to collect

- Outcomes the customer wanted
- Usage or results they confirmed
- Open issues
- The ask

## Workflow


### 1. Step 1

Open with their goal, not your roadmap.
### 2. Step 2

Show only results they confirmed or that come from data they accept.
### 3. Step 3

Address open issues before asking for an expansion.
### 4. Step 4

Make one ask, tied to a next outcome.
### 5. Step 5

Leave with owners on both sides.
### 6. Step 6

Do not surprise them with a price change they have not been prepared for. Flag it as a separate conversation.

## Output

Deliver a **customer QBR**.

- Purpose of this customer QBR, in two sentences.
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

Rita Santos, support lead at Fieldnote in Edmonton, needs a customer QBR by 30 September 2026. A QBR deck leads with new features and never mentions the customer's failed onboarding.

### Example data

```text
From: Rita Santos, support lead
Organization: Fieldnote, Edmonton
Date: 14 September 2026
Needed by: 30 September 2026

A QBR deck leads with new features and never mentions the customer's failed onboarding.

Outcomes the customer wanted: A QBR deck leads with new features and never mentions the customer's failed onboarding. Stated once, in the ask. Not written down anywhere else
Usage or results they confirmed: 60 in the last period. No prior period attached, so no trend
Open issues: Ticket 4412 is open. Ticket 4418 was raised verbally and never logged
The ask: A QBR deck leads with new features and never mentions the customer's failed onboarding. Stated once, in the ask. Not written down anywhere else
```

### Example outcome

**Customer qbr**
To: Rita Santos, support lead, Fieldnote
Date: 14 September 2026 · Needed by: 30 September 2026

**Decision**
Leads with the onboarding gap, uses only confirmed results, and parks the feature tour.

**What the file supports**

| Input | Value | Status |
| --- | --- | --- |
| Outcomes the customer wanted | A QBR deck leads with new features and never mentions the customer's failed onboarding. Stated once, in the ask. Not written down anywhere else | Needs confirmation |
| Usage or results they confirmed | 60 in the last period. No prior period attached, so no trend | Carried into the draft |
| Open issues | Ticket 4412 is open. Ticket 4418 was raised verbally and never logged | Carried into the draft |
| The ask | A QBR deck leads with new features and never mentions the customer's failed onboarding. Stated once, in the ask. Not written down anywhere else | Needs confirmation |

**How this draft was built**

**1. Open with their goal, not your roadmap**

**2. Show only results they confirmed or that come from data they accept**

**3. Address open issues before asking for an expansion**

**4. Make one ask, tied to a next outcome**

**5. Leave with owners on both sides**

**Deliberately not done**
- A product tour labeled a QBR.
- Unconfirmed results.
- A surprise commercial ask.

**Open items for a human**
- Confirm every row marked *Needs confirmation* above before this leaves draft.
- Anything absent from the file stayed absent. No figure, date, or name was supplied from outside it.

Next: Rita Santos by 30 September 2026. This is a draft, not a sign-off.

## Anti-patterns

- A product tour labeled a QBR
- Unconfirmed results
- A surprise commercial ask

## Related skills

- `account-plan`
- `customer-health-score`
