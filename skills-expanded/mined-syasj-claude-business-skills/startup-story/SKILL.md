---
name: startup-story
description: "Write the company story from the customer and the fact they can show, not from a borrowed pitch. Use when the user mentions startup story, origin story, pitch narrative, what do we say we are, or asks for a story note. Entrepreneurship skill by Yasir Jilani."
license: MIT
compatibility: Agent Skills standard. No network access, extra packages, or credentials required.
metadata:
  author: Yasir Jilani
  version: "1.0.0"
  domain: entrepreneurship
---

<!-- GENERATED FILE - edits here are overwritten by scripts/generate.py.
     Edit the 'startup-story' entry in source/, then run:
       python3 scripts/generate.py && python3 scripts/validate.py
     See CONTRIBUTING.md. -->

# Startup Story

Write the company story from the customer and the fact they can show, not from a borrowed pitch.

## When to use this skill

Use this skill when the user:

- startup story
- origin story
- pitch narrative
- what do we say we are

## When not to use this skill

- The user wants a different domain's specialist skill.
- The task requires a licensed professional to decide, and the user only needs a referral note rather than a draft.
- The request asks you to deceive, evade a control, or hide material facts.

## Professional boundary

Startup advice is a set of choices, not a promise of funding or growth. Do not invent traction, customers, or investor interest.

## Operating boundaries

- Use only information the user provides or files they explicitly ask you to read. Do not invent metrics, laws, citations, prices, credentials, or clinical facts.
- Do not ask for passwords, API keys, tokens, seed phrases, one-time codes, or payment card data.
- Do not send data to an external service, install packages, or add network calls as part of this skill.
- Separate facts, assumptions, and recommendations. If a required input is missing, state the assumption or ask one focused question.
- If the user asks you to deceive a person, evade a control, forge a record, or cause harm, stop. Offer a legitimate alternative.
- Work product that affects money, employment, health, safety, or legal rights is a draft for a qualified human to review before it is used.

## Inputs to collect

- The customer
- The fact they can show
- The ask
- Lines they copied from another pitch

## Workflow


### 1. Step 1

Name the customer.
### 2. Step 2

Use one fact they can show.
### 3. Step 3

Cut a line copied from another company.
### 4. Step 4

Match the ask to the fact.
### 5. Step 5

Do not add a market size they did not source.
### 6. Step 6

Keep it to one paragraph and one proof.

## Output

Deliver a **story note**.

- Purpose of this story note, in two sentences.
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

Mara's draft says Northline is the Stripe of local shops and that the market is $4 billion. She can show four paying shops in Airdrie and Calgary. The ask is a $15,000 tooling budget, not a round.

### Example data

```text
customer: independent shops, four paying
fact: 4 shops pay $49 a month, started June 2026
ask: $15000 tooling budget
lines copied: Stripe of local shops, $4 billion market, no source
```

### Example outcome

**Story**
Four independent shops pay $49 a month to get their Saturday list off a whiteboard. That started in June 2026.

Ask: $15,000 for tooling. Not a round.

Cut: 'Stripe of local shops'. Cut: $4 billion. No source.
The proof is the four shops. The story does not get bigger than that.

## Anti-patterns

- A copied pitch
- An unsourced market size
- A story with no customer

## Related skills

- `idea-screen`
- `investor-update`
