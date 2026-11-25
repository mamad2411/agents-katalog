---
name: positioning-statement
description: "Write a positioning statement that names the buyer, the alternative, and the difference you can prove. Use when the user mentions positioning, positioning statement, who is this for, category message, or asks for a positioning statement. Marketing skill by Yasir Jilani."
license: MIT
compatibility: Agent Skills standard. No network access, extra packages, or credentials required.
metadata:
  author: Yasir Jilani
  version: "1.0.0"
  domain: marketing
---

<!-- GENERATED FILE - edits here are overwritten by scripts/generate.py.
     Edit the 'positioning-statement' entry in source/, then run:
       python3 scripts/generate.py && python3 scripts/validate.py
     See CONTRIBUTING.md. -->

# Positioning Statement

Write a positioning statement that names the buyer, the alternative, and the difference you can prove.

## When to use this skill

Use this skill when the user:

- positioning
- positioning statement
- who is this for
- category message

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

- The primary buyer
- The alternative they use today
- The difference you can prove
- Buyers you will not serve

## Workflow


### 1. Buyer

One primary buyer. A statement for everyone is a statement for no one.
### 2. Alternative

Include the status quo. Name a vendor only if the user supplied that competitor.
### 3. Difference

One difference that matters to the buyer's job and that the user can evidence.
### 4. Proof

The evidence sits next to the difference. If proof is missing, the positioning is a hypothesis.
### 5. Boundary

Who it is not for. That line protects sales from bad-fit deals.
### 6. Length

A short statement plus a paragraph. No manifesto.

## Output

Deliver a **positioning statement**.

- Purpose of this positioning statement, in two sentences.
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

Lena Ortiz, marketing lead at Fieldnote in Edmonton, needs a positioning statement by 30 September 2026. A team says they are the 'AI platform for business' and cannot name the buyer or the alternative.

### Example data

```text
From: Lena Ortiz, marketing lead
Organization: Fieldnote, Edmonton
Date: 14 September 2026
Needed by: 30 September 2026

A team says they are the 'AI platform for business' and cannot name the buyer or the alternative.

The primary buyer: Kite Freight
The alternative they use today: two deals cited from memory. Neither has a written loss reason
The difference you can prove: Fall service page, recorded 14 September 2026. No supporting file attached
Buyers you will not serve: Fall service page. Stated in the ask, not documented anywhere else
```

### Example outcome

**Positioning statement**
To: Lena Ortiz, marketing lead, Fieldnote
Date: 14 September 2026 · Needed by: 30 September 2026

**Decision**
A statement aimed at one buyer, with the spreadsheet or incumbent they actually replace, and a hypothesis label if proof is thin.

**What the file supports**

| Input | Value | Status |
| --- | --- | --- |
| The primary buyer | Kite Freight | Needs confirmation |
| The alternative they use today | two deals cited from memory. Neither has a written loss reason | Carried into the draft |
| The difference you can prove | Fall service page, recorded 14 September 2026. No supporting file attached | Carried into the draft |
| Buyers you will not serve | Fall service page. Stated in the ask, not documented anywhere else | Needs confirmation |

**How this draft was built**

**1. Buyer**  
One primary buyer. A statement for everyone is a statement for no one.

**2. Alternative**  
Include the status quo. Name a vendor only if the user supplied that competitor.

**3. Difference**  
One difference that matters to the buyer's job and that the user can evidence.

**4. Proof**  
The evidence sits next to the difference. If proof is missing, the positioning is a hypothesis.

**5. Boundary**  
Who it is not for. That line protects sales from bad-fit deals.

**Deliberately not done**
- Positioning for everyone.
- A difference you cannot prove.
- A category claim copied from a larger company.

**Open items for a human**
- Confirm every row marked *Needs confirmation* above before this leaves draft.
- Anything absent from the file stayed absent. No figure, date, or name was supplied from outside it.

Next: Lena Ortiz by 30 September 2026. This is a draft, not a sign-off.

## Anti-patterns

- Positioning for everyone.
- A difference you cannot prove.
- A category claim copied from a larger company.

## Related skills

- `messaging-house`
- `competitive-strategy`
