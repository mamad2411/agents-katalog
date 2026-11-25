---
name: performance-budget
description: "Set a performance budget for a user journey and a plan for what happens when a change blows it. Use when the user mentions performance budget, latency budget, page weight, performance regression, or asks for a performance budget. Engineering skill by Yasir Jilani."
license: MIT
compatibility: Agent Skills standard. No network access, extra packages, or credentials required.
metadata:
  author: Yasir Jilani
  version: "1.0.0"
  domain: engineering
---

<!-- GENERATED FILE - edits here are overwritten by scripts/generate.py.
     Edit the 'performance-budget' entry in source/, then run:
       python3 scripts/generate.py && python3 scripts/validate.py
     See CONTRIBUTING.md. -->

# Performance Budget

Set a performance budget for a user journey and a plan for what happens when a change blows it.

## When to use this skill

Use this skill when the user:

- performance budget
- latency budget
- page weight
- performance regression

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

- The user journey
- Current measurements if any
- The pain users feel
- The constraint: mobile, warehouse network, or checkout

## Workflow


### 1. Journey

The page or action that matters. A budget on an unused admin page is optional.
### 2. Metric

A user-centered metric they can measure. If they have no measurement, the first step is to measure, not to invent a number.
### 3. Budget

Set the budget from their baseline or a stated user need. Label proposals as proposals.
### 4. Guard

Where in CI or review the budget is checked. A budget nobody checks is a slide.
### 5. Blow-up policy

Who may exceed it, and what must be fixed first.
### 6. No theater

Do not recommend a micro-optimization before the measurement exists.

## Output

Deliver a **performance budget**.

- Purpose of this performance budget, in two sentences.
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

Aisha Rahman, engineering lead at Fieldnote in Edmonton, needs a performance budget by 30 September 2026. A team wants a 100 millisecond budget because a talk recommended it, and they have never measured the checkout.

### Example data

```text
From: Aisha Rahman, engineering lead
Organization: Fieldnote, Edmonton
Date: 14 September 2026
Needed by: 30 September 2026

A team wants a 100 millisecond budget because a talk recommended it, and they have never measured the checkout.

The user journey: the one named in the ask. Version and owner not recorded
Current measurements if any: not defined beyond plan 140 and actual 70
The pain users feel: CAD 180, from their sheet, not a guess
The constraint: mobile, warehouse network, or checkout: mobile: in the file; warehouse network: not in the file; checkout: open
```

### Example outcome

**Variance note**
Fieldnote · period ending 14 September 2026

Decision: treat the gap as a miss against the file, not as a formatting issue. Do not call it timing unless the invoice date is in the file.

| Line | Plan | Actual | Gap |
| --- | --- | --- | --- |
| Main driver | 140 | 70 | 70 |
| One-off named in the file | — | not supplied | leave open |
| Full-period outlook | unchanged until the one-off is dated | | |

Measures checkout first and treats 100 milliseconds as an unadopted proposal.
Next action: Aisha Rahman marks the gap as timing or as a real miss by 30 September 2026.

## Anti-patterns

- An invented millisecond target presented as fact.
- A budget with no guard.
- Optimizing before measuring.

## Related skills

- `observability-plan`
- `slo-error-budget`
