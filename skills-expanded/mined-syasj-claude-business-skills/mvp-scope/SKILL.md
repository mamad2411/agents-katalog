---
name: mvp-scope
description: "Cut a product idea to the smallest test that answers the riskiest question. Use when the user mentions MVP, smallest test, scope the first version, what to build first, or asks for a MVP scope. Entrepreneurship skill by Yasir Jilani."
license: MIT
compatibility: Agent Skills standard. No network access, extra packages, or credentials required.
metadata:
  author: Yasir Jilani
  version: "1.0.0"
  domain: entrepreneurship
---

<!-- GENERATED FILE - edits here are overwritten by scripts/generate.py.
     Edit the 'mvp-scope' entry in source/, then run:
       python3 scripts/generate.py && python3 scripts/validate.py
     See CONTRIBUTING.md. -->

# MVP Scope

Cut a product idea to the smallest test that answers the riskiest question.

## When to use this skill

Use this skill when the user:

- MVP
- smallest test
- scope the first version
- what to build first

## When not to use this skill

- The user wants a different domain's specialist skill.
- The task requires a licensed professional to decide, and the user only needs a referral note rather than a draft.
- The request asks you to deceive, evade a control, or hide material facts.

## Professional boundary

Startup advice is a set of choices, not a promise of funding or growth. Do not invent traction, customers, or investor interest.

## Operating boundaries

- Use only information the user provides or files they explicitly ask you to read. Do not invent metrics, laws, citations, prices, credentials, or clinical facts.
- Do not ask for passwords, API keys, tokens, seed phrases, one-time codes, or payment card data.
- Do not send data to an external service, install packages, or add network calls as part of this skill.
- Separate facts, assumptions, and recommendations. If a required input is missing, state the assumption or ask one focused question.
- If the user asks you to deceive a person, evade a control, forge a record, or cause harm, stop. Offer a legitimate alternative.
- Work product that affects money, employment, health, safety, or legal rights is a draft for a qualified human to review before it is used.

## Inputs to collect

- The riskiest question
- The full idea
- What can be done manually
- The time box

## Workflow


### 1. Step 1

Name the riskiest question. Demand, delivery, or channel.
### 2. Step 2

Cut every feature that does not answer it.
### 3. Step 3

Prefer a manual concierge step over unbuilt software when that answers the question.
### 4. Step 4

State what the MVP must not do.
### 5. Step 5

Define the evidence that would justify the next slice.
### 6. Step 6

Do not call a large roadmap an MVP.

## Output

Deliver a **MVP scope**.

- Purpose of this MVP scope, in two sentences.
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

Mara Chen, founder at Northline Studio in Calgary, needs a MVP scope by 30 September 2026. An MVP list includes billing, admin, and a marketplace before one user has paid.

### Example data

```text
From: Mara Chen, founder
Organization: Northline Studio, Calgary
Date: 14 September 2026
Needed by: 30 September 2026

An MVP list includes billing, admin, and a marketplace before one user has paid.

The riskiest question: First four paying accounts is open. No score in the file
The full idea: An MVP list includes billing, admin, and a marketplace before one user has paid. Stated once, in the ask. Not written down anywhere else
What can be done manually: Landing page test, last reviewed 14 September 2026. No owner named since
The time box: five working days, due 30 September 2026
```

### Example outcome

**Mvp scope**
To: Mara Chen, founder, Northline Studio
Date: 14 September 2026 · Needed by: 30 September 2026

**Decision**
Tests payment or the core job manually and parks the rest.

**What the file supports**

| Input | Value | Status |
| --- | --- | --- |
| The riskiest question | First four paying accounts is open. No score in the file | Needs confirmation |
| The full idea | An MVP list includes billing, admin, and a marketplace before one user has paid. Stated once, in the ask. Not written down anywhere else | Carried into the draft |
| What can be done manually | Landing page test, last reviewed 14 September 2026. No owner named since | Carried into the draft |
| The time box | five working days, due 30 September 2026 | Needs confirmation |

**How this draft was built**

**1. Name the riskiest question. Demand, delivery, or channel**

**2. Cut every feature that does not answer it**

**3. Prefer a manual concierge step over unbuilt software when that answers the question**

**4. State what the MVP must not do**

**5. Define the evidence that would justify the next slice**

**Deliberately not done**
- A roadmap called an MVP.
- Building software before the question is clear.
- No non-goals.

**Open items for a human**
- Confirm every row marked *Needs confirmation* above before this leaves draft.
- Anything absent from the file stayed absent. No figure, date, or name was supplied from outside it.

Next: Mara Chen by 30 September 2026. This is a draft, not a sign-off.

## Anti-patterns

- A roadmap called an MVP
- Building software before the question is clear
- No non-goals

## Related skills

- `prd-writer`
- `experiment-design`
