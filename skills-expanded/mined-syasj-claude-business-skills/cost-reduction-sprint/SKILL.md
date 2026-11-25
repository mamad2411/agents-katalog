---
name: cost-reduction-sprint
description: "Find cost that can come out without pretending that every cut is free of service impact. Use when the user mentions cut costs, cost reduction, save money quickly, expense sprint, or asks for a cost reduction sprint plan. Finance skill by Yasir Jilani."
license: MIT
compatibility: Agent Skills standard. No network access, extra packages, or credentials required.
metadata:
  author: Yasir Jilani
  version: "1.0.0"
  domain: finance
---

<!-- GENERATED FILE - edits here are overwritten by scripts/generate.py.
     Edit the 'cost-reduction-sprint' entry in source/, then run:
       python3 scripts/generate.py && python3 scripts/validate.py
     See CONTRIBUTING.md. -->

# Cost Reduction Sprint

Find cost that can come out without pretending that every cut is free of service impact.

## When to use this skill

Use this skill when the user:

- cut costs
- cost reduction
- save money quickly
- expense sprint

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

- Cost baseline by category
- What must not be cut, in the user's words
- Contracts and notice periods if known
- Service or quality lines they will not cross

## Workflow


### 1. Set a target and a boundary

How much, by when, and what is protected. A sprint without a protected list damages the business at random.
### 2. Sort actions

Stop, renegotiate, delay, and redesign. Quick stops are not the same as structural redesigns.
### 3. Estimate savings from the baseline

Use the user's numbers. Mark one-time savings separately from run-rate.
### 4. Name the harm

Each material cut gets a service, risk, or morale consequence. If the user does not know it, list it as unknown rather than as zero.
### 5. Assign owners and dates

A list without owners is a mood.
### 6. Install a check

A short review two cycles later to see if the cost returned under another name.

## Output

Deliver a **cost reduction sprint plan**.

- Purpose of this cost reduction sprint plan, in two sentences.
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

Mara Chen, founder at Northline Studio in Calgary, needs a cost reduction sprint plan by 30 September 2026. A company needs to remove a stated monthly amount within 60 days and has already ruled out layoffs.

### Example data

```text
From: Mara Chen, founder
Organization: Northline Studio, Calgary
Date: 14 September 2026
Needed by: 30 September 2026

A company needs to remove a stated monthly amount within 60 days and has already ruled out layoffs.

Cost baseline by category: CAD 27 direct. Overhead not in this line
What must not be cut, in the user's words: Payroll 15 September, last reviewed 14 September 2026. No owner named since
Contracts and notice periods if known: month ending 14 September 2026
Service or quality lines they will not cross: the one named in the ask. Version and owner not recorded
```

### Example outcome

**Cost reduction sprint plan**
To: Mara Chen, founder, Northline Studio
Date: 14 September 2026 · Needed by: 30 September 2026

**Decision**
A sprint list of stops and renegotiations, run-rate versus one-time savings, and the service risk on each item.

**What the file supports**

| Input | Value | Status |
| --- | --- | --- |
| Cost baseline by category | CAD 27 direct. Overhead not in this line | Needs confirmation |
| What must not be cut, in the user's words | Payroll 15 September, last reviewed 14 September 2026. No owner named since | Carried into the draft |
| Contracts and notice periods if known | month ending 14 September 2026 | Carried into the draft |
| Service or quality lines they will not cross | the one named in the ask. Version and owner not recorded | Needs confirmation |

**How this draft was built**

**1. Set a target and a boundary**  
How much, by when, and what is protected. A sprint without a protected list damages the business at random.

**2. Sort actions**  
Stop, renegotiate, delay, and redesign. Quick stops are not the same as structural redesigns.

**3. Estimate savings from the baseline**  
Use the user's numbers. Mark one-time savings separately from run-rate.

**4. Name the harm**  
Each material cut gets a service, risk, or morale consequence. If the user does not know it, list it as unknown rather than as zero.

**5. Assign owners and dates**  
A list without owners is a mood.

**Deliberately not done**
- Across-the-board percentage cuts with no owner.
- Counting a delayed project as permanent savings.
- Cutting a protected safety or compliance cost the user said was off limits.

**Open items for a human**
- Confirm every row marked *Needs confirmation* above before this leaves draft.
- Anything absent from the file stayed absent. No figure, date, or name was supplied from outside it.

Next: Mara Chen by 30 September 2026. This is a draft, not a sign-off.

## Anti-patterns

- Across-the-board percentage cuts with no owner.
- Counting a delayed project as permanent savings.
- Cutting a protected safety or compliance cost the user said was off limits.

## Related skills

- `budget-variance-review`
- `vendor-ops-review`
- `zero-based-budget-review`
