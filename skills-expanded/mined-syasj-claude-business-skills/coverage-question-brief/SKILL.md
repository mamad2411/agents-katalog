---
name: coverage-question-brief
description: "Brief a coverage question for a licensed professional, with the policy words the user supplied. Use when the user mentions coverage question, does this policy cover, insurance interpretation, coverage brief, or asks for a coverage brief. Insurance operations skill by Yasir Jilani."
license: MIT
compatibility: Agent Skills standard. No network access, extra packages, or credentials required.
metadata:
  author: Yasir Jilani
  version: "1.0.0"
  domain: insurance
---

<!-- GENERATED FILE - edits here are overwritten by scripts/generate.py.
     Edit the 'coverage-question-brief' entry in source/, then run:
       python3 scripts/generate.py && python3 scripts/validate.py
     See CONTRIBUTING.md. -->

# Coverage Question Brief

Brief a coverage question for a licensed professional, with the policy words the user supplied.

## When to use this skill

Use this skill when the user:

- coverage question
- does this policy cover
- insurance interpretation
- coverage brief

## When not to use this skill

- The user wants a different domain's specialist skill.
- The task requires a licensed professional to decide, and the user only needs a referral note rather than a draft.
- The request asks you to deceive, evade a control, or hide material facts.

## Professional boundary

This is not coverage advice and not a claim determination. Do not tell anyone they are covered. Organize facts for a licensed professional.

## Operating boundaries

- Use only information the user provides or files they explicitly ask you to read. Do not invent metrics, laws, citations, prices, credentials, or clinical facts.
- Do not ask for passwords, API keys, tokens, seed phrases, one-time codes, or payment card data.
- Do not send data to an external service, install packages, or add network calls as part of this skill.
- Separate facts, assumptions, and recommendations. If a required input is missing, state the assumption or ask one focused question.
- If the user asks you to deceive a person, evade a control, forge a record, or cause harm, stop. Offer a legitimate alternative.
- Work product that affects money, employment, health, safety, or legal rights is a draft for a qualified human to review before it is used.

## Inputs to collect

- The question
- The policy words they pasted
- The facts
- The licensed reviewer

## Workflow


### 1. Step 1

Quote the policy words they supplied.
### 2. Step 2

State the facts.
### 3. Step 3

List the question for the licensed reviewer.
### 4. Step 4

Do not say the person is covered or not covered.
### 5. Step 5

If the policy text is missing, stop.
### 6. Step 6

Do not invent an endorsement.

## Output

Deliver a **coverage brief**.

- Purpose of this coverage brief, in two sentences.
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

Priya Shah, controller at Northline Studio in Calgary, needs a coverage brief by 30 September 2026. A colleague wants a firm yes on flood coverage from a brochure.

### Example data

```text
From: Priya Shah, controller
Organization: Northline Studio, Calgary
Date: 14 September 2026
Needed by: 30 September 2026

A colleague wants a firm yes on flood coverage from a brochure.

The question: A colleague wants a firm yes on flood coverage from a brochure
The policy words they pasted: their one-page rule dated 2 Mar 2026. No exception log
The facts: Claim file 8841, recorded 14 September 2026. No supporting file attached
The licensed reviewer: Priya Shah. No second reviewer named
```

### Example outcome

**Coverage brief**
To: Priya Shah, controller, Northline Studio
Date: 14 September 2026 · Needed by: 30 September 2026

**Decision**
Refuses the yes and asks for the policy form instead of the brochure.

**What the file supports**

| Input | Value | Status |
| --- | --- | --- |
| The question | A colleague wants a firm yes on flood coverage from a brochure | Needs confirmation |
| The policy words they pasted | their one-page rule dated 2 Mar 2026. No exception log | Carried into the draft |
| The facts | Claim file 8841, recorded 14 September 2026. No supporting file attached | Carried into the draft |
| The licensed reviewer | Priya Shah. No second reviewer named | Needs confirmation |

**How this draft was built**

**1. Quote the policy words they supplied**

**2. State the facts**

**3. List the question for the licensed reviewer**

**4. Do not say the person is covered or not covered**

**5. If the policy text is missing, stop**

**Deliberately not done**
- A coverage yes or no.
- An invented endorsement.
- A brief without the policy words.

**Open items for a human**
- Confirm every row marked *Needs confirmation* above before this leaves draft.
- Anything absent from the file stayed absent. No figure, date, or name was supplied from outside it.

Next: Priya Shah by 30 September 2026. This is a draft, not a sign-off.

## Anti-patterns

- A coverage yes or no
- An invented endorsement
- A brief without the policy words

## Related skills

- `claim-file-checklist`
- `contract-risk-review`
