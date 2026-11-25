---
name: customer-story
description: "Draft a customer story only from approved facts and the customer's words. Use when the user mentions customer story, case study, testimonial, customer quote, or asks for a customer story draft. Marketing skill by Yasir Jilani."
license: MIT
compatibility: Agent Skills standard. No network access, extra packages, or credentials required.
metadata:
  author: Yasir Jilani
  version: "1.0.0"
  domain: marketing
---

<!-- GENERATED FILE - edits here are overwritten by scripts/generate.py.
     Edit the 'customer-story' entry in source/, then run:
       python3 scripts/generate.py && python3 scripts/validate.py
     See CONTRIBUTING.md. -->

# Customer Story

Draft a customer story only from approved facts and the customer's words.

## When to use this skill

Use this skill when the user:

- customer story
- case study
- testimonial
- customer quote

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

- Approved facts and quotes
- The customer's approval status
- The outcome metrics they confirmed
- What they refused to say

## Workflow


### 1. Permission

If the customer has not approved the story, draft it as internal only and say so.
### 2. Quote hygiene

Use their words. Do not polish a quote into a different claim.
### 3. Metrics

Only numbers they confirmed. A 'significant improvement' stays qualitative if no number exists.
### 4. Structure

Problem, what they did, what changed, and what did not change. Honesty includes limits.
### 5. No invention

Do not add a logo wall, a job title, or a company size they did not confirm.
### 6. Approval line

What the customer still needs to sign off before publication.

## Output

Deliver a **customer story draft**.

- Purpose of this customer story draft, in two sentences.
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

Lena Ortiz, marketing lead at Fieldnote in Edmonton, needs a customer story draft by 30 September 2026. A marketer wants a case study that says costs fell 40 percent, and the customer only said 'it saved us time'.

### Example data

```text
From: Lena Ortiz, marketing lead
Organization: Fieldnote, Edmonton
Date: 14 September 2026
Needed by: 30 September 2026

A marketer wants a case study that says costs fell 40 percent, and the customer only said 'it saved us time'.

Approved facts and quotes: Email to lapsed buyers. Partly documented: the what is written down, the who is not
The customer's approval status: Fall service page, recorded 14 September 2026. No supporting file attached
The outcome metrics they confirmed: plan 180, actual 95
What they refused to say: A marketer wants a case study that says costs fell 40 percent, and the customer only said 'it saved us time'
```

### Example outcome

**Customer story draft**
To: Lena Ortiz, marketing lead, Fieldnote
Date: 14 September 2026 · Needed by: 30 September 2026

**Decision**
Keeps the time quote, omits the percentage, and marks publication as blocked until approval.

**What the file supports**

| Input | Value | Status |
| --- | --- | --- |
| Approved facts and quotes | Email to lapsed buyers. Partly documented: the what is written down, the who is not | Needs confirmation |
| The customer's approval status | Fall service page, recorded 14 September 2026. No supporting file attached | Carried into the draft |
| The outcome metrics they confirmed | plan 180, actual 95 | Carried into the draft |
| What they refused to say | A marketer wants a case study that says costs fell 40 percent, and the customer only said 'it saved us time' | Needs confirmation |

**How this draft was built**

**1. Permission**  
If the customer has not approved the story, draft it as internal only and say so.

**2. Quote hygiene**  
Use their words. Do not polish a quote into a different claim.

**3. Metrics**  
Only numbers they confirmed. A 'significant improvement' stays qualitative if no number exists.

**4. Structure**  
Problem, what they did, what changed, and what did not change. Honesty includes limits.

**5. No invention**  
Do not add a logo wall, a job title, or a company size they did not confirm.

**Deliberately not done**
- Invented quotes.
- Metrics the customer did not confirm.
- Publishing before approval.

**Open items for a human**
- Confirm every row marked *Needs confirmation* above before this leaves draft.
- Anything absent from the file stayed absent. No figure, date, or name was supplied from outside it.

Next: Lena Ortiz by 30 September 2026. This is a draft, not a sign-off.

## Anti-patterns

- Invented quotes.
- Metrics the customer did not confirm.
- Publishing before approval.

## Related skills

- `marketing-claims-review`
