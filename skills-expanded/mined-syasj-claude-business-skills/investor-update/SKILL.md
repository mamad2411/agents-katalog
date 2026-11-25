---
name: investor-update
description: "Draft an investor update that leads with cash, the metric, and the ask, without spin. Use when the user mentions investor update, shareholder update, monthly investor note, fundraising update, or asks for a investor update. Entrepreneurship skill by Yasir Jilani."
license: MIT
compatibility: Agent Skills standard. No network access, extra packages, or credentials required.
metadata:
  author: Yasir Jilani
  version: "1.0.0"
  domain: entrepreneurship
---

<!-- GENERATED FILE - edits here are overwritten by scripts/generate.py.
     Edit the 'investor-update' entry in source/, then run:
       python3 scripts/generate.py && python3 scripts/validate.py
     See CONTRIBUTING.md. -->

# Investor Update

Draft an investor update that leads with cash, the metric, and the ask, without spin.

## When to use this skill

Use this skill when the user:

- investor update
- shareholder update
- monthly investor note
- fundraising update

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

- Cash and runway facts
- The metric they track
- What went wrong
- The ask

## Workflow


### 1. Step 1

Lead with cash, runway, and the metric, from their books.
### 2. Step 2

Include the miss. Investors who hear only good news stop trusting the note.
### 3. Step 3

One ask, if any, with a date.
### 4. Step 4

Do not invent a term, a valuation, or interest from other investors.
### 5. Step 5

Keep customer names out unless the user may share them.
### 6. Step 6

Mark forecasts as forecasts.

## Output

Deliver a **investor update**.

- Purpose of this investor update, in two sentences.
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

Mara Chen, founder at Northline Studio in Calgary, needs an investor update by 30 September 2026. An update omits a churn spike because the round is opening.

### Example data

```text
From: Mara Chen, founder
Organization: Northline Studio, Calgary
Date: 14 September 2026
Needed by: 30 September 2026

An update omits a churn spike because the round is opening.

Cash and runway facts: Landing page test. Partly documented: the what is written down, the who is not
The metric they track: plan 160, actual 75
What went wrong: Landing page test, last reviewed 14 September 2026. No owner named since
The ask: An update omits a churn spike because the round is opening. Stated once, in the ask. Not written down anywhere else
```

### Example outcome

**Investor update**
To: Mara Chen, founder, Northline Studio
Date: 14 September 2026 · Needed by: 30 September 2026

**Decision**
Includes the spike, the cash fact, and no invented investor interest.

**What the file supports**

| Input | Value | Status |
| --- | --- | --- |
| Cash and runway facts | Landing page test. Partly documented: the what is written down, the who is not | Needs confirmation |
| The metric they track | plan 160, actual 75 | Carried into the draft |
| What went wrong | Landing page test, last reviewed 14 September 2026. No owner named since | Carried into the draft |
| The ask | An update omits a churn spike because the round is opening. Stated once, in the ask. Not written down anywhere else | Needs confirmation |

**How this draft was built**

**1. Lead with cash, runway, and the metric, from their books**

**2. Include the miss. Investors who hear only good news stop trusting the note**

**3. One ask, if any, with a date**

**4. Do not invent a term, a valuation, or interest from other investors**

**5. Keep customer names out unless the user may share them**

**Deliberately not done**
- Invented investor interest.
- A hidden miss.
- A valuation presented as fact.

**Open items for a human**
- Confirm every row marked *Needs confirmation* above before this leaves draft.
- Anything absent from the file stayed absent. No figure, date, or name was supplied from outside it.

Next: Mara Chen by 30 September 2026. This is a draft, not a sign-off.

## Anti-patterns

- Invented investor interest
- A hidden miss
- A valuation presented as fact

## Related skills

- `fundraising-model`
- `runway-and-burn`
