---
name: zero-based-budget-review
description: "Rebuild a cost pool from activities that still earn their keep, instead of last year plus a percent. Use when the user mentions zero based budget, rebuild the budget, justify this spend, cost pool review, or asks for a zero-based review of one cost pool. Finance skill by Yasir Jilani."
license: MIT
compatibility: Agent Skills standard. No network access, extra packages, or credentials required.
metadata:
  author: Yasir Jilani
  version: "1.0.0"
  domain: finance
---

<!-- GENERATED FILE - edits here are overwritten by scripts/generate.py.
     Edit the 'zero-based-budget-review' entry in source/, then run:
       python3 scripts/generate.py && python3 scripts/validate.py
     See CONTRIBUTING.md. -->

# Zero-Based Budget Review

Rebuild a cost pool from activities that still earn their keep, instead of last year plus a percent.

## When to use this skill

Use this skill when the user:

- zero based budget
- rebuild the budget
- justify this spend
- cost pool review

## When not to use this skill

- The user wants a different domain's specialist skill.
- The task requires a licensed professional to decide, and the user only needs a referral note rather than a draft.
- The request asks you to deceive, evade a control, or hide material facts.

## Professional boundary

This is not investment, tax, or financial advice. Do not invent rates of return, tax rates, or valuation multiples. A qualified finance professional must review any decision that moves money.

## Operating boundaries

- Use only information the user provides or files they explicitly ask you to read. Do not invent metrics, laws, citations, prices, credentials, or clinical facts.
- Do not ask for passwords, API keys, tokens, seed phrases, one-time codes, or payment card data.
- Do not send data to an external service, install packages, or add network calls as part of this skill.
- Separate facts, assumptions, and recommendations. If a required input is missing, state the assumption or ask one focused question.
- If the user asks you to deceive a person, evade a control, forge a record, or cause harm, stop. Offer a legitimate alternative.
- Work product that affects money, employment, health, safety, or legal rights is a draft for a qualified human to review before it is used.

## Inputs to collect

- The cost pool
- The activities it pays for
- Demand for those activities
- The decision rights

## Workflow


### 1. Bound the pool

One pool, such as travel, contractors, or a function's non-payroll spend. A company-wide zero-base in one sitting is theater.
### 2. List activities

What work the money buys. Vendors are not activities.
### 3. Tie to demand

Which activities a current strategy bet still requires. Orphan activities are the candidates.
### 4. Rebuild

Propose a keep, reduce, and stop list with amounts from the user's baseline.
### 5. Check the service

Who will feel a stop. Include that in the recommendation.
### 6. Leave a rhythm

When this pool is reviewed again, so it does not silently return to last-year-plus.

## Output

Deliver a **zero-based review of one cost pool**.

- Purpose of this zero-based review of one cost pool, in two sentences.
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

Mara Chen, founder at Northline Studio in Calgary, needs a zero-based review of one cost pool by 30 September 2026. Travel spend is up and nobody can say which trips still match the sales motion.

### Example data

```text
From: Mara Chen, founder
Organization: Northline Studio, Calgary
Date: 14 September 2026
Needed by: 30 September 2026

Travel spend is up and nobody can say which trips still match the sales motion.

The cost pool: CAD 44 direct. Overhead not in this line
The activities it pays for: Operating cash, recorded 14 September 2026. No supporting file attached
Demand for those activities: 55 in the last period. No prior period attached, so no trend
The decision rights: Travel spend is up and nobody can say which trips still match the sales motion
```

### Example outcome

**Variance note**
Northline Studio · period ending 14 September 2026

Decision: treat the gap as a miss against the file, not as a formatting issue. Do not call it timing unless the invoice date is in the file.

| Line | Plan | Actual | Gap |
| --- | --- | --- | --- |
| Main driver | 120 | 95 | 25 |
| One-off named in the file | — | not supplied | leave open |
| Full-period outlook | unchanged until the one-off is dated | | |

A keep, reduce, and stop list for travel activities, tied to the current motion, with the customer-facing trips protected if the user said they matter.
Next action: Mara Chen marks the gap as timing or as a real miss by 30 September 2026.

## Anti-patterns

- Last year plus five percent, renamed zero-based.
- Cutting a pool without naming the activity.
- A company-wide exercise with no decision rights.

## Related skills

- `cost-reduction-sprint`
- `budget-variance-review`
- `annual-planning-cycle`
