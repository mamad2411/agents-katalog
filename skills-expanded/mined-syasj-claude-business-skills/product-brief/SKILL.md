---
name: product-brief
description: "Write a product brief that frames the problem, the user, and the bet before anyone argues about features. Use when the user mentions product brief, opportunity brief, one-pager product, should we build, or asks for a product brief. Product skill by Yasir Jilani."
license: MIT
compatibility: Agent Skills standard. No network access, extra packages, or credentials required.
metadata:
  author: Yasir Jilani
  version: "1.0.0"
  domain: product
---

<!-- GENERATED FILE - edits here are overwritten by scripts/generate.py.
     Edit the 'product-brief' entry in source/, then run:
       python3 scripts/generate.py && python3 scripts/validate.py
     See CONTRIBUTING.md. -->

# Product Brief

Write a product brief that frames the problem, the user, and the bet before anyone argues about features.

## When to use this skill

Use this skill when the user:

- product brief
- opportunity brief
- one-pager product
- should we build

## When not to use this skill

- The user wants a different domain's specialist skill.
- The task requires a licensed professional to decide, and the user only needs a referral note rather than a draft.
- The request asks you to deceive, evade a control, or hide material facts.

## Professional boundary

Product recommendations are hypotheses until evidence says otherwise. Label confidence. Do not ship dark patterns that hide cost or consent.

## Operating boundaries

- Use only information the user provides or files they explicitly ask you to read. Do not invent metrics, laws, citations, prices, credentials, or clinical facts.
- Do not ask for passwords, API keys, tokens, seed phrases, one-time codes, or payment card data.
- Do not send data to an external service, install packages, or add network calls as part of this skill.
- Separate facts, assumptions, and recommendations. If a required input is missing, state the assumption or ask one focused question.
- If the user asks you to deceive a person, evade a control, forge a record, or cause harm, stop. Offer a legitimate alternative.
- Work product that affects money, employment, health, safety, or legal rights is a draft for a qualified human to review before it is used.

## Inputs to collect

- The user and the situation
- Evidence of the problem
- The business constraint
- What is already known to be out of scope

## Workflow


### 1. User and situation

Who hits the problem, and when. A persona name with no situation is not enough.
### 2. Problem evidence

Quotes, tickets, or data the user supplied. Mark guesses as guesses.
### 3. Bet

The change you believe will help, stated as a hypothesis.
### 4. Non-goals

At least three things this brief will not solve.
### 5. Risks

The assumption that would kill the bet if false.
### 6. Decision

Discover more, build a small slice, or stop. One recommendation.

## Output

Deliver a **product brief**.

- Purpose of this product brief, in two sentences.
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

Jonah Park, product manager at Fieldnote in Edmonton, needs a product brief by 30 September 2026. A stakeholder hands over a feature list and asks for a brief by tomorrow.

### Example data

```text
From: Jonah Park, product manager
Organization: Fieldnote, Edmonton
Date: 14 September 2026
Needed by: 30 September 2026

A stakeholder hands over a feature list and asks for a brief by tomorrow.

The user and the situation: Activation checklist, recorded 14 September 2026. No supporting file attached
Evidence of the problem: one PDF, 2 pages, dated 14 September 2026
The business constraint: no extra headcount, and no result that is not in this file
What is already known to be out of scope: anything not named in the ask
```

### Example outcome

**Product brief**
To: Jonah Park, product manager, Fieldnote
Date: 14 September 2026 · Needed by: 30 September 2026

**Decision**
Restates the missing problem evidence and refuses to pretend the feature list is a validated bet.

**What the file supports**

| Input | Value | Status |
| --- | --- | --- |
| The user and the situation | Activation checklist, recorded 14 September 2026. No supporting file attached | Needs confirmation |
| Evidence of the problem | one PDF, 2 pages, dated 14 September 2026 | Carried into the draft |
| The business constraint | no extra headcount, and no result that is not in this file | Carried into the draft |
| What is already known to be out of scope | anything not named in the ask | Needs confirmation |

**How this draft was built**

**1. User and situation**  
Who hits the problem, and when. A persona name with no situation is not enough.

**2. Problem evidence**  
Quotes, tickets, or data the user supplied. Mark guesses as guesses.

**3. Bet**  
The change you believe will help, stated as a hypothesis.

**4. Non-goals**  
At least three things this brief will not solve.

**5. Risks**  
The assumption that would kill the bet if false.

**Deliberately not done**
- A feature list titled as a brief.
- Invented user quotes.
- No non-goals.

**Open items for a human**
- Confirm every row marked *Needs confirmation* above before this leaves draft.
- Anything absent from the file stayed absent. No figure, date, or name was supplied from outside it.

Next: Jonah Park by 30 September 2026. This is a draft, not a sign-off.

## Anti-patterns

- A feature list titled as a brief.
- Invented user quotes.
- No non-goals.

## Related skills

- `opportunity-assessment`
- `prd-writer`
