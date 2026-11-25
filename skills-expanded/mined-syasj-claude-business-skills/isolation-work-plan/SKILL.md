---
name: isolation-work-plan
description: "Review an isolation or lockout plan for named points and a prove-dead step, without telling anyone to skip it. Use when the user mentions lockout plan, isolation review, permit to work review, energy isolation, or asks for a isolation plan review. Energy and utilities operations skill by Yasir Jilani."
license: MIT
compatibility: Agent Skills standard. No network access, extra packages, or credentials required.
metadata:
  author: Yasir Jilani
  version: "1.0.0"
  domain: energy
---

<!-- GENERATED FILE - edits here are overwritten by scripts/generate.py.
     Edit the 'isolation-work-plan' entry in source/, then run:
       python3 scripts/generate.py && python3 scripts/validate.py
     See CONTRIBUTING.md. -->

# Isolation Work Plan Review

Review an isolation or lockout plan for named points and a prove-dead step, without telling anyone to skip it.

## When to use this skill

Use this skill when the user:

- lockout plan
- isolation review
- permit to work review
- energy isolation

## When not to use this skill

- Bypassing lockout or isolation

## Professional boundary

Operational energy advice is not a permit and not a safety case. Do not bypass lockout, isolation, or regulatory limits.

## Operating boundaries

- Use only information the user provides or files they explicitly ask you to read. Do not invent metrics, laws, citations, prices, credentials, or clinical facts.
- Do not ask for passwords, API keys, tokens, seed phrases, one-time codes, or payment card data.
- Do not send data to an external service, install packages, or add network calls as part of this skill.
- Separate facts, assumptions, and recommendations. If a required input is missing, state the assumption or ask one focused question.
- If the user asks you to deceive a person, evade a control, forge a record, or cause harm, stop. Offer a legitimate alternative.
- Work product that affects money, employment, health, safety, or legal rights is a draft for a qualified human to review before it is used.

## Inputs to collect

- The equipment
- Isolation points they listed
- The prove-dead step
- The issuer

## Workflow


### 1. Step 1

Check that isolation points are named, not implied.
### 2. Step 2

Require the prove-dead step they use.
### 3. Step 3

Do not suggest a shortcut around a lock or a tag.
### 4. Step 4

Identify a missing point as a stop.
### 5. Step 5

Name the issuer and the worker role they described.
### 6. Step 6

This review is not a permit to start work.

## Output

Deliver a **isolation plan review**.

- Purpose of this isolation plan review, in two sentences.
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

Devon Hale, operations superintendent at Prairie Line Energy in Grande Prairie, needs an isolation plan review by 30 September 2026. A plan says to isolate 'as usual' and skip the test because the crew is experienced.

### Example data

```text
From: Devon Hale, operations superintendent
Organization: Prairie Line Energy, Grande Prairie
Date: 14 September 2026
Needed by: 30 September 2026

A plan says to isolate 'as usual' and skip the test because the crew is experienced.

The equipment: Feeder 12, recorded 14 September 2026. No supporting file attached
Isolation points they listed: Feeder 12; Site meter 4; September bill
The prove-dead step: Feeder 12; Site meter 4. Both unassigned as of 14 September 2026
The issuer: Feeder 12, recorded 14 September 2026. No supporting file attached
```

### Example outcome

**Isolation plan review**
To: Devon Hale, operations superintendent, Prairie Line Energy
Date: 14 September 2026 · Needed by: 30 September 2026

**Decision**
Blocks the skip and requires named points and the test.

**What the file supports**

| Input | Value | Status |
| --- | --- | --- |
| The equipment | Feeder 12, recorded 14 September 2026. No supporting file attached | Needs confirmation |
| Isolation points they listed | Feeder 12; Site meter 4; September bill | Carried into the draft |
| The prove-dead step | Feeder 12; Site meter 4. Both unassigned as of 14 September 2026 | Carried into the draft |
| The issuer | Feeder 12, recorded 14 September 2026. No supporting file attached | Needs confirmation |

**How this draft was built**

**1. Check that isolation points are named, not implied**

**2. Require the prove-dead step they use**

**3. Do not suggest a shortcut around a lock or a tag**

**4. Identify a missing point as a stop**

**5. Name the issuer and the worker role they described**

**Deliberately not done**
- A shortcut around lockout.
- Implied isolation points.
- A review treated as a permit.

**Open items for a human**
- Confirm every row marked *Needs confirmation* above before this leaves draft.
- Anything absent from the file stayed absent. No figure, date, or name was supplied from outside it.

Next: Devon Hale by 30 September 2026. This is a draft, not a sign-off.

## Anti-patterns

- A shortcut around lockout
- Implied isolation points
- A review treated as a permit

## Related skills

- `safety-toolbox-talk`
- `work-instruction`
