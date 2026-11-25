---
name: jobs-to-be-done
description: "Frame a job-to-be-done from a real situation, including the hire and the fire. Use when the user mentions jobs to be done, JTBD, job story, what job is the user hiring, or asks for a job story. Product skill by Yasir Jilani."
license: MIT
compatibility: Agent Skills standard. No network access, extra packages, or credentials required.
metadata:
  author: Yasir Jilani
  version: "1.0.0"
  domain: product
---

<!-- GENERATED FILE - edits here are overwritten by scripts/generate.py.
     Edit the 'jobs-to-be-done' entry in source/, then run:
       python3 scripts/generate.py && python3 scripts/validate.py
     See CONTRIBUTING.md. -->

# Jobs To Be Done

Frame a job-to-be-done from a real situation, including the hire and the fire.

## When to use this skill

Use this skill when the user:

- jobs to be done
- JTBD
- job story
- what job is the user hiring

## When not to use this skill

- The user wants a different domain's specialist skill.
- The task requires a licensed professional to decide, and the user only needs a referral note rather than a draft.
- The request asks you to deceive, evade a control, or hide material facts.

## Professional boundary

Product recommendations are hypotheses until evidence says otherwise. Label confidence. Do not ship dark patterns that hide cost or consent.

## Operating boundaries

- Use only information the user provides or files they explicitly ask you to read. Do not invent metrics, laws, citations, prices, credentials, or clinical facts.
- Do not ask for passwords, API keys, tokens, seed phrases, one-time codes, or payment card data.
- Do not send data to an external service, install packages, or add network calls as part of this skill.
- Separate facts, assumptions, and recommendations. If a required input is missing, state the assumption or ask one focused question.
- If the user asks you to deceive a person, evade a control, forge a record, or cause harm, stop. Offer a legitimate alternative.
- Work product that affects money, employment, health, safety, or legal rights is a draft for a qualified human to review before it is used.

## Inputs to collect

- A recent incident the user described
- What the person was trying to achieve
- What they used instead
- Forces they mentioned

## Workflow


### 1. Situation

When and where the struggle showed up. No situation, no job story.
### 2. Motivation

The progress they wanted, in their words if available.
### 3. Hire

What they used, including spreadsheets and workarounds.
### 4. Fire

What was awkward about the old way, from evidence, not from your pitch.
### 5. Anxieties

What made a new approach feel risky, if they said so. Do not invent psychology.
### 6. Implication

What the product must be hired to do, and what it should not pretend to do.

## Output

Deliver a **job story**.

- Purpose of this job story, in two sentences.
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

Jonah Park, product manager at Fieldnote in Edmonton, needs a job story by 30 September 2026. A team writes the job as 'use our dashboard' after a customer described exporting to a spreadsheet.

### Example data

```text
From: Jonah Park, product manager
Organization: Fieldnote, Edmonton
Date: 14 September 2026
Needed by: 30 September 2026

A team writes the job as 'use our dashboard' after a customer described exporting to a spreadsheet.

A recent incident the user described: Activation checklist, first seen 14 September 2026. No root cause recorded yet
What the person was trying to achieve: Usage limit warning, last reviewed 14 September 2026. No owner named since
What they used instead: A team writes the job as 'use our dashboard' after a customer described exporting to a spreadsheet
Forces they mentioned: Trial day-3 email, last reviewed 14 September 2026. No owner named since
```

### Example outcome

**Job story**
To: Jonah Park, product manager, Fieldnote
Date: 14 September 2026 · Needed by: 30 September 2026

**Decision**
A job story about the export moment, with the spreadsheet as the current hire.

**What the file supports**

| Input | Value | Status |
| --- | --- | --- |
| A recent incident the user described | Activation checklist, first seen 14 September 2026. No root cause recorded yet | Needs confirmation |
| What the person was trying to achieve | Usage limit warning, last reviewed 14 September 2026. No owner named since | Carried into the draft |
| What they used instead | A team writes the job as 'use our dashboard' after a customer described exporting to a spreadsheet | Carried into the draft |
| Forces they mentioned | Trial day-3 email, last reviewed 14 September 2026. No owner named since | Needs confirmation |

**How this draft was built**

**1. Situation**  
When and where the struggle showed up. No situation, no job story.

**2. Motivation**  
The progress they wanted, in their words if available.

**3. Hire**  
What they used, including spreadsheets and workarounds.

**4. Fire**  
What was awkward about the old way, from evidence, not from your pitch.

**5. Anxieties**  
What made a new approach feel risky, if they said so. Do not invent psychology.

**Deliberately not done**
- A job story that is a feature request in costume.
- Invented anxieties.
- Ignoring the workaround they already hired.

**Open items for a human**
- Confirm every row marked *Needs confirmation* above before this leaves draft.
- Anything absent from the file stayed absent. No figure, date, or name was supplied from outside it.

Next: Jonah Park by 30 September 2026. This is a draft, not a sign-off.

## Anti-patterns

- A job story that is a feature request in costume.
- Invented anxieties.
- Ignoring the workaround they already hired.

## Related skills

- `discovery-interview`
- `product-brief`
