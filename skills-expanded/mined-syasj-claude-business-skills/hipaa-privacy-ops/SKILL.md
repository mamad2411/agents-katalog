---
name: hipaa-privacy-ops
description: "Review a clinic privacy practice for minimum necessary access and a real incident path. Not a legal opinion. Use when the user mentions HIPAA operations, clinic privacy, minimum necessary, privacy incident clinic, or asks for a privacy operations checklist. Healthcare practice operations skill by Yasir Jilani."
license: MIT
compatibility: Agent Skills standard. No network access, extra packages, or credentials required.
metadata:
  author: Yasir Jilani
  version: "1.0.0"
  domain: healthcare
---

<!-- GENERATED FILE - edits here are overwritten by scripts/generate.py.
     Edit the 'hipaa-privacy-ops' entry in source/, then run:
       python3 scripts/generate.py && python3 scripts/validate.py
     See CONTRIBUTING.md. -->

# Privacy Operations for a Clinic

Review a clinic privacy practice for minimum necessary access and a real incident path. Not a legal opinion.

## When to use this skill

Use this skill when the user:

- HIPAA operations
- clinic privacy
- minimum necessary
- privacy incident clinic

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

- Who can open a chart
- The reason they need it
- How incidents are reported
- Known gaps

## Workflow


### 1. Step 1

Compare access to the job. Curiosity access is a finding.
### 2. Step 2

Check that conversations, screens, and printouts match their privacy rule.
### 3. Step 3

Write the incident path they have, or say it is missing.
### 4. Step 4

Do not declare HIPAA compliance. Send legal questions to counsel.
### 5. Step 5

Minimize identifiers in examples and tickets.
### 6. Step 6

Refuse any request to snoop in a chart for a non-care reason.

## Output

Deliver a **privacy operations checklist**.

- Purpose of this privacy operations checklist, in two sentences.
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

Dr. Helen Cho, clinic director at Cedar Clinic in Red Deer, needs a privacy operations checklist by 30 September 2026. A scheduler wants standing access to full clinical notes 'just in case'.

### Example data

```text
From: Dr. Helen Cho, clinic director
Organization: Cedar Clinic, Red Deer
Date: 14 September 2026
Needed by: 30 September 2026

A scheduler wants standing access to full clinical notes 'just in case'.

Who can open a chart: Dr. Helen Cho, clinic director
The reason they need it: Tuesday clinic, recorded 14 September 2026. No supporting file attached
How incidents are reported: one file, dated 14 September 2026. No earlier version attached for comparison
Known gaps: Tuesday clinic is missing a source
```

### Example outcome

**Privacy operations checklist**
Cedar Clinic · 14 September 2026 · Due 30 September 2026

**Decision**
Limits access to the scheduling need and refuses a compliance badge.

**Checklist**

- [x] **Who can open a chart** — Dr. Helen Cho, clinic director  
      Evidenced in the file
- [x] **The reason they need it** — Tuesday clinic, recorded 14 September 2026. No supporting file attached  
      Evidenced in the file
- [x] **How incidents are reported** — one file, dated 14 September 2026. No earlier version attached for comparison  
      Evidenced in the file
- [ ] **Known gaps** — Tuesday clinic is missing a source  
      Open — nothing in the file closes this

**The gates this list enforces, in order**

1. Compare access to the job. Curiosity access is a finding
2. Check that conversations, screens, and printouts match their privacy rule
3. Write the incident path they have, or say it is missing
4. Do not declare HIPAA compliance. Send legal questions to counsel
5. Minimize identifiers in examples and tickets

**Deliberately not done**
- A compliance badge.
- Snooping instructions.
- Identifiers in a training example.

**Stop rule**
Do not mark this pack complete while a box above is open. An open box is a finding, not a formality — it is the thing this checklist exists to catch.

Next: Dr. Helen Cho closes the open items before 30 September 2026.

## Anti-patterns

- A compliance badge
- Snooping instructions
- Identifiers in a training example

## Related skills

- `privacy-by-design`
- `patient-communication`
