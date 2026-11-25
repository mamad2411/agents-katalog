---
name: migration-plan
description: "Plan a migration from one system or contract to another with a dual-run, a cutover, and a backout. Use when the user mentions migration plan, cutover plan, move off this system, contract migration, or asks for a migration plan. Engineering skill by Yasir Jilani."
license: MIT
compatibility: Agent Skills standard. No network access, extra packages, or credentials required.
metadata:
  author: Yasir Jilani
  version: "1.0.0"
  domain: engineering
---

<!-- GENERATED FILE - edits here are overwritten by scripts/generate.py.
     Edit the 'migration-plan' entry in source/, then run:
       python3 scripts/generate.py && python3 scripts/validate.py
     See CONTRIBUTING.md. -->

# Migration Plan

Plan a migration from one system or contract to another with a dual-run, a cutover, and a backout.

## When to use this skill

Use this skill when the user:

- migration plan
- cutover plan
- move off this system
- contract migration

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

- Source and target
- Data or traffic involved
- Downtime tolerance
- Verification method

## Workflow


### 1. Inventory

What moves, and what must not move, from their description.
### 2. Dual run

How both sides can be compared before cutover. If comparison is impossible, say the risk is higher.
### 3. Cutover

The steps, the owner, and the go/no-go check.
### 4. Backout

The point of no return. Before it, how to return. After it, who accepts forward-only.
### 5. Communication

Who is told, including support. No customer claim you cannot honor.
### 6. Verification

The check that the new path is correct, using their data, not a hope.

## Output

Deliver a **migration plan**.

- Purpose of this migration plan, in two sentences.
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

Aisha Rahman, engineering lead at Fieldnote in Edmonton, needs a migration plan by 30 September 2026. A team plans to switch billing systems over a weekend with no way to compare invoices.

### Example data

```text
From: Aisha Rahman, engineering lead
Organization: Fieldnote, Edmonton
Date: 14 September 2026
Needed by: 30 September 2026

A team plans to switch billing systems over a weekend with no way to compare invoices.

Source and target: note from Aisha Rahman, 14 September 2026. No outside report
Data or traffic involved: 75 in the last period. No prior period attached, so no trend
Downtime tolerance: five working days, due 30 September 2026
Verification method: the method in the ask. No second design attached
```

### Example outcome

**Migration plan**
To: Aisha Rahman, engineering lead, Fieldnote
Date: 14 September 2026 · Needed by: 30 September 2026

**Decision**
Adds a comparison phase and names the point of no return before any weekend cutover is approved.

**What the file supports**

| Input | Value | Status |
| --- | --- | --- |
| Source and target | note from Aisha Rahman, 14 September 2026. No outside report | Needs confirmation |
| Data or traffic involved | 75 in the last period. No prior period attached, so no trend | Carried into the draft |
| Downtime tolerance | five working days, due 30 September 2026 | Carried into the draft |
| Verification method | the method in the ask. No second design attached | Needs confirmation |

**How this draft was built**

**1. Inventory**  
What moves, and what must not move, from their description.

**2. Dual run**  
How both sides can be compared before cutover. If comparison is impossible, say the risk is higher.

**3. Cutover**  
The steps, the owner, and the go/no-go check.

**4. Backout**  
The point of no return. Before it, how to return. After it, who accepts forward-only.

**5. Communication**  
Who is told, including support. No customer claim you cannot honor.

**Deliberately not done**
- A cutover with no backout and no accepted point of no return.
- Inventing record counts.
- A migration communicated as zero-risk.

**Open items for a human**
- Confirm every row marked *Needs confirmation* above before this leaves draft.
- Anything absent from the file stayed absent. No figure, date, or name was supplied from outside it.

Next: Aisha Rahman by 30 September 2026. This is a draft, not a sign-off.

## Anti-patterns

- A cutover with no backout and no accepted point of no return.
- Inventing record counts.
- A migration communicated as zero-risk.

## Related skills

- `data-migration-plan`
- `database-change-review`
