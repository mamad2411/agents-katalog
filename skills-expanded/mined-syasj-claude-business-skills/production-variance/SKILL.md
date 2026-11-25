---
name: production-variance
description: "Compare produced volumes to the nomination using the meters the user provides. Use when the user mentions production variance, actual versus nomination, daily production, volume miss, or asks for a variance note. Oil and gas operations skill by Yasir Jilani."
license: MIT
compatibility: Agent Skills standard. No network access, extra packages, or credentials required.
metadata:
  author: Yasir Jilani
  version: "1.0.0"
  domain: oil-gas
---

<!-- GENERATED FILE - edits here are overwritten by scripts/generate.py.
     Edit the 'production-variance' entry in source/, then run:
       python3 scripts/generate.py && python3 scripts/validate.py
     See CONTRIBUTING.md. -->

# Production Variance

Compare produced volumes to the nomination using the meters the user provides.

## When to use this skill

Use this skill when the user:

- production variance
- actual versus nomination
- daily production
- volume miss

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

- The nomination
- The meter volumes
- The day
- Who explains the gap

## Workflow


### 1. Step 1

Use their meters.
### 2. Step 2

Show nomination, actual, and gap.
### 3. Step 3

Do not invent a reservoir cause.
### 4. Step 4

Separate a meter they flagged as bad.
### 5. Step 5

Name the person who explains a gap over their threshold.
### 6. Step 6

Do not adjust a number to match the nomination.

## Output

Deliver a **variance note**.

- Purpose of this variance note, in two sentences.
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

Devon has Tuesday's numbers for pad 14-22. The nomination was 4.2 mmcf. The meter, which he flagged as clean, read 3.6. He wants the variance without a reservoir story.

### Example data

```text
day: 16 Sep 2026
pad: 14-22
nomination: 4.2 mmcf
meter: 3.6 mmcf
meter note: clean, no fault flag
threshold for a call: 0.3 mmcf
who explains: Devon Hale
```

### Example outcome

**Variance — pad 14-22, 16 September**
Nomination 4.2. Meter 3.6. Gap 0.6. Over his 0.3 threshold.
Meter note is clean, so this note does not blame the meter and does not invent a reservoir cause.
No adjustment to make 3.6 look like 4.2.
Next: Devon writes the explanation. This note only records the gap.

## Anti-patterns

- A volume changed to match the nom
- A cause with no meter
- A bad meter treated as good

## Related skills

- `gas-nomination`
- `gas-balance`
