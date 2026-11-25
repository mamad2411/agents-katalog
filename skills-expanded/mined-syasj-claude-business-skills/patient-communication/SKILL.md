---
name: patient-communication
description: "Draft a patient message in plain language that a clinician or clinic lead approves before sending. Use when the user mentions patient message, clinic letter, patient instructions draft, portal message, or asks for a patient message. Healthcare practice operations skill by Yasir Jilani."
license: MIT
compatibility: Agent Skills standard. No network access, extra packages, or credentials required.
metadata:
  author: Yasir Jilani
  version: "1.0.0"
  domain: healthcare
---

<!-- GENERATED FILE - edits here are overwritten by scripts/generate.py.
     Edit the 'patient-communication' entry in source/, then run:
       python3 scripts/generate.py && python3 scripts/validate.py
     See CONTRIBUTING.md. -->

# Patient Communication Draft

Draft a patient message in plain language that a clinician or clinic lead approves before sending.

## When to use this skill

Use this skill when the user:

- patient message
- clinic letter
- patient instructions draft
- portal message

## When not to use this skill

- Medication changes
- Diagnosis

## Professional boundary

This is not medical advice, diagnosis, or a treatment protocol. Do not recommend drugs, doses, or clinical interventions. Limit the work to practice operations, documentation quality, and communication drafts for a licensed clinician to approve.

## Operating boundaries

- Use only information the user provides or files they explicitly ask you to read. Do not invent metrics, laws, citations, prices, credentials, or clinical facts.
- Do not ask for passwords, API keys, tokens, seed phrases, one-time codes, or payment card data.
- Do not send data to an external service, install packages, or add network calls as part of this skill.
- Separate facts, assumptions, and recommendations. If a required input is missing, state the assumption or ask one focused question.
- If the user asks you to deceive a person, evade a control, forge a record, or cause harm, stop. Offer a legitimate alternative.
- Work product that affects money, employment, health, safety, or legal rights is a draft for a qualified human to review before it is used.

## Inputs to collect

- The purpose
- Facts a clinician confirmed
- The reading level they want
- The approval owner

## Workflow


### 1. Step 1

State the purpose in the first line.
### 2. Step 2

Include only facts a clinician or the record confirmed. Do not add advice, doses, or a diagnosis.
### 3. Step 3

Tell the patient who to call if symptoms worry them, using their escalation line.
### 4. Step 4

Avoid blame and jargon.
### 5. Step 5

Mark the draft unsent until the named clinician or lead approves it.
### 6. Step 6

Do not include another patient's information.

## Output

Deliver a **patient message**.

- Purpose of this patient message, in two sentences.
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

Dr. Helen Cho, clinic director at Cedar Clinic in Red Deer, needs a patient message by 30 September 2026. A draft tells a patient to double a medicine because the refill is late.

### Example data

```text
From: Dr. Helen Cho, clinic director
Organization: Cedar Clinic, Red Deer
Date: 14 September 2026
Needed by: 30 September 2026

A draft tells a patient to double a medicine because the refill is late.

The purpose: A draft tells a patient to double a medicine because the refill is late. Stated once, in the ask. Not written down anywhere else
Facts a clinician confirmed: Thursday clinic and one other, both unconfirmed as of 14 September 2026
The reading level they want: Tuesday clinic, recorded 14 September 2026. No supporting file attached
The approval owner: Dr. Helen Cho, clinic director
```

### Example outcome

**Patient message**
To: Dr. Helen Cho, clinic director, Cedar Clinic
Date: 14 September 2026 · Needed by: 30 September 2026

**Decision**
Removes the dose change, explains the operational status, and waits for clinician approval.

**What the file supports**

| Input | Value | Status |
| --- | --- | --- |
| The purpose | A draft tells a patient to double a medicine because the refill is late. Stated once, in the ask. Not written down anywhere else | Needs confirmation |
| Facts a clinician confirmed | Thursday clinic and one other, both unconfirmed as of 14 September 2026 | Carried into the draft |
| The reading level they want | Tuesday clinic, recorded 14 September 2026. No supporting file attached | Carried into the draft |
| The approval owner | Dr. Helen Cho, clinic director | Needs confirmation |

**How this draft was built**

**1. State the purpose in the first line**

**2. Include only facts a clinician or the record confirmed. Do not add advice, doses, or a diagnosis**

**3. Tell the patient who to call if symptoms worry them, using their escalation line**

**4. Avoid blame and jargon**

**5. Mark the draft unsent until the named clinician or lead approves it**

**Deliberately not done**
- Doses or new diagnoses.
- An unapproved clinical instruction.
- Another patient's data.

**Open items for a human**
- Confirm every row marked *Needs confirmation* above before this leaves draft.
- Anything absent from the file stayed absent. No figure, date, or name was supplied from outside it.

Next: Dr. Helen Cho by 30 September 2026. This is a draft, not a sign-off.

## Anti-patterns

- Doses or new diagnoses
- An unapproved clinical instruction
- Another patient's data

## Related skills

- `patient-experience-clinic`
- `clinical-documentation-quality`
