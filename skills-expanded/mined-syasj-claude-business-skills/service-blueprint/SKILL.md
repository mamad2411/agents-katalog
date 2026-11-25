---
name: service-blueprint
description: "Blueprint a service so frontstage customer steps and backstage failures sit on one page. Use when the user mentions service blueprint, service design, backstage map, blueprint a service, or asks for a service blueprint. Design skill by Yasir Jilani."
license: MIT
compatibility: Agent Skills standard. No network access, extra packages, or credentials required.
metadata:
  author: Yasir Jilani
  version: "1.0.0"
  domain: design
---

<!-- GENERATED FILE - edits here are overwritten by scripts/generate.py.
     Edit the 'service-blueprint' entry in source/, then run:
       python3 scripts/generate.py && python3 scripts/validate.py
     See CONTRIBUTING.md. -->

# Service Blueprint

Blueprint a service so frontstage customer steps and backstage failures sit on one page.

## When to use this skill

Use this skill when the user:

- service blueprint
- service design
- backstage map
- blueprint a service

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

- The customer job
- Frontstage steps
- Backstage teams
- Evidence of failure

## Workflow


### 1. Step 1

Start with the customer steps.
### 2. Step 2

Add the backstage actions and systems that support each step.
### 3. Step 3

Mark the fail points they have evidence for.
### 4. Step 4

Show the handoff that drops the ball.
### 5. Step 5

Pick one fail point to redesign.
### 6. Step 6

Do not draw a blueprint of a service they do not operate and call it current.

## Output

Deliver a **service blueprint**.

- Purpose of this service blueprint, in two sentences.
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

Lena Ortiz, design lead at Fieldnote in Edmonton, needs a service blueprint by 30 September 2026. The blueprint shows a smooth handoff, but tickets pile up between sales and onboarding.

### Example data

```text
From: Lena Ortiz, design lead
Organization: Fieldnote, Edmonton
Date: 14 September 2026
Needed by: 30 September 2026

The blueprint shows a smooth handoff, but tickets pile up between sales and onboarding.

The customer job: the shopper solving one task in one trip. Not segmented further in the file
Frontstage steps: Checkout screen v4; Empty-state copy. Both unassigned as of 14 September 2026
Backstage teams: two people on shift, one off
Evidence of failure: one PDF, 2 pages, dated 14 September 2026
```

### Example outcome

**Service blueprint**
To: Lena Ortiz, design lead, Fieldnote
Date: 14 September 2026 · Needed by: 30 September 2026

**Decision**
Draws the pile-up and assigns the handoff to fix.

**What the file supports**

| Input | Value | Status |
| --- | --- | --- |
| The customer job | the shopper solving one task in one trip. Not segmented further in the file | Needs confirmation |
| Frontstage steps | Checkout screen v4; Empty-state copy. Both unassigned as of 14 September 2026 | Carried into the draft |
| Backstage teams | two people on shift, one off | Carried into the draft |
| Evidence of failure | one PDF, 2 pages, dated 14 September 2026 | Needs confirmation |

**How this draft was built**

**1. Start with the customer steps**

**2. Add the backstage actions and systems that support each step**

**3. Mark the fail points they have evidence for**

**4. Show the handoff that drops the ball**

**5. Pick one fail point to redesign**

**Deliberately not done**
- A frontstage-only journey called a blueprint.
- Invented backstage steps.
- No fail point.

**Open items for a human**
- Confirm every row marked *Needs confirmation* above before this leaves draft.
- Anything absent from the file stayed absent. No figure, date, or name was supplied from outside it.

Next: Lena Ortiz by 30 September 2026. This is a draft, not a sign-off.

## Anti-patterns

- A frontstage-only journey called a blueprint
- Invented backstage steps
- No fail point

## Related skills

- `journey-map`
- `process-map`
