---
name: empty-state-design
description: "Design an empty state that explains why it is empty and offers the next honest action. Use when the user mentions empty state, blank screen, zero data state, first-run screen, or asks for a empty state spec. Design skill by Yasir Jilani."
license: MIT
compatibility: Agent Skills standard. No network access, extra packages, or credentials required.
metadata:
  author: Yasir Jilani
  version: "1.0.0"
  domain: design
---

<!-- GENERATED FILE - edits here are overwritten by scripts/generate.py.
     Edit the 'empty-state-design' entry in source/, then run:
       python3 scripts/generate.py && python3 scripts/validate.py
     See CONTRIBUTING.md. -->

# Empty State Design

Design an empty state that explains why it is empty and offers the next honest action.

## When to use this skill

Use this skill when the user:

- empty state
- blank screen
- zero data state
- first-run screen

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

- Why the screen is empty
- The action a user can take
- What they cannot do yet
- Tone

## Workflow


### 1. Say why the screen is empty

new user, filter, or no permission.
### 2. Step 2

Offer the next action only if it is really available.
### 3. Step 3

Do not fake sample data that looks like the user's own data.
### 4. Step 4

If a filter caused the empty state, show how to clear it.
### 5. Step 5

Keep the tone calm.
### 6. Step 6

Match the empty state to the permission model. Do not invite an action the role cannot perform.

## Output

Deliver a **empty state spec**.

- Purpose of this empty state spec, in two sentences.
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

Lena Ortiz, design lead at Fieldnote in Edmonton, needs an empty state spec by 30 September 2026. A dashboard shows sample revenue that looks like the customer's numbers.

### Example data

```text
From: Lena Ortiz, design lead
Organization: Fieldnote, Edmonton
Date: 14 September 2026
Needed by: 30 September 2026

A dashboard shows sample revenue that looks like the customer's numbers.

Why the screen is empty: A dashboard shows sample revenue that looks like the customer's numbers
The action a user can take: Checkout screen v4; Empty-state copy. Both unassigned as of 14 September 2026
What they cannot do yet: A dashboard shows sample revenue that looks like the customer's numbers
Tone: plain, for people who already know the context. No house guide attached
```

### Example outcome

**Empty state spec**
To: Lena Ortiz, design lead, Fieldnote
Date: 14 September 2026 · Needed by: 30 September 2026

**Decision**
Labels or removes the sample and explains the true empty reason.

**What the file supports**

| Input | Value | Status |
| --- | --- | --- |
| Why the screen is empty | A dashboard shows sample revenue that looks like the customer's numbers | Needs confirmation |
| The action a user can take | Checkout screen v4; Empty-state copy. Both unassigned as of 14 September 2026 | Carried into the draft |
| What they cannot do yet | A dashboard shows sample revenue that looks like the customer's numbers | Carried into the draft |
| Tone | plain, for people who already know the context. No house guide attached | Needs confirmation |

**How this draft was built**

**1. Say why the screen is empty**  
new user, filter, or no permission.

**2. Offer the next action only if it is really available**

**3. Do not fake sample data that looks like the user's own data**

**4. If a filter caused the empty state, show how to clear it**

**5. Keep the tone calm**

**Deliberately not done**
- Fake data that looks real.
- An action the role cannot do.
- An empty screen with no reason.

**Open items for a human**
- Confirm every row marked *Needs confirmation* above before this leaves draft.
- Anything absent from the file stayed absent. No figure, date, or name was supplied from outside it.

Next: Lena Ortiz by 30 September 2026. This is a draft, not a sign-off.

## Anti-patterns

- Fake data that looks real
- An action the role cannot do
- An empty screen with no reason

## Related skills

- `ux-writing`
- `wireframe-spec`
