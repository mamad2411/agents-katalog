---
name: gemba-walk
description: "Plan a gemba walk that observes a process and asks why, without turning it into a compliance raid. Use when the user mentions gemba walk, shop floor walk, go and see, process observation, or asks for a gemba notes. Manufacturing and quality skill by Yasir Jilani."
license: MIT
compatibility: Agent Skills standard. No network access, extra packages, or credentials required.
metadata:
  author: Yasir Jilani
  version: "1.0.0"
  domain: manufacturing
---

<!-- GENERATED FILE - edits here are overwritten by scripts/generate.py.
     Edit the 'gemba-walk' entry in source/, then run:
       python3 scripts/generate.py && python3 scripts/validate.py
     See CONTRIBUTING.md. -->

# Gemba Walk

Plan a gemba walk that observes a process and asks why, without turning it into a compliance raid.

## When to use this skill

Use this skill when the user:

- gemba walk
- shop floor walk
- go and see
- process observation

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

- The process to see
- The question
- Who will walk
- How notes will be used

## Workflow


### 1. Step 1

Pick one process and one question.
### 2. Step 2

Observe before suggesting. Write what you see, not a speech.
### 3. Step 3

Ask why a deviation happens. The answer is information.
### 4. Step 4

Do not use the walk to surprise-punish someone. Say how notes will be used.
### 5. Step 5

Leave with one improvement the team agrees to try, or a clear open question.
### 6. Step 6

Safety issues are stopped or escalated immediately under their rule.

## Output

Deliver a **gemba notes**.

- Purpose of this gemba notes, in two sentences.
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

Gus Moretti, plant manager at Redline Parts in Nisku, needs a gemba notes by 30 September 2026. A leader plans a walk to catch operators breaking the instruction.

### Example data

```text
From: Gus Moretti, plant manager
Organization: Redline Parts, Nisku
Date: 14 September 2026
Needed by: 30 September 2026

A leader plans a walk to catch operators breaking the instruction.

The process to see: email to Gus Moretti. No written steps after 1 Sep 2026
The question: A leader plans a walk to catch operators breaking the instruction
Who will walk: Gus Moretti, plant manager
How notes will be used: one file, dated 14 September 2026. No earlier version attached for comparison
```

### Example outcome

**Gemba notes**
To: Gus Moretti, plant manager, Redline Parts
Date: 14 September 2026 · Needed by: 30 September 2026

**Decision**
Observes the obstacle, bans surprise punishment, and still escalates safety issues.

**What the file supports**

| Input | Value | Status |
| --- | --- | --- |
| The process to see | email to Gus Moretti. No written steps after 1 Sep 2026 | Needs confirmation |
| The question | A leader plans a walk to catch operators breaking the instruction | Carried into the draft |
| Who will walk | Gus Moretti, plant manager | Carried into the draft |
| How notes will be used | one file, dated 14 September 2026. No earlier version attached for comparison | Needs confirmation |

**How this draft was built**

**1. Pick one process and one question**

**2. Observe before suggesting. Write what you see, not a speech**

**3. Ask why a deviation happens. The answer is information**

**4. Do not use the walk to surprise-punish someone. Say how notes will be used**

**5. Leave with one improvement the team agrees to try, or a clear open question**

**Deliberately not done**
- A compliance raid in disguise.
- Suggestions before observation.
- Ignoring a safety issue.

**Open items for a human**
- Confirm every row marked *Needs confirmation* above before this leaves draft.
- Anything absent from the file stayed absent. No figure, date, or name was supplied from outside it.

Next: Gus Moretti by 30 September 2026. This is a draft, not a sign-off.

## Anti-patterns

- A compliance raid in disguise
- Suggestions before observation
- Ignoring a safety issue

## Related skills

- `continuous-improvement`
- `shift-handover`
