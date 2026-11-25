---
name: customs-packet-check
description: "Check a shipment packet for the documents the user says the lane requires. Use when the user mentions customs documents, shipping packet, commercial invoice check, export packet, or asks for a packet check. Supply chain skill by Yasir Jilani."
license: MIT
compatibility: Agent Skills standard. No network access, extra packages, or credentials required.
metadata:
  author: Yasir Jilani
  version: "1.0.0"
  domain: supply-chain
---

<!-- GENERATED FILE - edits here are overwritten by scripts/generate.py.
     Edit the 'customs-packet-check' entry in source/, then run:
       python3 scripts/generate.py && python3 scripts/validate.py
     See CONTRIBUTING.md. -->

# Customs Packet Check

Check a shipment packet for the documents the user says the lane requires.

## When to use this skill

Use this skill when the user:

- customs documents
- shipping packet
- commercial invoice check
- export packet

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

- Their required list
- Documents in the packet
- The lane
- Who files

## Workflow


### 1. Step 1

Compare the packet to their list.
### 2. Step 2

Mark missing items.
### 3. Step 3

Do not suggest a false description or a lower value.
### 4. Step 4

Do not advise hiding goods.
### 5. Step 5

Name who must complete a missing form.
### 6. Step 6

This is a checklist, not a brokerage opinion.

## Output

Deliver a **packet check**.

- Purpose of this packet check, in two sentences.
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

A packet for filters from Calgary to a US customer is missing the commercial invoice. A note in the folder suggests describing them as samples so the value line can be blank.

### Example data

```text
lane: Calgary to US customer, her required list
required: commercial invoice, packing list, COO if the customer asked
in the packet: packing list, no invoice, no COO ask on file
suggestion in the folder: call them samples
value on the PO: 40 filters, $18 each
who files: the forwarder, after her packet is complete
```

### Example outcome

**Packet check**
Hold. The commercial invoice is missing.
Do not describe the filters as samples. The PO says 40 filters at $18. A false description is not a fix.
COO: not required in her list for this shipment. Do not add one to look busy.
Who completes the invoice: Diane, then the forwarder files. This check is not a brokerage opinion.

## Anti-patterns

- A false commodity description
- A lowered value
- A packet marked complete with a hole

## Related skills

- `landed-cost`
- `logistics-exception`
