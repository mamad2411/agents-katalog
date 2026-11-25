---
name: control-design
description: "Design a control that prevents or detects a named failure, and specify the evidence it leaves. Use when the user mentions design a control, control activity, preventive control, detective control, or asks for a control design. Risk and compliance skill by Yasir Jilani."
license: MIT
compatibility: Agent Skills standard. No network access, extra packages, or credentials required.
metadata:
  author: Yasir Jilani
  version: "1.0.0"
  domain: risk
---

<!-- GENERATED FILE - edits here are overwritten by scripts/generate.py.
     Edit the 'control-design' entry in source/, then run:
       python3 scripts/generate.py && python3 scripts/validate.py
     See CONTRIBUTING.md. -->

# Control Design

Design a control that prevents or detects a named failure, and specify the evidence it leaves.

## When to use this skill

Use this skill when the user:

- design a control
- control activity
- preventive control
- detective control

## When not to use this skill

- The user wants a different domain's specialist skill.
- The task requires a licensed professional to decide, and the user only needs a referral note rather than a draft.
- The request asks you to deceive, evade a control, or hide material facts.

## Professional boundary

Risk work prioritizes uncertainty. It is not a certification. Do not claim SOC 2, ISO, HIPAA, or similar compliance unless the user has evidence of it.

## Operating boundaries

- Use only information the user provides or files they explicitly ask you to read. Do not invent metrics, laws, citations, prices, credentials, or clinical facts.
- Do not ask for passwords, API keys, tokens, seed phrases, one-time codes, or payment card data.
- Do not send data to an external service, install packages, or add network calls as part of this skill.
- Separate facts, assumptions, and recommendations. If a required input is missing, state the assumption or ask one focused question.
- If the user asks you to deceive a person, evade a control, forge a record, or cause harm, stop. Offer a legitimate alternative.
- Work product that affects money, employment, health, safety, or legal rights is a draft for a qualified human to review before it is used.

## Inputs to collect

- The failure to prevent
- How the work happens today
- Who can perform the control
- Evidence available

## Workflow


### 1. Step 1

State the failure in one sentence.
### 2. Step 2

Choose preventive or detective based on when the harm becomes irreversible.
### 3. Step 3

Assign a performer who is not the only person benefiting from a bypass, when they can staff that.
### 4. Specify the evidence

a review note, a system log, or a sign-off.
### 5. Step 5

Define the frequency.
### 6. Step 6

A control with no evidence is a hope. Say so.

## Output

Deliver a **control design**.

- Purpose of this control design, in two sentences.
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

Priya Shah, controller at Northline Studio in Calgary, needs a control design by 30 September 2026. The control is 'management reviews revenue' with no sample and no sign-off.

### Example data

```text
From: Priya Shah, controller
Organization: Northline Studio, Calgary
Date: 14 September 2026
Needed by: 30 September 2026

The control is 'management reviews revenue' with no sample and no sign-off.

The failure to prevent: Control 7.2 access review, first seen 14 September 2026. No root cause recorded yet
How the work happens today: Control 7.2 access review; Vendor Redline Parts. Both unassigned as of 14 September 2026
Who can perform the control: Priya Shah, controller
Evidence available: one PDF, 2 pages, dated 14 September 2026
```

### Example outcome

**Control design**
To: Priya Shah, controller, Northline Studio
Date: 14 September 2026 · Needed by: 30 September 2026

**Decision**
Names the sample, the reviewer, and the evidence left behind.

**What the file supports**

| Input | Value | Status |
| --- | --- | --- |
| The failure to prevent | Control 7.2 access review, first seen 14 September 2026. No root cause recorded yet | Needs confirmation |
| How the work happens today | Control 7.2 access review; Vendor Redline Parts. Both unassigned as of 14 September 2026 | Carried into the draft |
| Who can perform the control | Priya Shah, controller | Carried into the draft |
| Evidence available | one PDF, 2 pages, dated 14 September 2026 | Needs confirmation |

**How this draft was built**

**1. State the failure in one sentence**

**2. Choose preventive or detective based on when the harm becomes irreversible**

**3. Assign a performer who is not the only person benefiting from a bypass, when they can staff that**

**4. Specify the evidence**  
a review note, a system log, or a sign-off.

**5. Define the frequency**

**Deliberately not done**
- A control with no evidence.
- The beneficiary is the only reviewer.
- A policy sentence with no activity.

**Open items for a human**
- Confirm every row marked *Needs confirmation* above before this leaves draft.
- Anything absent from the file stayed absent. No figure, date, or name was supplied from outside it.

Next: Priya Shah by 30 September 2026. This is a draft, not a sign-off.

## Anti-patterns

- A control with no evidence
- The beneficiary is the only reviewer
- A policy sentence with no activity

## Related skills

- `internal-controls-walkthrough`
- `sox-walkthrough`
