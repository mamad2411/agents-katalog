---
name: lead-time-review
description: "Compare the lead time in the system to the receipts the user can show. Use when the user mentions lead time review, supplier lead time, system lead time wrong, receipt lag, or asks for a lead-time note. Supply chain skill by Yasir Jilani."
license: MIT
compatibility: Agent Skills standard. No network access, extra packages, or credentials required.
metadata:
  author: Yasir Jilani
  version: "1.0.0"
  domain: supply-chain
---

<!-- GENERATED FILE - edits here are overwritten by scripts/generate.py.
     Edit the 'lead-time-review' entry in source/, then run:
       python3 scripts/generate.py && python3 scripts/validate.py
     See CONTRIBUTING.md. -->

# Lead Time Review

Compare the lead time in the system to the receipts the user can show.

## When to use this skill

Use this skill when the user:

- lead time review
- supplier lead time
- system lead time wrong
- receipt lag

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

- The system lead time
- Recent receipts
- The buyer
- The date the PO was placed

## Workflow


### 1. Step 1

Use receipt dates they have.
### 2. Step 2

If they have fewer than three receipts, say the review is thin.
### 3. Step 3

Do not average in a receipt they excluded.
### 4. Step 4

Recommend a system change only if the gap repeats.
### 5. Step 5

Name who edits the system.
### 6. Step 6

Do not quietly pad the lead time with no receipt.

## Output

Deliver a **lead-time note**.

- Purpose of this lead-time note, in two sentences.
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

The system lead time for Redline Parts on SKU 1044 is 14 days. Diane has three receipts: 26, 28, and 27 days from PO to dock.

### Example data

```text
system lead time: 14 days
receipts: PO 12 Jul to dock 7 Aug (26 days); PO 2 Aug to dock 30 Aug (28); PO 18 Aug to dock 14 Sep (27)
excluded: one air freight in June, she said it is not the pattern
who edits the system: Diane Cho
```

### Example outcome

**Lead-time note**
Three ground receipts: 26, 28, 27 days. The system says 14. The gap repeats.
The June air freight stays out, as she asked.
Recommendation: Diane changes the system to 28 days, matching the slow receipt, not the average dressed up as exact.
Thin? No. Three receipts agree. Still her edit, not an automatic write.
Do not pad further without another receipt.

## Anti-patterns

- A padded lead time with no receipts
- One late truck treated as the new standard
- No owner for the system field

## Related skills

- `inventory-policy`
- `supplier-scorecard`
