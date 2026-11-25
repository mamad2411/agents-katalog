---
name: shortage-playbook
description: "Allocate a shortage fairly against a stated rule, and communicate it without favoritism hidden in a spreadsheet. Use when the user mentions shortage, allocation, fair share, supply shortage playbook, or asks for a shortage playbook. Supply chain skill by Yasir Jilani."
license: MIT
compatibility: Agent Skills standard. No network access, extra packages, or credentials required.
metadata:
  author: Yasir Jilani
  version: "1.0.0"
  domain: supply-chain
---

<!-- GENERATED FILE - edits here are overwritten by scripts/generate.py.
     Edit the 'shortage-playbook' entry in source/, then run:
       python3 scripts/generate.py && python3 scripts/validate.py
     See CONTRIBUTING.md. -->

# Shortage Playbook

Allocate a shortage fairly against a stated rule, and communicate it without favoritism hidden in a spreadsheet.

## When to use this skill

Use this skill when the user:

- shortage
- allocation
- fair share
- supply shortage playbook

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

- Available quantity
- Demand by customer or channel
- The allocation rule they want
- Contractual priorities they named

## Workflow


### 1. Step 1

State the available quantity and the date.
### 2. Apply the rule they chose

contract first, pro rata, or margin. If no rule exists, recommend they set one before allocating by friendship.
### 3. Step 3

Honor contractual priorities they confirmed. Do not invent a contract.
### 4. Step 4

Show who is cut and by how much.
### 5. Step 5

Draft a truthful customer message.
### 6. Step 6

Record exceptions so the rule does not become theater.

## Output

Deliver a **shortage playbook**.

- Purpose of this shortage playbook, in two sentences.
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

Diane Cho, supply lead at Harbor Goods in Airdrie, needs a shortage playbook by 30 September 2026. A planner gives the scarce item to the loudest salesperson's account.

### Example data

```text
From: Diane Cho, supply lead
Organization: Harbor Goods, Airdrie
Date: 14 September 2026
Needed by: 30 September 2026

A planner gives the scarce item to the loudest salesperson's account.

Available quantity: 35 in the last period. No prior period attached, so no trend
Demand by customer or channel: 35 in the last period. No prior period attached, so no trend
The allocation rule they want: their one-page rule dated 2 Mar 2026. No exception log since
Contractual priorities they named: unsigned draft, 8 pages, no signature date
```

### Example outcome

**Shortage playbook**
To: Diane Cho, supply lead, Harbor Goods
Date: 14 September 2026 · Needed by: 30 September 2026

**Decision**
Applies a written rule, records exceptions, and tells affected customers the truth.

**What the file supports**

| Input | Value | Status |
| --- | --- | --- |
| Available quantity | 35 in the last period. No prior period attached, so no trend | Needs confirmation |
| Demand by customer or channel | 35 in the last period. No prior period attached, so no trend | Carried into the draft |
| The allocation rule they want | their one-page rule dated 2 Mar 2026. No exception log since | Carried into the draft |
| Contractual priorities they named | unsigned draft, 8 pages, no signature date | Needs confirmation |

**How this draft was built**

**1. State the available quantity and the date**

**2. Apply the rule they chose**  
contract first, pro rata, or margin. If no rule exists, recommend they set one before allocating by friendship.

**3. Honor contractual priorities they confirmed. Do not invent a contract**

**4. Show who is cut and by how much**

**5. Draft a truthful customer message**

**Deliberately not done**
- Allocation by friendship with no record.
- Invented contractual priority.
- A message that says stock is fine.

**Open items for a human**
- Confirm every row marked *Needs confirmation* above before this leaves draft.
- Anything absent from the file stayed absent. No figure, date, or name was supplied from outside it.

Next: Diane Cho by 30 September 2026. This is a draft, not a sign-off.

## Anti-patterns

- Allocation by friendship with no record
- Invented contractual priority
- A message that says stock is fine

## Related skills

- `war-room-brief`
- `logistics-exception`
