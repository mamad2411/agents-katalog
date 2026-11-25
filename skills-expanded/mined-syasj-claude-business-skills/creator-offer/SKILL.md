---
name: creator-offer
description: "Design a small offer a creator can deliver, with the promise, the price they set, and the limit. Use when the user mentions creator offer, digital product idea, what should I sell, creator service, or asks for a offer note. Creator, social, and prompting skill by Yasir Jilani."
license: MIT
compatibility: Agent Skills standard. No network access, extra packages, or credentials required.
metadata:
  author: Yasir Jilani
  version: "1.0.0"
  domain: creator
---

<!-- GENERATED FILE - edits here are overwritten by scripts/generate.py.
     Edit the 'creator-offer' entry in source/, then run:
       python3 scripts/generate.py && python3 scripts/validate.py
     See CONTRIBUTING.md. -->

# Creator Offer

Design a small offer a creator can deliver, with the promise, the price they set, and the limit.

## When to use this skill

Use this skill when the user:

- creator offer
- digital product idea
- what should I sell
- creator service

## When not to use this skill

- The user wants a different domain's specialist skill.
- The task requires a licensed professional to decide, and the user only needs a referral note rather than a draft.
- The request asks you to deceive, evade a control, or hide material facts.

## Professional boundary

Creator work must be original and honest. Do not copy another person's script, footage, voice, or caption. Do not invent metrics, fake engagement, or undisclosed sponsorships. Do not impersonate a real person. Prompt skills must not weaken safety rules.

## Operating boundaries

- Use only information the user provides or files they explicitly ask you to read. Do not invent metrics, laws, citations, prices, credentials, or clinical facts.
- Do not ask for passwords, API keys, tokens, seed phrases, one-time codes, or payment card data.
- Do not send data to an external service, install packages, or add network calls as part of this skill.
- Separate facts, assumptions, and recommendations. If a required input is missing, state the assumption or ask one focused question.
- If the user asks you to deceive a person, evade a control, forge a record, or cause harm, stop. Offer a legitimate alternative.
- Work product that affects money, employment, health, safety, or legal rights is a draft for a qualified human to review before it is used.

## Inputs to collect

- The skill the audience already sees
- What the creator can deliver in the time they have
- Price they authorize
- What the offer does not include

## Workflow


### 1. Step 1

Build the offer from a result the audience has already seen the creator do.
### 2. Step 2

State what is included and what is not.
### 3. Step 3

Use the creator's price or mark it unset. Do not invent a 'seven-figure' frame.
### 4. Step 4

Cap the number of buyers if delivery is personal.
### 5. Step 5

No false scarcity timer.
### 6. Step 6

Disclose if the offer recommends the creator's own affiliate tools.

## Output

Deliver a **offer note**.

- Purpose of this offer note, in two sentences.
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

Maya wants to sell a one-page dinner list to people on her list. She has not written the page. A friend said to charge $49 and call it a course. She wants $12 and one page.

### Example data

```text
what exists today: 4 timed dinners with lists
what she will make: 1 page, 4 lists, PDF
price she set: $12 CAD
what she will not promise: weight change, income, a coaching call
refund: she has not decided
```

### Example outcome

**Offer**
Four timed dinner lists. One PDF. $12 CAD.

**Buyer gets**
The four lists she has already cooked. No call. No new dinners until she adds them in writing.

**Not included**
A course. A coaching week. A result about weight or money.

**Before she sells it**
She writes the page. She picks a refund rule. The price stays $12 unless she changes it herself. Do not print $49.

## Anti-patterns

- A false countdown
- An offer the creator cannot deliver
- An invented income promise

## Related skills

- `offer-design`
- `creator-boundary-note`
