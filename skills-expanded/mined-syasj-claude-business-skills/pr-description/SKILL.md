---
name: pr-description
description: "Write a pull request description that explains the why, the risk, and how to test. Use when the user mentions PR description, pull request text, write the PR, changelog for a change, or asks for a pull request description. Engineering skill by Yasir Jilani."
license: MIT
compatibility: Agent Skills standard. No network access, extra packages, or credentials required.
metadata:
  author: Yasir Jilani
  version: "1.0.0"
  domain: engineering
---

<!-- GENERATED FILE - edits here are overwritten by scripts/generate.py.
     Edit the 'pr-description' entry in source/, then run:
       python3 scripts/generate.py && python3 scripts/validate.py
     See CONTRIBUTING.md. -->

# Pull Request Description

Write a pull request description that explains the why, the risk, and how to test.

## When to use this skill

Use this skill when the user:

- PR description
- pull request text
- write the PR
- changelog for a change

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

- What changed
- Why
- How to test
- Risks and rollout

## Workflow


### 1. Why

The user or operator problem, not a restatement of the diff.
### 2. What

The approach in a few lines. Point to the design if there is one.
### 3. Test

The steps a reviewer can run, and the cases you did not test.
### 4. Risk

Migrations, flags, and user-visible changes.
### 5. Screens or samples

Only if the user supplied them. Do not invent output.
### 6. Rollback

One line on how to undo the change.

## Output

Deliver a **pull request description**.

- Purpose of this pull request description, in two sentences.
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

Aisha Rahman, engineering lead at Fieldnote in Edmonton, needs a pull request description by 30 September 2026. A PR titled 'updates' changes a payment calculation and the description is empty.

### Example data

```text
From: Aisha Rahman, engineering lead
Organization: Fieldnote, Edmonton
Date: 14 September 2026
Needed by: 30 September 2026

A PR titled 'updates' changes a payment calculation and the description is empty.

What changed: requested 14 September 2026. Not yet approved
Why: A PR titled 'updates' changes a payment calculation and the description is empty
How to test: Invoice job, last reviewed 14 September 2026. No owner named since
Risks and rollout: Checkout service is open. No score in the file
```

### Example outcome

**Pull request description**
To: Aisha Rahman, engineering lead, Fieldnote
Date: 14 September 2026 · Needed by: 30 September 2026

**Decision**
States the payment behavior, the missing test if none was run, and the rollback.

**What the file supports**

| Input | Value | Status |
| --- | --- | --- |
| What changed | requested 14 September 2026. Not yet approved | Needs confirmation |
| Why | A PR titled 'updates' changes a payment calculation and the description is empty | Carried into the draft |
| How to test | Invoice job, last reviewed 14 September 2026. No owner named since | Carried into the draft |
| Risks and rollout | Checkout service is open. No score in the file | Needs confirmation |

**How this draft was built**

**1. Why**  
The user or operator problem, not a restatement of the diff.

**2. What**  
The approach in a few lines. Point to the design if there is one.

**3. Test**  
The steps a reviewer can run, and the cases you did not test.

**4. Risk**  
Migrations, flags, and user-visible changes.

**5. Screens or samples**  
Only if the user supplied them. Do not invent output.

**Deliberately not done**
- A description that says 'fix bug'.
- Claiming tests you did not run.
- Hidden migration risk.

**Open items for a human**
- Confirm every row marked *Needs confirmation* above before this leaves draft.
- Anything absent from the file stayed absent. No figure, date, or name was supplied from outside it.

Next: Aisha Rahman by 30 September 2026. This is a draft, not a sign-off.

## Anti-patterns

- A description that says 'fix bug'.
- Claiming tests you did not run.
- Hidden migration risk.

## Related skills

- `code-review-standard`
- `release-checklist`
