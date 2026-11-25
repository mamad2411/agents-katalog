---
name: returns-process
description: "Design a returns process with a reason code, a disposition, and a customer promise you can keep. Use when the user mentions returns process, RMA, reverse logistics, refund operations, or asks for a returns process. Supply chain skill by Yasir Jilani."
license: MIT
compatibility: Agent Skills standard. No network access, extra packages, or credentials required.
metadata:
  author: Yasir Jilani
  version: "1.0.0"
  domain: supply-chain
---

<!-- GENERATED FILE - edits here are overwritten by scripts/generate.py.
     Edit the 'returns-process' entry in source/, then run:
       python3 scripts/generate.py && python3 scripts/validate.py
     See CONTRIBUTING.md. -->

# Returns Process

Design a returns process with a reason code, a disposition, and a customer promise you can keep.

## When to use this skill

Use this skill when the user:

- returns process
- RMA
- reverse logistics
- refund operations

## When not to use this skill

- The user wants a different domain's specialist skill.
- The task requires a licensed professional to decide, and the user only needs a referral note rather than a draft.
- The request asks you to deceive, evade a control, or hide material facts.

## Professional boundary

Inventory and supplier recommendations depend on the user's lead times and service targets. Do not invent supplier performance.

## Operating boundaries

- Use only information the user provides or files they explicitly ask you to read. Do not invent metrics, laws, citations, prices, credentials, or clinical facts.
- Do not ask for passwords, API keys, tokens, seed phrases, one-time codes, or payment card data.
- Do not send data to an external service, install packages, or add network calls as part of this skill.
- Separate facts, assumptions, and recommendations. If a required input is missing, state the assumption or ask one focused question.
- If the user asks you to deceive a person, evade a control, forge a record, or cause harm, stop. Offer a legitimate alternative.
- Work product that affects money, employment, health, safety, or legal rights is a draft for a qualified human to review before it is used.

## Inputs to collect

- Reasons they see
- Disposition options
- Refund authority
- Customer promise

## Workflow


### 1. Step 1

Capture a reason code that operations can act on.
### 2. Route disposition

restock, repair, or scrap, based on their rules.
### 3. Step 3

State the customer promise and the clock they can meet.
### 4. Step 4

Separate a policy exception from the standard path.
### 5. Step 5

Track fraud concerns as a control question, not as an accusation in the customer message.
### 6. Step 6

Do not help conceal returned goods from inventory records.

## Output

Deliver a **returns process**.

- Purpose of this returns process, in two sentences.
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

Diane Cho, supply lead at Harbor Goods in Airdrie, needs a returns process by 30 September 2026. The website promises instant refunds and the warehouse has not inspected the unit.

### Example data

```text
From: Diane Cho, supply lead
Organization: Harbor Goods, Airdrie
Date: 14 September 2026
Needed by: 30 September 2026

The website promises instant refunds and the warehouse has not inspected the unit.

Reasons they see: Calgary-Edmonton lane. Stated in the ask, not documented anywhere else
Disposition options: keep SKU 1044 cabin filter, or stop. No third option written
Refund authority: SKU 1044 cabin filter and one other, both unconfirmed as of 14 September 2026
Customer promise: Kite Freight
```

### Example outcome

**Returns process**
To: Diane Cho, supply lead, Harbor Goods
Date: 14 September 2026 · Needed by: 30 September 2026

**Decision**
Aligns the promise with inspection and keeps inventory records honest.

**What the file supports**

| Input | Value | Status |
| --- | --- | --- |
| Reasons they see | Calgary-Edmonton lane. Stated in the ask, not documented anywhere else | Needs confirmation |
| Disposition options | keep SKU 1044 cabin filter, or stop. No third option written | Carried into the draft |
| Refund authority | SKU 1044 cabin filter and one other, both unconfirmed as of 14 September 2026 | Carried into the draft |
| Customer promise | Kite Freight | Needs confirmation |

**How this draft was built**

**1. Capture a reason code that operations can act on**

**2. Route disposition**  
restock, repair, or scrap, based on their rules.

**3. State the customer promise and the clock they can meet**

**4. Separate a policy exception from the standard path**

**5. Track fraud concerns as a control question, not as an accusation in the customer message**

**Deliberately not done**
- A promise they cannot meet.
- Concealed returns.
- Accusing a customer in the template.

**Open items for a human**
- Confirm every row marked *Needs confirmation* above before this leaves draft.
- Anything absent from the file stayed absent. No figure, date, or name was supplied from outside it.

Next: Diane Cho by 30 September 2026. This is a draft, not a sign-off.

## Anti-patterns

- A promise they cannot meet
- Concealed returns
- Accusing a customer in the template

## Related skills

- `service-recovery`
- `inventory-accounting`
