---
name: sku-cut-review
description: "Propose SKUs to stop reordering from the movement and the stock the user shows. Use when the user mentions SKU rationalization, what should we stop buying, dead stock, range cut, or asks for a cut list. Supply chain skill by Yasir Jilani."
license: MIT
compatibility: Agent Skills standard. No network access, extra packages, or credentials required.
metadata:
  author: Yasir Jilani
  version: "1.0.0"
  domain: supply-chain
---

<!-- GENERATED FILE - edits here are overwritten by scripts/generate.py.
     Edit the 'sku-cut-review' entry in source/, then run:
       python3 scripts/generate.py && python3 scripts/validate.py
     See CONTRIBUTING.md. -->

# SKU Cut Review

Propose SKUs to stop reordering from the movement and the stock the user shows.

## When to use this skill

Use this skill when the user:

- SKU rationalization
- what should we stop buying
- dead stock
- range cut

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

- The SKUs
- Units sold in their window
- Stock on hand
- A SKU they must keep

## Workflow


### 1. Step 1

Rank by the movement they showed.
### 2. Step 2

A must-keep SKU stays even if it is slow.
### 3. Step 3

Do not cut a SKU because a template says so.
### 4. Step 4

Separate a seasonal item if they said it is seasonal.
### 5. Step 5

Recommend stop-reorder, not a fake write-off.
### 6. Step 6

Name who approves the cut.

## Output

Deliver a **cut list**.

- Purpose of this cut list, in two sentences.
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

Four SKUs sold zero units in 90 days. One is a winter blade Diane says they must keep for November. All four still have stock on the shelf.

### Example data

```text
window: 16 Jun to 14 Sep 2026
SKU 1044 filters: 0 sold, 18 on hand
SKU 2201 wiper: 0 sold, 6 on hand
SKU 2208 mat: 0 sold, 4 on hand
SKU 3310 winter blade: 0 sold, 20 on hand, must keep for November
approver: Diane
```

### Example outcome

**Stop-reorder**
| SKU | Sold | On hand | Call |
| --- | --- | --- | --- |
| 1044 | 0 | 18 | stop reorder |
| 2201 | 0 | 6 | stop reorder |
| 2208 | 0 | 4 | stop reorder |
| 3310 | 0 | 20 | keep, winter |

This is not a write-off and not a savings number. Stock stays on the shelf until she decides a clearance. Approver: Diane.

## Anti-patterns

- A cut list with no sales file
- Cutting a protected SKU
- A write-off invented as savings

## Related skills

- `inventory-policy`
- `assortment-review`
