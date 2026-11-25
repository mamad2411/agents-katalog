---
name: flare-volume-note
description: "Report flare volumes from the meter the user has, with the reason code they supplied. Use when the user mentions flare report, flaring volume, flare log, gas flared, or asks for a flare note. Oil and gas operations skill by Yasir Jilani."
license: MIT
compatibility: Agent Skills standard. No network access, extra packages, or credentials required.
metadata:
  author: Yasir Jilani
  version: "1.0.0"
  domain: oil-gas
---

<!-- GENERATED FILE - edits here are overwritten by scripts/generate.py.
     Edit the 'flare-volume-note' entry in source/, then run:
       python3 scripts/generate.py && python3 scripts/validate.py
     See CONTRIBUTING.md. -->

# Flare Volume Note

Report flare volumes from the meter the user has, with the reason code they supplied.

## When to use this skill

Use this skill when the user:

- flare report
- flaring volume
- flare log
- gas flared

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

- The meter
- The volume
- The reason code they use
- The period

## Workflow


### 1. Step 1

Use the meter volume.
### 2. Step 2

Use their reason code. Do not invent a regulatory factor.
### 3. Step 3

If the meter was down, say the volume is missing.
### 4. Step 4

Do not estimate a flare to fill a report.
### 5. Step 5

Name who signs the report.
### 6. Step 6

This is not an emissions assurance opinion.

## Output

Deliver a **flare note**.

- Purpose of this flare note, in two sentences.
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

The flare meter was down on 12 September. A draft report enters zero so the month still adds up. Devon has a reason code for a compressor trip on the 11th, when the meter worked.

### Example data

```text
period: 11 and 12 Sep 2026
11 Sep: meter 0.18 mmcf, reason code CT-compressor, his code
12 Sep: meter down, no reading
draft: 12 Sep entered as 0
signer: Devon Hale
```

### Example outcome

**Flare note**
11 September: 0.18 mmcf, reason CT-compressor, from his code. Use that.
12 September: blank. The meter was down. Zero is rejected. An estimate is not in this note.
This is not an emissions-factor calculation and not an assurance opinion.
Signer: Devon, after the 12th stays blank or a real reading replaces it.

## Anti-patterns

- An estimated flare presented as metered
- A factor from memory
- A down meter called zero

## Related skills

- `emissions-inventory-brief`
- `production-variance`
