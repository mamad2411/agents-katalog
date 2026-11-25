---
name: dealer-morning-review
description: "Set the service morning from the appointments and the parts the dealer can see. Use when the user mentions dealer morning, service morning huddle, shop board, advisor huddle, or asks for a morning note. Automotive skill by Yasir Jilani."
license: MIT
compatibility: Agent Skills standard. No network access, extra packages, or credentials required.
metadata:
  author: Yasir Jilani
  version: "1.0.0"
  domain: automotive
---

<!-- GENERATED FILE - edits here are overwritten by scripts/generate.py.
     Edit the 'dealer-morning-review' entry in source/, then run:
       python3 scripts/generate.py && python3 scripts/validate.py
     See CONTRIBUTING.md. -->

# Dealer Morning Review

Set the service morning from the appointments and the parts the dealer can see.

## When to use this skill

Use this skill when the user:

- dealer morning
- service morning huddle
- shop board
- advisor huddle

## When not to use this skill

- The user wants a different domain's specialist skill.
- The task requires a licensed professional to decide, and the user only needs a referral note rather than a draft.
- The request asks you to deceive, evade a control, or hide material facts.

## Professional boundary

Not a repair procedure for safety-critical systems and not a recall determination. Do not invent defect rates or tell anyone to disable a safety feature.

## Operating boundaries

- Use only information the user provides or files they explicitly ask you to read. Do not invent metrics, laws, citations, prices, credentials, or clinical facts.
- Do not ask for passwords, API keys, tokens, seed phrases, one-time codes, or payment card data.
- Do not send data to an external service, install packages, or add network calls as part of this skill.
- Separate facts, assumptions, and recommendations. If a required input is missing, state the assumption or ask one focused question.
- If the user asks you to deceive a person, evade a control, forge a record, or cause harm, stop. Offer a legitimate alternative.
- Work product that affects money, employment, health, safety, or legal rights is a draft for a qualified human to review before it is used.

## Inputs to collect

- Today's appointments
- Parts not in
- Techs on shift
- A job that must not be promised

## Workflow


### 1. Step 1

List appointments they can start.
### 2. Step 2

Hold jobs whose parts are not in.
### 3. Step 3

Match techs on shift, not the full roster.
### 4. Step 4

Do not promise a same-day finish the parts cannot support.
### 5. Step 5

Name the advisor who calls the customer.
### 6. Step 6

Do not invent a capacity number.

## Output

Deliver a **morning note**.

- Purpose of this morning note, in two sentences.
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

Bright Axle has 14 appointments today and 2 techs on shift. RO 4418 is a brake job. The pads are not in. Carla needs the board before 7:30.

### Example data

```text
date: 16 Sep 2026
appointments: 14
techs on shift: 2
off: 1 tech
RO 4418: brake pads not in, customer was told today
advisor who calls: Carla Singh
```

### Example outcome

**Morning board**
Do not promise RO 4418 today. Pads are not in. Carla calls before 8:00.
Techs on the board: 2. The third name stays off.
The other appointments stay only if parts are in. This note does not invent a capacity number beyond those two techs.
Next: Carla, the 4418 call.

## Anti-patterns

- A promise with parts missing
- A tech counted who is off
- A full board that cannot be worked

## Related skills

- `service-lane-plan`
- `parts-backorder-note`
