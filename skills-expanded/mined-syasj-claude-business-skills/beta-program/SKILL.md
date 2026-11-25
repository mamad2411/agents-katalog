---
name: beta-program
description: "Design a beta that learns a specific risk, with participant criteria and an exit. Use when the user mentions beta program, design partners, early access, pilot program, or asks for a beta plan. Product skill by Yasir Jilani."
license: MIT
compatibility: Agent Skills standard. No network access, extra packages, or credentials required.
metadata:
  author: Yasir Jilani
  version: "1.0.0"
  domain: product
---

<!-- GENERATED FILE - edits here are overwritten by scripts/generate.py.
     Edit the 'beta-program' entry in source/, then run:
       python3 scripts/generate.py && python3 scripts/validate.py
     See CONTRIBUTING.md. -->

# Beta Program

Design a beta that learns a specific risk, with participant criteria and an exit.

## When to use this skill

Use this skill when the user:

- beta program
- design partners
- early access
- pilot program

## When not to use this skill

- The user wants a different domain's specialist skill.
- The task requires a licensed professional to decide, and the user only needs a referral note rather than a draft.
- The request asks you to deceive, evade a control, or hide material facts.

## Professional boundary

Product recommendations are hypotheses until evidence says otherwise. Label confidence. Do not ship dark patterns that hide cost or consent.

## Operating boundaries

- Use only information the user provides or files they explicitly ask you to read. Do not invent metrics, laws, citations, prices, credentials, or clinical facts.
- Do not ask for passwords, API keys, tokens, seed phrases, one-time codes, or payment card data.
- Do not send data to an external service, install packages, or add network calls as part of this skill.
- Separate facts, assumptions, and recommendations. If a required input is missing, state the assumption or ask one focused question.
- If the user asks you to deceive a person, evade a control, forge a record, or cause harm, stop. Offer a legitimate alternative.
- Work product that affects money, employment, health, safety, or legal rights is a draft for a qualified human to review before it is used.

## Inputs to collect

- The risk the beta must retire
- Participant criteria
- Support capacity
- Exit criteria

## Workflow


### 1. Learning goal

The question the beta answers. A beta with no question is a soft launch.
### 2. Participants

Who is in and who is out. Do not recruit people who cannot hit the risk you care about.
### 3. Expectations

What beta users are promised, including roughness. No implied production SLA unless the user is offering one.
### 4. Feedback path

How issues arrive, and who triages them.
### 5. Exit

The evidence that ends the beta, successfully or not.
### 6. Reference use

Do not turn a beta quote into a public claim without approval.

## Output

Deliver a **beta plan**.

- Purpose of this beta plan, in two sentences.
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

Jonah Park, product manager at Fieldnote in Edmonton, needs a beta plan by 30 September 2026. Sales wants to call twenty unpaid pilots a beta and quote them on the website.

### Example data

```text
From: Jonah Park, product manager
Organization: Fieldnote, Edmonton
Date: 14 September 2026
Needed by: 30 September 2026

Sales wants to call twenty unpaid pilots a beta and quote them on the website.

The risk the beta must retire: Activation checklist is open. No score in the file
Participant criteria: Jonah Park plus two others named in the thread. No distribution list attached
Support capacity: two people, no overtime figure
Exit criteria: their existing list, 6 lines. Two lines have no owner
```

### Example outcome

**Beta plan**
To: Jonah Park, product manager, Fieldnote
Date: 14 September 2026 · Needed by: 30 September 2026

**Decision**
A plan with a learning goal, a cap matched to support capacity, and a ban on public quotes without approval.

**What the file supports**

| Input | Value | Status |
| --- | --- | --- |
| The risk the beta must retire | Activation checklist is open. No score in the file | Needs confirmation |
| Participant criteria | Jonah Park plus two others named in the thread. No distribution list attached | Carried into the draft |
| Support capacity | two people, no overtime figure | Carried into the draft |
| Exit criteria | their existing list, 6 lines. Two lines have no owner | Needs confirmation |

**How this draft was built**

**1. Learning goal**  
The question the beta answers. A beta with no question is a soft launch.

**2. Participants**  
Who is in and who is out. Do not recruit people who cannot hit the risk you care about.

**3. Expectations**  
What beta users are promised, including roughness. No implied production SLA unless the user is offering one.

**4. Feedback path**  
How issues arrive, and who triages them.

**5. Exit**  
The evidence that ends the beta, successfully or not.

**Deliberately not done**
- A beta that is an unlimited free launch.
- No exit criteria.
- Public claims from an unhappy pilot.

**Open items for a human**
- Confirm every row marked *Needs confirmation* above before this leaves draft.
- Anything absent from the file stayed absent. No figure, date, or name was supplied from outside it.

Next: Jonah Park by 30 September 2026. This is a draft, not a sign-off.

## Anti-patterns

- A beta that is an unlimited free launch.
- No exit criteria.
- Public claims from an unhappy pilot.

## Related skills

- `customer-story`
- `launch-readiness`
