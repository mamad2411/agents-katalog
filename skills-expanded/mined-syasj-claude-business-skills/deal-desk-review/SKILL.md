---
name: deal-desk-review
description: "Review a nonstandard deal for margin, precedent, and delivery risk before anyone signs. Use when the user mentions deal desk, nonstandard terms, discount approval, special deal review, or asks for a deal desk note. Sales skill by Yasir Jilani."
license: MIT
compatibility: Agent Skills standard. No network access, extra packages, or credentials required.
metadata:
  author: Yasir Jilani
  version: "1.0.0"
  domain: sales
---

<!-- GENERATED FILE - edits here are overwritten by scripts/generate.py.
     Edit the 'deal-desk-review' entry in source/, then run:
       python3 scripts/generate.py && python3 scripts/validate.py
     See CONTRIBUTING.md. -->

# Deal Desk Review

Review a nonstandard deal for margin, precedent, and delivery risk before anyone signs.

## When to use this skill

Use this skill when the user:

- deal desk
- nonstandard terms
- discount approval
- special deal review

## When not to use this skill

- The user wants a different domain's specialist skill.
- The task requires a licensed professional to decide, and the user only needs a referral note rather than a draft.
- The request asks you to deceive, evade a control, or hide material facts.

## Professional boundary

Sell honestly. Do not invent customer proof, discounts, or competitor facts. Do not write deceptive, phishing, or high-pressure scripts.

## Operating boundaries

- Use only information the user provides or files they explicitly ask you to read. Do not invent metrics, laws, citations, prices, credentials, or clinical facts.
- Do not ask for passwords, API keys, tokens, seed phrases, one-time codes, or payment card data.
- Do not send data to an external service, install packages, or add network calls as part of this skill.
- Separate facts, assumptions, and recommendations. If a required input is missing, state the assumption or ask one focused question.
- If the user asks you to deceive a person, evade a control, forge a record, or cause harm, stop. Offer a legitimate alternative.
- Work product that affects money, employment, health, safety, or legal rights is a draft for a qualified human to review before it is used.

## Inputs to collect

- The asked discount or term
- Margin math the user can show
- Delivery implications
- Precedent they worry about

## Workflow


### 1. Restate the ask

What is nonstandard, in one sentence.
### 2. Margin

Compute from their costs and price. If cost is missing, the review is incomplete. Do not invent a cost.
### 3. Delivery

Can the team deliver the promised start date and scope. A yes from sales is not a yes from delivery.
### 4. Precedent

Who else will ask for the same term if this is signed. Write that consequence.
### 5. Give-get

What the company gets for the concession.
### 6. Decision

Approve, approve with conditions, or decline. Name the approver role the user said has authority. Do not invent authority.

## Output

Deliver a **deal desk note**.

- Purpose of this deal desk note, in two sentences.
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

Samir Qureshi, account executive at Fieldnote in Edmonton, needs a deal desk note by 30 September 2026. Sales wants a custom integration included free to win a logo, and delivery has not estimated it.

### Example data

```text
From: Samir Qureshi, account executive
Organization: Fieldnote, Edmonton
Date: 14 September 2026
Needed by: 30 September 2026

Sales wants a custom integration included free to win a logo, and delivery has not estimated it.

The asked discount or term: Sales wants a custom integration included free to win a logo, and delivery has not estimated it. Stated once, in the ask. Not written down anywhere else
Margin math the user can show: Cedar Clinic, recorded 14 September 2026. No supporting file attached
Delivery implications: Cedar Clinic and one other, both unconfirmed as of 14 September 2026
Precedent they worry about: Cedar Clinic, last reviewed 14 September 2026. No owner named since
```

### Example outcome

**Deal desk note**
To: Samir Qureshi, account executive, Fieldnote
Date: 14 September 2026 · Needed by: 30 September 2026

**Decision**
Conditions any approval on a delivery estimate and names the precedent risk of free custom work.

**What the file supports**

| Input | Value | Status |
| --- | --- | --- |
| The asked discount or term | Sales wants a custom integration included free to win a logo, and delivery has not estimated it. Stated once, in the ask. Not written down anywhere else | Needs confirmation |
| Margin math the user can show | Cedar Clinic, recorded 14 September 2026. No supporting file attached | Carried into the draft |
| Delivery implications | Cedar Clinic and one other, both unconfirmed as of 14 September 2026 | Carried into the draft |
| Precedent they worry about | Cedar Clinic, last reviewed 14 September 2026. No owner named since | Needs confirmation |

**How this draft was built**

**1. Restate the ask**  
What is nonstandard, in one sentence.

**2. Margin**  
Compute from their costs and price. If cost is missing, the review is incomplete. Do not invent a cost.

**3. Delivery**  
Can the team deliver the promised start date and scope. A yes from sales is not a yes from delivery.

**4. Precedent**  
Who else will ask for the same term if this is signed. Write that consequence.

**5. Give-get**  
What the company gets for the concession.

**Deliberately not done**
- Approving a discount with no margin math.
- Ignoring delivery capacity.
- An approval that pretends not to set a precedent.

**Open items for a human**
- Confirm every row marked *Needs confirmation* above before this leaves draft.
- Anything absent from the file stayed absent. No figure, date, or name was supplied from outside it.

Next: Samir Qureshi by 30 September 2026. This is a draft, not a sign-off.

## Anti-patterns

- Approving a discount with no margin math.
- Ignoring delivery capacity.
- An approval that pretends not to set a precedent.

## Related skills

- `pricing-negotiation`
- `proposal-writer`
