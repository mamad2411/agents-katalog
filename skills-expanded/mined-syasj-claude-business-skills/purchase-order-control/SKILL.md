---
name: purchase-order-control
description: "Review purchase-order control so orders are approved, received, and matched without informal side deals. Use when the user mentions purchase order control, PO process, three-way match, buying controls, or asks for a PO control review. Supply chain skill by Yasir Jilani."
license: MIT
compatibility: Agent Skills standard. No network access, extra packages, or credentials required.
metadata:
  author: Yasir Jilani
  version: "1.0.0"
  domain: supply-chain
---

<!-- GENERATED FILE - edits here are overwritten by scripts/generate.py.
     Edit the 'purchase-order-control' entry in source/, then run:
       python3 scripts/generate.py && python3 scripts/validate.py
     See CONTRIBUTING.md. -->

# Purchase Order Control

Review purchase-order control so orders are approved, received, and matched without informal side deals.

## When to use this skill

Use this skill when the user:

- purchase order control
- PO process
- three-way match
- buying controls

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

- Who can raise and approve
- Receipt practice
- Match exceptions
- Known side arrangements

## Workflow


### 1. Step 1

Map raise, approve, receive, and pay. Note where one person does two steps.
### 2. Step 2

A side arrangement with no PO is a finding.
### 3. Step 3

Receipt should evidence that goods or services arrived.
### 4. Step 4

Match exceptions need an owner, not a permanent override.
### 5. Step 5

Do not help conceal a purchase from the required approver.
### 6. Step 6

Recommend the smallest control that would have caught their last miss.

## Output

Deliver a **PO control review**.

- Purpose of this PO control review, in two sentences.
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

Diane Cho, supply lead at Harbor Goods in Airdrie, needs a PO control review by 30 September 2026. A team lead emails a supplier directly to avoid the PO system.

### Example data

```text
From: Diane Cho, supply lead
Organization: Harbor Goods, Airdrie
Date: 14 September 2026
Needed by: 30 September 2026

A team lead emails a supplier directly to avoid the PO system.

Who can raise and approve: Diane Cho, supply lead
Receipt practice: Calgary-Edmonton lane. Partly documented: the what is written down, the who is not
Match exceptions: SKU 1044 cabin filter is open. Redline Parts was raised verbally and never logged
Known side arrangements: Redline Parts. Stated in the ask, not documented anywhere else
```

### Example outcome

**Po control review**
To: Diane Cho, supply lead, Harbor Goods
Date: 14 September 2026 · Needed by: 30 September 2026

**Decision**
Treats the email order as a control break and names the missing approval.

**What the file supports**

| Input | Value | Status |
| --- | --- | --- |
| Who can raise and approve | Diane Cho, supply lead | Needs confirmation |
| Receipt practice | Calgary-Edmonton lane. Partly documented: the what is written down, the who is not | Carried into the draft |
| Match exceptions | SKU 1044 cabin filter is open. Redline Parts was raised verbally and never logged | Carried into the draft |
| Known side arrangements | Redline Parts. Stated in the ask, not documented anywhere else | Needs confirmation |

**How this draft was built**

**1. Map raise, approve, receive, and pay. Note where one person does two steps**

**2. A side arrangement with no PO is a finding**

**3. Receipt should evidence that goods or services arrived**

**4. Match exceptions need an owner, not a permanent override**

**5. Do not help conceal a purchase from the required approver**

**Deliberately not done**
- Concealing a purchase.
- A permanent match override.
- One person ordering and approving.

**Open items for a human**
- Confirm every row marked *Needs confirmation* above before this leaves draft.
- Anything absent from the file stayed absent. No figure, date, or name was supplied from outside it.

Next: Diane Cho by 30 September 2026. This is a draft, not a sign-off.

## Anti-patterns

- Concealing a purchase
- A permanent match override
- One person ordering and approving

## Related skills

- `accounts-payable-control`
- `procurement-award-note`
