---
name: steering-committee-pack
description: "Prepare a steering pack that asks for decisions and shows exceptions, in a few pages. Use when the user mentions steering committee, steerco pack, project board pack, governance pack, or asks for a steering pack. Project delivery skill by Yasir Jilani."
license: MIT
compatibility: Agent Skills standard. No network access, extra packages, or credentials required.
metadata:
  author: Yasir Jilani
  version: "1.0.0"
  domain: delivery
---

<!-- GENERATED FILE - edits here are overwritten by scripts/generate.py.
     Edit the 'steering-committee-pack' entry in source/, then run:
       python3 scripts/generate.py && python3 scripts/validate.py
     See CONTRIBUTING.md. -->

# Steering Committee Pack

Prepare a steering pack that asks for decisions and shows exceptions, in a few pages.

## When to use this skill

Use this skill when the user:

- steering committee
- steerco pack
- project board pack
- governance pack

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

- Decisions required
- Exception status
- Options
- Pre-read length they will tolerate

## Workflow


### 1. Step 1

Open with the decisions and the recommendation.
### 2. Step 2

Show only exceptions against the charter baseline.
### 3. Step 3

For each decision, give options and a recommendation.
### 4. Step 4

Put detail in an appendix the pack points to.
### 5. Step 5

Note decisions the committee made last time and whether they landed.
### 6. Step 6

Do not bring a decision the sponsor already delegated unless the delegation failed.

## Output

Deliver a **steering pack**.

- Purpose of this steering pack, in two sentences.
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

Owen Blake, delivery lead at Harbor Goods in Airdrie, needs a steering pack by 30 September 2026. A 40-page pack buries a request for more budget on page 31.

### Example data

```text
From: Owen Blake, delivery lead
Organization: Harbor Goods, Airdrie
Date: 14 September 2026
Needed by: 30 September 2026

A 40-page pack buries a request for more budget on page 31.

Decisions required: A 40-page pack buries a request for more budget on page 31
Exception status: Milestone 3 handover is open. RAID item 12 was raised verbally and never logged
Options: keep Milestone 3 handover, or stop. No third option written
Pre-read length they will tolerate: 20 in the last period. No prior period attached, so no trend
```

### Example outcome

**Steering pack**
To: Owen Blake, delivery lead, Harbor Goods
Date: 14 September 2026 · Needed by: 30 September 2026

**Decision**
Leads with the budget decision, the options, and the recommendation.

**What the file supports**

| Input | Value | Status |
| --- | --- | --- |
| Decisions required | A 40-page pack buries a request for more budget on page 31 | Needs confirmation |
| Exception status | Milestone 3 handover is open. RAID item 12 was raised verbally and never logged | Carried into the draft |
| Options | keep Milestone 3 handover, or stop. No third option written | Carried into the draft |
| Pre-read length they will tolerate | 20 in the last period. No prior period attached, so no trend | Needs confirmation |

**How this draft was built**

**1. Open with the decisions and the recommendation**

**2. Show only exceptions against the charter baseline**

**3. For each decision, give options and a recommendation**

**4. Put detail in an appendix the pack points to**

**5. Note decisions the committee made last time and whether they landed**

**Deliberately not done**
- A steerco that is a status tour.
- No recommendation.
- Ignoring last meeting's actions.

**Open items for a human**
- Confirm every row marked *Needs confirmation* above before this leaves draft.
- Anything absent from the file stayed absent. No figure, date, or name was supplied from outside it.

Next: Owen Blake by 30 September 2026. This is a draft, not a sign-off.

## Anti-patterns

- A steerco that is a status tour
- No recommendation
- Ignoring last meeting's actions

## Related skills

- `board-memo-writer`
- `status-report`
