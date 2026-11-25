---
name: demand-response-offer
description: "Review a demand-response offer against the load the user can actually drop. Use when the user mentions demand response, curtailment offer, load shed offer, DR contract, or asks for a offer note. Energy and utilities operations skill by Yasir Jilani."
license: MIT
compatibility: Agent Skills standard. No network access, extra packages, or credentials required.
metadata:
  author: Yasir Jilani
  version: "1.0.0"
  domain: energy
---

<!-- GENERATED FILE - edits here are overwritten by scripts/generate.py.
     Edit the 'demand-response-offer' entry in source/, then run:
       python3 scripts/generate.py && python3 scripts/validate.py
     See CONTRIBUTING.md. -->

# Demand Response Offer

Review a demand-response offer against the load the user can actually drop.

## When to use this skill

Use this skill when the user:

- demand response
- curtailment offer
- load shed offer
- DR contract

## When not to use this skill

- The user wants a different domain's specialist skill.
- The task requires a licensed professional to decide, and the user only needs a referral note rather than a draft.
- The request asks you to deceive, evade a control, or hide material facts.

## Professional boundary

Operational energy advice is not a permit and not a safety case. Do not bypass lockout, isolation, or regulatory limits.

## Operating boundaries

- Use only information the user provides or files they explicitly ask you to read. Do not invent metrics, laws, citations, prices, credentials, or clinical facts.
- Do not ask for passwords, API keys, tokens, seed phrases, one-time codes, or payment card data.
- Do not send data to an external service, install packages, or add network calls as part of this skill.
- Separate facts, assumptions, and recommendations. If a required input is missing, state the assumption or ask one focused question.
- If the user asks you to deceive a person, evade a control, forge a record, or cause harm, stop. Offer a legitimate alternative.
- Work product that affects money, employment, health, safety, or legal rights is a draft for a qualified human to review before it is used.

## Inputs to collect

- The offer
- The load they can drop
- The hours
- The penalty they highlighted

## Workflow


### 1. Step 1

Compare the offer's drop to the load they can show.
### 2. Step 2

If they cannot drop that much, say so.
### 3. Step 3

Note the hours.
### 4. Step 4

Put the penalty in the note if they highlighted it.
### 5. Step 5

Do not invent a payment.
### 6. Step 6

Recommend sign only if the drop fits.

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

An offer pays for a 500 kW drop on weekday afternoons. The site log shows they can shed 200 kW by turning off two pumps. The offer includes a penalty if they miss the drop. The payment figure is $40 per kW-month.

### Example data

```text
offer drop: 500 kW
hours: weekdays 14:00-18:00
load they can drop: 200 kW, two pumps, log from August
penalty: in the offer, highlighted
payment: $40 per kW-month, in the offer
```

### Example outcome

**Offer note**
Do not sign for 500 kW. The log shows 200.
If they sign, the number has to be a drop they have shown. 200 is the figure in the file.
Penalty: it is in the offer. Do not leave it out of the conversation.
Payment in the offer: $40 per kW-month. This note does not improve it.
Hours match a window they can staff only if Devon says the pumps can stop at 14:00. He has not said that yet.

## Anti-patterns

- A drop they cannot make
- A payment not in the offer
- A penalty left out

## Related skills

- `curtailment-note`
- `tariff-change-note`
