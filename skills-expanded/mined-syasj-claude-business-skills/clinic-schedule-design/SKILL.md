---
name: clinic-schedule-design
description: "Design a clinic schedule around visit types and staffing, without pretending to triage medical urgency. Use when the user mentions clinic schedule, appointment template, provider schedule, clinic capacity, or asks for a clinic schedule. Healthcare practice operations skill by Yasir Jilani."
license: MIT
compatibility: Agent Skills standard. No network access, extra packages, or credentials required.
metadata:
  author: Yasir Jilani
  version: "1.0.0"
  domain: healthcare
---

<!-- GENERATED FILE - edits here are overwritten by scripts/generate.py.
     Edit the 'clinic-schedule-design' entry in source/, then run:
       python3 scripts/generate.py && python3 scripts/validate.py
     See CONTRIBUTING.md. -->

# Clinic Schedule Design

Design a clinic schedule around visit types and staffing, without pretending to triage medical urgency.

## When to use this skill

Use this skill when the user:

- clinic schedule
- appointment template
- provider schedule
- clinic capacity

## When not to use this skill

- Medical diagnosis
- Treatment protocols

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

- Visit types and lengths they use
- Provider availability
- Room limits
- No-show experience they shared

## Workflow


### 1. Step 1

Separate visit types they already use. Do not invent clinical priorities.
### 2. Step 2

Fit the template to rooms and staffing they named.
### 3. Step 3

Hold a small portion for same-day access only if they asked for that operational goal.
### 4. Step 4

Show what happens on a provider absence.
### 5. Step 5

Do not promise a wait time the template cannot support.
### 6. Step 6

This is scheduling, not triage. Medical urgency belongs to a licensed clinician.

## Output

Deliver a **clinic schedule**.

- Purpose of this clinic schedule, in two sentences.
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

Dr. Helen Cho, clinic director at Cedar Clinic in Red Deer, needs a clinic schedule by 30 September 2026. A manager wants to double-book every slot because the wait list is long.

### Example data

```text
From: Dr. Helen Cho, clinic director
Organization: Cedar Clinic, Red Deer
Date: 14 September 2026
Needed by: 30 September 2026

A manager wants to double-book every slot because the wait list is long.

Visit types and lengths they use: plain, for people who already know the context. No house guide attached
Provider availability: Tuesday clinic. Partly documented: the what is written down, the who is not
Room limits: Referral desk. Partly documented: the what is written down, the who is not
No-show experience they shared: Thursday clinic, last reviewed 14 September 2026. No owner named since
```

### Example outcome

**Clinic schedule**
To: Dr. Helen Cho, clinic director, Cedar Clinic
Date: 14 September 2026 · Needed by: 30 September 2026

**Decision**
Shows the double-book harm and offers an access hold only within real room capacity.

**What the file supports**

| Input | Value | Status |
| --- | --- | --- |
| Visit types and lengths they use | plain, for people who already know the context. No house guide attached | Needs confirmation |
| Provider availability | Tuesday clinic. Partly documented: the what is written down, the who is not | Carried into the draft |
| Room limits | Referral desk. Partly documented: the what is written down, the who is not | Carried into the draft |
| No-show experience they shared | Thursday clinic, last reviewed 14 September 2026. No owner named since | Needs confirmation |

**How this draft was built**

**1. Separate visit types they already use. Do not invent clinical priorities**

**2. Fit the template to rooms and staffing they named**

**3. Hold a small portion for same-day access only if they asked for that operational goal**

**4. Show what happens on a provider absence**

**5. Do not promise a wait time the template cannot support**

**Deliberately not done**
- Clinical triage disguised as a template.
- A template that ignores rooms.
- A promised wait they cannot meet.

**Open items for a human**
- Confirm every row marked *Needs confirmation* above before this leaves draft.
- Anything absent from the file stayed absent. No figure, date, or name was supplied from outside it.

Next: Dr. Helen Cho by 30 September 2026. This is a draft, not a sign-off.

## Anti-patterns

- Clinical triage disguised as a template
- A template that ignores rooms
- A promised wait they cannot meet

## Related skills

- `patient-experience-clinic`
- `capacity-plan`
