---
name: dock-exception-note
description: "Record a dock exception with the count, the PO, and the photo or tally they have. Use when the user mentions dock exception, short shipment, receiving discrepancy, OS&D, or asks for a dock note. Supply chain skill by Yasir Jilani."
license: MIT
compatibility: Agent Skills standard. No network access, extra packages, or credentials required.
metadata:
  author: Yasir Jilani
  version: "1.0.0"
  domain: supply-chain
---

<!-- GENERATED FILE - edits here are overwritten by scripts/generate.py.
     Edit the 'dock-exception-note' entry in source/, then run:
       python3 scripts/generate.py && python3 scripts/validate.py
     See CONTRIBUTING.md. -->

# Dock Exception

Record a dock exception with the count, the PO, and the photo or tally they have.

## When to use this skill

Use this skill when the user:

- dock exception
- short shipment
- receiving discrepancy
- OS&D

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

- The PO
- The tally
- The carrier
- The photo or note

## Workflow


### 1. Step 1

Record counted versus billed.
### 2. Step 2

Attach the PO line.
### 3. Step 3

Do not accuse theft from a short count alone.
### 4. Step 4

Say whether the trailer was sealed, if they noted it.
### 5. Step 5

Name who tells the buyer.
### 6. Step 6

Hold the difference out of available stock until it is resolved.

## Output

Deliver a **dock note**.

- Purpose of this dock note, in two sentences.
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

PO 5521 billed 40 filters. The dock tally is 32. The seal note says intact. No photo. Diane needs the exception before the 32 are marked as 40 in stock.

### Example data

```text
PO: 5521
billed: 40 of SKU 1044
tally: 32
seal: noted intact
photo: none
carrier: Kite Freight
date: 14 Sep 2026
```

### Example outcome

**Dock note — PO 5521**
Short 8. Available stock from this receipt: 32, not 40.
Seal was noted intact. That is not a theft finding. No photo is in the file.
Tell the buyer: Diane. Tell the carrier: after she sends this count, not before.
Do not raise available stock to match the PO while the 8 are open.

## Anti-patterns

- Available stock increased to match the PO
- A theft claim with no evidence
- No PO line

## Related skills

- `logistics-exception`
- `incoming-inspection`
