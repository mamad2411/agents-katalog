---
name: patient-experience-clinic
description: "Review a clinic experience problem using waits, communication, and respect, without blaming the patient. Use when the user mentions patient experience, clinic complaint, waiting room experience, visit experience, or asks for a clinic experience review. Healthcare practice operations skill by Yasir Jilani."
license: MIT
compatibility: Agent Skills standard. No network access, extra packages, or credentials required.
metadata:
  author: Yasir Jilani
  version: "1.0.0"
  domain: healthcare
---

<!-- GENERATED FILE - edits here are overwritten by scripts/generate.py.
     Edit the 'patient-experience-clinic' entry in source/, then run:
       python3 scripts/generate.py && python3 scripts/validate.py
     See CONTRIBUTING.md. -->

# Clinic Experience Review

Review a clinic experience problem using waits, communication, and respect, without blaming the patient.

## When to use this skill

Use this skill when the user:

- patient experience
- clinic complaint
- waiting room experience
- visit experience

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

- The complaint or observation
- Wait data if any
- What staff can change
- Privacy constraints

## Workflow


### 1. Describe the failed moment

wait, confusion, or disrespect.
### 2. Step 2

Use their wait data or mark it unknown.
### 3. Step 3

Separate a capacity problem from a courtesy problem.
### 4. Step 4

Recommend one change staff can make this month.
### 5. Step 5

Do not identify a patient in a broader share-out.
### 6. Step 6

Clinical complaints go to the clinical lead, not to a scripted apology alone.

## Output

Deliver a **clinic experience review**.

- Purpose of this clinic experience review, in two sentences.
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

Dr. Helen Cho, clinic director at Cedar Clinic in Red Deer, needs a clinic experience review by 30 September 2026. Patients wait 70 minutes and the draft response tells staff to smile more.

### Example data

```text
From: Dr. Helen Cho, clinic director
Organization: Cedar Clinic, Red Deer
Date: 14 September 2026
Needed by: 30 September 2026

Patients wait 70 minutes and the draft response tells staff to smile more.

The complaint or observation: Tuesday clinic, first seen 14 September 2026. No root cause recorded yet
Wait data if any: Tuesday clinic. Stated in the ask, not documented anywhere else
What staff can change: two people on shift
Privacy constraints: no extra headcount, and no result that is not in this file
```

### Example outcome

**Clinic experience review**
To: Dr. Helen Cho, clinic director, Cedar Clinic
Date: 14 September 2026 · Needed by: 30 September 2026

**Decision**
Treats the wait as a capacity problem and limits the script to truthful status updates.

**What the file supports**

| Input | Value | Status |
| --- | --- | --- |
| The complaint or observation | Tuesday clinic, first seen 14 September 2026. No root cause recorded yet | Needs confirmation |
| Wait data if any | Tuesday clinic. Stated in the ask, not documented anywhere else | Carried into the draft |
| What staff can change | two people on shift | Carried into the draft |
| Privacy constraints | no extra headcount, and no result that is not in this file | Needs confirmation |

**How this draft was built**

**1. Describe the failed moment**  
wait, confusion, or disrespect.

**2. Use their wait data or mark it unknown**

**3. Separate a capacity problem from a courtesy problem**

**4. Recommend one change staff can make this month**

**5. Do not identify a patient in a broader share-out**

**Deliberately not done**
- Blaming the patient.
- Identifying a patient in a public note.
- A courtesy script for a capacity failure.

**Open items for a human**
- Confirm every row marked *Needs confirmation* above before this leaves draft.
- Anything absent from the file stayed absent. No figure, date, or name was supplied from outside it.

Next: Dr. Helen Cho by 30 September 2026. This is a draft, not a sign-off.

## Anti-patterns

- Blaming the patient
- Identifying a patient in a public note
- A courtesy script for a capacity failure

## Related skills

- `clinic-schedule-design`
- `complaint-root-cause`
