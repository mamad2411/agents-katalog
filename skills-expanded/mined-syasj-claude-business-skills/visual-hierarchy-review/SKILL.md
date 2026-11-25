---
name: visual-hierarchy-review
description: "Review visual hierarchy so the next action and the key fact win, within the brand constraints they have. Use when the user mentions visual hierarchy, layout review, what should stand out, scan review, or asks for a hierarchy review. Design skill by Yasir Jilani."
license: MIT
compatibility: Agent Skills standard. No network access, extra packages, or credentials required.
metadata:
  author: Yasir Jilani
  version: "1.0.0"
  domain: design
---

<!-- GENERATED FILE - edits here are overwritten by scripts/generate.py.
     Edit the 'visual-hierarchy-review' entry in source/, then run:
       python3 scripts/generate.py && python3 scripts/validate.py
     See CONTRIBUTING.md. -->

# Visual Hierarchy Review

Review visual hierarchy so the next action and the key fact win, within the brand constraints they have.

## When to use this skill

Use this skill when the user:

- visual hierarchy
- layout review
- what should stand out
- scan review

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

- The primary action
- The key fact
- The layout
- Brand constraints

## Workflow


### 1. Step 1

Name the first thing a busy user must see.
### 2. Step 2

Check whether size, position, and contrast support that order, from what you can see.
### 3. Step 3

Demote decorations that compete with the action.
### 4. Step 4

Keep required legal text visible enough to read.
### 5. Step 5

Recommend the smallest change that fixes the order.
### 6. Step 6

Do not restyle the brand for taste.

## Output

Deliver a **hierarchy review**.

- Purpose of this hierarchy review, in two sentences.
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

Lena Ortiz, design lead at Fieldnote in Edmonton, needs a hierarchy review by 30 September 2026. A hero image buries the price and the purchase action.

### Example data

```text
From: Lena Ortiz, design lead
Organization: Fieldnote, Edmonton
Date: 14 September 2026
Needed by: 30 September 2026

A hero image buries the price and the purchase action.

The primary action: Checkout screen v4; Empty-state copy. Both unassigned as of 14 September 2026
The key fact: Checkout screen v4, recorded 14 September 2026. No supporting file attached
The layout: Checkout screen v4, recorded 14 September 2026. No supporting file attached
Brand constraints: no extra headcount, and no result that is not in this file
```

### Example outcome

**Hierarchy review**
To: Lena Ortiz, design lead, Fieldnote
Date: 14 September 2026 · Needed by: 30 September 2026

**Decision**
Brings the price and action forward and leaves the brand system alone.

**What the file supports**

| Input | Value | Status |
| --- | --- | --- |
| The primary action | Checkout screen v4; Empty-state copy. Both unassigned as of 14 September 2026 | Needs confirmation |
| The key fact | Checkout screen v4, recorded 14 September 2026. No supporting file attached | Carried into the draft |
| The layout | Checkout screen v4, recorded 14 September 2026. No supporting file attached | Carried into the draft |
| Brand constraints | no extra headcount, and no result that is not in this file | Needs confirmation |

**How this draft was built**

**1. Name the first thing a busy user must see**

**2. Check whether size, position, and contrast support that order, from what you can see**

**3. Demote decorations that compete with the action**

**4. Keep required legal text visible enough to read**

**5. Recommend the smallest change that fixes the order**

**Deliberately not done**
- A restyle with no hierarchy problem.
- Legal text hidden.
- Decoration competing with the action.

**Open items for a human**
- Confirm every row marked *Needs confirmation* above before this leaves draft.
- Anything absent from the file stayed absent. No figure, date, or name was supplied from outside it.

Next: Lena Ortiz by 30 September 2026. This is a draft, not a sign-off.

## Anti-patterns

- A restyle with no hierarchy problem
- Legal text hidden
- Decoration competing with the action

## Related skills

- `design-critique`
- `landing-page-cro`
