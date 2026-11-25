---
name: interview-guide-research
description: "Write a research interview guide that asks about lived events and records consent the user already requires. Use when the user mentions research interview, qualitative interview guide, interview protocol, field interview, or asks for a research interview guide. Research skill by Yasir Jilani."
license: MIT
compatibility: Agent Skills standard. No network access, extra packages, or credentials required.
metadata:
  author: Yasir Jilani
  version: "1.0.0"
  domain: research
---

<!-- GENERATED FILE - edits here are overwritten by scripts/generate.py.
     Edit the 'interview-guide-research' entry in source/, then run:
       python3 scripts/generate.py && python3 scripts/validate.py
     See CONTRIBUTING.md. -->

# Research Interview Guide

Write a research interview guide that asks about lived events and records consent the user already requires.

## When to use this skill

Use this skill when the user:

- research interview
- qualitative interview guide
- interview protocol
- field interview

## When not to use this skill

- The user wants a different domain's specialist skill.
- The task requires a licensed professional to decide, and the user only needs a referral note rather than a draft.
- The request asks you to deceive, evade a control, or hide material facts.

## Professional boundary

Do not fabricate citations, quotations, data, or participants. Separate evidence you were given from claims that still need a source.

## Operating boundaries

- Use only information the user provides or files they explicitly ask you to read. Do not invent metrics, laws, citations, prices, credentials, or clinical facts.
- Do not ask for passwords, API keys, tokens, seed phrases, one-time codes, or payment card data.
- Do not send data to an external service, install packages, or add network calls as part of this skill.
- Separate facts, assumptions, and recommendations. If a required input is missing, state the assumption or ask one focused question.
- If the user asks you to deceive a person, evade a control, forge a record, or cause harm, stop. Offer a legitimate alternative.
- Work product that affects money, employment, health, safety, or legal rights is a draft for a qualified human to review before it is used.

## Inputs to collect

- The question
- The participant type
- Consent requirements they stated
- Sensitive topics

## Workflow


### 1. Step 1

Open with consent in the form they specified. Do not invent a legal consent standard.
### 2. Step 2

Ask about recent events, not hypothetical ideals.
### 3. Step 3

Order questions from safer context to more sensitive topics.
### 4. Step 4

Plan probes that do not put words in the participant's mouth.
### 5. Step 5

State how notes will be stored, using their plan. Do not design covert recording.
### 6. Step 6

This is research, not a sales discovery call, unless they said it is both.

## Output

Deliver a **research interview guide**.

- Purpose of this research interview guide, in two sentences.
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

Dr. Nia Okonkwo, research lead at Riverbend College in Lethbridge, needs a research interview guide by 30 September 2026. A guide starts by asking participants to agree that the product is essential.

### Example data

```text
From: Dr. Nia Okonkwo, research lead
Organization: Riverbend College, Lethbridge
Date: 14 September 2026
Needed by: 30 September 2026

A guide starts by asking participants to agree that the product is essential.

The question: A guide starts by asking participants to agree that the product is essential
The participant type: Dr. Nia Okonkwo plus two others named in the thread. No distribution list attached
Consent requirements they stated: their one-page rule dated 2 Mar 2026. No exception log since
Sensitive topics: email and billing address only. They stated no health or payment data
```

### Example outcome

**Research interview guide**
To: Dr. Nia Okonkwo, research lead, Riverbend College
Date: 14 September 2026 · Needed by: 30 September 2026

**Decision**
Asks for the last real incident and includes their consent step.

**What the file supports**

| Input | Value | Status |
| --- | --- | --- |
| The question | A guide starts by asking participants to agree that the product is essential | Needs confirmation |
| The participant type | Dr. Nia Okonkwo plus two others named in the thread. No distribution list attached | Carried into the draft |
| Consent requirements they stated | their one-page rule dated 2 Mar 2026. No exception log since | Carried into the draft |
| Sensitive topics | email and billing address only. They stated no health or payment data | Needs confirmation |

**How this draft was built**

**1. Open with consent in the form they specified. Do not invent a legal consent standard**

**2. Ask about recent events, not hypothetical ideals**

**3. Order questions from safer context to more sensitive topics**

**4. Plan probes that do not put words in the participant's mouth**

**5. State how notes will be stored, using their plan. Do not design covert recording**

**Deliberately not done**
- Covert recording.
- Leading questions that supply the finding.
- Skipping their consent step.

**Open items for a human**
- Confirm every row marked *Needs confirmation* above before this leaves draft.
- Anything absent from the file stayed absent. No figure, date, or name was supplied from outside it.

Next: Dr. Nia Okonkwo by 30 September 2026. This is a draft, not a sign-off.

## Anti-patterns

- Covert recording
- Leading questions that supply the finding
- Skipping their consent step

## Related skills

- `discovery-interview`
- `qualitative-coding`
