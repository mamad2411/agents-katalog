---
name: saas-metrics-pack
description: "Define a small SaaS metrics pack from the company's own billing reality, without imported benchmark theater. Use when the user mentions SaaS metrics, ARR MRR churn, net revenue retention, magic number, or asks for a SaaS metrics definitions. Finance skill by Yasir Jilani."
license: MIT
compatibility: Agent Skills standard. No network access, extra packages, or credentials required.
metadata:
  author: Yasir Jilani
  version: "1.0.0"
  domain: finance
---

<!-- GENERATED FILE - edits here are overwritten by scripts/generate.py.
     Edit the 'saas-metrics-pack' entry in source/, then run:
       python3 scripts/generate.py && python3 scripts/validate.py
     See CONTRIBUTING.md. -->

# SaaS Metrics Pack

Define a small SaaS metrics pack from the company's own billing reality, without imported benchmark theater.

## When to use this skill

Use this skill when the user:

- SaaS metrics
- ARR MRR churn
- net revenue retention
- magic number

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

- How customers are billed
- Expansion, contraction, and churn definitions they want to use
- Segments that should not be mixed
- The decision the pack supports

## Workflow


### 1. Define ARR or MRR from contracts

Write the inclusion rule. One-time services do not become ARR because someone wishes they would.
### 2. Define retention carefully

Logo churn and revenue retention answer different questions. Do not blend them into one cheerful number.
### 3. Segment if the motion differs

A self-serve cohort and an enterprise cohort do not share one retention story unless the user shows they do.
### 4. Show the bridge

Starting recurring revenue, new, expansion, contraction, churn, ending. A single ending balance is not a pack.
### 5. Skip vanity multiples

Do not compute a metric the billing data cannot support. Say it is unavailable.
### 6. Refuse borrowed benchmarks

You may explain what a metric means. Do not declare the company healthy because a blog once named a number.

## Output

Deliver a **SaaS metrics definitions**.

- Purpose of this SaaS metrics definitions, in two sentences.
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

Mara Chen, founder at Northline Studio in Calgary, needs a SaaS metrics definitions by 30 September 2026. A finance lead wants a board slide for net retention, but implementation fees have been folded into ARR.

### Example data

```text
From: Mara Chen, founder
Organization: Northline Studio, Calgary
Date: 14 September 2026
Needed by: 30 September 2026

A finance lead wants a board slide for net retention, but implementation fees have been folded into ARR.

How customers are billed: Harbor & Co receipt, last reviewed 14 September 2026. No owner named since
Expansion, contraction, and churn definitions they want to use: unsigned draft, 8 pages, no signature date
Segments that should not be mixed: Operating cash, recorded 14 September 2026. No supporting file attached
The decision the pack supports: A finance lead wants a board slide for net retention, but implementation fees have been folded into ARR
```

### Example outcome

**Saas metrics definitions**
Northline Studio · 14 September 2026 · Due 30 September 2026

**Decision**
Definitions that pull fees back out, a revenue bridge, and no invented benchmark grade.

| Item | Figure in the file | Call | Why |
| --- | --- | --- | --- |
| Kite Freight | plan 160, actual 95 | Use | Both sides of the comparison are in the file |
| Lantern Inn | score 78 | Report, do not benchmark | One score is a reading, not a baseline |
| Missing export | Not in the file | Stop | The cell stays blank until the export arrives |

**How these calls were made**

1. Define ARR or MRR from contracts
2. Define retention carefully
3. Segment if the motion differs
4. Show the bridge
5. Skip vanity multiples

**Deliberately not done**
- Calling services revenue ARR.
- One churn number for two different motions.
- A benchmark comparison invented from memory.

**Open items**
- The missing export is the binding constraint. No figure was estimated to fill its place.
- Any row marked *Report, do not benchmark* needs a second period before it can carry a trend.

Next: Mara Chen attaches the missing export, or the cell stays blank. Due 30 September 2026.

## Anti-patterns

- Calling services revenue ARR.
- One churn number for two different motions.
- A benchmark comparison invented from memory.

## Related skills

- `unit-economics`
- `management-reporting-pack`
- `metric-definition`
