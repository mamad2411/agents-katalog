---
name: test-strategy
description: "Choose a test strategy for a change that matches risk, instead of demanding every kind of test. Use when the user mentions test strategy, what tests do we need, test plan, coverage argument, or asks for a test strategy note. Engineering skill by Yasir Jilani."
license: MIT
compatibility: Agent Skills standard. No network access, extra packages, or credentials required.
metadata:
  author: Yasir Jilani
  version: "1.0.0"
  domain: engineering
---

<!-- GENERATED FILE - edits here are overwritten by scripts/generate.py.
     Edit the 'test-strategy' entry in source/, then run:
       python3 scripts/generate.py && python3 scripts/validate.py
     See CONTRIBUTING.md. -->

# Test Strategy

Choose a test strategy for a change that matches risk, instead of demanding every kind of test.

## When to use this skill

Use this skill when the user:

- test strategy
- what tests do we need
- test plan
- coverage argument

## When not to use this skill

- The user wants a different domain's specialist skill.
- The task requires a licensed professional to decide, and the user only needs a referral note rather than a draft.
- The request asks you to deceive, evade a control, or hide material facts.

## Professional boundary

Prefer the repository's existing patterns. Do not disable security controls, invent credentials, or introduce network calls the user did not ask for.

## Operating boundaries

- Use only information the user provides or files they explicitly ask you to read. Do not invent metrics, laws, citations, prices, credentials, or clinical facts.
- Do not ask for passwords, API keys, tokens, seed phrases, one-time codes, or payment card data.
- Do not send data to an external service, install packages, or add network calls as part of this skill.
- Separate facts, assumptions, and recommendations. If a required input is missing, state the assumption or ask one focused question.
- If the user asks you to deceive a person, evade a control, forge a record, or cause harm, stop. Offer a legitimate alternative.
- Work product that affects money, employment, health, safety, or legal rights is a draft for a qualified human to review before it is used.

## Inputs to collect

- The change and its risk
- Existing tests
- What has broken before
- Time available

## Workflow


### 1. Risk

Where a bug would hurt users, money, or data. Tests follow risk.
### 2. Layer

Unit, integration, or end-to-end, chosen for the risk. Do not demand an end-to-end test for a pure function by reflex.
### 3. Gaps

The specific case that is untested. Name it.
### 4. Flakes

Do not add a known-flaky test as the only safety net. Say so.
### 5. Non-goals

What you will not automate now, and why.
### 6. Done

The test list that would make the change reviewable.

## Output

Deliver a **test strategy note**.

- Purpose of this test strategy note, in two sentences.
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

Aisha Rahman, engineering lead at Fieldnote in Edmonton, needs a test strategy note by 30 September 2026. A team argues about coverage percent while a refund path has no test.

### Example data

```text
From: Aisha Rahman, engineering lead
Organization: Fieldnote, Edmonton
Date: 14 September 2026
Needed by: 30 September 2026

A team argues about coverage percent while a refund path has no test.

The change and its risk: Checkout service is open. No score in the file
Existing tests: Invoice job, last reviewed 14 September 2026. No owner named since
What has broken before: Status page, last reviewed 14 September 2026. No owner named since
Time available: five working days, due 30 September 2026
```

### Example outcome

**Test strategy note**
To: Aisha Rahman, engineering lead, Fieldnote
Date: 14 September 2026 · Needed by: 30 September 2026

**Decision**
Prioritizes the refund path and treats the coverage number as secondary.

**What the file supports**

| Input | Value | Status |
| --- | --- | --- |
| The change and its risk | Checkout service is open. No score in the file | Needs confirmation |
| Existing tests | Invoice job, last reviewed 14 September 2026. No owner named since | Carried into the draft |
| What has broken before | Status page, last reviewed 14 September 2026. No owner named since | Carried into the draft |
| Time available | five working days, due 30 September 2026 | Needs confirmation |

**How this draft was built**

**1. Risk**  
Where a bug would hurt users, money, or data. Tests follow risk.

**2. Layer**  
Unit, integration, or end-to-end, chosen for the risk. Do not demand an end-to-end test for a pure function by reflex.

**3. Gaps**  
The specific case that is untested. Name it.

**4. Flakes**  
Do not add a known-flaky test as the only safety net. Say so.

**5. Non-goals**  
What you will not automate now, and why.

**Deliberately not done**
- Coverage percentage as the goal.
- A flaky end-to-end test as the only check.
- No test on a payments or auth change.

**Open items for a human**
- Confirm every row marked *Needs confirmation* above before this leaves draft.
- Anything absent from the file stayed absent. No figure, date, or name was supplied from outside it.

Next: Aisha Rahman by 30 September 2026. This is a draft, not a sign-off.

## Anti-patterns

- Coverage percentage as the goal.
- A flaky end-to-end test as the only check.
- No test on a payments or auth change.

## Related skills

- `code-review-standard`
- `definition-of-done`
