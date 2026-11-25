---
name: tariff-change-note
description: "Explain a tariff change from the sheet the user has, in the units on that sheet. Use when the user mentions tariff change, rate change, utility rate, price plan change, or asks for a tariff note. Energy and utilities operations skill by Yasir Jilani."
license: MIT
compatibility: Agent Skills standard. No network access, extra packages, or credentials required.
metadata:
  author: Yasir Jilani
  version: "1.0.0"
  domain: energy
---

<!-- GENERATED FILE - edits here are overwritten by scripts/generate.py.
     Edit the 'tariff-change-note' entry in source/, then run:
       python3 scripts/generate.py && python3 scripts/validate.py
     See CONTRIBUTING.md. -->

# Tariff Change Note

Explain a tariff change from the sheet the user has, in the units on that sheet.

## When to use this skill

Use this skill when the user:

- tariff change
- rate change
- utility rate
- price plan change

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

- The old rate
- The new rate
- The date
- Who is affected

## Workflow


### 1. Step 1

Use the sheet.
### 2. Step 2

Show old and new in the same unit.
### 3. Step 3

Do not invent a bill impact without their usage.
### 4. Step 4

Name the date it starts.
### 5. Step 5

Say who it applies to, from the sheet.
### 6. Step 6

This is not a regulatory filing.

## Output

Deliver a **tariff note**.

- Purpose of this tariff note, in two sentences.
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

Prairie Line's small-site rate sheet shows energy at 9.2 cents per kWh until 30 September and 9.8 cents from 1 October. A draft says bills will rise 20 percent. No usage file is attached.

### Example data

```text
old: 9.2 cents/kWh through 30 Sep 2026
new: 9.8 cents/kWh from 1 Oct 2026
who: small commercial sites on this sheet
usage: not attached
draft claim: bills up 20 percent
```

### Example outcome

**Tariff note**
From 1 October 2026 the sheet shows 9.8 cents per kWh, up from 9.2. Same unit.
The 20 percent bill line comes out. No usage was attached, so no bill impact is calculated.
Who: small commercial sites on this sheet. Do not extend it to every account.
This is not a filing.

## Anti-patterns

- A bill impact with no usage
- A rate from memory
- A start date they do not have

## Related skills

- `utility-bill-check`
- `pricing-margin-bridge`
