---
name: category-design
description: "Pressure-test a category narrative so it teaches the buyer a real shift, not a made-up adjective. Use when the user mentions category design, category narrative, create a category, market category, or asks for a category narrative review. Marketing skill by Yasir Jilani."
license: MIT
compatibility: Agent Skills standard. No network access, extra packages, or credentials required.
metadata:
  author: Yasir Jilani
  version: "1.0.0"
  domain: marketing
---

<!-- GENERATED FILE - edits here are overwritten by scripts/generate.py.
     Edit the 'category-design' entry in source/, then run:
       python3 scripts/generate.py && python3 scripts/validate.py
     See CONTRIBUTING.md. -->

# Category Narrative

Pressure-test a category narrative so it teaches the buyer a real shift, not a made-up adjective.

## When to use this skill

Use this skill when the user:

- category design
- category narrative
- create a category
- market category

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

- The shift the buyer is experiencing
- The old way
- Evidence the shift is real
- The company's right to speak

## Workflow


### 1. Shift

Describe the buyer's change in their language. A new adjective is not a category.
### 2. Old way

What they do today, fairly. Do not caricature customers.
### 3. Evidence

Signs the shift is happening outside the company's slide. If the only evidence is the slide, call it a hypothesis.
### 4. Right to speak

Why this company is a credible teacher of the shift. A narrative without credibility is an ad.
### 5. Language

A name the buyer can use in a meeting. If they would not say it, it is internal.
### 6. Restraint

Do not tell the team to 'own the category' as a fact. Recommend a teaching plan instead.

## Output

Deliver a **category narrative review**.

- Purpose of this category narrative review, in two sentences.
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

Lena Ortiz, marketing lead at Fieldnote in Edmonton, needs a category narrative review by 30 September 2026. A startup wants to announce it created a new category because it added an AI button.

### Example data

```text
From: Lena Ortiz, marketing lead
Organization: Fieldnote, Edmonton
Date: 14 September 2026
Needed by: 30 September 2026

A startup wants to announce it created a new category because it added an AI button.

The shift the buyer is experiencing: Fall service page, recorded 14 September 2026. No supporting file attached
The old way: Fall service page, recorded 14 September 2026. No supporting file attached
Evidence the shift is real: one PDF, 2 pages, dated 14 September 2026
The company's right to speak: Fall service page, recorded 14 September 2026. No supporting file attached
```

### Example outcome

**Category narrative review**
To: Lena Ortiz, marketing lead, Fieldnote
Date: 14 September 2026 · Needed by: 30 September 2026

**Decision**
Rejects the announcement, restates the missing buyer shift, and proposes a hypothesis test instead.

**What the file supports**

| Input | Value | Status |
| --- | --- | --- |
| The shift the buyer is experiencing | Fall service page, recorded 14 September 2026. No supporting file attached | Needs confirmation |
| The old way | Fall service page, recorded 14 September 2026. No supporting file attached | Carried into the draft |
| Evidence the shift is real | one PDF, 2 pages, dated 14 September 2026 | Carried into the draft |
| The company's right to speak | Fall service page, recorded 14 September 2026. No supporting file attached | Needs confirmation |

**How this draft was built**

**1. Shift**  
Describe the buyer's change in their language. A new adjective is not a category.

**2. Old way**  
What they do today, fairly. Do not caricature customers.

**3. Evidence**  
Signs the shift is happening outside the company's slide. If the only evidence is the slide, call it a hypothesis.

**4. Right to speak**  
Why this company is a credible teacher of the shift. A narrative without credibility is an ad.

**5. Language**  
A name the buyer can use in a meeting. If they would not say it, it is internal.

**Deliberately not done**
- A coined adjective with no buyer shift.
- Declaring category ownership.
- Mocking the customer's current tools.

**Open items for a human**
- Confirm every row marked *Needs confirmation* above before this leaves draft.
- Anything absent from the file stayed absent. No figure, date, or name was supplied from outside it.

Next: Lena Ortiz by 30 September 2026. This is a draft, not a sign-off.

## Anti-patterns

- A coined adjective with no buyer shift.
- Declaring category ownership.
- Mocking the customer's current tools.

## Related skills

- `positioning-statement`
- `corporate-narrative`
