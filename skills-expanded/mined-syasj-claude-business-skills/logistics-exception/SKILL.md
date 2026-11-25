---
name: logistics-exception
description: "Handle a logistics exception with the customer impact, the options, and a truthful status. Use when the user mentions logistics exception, delayed shipment, freight exception, missed delivery, or asks for a logistics exception note. Supply chain skill by Yasir Jilani."
license: MIT
compatibility: Agent Skills standard. No network access, extra packages, or credentials required.
metadata:
  author: Yasir Jilani
  version: "1.0.0"
  domain: supply-chain
---

<!-- GENERATED FILE - edits here are overwritten by scripts/generate.py.
     Edit the 'logistics-exception' entry in source/, then run:
       python3 scripts/generate.py && python3 scripts/validate.py
     See CONTRIBUTING.md. -->

# Logistics Exception

Handle a logistics exception with the customer impact, the options, and a truthful status.

## When to use this skill

Use this skill when the user:

- logistics exception
- delayed shipment
- freight exception
- missed delivery

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

- The shipment
- The promise made
- Options and costs they have
- Who must be told

## Workflow


### 1. Step 1

State the promise and the new fact.
### 2. List options they can actually buy

wait, reroute, or partial ship.
### 3. Step 3

Show the customer impact in their words.
### 4. Step 4

Draft a status that does not promise a recovery time they do not have.
### 5. Step 5

Name the owner for the next update.
### 6. Step 6

Do not hide the miss behind vague tracking language.

## Output

Deliver a **logistics exception note**.

- Purpose of this logistics exception note, in two sentences.
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

Diane Cho, supply lead at Harbor Goods in Airdrie, needs a logistics exception note by 30 September 2026. A carrier missed a pickup and the draft tells the customer the order is on time.

### Example data

```text
From: Diane Cho, supply lead
Organization: Harbor Goods, Airdrie
Date: 14 September 2026
Needed by: 30 September 2026

A carrier missed a pickup and the draft tells the customer the order is on time.

The shipment: SKU 1044 cabin filter, recorded 14 September 2026. No supporting file attached
The promise made: none written down beyond the ask
Options and costs they have: CAD 36 direct. Overhead not in this line
Who must be told: Diane Cho, supply lead
```

### Example outcome

**Logistics exception note**
To: Diane Cho, supply lead, Harbor Goods
Date: 14 September 2026 · Needed by: 30 September 2026

**Decision**
States the miss, lists real options, and removes the on-time claim.

**What the file supports**

| Input | Value | Status |
| --- | --- | --- |
| The shipment | SKU 1044 cabin filter, recorded 14 September 2026. No supporting file attached | Needs confirmation |
| The promise made | none written down beyond the ask | Carried into the draft |
| Options and costs they have | CAD 36 direct. Overhead not in this line | Carried into the draft |
| Who must be told | Diane Cho, supply lead | Needs confirmation |

**How this draft was built**

**1. State the promise and the new fact**

**2. List options they can actually buy**  
wait, reroute, or partial ship.

**3. Show the customer impact in their words**

**4. Draft a status that does not promise a recovery time they do not have**

**5. Name the owner for the next update**

**Deliberately not done**
- A fake recovery time.
- No owner.
- Vague tracking language that hides the miss.

**Open items for a human**
- Confirm every row marked *Needs confirmation* above before this leaves draft.
- Anything absent from the file stayed absent. No figure, date, or name was supplied from outside it.

Next: Diane Cho by 30 September 2026. This is a draft, not a sign-off.

## Anti-patterns

- A fake recovery time
- No owner
- Vague tracking language that hides the miss

## Related skills

- `customer-communication-incident`
- `shortage-playbook`
