---
name: churn-interview
description: "Prepare a churn or cancellation interview that learns the real reason without arguing. Use when the user mentions churn interview, cancellation reason, why they left, exit interview customer, or asks for a churn interview. Customer experience skill by Yasir Jilani."
license: MIT
compatibility: Agent Skills standard. No network access, extra packages, or credentials required.
metadata:
  author: Yasir Jilani
  version: "1.0.0"
  domain: customer
---

<!-- GENERATED FILE - edits here are overwritten by scripts/generate.py.
     Edit the 'churn-interview' entry in source/, then run:
       python3 scripts/generate.py && python3 scripts/validate.py
     See CONTRIBUTING.md. -->

# Churn Interview

Prepare a churn or cancellation interview that learns the real reason without arguing.

## When to use this skill

Use this skill when the user:

- churn interview
- cancellation reason
- why they left
- exit interview customer

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

- What you already know
- What the team suspects
- Who will talk
- What remedy is still possible

## Workflow


### 1. Step 1

Open with curiosity, not a save pitch.
### 2. Step 2

Ask about the moment they decided, and what they use instead, if they will say.
### 3. Step 3

Do not argue them out of their reason.
### 4. Step 4

Separate a product gap, a value gap, and a commercial mismatch.
### 5. Step 5

Record the reason in their words.
### 6. Step 6

If a save is allowed, offer it after the reason is understood, and only within policy.

## Output

Deliver a **churn interview**.

- Purpose of this churn interview, in two sentences.
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

Rita Santos, support lead at Fieldnote in Edmonton, needs a churn interview by 30 September 2026. A script opens by telling the customer they are making a mistake.

### Example data

```text
From: Rita Santos, support lead
Organization: Fieldnote, Edmonton
Date: 14 September 2026
Needed by: 30 September 2026

A script opens by telling the customer they are making a mistake.

What you already know: Ticket 4420, last reviewed 14 September 2026. No owner named since
What the team suspects: two people on shift, one off
Who will talk: Rita Santos, support lead
What remedy is still possible: Ticket 4420, last reviewed 14 September 2026. No owner named since
```

### Example outcome

**Churn interview**
To: Rita Santos, support lead, Fieldnote
Date: 14 September 2026 · Needed by: 30 September 2026

**Decision**
Asks for the decision moment first and holds any save offer until after.

**What the file supports**

| Input | Value | Status |
| --- | --- | --- |
| What you already know | Ticket 4420, last reviewed 14 September 2026. No owner named since | Needs confirmation |
| What the team suspects | two people on shift, one off | Carried into the draft |
| Who will talk | Rita Santos, support lead | Carried into the draft |
| What remedy is still possible | Ticket 4420, last reviewed 14 September 2026. No owner named since | Needs confirmation |

**How this draft was built**

**1. Open with curiosity, not a save pitch**

**2. Ask about the moment they decided, and what they use instead, if they will say**

**3. Do not argue them out of their reason**

**4. Separate a product gap, a value gap, and a commercial mismatch**

**5. Record the reason in their words**

**Deliberately not done**
- Arguing with the reason.
- A save offer before listening.
- Inventing the replacement they chose.

**Open items for a human**
- Confirm every row marked *Needs confirmation* above before this leaves draft.
- Anything absent from the file stayed absent. No figure, date, or name was supplied from outside it.

Next: Rita Santos by 30 September 2026. This is a draft, not a sign-off.

## Anti-patterns

- Arguing with the reason
- A save offer before listening
- Inventing the replacement they chose

## Related skills

- `renewal-save`
- `feedback-synthesis`
