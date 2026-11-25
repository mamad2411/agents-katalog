---
name: change-order
description: "Brief a change order with the cause, the cost basis they have, and the time effect. Use when the user mentions change order, variation, extra work, construction change, or asks for a change-order brief. Construction skill by Yasir Jilani."
license: MIT
compatibility: Agent Skills standard. No network access, extra packages, or credentials required.
metadata:
  author: Yasir Jilani
  version: "1.0.0"
  domain: construction
---

<!-- GENERATED FILE - edits here are overwritten by scripts/generate.py.
     Edit the 'change-order' entry in source/, then run:
       python3 scripts/generate.py && python3 scripts/validate.py
     See CONTRIBUTING.md. -->

# Change Order Brief

Brief a change order with the cause, the cost basis they have, and the time effect.

## When to use this skill

Use this skill when the user:

- change order
- variation
- extra work
- construction change

## When not to use this skill

- The user wants a different domain's specialist skill.
- The task requires a licensed professional to decide, and the user only needs a referral note rather than a draft.
- The request asks you to deceive, evade a control, or hide material facts.

## Professional boundary

Site safety and contract administration follow the contract and the site rules. Do not tell anyone to skip a safety control. Do not invent quantities.

## Operating boundaries

- Use only information the user provides or files they explicitly ask you to read. Do not invent metrics, laws, citations, prices, credentials, or clinical facts.
- Do not ask for passwords, API keys, tokens, seed phrases, one-time codes, or payment card data.
- Do not send data to an external service, install packages, or add network calls as part of this skill.
- Separate facts, assumptions, and recommendations. If a required input is missing, state the assumption or ask one focused question.
- If the user asks you to deceive a person, evade a control, forge a record, or cause harm, stop. Offer a legitimate alternative.
- Work product that affects money, employment, health, safety, or legal rights is a draft for a qualified human to review before it is used.

## Inputs to collect

- The cause
- Drawings or instructions they have
- Cost backup
- Time effect

## Workflow


### 1. Step 1

State the cause and who directed the work.
### 2. Step 2

Attach cost backup they have. Do not invent unit rates.
### 3. Step 3

Show time effect separately from cost.
### 4. Step 4

Identify contract clauses only if they pasted them.
### 5. Step 5

Mark entitlement as a question for the contract administrator.
### 6. Step 6

Do not advise hiding the change in a contingency with no record.

## Output

Deliver a **change-order brief**.

- Purpose of this change-order brief, in two sentences.
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

Tom Reilly, site lead at Birch Siteworks in Cochrane, needs a change-order brief by 30 September 2026. A superintendent wants a change order with a round number and no backup.

### Example data

```text
From: Tom Reilly, site lead
Organization: Birch Siteworks, Cochrane
Date: 14 September 2026
Needed by: 30 September 2026

A superintendent wants a change order with a round number and no backup.

The cause: Birch site, Cochrane, recorded 14 September 2026. No supporting file attached
Drawings or instructions they have: two deals cited from memory. Neither has a written loss reason
Cost backup: CAD 44 direct. Overhead not in this line
Time effect: five working days, due 30 September 2026
```

### Example outcome

**Change-order brief**
To: Tom Reilly, site lead, Birch Siteworks
Date: 14 September 2026 · Needed by: 30 September 2026

**Decision**
Blocks the round number until backup exists and records the direction to proceed.

**What the file supports**

| Input | Value | Status |
| --- | --- | --- |
| The cause | Birch site, Cochrane, recorded 14 September 2026. No supporting file attached | Needs confirmation |
| Drawings or instructions they have | two deals cited from memory. Neither has a written loss reason | Carried into the draft |
| Cost backup | CAD 44 direct. Overhead not in this line | Carried into the draft |
| Time effect | five working days, due 30 September 2026 | Needs confirmation |

**How this draft was built**

**1. State the cause and who directed the work**

**2. Attach cost backup they have. Do not invent unit rates**

**3. Show time effect separately from cost**

**4. Identify contract clauses only if they pasted them**

**5. Mark entitlement as a question for the contract administrator**

**Deliberately not done**
- Invented rates.
- Hidden changes.
- An entitlement ruling from memory.

**Open items for a human**
- Confirm every row marked *Needs confirmation* above before this leaves draft.
- Anything absent from the file stayed absent. No figure, date, or name was supplied from outside it.

Next: Tom Reilly by 30 September 2026. This is a draft, not a sign-off.

## Anti-patterns

- Invented rates
- Hidden changes
- An entitlement ruling from memory

## Related skills

- `scope-change-control`
- `estimate-assumption-log`
