---
name: prototype-test-script
description: "Write a prototype test script that gives the participant a goal and does not reveal the clicks. Use when the user mentions prototype test, usability script, test script, moderated test, or asks for a prototype test script. Design skill by Yasir Jilani."
license: MIT
compatibility: Agent Skills standard. No network access, extra packages, or credentials required.
metadata:
  author: Yasir Jilani
  version: "1.0.0"
  domain: design
---

<!-- GENERATED FILE - edits here are overwritten by scripts/generate.py.
     Edit the 'prototype-test-script' entry in source/, then run:
       python3 scripts/generate.py && python3 scripts/validate.py
     See CONTRIBUTING.md. -->

# Prototype Test Script

Write a prototype test script that gives the participant a goal and does not reveal the clicks.

## When to use this skill

Use this skill when the user:

- prototype test
- usability script
- test script
- moderated test

## When not to use this skill

- The user wants a different domain's specialist skill.
- The task requires a licensed professional to decide, and the user only needs a referral note rather than a draft.
- The request asks you to deceive, evade a control, or hide material facts.

## Professional boundary

Design critique improves the work. Do not copy a third party's branded assets. Accessibility is part of done, not a later pass to skip.

## Operating boundaries

- Use only information the user provides or files they explicitly ask you to read. Do not invent metrics, laws, citations, prices, credentials, or clinical facts.
- Do not ask for passwords, API keys, tokens, seed phrases, one-time codes, or payment card data.
- Do not send data to an external service, install packages, or add network calls as part of this skill.
- Separate facts, assumptions, and recommendations. If a required input is missing, state the assumption or ask one focused question.
- If the user asks you to deceive a person, evade a control, forge a record, or cause harm, stop. Offer a legitimate alternative.
- Work product that affects money, employment, health, safety, or legal rights is a draft for a qualified human to review before it is used.

## Inputs to collect

- The prototype scope
- The goal
- The participant
- Time

## Workflow


### 1. Step 1

Set the scene without naming the button.
### 2. Step 2

Give a goal and a definition of done.
### 3. Step 3

Plan neutral probes for hesitation.
### 4. Step 4

Do not ask if they like it until the task is done, if at all.
### 5. Step 5

Note what the prototype cannot do so the facilitator does not fake a path.
### 6. Step 6

End with consent-respecting notes and no identity beyond the study id.

## Output

Deliver a **prototype test script**.

- Purpose of this prototype test script, in two sentences.
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

Lena Ortiz, design lead at Fieldnote in Edmonton, needs a prototype test script by 30 September 2026. A script says 'click the blue button in the corner' as the task.

### Example data

```text
From: Lena Ortiz, design lead
Organization: Fieldnote, Edmonton
Date: 14 September 2026
Needed by: 30 September 2026

A script says 'click the blue button in the corner' as the task.

The prototype scope: this decision only
The goal: A script says 'click the blue button in the corner' as the task. Stated once, in the ask. Not written down anywhere else
The participant: Lena Ortiz plus two others named in the thread. No distribution list attached
Time: five working days, due 30 September 2026
```

### Example outcome

**Prototype test script**
To: Lena Ortiz, design lead, Fieldnote
Date: 14 September 2026 · Needed by: 30 September 2026

**Decision**
Gives the goal and removes the click path.

**What the file supports**

| Input | Value | Status |
| --- | --- | --- |
| The prototype scope | this decision only | Needs confirmation |
| The goal | A script says 'click the blue button in the corner' as the task. Stated once, in the ask. Not written down anywhere else | Carried into the draft |
| The participant | Lena Ortiz plus two others named in the thread. No distribution list attached | Carried into the draft |
| Time | five working days, due 30 September 2026 | Needs confirmation |

**How this draft was built**

**1. Set the scene without naming the button**

**2. Give a goal and a definition of done**

**3. Plan neutral probes for hesitation**

**4. Do not ask if they like it until the task is done, if at all**

**5. Note what the prototype cannot do so the facilitator does not fake a path**

**Deliberately not done**
- Click-by-click instructions.
- A likeability question as the test.
- A fake path the prototype cannot do.

**Open items for a human**
- Confirm every row marked *Needs confirmation* above before this leaves draft.
- Anything absent from the file stayed absent. No figure, date, or name was supplied from outside it.

Next: Lena Ortiz by 30 September 2026. This is a draft, not a sign-off.

## Anti-patterns

- Click-by-click instructions
- A likeability question as the test
- A fake path the prototype cannot do

## Related skills

- `usability-test-plan`
- `usability-findings`
