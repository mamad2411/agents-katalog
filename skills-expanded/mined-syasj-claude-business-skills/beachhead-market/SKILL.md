---
name: beachhead-market
description: "Pick the first market from the customers they can already reach. Use when the user mentions beachhead, first market, who is the wedge, niche first, or asks for a beachhead note. Entrepreneurship skill by Yasir Jilani."
license: MIT
compatibility: Agent Skills standard. No network access, extra packages, or credentials required.
metadata:
  author: Yasir Jilani
  version: "1.0.0"
  domain: entrepreneurship
---

<!-- GENERATED FILE - edits here are overwritten by scripts/generate.py.
     Edit the 'beachhead-market' entry in source/, then run:
       python3 scripts/generate.py && python3 scripts/validate.py
     See CONTRIBUTING.md. -->

# Beachhead Market

Pick the first market from the customers they can already reach.

## When to use this skill

Use this skill when the user:

- beachhead
- first market
- who is the wedge
- niche first

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

- The segments they named
- Who they can reach this month
- Who pays today
- A segment they should not chase yet

## Workflow


### 1. Step 1

Prefer the segment they can reach.
### 2. Step 2

A paying customer beats a imagined segment.
### 3. Step 3

Say who is not the beachhead.
### 4. Step 4

Do not pick a segment because it is large.
### 5. Step 5

Name the offer for that segment.
### 6. Step 6

One beachhead.

## Output

Deliver a **beachhead note**.

- Purpose of this beachhead note, in two sentences.
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

Mara can visit shops in Airdrie and north Calgary this month. A draft says the beachhead is every small business in Canada because the market is larger.

### Example data

```text
can reach this month: shops in Airdrie and north Calgary, she can drive there
pays today: 4 shops, 3 in that drive
draft beachhead: every small business in Canada
offer: $49 Saturday list
```

### Example outcome

**Beachhead**
Shops she can drive to in Airdrie and north Calgary. One beachhead.
Not now: every small business in Canada. Size is not the reason.
Offer for this segment: the $49 Saturday list. Do not add a second product to chase a bigger map.
Three of the four paying shops are already in this drive. That is the wedge.

## Anti-patterns

- A beachhead they cannot reach
- Two beachheads
- A choice based on market size alone

## Related skills

- `idea-screen`
- `first-ten-customers`
