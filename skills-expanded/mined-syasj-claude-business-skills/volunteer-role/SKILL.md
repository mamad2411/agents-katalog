---
name: volunteer-role
description: "Write a volunteer role with the work, the time, and the supervision, without unpaid-staff exploitation hidden in cheerful language. Use when the user mentions volunteer role, volunteer description, unpaid role brief, volunteer handbook section, or asks for a volunteer role brief. Nonprofit and public interest skill by Yasir Jilani."
license: MIT
compatibility: Agent Skills standard. No network access, extra packages, or credentials required.
metadata:
  author: Yasir Jilani
  version: "1.0.0"
  domain: nonprofit
---

<!-- GENERATED FILE - edits here are overwritten by scripts/generate.py.
     Edit the 'volunteer-role' entry in source/, then run:
       python3 scripts/generate.py && python3 scripts/validate.py
     See CONTRIBUTING.md. -->

# Volunteer Role

Write a volunteer role with the work, the time, and the supervision, without unpaid-staff exploitation hidden in cheerful language.

## When to use this skill

Use this skill when the user:

- volunteer role
- volunteer description
- unpaid role brief
- volunteer handbook section

## When not to use this skill

- The user wants a different domain's specialist skill.
- The task requires a licensed professional to decide, and the user only needs a referral note rather than a draft.
- The request asks you to deceive, evade a control, or hide material facts.

## Professional boundary

Do not invent impact metrics or donor intent. Fundraising copy must be accurate and free of pressure tactics that misstate the need.

## Operating boundaries

- Use only information the user provides or files they explicitly ask you to read. Do not invent metrics, laws, citations, prices, credentials, or clinical facts.
- Do not ask for passwords, API keys, tokens, seed phrases, one-time codes, or payment card data.
- Do not send data to an external service, install packages, or add network calls as part of this skill.
- Separate facts, assumptions, and recommendations. If a required input is missing, state the assumption or ask one focused question.
- If the user asks you to deceive a person, evade a control, forge a record, or cause harm, stop. Offer a legitimate alternative.
- Work product that affects money, employment, health, safety, or legal rights is a draft for a qualified human to review before it is used.

## Inputs to collect

- The work
- Time expected
- Supervisor
- What volunteers will not do

## Workflow


### 1. Step 1

Describe the work and the time honestly.
### 2. Step 2

Name the supervisor.
### 3. State boundaries

what requires staff or a professional.
### 4. Step 4

Do not assign regulated duties to volunteers unless the user says their policy allows it, and even then flag review.
### 5. Step 5

Explain how to stop volunteering.
### 6. Step 6

Keep the tone respectful. Volunteers are not free employees to squeeze.

## Output

Deliver a **volunteer role brief**.

- Purpose of this volunteer role brief, in two sentences.
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

Amira Hassan, program director at Open Kitchen Society in Calgary, needs a volunteer role brief by 30 September 2026. A role asks volunteers to give clinical advice with no clinician present.

### Example data

```text
From: Amira Hassan, program director
Organization: Open Kitchen Society, Calgary
Date: 14 September 2026
Needed by: 30 September 2026

A role asks volunteers to give clinical advice with no clinician present.

The work: Literacy program; Grant report draft. Both unassigned as of 14 September 2026
Time expected: five working days, due 30 September 2026
Supervisor: Donor list segment B. Partly documented: the what is written down, the who is not
What volunteers will not do: Donor list segment B, last reviewed 14 September 2026. No owner named since
```

### Example outcome

**Volunteer role brief**
To: Amira Hassan, program director, Open Kitchen Society
Date: 14 September 2026 · Needed by: 30 September 2026

**Decision**
Removes the clinical duty and names a supervisor for the remaining work.

**What the file supports**

| Input | Value | Status |
| --- | --- | --- |
| The work | Literacy program; Grant report draft. Both unassigned as of 14 September 2026 | Needs confirmation |
| Time expected | five working days, due 30 September 2026 | Carried into the draft |
| Supervisor | Donor list segment B. Partly documented: the what is written down, the who is not | Carried into the draft |
| What volunteers will not do | Donor list segment B, last reviewed 14 September 2026. No owner named since | Needs confirmation |

**How this draft was built**

**1. Describe the work and the time honestly**

**2. Name the supervisor**

**3. State boundaries**  
what requires staff or a professional.

**4. Do not assign regulated duties to volunteers unless the user says their policy allows it, and even then flag review**

**5. Explain how to stop volunteering**

**Deliberately not done**
- Hidden time demands.
- Regulated work pushed to volunteers casually.
- No supervisor.

**Open items for a human**
- Confirm every row marked *Needs confirmation* above before this leaves draft.
- Anything absent from the file stayed absent. No figure, date, or name was supplied from outside it.

Next: Amira Hassan by 30 September 2026. This is a draft, not a sign-off.

## Anti-patterns

- Hidden time demands
- Regulated work pushed to volunteers casually
- No supervisor

## Related skills

- `job-description-writer`
- `patient-communication`
