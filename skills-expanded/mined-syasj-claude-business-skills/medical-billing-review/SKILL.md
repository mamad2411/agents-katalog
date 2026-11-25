---
name: medical-billing-review
description: "Review a billing packet for missing elements and coding questions, without upcoding or inventing services. Use when the user mentions medical billing review, claim checklist, coding question operations, clean claim, or asks for a billing review checklist. Healthcare practice operations skill by Yasir Jilani."
license: MIT
compatibility: Agent Skills standard. No network access, extra packages, or credentials required.
metadata:
  author: Yasir Jilani
  version: "1.0.0"
  domain: healthcare
---

<!-- GENERATED FILE - edits here are overwritten by scripts/generate.py.
     Edit the 'medical-billing-review' entry in source/, then run:
       python3 scripts/generate.py && python3 scripts/validate.py
     See CONTRIBUTING.md. -->

# Medical Billing Review

Review a billing packet for missing elements and coding questions, without upcoding or inventing services.

## When to use this skill

Use this skill when the user:

- medical billing review
- claim checklist
- coding question operations
- clean claim

## When not to use this skill

- Upcoding
- False claims

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

- The services they say were provided
- The codes they are considering
- Payer edits they supplied
- The documentation present

## Workflow


### 1. Step 1

Match codes only to services they say were documented.
### 2. Step 2

List missing documentation. Do not suggest adding a service that did not happen.
### 3. Step 3

Use payer edits they pasted. Do not invent a payer rule.
### 4. Step 4

Flag questions for a certified coder. This skill is not a coder's final assignment.
### 5. Step 5

Separate a patient estimate from a coverage promise.
### 6. Step 6

Refuse upcoding, unbundling schemes, and false claims.

## Output

Deliver a **billing review checklist**.

- Purpose of this billing review checklist, in two sentences.
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

Dr. Helen Cho, clinic director at Cedar Clinic in Red Deer, needs a billing review checklist by 30 September 2026. A biller wants a higher code because the visit 'felt complex' though the note does not support it.

### Example data

```text
From: Dr. Helen Cho, clinic director
Organization: Cedar Clinic, Red Deer
Date: 14 September 2026
Needed by: 30 September 2026

A biller wants a higher code because the visit 'felt complex' though the note does not support it.

The services they say were provided: the one named in the ask. Version and owner not recorded
The codes they are considering: Tuesday clinic, recorded 14 September 2026. No supporting file attached
Payer edits they supplied: Tuesday clinic, last reviewed 14 September 2026. No owner named since
The documentation present: one PDF, 2 pages, dated 14 September 2026
```

### Example outcome

**Billing review checklist**
Cedar Clinic · 14 September 2026 · Due 30 September 2026

**Decision**
Keeps the supported code and sends the complexity question to a coder with the note gap visible.

**Checklist**

- [x] **The services they say were provided** — the one named in the ask. Version and owner not recorded  
      Evidenced in the file
- [x] **The codes they are considering** — Tuesday clinic, recorded 14 September 2026. No supporting file attached  
      Evidenced in the file
- [x] **Payer edits they supplied** — Tuesday clinic, last reviewed 14 September 2026. No owner named since  
      Evidenced in the file
- [ ] **The documentation present** — one PDF, 2 pages, dated 14 September 2026  
      Open — nothing in the file closes this

**The gates this list enforces, in order**

1. Match codes only to services they say were documented
2. List missing documentation. Do not suggest adding a service that did not happen
3. Use payer edits they pasted. Do not invent a payer rule
4. Flag questions for a certified coder. This skill is not a coder's final assignment
5. Separate a patient estimate from a coverage promise

**Deliberately not done**
- Upcoding.
- Invented services.
- A coverage promise.

**Stop rule**
Do not mark this pack complete while a box above is open. An open box is a finding, not a formality — it is the thing this checklist exists to catch.

Next: Dr. Helen Cho closes the open items before 30 September 2026.

## Anti-patterns

- Upcoding
- Invented services
- A coverage promise

## Related skills

- `clinical-documentation-quality`
- `prior-authorization-ops`
