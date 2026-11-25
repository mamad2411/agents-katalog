---
name: utility-bill-check
description: "Check a bill against the meter read and the rate the user has. Use when the user mentions utility bill, check this bill, energy invoice, bill audit, or asks for a bill check. Energy and utilities operations skill by Yasir Jilani."
license: MIT
compatibility: Agent Skills standard. No network access, extra packages, or credentials required.
metadata:
  author: Yasir Jilani
  version: "1.0.0"
  domain: energy
---

<!-- GENERATED FILE - edits here are overwritten by scripts/generate.py.
     Edit the 'utility-bill-check' entry in source/, then run:
       python3 scripts/generate.py && python3 scripts/validate.py
     See CONTRIBUTING.md. -->

# Utility Bill Check

Check a bill against the meter read and the rate the user has.

## When to use this skill

Use this skill when the user:

- utility bill
- check this bill
- energy invoice
- bill audit

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

- The bill
- The meter read
- The rate sheet
- The prior bill if they have it

## Workflow


### 1. Step 1

Compare the billed units to the read they have.
### 2. Step 2

Apply the rate from their sheet.
### 3. Step 3

A mismatch is a finding, not a fraud claim.
### 4. Step 4

Do not invent a tax.
### 5. Step 5

Say which line cannot be checked.
### 6. Step 6

Name who calls the utility.

## Output

Deliver a **bill check**.

- Purpose of this bill check, in two sentences.
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

The September bill for site meter 4 shows 1,200 kWh. The read book shows 48,200 minus 47,150, which is 1,050. The rate sheet is 9.2 cents. Devon wants the check before anyone calls it fraud.

### Example data

```text
bill: Sep 2026, meter 4, 1200 kWh
read: 48200 end, 47150 start
rate sheet: 9.2 cents/kWh
prior bill: not in the folder
who calls: Devon Hale
```

### Example outcome

**Bill check**
Read difference: 47,150 to 48,200 is 1,050 kWh. Bill says 1,200. Gap 150 kWh.
At 9.2 cents that is a dollar gap, not a fraud finding. This note does not accuse anyone.
Lines not checked: riders and tax. The prior bill is not in the folder.
Next: Devon asks the utility about the 150 kWh. He does not short-pay from this note alone.

## Anti-patterns

- A fraud claim from a mismatch
- A rate from memory
- A tax invented to force the total

## Related skills

- `tariff-change-note`
