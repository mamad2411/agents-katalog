---
name: fixed-asset-register
description: "Review a fixed-asset register so additions, disposals, and depreciation have an owner and a trail. Use when the user mentions fixed asset register, depreciation review, asset disposal, capital versus expense, or asks for a fixed-asset register review. Accounting skill by Yasir Jilani."
license: MIT
compatibility: Agent Skills standard. No network access, extra packages, or credentials required.
metadata:
  author: Yasir Jilani
  version: "1.0.0"
  domain: accounting
---

<!-- GENERATED FILE - edits here are overwritten by scripts/generate.py.
     Edit the 'fixed-asset-register' entry in source/, then run:
       python3 scripts/generate.py && python3 scripts/validate.py
     See CONTRIBUTING.md. -->

# Fixed Asset Register

Review a fixed-asset register so additions, disposals, and depreciation have an owner and a trail.

## When to use this skill

Use this skill when the user:

- fixed asset register
- depreciation review
- asset disposal
- capital versus expense

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

- Register and GL balances
- Capitalization threshold
- Recent additions and disposals
- Useful lives they claim to use

## Workflow


### 1. Tie the register to the GL

Gross cost, accumulated depreciation, and net book value. A register that does not tie is the finding.
### 2. Test additions against the threshold

Items under the threshold that were capitalized, or over it that were expensed, get a question. Do not rewrite their policy from memory.
### 3. Disposals

A disposed asset needs a date and a proceed or a statement that proceeds were zero. Ghost assets still depreciating are a finding.
### 4. Lives and methods

Flag inconsistencies inside their stated policy. Do not impose a new life because it 'feels standard'.
### 5. Physical existence

Recommend a sample check for assets the user says have gone missing. Do not invent a count.
### 6. Draft adjustments

Propose, do not post. Label any fully depreciated asset still in use as a policy question, not as an error by itself.

## Output

Deliver a **fixed-asset register review**.

- Purpose of this fixed-asset register review, in two sentences.
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

Priya Shah, controller at Northline Studio in Calgary, needs a fixed-asset register review by 30 September 2026. The register net book value does not match the GL, and several laptops are still depreciating after people left.

### Example data

```text
From: Priya Shah, controller
Organization: Northline Studio, Calgary
Date: 14 September 2026
Needed by: 30 September 2026

The register net book value does not match the GL, and several laptops are still depreciating after people left.

Register and GL balances: Undeposited funds, recorded 14 September 2026. No supporting file attached
Capitalization threshold: their one-page rule dated 2 Mar 2026. No exception log since
Recent additions and disposals: Sales tax payable. Partly documented: the what is written down, the who is not
Useful lives they claim to use: the draft sentence is broader than the note
```

### Example outcome

**Fixed-asset register review**
To: Priya Shah, controller, Northline Studio
Date: 14 September 2026 · Needed by: 30 September 2026

**Decision**
Leads with the tie-out break, lists disposal questions, and proposes sample checks rather than silent write-offs.

**What the file supports**

| Input | Value | Status |
| --- | --- | --- |
| Register and GL balances | Undeposited funds, recorded 14 September 2026. No supporting file attached | Needs confirmation |
| Capitalization threshold | their one-page rule dated 2 Mar 2026. No exception log since | Carried into the draft |
| Recent additions and disposals | Sales tax payable. Partly documented: the what is written down, the who is not | Carried into the draft |
| Useful lives they claim to use | the draft sentence is broader than the note | Needs confirmation |

**How this draft was built**

**1. Tie the register to the GL**  
Gross cost, accumulated depreciation, and net book value. A register that does not tie is the finding.

**2. Test additions against the threshold**  
Items under the threshold that were capitalized, or over it that were expensed, get a question. Do not rewrite their policy from memory.

**3. Disposals**  
A disposed asset needs a date and a proceed or a statement that proceeds were zero. Ghost assets still depreciating are a finding.

**4. Lives and methods**  
Flag inconsistencies inside their stated policy. Do not impose a new life because it 'feels standard'.

**5. Physical existence**  
Recommend a sample check for assets the user says have gone missing. Do not invent a count.

**Deliberately not done**
- Inventing useful lives.
- Ignoring a register that does not tie.
- Writing off assets with no user evidence.

**Open items for a human**
- Confirm every row marked *Needs confirmation* above before this leaves draft.
- Anything absent from the file stayed absent. No figure, date, or name was supplied from outside it.

Next: Priya Shah by 30 September 2026. This is a draft, not a sign-off.

## Anti-patterns

- Inventing useful lives.
- Ignoring a register that does not tie.
- Writing off assets with no user evidence.

## Related skills

- `capex-business-case`
- `month-end-close`
- `internal-controls-walkthrough`
