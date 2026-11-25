---
name: analyst-briefing
description: "Prepare an analyst or reviewer briefing that separates roadmap from shipped product. Use when the user mentions analyst briefing, reviewer briefing, industry analyst prep, briefing notes, or asks for a analyst briefing notes. Marketing skill by Yasir Jilani."
license: MIT
compatibility: Agent Skills standard. No network access, extra packages, or credentials required.
metadata:
  author: Yasir Jilani
  version: "1.0.0"
  domain: marketing
---

<!-- GENERATED FILE - edits here are overwritten by scripts/generate.py.
     Edit the 'analyst-briefing' entry in source/, then run:
       python3 scripts/generate.py && python3 scripts/validate.py
     See CONTRIBUTING.md. -->

# Analyst Briefing

Prepare an analyst or reviewer briefing that separates roadmap from shipped product.

## When to use this skill

Use this skill when the user:

- analyst briefing
- reviewer briefing
- industry analyst prep
- briefing notes

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

- The questions they are likely to ask
- Shipped facts
- Roadmap items that must be labeled
- Proof

## Workflow


### 1. Shipped versus planned

Two lists. Never let planned items sit in the shipped list.
### 2. Proof pack

The metrics and customer evidence cleared for sharing.
### 3. Answers

Short answers to likely questions, including where the product is a poor fit.
### 4. Claims

Remove anything the claims review would block.
### 5. Follow-up

What you will send after, and what you will not send because it is unverified.
### 6. Tone

Brief and precise. No hype adjectives standing in for facts.

## Output

Deliver a **analyst briefing notes**.

- Purpose of this analyst briefing notes, in two sentences.
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

Lena Ortiz, marketing lead at Fieldnote in Edmonton, needs an analyst briefing notes by 30 September 2026. A briefing deck shows a beta feature in the current architecture diagram with no label.

### Example data

```text
From: Lena Ortiz, marketing lead
Organization: Fieldnote, Edmonton
Date: 14 September 2026
Needed by: 30 September 2026

A briefing deck shows a beta feature in the current architecture diagram with no label.

The questions they are likely to ask: A briefing deck shows a beta feature in the current architecture diagram with no label
Shipped facts: Local search ad, last reviewed 14 September 2026. No owner named since
Roadmap items that must be labeled: Fall service page. Stated in the ask, not documented anywhere else
Proof: one customer email, 14 September 2026, no attachment beyond that
```

### Example outcome

**Analyst briefing notes**
To: Lena Ortiz, marketing lead, Fieldnote
Date: 14 September 2026 · Needed by: 30 September 2026

**Decision**
Notes that label the beta, move it out of the shipped list, and include the poor-fit segment.

**What the file supports**

| Input | Value | Status |
| --- | --- | --- |
| The questions they are likely to ask | A briefing deck shows a beta feature in the current architecture diagram with no label | Needs confirmation |
| Shipped facts | Local search ad, last reviewed 14 September 2026. No owner named since | Carried into the draft |
| Roadmap items that must be labeled | Fall service page. Stated in the ask, not documented anywhere else | Carried into the draft |
| Proof | one customer email, 14 September 2026, no attachment beyond that | Needs confirmation |

**How this draft was built**

**1. Shipped versus planned**  
Two lists. Never let planned items sit in the shipped list.

**2. Proof pack**  
The metrics and customer evidence cleared for sharing.

**3. Answers**  
Short answers to likely questions, including where the product is a poor fit.

**4. Claims**  
Remove anything the claims review would block.

**5. Follow-up**  
What you will send after, and what you will not send because it is unverified.

**Deliberately not done**
- Roadmap presented as shipped.
- Hiding the poor-fit segment.
- Unverified metrics in the leave-behind.

**Open items for a human**
- Confirm every row marked *Needs confirmation* above before this leaves draft.
- Anything absent from the file stayed absent. No figure, date, or name was supplied from outside it.

Next: Lena Ortiz by 30 September 2026. This is a draft, not a sign-off.

## Anti-patterns

- Roadmap presented as shipped.
- Hiding the poor-fit segment.
- Unverified metrics in the leave-behind.

## Related skills

- `positioning-statement`
- `marketing-claims-review`
