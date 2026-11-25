---
name: guest-recovery
description: "Plan guest recovery after a service miss, with a truthful apology and a remedy inside authority. Use when the user mentions guest recovery, hotel complaint, restaurant complaint, service miss hospitality, or asks for a guest recovery note. Hospitality skill by Yasir Jilani."
license: MIT
compatibility: Agent Skills standard. No network access, extra packages, or credentials required.
metadata:
  author: Yasir Jilani
  version: "1.0.0"
  domain: hospitality
---

<!-- GENERATED FILE - edits here are overwritten by scripts/generate.py.
     Edit the 'guest-recovery' entry in source/, then run:
       python3 scripts/generate.py && python3 scripts/validate.py
     See CONTRIBUTING.md. -->

# Guest Recovery

Plan guest recovery after a service miss, with a truthful apology and a remedy inside authority.

## When to use this skill

Use this skill when the user:

- guest recovery
- hotel complaint
- restaurant complaint
- service miss hospitality

## When not to use this skill

- Paying to remove a review

## Professional boundary

Guest recovery should be sincere and within policy. Do not invent compensation authority the user has not granted.

## Operating boundaries

- Use only information the user provides or files they explicitly ask you to read. Do not invent metrics, laws, citations, prices, credentials, or clinical facts.
- Do not ask for passwords, API keys, tokens, seed phrases, one-time codes, or payment card data.
- Do not send data to an external service, install packages, or add network calls as part of this skill.
- Separate facts, assumptions, and recommendations. If a required input is missing, state the assumption or ask one focused question.
- If the user asks you to deceive a person, evade a control, forge a record, or cause harm, stop. Offer a legitimate alternative.
- Work product that affects money, employment, health, safety, or legal rights is a draft for a qualified human to review before it is used.

## Inputs to collect

- The miss
- The guest's ask
- Authorized remedies
- The manager

## Workflow


### 1. Step 1

Acknowledge the specific miss.
### 2. Step 2

Do not invent a cause.
### 3. Step 3

Offer only an authorized remedy.
### 4. Step 4

Say what will change for the rest of the stay or meal if you know.
### 5. Step 5

Do not ask the guest to delete a review for compensation.
### 6. Step 6

Feed a repeated miss to the shift brief.

## Output

Deliver a **guest recovery note**.

- Purpose of this guest recovery note, in two sentences.
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

Sofia Alvarez, front office manager at Lantern Inn in Banff, needs a guest recovery note by 30 September 2026. A manager wants to offer a free stay if the guest removes a public review.

### Example data

```text
From: Sofia Alvarez, front office manager
Organization: Lantern Inn, Banff
Date: 14 September 2026
Needed by: 30 September 2026

A manager wants to offer a free stay if the guest removes a public review.

The miss: Friday dinner service, recorded 14 September 2026. No supporting file attached
The guest's ask: A manager wants to offer a free stay if the guest removes a public review. Stated once, in the ask. Not written down anywhere else
Authorized remedies: Friday dinner service and one other, both unconfirmed as of 14 September 2026
The manager: Friday dinner service, recorded 14 September 2026. No supporting file attached
```

### Example outcome

**Guest recovery note**
To: Sofia Alvarez, front office manager, Lantern Inn
Date: 14 September 2026 · Needed by: 30 September 2026

**Decision**
Refuses the bargain and stays inside the authorized remedy.

**What the file supports**

| Input | Value | Status |
| --- | --- | --- |
| The miss | Friday dinner service, recorded 14 September 2026. No supporting file attached | Needs confirmation |
| The guest's ask | A manager wants to offer a free stay if the guest removes a public review. Stated once, in the ask. Not written down anywhere else | Carried into the draft |
| Authorized remedies | Friday dinner service and one other, both unconfirmed as of 14 September 2026 | Carried into the draft |
| The manager | Friday dinner service, recorded 14 September 2026. No supporting file attached | Needs confirmation |

**How this draft was built**

**1. Acknowledge the specific miss**

**2. Do not invent a cause**

**3. Offer only an authorized remedy**

**4. Say what will change for the rest of the stay or meal if you know**

**5. Do not ask the guest to delete a review for compensation**

**Deliberately not done**
- A review-deletion bargain.
- An unauthorized comp.
- A fake cause.

**Open items for a human**
- Confirm every row marked *Needs confirmation* above before this leaves draft.
- Anything absent from the file stayed absent. No figure, date, or name was supplied from outside it.

Next: Sofia Alvarez by 30 September 2026. This is a draft, not a sign-off.

## Anti-patterns

- A review-deletion bargain
- An unauthorized comp
- A fake cause

## Related skills

- `service-recovery`
- `csat-recovery`
