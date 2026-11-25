---
name: safety-toolbox-talk
description: "Draft a toolbox talk for a specific site hazard, with the control the crew must use. Use when the user mentions toolbox talk, safety briefing, pre-task briefing, site safety talk, or asks for a toolbox talk. Construction skill by Yasir Jilani."
license: MIT
compatibility: Agent Skills standard. No network access, extra packages, or credentials required.
metadata:
  author: Yasir Jilani
  version: "1.0.0"
  domain: construction
---

<!-- GENERATED FILE - edits here are overwritten by scripts/generate.py.
     Edit the 'safety-toolbox-talk' entry in source/, then run:
       python3 scripts/generate.py && python3 scripts/validate.py
     See CONTRIBUTING.md. -->

# Safety Toolbox Talk

Draft a toolbox talk for a specific site hazard, with the control the crew must use.

## When to use this skill

Use this skill when the user:

- toolbox talk
- safety briefing
- pre-task briefing
- site safety talk

## When not to use this skill

- Skipping safety controls

## Professional boundary

Site safety and contract administration follow the contract and the site rules. Do not tell anyone to skip a safety control. Do not invent quantities.

## Operating boundaries

- Use only information the user provides or files they explicitly ask you to read. Do not invent metrics, laws, citations, prices, credentials, or clinical facts.
- Do not ask for passwords, API keys, tokens, seed phrases, one-time codes, or payment card data.
- Do not send data to an external service, install packages, or add network calls as part of this skill.
- Separate facts, assumptions, and recommendations. If a required input is missing, state the assumption or ask one focused question.
- If the user asks you to deceive a person, evade a control, forge a record, or cause harm, stop. Offer a legitimate alternative.
- Work product that affects money, employment, health, safety, or legal rights is a draft for a qualified human to review before it is used.

## Inputs to collect

- The hazard
- The required control
- The crew
- Incidents they can mention without blame

## Workflow


### 1. Step 1

Name the hazard in the work they are about to do.
### 2. Step 2

State the control in steps.
### 3. Say what to do if the control is missing

stop and tell the supervisor.
### 4. Step 4

Do not tell anyone to skip a guard, a harness, or a lockout.
### 5. Step 5

Keep blame out of the example.
### 6. Step 6

End with a check that the control is in place today.

## Output

Deliver a **toolbox talk**.

- Purpose of this toolbox talk, in two sentences.
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

Tom Reilly, site lead at Birch Siteworks in Cochrane, needs a toolbox talk by 30 September 2026. A draft says to skip the harness because the task is short.

### Example data

```text
From: Tom Reilly, site lead
Organization: Birch Siteworks, Cochrane
Date: 14 September 2026
Needed by: 30 September 2026

A draft says to skip the harness because the task is short.

The hazard: Birch site, Cochrane, recorded 14 September 2026. No supporting file attached
The required control: their one-page rule dated 2 Mar 2026. No exception log since
The crew: Birch site, Cochrane, recorded 14 September 2026. No supporting file attached
Incidents they can mention without blame: Birch site, Cochrane, first seen 14 September 2026. No root cause recorded yet
```

### Example outcome

**Toolbox talk**
To: Tom Reilly, site lead, Birch Siteworks
Date: 14 September 2026 · Needed by: 30 September 2026

**Decision**
Requires the harness and stops the task if it is missing.

**What the file supports**

| Input | Value | Status |
| --- | --- | --- |
| The hazard | Birch site, Cochrane, recorded 14 September 2026. No supporting file attached | Needs confirmation |
| The required control | their one-page rule dated 2 Mar 2026. No exception log since | Carried into the draft |
| The crew | Birch site, Cochrane, recorded 14 September 2026. No supporting file attached | Carried into the draft |
| Incidents they can mention without blame | Birch site, Cochrane, first seen 14 September 2026. No root cause recorded yet | Needs confirmation |

**How this draft was built**

**1. Name the hazard in the work they are about to do**

**2. State the control in steps**

**3. Say what to do if the control is missing**  
stop and tell the supervisor.

**4. Do not tell anyone to skip a guard, a harness, or a lockout**

**5. Keep blame out of the example**

**Deliberately not done**
- Advice to skip a safety control.
- A generic talk with no hazard.
- Blame.

**Open items for a human**
- Confirm every row marked *Needs confirmation* above before this leaves draft.
- Anything absent from the file stayed absent. No figure, date, or name was supplied from outside it.

Next: Tom Reilly by 30 September 2026. This is a draft, not a sign-off.

## Anti-patterns

- Advice to skip a safety control
- A generic talk with no hazard
- Blame

## Related skills

- `gemba-walk`
- `site-daily-report`
