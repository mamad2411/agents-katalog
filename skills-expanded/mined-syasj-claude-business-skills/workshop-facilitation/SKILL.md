---
name: workshop-facilitation
description: "Plan a workshop that produces a shared artifact, with timing and a way to hear quiet people. Use when the user mentions facilitate a workshop, workshop plan, training facilitation, working session, or asks for a workshop plan. Education and training skill by Yasir Jilani."
license: MIT
compatibility: Agent Skills standard. No network access, extra packages, or credentials required.
metadata:
  author: Yasir Jilani
  version: "1.0.0"
  domain: education
---

<!-- GENERATED FILE - edits here are overwritten by scripts/generate.py.
     Edit the 'workshop-facilitation' entry in source/, then run:
       python3 scripts/generate.py && python3 scripts/validate.py
     See CONTRIBUTING.md. -->

# Workshop Facilitation

Plan a workshop that produces a shared artifact, with timing and a way to hear quiet people.

## When to use this skill

Use this skill when the user:

- facilitate a workshop
- workshop plan
- training facilitation
- working session

## When not to use this skill

- The user wants a different domain's specialist skill.
- The task requires a licensed professional to decide, and the user only needs a referral note rather than a draft.
- The request asks you to deceive, evade a control, or hide material facts.

## Professional boundary

Learning design supports the instructor. Do not complete graded work for a student or help anyone cheat. Do not invent accreditation requirements.

## Operating boundaries

- Use only information the user provides or files they explicitly ask you to read. Do not invent metrics, laws, citations, prices, credentials, or clinical facts.
- Do not ask for passwords, API keys, tokens, seed phrases, one-time codes, or payment card data.
- Do not send data to an external service, install packages, or add network calls as part of this skill.
- Separate facts, assumptions, and recommendations. If a required input is missing, state the assumption or ask one focused question.
- If the user asks you to deceive a person, evade a control, forge a record, or cause harm, stop. Offer a legitimate alternative.
- Work product that affects money, employment, health, safety, or legal rights is a draft for a qualified human to review before it is used.

## Inputs to collect

- The artifact the room must leave with
- Participants
- Time
- Sensitive topics

## Workflow


### 1. Define the artifact

a decision, a list, or a draft.
### 2. Step 2

Design activities that create the artifact, not icebreakers that consume the hour.
### 3. Step 3

Timebox. Leave a close that assigns owners.
### 4. Step 4

Plan a way for quiet people to contribute without putting anyone on the spot in a harmful way.
### 5. Step 5

Handle disagreement as a recorded option, not as a forced consensus.
### 6. Step 6

Do not run a workshop that pretends people consented to a decision they did not make.

## Output

Deliver a **workshop plan**.

- Purpose of this workshop plan, in two sentences.
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

Mark Ellison, program chair at Riverbend College in Lethbridge, needs a workshop plan by 30 September 2026. A two-hour workshop has no decision and six get-to-know-you games.

### Example data

```text
From: Mark Ellison, program chair
Organization: Riverbend College, Lethbridge
Date: 14 September 2026
Needed by: 30 September 2026

A two-hour workshop has no decision and six get-to-know-you games.

The artifact the room must leave with: Module 2 lesson plan, recorded 14 September 2026. No supporting file attached
Participants: Mark Ellison plus two others named in the thread. No distribution list attached
Time: five working days, due 30 September 2026
Sensitive topics: email and billing address only. They stated no health or payment data
```

### Example outcome

**Workshop plan**
To: Mark Ellison, program chair, Riverbend College
Date: 14 September 2026 · Needed by: 30 September 2026

**Decision**
A plan aimed at one recorded decision, with a dissent line and owners.

**What the file supports**

| Input | Value | Status |
| --- | --- | --- |
| The artifact the room must leave with | Module 2 lesson plan, recorded 14 September 2026. No supporting file attached | Needs confirmation |
| Participants | Mark Ellison plus two others named in the thread. No distribution list attached | Carried into the draft |
| Time | five working days, due 30 September 2026 | Carried into the draft |
| Sensitive topics | email and billing address only. They stated no health or payment data | Needs confirmation |

**How this draft was built**

**1. Define the artifact**  
a decision, a list, or a draft.

**2. Design activities that create the artifact, not icebreakers that consume the hour**

**3. Timebox. Leave a close that assigns owners**

**4. Plan a way for quiet people to contribute without putting anyone on the spot in a harmful way**

**5. Handle disagreement as a recorded option, not as a forced consensus**

**Deliberately not done**
- No artifact.
- Fake consensus.
- An agenda of icebreakers.

**Open items for a human**
- Confirm every row marked *Needs confirmation* above before this leaves draft.
- Anything absent from the file stayed absent. No figure, date, or name was supplied from outside it.

Next: Mark Ellison by 30 September 2026. This is a draft, not a sign-off.

## Anti-patterns

- No artifact
- Fake consensus
- An agenda of icebreakers

## Related skills

- `executive-offsite-design`
- `lesson-plan`
