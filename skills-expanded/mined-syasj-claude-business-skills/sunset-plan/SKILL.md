---
name: sunset-plan
description: "Plan the retirement of a feature or product so users are told the truth and given a path. Use when the user mentions sunset a feature, deprecate, end of life, retire a product, or asks for a sunset plan. Product skill by Yasir Jilani."
license: MIT
compatibility: Agent Skills standard. No network access, extra packages, or credentials required.
metadata:
  author: Yasir Jilani
  version: "1.0.0"
  domain: product
---

<!-- GENERATED FILE - edits here are overwritten by scripts/generate.py.
     Edit the 'sunset-plan' entry in source/, then run:
       python3 scripts/generate.py && python3 scripts/validate.py
     See CONTRIBUTING.md. -->

# Sunset Plan

Plan the retirement of a feature or product so users are told the truth and given a path.

## When to use this skill

Use this skill when the user:

- sunset a feature
- deprecate
- end of life
- retire a product

## When not to use this skill

- The user wants a different domain's specialist skill.
- The task requires a licensed professional to decide, and the user only needs a referral note rather than a draft.
- The request asks you to deceive, evade a control, or hide material facts.

## Professional boundary

Product recommendations are hypotheses until evidence says otherwise. Label confidence. Do not ship dark patterns that hide cost or consent.

## Operating boundaries

- Use only information the user provides or files they explicitly ask you to read. Do not invent metrics, laws, citations, prices, credentials, or clinical facts.
- Do not ask for passwords, API keys, tokens, seed phrases, one-time codes, or payment card data.
- Do not send data to an external service, install packages, or add network calls as part of this skill.
- Separate facts, assumptions, and recommendations. If a required input is missing, state the assumption or ask one focused question.
- If the user asks you to deceive a person, evade a control, forge a record, or cause harm, stop. Offer a legitimate alternative.
- Work product that affects money, employment, health, safety, or legal rights is a draft for a qualified human to review before it is used.

## Inputs to collect

- What is being retired
- Who uses it, if known
- The replacement, if any
- Contractual constraints the user mentioned

## Workflow


### 1. Why

The reason to retire, in plain language. Cost, risk, or focus. Do not invent usage data.
### 2. Who is affected

Use their data. If you do not know who uses it, the first step is to find out before announcing.
### 3. Path

The replacement or the workaround, including what it does not cover.
### 4. Timeline

Notice, migration window, and removal date that the user can honor. No fake date.
### 5. Support

Who answers migration questions. A sunset email with no owner creates a support incident.
### 6. Commitments

Flag contracts or promises the user says exist, and send those to counsel or account owners. Do not advise breaking a contract.

## Output

Deliver a **sunset plan**.

- Purpose of this sunset plan, in two sentences.
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

Jonah Park, product manager at Fieldnote in Edmonton, needs a sunset plan by 30 September 2026. Engineering wants to delete an API next week that three customers still call.

### Example data

```text
From: Jonah Park, product manager
Organization: Fieldnote, Edmonton
Date: 14 September 2026
Needed by: 30 September 2026

Engineering wants to delete an API next week that three customers still call.

What is being retired: Usage limit warning, last reviewed 14 September 2026. No owner named since
Who uses it, if known: Jonah Park, product manager
The replacement, if any: Activation checklist, recorded 14 September 2026. No supporting file attached
Contractual constraints the user mentioned: no extra headcount, and no result that is not in this file
```

### Example outcome

**Sunset plan**
To: Jonah Park, product manager, Fieldnote
Date: 14 September 2026 · Needed by: 30 September 2026

**Decision**
Blocks the deletion until notice and a migration owner exist, and flags contract questions.

**What the file supports**

| Input | Value | Status |
| --- | --- | --- |
| What is being retired | Usage limit warning, last reviewed 14 September 2026. No owner named since | Needs confirmation |
| Who uses it, if known | Jonah Park, product manager | Carried into the draft |
| The replacement, if any | Activation checklist, recorded 14 September 2026. No supporting file attached | Carried into the draft |
| Contractual constraints the user mentioned | no extra headcount, and no result that is not in this file | Needs confirmation |

**How this draft was built**

**1. Why**  
The reason to retire, in plain language. Cost, risk, or focus. Do not invent usage data.

**2. Who is affected**  
Use their data. If you do not know who uses it, the first step is to find out before announcing.

**3. Path**  
The replacement or the workaround, including what it does not cover.

**4. Timeline**  
Notice, migration window, and removal date that the user can honor. No fake date.

**5. Support**  
Who answers migration questions. A sunset email with no owner creates a support incident.

**Deliberately not done**
- A surprise removal.
- Advising the company to ignore a contract.
- An announcement with no migration path and no owner.

**Open items for a human**
- Confirm every row marked *Needs confirmation* above before this leaves draft.
- Anything absent from the file stayed absent. No figure, date, or name was supplied from outside it.

Next: Jonah Park by 30 September 2026. This is a draft, not a sign-off.

## Anti-patterns

- A surprise removal.
- Advising the company to ignore a contract.
- An announcement with no migration path and no owner.

## Related skills

- `change-leadership`
- `customer-communication-incident`
