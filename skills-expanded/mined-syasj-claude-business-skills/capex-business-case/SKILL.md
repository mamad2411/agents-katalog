---
name: capex-business-case
description: "Write a capital-spend case that states the problem, the alternatives, and the cash consequences without fake precision. Use when the user mentions capex case, capital request, should we buy this equipment, investment business case, or asks for a capex business case. Finance skill by Yasir Jilani."
license: MIT
compatibility: Agent Skills standard. No network access, extra packages, or credentials required.
metadata:
  author: Yasir Jilani
  version: "1.0.0"
  domain: finance
---

<!-- GENERATED FILE - edits here are overwritten by scripts/generate.py.
     Edit the 'capex-business-case' entry in source/, then run:
       python3 scripts/generate.py && python3 scripts/validate.py
     See CONTRIBUTING.md. -->

# Capex Business Case

Write a capital-spend case that states the problem, the alternatives, and the cash consequences without fake precision.

## When to use this skill

Use this skill when the user:

- capex case
- capital request
- should we buy this equipment
- investment business case

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

- The problem the spend solves
- Cost and timing the user has
- Alternatives including do nothing
- How benefits will be observed

## Workflow


### 1. Define the problem

Downtime, capacity, safety, or compliance. A request that starts with the vendor's name is not ready.
### 2. Compare alternatives

Buy, lease, outsource, or defer. Include do nothing and its operational cost if the user described one.
### 3. Lay out cash

Deposit, install, training, and maintenance. Benefits are cash or a clearly non-cash obligation the user names, such as a safety requirement.
### 4. Avoid theatrical IRR

If the user wants a return metric, compute it only from their cash items and show the sensitivity. Do not invent a hurdle rate.
### 5. Name the benefit owner

Who will confirm, after installation, that the benefit showed up.
### 6. State the kill

What finding during procurement would stop the spend.

## Output

Deliver a **capex business case**.

- Purpose of this capex business case, in two sentences.
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

Mara Chen, founder at Northline Studio in Calgary, needs a capex business case by 30 September 2026. Operations wants a packaging machine and has one quote and a claim that it will 'pay for itself'.

### Example data

```text
From: Mara Chen, founder
Organization: Northline Studio, Calgary
Date: 14 September 2026
Needed by: 30 September 2026

Operations wants a packaging machine and has one quote and a claim that it will 'pay for itself'.

The problem the spend solves: Operations wants a packaging machine and has one quote and a claim that it will 'pay for itself'. Stated once, in the ask. Not written down anywhere else
Cost and timing the user has: CAD 18 direct. Overhead not in this line
Alternatives including do nothing: two deals cited from memory. Neither has a written loss reason
How benefits will be observed: Harbor & Co receipt, last reviewed 14 September 2026. No owner named since
```

### Example outcome

**Capex business case**
To: Mara Chen, founder, Northline Studio
Date: 14 September 2026 · Needed by: 30 September 2026

**Decision**
A case with alternatives, cash timing, a benefit the team can later observe, and no invented hurdle rate.

**What the file supports**

| Input | Value | Status |
| --- | --- | --- |
| The problem the spend solves | Operations wants a packaging machine and has one quote and a claim that it will 'pay for itself'. Stated once, in the ask. Not written down anywhere else | Needs confirmation |
| Cost and timing the user has | CAD 18 direct. Overhead not in this line | Carried into the draft |
| Alternatives including do nothing | two deals cited from memory. Neither has a written loss reason | Carried into the draft |
| How benefits will be observed | Harbor & Co receipt, last reviewed 14 September 2026. No owner named since | Needs confirmation |

**How this draft was built**

**1. Define the problem**  
Downtime, capacity, safety, or compliance. A request that starts with the vendor's name is not ready.

**2. Compare alternatives**  
Buy, lease, outsource, or defer. Include do nothing and its operational cost if the user described one.

**3. Lay out cash**  
Deposit, install, training, and maintenance. Benefits are cash or a clearly non-cash obligation the user names, such as a safety requirement.

**4. Avoid theatrical IRR**  
If the user wants a return metric, compute it only from their cash items and show the sensitivity. Do not invent a hurdle rate.

**5. Name the benefit owner**  
Who will confirm, after installation, that the benefit showed up.

**Deliberately not done**
- A vendor quote pasted into a memo with no alternative.
- An IRR built on imagined savings.
- Ignoring training and downtime during install.

**Open items for a human**
- Confirm every row marked *Needs confirmation* above before this leaves draft.
- Anything absent from the file stayed absent. No figure, date, or name was supplied from outside it.

Next: Mara Chen by 30 September 2026. This is a draft, not a sign-off.

## Anti-patterns

- A vendor quote pasted into a memo with no alternative.
- An IRR built on imagined savings.
- Ignoring training and downtime during install.

## Related skills

- `investment-memo`
- `break-even-analysis`
- `production-schedule`
