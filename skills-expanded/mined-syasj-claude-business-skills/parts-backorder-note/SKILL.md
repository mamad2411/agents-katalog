---
name: parts-backorder-note
description: "Tell the advisor what to say when a part is not in and a promise date is already on the RO. Use when the user mentions parts backorder, part not in, customer waiting on a part, ETA, or asks for a backorder note. Automotive skill by Yasir Jilani."
license: MIT
compatibility: Agent Skills standard. No network access, extra packages, or credentials required.
metadata:
  author: Yasir Jilani
  version: "1.0.0"
  domain: automotive
---

<!-- GENERATED FILE - edits here are overwritten by scripts/generate.py.
     Edit the 'parts-backorder-note' entry in source/, then run:
       python3 scripts/generate.py && python3 scripts/validate.py
     See CONTRIBUTING.md. -->

# Parts Backorder

Tell the advisor what to say when a part is not in and a promise date is already on the RO.

## When to use this skill

Use this skill when the user:

- parts backorder
- part not in
- customer waiting on a part
- ETA

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

- The RO
- The part
- The promise date
- The customer promise already made

## Workflow


### 1. Step 1

State the part and the RO.
### 2. Step 2

Use the ETA they have. If none, say none.
### 3. Step 3

Do not invent a delivery date.
### 4. Step 4

Compare to the promise already made.
### 5. Step 5

Give the advisor one sentence for the customer.
### 6. Step 6

Offer a loaner only if they said one is available.

## Output

Deliver a **backorder note**.

- Purpose of this backorder note, in two sentences.
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

RO 4418 was promised today. The brake pads are backordered. The supplier ETA field is blank. No loaner is free.

### Example data

```text
RO: 4418
part: front pads
promise already made: today, 16 Sep 2026
ETA: blank
loaner: none free
advisor: Carla Singh
```

### Example outcome

**What Carla can say**
The pads for RO 4418 are not in. I do not have a date. I am pulling today's promise.

Do not add a Friday ETA. The field is blank.
Do not offer a loaner. None is free.
Next: Carla makes the call. The RO promise date comes off today's board.

## Anti-patterns

- An invented ETA
- A loaner that does not exist
- A promise left unchanged when parts slipped

## Related skills

- `service-lane-plan`
- `dealer-morning-review`
