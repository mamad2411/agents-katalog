---
name: staff-credentialing
description: "Checklist a credentialing file for missing documents and expirations, without declaring someone privileged. Use when the user mentions credentialing, provider file, license expiration, privileging checklist, or asks for a credentialing checklist. Healthcare practice operations skill by Yasir Jilani."
license: MIT
compatibility: Agent Skills standard. No network access, extra packages, or credentials required.
metadata:
  author: Yasir Jilani
  version: "1.0.0"
  domain: healthcare
---

<!-- GENERATED FILE - edits here are overwritten by scripts/generate.py.
     Edit the 'staff-credentialing' entry in source/, then run:
       python3 scripts/generate.py && python3 scripts/validate.py
     See CONTRIBUTING.md. -->

# Credentialing File Checklist

Checklist a credentialing file for missing documents and expirations, without declaring someone privileged.

## When to use this skill

Use this skill when the user:

- credentialing
- provider file
- license expiration
- privileging checklist

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

- The required documents they listed
- Expiry dates they have
- The reviewer
- Known gaps

## Workflow


### 1. Step 1

Compare the file to their required list.
### 2. Step 2

Flag expired or missing items. Do not guess an expiry.
### 3. Step 3

A complete file is not a privileging decision. Say who must decide.
### 4. Step 4

Track a reappointment date.
### 5. Step 5

Do not fabricate a license number or a verification result.
### 6. Step 6

Escalate a lapse that their policy says stops scheduling.

## Output

Deliver a **credentialing checklist**.

- Purpose of this credentialing checklist, in two sentences.
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

Dr. Helen Cho, clinic director at Cedar Clinic in Red Deer, needs a credentialing checklist by 30 September 2026. A file is missing a current license and the team wants to assume it renewed.

### Example data

```text
From: Dr. Helen Cho, clinic director
Organization: Cedar Clinic, Red Deer
Date: 14 September 2026
Needed by: 30 September 2026

A file is missing a current license and the team wants to assume it renewed.

The required documents they listed: one PDF, 2 pages, dated 14 September 2026
Expiry dates they have: 30 September 2026
The reviewer: Dr. Helen Cho. No second reviewer named
Known gaps: Tuesday clinic is missing a source
```

### Example outcome

**Credentialing checklist**
Cedar Clinic · 14 September 2026 · Due 30 September 2026

**Decision**
Marks the license unverified and blocks any assumption of renewal.

**Checklist**

- [x] **The required documents they listed** — one PDF, 2 pages, dated 14 September 2026  
      Evidenced in the file
- [x] **Expiry dates they have** — 30 September 2026  
      Evidenced in the file
- [x] **The reviewer** — Dr. Helen Cho. No second reviewer named  
      Evidenced in the file
- [ ] **Known gaps** — Tuesday clinic is missing a source  
      Open — nothing in the file closes this

**The gates this list enforces, in order**

1. Compare the file to their required list
2. Flag expired or missing items. Do not guess an expiry
3. A complete file is not a privileging decision. Say who must decide
4. Track a reappointment date
5. Do not fabricate a license number or a verification result

**Deliberately not done**
- A homemade privileging decision.
- Fabricated license data.
- A lapse left off the schedule note.

**Stop rule**
Do not mark this pack complete while a box above is open. An open box is a finding, not a formality — it is the thing this checklist exists to catch.

Next: Dr. Helen Cho closes the open items before 30 September 2026.

## Anti-patterns

- A homemade privileging decision
- Fabricated license data
- A lapse left off the schedule note

## Related skills

- `clinic-schedule-design`
- `compliance-calendar`
