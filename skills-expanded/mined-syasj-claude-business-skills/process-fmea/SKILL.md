---
name: process-fmea
description: "Facilitate a process FMEA on a few high-risk steps, with actions for the failures that lack detection. Use when the user mentions FMEA, process FMEA, failure mode, risk in the process, or asks for a FMEA notes. Manufacturing and quality skill by Yasir Jilani."
license: MIT
compatibility: Agent Skills standard. No network access, extra packages, or credentials required.
metadata:
  author: Yasir Jilani
  version: "1.0.0"
  domain: manufacturing
---

<!-- GENERATED FILE - edits here are overwritten by scripts/generate.py.
     Edit the 'process-fmea' entry in source/, then run:
       python3 scripts/generate.py && python3 scripts/validate.py
     See CONTRIBUTING.md. -->

# Process FMEA Facilitation

Facilitate a process FMEA on a few high-risk steps, with actions for the failures that lack detection.

## When to use this skill

Use this skill when the user:

- FMEA
- process FMEA
- failure mode
- risk in the process

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

- The process steps
- Failures they have seen
- Current controls
- Their scoring scale if any

## Workflow


### 1. Step 1

Limit the session to the steps that can hurt the customer or safety.
### 2. Step 2

Write failure modes as what goes wrong, not as one-word fears.
### 3. Step 3

Record current prevention and detection.
### 4. Step 4

Use their scale or a labeled simple scale. Do not pretend a score is precise.
### 5. Step 5

Actions go to high-severity gaps with weak detection.
### 6. Step 6

Do not lower a severity score to make the chart look calm.

## Output

Deliver a **FMEA notes**.

- Purpose of this FMEA notes, in two sentences.
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

Gus Moretti, plant manager at Redline Parts in Nisku, needs a FMEA notes by 30 September 2026. A team wants to mark a safety failure as low severity so the FMEA looks acceptable.

### Example data

```text
From: Gus Moretti, plant manager
Organization: Redline Parts, Nisku
Date: 14 September 2026
Needed by: 30 September 2026

A team wants to mark a safety failure as low severity so the FMEA looks acceptable.

The process steps: email to Gus Moretti. No written steps after 1 Sep 2026
Failures they have seen: Line 2, first seen 14 September 2026. No root cause recorded yet
Current controls: their one-page rule dated 2 Mar 2026. No exception log since
Their scoring scale if any: Lot 26-0914, last reviewed 14 September 2026. No owner named since
```

### Example outcome

**Fmea notes**
To: Gus Moretti, plant manager, Redline Parts
Date: 14 September 2026 · Needed by: 30 September 2026

**Decision**
Notes that keep the high severity and assign an action instead of editing the score.

**What the file supports**

| Input | Value | Status |
| --- | --- | --- |
| The process steps | email to Gus Moretti. No written steps after 1 Sep 2026 | Needs confirmation |
| Failures they have seen | Line 2, first seen 14 September 2026. No root cause recorded yet | Carried into the draft |
| Current controls | their one-page rule dated 2 Mar 2026. No exception log since | Carried into the draft |
| Their scoring scale if any | Lot 26-0914, last reviewed 14 September 2026. No owner named since | Needs confirmation |

**How this draft was built**

**1. Limit the session to the steps that can hurt the customer or safety**

**2. Write failure modes as what goes wrong, not as one-word fears**

**3. Record current prevention and detection**

**4. Use their scale or a labeled simple scale. Do not pretend a score is precise**

**5. Actions go to high-severity gaps with weak detection**

**Deliberately not done**
- Lowering severity to look green.
- A whole factory in one session.
- Scores with no action.

**Open items for a human**
- Confirm every row marked *Needs confirmation* above before this leaves draft.
- Anything absent from the file stayed absent. No figure, date, or name was supplied from outside it.

Next: Gus Moretti by 30 September 2026. This is a draft, not a sign-off.

## Anti-patterns

- Lowering severity to look green
- A whole factory in one session
- Scores with no action

## Related skills

- `quality-control-plan`
- `risk-assessment`
