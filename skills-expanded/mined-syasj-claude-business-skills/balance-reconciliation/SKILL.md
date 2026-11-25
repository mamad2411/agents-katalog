---
name: balance-reconciliation
description: "Reconcile two extracts the user provides and list the rows that do not match. Use when the user mentions reconcile two files, data reconciliation, tie-out, balance check, or asks for a reconciliation. Data and analytics skill by Yasir Jilani."
license: MIT
compatibility: Agent Skills standard. No network access, extra packages, or credentials required.
metadata:
  author: Yasir Jilani
  version: "1.0.0"
  domain: data
---

<!-- GENERATED FILE - edits here are overwritten by scripts/generate.py.
     Edit the 'balance-reconciliation' entry in source/, then run:
       python3 scripts/generate.py && python3 scripts/validate.py
     See CONTRIBUTING.md. -->

# Balance Reconciliation

Reconcile two extracts the user provides and list the rows that do not match.

## When to use this skill

Use this skill when the user:

- reconcile two files
- data reconciliation
- tie-out
- balance check

## When not to use this skill

- The user wants a different domain's specialist skill.
- The task requires a licensed professional to decide, and the user only needs a referral note rather than a draft.
- The request asks you to deceive, evade a control, or hide material facts.

## Professional boundary

Do not invent numbers. If a source file is missing, say so. Distinguish observation from inference. Do not re-identify private data to make a point.

## Operating boundaries

- Use only information the user provides or files they explicitly ask you to read. Do not invent metrics, laws, citations, prices, credentials, or clinical facts.
- Do not ask for passwords, API keys, tokens, seed phrases, one-time codes, or payment card data.
- Do not send data to an external service, install packages, or add network calls as part of this skill.
- Separate facts, assumptions, and recommendations. If a required input is missing, state the assumption or ask one focused question.
- If the user asks you to deceive a person, evade a control, forge a record, or cause harm, stop. Offer a legitimate alternative.
- Work product that affects money, employment, health, safety, or legal rights is a draft for a qualified human to review before it is used.

## Inputs to collect

- Both extracts
- The key
- The amount column
- The as-of time

## Workflow


### 1. Step 1

Match on the key they named.
### 2. Step 2

Sum both sides from the files. Do not type a total from memory.
### 3. Step 3

List unmatched keys.
### 4. Step 4

Separate a timing gap from a real break if the timestamps show it.
### 5. Step 5

Stop if a key is missing.
### 6. Step 6

Do not force a plug figure.

## Output

Deliver a **reconciliation**.

- Purpose of this reconciliation, in two sentences.
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

Noah has two extracts for 12 September. orders_daily sums to $18,400. The billing export sums to $17,160. Three order ids appear on only one side.

### Example data

```text
as of: 12 Sep 2026
key: order_id
amount column: total_cad
orders_daily: 42 rows, sum 18400
billing export: 40 rows, sum 17160
only in orders_daily: 4412, 4418, 4420
only in billing: none
difference: 1240
```

### Example outcome

**Tie-out — 12 September**
orders_daily $18,400. Billing $17,160. Gap $1,240. No plug.

| order_id | In orders_daily | In billing |
| --- | --- | --- |
| 4412 | yes | no |
| 4418 | yes | no |
| 4420 | yes | no |

The three ids are the unmatched set in these files. This note does not say why they are missing.
Do not refresh a revenue slide from orders_daily until Noah explains the three ids.
Next: Noah checks those ids by 16 September.

## Anti-patterns

- A plug to make it balance
- Matching on a name instead of the key
- Ignoring one file

## Related skills

- `account-reconciliation-standard`
- `data-quality-check`
