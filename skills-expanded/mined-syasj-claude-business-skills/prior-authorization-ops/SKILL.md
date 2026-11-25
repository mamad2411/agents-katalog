---
name: prior-authorization-ops
description: "Organize a prior-authorization packet and clock from the payer rules the user supplied. Use when the user mentions prior authorization, payer authorization, auth packet, authorization checklist, or asks for a authorization operations checklist. Healthcare practice operations skill by Yasir Jilani."
license: MIT
compatibility: Agent Skills standard. No network access, extra packages, or credentials required.
metadata:
  author: Yasir Jilani
  version: "1.0.0"
  domain: healthcare
---

<!-- GENERATED FILE - edits here are overwritten by scripts/generate.py.
     Edit the 'prior-authorization-ops' entry in source/, then run:
       python3 scripts/generate.py && python3 scripts/validate.py
     See CONTRIBUTING.md. -->

# Prior Authorization Operations

Organize a prior-authorization packet and clock from the payer rules the user supplied.

## When to use this skill

Use this skill when the user:

- prior authorization
- payer authorization
- auth packet
- authorization checklist

## When not to use this skill

- Altering records
- Fraudulent billing

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

- The payer requirements they have
- The documents on hand
- The internal owner
- The requested date

## Workflow


### 1. Step 1

Use only requirements the user supplied. Do not invent payer rules.
### 2. Step 2

List missing documents as gaps, not as reasons to fabricate a note.
### 3. Step 3

Assign an owner and a follow-up clock.
### 4. Step 4

Tell the patient the status in plain language without promising approval.
### 5. Step 5

Refuse any request to alter a clinical record to win an authorization.
### 6. Step 6

Clinical criteria questions go to a clinician or the payer, not to a guessed answer.

## Output

Deliver a **authorization operations checklist**.

- Purpose of this authorization operations checklist, in two sentences.
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

Dr. Helen Cho, clinic director at Cedar Clinic in Red Deer, needs an authorization operations checklist by 30 September 2026. Staff want to change a note so the authorization is more likely to pass.

### Example data

```text
From: Dr. Helen Cho, clinic director
Organization: Cedar Clinic, Red Deer
Date: 14 September 2026
Needed by: 30 September 2026

Staff want to change a note so the authorization is more likely to pass.

The payer requirements they have: their one-page rule dated 2 Mar 2026. No exception log since
The documents on hand: one PDF, 2 pages, dated 14 September 2026
The internal owner: Dr. Helen Cho, clinic director
The requested date: 30 September 2026
```

### Example outcome

**Authorization operations checklist**
Cedar Clinic · 14 September 2026 · Due 30 September 2026

**Decision**
A checklist of real gaps and a refusal to alter the record.

**Checklist**

- [x] **The payer requirements they have** — their one-page rule dated 2 Mar 2026. No exception log since  
      Evidenced in the file
- [x] **The documents on hand** — one PDF, 2 pages, dated 14 September 2026  
      Evidenced in the file
- [x] **The internal owner** — Dr. Helen Cho, clinic director  
      Evidenced in the file
- [ ] **The requested date** — 30 September 2026  
      Open — nothing in the file closes this

**The gates this list enforces, in order**

1. Use only requirements the user supplied. Do not invent payer rules
2. List missing documents as gaps, not as reasons to fabricate a note
3. Assign an owner and a follow-up clock
4. Tell the patient the status in plain language without promising approval
5. Refuse any request to alter a clinical record to win an authorization

**Deliberately not done**
- Fabricated clinical notes.
- A promised approval.
- Invented payer rules.

**Stop rule**
Do not mark this pack complete while a box above is open. An open box is a finding, not a formality — it is the thing this checklist exists to catch.

Next: Dr. Helen Cho closes the open items before 30 September 2026.

## Anti-patterns

- Fabricated clinical notes
- A promised approval
- Invented payer rules

## Related skills

- `medical-billing-review`
- `clinical-documentation-quality`
