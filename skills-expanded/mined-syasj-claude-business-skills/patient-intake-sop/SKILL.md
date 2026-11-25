---
name: patient-intake-sop
description: "Write an intake procedure that collects only what the visit needs and tells staff when to stop and ask a clinician. Use when the user mentions patient intake, front desk procedure, registration SOP, intake checklist, or asks for a intake procedure. Healthcare practice operations skill by Yasir Jilani."
license: MIT
compatibility: Agent Skills standard. No network access, extra packages, or credentials required.
metadata:
  author: Yasir Jilani
  version: "1.0.0"
  domain: healthcare
---

<!-- GENERATED FILE - edits here are overwritten by scripts/generate.py.
     Edit the 'patient-intake-sop' entry in source/, then run:
       python3 scripts/generate.py && python3 scripts/validate.py
     See CONTRIBUTING.md. -->

# Patient Intake SOP

Write an intake procedure that collects only what the visit needs and tells staff when to stop and ask a clinician.

## When to use this skill

Use this skill when the user:

- patient intake
- front desk procedure
- registration SOP
- intake checklist

## When not to use this skill

- Diagnosis
- Drug doses

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

- The visit types
- Data they truly need
- Their privacy rules
- Escalation to a clinician

## Workflow


### 1. Step 1

List data elements required for registration and billing they described. Cut the rest.
### 2. Step 2

Write the script for missing information without pressuring a patient in distress.
### 3. Step 3

Tell staff which answers must go to a clinician rather than be interpreted at the desk.
### 4. Step 4

Include identity-check steps they already use. Do not invent a legal ID rule.
### 5. Step 5

Protect the conversation from the waiting room when the topic is sensitive.
### 6. Step 6

No passwords, no treatment advice, no doses.

## Output

Deliver a **intake procedure**.

- Purpose of this intake procedure, in two sentences.
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

Dr. Helen Cho, clinic director at Cedar Clinic in Red Deer, needs an intake procedure by 30 September 2026. An intake script asks the front desk to decide if chest pain can wait.

### Example data

```text
From: Dr. Helen Cho, clinic director
Organization: Cedar Clinic, Red Deer
Date: 14 September 2026
Needed by: 30 September 2026

An intake script asks the front desk to decide if chest pain can wait.

The visit types: Tuesday clinic, recorded 14 September 2026. No supporting file attached
Data they truly need: Tuesday clinic. Partly documented: the what is written down, the who is not
Their privacy rules: email and billing address. They said no health data
Escalation to a clinician: Tuesday clinic, first seen 14 September 2026. No root cause recorded yet
```

### Example outcome

**Intake procedure**
To: Dr. Helen Cho, clinic director, Cedar Clinic
Date: 14 September 2026 · Needed by: 30 September 2026

**Decision**
Stops and escalates urgent symptoms to a clinician instead of scoring them at the desk.

**What the file supports**

| Input | Value | Status |
| --- | --- | --- |
| The visit types | Tuesday clinic, recorded 14 September 2026. No supporting file attached | Needs confirmation |
| Data they truly need | Tuesday clinic. Partly documented: the what is written down, the who is not | Carried into the draft |
| Their privacy rules | email and billing address. They said no health data | Carried into the draft |
| Escalation to a clinician | Tuesday clinic, first seen 14 September 2026. No root cause recorded yet | Needs confirmation |

**How this draft was built**

**1. List data elements required for registration and billing they described. Cut the rest**

**2. Write the script for missing information without pressuring a patient in distress**

**3. Tell staff which answers must go to a clinician rather than be interpreted at the desk**

**4. Include identity-check steps they already use. Do not invent a legal ID rule**

**5. Protect the conversation from the waiting room when the topic is sensitive**

**Deliberately not done**
- Desk staff giving treatment advice.
- Collecting data with no purpose.
- A public conversation about a sensitive issue.

**Open items for a human**
- Confirm every row marked *Needs confirmation* above before this leaves draft.
- Anything absent from the file stayed absent. No figure, date, or name was supplied from outside it.

Next: Dr. Helen Cho by 30 September 2026. This is a draft, not a sign-off.

## Anti-patterns

- Desk staff giving treatment advice
- Collecting data with no purpose
- A public conversation about a sensitive issue

## Related skills

- `hipaa-privacy-ops`
- `patient-communication`
