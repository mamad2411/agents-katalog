---
name: telehealth-visit-ops
description: "Write the operations checklist for a telehealth visit: identity, consent, backup, and privacy. Use when the user mentions telehealth operations, virtual visit checklist, video visit SOP, remote clinic visit, or asks for a telehealth operations checklist. Healthcare practice operations skill by Yasir Jilani."
license: MIT
compatibility: Agent Skills standard. No network access, extra packages, or credentials required.
metadata:
  author: Yasir Jilani
  version: "1.0.0"
  domain: healthcare
---

<!-- GENERATED FILE - edits here are overwritten by scripts/generate.py.
     Edit the 'telehealth-visit-ops' entry in source/, then run:
       python3 scripts/generate.py && python3 scripts/validate.py
     See CONTRIBUTING.md. -->

# Telehealth Visit Operations

Write the operations checklist for a telehealth visit: identity, consent, backup, and privacy.

## When to use this skill

Use this skill when the user:

- telehealth operations
- virtual visit checklist
- video visit SOP
- remote clinic visit

## When not to use this skill

- The user wants a different domain's specialist skill.
- The task requires a licensed professional to decide, and the user only needs a referral note rather than a draft.
- The request asks you to deceive, evade a control, or hide material facts.

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

- Their identity check
- Consent practice
- Backup if video fails
- Privacy expectations

## Workflow


### 1. Step 1

Confirm identity the way they already require. Do not invent a legal standard.
### 2. Step 2

State where consent is recorded if they said it is required.
### 3. Step 3

Give the patient a backup path when video fails.
### 4. Step 4

Remind staff about who else is in the room and what the camera shows.
### 5. Step 5

Do not provide clinical advice for the visit content.
### 6. Step 6

Escalate emergencies to their emergency instruction, which should be to local emergency services when they say that.

## Output

Deliver a **telehealth operations checklist**.

- Purpose of this telehealth operations checklist, in two sentences.
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

Dr. Helen Cho, clinic director at Cedar Clinic in Red Deer, needs a telehealth operations checklist by 30 September 2026. A checklist has no plan for a dropped call and tells staff to improvise medical advice.

### Example data

```text
From: Dr. Helen Cho, clinic director
Organization: Cedar Clinic, Red Deer
Date: 14 September 2026
Needed by: 30 September 2026

A checklist has no plan for a dropped call and tells staff to improvise medical advice.

Their identity check: Thursday clinic, last reviewed 14 September 2026. No owner named since
Consent practice: Thursday clinic. Partly documented: the what is written down, the who is not
Backup if video fails: Tuesday clinic, last reviewed 14 September 2026. No owner named since
Privacy expectations: email and billing address. They said no health data
```

### Example outcome

**Telehealth operations checklist**
Cedar Clinic · 14 September 2026 · Due 30 September 2026

**Decision**
Clinical content belongs to the clinician.

**Checklist**

- [x] **Their identity check** — Thursday clinic, last reviewed 14 September 2026. No owner named since  
      Evidenced in the file
- [x] **Consent practice** — Thursday clinic. Partly documented: the what is written down, the who is not  
      Evidenced in the file
- [x] **Backup if video fails** — Tuesday clinic, last reviewed 14 September 2026. No owner named since  
      Evidenced in the file
- [ ] **Privacy expectations** — email and billing address. They said no health data  
      Open — nothing in the file closes this

**The gates this list enforces, in order**

1. Confirm identity the way they already require. Do not invent a legal standard
2. State where consent is recorded if they said it is required
3. Give the patient a backup path when video fails
4. Remind staff about who else is in the room and what the camera shows
5. Do not provide clinical advice for the visit content

**Deliberately not done**
- Clinical advice in the ops checklist.
- No backup path.
- A camera angle that exposes a waiting room.

**Stop rule**
Do not mark this pack complete while a box above is open. An open box is a finding, not a formality — it is the thing this checklist exists to catch.

Next: Dr. Helen Cho closes the open items before 30 September 2026.

## Anti-patterns

- Clinical advice in the ops checklist
- No backup path
- A camera angle that exposes a waiting room

## Related skills

- `patient-intake-sop`
- `patient-communication`
