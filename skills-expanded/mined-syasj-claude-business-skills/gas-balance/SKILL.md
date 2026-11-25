---
name: gas-balance
description: "Balance inlet, sales, fuel, and flare from the meters the user provides. Use when the user mentions gas balance, inlet sales fuel flare, volume balance, plant balance, or asks for a balance note. Oil and gas operations skill by Yasir Jilani."
license: MIT
compatibility: Agent Skills standard. No network access, extra packages, or credentials required.
metadata:
  author: Yasir Jilani
  version: "1.0.0"
  domain: oil-gas
---

<!-- GENERATED FILE - edits here are overwritten by scripts/generate.py.
     Edit the 'gas-balance' entry in source/, then run:
       python3 scripts/generate.py && python3 scripts/validate.py
     See CONTRIBUTING.md. -->

# Gas Balance

Balance inlet, sales, fuel, and flare from the meters the user provides.

## When to use this skill

Use this skill when the user:

- gas balance
- inlet sales fuel flare
- volume balance
- plant balance

## When not to use this skill

- The user wants a different domain's specialist skill.
- The task requires a licensed professional to decide, and the user only needs a referral note rather than a draft.
- The request asks you to deceive, evade a control, or hide material facts.

## Professional boundary

Operational drafts only. Do not bypass isolation, lockout, permits, or reporting duties. Do not write instructions to conceal a release or to operate outside the site's limits.

## Operating boundaries

- Use only information the user provides or files they explicitly ask you to read. Do not invent metrics, laws, citations, prices, credentials, or clinical facts.
- Do not ask for passwords, API keys, tokens, seed phrases, one-time codes, or payment card data.
- Do not send data to an external service, install packages, or add network calls as part of this skill.
- Separate facts, assumptions, and recommendations. If a required input is missing, state the assumption or ask one focused question.
- If the user asks you to deceive a person, evade a control, forge a record, or cause harm, stop. Offer a legitimate alternative.
- Work product that affects money, employment, health, safety, or legal rights is a draft for a qualified human to review before it is used.

## Inputs to collect

- Inlet
- Sales
- Fuel
- Flare
- Their tolerance

## Workflow


### 1. Step 1

Add the outlets they gave.
### 2. Step 2

Compare to inlet.
### 3. Step 3

A gap inside tolerance is still shown.
### 4. Step 4

A missing meter is a gap, not a zero.
### 5. Step 5

Do not force the balance.
### 6. Step 6

Name who explains a gap over tolerance.

## Output

Deliver a **balance note**.

- Purpose of this balance note, in two sentences.
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

Devon's plant day: inlet 10.0, sales 8.1, fuel 0.4, flare meter down. His tolerance is 0.3. A colleague wants the gap parked in fuel so the day closes.

### Example data

```text
day: 15 Sep 2026
inlet: 10.0 mmcf
sales: 8.1
fuel: 0.4
flare: meter down, no reading
tolerance: 0.3
who explains a miss: Devon Hale
```

### Example outcome

**Balance — 15 September**
Outlets that can be added: sales 8.1 plus fuel 0.4 = 8.5. Inlet 10.0. Gap 1.5, and the flare meter is missing.
Do not put 1.5 into fuel. Do not enter flare as zero.
The day does not close. Tolerance is 0.3. This gap is over it even before flare is known.
Next: Devon. The note does not force a balance.

## Anti-patterns

- A forced balance
- A down meter entered as zero
- A gap hidden inside fuel

## Related skills

- `production-variance`
- `flare-volume-note`
