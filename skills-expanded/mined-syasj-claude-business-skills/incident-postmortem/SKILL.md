---
name: incident-postmortem
description: "Write a blameless postmortem that records the timeline, the impact, and the corrective actions that change a system. Use when the user mentions postmortem, incident review, writeup of an outage, blameless review, or asks for a postmortem. Engineering skill by Yasir Jilani."
license: MIT
compatibility: Agent Skills standard. No network access, extra packages, or credentials required.
metadata:
  author: Yasir Jilani
  version: "1.0.0"
  domain: engineering
---

<!-- GENERATED FILE - edits here are overwritten by scripts/generate.py.
     Edit the 'incident-postmortem' entry in source/, then run:
       python3 scripts/generate.py && python3 scripts/validate.py
     See CONTRIBUTING.md. -->

# Incident Postmortem

Write a blameless postmortem that records the timeline, the impact, and the corrective actions that change a system.

## When to use this skill

Use this skill when the user:

- postmortem
- incident review
- writeup of an outage
- blameless review

## When not to use this skill

- The user wants a different domain's specialist skill.
- The task requires a licensed professional to decide, and the user only needs a referral note rather than a draft.
- The request asks you to deceive, evade a control, or hide material facts.

## Professional boundary

Prefer the repository's existing patterns. Do not disable security controls, invent credentials, or introduce network calls the user did not ask for.

## Operating boundaries

- Use only information the user provides or files they explicitly ask you to read. Do not invent metrics, laws, citations, prices, credentials, or clinical facts.
- Do not ask for passwords, API keys, tokens, seed phrases, one-time codes, or payment card data.
- Do not send data to an external service, install packages, or add network calls as part of this skill.
- Separate facts, assumptions, and recommendations. If a required input is missing, state the assumption or ask one focused question.
- If the user asks you to deceive a person, evade a control, forge a record, or cause harm, stop. Offer a legitimate alternative.
- Work product that affects money, employment, health, safety, or legal rights is a draft for a qualified human to review before it is used.

## Inputs to collect

- Timeline of facts
- User impact
- What detection showed
- Actions already taken

## Workflow


### 1. Facts

A timeline with times and sources. Unknowns stay unknown. Do not invent a root cause to close the doc.
### 2. Impact

Who was affected and how, using the user's data. No inflated or minimized impact.
### 3. Contributing factors

System and process, not a villain. Human error is a prompt to ask why the system allowed it.
### 4. Detection

How it was found, and how it could be found sooner without a surveillance program on people.
### 5. Actions

A few actions with owners that change code, config, or process. A lesson with no owner is a wish.
### 6. Follow-up

A date to check that actions landed. No action, no closure.

## Output

Deliver a **postmortem**.

- Purpose of this postmortem, in two sentences.
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

Aisha Rahman, engineering lead at Fieldnote in Edmonton, needs a postmortem by 30 September 2026. A draft postmortem says the outage happened because 'Alex was careless'.

### Example data

```text
From: Aisha Rahman, engineering lead
Organization: Fieldnote, Edmonton
Date: 14 September 2026
Needed by: 30 September 2026

A draft postmortem says the outage happened because 'Alex was careless'.

Timeline of facts: five working days, due 30 September 2026
User impact: Invoice job. Stated in the ask, not documented anywhere else
What detection showed: Status page, last reviewed 14 September 2026. No owner named since
Actions already taken: Checkout service; Invoice job. Both unassigned as of 14 September 2026
```

### Example outcome

**Postmortem**
To: Aisha Rahman, engineering lead, Fieldnote
Date: 14 September 2026 · Needed by: 30 September 2026

**Decision**
Replaces the blame line with the missing guardrail and one owned system fix.

**What the file supports**

| Input | Value | Status |
| --- | --- | --- |
| Timeline of facts | five working days, due 30 September 2026 | Needs confirmation |
| User impact | Invoice job. Stated in the ask, not documented anywhere else | Carried into the draft |
| What detection showed | Status page, last reviewed 14 September 2026. No owner named since | Carried into the draft |
| Actions already taken | Checkout service; Invoice job. Both unassigned as of 14 September 2026 | Needs confirmation |

**How this draft was built**

**1. Facts**  
A timeline with times and sources. Unknowns stay unknown. Do not invent a root cause to close the doc.

**2. Impact**  
Who was affected and how, using the user's data. No inflated or minimized impact.

**3. Contributing factors**  
System and process, not a villain. Human error is a prompt to ask why the system allowed it.

**4. Detection**  
How it was found, and how it could be found sooner without a surveillance program on people.

**5. Actions**  
A few actions with owners that change code, config, or process. A lesson with no owner is a wish.

**Deliberately not done**
- A blame essay.
- An invented root cause.
- Twenty actions and no owners.

**Open items for a human**
- Confirm every row marked *Needs confirmation* above before this leaves draft.
- Anything absent from the file stayed absent. No figure, date, or name was supplied from outside it.

Next: Aisha Rahman by 30 September 2026. This is a draft, not a sign-off.

## Anti-patterns

- A blame essay.
- An invented root cause.
- Twenty actions and no owners.

## Related skills

- `oncall-handoff`
- `incident-response-coord`
