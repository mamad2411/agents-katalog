---
name: supplier-risk-note
description: "Note a supplier risk from the evidence the buyer has, without a mood score. Use when the user mentions supplier risk, vendor risk, single source, supply risk, or asks for a risk note. Supply chain skill by Yasir Jilani."
license: MIT
compatibility: Agent Skills standard. No network access, extra packages, or credentials required.
metadata:
  author: Yasir Jilani
  version: "1.0.0"
  domain: supply-chain
---

<!-- GENERATED FILE - edits here are overwritten by scripts/generate.py.
     Edit the 'supplier-risk-note' entry in source/, then run:
       python3 scripts/generate.py && python3 scripts/validate.py
     See CONTRIBUTING.md. -->

# Supplier Risk Note

Note a supplier risk from the evidence the buyer has, without a mood score.

## When to use this skill

Use this skill when the user:

- supplier risk
- vendor risk
- single source
- supply risk

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

- The supplier
- The part
- The evidence
- The alternate if they have one

## Workflow


### 1. Step 1

State the part and the supplier.
### 2. Step 2

Use only the miss, the lead time, or the single-source fact they showed.
### 3. Step 3

If there is no alternate, say so.
### 4. Step 4

Do not invent a financial score.
### 5. Step 5

Recommend a cover action they can take this month.
### 6. Step 6

Do not blame the supplier for a forecast they doubled.

## Output

Deliver a **risk note**.

- Purpose of this risk note, in two sentences.
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

Harbor Goods buys SKU 1044 cabin filters only from Redline Parts. Lead time is 28 days. In August they were short 14 units. There is no second supplier in the file.

### Example data

```text
supplier: Redline Parts
sku: 1044 cabin filter
lead time in system: 28 days
August miss: 14 units, receipt 28 Aug 2026
alternate: none on file
buyer-caused forecast change: not in this file
cover Diane can place: a 2-week bridge buy if she finds a second quote
```

### Example outcome

**Risk note — SKU 1044**
Single source. 28-day lead time. August miss: 14 units. That is the evidence. No credit score is in the file, so none is written.

No alternate is on file. That is the risk, not a mood.
Cover this month: Diane gets one second quote, or she accepts the 28-day exposure. This note does not pick a vendor for her.
Do not add a forecast-blame line. None was in the file.

## Anti-patterns

- A credit score from memory
- A risk color with no evidence
- Ignoring buyer-caused misses

## Related skills

- `supplier-scorecard`
- `shortage-playbook`
