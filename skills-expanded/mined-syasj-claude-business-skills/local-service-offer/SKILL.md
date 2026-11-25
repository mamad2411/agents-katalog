---
name: local-service-offer
description: "Write a local offer from the price and the hours the owner can honor. Use when the user mentions local offer, shop special, service offer, what should I advertise, or asks for a offer. Small business skill by Yasir Jilani."
license: MIT
compatibility: Agent Skills standard. No network access, extra packages, or credentials required.
metadata:
  author: Yasir Jilani
  version: "1.0.0"
  domain: small-business
---

<!-- GENERATED FILE - edits here are overwritten by scripts/generate.py.
     Edit the 'local-service-offer' entry in source/, then run:
       python3 scripts/generate.py && python3 scripts/validate.py
     See CONTRIBUTING.md. -->

# Local Service Offer

Write a local offer from the price and the hours the owner can honor.

## When to use this skill

Use this skill when the user:

- local offer
- shop special
- service offer
- what should I advertise

## When not to use this skill

- The user wants a different domain's specialist skill.
- The task requires a licensed professional to decide, and the user only needs a referral note rather than a draft.
- The request asks you to deceive, evade a control, or hide material facts.

## Professional boundary

Not legal, tax, or employment advice. Do not invent license rules, tax rates, or a local bylaw.

## Operating boundaries

- Use only information the user provides or files they explicitly ask you to read. Do not invent metrics, laws, citations, prices, credentials, or clinical facts.
- Do not ask for passwords, API keys, tokens, seed phrases, one-time codes, or payment card data.
- Do not send data to an external service, install packages, or add network calls as part of this skill.
- Separate facts, assumptions, and recommendations. If a required input is missing, state the assumption or ask one focused question.
- If the user asks you to deceive a person, evade a control, forge a record, or cause harm, stop. Offer a legitimate alternative.
- Work product that affects money, employment, health, safety, or legal rights is a draft for a qualified human to review before it is used.

## Inputs to collect

- The service
- The price they will honor
- The dates
- The limit

## Workflow


### 1. Step 1

Use their price.
### 2. Step 2

Limit the dates.
### 3. Step 3

State how many they can do.
### 4. Step 4

Do not add a discount they did not set.
### 5. Step 5

Match the hours on the door.
### 6. Step 6

No fake scarcity.

## Output

Deliver a **offer**.

- Purpose of this offer, in two sentences.
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

An ad draft says half-price oil changes all month. Diane priced $49 for Fridays only, and the lane can do six cars a day. The door is closed Sunday.

### Example data

```text
service: oil change
price she will honor: $49, Fridays in September 2026
capacity: 6 cars
door: closed Sunday
draft ad: half price, all month
half-price figure: she did not set one
```

### Example outcome

**Offer**
Friday oil changes, $49, six cars. September Fridays only.

Not the offer: half price, all month, Sunday.
Six is the cap. When six are booked, the ad stops for that Friday. No fake 'only two left' if the book is empty.
The door hours stand. Sunday is closed.

## Anti-patterns

- A price they cannot honor
- A fake countdown
- Hours that contradict the door

## Related skills

- `local-seo-note`
- `dealer-launch-check`
