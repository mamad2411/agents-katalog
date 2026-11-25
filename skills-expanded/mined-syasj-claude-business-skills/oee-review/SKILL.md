---
name: oee-review
description: "Review overall equipment effectiveness only as far as their data supports, and pick one loss to attack. Use when the user mentions OEE, equipment effectiveness, downtime review, loss tree, or asks for a OEE review. Manufacturing and quality skill by Yasir Jilani."
license: MIT
compatibility: Agent Skills standard. No network access, extra packages, or credentials required.
metadata:
  author: Yasir Jilani
  version: "1.0.0"
  domain: manufacturing
---

<!-- GENERATED FILE - edits here are overwritten by scripts/generate.py.
     Edit the 'oee-review' entry in source/, then run:
       python3 scripts/generate.py && python3 scripts/validate.py
     See CONTRIBUTING.md. -->

# OEE Review

Review overall equipment effectiveness only as far as their data supports, and pick one loss to attack.

## When to use this skill

Use this skill when the user:

- OEE
- equipment effectiveness
- downtime review
- loss tree

## When not to use this skill

- The user wants a different domain's specialist skill.
- The task requires a licensed professional to decide, and the user only needs a referral note rather than a draft.
- The request asks you to deceive, evade a control, or hide material facts.

## Professional boundary

Quality and safety procedures are drafts for the site's quality system. Do not bypass a hold, calibration, or safety step.

## Operating boundaries

- Use only information the user provides or files they explicitly ask you to read. Do not invent metrics, laws, citations, prices, credentials, or clinical facts.
- Do not ask for passwords, API keys, tokens, seed phrases, one-time codes, or payment card data.
- Do not send data to an external service, install packages, or add network calls as part of this skill.
- Separate facts, assumptions, and recommendations. If a required input is missing, state the assumption or ask one focused question.
- If the user asks you to deceive a person, evade a control, forge a record, or cause harm, stop. Offer a legitimate alternative.
- Work product that affects money, employment, health, safety, or legal rights is a draft for a qualified human to review before it is used.

## Inputs to collect

- Availability, performance, and quality data they have
- The biggest loss they see
- The time window
- The owner

## Workflow


### 1. Step 1

Use only components they measured. Do not invent an OEE number.
### 2. Step 2

Define the time base they used.
### 3. Step 3

Pick the largest evidenced loss.
### 4. Step 4

Recommend one countermeasure with an owner.
### 5. Step 5

Do not turn OEE into a punishment metric in the write-up.
### 6. Step 6

Recheck after the countermeasure, not after a speech.

## Output

Deliver a **OEE review**.

- Purpose of this OEE review, in two sentences.
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

Gus Moretti, plant manager at Redline Parts in Nisku, needs an OEE review by 30 September 2026. A manager wants an OEE of 85 quoted to a customer, and downtime is not recorded.

### Example data

```text
From: Gus Moretti, plant manager
Organization: Redline Parts, Nisku
Date: 14 September 2026
Needed by: 30 September 2026

A manager wants an OEE of 85 quoted to a customer, and downtime is not recorded.

Availability, performance, and quality data they have: 60 in the last period. No prior period attached, so no trend
The biggest loss they see: Line 2, recorded 14 September 2026. No supporting file attached
The time window: five working days, due 30 September 2026
The owner: Gus Moretti, plant manager
```

### Example outcome

**Oee review**
To: Gus Moretti, plant manager, Redline Parts
Date: 14 September 2026 · Needed by: 30 September 2026

**Decision**
Refuses the number and starts a downtime record before any customer claim.

**What the file supports**

| Input | Value | Status |
| --- | --- | --- |
| Availability, performance, and quality data they have | 60 in the last period. No prior period attached, so no trend | Needs confirmation |
| The biggest loss they see | Line 2, recorded 14 September 2026. No supporting file attached | Carried into the draft |
| The time window | five working days, due 30 September 2026 | Carried into the draft |
| The owner | Gus Moretti, plant manager | Needs confirmation |

**How this draft was built**

**1. Use only components they measured. Do not invent an OEE number**

**2. Define the time base they used**

**3. Pick the largest evidenced loss**

**4. Recommend one countermeasure with an owner**

**5. Do not turn OEE into a punishment metric in the write-up**

**Deliberately not done**
- An invented OEE.
- Three losses attacked at once.
- A blame report.

**Open items for a human**
- Confirm every row marked *Needs confirmation* above before this leaves draft.
- Anything absent from the file stayed absent. No figure, date, or name was supplied from outside it.

Next: Gus Moretti by 30 September 2026. This is a draft, not a sign-off.

## Anti-patterns

- An invented OEE
- Three losses attacked at once
- A blame report

## Related skills

- `continuous-improvement`
- `marketing-claims-review`
