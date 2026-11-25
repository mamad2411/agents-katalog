---
name: wireframe-spec
description: "Specify a wireframe's structure, priority, and states so visual design does not have to guess. Use when the user mentions wireframe spec, low fidelity spec, screen structure, UX spec, or asks for a wireframe specification. Design skill by Yasir Jilani."
license: MIT
compatibility: Agent Skills standard. No network access, extra packages, or credentials required.
metadata:
  author: Yasir Jilani
  version: "1.0.0"
  domain: design
---

<!-- GENERATED FILE - edits here are overwritten by scripts/generate.py.
     Edit the 'wireframe-spec' entry in source/, then run:
       python3 scripts/generate.py && python3 scripts/validate.py
     See CONTRIBUTING.md. -->

# Wireframe Spec

Specify a wireframe's structure, priority, and states so visual design does not have to guess.

## When to use this skill

Use this skill when the user:

- wireframe spec
- low fidelity spec
- screen structure
- UX spec

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

- The task
- The content priority
- States: empty, error, success
- Constraints

## Workflow


### 1. Step 1

Order content by the decision on the screen.
### 2. Step 2

Specify primary and secondary actions.
### 3. Step 3

Include empty, loading, and error states. A happy path only is incomplete.
### 4. Step 4

Note what data is required. Do not invent personal data in examples.
### 5. Step 5

Mark open questions.
### 6. Step 6

Hand off the job of the screen, not a prescription of every pixel, unless the user asked for visual design.

## Output

Deliver a **wireframe specification**.

- Purpose of this wireframe specification, in two sentences.
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

Lena Ortiz, design lead at Fieldnote in Edmonton, needs a wireframe specification by 30 September 2026. A wireframe shows a full dashboard and no empty state for a new account.

### Example data

```text
From: Lena Ortiz, design lead
Organization: Fieldnote, Edmonton
Date: 14 September 2026
Needed by: 30 September 2026

A wireframe shows a full dashboard and no empty state for a new account.

The task: A wireframe shows a full dashboard and no empty state for a new account. Stated once, in the ask. Not written down anywhere else
The content priority: Checkout screen v4, recorded 14 September 2026. No supporting file attached
States: empty, error, success: empty: in the file; error: not in the file; success: open
Constraints: no extra headcount, and no result that is not in this file
```

### Example outcome

**Wireframe specification**
To: Lena Ortiz, design lead, Fieldnote
Date: 14 September 2026 · Needed by: 30 September 2026

**Decision**
Adds the empty state and names the primary action.

**What the file supports**

| Input | Value | Status |
| --- | --- | --- |
| The task | A wireframe shows a full dashboard and no empty state for a new account. Stated once, in the ask. Not written down anywhere else | Needs confirmation |
| The content priority | Checkout screen v4, recorded 14 September 2026. No supporting file attached | Carried into the draft |
| States: empty, error, success | empty: in the file; error: not in the file; success: open | Carried into the draft |
| Constraints | no extra headcount, and no result that is not in this file | Needs confirmation |

**How this draft was built**

**1. Order content by the decision on the screen**

**2. Specify primary and secondary actions**

**3. Include empty, loading, and error states. A happy path only is incomplete**

**4. Note what data is required. Do not invent personal data in examples**

**5. Mark open questions**

**Deliberately not done**
- A happy path only.
- Fake personal data in the example.
- No primary action.

**Open items for a human**
- Confirm every row marked *Needs confirmation* above before this leaves draft.
- Anything absent from the file stayed absent. No figure, date, or name was supplied from outside it.

Next: Lena Ortiz by 30 September 2026. This is a draft, not a sign-off.

## Anti-patterns

- A happy path only
- Fake personal data in the example
- No primary action

## Related skills

- `empty-state-design`
- `design-handoff`
