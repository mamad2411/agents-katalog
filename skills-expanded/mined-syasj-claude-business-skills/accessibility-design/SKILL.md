---
name: accessibility-design
description: "Review a design for access barriers before build, without issuing a conformance certificate. Use when the user mentions accessibility design, a11y design review, inclusive design review, contrast and focus, or asks for a accessibility design note. Design skill by Yasir Jilani."
license: MIT
compatibility: Agent Skills standard. No network access, extra packages, or credentials required.
metadata:
  author: Yasir Jilani
  version: "1.0.0"
  domain: design
---

<!-- GENERATED FILE - edits here are overwritten by scripts/generate.py.
     Edit the 'accessibility-design' entry in source/, then run:
       python3 scripts/generate.py && python3 scripts/validate.py
     See CONTRIBUTING.md. -->

# Accessibility Design Review

Review a design for access barriers before build, without issuing a conformance certificate.

## When to use this skill

Use this skill when the user:

- accessibility design
- a11y design review
- inclusive design review
- contrast and focus

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

- The flow
- Text and controls
- Known barriers
- The target they claim

## Workflow


### 1. Step 1

Check the flow for keyboard order, names, and focus as far as the mock shows.
### 2. Step 2

Flag text that will fail contrast if the values are visible. Do not invent a pass.
### 3. Step 3

Error identification must not depend on color alone.
### 4. Step 4

Touch and target size are noted if they specified a platform.
### 5. Step 5

Write fixes a designer can make now.
### 6. Step 6

Do not claim WCAG conformance from a visual review.

## Output

Deliver a **accessibility design note**.

- Purpose of this accessibility design note, in two sentences.
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

Lena Ortiz, design lead at Fieldnote in Edmonton, needs an accessibility design note by 30 September 2026. A mock uses placeholder color as the only label.

### Example data

```text
From: Lena Ortiz, design lead
Organization: Fieldnote, Edmonton
Date: 14 September 2026
Needed by: 30 September 2026

A mock uses placeholder color as the only label.

The flow: the one named in the ask. Version and owner not recorded
Text and controls: their one-page rule dated 2 Mar 2026. No exception log since
Known barriers: Checkout screen v4 is open. Empty-state copy was raised verbally and never logged
The target they claim: 140
```

### Example outcome

**Accessibility design note**
To: Lena Ortiz, design lead, Fieldnote
Date: 14 September 2026 · Needed by: 30 September 2026

**Decision**
Requires a visible label and refuses a conformance claim.

**What the file supports**

| Input | Value | Status |
| --- | --- | --- |
| The flow | the one named in the ask. Version and owner not recorded | Needs confirmation |
| Text and controls | their one-page rule dated 2 Mar 2026. No exception log since | Carried into the draft |
| Known barriers | Checkout screen v4 is open. Empty-state copy was raised verbally and never logged | Carried into the draft |
| The target they claim | 140 | Needs confirmation |

**How this draft was built**

**1. Check the flow for keyboard order, names, and focus as far as the mock shows**

**2. Flag text that will fail contrast if the values are visible. Do not invent a pass**

**3. Error identification must not depend on color alone**

**4. Touch and target size are noted if they specified a platform**

**5. Write fixes a designer can make now**

**Deliberately not done**
- A conformance badge from a glance.
- Errors shown by color only.
- No focus order on a custom control.

**Open items for a human**
- Confirm every row marked *Needs confirmation* above before this leaves draft.
- Anything absent from the file stayed absent. No figure, date, or name was supplied from outside it.

Next: Lena Ortiz by 30 September 2026. This is a draft, not a sign-off.

## Anti-patterns

- A conformance badge from a glance
- Errors shown by color only
- No focus order on a custom control

## Related skills

- `accessibility-review`
- `design-critique`
