---
name: care-team-huddle
description: "Plan a short care-team huddle around flow and safety flags, not a full case conference. Use when the user mentions huddle agenda, care team huddle, morning huddle, clinic huddle, or asks for a huddle agenda. Healthcare practice operations skill by Yasir Jilani."
license: MIT
compatibility: Agent Skills standard. No network access, extra packages, or credentials required.
metadata:
  author: Yasir Jilani
  version: "1.0.0"
  domain: healthcare
---

<!-- GENERATED FILE - edits here are overwritten by scripts/generate.py.
     Edit the 'care-team-huddle' entry in source/, then run:
       python3 scripts/generate.py && python3 scripts/validate.py
     See CONTRIBUTING.md. -->

# Care Team Huddle

Plan a short care-team huddle around flow and safety flags, not a full case conference.

## When to use this skill

Use this skill when the user:

- huddle agenda
- care team huddle
- morning huddle
- clinic huddle

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

- Today's schedule issues
- Safety flags they already use
- Staffing gaps
- The time box

## Workflow


### 1. Step 1

Limit the huddle to the time box.
### 2. List schedule risks

missing results they already know about, interpreter needs, and staffing gaps.
### 3. Step 3

Safety flags are read from their list. Do not invent clinical risk.
### 4. Step 4

Assign one owner for each flow problem.
### 5. Step 5

Park teaching and long cases for another forum.
### 6. Step 6

End with who will tell the front desk.

## Output

Deliver a **huddle agenda**.

- Purpose of this huddle agenda, in two sentences.
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

Dr. Helen Cho, clinic director at Cedar Clinic in Red Deer, needs a huddle agenda by 30 September 2026. A 10-minute huddle is packed with three teaching topics and no staffing note.

### Example data

```text
From: Dr. Helen Cho, clinic director
Organization: Cedar Clinic, Red Deer
Date: 14 September 2026
Needed by: 30 September 2026

A 10-minute huddle is packed with three teaching topics and no staffing note.

Today's schedule issues: Referral desk and one other, both unconfirmed as of 14 September 2026
Safety flags they already use: Referral desk. Partly documented: the what is written down, the who is not
Staffing gaps: Tuesday clinic is missing a source
The time box: five working days, due 30 September 2026
```

### Example outcome

**Huddle agenda**
To: Dr. Helen Cho, clinic director, Cedar Clinic
Date: 14 September 2026 · Needed by: 30 September 2026

**Decision**
Keeps the staffing gap, drops the teaching, and names the front-desk owner.

**What the file supports**

| Input | Value | Status |
| --- | --- | --- |
| Today's schedule issues | Referral desk and one other, both unconfirmed as of 14 September 2026 | Needs confirmation |
| Safety flags they already use | Referral desk. Partly documented: the what is written down, the who is not | Carried into the draft |
| Staffing gaps | Tuesday clinic is missing a source | Carried into the draft |
| The time box | five working days, due 30 September 2026 | Needs confirmation |

**How this draft was built**

**1. Limit the huddle to the time box**

**2. List schedule risks**  
missing results they already know about, interpreter needs, and staffing gaps.

**3. Safety flags are read from their list. Do not invent clinical risk**

**4. Assign one owner for each flow problem**

**5. Park teaching and long cases for another forum**

**Deliberately not done**
- A huddle that becomes a meeting.
- Invented clinical risks.
- No owner for a flow problem.

**Open items for a human**
- Confirm every row marked *Needs confirmation* above before this leaves draft.
- Anything absent from the file stayed absent. No figure, date, or name was supplied from outside it.

Next: Dr. Helen Cho by 30 September 2026. This is a draft, not a sign-off.

## Anti-patterns

- A huddle that becomes a meeting
- Invented clinical risks
- No owner for a flow problem

## Related skills

- `clinic-schedule-design`
- `shift-handover`
