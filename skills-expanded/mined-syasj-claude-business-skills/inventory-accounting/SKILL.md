---
name: inventory-accounting
description: "Review inventory accounting issues: cut-off, obsolescence, and the tie between the count and the ledger. Use when the user mentions inventory accounting, stock valuation, obsolescence, inventory count tie-out, or asks for a inventory accounting review. Accounting skill by Yasir Jilani."
license: MIT
compatibility: Agent Skills standard. No network access, extra packages, or credentials required.
metadata:
  author: Yasir Jilani
  version: "1.0.0"
  domain: accounting
---

<!-- GENERATED FILE - edits here are overwritten by scripts/generate.py.
     Edit the 'inventory-accounting' entry in source/, then run:
       python3 scripts/generate.py && python3 scripts/validate.py
     See CONTRIBUTING.md. -->

# Inventory Accounting Review

Review inventory accounting issues: cut-off, obsolescence, and the tie between the count and the ledger.

## When to use this skill

Use this skill when the user:

- inventory accounting
- stock valuation
- obsolescence
- inventory count tie-out

## When not to use this skill

- The user wants a different domain's specialist skill.
- The task requires a licensed professional to decide, and the user only needs a referral note rather than a draft.
- The request asks you to deceive, evade a control, or hide material facts.

## Professional boundary

This is not an audit opinion, compilation, or tax advice. Do not invent accounting standards. Use the policy, framework, and chart of accounts the organization actually follows.

## Operating boundaries

- Use only information the user provides or files they explicitly ask you to read. Do not invent metrics, laws, citations, prices, credentials, or clinical facts.
- Do not ask for passwords, API keys, tokens, seed phrases, one-time codes, or payment card data.
- Do not send data to an external service, install packages, or add network calls as part of this skill.
- Separate facts, assumptions, and recommendations. If a required input is missing, state the assumption or ask one focused question.
- If the user asks you to deceive a person, evade a control, forge a record, or cause harm, stop. Offer a legitimate alternative.
- Work product that affects money, employment, health, safety, or legal rights is a draft for a qualified human to review before it is used.

## Inputs to collect

- Count and GL figures
- Costing method they use
- Slow or damaged stock they know about
- Cut-off concerns

## Workflow


### 1. Tie count to GL

Quantity times their cost, rolled to the balance. Explain any difference as timing, cost layer, or unknown.
### 2. Cut-off

Goods received or shipped around period end need a status. Do not assume title transferred.
### 3. Obsolescence

Use their evidence of age, damage, or expired demand. A reserve without evidence is a plug. A zero reserve despite their evidence is a question.
### 4. Costing method

Describe the method they say they use. Do not switch them to another method casually.
### 5. Standard cost variances

If they use standards, variances need a disposition. Unreviewed variances are not inventory gospel.
### 6. Hand off judgment

The reserve percentage is for the accounting owner. You prepare the fact pattern.

## Output

Deliver a **inventory accounting review**.

- Purpose of this inventory accounting review, in two sentences.
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

Priya Shah, controller at Northline Studio in Calgary, needs an inventory accounting review by 30 September 2026. A year-end count is short of the GL, and the warehouse says some goods were shipped but still in the system.

### Example data

```text
From: Priya Shah, controller
Organization: Northline Studio, Calgary
Date: 14 September 2026
Needed by: 30 September 2026

A year-end count is short of the GL, and the warehouse says some goods were shipped but still in the system.

Count and GL figures: 40 in the last period. No prior period attached, so no trend
Costing method they use: CAD 36 direct. Overhead not in this line
Slow or damaged stock they know about: Undeposited funds, recorded 14 September 2026. No supporting file attached
Cut-off concerns: Operating cash. Stated in the ask, not documented anywhere else
```

### Example outcome

**Inventory accounting review**
To: Priya Shah, controller, Northline Studio
Date: 14 September 2026 · Needed by: 30 September 2026

**Decision**
Isolates the shipped-not-relieved population and asks for cut-off evidence before anyone books a shrinkage number.

**What the file supports**

| Input | Value | Status |
| --- | --- | --- |
| Count and GL figures | 40 in the last period. No prior period attached, so no trend | Needs confirmation |
| Costing method they use | CAD 36 direct. Overhead not in this line | Carried into the draft |
| Slow or damaged stock they know about | Undeposited funds, recorded 14 September 2026. No supporting file attached | Carried into the draft |
| Cut-off concerns | Operating cash. Stated in the ask, not documented anywhere else | Needs confirmation |

**How this draft was built**

**1. Tie count to GL**  
Quantity times their cost, rolled to the balance. Explain any difference as timing, cost layer, or unknown.

**2. Cut-off**  
Goods received or shipped around period end need a status. Do not assume title transferred.

**3. Obsolescence**  
Use their evidence of age, damage, or expired demand. A reserve without evidence is a plug. A zero reserve despite their evidence is a question.

**4. Costing method**  
Describe the method they say they use. Do not switch them to another method casually.

**5. Standard cost variances**  
If they use standards, variances need a disposition. Unreviewed variances are not inventory gospel.

**Deliberately not done**
- A reserve percentage copied from a textbook.
- Ignoring cut-off.
- Changing costing method as a formatting choice.

**Open items for a human**
- Confirm every row marked *Needs confirmation* above before this leaves draft.
- Anything absent from the file stayed absent. No figure, date, or name was supplied from outside it.

Next: Priya Shah by 30 September 2026. This is a draft, not a sign-off.

## Anti-patterns

- A reserve percentage copied from a textbook.
- Ignoring cut-off.
- Changing costing method as a formatting choice.

## Related skills

- `inventory-policy`
- `incoming-inspection`
- `month-end-close`
