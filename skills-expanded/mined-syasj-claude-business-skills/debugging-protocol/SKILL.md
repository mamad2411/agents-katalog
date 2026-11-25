---
name: debugging-protocol
description: "Debug a defect by stating the symptom, the hypothesis, and the next observation, instead of changing five things at once. Use when the user mentions debug this, debugging help, why is this failing, defect investigation, or asks for a debugging note. Engineering skill by Yasir Jilani."
license: MIT
compatibility: Agent Skills standard. No network access, extra packages, or credentials required.
metadata:
  author: Yasir Jilani
  version: "1.0.0"
  domain: engineering
---

<!-- GENERATED FILE - edits here are overwritten by scripts/generate.py.
     Edit the 'debugging-protocol' entry in source/, then run:
       python3 scripts/generate.py && python3 scripts/validate.py
     See CONTRIBUTING.md. -->

# Debugging Protocol

Debug a defect by stating the symptom, the hypothesis, and the next observation, instead of changing five things at once.

## When to use this skill

Use this skill when the user:

- debug this
- debugging help
- why is this failing
- defect investigation

## When not to use this skill

- The user wants a different domain's specialist skill.
- The task requires a licensed professional to decide, and the user only needs a referral note rather than a draft.
- The request asks you to deceive, evade a control, or hide material facts.

## Professional boundary

Prefer the repository's existing patterns. Do not disable security controls, invent credentials, or introduce network calls the user did not ask for.

## Operating boundaries

- Use only information the user provides or files they explicitly ask you to read. Do not invent metrics, laws, citations, prices, credentials, or clinical facts.
- Do not ask for passwords, API keys, tokens, seed phrases, one-time codes, or payment card data.
- Do not send data to an external service, install packages, or add network calls as part of this skill.
- Separate facts, assumptions, and recommendations. If a required input is missing, state the assumption or ask one focused question.
- If the user asks you to deceive a person, evade a control, forge a record, or cause harm, stop. Offer a legitimate alternative.
- Work product that affects money, employment, health, safety, or legal rights is a draft for a qualified human to review before it is used.

## Inputs to collect

- The symptom
- What changed recently
- Evidence already collected
- The environment

## Workflow


### 1. Symptom

What the user or system does, and what was expected. Include the error text they provided. Do not invent logs.
### 2. Boundary

Where it last worked. Version, user, or data slice.
### 3. Hypothesis

One hypothesis that predicts a new observation.
### 4. Observation

The safest check that would confirm or kill it. Read-only before write actions.
### 5. Change

Only after the observation. One change at a time.
### 6. Record

What you learned, so the next person does not repeat the loop. No exploit development and no bypass of auth to 'make it easier'.

## Output

Deliver a **debugging note**.

- Purpose of this debugging note, in two sentences.
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

Aisha Rahman, engineering lead at Fieldnote in Edmonton, needs a debugging note by 30 September 2026. A bug appears only for one customer, and the draft plan changes three services before reading that customer's error.

### Example data

```text
From: Aisha Rahman, engineering lead
Organization: Fieldnote, Edmonton
Date: 14 September 2026
Needed by: 30 September 2026

A bug appears only for one customer, and the draft plan changes three services before reading that customer's error.

The symptom: Checkout service, recorded 14 September 2026. No supporting file attached
What changed recently: requested 14 September 2026. Not yet approved
Evidence already collected: one PDF, 2 pages, dated 14 September 2026
The environment: the one named in the ask. Version and owner not recorded
```

### Example outcome

**Debugging note**
To: Aisha Rahman, engineering lead, Fieldnote
Date: 14 September 2026 · Needed by: 30 September 2026

**Decision**
A note with one hypothesis, a read-only check, and a ban on disabling auth as a debugging shortcut.

**What the file supports**

| Input | Value | Status |
| --- | --- | --- |
| The symptom | Checkout service, recorded 14 September 2026. No supporting file attached | Needs confirmation |
| What changed recently | requested 14 September 2026. Not yet approved | Carried into the draft |
| Evidence already collected | one PDF, 2 pages, dated 14 September 2026 | Carried into the draft |
| The environment | the one named in the ask. Version and owner not recorded | Needs confirmation |

**How this draft was built**

**1. Symptom**  
What the user or system does, and what was expected. Include the error text they provided. Do not invent logs.

**2. Boundary**  
Where it last worked. Version, user, or data slice.

**3. Hypothesis**  
One hypothesis that predicts a new observation.

**4. Observation**  
The safest check that would confirm or kill it. Read-only before write actions.

**5. Change**  
Only after the observation. One change at a time.

**Deliberately not done**
- Changing five things at once.
- Inventing log lines.
- Disabling auth to debug.

**Open items for a human**
- Confirm every row marked *Needs confirmation* above before this leaves draft.
- Anything absent from the file stayed absent. No figure, date, or name was supplied from outside it.

Next: Aisha Rahman by 30 September 2026. This is a draft, not a sign-off.

## Anti-patterns

- Changing five things at once.
- Inventing log lines.
- Disabling auth to debug.

## Related skills

- `incident-postmortem`
- `code-review-standard`
