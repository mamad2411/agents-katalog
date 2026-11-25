---
name: slo-error-budget
description: "Draft an SLO from a user journey and explain how the error budget changes release behavior. Use when the user mentions SLO, error budget, service level objective, reliability target, or asks for a SLO draft. Engineering skill by Yasir Jilani."
license: MIT
compatibility: Agent Skills standard. No network access, extra packages, or credentials required.
metadata:
  author: Yasir Jilani
  version: "1.0.0"
  domain: engineering
---

<!-- GENERATED FILE - edits here are overwritten by scripts/generate.py.
     Edit the 'slo-error-budget' entry in source/, then run:
       python3 scripts/generate.py && python3 scripts/validate.py
     See CONTRIBUTING.md. -->

# SLO and Error Budget

Draft an SLO from a user journey and explain how the error budget changes release behavior.

## When to use this skill

Use this skill when the user:

- SLO
- error budget
- service level objective
- reliability target

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
- Current performance if known
- The pain that matters
- Release cadence

## Workflow


### 1. Journey

The user action the SLO protects. Internal CPU is not an SLO by default.
### 2. Indicator

A measurable signal they can actually collect. If they cannot collect it, the first task is instrumentation.
### 3. Target

Use their history or mark the target as a proposal. Do not invent a 99.99 because it sounds serious.
### 4. Budget

What the target implies for unavailability in the window, shown as arithmetic from their numbers.
### 5. Policy

What the team does when the budget is gone: slow releases, fix reliability, or accept the burn explicitly.
### 6. Exclusions

Maintenance windows only if the user already has that policy. Do not hide outages in exclusions.

## Output

Deliver a **SLO draft**.

- Purpose of this SLO draft, in two sentences.
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

Aisha Rahman, engineering lead at Fieldnote in Edmonton, needs a SLO draft by 30 September 2026. A team copies a 99.99 SLO from a blog and has no latency metric.

### Example data

```text
From: Aisha Rahman, engineering lead
Organization: Fieldnote, Edmonton
Date: 14 September 2026
Needed by: 30 September 2026

A team copies a 99.99 SLO from a blog and has no latency metric.

The user journey: the one named in the ask. Version and owner not recorded
Current performance if known: 30 in the last period. No prior period attached, so no trend
The pain that matters: Checkout service, recorded 14 September 2026. No supporting file attached
Release cadence: Status page and one other, both unconfirmed as of 14 September 2026
```

### Example outcome

**Variance note**
Fieldnote · period ending 14 September 2026

Decision: treat the gap as a miss against the file, not as a formatting issue. Do not call it timing unless the invoice date is in the file.

| Line | Plan | Actual | Gap |
| --- | --- | --- | --- |
| Main driver | 150 | 80 | 70 |
| One-off named in the file | — | not supplied | leave open |
| Full-period outlook | unchanged until the one-off is dated | | |

Refuses the copied target, names the missing metric, and proposes a journey-based indicator.
Next action: Aisha Rahman marks the gap as timing or as a real miss by 30 September 2026.

## Anti-patterns

- A 99.99 target with no baseline.
- An SLO on a vanity metric.
- No policy when the budget burns.

## Related skills

- `observability-plan`
- `release-checklist`
