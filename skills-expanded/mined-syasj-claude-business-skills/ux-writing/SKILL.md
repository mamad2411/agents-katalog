---
name: ux-writing
description: "Write interface copy that tells the user what happened, what to do, and what they are committing to. Use when the user mentions UX writing, microcopy, button label, empty state copy, or asks for a interface copy. Design skill by Yasir Jilani."
license: MIT
compatibility: Agent Skills standard. No network access, extra packages, or credentials required.
metadata:
  author: Yasir Jilani
  version: "1.0.0"
  domain: design
---

<!-- GENERATED FILE - edits here are overwritten by scripts/generate.py.
     Edit the 'ux-writing' entry in source/, then run:
       python3 scripts/generate.py && python3 scripts/validate.py
     See CONTRIBUTING.md. -->

# UX Writing

Write interface copy that tells the user what happened, what to do, and what they are committing to.

## When to use this skill

Use this skill when the user:

- UX writing
- microcopy
- button label
- empty state copy
- error message

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

- The user action
- The system state
- The tone guide if any
- Legal lines they must include

## Workflow


### 1. Step 1

Label the action as the outcome, not as OK, when the outcome matters.
### 2. Step 2

Error text says what went wrong and how to fix it, if known.
### 3. Step 3

Empty states teach the next action.
### 4. Step 4

Commitment moments state the consequence before the click.
### 5. Step 5

Use their required legal line verbatim. Do not invent one.
### 6. Step 6

Cut cleverness that hides meaning.

## Output

Deliver a **interface copy**.

- Purpose of this interface copy, in two sentences.
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

Lena Ortiz, design lead at Fieldnote in Edmonton, needs an interface copy by 30 September 2026. A delete dialog says 'Let's do this' and does not name the deletion.

### Example data

```text
From: Lena Ortiz, design lead
Organization: Fieldnote, Edmonton
Date: 14 September 2026
Needed by: 30 September 2026

A delete dialog says 'Let's do this' and does not name the deletion.

The user action: Checkout screen v4; Empty-state copy. Both unassigned as of 14 September 2026
The system state: the one named in the ask. Version and owner not recorded
The tone guide if any: plain, for people who already know the context. No house guide attached
Legal lines they must include: Colour contrast audit and one other, both unconfirmed as of 14 September 2026
```

### Example outcome

**Interface copy**
To: Lena Ortiz, design lead, Fieldnote
Date: 14 September 2026 · Needed by: 30 September 2026

**Decision**
Copy that names the deletion and the consequence before confirm.

**What the file supports**

| Input | Value | Status |
| --- | --- | --- |
| The user action | Checkout screen v4; Empty-state copy. Both unassigned as of 14 September 2026 | Needs confirmation |
| The system state | the one named in the ask. Version and owner not recorded | Carried into the draft |
| The tone guide if any | plain, for people who already know the context. No house guide attached | Carried into the draft |
| Legal lines they must include | Colour contrast audit and one other, both unconfirmed as of 14 September 2026 | Needs confirmation |

**How this draft was built**

**1. Label the action as the outcome, not as OK, when the outcome matters**

**2. Error text says what went wrong and how to fix it, if known**

**3. Empty states teach the next action**

**4. Commitment moments state the consequence before the click**

**5. Use their required legal line verbatim. Do not invent one**

**Deliberately not done**
- An OK button on a destructive action.
- Cute error text with no fix.
- Invented legal lines.

**Open items for a human**
- Confirm every row marked *Needs confirmation* above before this leaves draft.
- Anything absent from the file stayed absent. No figure, date, or name was supplied from outside it.

Next: Lena Ortiz by 30 September 2026. This is a draft, not a sign-off.

## Anti-patterns

- An OK button on a destructive action
- Cute error text with no fix
- Invented legal lines

## Related skills

- `brand-voice-guide`
- `empty-state-design`
