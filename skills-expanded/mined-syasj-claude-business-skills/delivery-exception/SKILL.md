---
name: delivery-exception
description: "Handle a failed delivery with a new promise you can keep and a reason the customer can understand. Use when the user mentions failed delivery, delivery exception, missed stop, redelivery plan, or asks for a delivery exception. Transport and logistics operations skill by Yasir Jilani."
license: MIT
compatibility: Agent Skills standard. No network access, extra packages, or credentials required.
metadata:
  author: Yasir Jilani
  version: "1.0.0"
  domain: transport
---

<!-- GENERATED FILE - edits here are overwritten by scripts/generate.py.
     Edit the 'delivery-exception' entry in source/, then run:
       python3 scripts/generate.py && python3 scripts/validate.py
     See CONTRIBUTING.md. -->

# Delivery Exception

Handle a failed delivery with a new promise you can keep and a reason the customer can understand.

## When to use this skill

Use this skill when the user:

- failed delivery
- delivery exception
- missed stop
- redelivery plan

## When not to use this skill

- The user wants a different domain's specialist skill.
- The task requires a licensed professional to decide, and the user only needs a referral note rather than a draft.
- The request asks you to deceive, evade a control, or hide material facts.

## Professional boundary

Transport plans follow hours, load, and safety rules the user states. Do not advise concealment of cargo or evasion of inspections.

## Operating boundaries

- Use only information the user provides or files they explicitly ask you to read. Do not invent metrics, laws, citations, prices, credentials, or clinical facts.
- Do not ask for passwords, API keys, tokens, seed phrases, one-time codes, or payment card data.
- Do not send data to an external service, install packages, or add network calls as part of this skill.
- Separate facts, assumptions, and recommendations. If a required input is missing, state the assumption or ask one focused question.
- If the user asks you to deceive a person, evade a control, forge a record, or cause harm, stop. Offer a legitimate alternative.
- Work product that affects money, employment, health, safety, or legal rights is a draft for a qualified human to review before it is used.

## Inputs to collect

- The failure reason
- The customer's instruction
- Options
- The next honest window

## Workflow


### 1. Step 1

Record the reason they know.
### 2. Offer options they can perform

redelivery, pickup, or hold.
### 3. Step 3

Do not promise a window the route cannot make.
### 4. Step 4

Tell the customer the truth without blaming them for a company miss.
### 5. Step 5

Update the order status so the next driver sees it.
### 6. Step 6

Escalate perishable or sensitive loads under their rule.

## Output

Deliver a **delivery exception**.

- Purpose of this delivery exception, in two sentences.
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

Luis Ortega, dispatch lead at Kite Freight in Calgary, needs a delivery exception by 30 September 2026. A text says the parcel was delivered though the driver marked an access failure.

### Example data

```text
From: Luis Ortega, dispatch lead
Organization: Kite Freight, Calgary
Date: 14 September 2026
Needed by: 30 September 2026

A text says the parcel was delivered though the driver marked an access failure.

The failure reason: Calgary-Edmonton lane, first seen 14 September 2026. No root cause recorded yet
The customer's instruction: Calgary-Edmonton lane, recorded 14 September 2026. No supporting file attached
Options: keep Calgary-Edmonton lane, or stop. No third option written
The next honest window: two deals cited from memory. Neither has a written loss reason
```

### Example outcome

**Delivery exception**
To: Luis Ortega, dispatch lead, Kite Freight
Date: 14 September 2026 · Needed by: 30 September 2026

**Decision**
Corrects the status and offers a real redelivery window.

**What the file supports**

| Input | Value | Status |
| --- | --- | --- |
| The failure reason | Calgary-Edmonton lane, first seen 14 September 2026. No root cause recorded yet | Needs confirmation |
| The customer's instruction | Calgary-Edmonton lane, recorded 14 September 2026. No supporting file attached | Carried into the draft |
| Options | keep Calgary-Edmonton lane, or stop. No third option written | Carried into the draft |
| The next honest window | two deals cited from memory. Neither has a written loss reason | Needs confirmation |

**How this draft was built**

**1. Record the reason they know**

**2. Offer options they can perform**  
redelivery, pickup, or hold.

**3. Do not promise a window the route cannot make**

**4. Tell the customer the truth without blaming them for a company miss**

**5. Update the order status so the next driver sees it**

**Deliberately not done**
- A window the route cannot make.
- A blame-the-customer template.
- A status left stale.

**Open items for a human**
- Confirm every row marked *Needs confirmation* above before this leaves draft.
- Anything absent from the file stayed absent. No figure, date, or name was supplied from outside it.

Next: Luis Ortega by 30 September 2026. This is a draft, not a sign-off.

## Anti-patterns

- A window the route cannot make
- A blame-the-customer template
- A status left stale

## Related skills

- `logistics-exception`
- `customer-communication-incident`
