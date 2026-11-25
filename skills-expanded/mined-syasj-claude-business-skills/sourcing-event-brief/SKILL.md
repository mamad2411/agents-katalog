---
name: sourcing-event-brief
description: "Brief a sourcing event with the need, the evaluation criteria, and the rules before vendors are contacted. Use when the user mentions sourcing event, RFP brief, tender brief, go to market procurement, or asks for a sourcing brief. Procurement skill by Yasir Jilani."
license: MIT
compatibility: Agent Skills standard. No network access, extra packages, or credentials required.
metadata:
  author: Yasir Jilani
  version: "1.0.0"
  domain: procurement
---

<!-- GENERATED FILE - edits here are overwritten by scripts/generate.py.
     Edit the 'sourcing-event-brief' entry in source/, then run:
       python3 scripts/generate.py && python3 scripts/validate.py
     See CONTRIBUTING.md. -->

# Sourcing Event Brief

Brief a sourcing event with the need, the evaluation criteria, and the rules before vendors are contacted.

## When to use this skill

Use this skill when the user:

- sourcing event
- RFP brief
- tender brief
- go to market procurement

## When not to use this skill

- The user wants a different domain's specialist skill.
- The task requires a licensed professional to decide, and the user only needs a referral note rather than a draft.
- The request asks you to deceive, evade a control, or hide material facts.

## Professional boundary

Buying decisions follow the organization's authority limits. Do not steer an award to a supplier for a personal benefit, and do not invent bids.

## Operating boundaries

- Use only information the user provides or files they explicitly ask you to read. Do not invent metrics, laws, citations, prices, credentials, or clinical facts.
- Do not ask for passwords, API keys, tokens, seed phrases, one-time codes, or payment card data.
- Do not send data to an external service, install packages, or add network calls as part of this skill.
- Separate facts, assumptions, and recommendations. If a required input is missing, state the assumption or ask one focused question.
- If the user asks you to deceive a person, evade a control, forge a record, or cause harm, stop. Offer a legitimate alternative.
- Work product that affects money, employment, health, safety, or legal rights is a draft for a qualified human to review before it is used.

## Inputs to collect

- The need
- Constraints
- Evaluation criteria
- Authority

## Workflow


### 1. Step 1

Define the need as an outcome.
### 2. Step 2

Write criteria before seeing vendor pitches.
### 3. Step 3

State must-haves versus scored items.
### 4. Step 4

Name who may talk to vendors.
### 5. Step 5

Do not tailor criteria to a favorite after bids arrive.
### 6. Step 6

Publish the timeline they can honor.

## Output

Deliver a **sourcing brief**.

- Purpose of this sourcing brief, in two sentences.
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

Diane Cho, buyer at Harbor Goods in Airdrie, needs a sourcing brief by 30 September 2026. A brief is edited so only the incumbent can score full marks, after drafts were shared.

### Example data

```text
From: Diane Cho, buyer
Organization: Harbor Goods, Airdrie
Date: 14 September 2026
Needed by: 30 September 2026

A brief is edited so only the incumbent can score full marks, after drafts were shared.

The need: Quote set, 3 vendors, recorded 14 September 2026. No supporting file attached
Constraints: no extra headcount, and no result that is not in this file
Evaluation criteria: their existing list, 6 lines. Two lines have no owner
Authority: Quote set, 3 vendors and one other, both unconfirmed as of 14 September 2026
```

### Example outcome

**Sourcing brief**
To: Diane Cho, buyer, Harbor Goods
Date: 14 September 2026 · Needed by: 30 September 2026

**Decision**
Freezes fair criteria and discloses must-haves before bids.

**What the file supports**

| Input | Value | Status |
| --- | --- | --- |
| The need | Quote set, 3 vendors, recorded 14 September 2026. No supporting file attached | Needs confirmation |
| Constraints | no extra headcount, and no result that is not in this file | Carried into the draft |
| Evaluation criteria | their existing list, 6 lines. Two lines have no owner | Carried into the draft |
| Authority | Quote set, 3 vendors and one other, both unconfirmed as of 14 September 2026 | Needs confirmation |

**How this draft was built**

**1. Define the need as an outcome**

**2. Write criteria before seeing vendor pitches**

**3. State must-haves versus scored items**

**4. Name who may talk to vendors**

**5. Do not tailor criteria to a favorite after bids arrive**

**Deliberately not done**
- Criteria written after seeing a favorite.
- Undisclosed must-haves.
- A timeline they will miss.

**Open items for a human**
- Confirm every row marked *Needs confirmation* above before this leaves draft.
- Anything absent from the file stayed absent. No figure, date, or name was supplied from outside it.

Next: Diane Cho by 30 September 2026. This is a draft, not a sign-off.

## Anti-patterns

- Criteria written after seeing a favorite
- Undisclosed must-haves
- A timeline they will miss

## Related skills

- `rfp-response`
- `procurement-award-note`
