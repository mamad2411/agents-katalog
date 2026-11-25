---
name: journey-map
description: "Map a customer journey around a real job, including waits, handoffs, and backstage failures. Use when the user mentions journey map, customer journey, experience map, map the onboarding journey, or asks for a journey map. Customer experience skill by Yasir Jilani."
license: MIT
compatibility: Agent Skills standard. No network access, extra packages, or credentials required.
metadata:
  author: Yasir Jilani
  version: "1.0.0"
  domain: customer
---

<!-- GENERATED FILE - edits here are overwritten by scripts/generate.py.
     Edit the 'journey-map' entry in source/, then run:
       python3 scripts/generate.py && python3 scripts/validate.py
     See CONTRIBUTING.md. -->

# Journey Map

Map a customer journey around a real job, including waits, handoffs, and backstage failures.

## When to use this skill

Use this skill when the user:

- journey map
- customer journey
- experience map
- map the onboarding journey

## When not to use this skill

- The user wants a different domain's specialist skill.
- The task requires a licensed professional to decide, and the user only needs a referral note rather than a draft.
- The request asks you to deceive, evade a control, or hide material facts.

## Professional boundary

Do not blame the customer. Do not invent policy exceptions. Do not ask a customer for passwords or full payment card numbers.

## Operating boundaries

- Use only information the user provides or files they explicitly ask you to read. Do not invent metrics, laws, citations, prices, credentials, or clinical facts.
- Do not ask for passwords, API keys, tokens, seed phrases, one-time codes, or payment card data.
- Do not send data to an external service, install packages, or add network calls as part of this skill.
- Separate facts, assumptions, and recommendations. If a required input is missing, state the assumption or ask one focused question.
- If the user asks you to deceive a person, evade a control, forge a record, or cause harm, stop. Offer a legitimate alternative.
- Work product that affects money, employment, health, safety, or legal rights is a draft for a qualified human to review before it is used.

## Inputs to collect

- The job the customer is trying to finish
- Stages they actually pass
- Evidence of pain
- Backstage teams

## Workflow


### 1. Step 1

Define the job and the actor. A map of 'the customer' in general is too vague.
### 2. Step 2

Use stages they can evidence. Do not add a delightful stage they wish existed and call it current.
### 3. Step 3

Mark waits and repeats.
### 4. Step 4

Show the backstage handoff that causes a frontstage failure.
### 5. Step 5

Pick one moment to fix first, based on severity or drop-off they can show.
### 6. Step 6

Keep emotions only if a customer stated them. Do not invent a feeling.

## Output

Deliver a **journey map**.

- Purpose of this journey map, in two sentences.
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

Rita Santos, support lead at Fieldnote in Edmonton, needs a journey map by 30 September 2026. A map shows effortless onboarding while support tickets cluster on setup.

### Example data

```text
From: Rita Santos, support lead
Organization: Fieldnote, Edmonton
Date: 14 September 2026
Needed by: 30 September 2026

A map shows effortless onboarding while support tickets cluster on setup.

The job the customer is trying to finish: the shopper solving one task in one trip. Not segmented further in the file
Stages they actually pass: Ticket 4412, last reviewed 14 September 2026. No owner named since
Evidence of pain: one PDF, 2 pages, dated 14 September 2026
Backstage teams: two people on shift, one off
```

### Example outcome

**Journey map**
To: Rita Santos, support lead, Fieldnote
Date: 14 September 2026 · Needed by: 30 September 2026

**Decision**
Includes the setup failure and picks that moment to fix.

**What the file supports**

| Input | Value | Status |
| --- | --- | --- |
| The job the customer is trying to finish | the shopper solving one task in one trip. Not segmented further in the file | Needs confirmation |
| Stages they actually pass | Ticket 4412, last reviewed 14 September 2026. No owner named since | Carried into the draft |
| Evidence of pain | one PDF, 2 pages, dated 14 September 2026 | Carried into the draft |
| Backstage teams | two people on shift, one off | Needs confirmation |

**How this draft was built**

**1. Define the job and the actor. A map of 'the customer' in general is too vague**

**2. Use stages they can evidence. Do not add a delightful stage they wish existed and call it current**

**3. Mark waits and repeats**

**4. Show the backstage handoff that causes a frontstage failure**

**5. Pick one moment to fix first, based on severity or drop-off they can show**

**Deliberately not done**
- A fantasy journey labeled current.
- Invented emotions.
- No backstage handoff.

**Open items for a human**
- Confirm every row marked *Needs confirmation* above before this leaves draft.
- Anything absent from the file stayed absent. No figure, date, or name was supplied from outside it.

Next: Rita Santos by 30 September 2026. This is a draft, not a sign-off.

## Anti-patterns

- A fantasy journey labeled current
- Invented emotions
- No backstage handoff

## Related skills

- `service-blueprint`
- `onboarding-success-plan`
