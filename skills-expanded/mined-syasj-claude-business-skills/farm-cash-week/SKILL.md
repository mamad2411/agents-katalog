---
name: farm-cash-week
description: "Review a farm's coming weeks of cash against known receipts and bills. Use when the user mentions farm cash, seasonal cash, harvest cash, farm treasury, or asks for a weekly farm cash note. Agriculture operations skill by Yasir Jilani."
license: MIT
compatibility: Agent Skills standard. No network access, extra packages, or credentials required.
metadata:
  author: Yasir Jilani
  version: "1.0.0"
  domain: agriculture
---

<!-- GENERATED FILE - edits here are overwritten by scripts/generate.py.
     Edit the 'farm-cash-week' entry in source/, then run:
       python3 scripts/generate.py && python3 scripts/validate.py
     See CONTRIBUTING.md. -->

# Farm Cash Week

Review a farm's coming weeks of cash against known receipts and bills.

## When to use this skill

Use this skill when the user:

- farm cash
- seasonal cash
- harvest cash
- farm treasury

## When not to use this skill

- The user wants a different domain's specialist skill.
- The task requires a licensed professional to decide, and the user only needs a referral note rather than a draft.
- The request asks you to deceive, evade a control, or hide material facts.

## Professional boundary

Farm plans are operational, not agronomic prescriptions for hazardous materials. Do not provide instructions for synthesizing pesticides, toxins, or pathogens. A local agronomist or veterinarian should confirm field decisions.

## Operating boundaries

- Use only information the user provides or files they explicitly ask you to read. Do not invent metrics, laws, citations, prices, credentials, or clinical facts.
- Do not ask for passwords, API keys, tokens, seed phrases, one-time codes, or payment card data.
- Do not send data to an external service, install packages, or add network calls as part of this skill.
- Separate facts, assumptions, and recommendations. If a required input is missing, state the assumption or ask one focused question.
- If the user asks you to deceive a person, evade a control, forge a record, or cause harm, stop. Offer a legitimate alternative.
- Work product that affects money, employment, health, safety, or legal rights is a draft for a qualified human to review before it is used.

## Inputs to collect

- Cash
- Expected receipts they consider real
- Bills due
- The buffer they want

## Workflow


### 1. Step 1

List receipts only if a buyer or program has confirmed them, or label them hoped.
### 2. Step 2

List bills by date.
### 3. Step 3

Show the week the buffer breaks.
### 4. Step 4

Separate a capital buy from operating bills.
### 5. Step 5

Do not advise a lender fraud or a concealed sale.
### 6. Step 6

Recommend a conversation with their lender or advisor if the break is inside the buffer.

## Output

Deliver a **weekly farm cash note**.

- Purpose of this weekly farm cash note, in two sentences.
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

Ruth McKay, operator at Two Hills Farm in Olds, needs a weekly farm cash note by 30 September 2026. A note treats an unsigned grain contract as cash already coming.

### Example data

```text
From: Ruth McKay, operator
Organization: Two Hills Farm, Olds
Date: 14 September 2026
Needed by: 30 September 2026

A note treats an unsigned grain contract as cash already coming.

Cash: Harvest window. Partly documented: the what is written down, the who is not
Expected receipts they consider real: North quarter, 140 acres and one other, both unconfirmed as of 14 September 2026
Bills due: North quarter, 140 acres and one other, both unconfirmed as of 14 September 2026
The buffer they want: North quarter, 140 acres, recorded 14 September 2026. No supporting file attached
```

### Example outcome

**Weekly farm cash note**
To: Ruth McKay, operator, Two Hills Farm
Date: 14 September 2026 · Needed by: 30 September 2026

**Decision**
Labels the contract hoped and shows the break week without it.

**What the file supports**

| Input | Value | Status |
| --- | --- | --- |
| Cash | Harvest window. Partly documented: the what is written down, the who is not | Needs confirmation |
| Expected receipts they consider real | North quarter, 140 acres and one other, both unconfirmed as of 14 September 2026 | Carried into the draft |
| Bills due | North quarter, 140 acres and one other, both unconfirmed as of 14 September 2026 | Carried into the draft |
| The buffer they want | North quarter, 140 acres, recorded 14 September 2026. No supporting file attached | Needs confirmation |

**How this draft was built**

**1. List receipts only if a buyer or program has confirmed them, or label them hoped**

**2. List bills by date**

**3. Show the week the buffer breaks**

**4. Separate a capital buy from operating bills**

**5. Do not advise a lender fraud or a concealed sale**

**Deliberately not done**
- Hoped receipts shown as certain.
- Concealed sales.
- A capital buy hidden in operations.

**Open items for a human**
- Confirm every row marked *Needs confirmation* above before this leaves draft.
- Anything absent from the file stayed absent. No figure, date, or name was supplied from outside it.

Next: Ruth McKay by 30 September 2026. This is a draft, not a sign-off.

## Anti-patterns

- Hoped receipts shown as certain
- Concealed sales
- A capital buy hidden in operations

## Related skills

- `cash-flow-forecast`
- `season-plan`
