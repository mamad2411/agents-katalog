---
name: incoming-inspection
description: "Plan incoming inspection for a material based on risk and the reaction to a failed lot. Use when the user mentions incoming inspection, receiving inspection, supplier quality check, incoming QC, or asks for a incoming inspection plan. Manufacturing and quality skill by Yasir Jilani."
license: MIT
compatibility: Agent Skills standard. No network access, extra packages, or credentials required.
metadata:
  author: Yasir Jilani
  version: "1.0.0"
  domain: manufacturing
---

<!-- GENERATED FILE - edits here are overwritten by scripts/generate.py.
     Edit the 'incoming-inspection' entry in source/, then run:
       python3 scripts/generate.py && python3 scripts/validate.py
     See CONTRIBUTING.md. -->

# Incoming Inspection

Plan incoming inspection for a material based on risk and the reaction to a failed lot.

## When to use this skill

Use this skill when the user:

- incoming inspection
- receiving inspection
- supplier quality check
- incoming QC

## When not to use this skill

- The user wants a different domain's specialist skill.
- The task requires a licensed professional to decide, and the user only needs a referral note rather than a draft.
- The request asks you to deceive, evade a control, or hide material facts.

## Professional boundary

Quality and safety procedures are drafts for the site's quality system. Do not bypass a hold, calibration, or safety step.

## Operating boundaries

- Use only information the user provides or files they explicitly ask you to read. Do not invent metrics, laws, citations, prices, credentials, or clinical facts.
- Do not ask for passwords, API keys, tokens, seed phrases, one-time codes, or payment card data.
- Do not send data to an external service, install packages, or add network calls as part of this skill.
- Separate facts, assumptions, and recommendations. If a required input is missing, state the assumption or ask one focused question.
- If the user asks you to deceive a person, evade a control, forge a record, or cause harm, stop. Offer a legitimate alternative.
- Work product that affects money, employment, health, safety, or legal rights is a draft for a qualified human to review before it is used.

## Inputs to collect

- The material risk
- The characteristics
- Sample practice they use
- Fail reaction

## Workflow


### 1. Step 1

Tie inspection to risk. Critical characteristics are not sampled away because the dock is busy, if their rule says so.
### 2. Step 2

Write the accept and fail reaction.
### 3. Step 3

Identify the hold location so failed material cannot be issued.
### 4. Step 4

Feed repeats to supplier quality.
### 5. Step 5

Do not skip a hold to keep a line running unless the user names a deviation owner.
### 6. Step 6

Record results in the system they use, not only on a scrap of paper.

## Output

Deliver a **incoming inspection plan**.

- Purpose of this incoming inspection plan, in two sentences.
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

Gus Moretti, plant manager at Redline Parts in Nisku, needs an incoming inspection plan by 30 September 2026. Failed material is left on the issue shelf so the line does not stop.

### Example data

```text
From: Gus Moretti, plant manager
Organization: Redline Parts, Nisku
Date: 14 September 2026
Needed by: 30 September 2026

Failed material is left on the issue shelf so the line does not stop.

The material risk: Line 2 is open. No score in the file
The characteristics: Line 2, recorded 14 September 2026. No supporting file attached
Sample practice they use: Gauge 7, recorded 14 September 2026. No supporting file attached
Fail reaction: Line 2; Lot 26-0914. Both unassigned as of 14 September 2026
```

### Example outcome

**Incoming inspection plan**
To: Gus Moretti, plant manager, Redline Parts
Date: 14 September 2026 · Needed by: 30 September 2026

**Decision**
Moves failed material to hold and requires a named deviation before any use.

**What the file supports**

| Input | Value | Status |
| --- | --- | --- |
| The material risk | Line 2 is open. No score in the file | Needs confirmation |
| The characteristics | Line 2, recorded 14 September 2026. No supporting file attached | Carried into the draft |
| Sample practice they use | Gauge 7, recorded 14 September 2026. No supporting file attached | Carried into the draft |
| Fail reaction | Line 2; Lot 26-0914. Both unassigned as of 14 September 2026 | Needs confirmation |

**How this draft was built**

**1. Tie inspection to risk. Critical characteristics are not sampled away because the dock is busy, if their rule says so**

**2. Write the accept and fail reaction**

**3. Identify the hold location so failed material cannot be issued**

**4. Feed repeats to supplier quality**

**5. Do not skip a hold to keep a line running unless the user names a deviation owner**

**Deliberately not done**
- A failed lot left in the issue location.
- Skipping a critical check for speed.
- No fail reaction.

**Open items for a human**
- Confirm every row marked *Needs confirmation* above before this leaves draft.
- Anything absent from the file stayed absent. No figure, date, or name was supplied from outside it.

Next: Gus Moretti by 30 September 2026. This is a draft, not a sign-off.

## Anti-patterns

- A failed lot left in the issue location
- Skipping a critical check for speed
- No fail reaction

## Related skills

- `quality-control-plan`
- `supplier-quality`
