---
name: logging-and-detection
description: "Specify defensive logs and alerts for a likely abuse, without writing an intrusion guide. Use when the user mentions detection use case, what should we alert on, security logging, audit logging, or asks for a detection note. Security defense skill by Yasir Jilani."
license: MIT
compatibility: Agent Skills standard. No network access, extra packages, or credentials required.
metadata:
  author: Yasir Jilani
  version: "1.0.0"
  domain: security
---

<!-- GENERATED FILE - edits here are overwritten by scripts/generate.py.
     Edit the 'logging-and-detection' entry in source/, then run:
       python3 scripts/generate.py && python3 scripts/validate.py
     See CONTRIBUTING.md. -->

# Logging and Detection

Specify defensive logs and alerts for a likely abuse, without writing an intrusion guide.

## When to use this skill

Use this skill when the user:

- detection use case
- what should we alert on
- security logging
- audit logging

## When not to use this skill

- The user wants a different domain's specialist skill.
- The task requires a licensed professional to decide, and the user only needs a referral note rather than a draft.
- The request asks you to deceive, evade a control, or hide material facts.

## Professional boundary

Defensive use only. Do not write exploits, payloads, bypasses, malware, or intrusion steps. Describe controls, ownership, detection, and safe verification.

## Operating boundaries

- Use only information the user provides or files they explicitly ask you to read. Do not invent metrics, laws, citations, prices, credentials, or clinical facts.
- Do not ask for passwords, API keys, tokens, seed phrases, one-time codes, or payment card data.
- Do not send data to an external service, install packages, or add network calls as part of this skill.
- Separate facts, assumptions, and recommendations. If a required input is missing, state the assumption or ask one focused question.
- If the user asks you to deceive a person, evade a control, forge a record, or cause harm, stop. Offer a legitimate alternative.
- Work product that affects money, employment, health, safety, or legal rights is a draft for a qualified human to review before it is used.

## Inputs to collect

- The abuse or failure to detect
- The logs they already have
- Who responds
- Privacy limits

## Workflow


### 1. Step 1

Describe the abuse in outcome language, such as mass export or repeated denied access. No attack procedure.
### 2. Step 2

Specify the event fields needed to investigate, excluding secrets and excessive personal data.
### 3. Step 3

Write the alert in terms of a threshold they choose, and who is paged.
### 4. Step 4

Include a false-positive note so the alert is tunable.
### 5. Step 5

State the response's first safe step, usually verify and contain, and point to the incident skill.
### 6. Step 6

Do not propose stealth monitoring of employees beyond the stated security event.

## Output

Deliver a **detection note**.

- Purpose of this detection note, in two sentences.
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

Aisha Rahman, engineering lead at Fieldnote in Edmonton, needs a detection note by 30 September 2026. A team wants an alert on data export but also asks to log every keystroke of a department.

### Example data

```text
From: Aisha Rahman, engineering lead
Organization: Fieldnote, Edmonton
Date: 14 September 2026
Needed by: 30 September 2026

A team wants an alert on data export but also asks to log every keystroke of a department.

The abuse or failure to detect: Access review Q3, first seen 14 September 2026. No root cause recorded yet
The logs they already have: one file, dated 14 September 2026. No earlier version attached for comparison
Who responds: Aisha Rahman, engineering lead
Privacy limits: email and billing address. They said no health data
```

### Example outcome

**Detection note**
To: Aisha Rahman, engineering lead, Fieldnote
Date: 14 September 2026 · Needed by: 30 September 2026

**Decision**
Refuses the keystroke surveillance.

**What the file supports**

| Input | Value | Status |
| --- | --- | --- |
| The abuse or failure to detect | Access review Q3, first seen 14 September 2026. No root cause recorded yet | Needs confirmation |
| The logs they already have | one file, dated 14 September 2026. No earlier version attached for comparison | Carried into the draft |
| Who responds | Aisha Rahman, engineering lead | Carried into the draft |
| Privacy limits | email and billing address. They said no health data | Needs confirmation |

**How this draft was built**

**1. Describe the abuse in outcome language, such as mass export or repeated denied access. No attack procedure**

**2. Specify the event fields needed to investigate, excluding secrets and excessive personal data**

**3. Write the alert in terms of a threshold they choose, and who is paged**

**4. Include a false-positive note so the alert is tunable**

**5. State the response's first safe step, usually verify and contain, and point to the incident skill**

**Deliberately not done**
- An intrusion how-to.
- Logging secrets.
- Employee surveillance beyond the stated event.

**Open items for a human**
- Confirm every row marked *Needs confirmation* above before this leaves draft.
- Anything absent from the file stayed absent. No figure, date, or name was supplied from outside it.

Next: Aisha Rahman by 30 September 2026. This is a draft, not a sign-off.

## Anti-patterns

- An intrusion how-to
- Logging secrets
- Employee surveillance beyond the stated event

## Related skills

- `observability-plan`
- `access-review`
