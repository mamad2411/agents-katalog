---
name: decision-journal
description: "Write a personal decision journal entry with the choice, the expectation, and a review date. Use when the user mentions decision journal, log my decision, decision diary, review a past decision, or asks for a decision journal entry. Productivity skill by Yasir Jilani."
license: MIT
compatibility: Agent Skills standard. No network access, extra packages, or credentials required.
metadata:
  author: Yasir Jilani
  version: "1.0.0"
  domain: productivity
---

<!-- GENERATED FILE - edits here are overwritten by scripts/generate.py.
     Edit the 'decision-journal' entry in source/, then run:
       python3 scripts/generate.py && python3 scripts/validate.py
     See CONTRIBUTING.md. -->

# Decision Journal

Write a personal decision journal entry with the choice, the expectation, and a review date.

## When to use this skill

Use this skill when the user:

- decision journal
- log my decision
- decision diary
- review a past decision

## When not to use this skill

- The user wants a different domain's specialist skill.
- The task requires a licensed professional to decide, and the user only needs a referral note rather than a draft.
- The request asks you to deceive, evade a control, or hide material facts.

## Professional boundary

Productivity systems serve the person's actual constraints. Do not recommend surveillance of colleagues or hidden monitoring.

## Operating boundaries

- Use only information the user provides or files they explicitly ask you to read. Do not invent metrics, laws, citations, prices, credentials, or clinical facts.
- Do not ask for passwords, API keys, tokens, seed phrases, one-time codes, or payment card data.
- Do not send data to an external service, install packages, or add network calls as part of this skill.
- Separate facts, assumptions, and recommendations. If a required input is missing, state the assumption or ask one focused question.
- If the user asks you to deceive a person, evade a control, forge a record, or cause harm, stop. Offer a legitimate alternative.
- Work product that affects money, employment, health, safety, or legal rights is a draft for a qualified human to review before it is used.

## Inputs to collect

- The decision
- Options
- What you expect to happen
- The review date

## Workflow


### 1. Step 1

State the decision and the date.
### 2. Step 2

Record the expectation in a way you can later check.
### 3. Step 3

Note the main uncertainty.
### 4. Step 4

Do not rewrite the entry after the outcome to look wiser.
### 5. Step 5

On review, compare expectation to what happened.
### 6. Step 6

Extract one rule, or explicitly say there is no rule yet.

## Output

Deliver a **decision journal entry**.

- Purpose of this decision journal entry, in two sentences.
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

Mara Chen, founder at Northline Studio in Calgary, needs a decision journal entry by 30 September 2026. A journal entry is edited after a failure to say the risk was always obvious.

### Example data

```text
From: Mara Chen, founder
Organization: Northline Studio, Calgary
Date: 14 September 2026
Needed by: 30 September 2026

A journal entry is edited after a failure to say the risk was always obvious.

The decision: A journal entry is edited after a failure to say the risk was always obvious
Options: keep Friday review block, or stop. No third option written
What you expect to happen: Q4 objective 2, last reviewed 14 September 2026. No owner named since
The review date: 30 September 2026
```

### Example outcome

**Decision journal entry**
To: Mara Chen, founder, Northline Studio
Date: 14 September 2026 · Needed by: 30 September 2026

**Decision**
Keeps the original expectation and sets a review without rewriting the past.

**What the file supports**

| Input | Value | Status |
| --- | --- | --- |
| The decision | A journal entry is edited after a failure to say the risk was always obvious | Needs confirmation |
| Options | keep Friday review block, or stop. No third option written | Carried into the draft |
| What you expect to happen | Q4 objective 2, last reviewed 14 September 2026. No owner named since | Carried into the draft |
| The review date | 30 September 2026 | Needs confirmation |

**How this draft was built**

**1. State the decision and the date**

**2. Record the expectation in a way you can later check**

**3. Note the main uncertainty**

**4. Do not rewrite the entry after the outcome to look wiser**

**5. On review, compare expectation to what happened**

**Deliberately not done**
- Rewriting history.
- An entry with no expectation.
- A rule from one case.

**Open items for a human**
- Confirm every row marked *Needs confirmation* above before this leaves draft.
- Anything absent from the file stayed absent. No figure, date, or name was supplied from outside it.

Next: Mara Chen by 30 September 2026. This is a draft, not a sign-off.

## Anti-patterns

- Rewriting history
- An entry with no expectation
- A rule from one case

## Related skills

- `decision-log`
- `founder-decision-review`
