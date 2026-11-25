---
name: consultation-summary
description: "Summarize a consultation without burying dissenting views. Use when the user mentions consultation summary, public comments, hearing summary, feedback summary public, or asks for a consultation summary. Public sector skill by Yasir Jilani."
license: MIT
compatibility: Agent Skills standard. No network access, extra packages, or credentials required.
metadata:
  author: Yasir Jilani
  version: "1.0.0"
  domain: public-sector
---

<!-- GENERATED FILE - edits here are overwritten by scripts/generate.py.
     Edit the 'consultation-summary' entry in source/, then run:
       python3 scripts/generate.py && python3 scripts/validate.py
     See CONTRIBUTING.md. -->

# Consultation Summary

Summarize a consultation without burying dissenting views.

## When to use this skill

Use this skill when the user:

- consultation summary
- public comments
- hearing summary
- feedback summary public

## When not to use this skill

- The user wants a different domain's specialist skill.
- The task requires a licensed professional to decide, and the user only needs a referral note rather than a draft.
- The request asks you to deceive, evade a control, or hide material facts.

## Professional boundary

Public work should be accurate, even-handed, and suitable for the record. Do not draft deceptive communications, voter manipulation, or surveillance programs.

## Operating boundaries

- Use only information the user provides or files they explicitly ask you to read. Do not invent metrics, laws, citations, prices, credentials, or clinical facts.
- Do not ask for passwords, API keys, tokens, seed phrases, one-time codes, or payment card data.
- Do not send data to an external service, install packages, or add network calls as part of this skill.
- Separate facts, assumptions, and recommendations. If a required input is missing, state the assumption or ask one focused question.
- If the user asks you to deceive a person, evade a control, forge a record, or cause harm, stop. Offer a legitimate alternative.
- Work product that affects money, employment, health, safety, or legal rights is a draft for a qualified human to review before it is used.

## Inputs to collect

- The question consulted
- The responses they have
- How people were invited
- The decision still open

## Workflow


### 1. Step 1

State the question and the invitation method.
### 2. Step 2

Count responses only from their log.
### 3. Step 3

Summarize themes and include dissent.
### 4. Step 4

Do not claim the public agreed if the sample is self-selected. Say so.
### 5. Step 5

Separate comments from the decision.
### 6. Step 6

Do not identify private individuals beyond their public submission rules.

## Output

Deliver a **consultation summary**.

- Purpose of this consultation summary, in two sentences.
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

Pat Nguyen, clerk at Town of Airdrie in Airdrie, needs a consultation summary by 30 September 2026. A summary says residents support a plan when most comments opposed it.

### Example data

```text
From: Pat Nguyen, clerk
Organization: Town of Airdrie, Airdrie
Date: 14 September 2026
Needed by: 30 September 2026

A summary says residents support a plan when most comments opposed it.

The question consulted: A summary says residents support a plan when most comments opposed it
The responses they have: Council agenda item 6, recorded 14 September 2026. No supporting file attached
How people were invited: Posted comment period, last reviewed 14 September 2026. No owner named since
The decision still open: A summary says residents support a plan when most comments opposed it
```

### Example outcome

**Consultation summary**
To: Pat Nguyen, clerk, Town of Airdrie
Date: 14 September 2026 · Needed by: 30 September 2026

**Decision**
Reports the opposition and refuses the support claim.

**What the file supports**

| Input | Value | Status |
| --- | --- | --- |
| The question consulted | A summary says residents support a plan when most comments opposed it | Needs confirmation |
| The responses they have | Council agenda item 6, recorded 14 September 2026. No supporting file attached | Carried into the draft |
| How people were invited | Posted comment period, last reviewed 14 September 2026. No owner named since | Carried into the draft |
| The decision still open | A summary says residents support a plan when most comments opposed it | Needs confirmation |

**How this draft was built**

**1. State the question and the invitation method**

**2. Count responses only from their log**

**3. Summarize themes and include dissent**

**4. Do not claim the public agreed if the sample is self-selected. Say so**

**5. Separate comments from the decision**

**Deliberately not done**
- Buried dissent.
- A false claim of public agreement.
- Identifying private people against their rules.

**Open items for a human**
- Confirm every row marked *Needs confirmation* above before this leaves draft.
- Anything absent from the file stayed absent. No figure, date, or name was supplied from outside it.

Next: Pat Nguyen by 30 September 2026. This is a draft, not a sign-off.

## Anti-patterns

- Buried dissent
- A false claim of public agreement
- Identifying private people against their rules

## Related skills

- `survey-analysis`
- `feedback-synthesis`
