---
name: design-system-token
description: "Decide whether a new visual style becomes a token or stays a one-off, based on reuse. Use when the user mentions design token, design system decision, should this be a component, style decision, or asks for a token decision. Design skill by Yasir Jilani."
license: MIT
compatibility: Agent Skills standard. No network access, extra packages, or credentials required.
metadata:
  author: Yasir Jilani
  version: "1.0.0"
  domain: design
---

<!-- GENERATED FILE - edits here are overwritten by scripts/generate.py.
     Edit the 'design-system-token' entry in source/, then run:
       python3 scripts/generate.py && python3 scripts/validate.py
     See CONTRIBUTING.md. -->

# Design Token Decision

Decide whether a new visual style becomes a token or stays a one-off, based on reuse.

## When to use this skill

Use this skill when the user:

- design token
- design system decision
- should this be a component
- style decision

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

- The style in question
- Where it is used
- Existing tokens
- The owner of the system

## Workflow


### 1. Step 1

Count real reuse. One screen does not automatically earn a token.
### 2. Step 2

Match an existing token before adding one.
### 3. Step 3

Name the token by purpose, not by a hex value alone.
### 4. Step 4

Note accessibility contrast as a requirement, not a later wish, when text is involved.
### 5. Step 5

Record who may add tokens.
### 6. Step 6

Do not fork the system in a product file and call it a token.

## Output

Deliver a **token decision**.

- Purpose of this token decision, in two sentences.
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

Lena Ortiz, design lead at Fieldnote in Edmonton, needs a token decision by 30 September 2026. A campaign color is about to become a global brand token after one banner.

### Example data

```text
From: Lena Ortiz, design lead
Organization: Fieldnote, Edmonton
Date: 14 September 2026
Needed by: 30 September 2026

A campaign color is about to become a global brand token after one banner.

The style in question: A campaign color is about to become a global brand token after one banner
Where it is used: Empty-state copy, recorded 14 September 2026. No supporting file attached
Existing tokens: Empty-state copy, last reviewed 14 September 2026. No owner named since
The owner of the system: Lena Ortiz, design lead
```

### Example outcome

**Token decision**
To: Lena Ortiz, design lead, Fieldnote
Date: 14 September 2026 · Needed by: 30 September 2026

**Decision**
Keeps the campaign color local until reuse is real.

**What the file supports**

| Input | Value | Status |
| --- | --- | --- |
| The style in question | A campaign color is about to become a global brand token after one banner | Needs confirmation |
| Where it is used | Empty-state copy, recorded 14 September 2026. No supporting file attached | Carried into the draft |
| Existing tokens | Empty-state copy, last reviewed 14 September 2026. No owner named since | Carried into the draft |
| The owner of the system | Lena Ortiz, design lead | Needs confirmation |

**How this draft was built**

**1. Count real reuse. One screen does not automatically earn a token**

**2. Match an existing token before adding one**

**3. Name the token by purpose, not by a hex value alone**

**4. Note accessibility contrast as a requirement, not a later wish, when text is involved**

**5. Record who may add tokens**

**Deliberately not done**
- A token for a one-off.
- A hex-named token with no purpose.
- A fork called a system.

**Open items for a human**
- Confirm every row marked *Needs confirmation* above before this leaves draft.
- Anything absent from the file stayed absent. No figure, date, or name was supplied from outside it.

Next: Lena Ortiz by 30 September 2026. This is a draft, not a sign-off.

## Anti-patterns

- A token for a one-off
- A hex-named token with no purpose
- A fork called a system

## Related skills

- `design-handoff`
