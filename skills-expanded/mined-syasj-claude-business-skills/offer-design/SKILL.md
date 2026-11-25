---
name: offer-design
description: "Design an offer with a clear value, a price logic the user supplied, and terms a customer can understand. Use when the user mentions design an offer, promotional offer, packaging offer, lead magnet review, or asks for a offer design. Marketing skill by Yasir Jilani."
license: MIT
compatibility: Agent Skills standard. No network access, extra packages, or credentials required.
metadata:
  author: Yasir Jilani
  version: "1.0.0"
  domain: marketing
---

<!-- GENERATED FILE - edits here are overwritten by scripts/generate.py.
     Edit the 'offer-design' entry in source/, then run:
       python3 scripts/generate.py && python3 scripts/validate.py
     See CONTRIBUTING.md. -->

# Offer Design

Design an offer with a clear value, a price logic the user supplied, and terms a customer can understand.

## When to use this skill

Use this skill when the user:

- design an offer
- promotional offer
- packaging offer
- lead magnet review

## When not to use this skill

- The user wants a different domain's specialist skill.
- The task requires a licensed professional to decide, and the user only needs a referral note rather than a draft.
- The request asks you to deceive, evade a control, or hide material facts.

## Professional boundary

Do not invent testimonials, reviews, metrics, or claims the user cannot support. Do not draft spam, cloaking, fake scarcity, or impersonation.

## Operating boundaries

- Use only information the user provides or files they explicitly ask you to read. Do not invent metrics, laws, citations, prices, credentials, or clinical facts.
- Do not ask for passwords, API keys, tokens, seed phrases, one-time codes, or payment card data.
- Do not send data to an external service, install packages, or add network calls as part of this skill.
- Separate facts, assumptions, and recommendations. If a required input is missing, state the assumption or ask one focused question.
- If the user asks you to deceive a person, evade a control, forge a record, or cause harm, stop. Offer a legitimate alternative.
- Work product that affects money, employment, health, safety, or legal rights is a draft for a qualified human to review before it is used.

## Inputs to collect

- The audience
- What they get
- The price or exchange
- Constraints from finance or delivery

## Workflow


### 1. Value

What the customer receives in concrete terms.
### 2. Exchange

What you ask in return: money, time, or a meeting. Say it plainly.
### 3. Eligibility

Who the offer is for and when it ends, if it ends. No fake end date.
### 4. Delivery

Confirm the team can fulfill it. Marketing cannot offer what delivery cannot do.
### 5. Terms

The conditions a reasonable customer must see before accepting.
### 6. Measurement

What acceptance means, and what would make you retire the offer.

## Output

Deliver a **offer design**.

- Purpose of this offer design, in two sentences.
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

Lena Ortiz, marketing lead at Fieldnote in Edmonton, needs an offer design by 30 September 2026. A campaign offers a free onboarding package that customer success says it cannot staff.

### Example data

```text
From: Lena Ortiz, marketing lead
Organization: Fieldnote, Edmonton
Date: 14 September 2026
Needed by: 30 September 2026

A campaign offers a free onboarding package that customer success says it cannot staff.

The audience: people who already buy from Fieldnote
What they get: A campaign offers a free onboarding package that customer success says it cannot staff
The price or exchange: CAD 79
Constraints from finance or delivery: no extra headcount, and no result that is not in this file
```

### Example outcome

**Offer design**
To: Lena Ortiz, marketing lead, Fieldnote
Date: 14 September 2026 · Needed by: 30 September 2026

**Decision**
Either cuts the promise or waits until staffing is real, with visible terms.

**What the file supports**

| Input | Value | Status |
| --- | --- | --- |
| The audience | people who already buy from Fieldnote | Needs confirmation |
| What they get | A campaign offers a free onboarding package that customer success says it cannot staff | Carried into the draft |
| The price or exchange | CAD 79 | Carried into the draft |
| Constraints from finance or delivery | no extra headcount, and no result that is not in this file | Needs confirmation |

**How this draft was built**

**1. Value**  
What the customer receives in concrete terms.

**2. Exchange**  
What you ask in return: money, time, or a meeting. Say it plainly.

**3. Eligibility**  
Who the offer is for and when it ends, if it ends. No fake end date.

**4. Delivery**  
Confirm the team can fulfill it. Marketing cannot offer what delivery cannot do.

**5. Terms**  
The conditions a reasonable customer must see before accepting.

**Deliberately not done**
- Hidden conditions.
- Fake end dates.
- An offer operations cannot fulfill.

**Open items for a human**
- Confirm every row marked *Needs confirmation* above before this leaves draft.
- Anything absent from the file stayed absent. No figure, date, or name was supplied from outside it.

Next: Lena Ortiz by 30 September 2026. This is a draft, not a sign-off.

## Anti-patterns

- Hidden conditions.
- Fake end dates.
- An offer operations cannot fulfill.

## Related skills

- `pricing-packaging`
- `campaign-brief`
