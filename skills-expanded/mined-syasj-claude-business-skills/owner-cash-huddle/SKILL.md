---
name: owner-cash-huddle
description: "Set the week's cash picture from the till, the bills due, and the owner's buffer. Use when the user mentions weekly cash, owner huddle, can I pay this bill, shop cash, or asks for a cash huddle. Small business skill by Yasir Jilani."
license: MIT
compatibility: Agent Skills standard. No network access, extra packages, or credentials required.
metadata:
  author: Yasir Jilani
  version: "1.0.0"
  domain: small-business
---

<!-- GENERATED FILE - edits here are overwritten by scripts/generate.py.
     Edit the 'owner-cash-huddle' entry in source/, then run:
       python3 scripts/generate.py && python3 scripts/validate.py
     See CONTRIBUTING.md. -->

# Owner Cash Huddle

Set the week's cash picture from the till, the bills due, and the owner's buffer.

## When to use this skill

Use this skill when the user:

- weekly cash
- owner huddle
- can I pay this bill
- shop cash

## When not to use this skill

- The user wants a different domain's specialist skill.
- The task requires a licensed professional to decide, and the user only needs a referral note rather than a draft.
- The request asks you to deceive, evade a control, or hide material facts.

## Professional boundary

Not legal, tax, or employment advice. Do not invent license rules, tax rates, or a local bylaw.

## Operating boundaries

- Use only information the user provides or files they explicitly ask you to read. Do not invent metrics, laws, citations, prices, credentials, or clinical facts.
- Do not ask for passwords, API keys, tokens, seed phrases, one-time codes, or payment card data.
- Do not send data to an external service, install packages, or add network calls as part of this skill.
- Separate facts, assumptions, and recommendations. If a required input is missing, state the assumption or ask one focused question.
- If the user asks you to deceive a person, evade a control, forge a record, or cause harm, stop. Offer a legitimate alternative.
- Work product that affects money, employment, health, safety, or legal rights is a draft for a qualified human to review before it is used.

## Inputs to collect

- Cash on hand
- Bills due this week
- Expected receipts
- The buffer they will not go under

## Workflow


### 1. Step 1

Start from cash they counted.
### 2. Step 2

List bills by date.
### 3. Step 3

Receipts are expected, not spent.
### 4. Step 4

Flag any day under the buffer.
### 5. Step 5

Do not tell them to skip a tax remittance.
### 6. Step 6

One decision for the week.

## Output

Deliver a **cash huddle**.

- Purpose of this cash huddle, in two sentences.
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

Diane counted $4,200 in the Harbor Goods till on Monday. Rent of $3,000 is due Thursday. A customer said they might pay $2,000. Her buffer is $1,500. A tax remittance of $800 is also due Friday.

### Example data

```text
counted: 4200 CAD, Mon 15 Sep 2026
rent: 3000, Thu 18 Sep
tax remittance: 800, Fri 19 Sep
maybe receipt: 2000, not in the bank
buffer: 1500
```

### Example outcome

**Week huddle**
Do not spend the $2,000. It is not in the till.

| Day | Cash if nothing else arrives | Bill |
| --- | --- | --- |
| Mon | 4,200 | — |
| Thu | 1,200 after rent | rent 3,000 |
| Fri | 400 after tax | tax 800 |

Thursday after rent is $1,200, under the $1,500 buffer, before Friday's tax. Friday's tax still gets paid. It is not the lever.
Decision: no owner draw and no new order this week unless the $2,000 actually arrives.

## Anti-patterns

- A tax skipped to make the week work
- Receipts treated as cash
- No buffer

## Related skills

- `cash-flow-forecast`
- `owner-draw-note`
