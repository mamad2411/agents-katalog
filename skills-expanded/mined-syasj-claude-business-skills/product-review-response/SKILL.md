---
name: product-review-response
description: "Draft a response to a customer product review that acknowledges the experience and does not argue. Use when the user mentions review response, respond to review, customer review reply, product feedback response, or asks for a review response. Retail and commerce skill by Yasir Jilani."
license: MIT
compatibility: Agent Skills standard. No network access, extra packages, or credentials required.
metadata:
  author: Yasir Jilani
  version: "1.0.0"
  domain: retail
---

<!-- GENERATED FILE - edits here are overwritten by scripts/generate.py.
     Edit the 'product-review-response' entry in source/, then run:
       python3 scripts/generate.py && python3 scripts/validate.py
     See CONTRIBUTING.md. -->

# Product Review Response

Draft a response to a customer product review that acknowledges the experience and does not argue.

## When to use this skill

Use this skill when the user:

- review response
- respond to review
- customer review reply
- product feedback response

## When not to use this skill

- The user wants a different domain's specialist skill.
- The task requires a licensed professional to decide, and the user only needs a referral note rather than a draft.
- The request asks you to deceive, evade a control, or hide material facts.

## Professional boundary

Do not invent inventory, prices, or reviews. Do not write deceptive promotions.

## Operating boundaries

- Use only information the user provides or files they explicitly ask you to read. Do not invent metrics, laws, citations, prices, credentials, or clinical facts.
- Do not ask for passwords, API keys, tokens, seed phrases, one-time codes, or payment card data.
- Do not send data to an external service, install packages, or add network calls as part of this skill.
- Separate facts, assumptions, and recommendations. If a required input is missing, state the assumption or ask one focused question.
- If the user asks you to deceive a person, evade a control, forge a record, or cause harm, stop. Offer a legitimate alternative.
- Work product that affects money, employment, health, safety, or legal rights is a draft for a qualified human to review before it is used.

## Inputs to collect

- The review text
- The star rating
- What the brand can offer
- Whether the issue is known

## Workflow


### 1. Step 1

Acknowledge what the reviewer said without paraphrasing it back sarcastically.
### 2. Step 2

Do not argue about whether the experience happened.
### 3. Step 3

If an issue is known and fixed, say so specifically.
### 4. Step 4

If resolution is possible, invite a private conversation and name the contact method.
### 5. Step 5

Keep it short. A long response looks defensive.
### 6. Step 6

Do not paste a template that ignores what they actually said.

## Output

Deliver a **review response**.

- Purpose of this review response, in two sentences.
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

Diane Cho, store lead at Harbor Goods in Airdrie, needs a review response by 30 September 2026. A one-star review says the zipper broke in a week. The response says "we're sorry you feel that way."

### Example data

```text
From: Diane Cho, store lead
Organization: Harbor Goods, Airdrie
Date: 14 September 2026
Needed by: 30 September 2026

A one-star review says the zipper broke in a week. The response says "we're sorry you feel that way."

The review text: SKU 1044 cabin filter, recorded 14 September 2026. No supporting file attached
The star rating: SKU 1044 cabin filter, recorded 14 September 2026. No supporting file attached
What the brand can offer: CAD 120, dates not set, cap not set
Whether the issue is known: SKU 1044 cabin filter. Partly documented: the what is written down, the who is not
```

### Example outcome

**Review response**
To: Diane Cho, store lead, Harbor Goods
Date: 14 September 2026 · Needed by: 30 September 2026

**Decision**
Acknowledges the zipper, says what the warranty covers, and invites a direct contact.

**What the file supports**

| Input | Value | Status |
| --- | --- | --- |
| The review text | SKU 1044 cabin filter, recorded 14 September 2026. No supporting file attached | Needs confirmation |
| The star rating | SKU 1044 cabin filter, recorded 14 September 2026. No supporting file attached | Carried into the draft |
| What the brand can offer | CAD 120, dates not set, cap not set | Carried into the draft |
| Whether the issue is known | SKU 1044 cabin filter. Partly documented: the what is written down, the who is not | Needs confirmation |

**How this draft was built**

**1. Acknowledge what the reviewer said without paraphrasing it back sarcastically**

**2. Do not argue about whether the experience happened**

**3. If an issue is known and fixed, say so specifically**

**4. If resolution is possible, invite a private conversation and name the contact method**

**5. Keep it short. A long response looks defensive**

**Deliberately not done**
- Arguing with the reviewer.
- A copy-paste template.
- Promising a fix you cannot deliver.

**Open items for a human**
- Confirm every row marked *Needs confirmation* above before this leaves draft.
- Anything absent from the file stayed absent. No figure, date, or name was supplied from outside it.

Next: Diane Cho by 30 September 2026. This is a draft, not a sign-off.

## Anti-patterns

- Arguing with the reviewer
- A copy-paste template
- Promising a fix you cannot deliver

## Related skills

- `service-recovery`
- `support-macro`
