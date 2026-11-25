---
name: sla-design
description: "Design a service level that matches a customer promise the team can measure and staff. Use when the user mentions SLA design, service level, define an SLA, support response target, or asks for a service level design. Operations skill by Yasir Jilani."
license: MIT
compatibility: Agent Skills standard. No network access, extra packages, or credentials required.
metadata:
  author: Yasir Jilani
  version: "1.0.0"
  domain: operations
---

<!-- GENERATED FILE - edits here are overwritten by scripts/generate.py.
     Edit the 'sla-design' entry in source/, then run:
       python3 scripts/generate.py && python3 scripts/validate.py
     See CONTRIBUTING.md. -->

# SLA Design

Design a service level that matches a customer promise the team can measure and staff.

## When to use this skill

Use this skill when the user:

- SLA design
- service level
- define an SLA
- support response target

## When not to use this skill

- The user wants a different domain's specialist skill.
- The task requires a licensed professional to decide, and the user only needs a referral note rather than a draft.
- The request asks you to deceive, evade a control, or hide material facts.

## Professional boundary

Operating procedures should be usable by the team that will run them. Do not add surveillance of employees beyond what the user explicitly asks to document as policy.

## Operating boundaries

- Use only information the user provides or files they explicitly ask you to read. Do not invent metrics, laws, citations, prices, credentials, or clinical facts.
- Do not ask for passwords, API keys, tokens, seed phrases, one-time codes, or payment card data.
- Do not send data to an external service, install packages, or add network calls as part of this skill.
- Separate facts, assumptions, and recommendations. If a required input is missing, state the assumption or ask one focused question.
- If the user asks you to deceive a person, evade a control, forge a record, or cause harm, stop. Offer a legitimate alternative.
- Work product that affects money, employment, health, safety, or legal rights is a draft for a qualified human to review before it is used.

## Inputs to collect

- The promise customers already hear
- Current performance if known
- Staffing
- Exceptions

## Workflow


### 1. Step 1

Start from the promise already made. If operations cannot meet it, the finding is the promise or the staffing, not a prettier SLA.
### 2. Define the clock

when it starts and stops, and which tickets count.
### 3. Step 3

Set a target from their history or mark it as a proposal.
### 4. Step 4

Add an exception path for cases the SLA should not pretend to cover.
### 5. Step 5

Name the measure and the owner.
### 6. Step 6

Do not hide a missed SLA by reclassifying work after the fact. Recommend against that.

## Output

Deliver a **service level design**.

- Purpose of this service level design, in two sentences.
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

Diane Cho, operations manager at Harbor Goods in Airdrie, needs a service level design by 30 September 2026. Sales promises a one-hour response and the queue currently averages a day.

### Example data

```text
From: Diane Cho, operations manager
Organization: Harbor Goods, Airdrie
Date: 14 September 2026
Needed by: 30 September 2026

Sales promises a one-hour response and the queue currently averages a day.

The promise customers already hear: none written down beyond the ask
Current performance if known: 70 in the last period. No prior period attached, so no trend
Staffing: two people on shift
Exceptions: Tuesday shift is open. SOP 118 receiving was raised verbally and never logged
```

### Example outcome

**Service level design**
To: Diane Cho, operations manager, Harbor Goods
Date: 14 September 2026 · Needed by: 30 September 2026

**Decision**
Exposes the gap and proposes either a truthful promise or a staffed path, with no silent reclassification.

**What the file supports**

| Input | Value | Status |
| --- | --- | --- |
| The promise customers already hear | none written down beyond the ask | Needs confirmation |
| Current performance if known | 70 in the last period. No prior period attached, so no trend | Carried into the draft |
| Staffing | two people on shift | Carried into the draft |
| Exceptions | Tuesday shift is open. SOP 118 receiving was raised verbally and never logged | Needs confirmation |

**How this draft was built**

**1. Start from the promise already made. If operations cannot meet it, the finding is the promise or the staffing, not a prettier SLA**

**2. Define the clock**  
when it starts and stops, and which tickets count.

**3. Set a target from their history or mark it as a proposal**

**4. Add an exception path for cases the SLA should not pretend to cover**

**5. Name the measure and the owner**

**Deliberately not done**
- An SLA nobody measures.
- Reclassifying misses.
- A target copied from a competitor.

**Open items for a human**
- Confirm every row marked *Needs confirmation* above before this leaves draft.
- Anything absent from the file stayed absent. No figure, date, or name was supplied from outside it.

Next: Diane Cho by 30 September 2026. This is a draft, not a sign-off.

## Anti-patterns

- An SLA nobody measures
- Reclassifying misses
- A target copied from a competitor

## Related skills

- `service-catalog`
- `ticket-quality-review`
