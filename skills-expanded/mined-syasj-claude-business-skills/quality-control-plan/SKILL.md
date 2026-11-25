---
name: quality-control-plan
description: "Draft a control plan for a process step: what is checked, how often, and what happens on a fail. Use when the user mentions control plan, quality plan, inspection plan, process control plan, or asks for a control plan. Manufacturing and quality skill by Yasir Jilani."
license: MIT
compatibility: Agent Skills standard. No network access, extra packages, or credentials required.
metadata:
  author: Yasir Jilani
  version: "1.0.0"
  domain: manufacturing
---

<!-- GENERATED FILE - edits here are overwritten by scripts/generate.py.
     Edit the 'quality-control-plan' entry in source/, then run:
       python3 scripts/generate.py && python3 scripts/validate.py
     See CONTRIBUTING.md. -->

# Quality Control Plan

Draft a control plan for a process step: what is checked, how often, and what happens on a fail.

## When to use this skill

Use this skill when the user:

- control plan
- quality plan
- inspection plan
- process control plan

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

- The characteristic
- The method
- The frequency
- The reaction to a fail

## Workflow


### 1. Step 1

Name the characteristic that matters to the customer or the safety rule they cited.
### 2. Step 2

Specify method and frequency they can staff.
### 3. Write the reaction to a fail

stop, sort, or call. A fail with no reaction is a finding.
### 4. Step 4

Identify the owner of the check.
### 5. Step 5

Do not loosen a limit they said is safety-related.
### 6. Step 6

Link the plan to the work instruction rather than creating a second unofficial standard.

## Output

Deliver a **control plan**.

- Purpose of this control plan, in two sentences.
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

Gus Moretti, plant manager at Redline Parts in Nisku, needs a control plan by 30 September 2026. A plan checks a safety dimension weekly because daily checks feel expensive.

### Example data

```text
From: Gus Moretti, plant manager
Organization: Redline Parts, Nisku
Date: 14 September 2026
Needed by: 30 September 2026

A plan checks a safety dimension weekly because daily checks feel expensive.

The characteristic: Line 2, recorded 14 September 2026. No supporting file attached
The method: the method in the ask. No second design attached
The frequency: Line 2, recorded 14 September 2026. No supporting file attached
The reaction to a fail: Line 2; Lot 26-0914. Both unassigned as of 14 September 2026
```

### Example outcome

**Control plan**
To: Gus Moretti, plant manager, Redline Parts
Date: 14 September 2026 · Needed by: 30 September 2026

**Decision**
Keeps the safety check at the frequency their rule requires and flags the cost as a separate decision.

**What the file supports**

| Input | Value | Status |
| --- | --- | --- |
| The characteristic | Line 2, recorded 14 September 2026. No supporting file attached | Needs confirmation |
| The method | the method in the ask. No second design attached | Carried into the draft |
| The frequency | Line 2, recorded 14 September 2026. No supporting file attached | Carried into the draft |
| The reaction to a fail | Line 2; Lot 26-0914. Both unassigned as of 14 September 2026 | Needs confirmation |

**How this draft was built**

**1. Name the characteristic that matters to the customer or the safety rule they cited**

**2. Specify method and frequency they can staff**

**3. Write the reaction to a fail**  
stop, sort, or call. A fail with no reaction is a finding.

**4. Identify the owner of the check**

**5. Do not loosen a limit they said is safety-related**

**Deliberately not done**
- A check with no reaction.
- Loosening a safety limit.
- An unstaffed frequency.

**Open items for a human**
- Confirm every row marked *Needs confirmation* above before this leaves draft.
- Anything absent from the file stayed absent. No figure, date, or name was supplied from outside it.

Next: Gus Moretti by 30 September 2026. This is a draft, not a sign-off.

## Anti-patterns

- A check with no reaction
- Loosening a safety limit
- An unstaffed frequency

## Related skills

- `incoming-inspection`
- `work-instruction`
