---
name: asset-maintenance-priority
description: "Prioritize maintenance work by safety and customer impact, using their defect list. Use when the user mentions maintenance priority, work order triage, asset backlog, utility maintenance, or asks for a maintenance priority. Energy and utilities operations skill by Yasir Jilani."
license: MIT
compatibility: Agent Skills standard. No network access, extra packages, or credentials required.
metadata:
  author: Yasir Jilani
  version: "1.0.0"
  domain: energy
---

<!-- GENERATED FILE - edits here are overwritten by scripts/generate.py.
     Edit the 'asset-maintenance-priority' entry in source/, then run:
       python3 scripts/generate.py && python3 scripts/validate.py
     See CONTRIBUTING.md. -->

# Maintenance Priority

Prioritize maintenance work by safety and customer impact, using their defect list.

## When to use this skill

Use this skill when the user:

- maintenance priority
- work order triage
- asset backlog
- utility maintenance

## When not to use this skill

- The user wants a different domain's specialist skill.
- The task requires a licensed professional to decide, and the user only needs a referral note rather than a draft.
- The request asks you to deceive, evade a control, or hide material facts.

## Professional boundary

Operational energy advice is not a permit and not a safety case. Do not bypass lockout, isolation, or regulatory limits.

## Operating boundaries

- Use only information the user provides or files they explicitly ask you to read. Do not invent metrics, laws, citations, prices, credentials, or clinical facts.
- Do not ask for passwords, API keys, tokens, seed phrases, one-time codes, or payment card data.
- Do not send data to an external service, install packages, or add network calls as part of this skill.
- Separate facts, assumptions, and recommendations. If a required input is missing, state the assumption or ask one focused question.
- If the user asks you to deceive a person, evade a control, forge a record, or cause harm, stop. Offer a legitimate alternative.
- Work product that affects money, employment, health, safety, or legal rights is a draft for a qualified human to review before it is used.

## Inputs to collect

- The defect list
- Safety flags
- Customer impact
- Crew capacity

## Workflow


### 1. Step 1

Put safety defects they flagged first.
### 2. Step 2

Then customer-impacting defects.
### 3. Step 3

Capacity-cut the rest visibly.
### 4. Step 4

Do not defer a known safety defect to make a metric look better.
### 5. Step 5

Assign an owner and a date to the kept work.
### 6. Step 6

Note what information is missing before a crew is sent.

## Output

Deliver a **maintenance priority**.

- Purpose of this maintenance priority, in two sentences.
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

Devon Hale, operations superintendent at Prairie Line Energy in Grande Prairie, needs a maintenance priority by 30 September 2026. A cosmetic backlog is scheduled ahead of a known leak on a safety device.

### Example data

```text
From: Devon Hale, operations superintendent
Organization: Prairie Line Energy, Grande Prairie
Date: 14 September 2026
Needed by: 30 September 2026

A cosmetic backlog is scheduled ahead of a known leak on a safety device.

The defect list: Feeder 12; Site meter 4; September bill
Safety flags: September bill. Partly documented: the what is written down, the who is not
Customer impact: Redline Parts
Crew capacity: two people, no overtime figure
```

### Example outcome

**Maintenance priority**
To: Devon Hale, operations superintendent, Prairie Line Energy
Date: 14 September 2026 · Needed by: 30 September 2026

**Decision**
Puts the safety device first and parks cosmetics over capacity.

**What the file supports**

| Input | Value | Status |
| --- | --- | --- |
| The defect list | Feeder 12; Site meter 4; September bill | Needs confirmation |
| Safety flags | September bill. Partly documented: the what is written down, the who is not | Carried into the draft |
| Customer impact | Redline Parts | Carried into the draft |
| Crew capacity | two people, no overtime figure | Needs confirmation |

**How this draft was built**

**1. Put safety defects they flagged first**

**2. Then customer-impacting defects**

**3. Capacity-cut the rest visibly**

**4. Do not defer a known safety defect to make a metric look better**

**5. Assign an owner and a date to the kept work**

**Deliberately not done**
- Deferring a known safety defect for a metric.
- No capacity cut.
- A crew sent with no location.

**Open items for a human**
- Confirm every row marked *Needs confirmation* above before this leaves draft.
- Anything absent from the file stayed absent. No figure, date, or name was supplied from outside it.

Next: Devon Hale by 30 September 2026. This is a draft, not a sign-off.

## Anti-patterns

- Deferring a known safety defect for a metric
- No capacity cut
- A crew sent with no location

## Related skills

- `portfolio-prioritization`
- `capacity-plan`
