---
name: refactor-plan
description: "Plan a refactor that improves a named risk without pretending a rewrite is free. Use when the user mentions refactor plan, rewrite versus refactor, pay down this code, code health plan, or asks for a refactor plan. Engineering skill by Yasir Jilani."
license: MIT
compatibility: Agent Skills standard. No network access, extra packages, or credentials required.
metadata:
  author: Yasir Jilani
  version: "1.0.0"
  domain: engineering
---

<!-- GENERATED FILE - edits here are overwritten by scripts/generate.py.
     Edit the 'refactor-plan' entry in source/, then run:
       python3 scripts/generate.py && python3 scripts/validate.py
     See CONTRIBUTING.md. -->

# Refactor Plan

Plan a refactor that improves a named risk without pretending a rewrite is free.

## When to use this skill

Use this skill when the user:

- refactor plan
- rewrite versus refactor
- pay down this code
- code health plan

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

- The pain: bugs, change fear, or incidents
- The boundaries of the code
- Tests that exist
- Deadline pressure

## Workflow


### 1. Pain

The user-visible or developer-visible pain. 'It is ugly' is not enough unless change is slow or risky because of it.
### 2. Characterize

What the code does, from tests or the user's description. Do not refactor behavior you cannot name.
### 3. Safety

Tests or characterization checks to add first. A refactor without a safety net is a rewrite in the dark.
### 4. Slices

Small steps that keep the system shipping. A big-bang rewrite needs a written reason and a rollback.
### 5. Non-goals

Behavior you will not change. Call out any behavior change as a product decision.
### 6. Stop

When the pain is reduced enough to return to product work.

## Output

Deliver a **refactor plan**.

- Purpose of this refactor plan, in two sentences.
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

Aisha Rahman, engineering lead at Fieldnote in Edmonton, needs a refactor plan by 30 September 2026. An engineer wants six weeks to rewrite a billing module before adding a small fee change.

### Example data

```text
From: Aisha Rahman, engineering lead
Organization: Fieldnote, Edmonton
Date: 14 September 2026
Needed by: 30 September 2026

An engineer wants six weeks to rewrite a billing module before adding a small fee change.

The pain: bugs, change fear, or incidents: bugs: in the file; change fear: not in the file; incidents: open
The boundaries of the code: Checkout service, recorded 14 September 2026. No supporting file attached
Tests that exist: Status page, recorded 14 September 2026. No supporting file attached
Deadline pressure: 30 September 2026
```

### Example outcome

**Refactor plan**
To: Aisha Rahman, engineering lead, Fieldnote
Date: 14 September 2026 · Needed by: 30 September 2026

**Decision**
Adds characterization tests and a smaller slice that unblocks the fee change, and treats a full rewrite as a separate decision.

**What the file supports**

| Input | Value | Status |
| --- | --- | --- |
| The pain: bugs, change fear, or incidents | bugs: in the file; change fear: not in the file; incidents: open | Needs confirmation |
| The boundaries of the code | Checkout service, recorded 14 September 2026. No supporting file attached | Carried into the draft |
| Tests that exist | Status page, recorded 14 September 2026. No supporting file attached | Carried into the draft |
| Deadline pressure | 30 September 2026 | Needs confirmation |

**How this draft was built**

**1. Pain**  
The user-visible or developer-visible pain. 'It is ugly' is not enough unless change is slow or risky because of it.

**2. Characterize**  
What the code does, from tests or the user's description. Do not refactor behavior you cannot name.

**3. Safety**  
Tests or characterization checks to add first. A refactor without a safety net is a rewrite in the dark.

**4. Slices**  
Small steps that keep the system shipping. A big-bang rewrite needs a written reason and a rollback.

**5. Non-goals**  
Behavior you will not change. Call out any behavior change as a product decision.

**Deliberately not done**
- A rewrite because the code is old.
- Refactoring with no tests and no characterization.
- Sneaking behavior changes into a refactor.

**Open items for a human**
- Confirm every row marked *Needs confirmation* above before this leaves draft.
- Anything absent from the file stayed absent. No figure, date, or name was supplied from outside it.

Next: Aisha Rahman by 30 September 2026. This is a draft, not a sign-off.

## Anti-patterns

- A rewrite because the code is old.
- Refactoring with no tests and no characterization.
- Sneaking behavior changes into a refactor.

## Related skills

- `tech-debt-triage`
- `test-strategy`
