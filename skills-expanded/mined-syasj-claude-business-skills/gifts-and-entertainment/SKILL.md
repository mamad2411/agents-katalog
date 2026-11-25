---
name: gifts-and-entertainment
description: "Apply a gifts and entertainment rule to a specific offer, and record the decision. Use when the user mentions gift policy, can we accept this, entertainment request, hospitality gift, or asks for a gift decision note. Risk and compliance skill by Yasir Jilani."
license: MIT
compatibility: Agent Skills standard. No network access, extra packages, or credentials required.
metadata:
  author: Yasir Jilani
  version: "1.0.0"
  domain: risk
---

<!-- GENERATED FILE - edits here are overwritten by scripts/generate.py.
     Edit the 'gifts-and-entertainment' entry in source/, then run:
       python3 scripts/generate.py && python3 scripts/validate.py
     See CONTRIBUTING.md. -->

# Gifts and Entertainment

Apply a gifts and entertainment rule to a specific offer, and record the decision.

## When to use this skill

Use this skill when the user:

- gift policy
- can we accept this
- entertainment request
- hospitality gift

## When not to use this skill

- The user wants a different domain's specialist skill.
- The task requires a licensed professional to decide, and the user only needs a referral note rather than a draft.
- The request asks you to deceive, evade a control, or hide material facts.

## Professional boundary

Risk work prioritizes uncertainty. It is not a certification. Do not claim SOC 2, ISO, HIPAA, or similar compliance unless the user has evidence of it.

## Operating boundaries

- Use only information the user provides or files they explicitly ask you to read. Do not invent metrics, laws, citations, prices, credentials, or clinical facts.
- Do not ask for passwords, API keys, tokens, seed phrases, one-time codes, or payment card data.
- Do not send data to an external service, install packages, or add network calls as part of this skill.
- Separate facts, assumptions, and recommendations. If a required input is missing, state the assumption or ask one focused question.
- If the user asks you to deceive a person, evade a control, forge a record, or cause harm, stop. Offer a legitimate alternative.
- Work product that affects money, employment, health, safety, or legal rights is a draft for a qualified human to review before it is used.

## Inputs to collect

- The offer and its value if known
- Who offered it
- The decision pending with that party
- Their policy

## Workflow


### 1. Step 1

State the offer, the giver, and whether a decision is pending with that party.
### 2. Step 2

Apply their policy thresholds. If they have no policy, recommend a decision from leadership rather than inventing a legal rule.
### 3. Step 3

A pending procurement or hiring decision raises the risk. Say so.
### 4. Step 4

Recommend accept, decline, or accept with disclosure, for their approver to confirm.
### 5. Step 5

Record it.
### 6. Step 6

Do not help disguise a gift as something else.

## Output

Deliver a **gift decision note**.

- Purpose of this gift decision note, in two sentences.
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

Priya Shah, controller at Northline Studio in Calgary, needs a gift decision note by 30 September 2026. A bidder offers tickets during an open RFP and the draft calls them a friendly dinner.

### Example data

```text
From: Priya Shah, controller
Organization: Northline Studio, Calgary
Date: 14 September 2026
Needed by: 30 September 2026

A bidder offers tickets during an open RFP and the draft calls them a friendly dinner.

The offer and its value if known: CAD 120, dates not set, cap not set
Who offered it: CAD 120, dates not set, cap not set
The decision pending with that party: A bidder offers tickets during an open RFP and the draft calls them a friendly dinner
Their policy: their one-page rule dated 2 Mar 2026. No exception log
```

### Example outcome

**Gift decision note**
To: Priya Shah, controller, Northline Studio
Date: 14 September 2026 · Needed by: 30 September 2026

**Decision**
Names the open RFP, refuses the disguise, and recommends decline or disclosure under their policy.

**What the file supports**

| Input | Value | Status |
| --- | --- | --- |
| The offer and its value if known | CAD 120, dates not set, cap not set | Needs confirmation |
| Who offered it | CAD 120, dates not set, cap not set | Carried into the draft |
| The decision pending with that party | A bidder offers tickets during an open RFP and the draft calls them a friendly dinner | Carried into the draft |
| Their policy | their one-page rule dated 2 Mar 2026. No exception log | Needs confirmation |

**How this draft was built**

**1. State the offer, the giver, and whether a decision is pending with that party**

**2. Apply their policy thresholds. If they have no policy, recommend a decision from leadership rather than inventing a legal rule**

**3. A pending procurement or hiring decision raises the risk. Say so**

**4. Recommend accept, decline, or accept with disclosure, for their approver to confirm**

**5. Record it**

**Deliberately not done**
- Disguising a gift.
- Inventing a legal threshold.
- Accepting a gift during a live bid without flagging it.

**Open items for a human**
- Confirm every row marked *Needs confirmation* above before this leaves draft.
- Anything absent from the file stayed absent. No figure, date, or name was supplied from outside it.

Next: Priya Shah by 30 September 2026. This is a draft, not a sign-off.

## Anti-patterns

- Disguising a gift
- Inventing a legal threshold
- Accepting a gift during a live bid without flagging it

## Related skills

- `conflict-of-interest`
- `procurement-award-note`
