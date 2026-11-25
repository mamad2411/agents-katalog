---
name: internal-controls-walkthrough
description: "Walk through one process and describe the control as it is actually performed, including where it can fail. Use when the user mentions control walkthrough, internal controls, SOX walkthrough, process control review, or asks for a control walkthrough note. Accounting skill by Yasir Jilani."
license: MIT
compatibility: Agent Skills standard. No network access, extra packages, or credentials required.
metadata:
  author: Yasir Jilani
  version: "1.0.0"
  domain: accounting
---

<!-- GENERATED FILE - edits here are overwritten by scripts/generate.py.
     Edit the 'internal-controls-walkthrough' entry in source/, then run:
       python3 scripts/generate.py && python3 scripts/validate.py
     See CONTRIBUTING.md. -->

# Internal Controls Walkthrough

Walk through one process and describe the control as it is actually performed, including where it can fail.

## When to use this skill

Use this skill when the user:

- control walkthrough
- internal controls
- SOX walkthrough
- process control review

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

- The process
- The risk they care about
- Who performs the control
- Evidence the control produces

## Workflow


### 1. Name the risk

What could go wrong in money, compliance, or reporting terms. A control with no risk is a habit.
### 2. Describe the as-is

Who does what, how often, and what evidence exists. Use the user's description. Do not draw a fantasy flowchart of best practice and call it their process.
### 3. Find gaps

Missing evidence, self-review, or a control that happens after the transaction is already irreversible.
### 4. Distinguish design and operation

You can comment on design from an interview. You cannot say the control operated all year unless they give you samples.
### 5. Recommend one fix

Evidence, a second reviewer, or a system check. A list of twenty improvements will not land.
### 6. No false assurance

This note is not a controls opinion and not a certification.

## Output

Deliver a **control walkthrough note**.

- Purpose of this control walkthrough note, in two sentences.
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

Priya Shah, controller at Northline Studio in Calgary, needs a control walkthrough note by 30 September 2026. The team says vendor payments are 'reviewed' but cannot show what the reviewer looks at.

### Example data

```text
From: Priya Shah, controller
Organization: Northline Studio, Calgary
Date: 14 September 2026
Needed by: 30 September 2026

The team says vendor payments are 'reviewed' but cannot show what the reviewer looks at.

The process: email to Priya Shah. No written steps after 1 Sep 2026
The risk they care about: Operating cash is open. No score in the file
Who performs the control: Priya Shah, controller
Evidence the control produces: one PDF, 2 pages, dated 14 September 2026
```

### Example outcome

**Control walkthrough note**
To: Priya Shah, controller, Northline Studio
Date: 14 September 2026 · Needed by: 30 September 2026

**Decision**
States the risk, describes the review as undocumented, and recommends one evidence fix without claiming certification.

**What the file supports**

| Input | Value | Status |
| --- | --- | --- |
| The process | email to Priya Shah. No written steps after 1 Sep 2026 | Needs confirmation |
| The risk they care about | Operating cash is open. No score in the file | Carried into the draft |
| Who performs the control | Priya Shah, controller | Carried into the draft |
| Evidence the control produces | one PDF, 2 pages, dated 14 September 2026 | Needs confirmation |

**How this draft was built**

**1. Name the risk**  
What could go wrong in money, compliance, or reporting terms. A control with no risk is a habit.

**2. Describe the as-is**  
Who does what, how often, and what evidence exists. Use the user's description. Do not draw a fantasy flowchart of best practice and call it their process.

**3. Find gaps**  
Missing evidence, self-review, or a control that happens after the transaction is already irreversible.

**4. Distinguish design and operation**  
You can comment on design from an interview. You cannot say the control operated all year unless they give you samples.

**5. Recommend one fix**  
Evidence, a second reviewer, or a system check. A list of twenty improvements will not land.

**Deliberately not done**
- A best-practice narrative presented as their process.
- Claiming the control operated all year from one interview.
- A certification no one issued.

**Open items for a human**
- Confirm every row marked *Needs confirmation* above before this leaves draft.
- Anything absent from the file stayed absent. No figure, date, or name was supplied from outside it.

Next: Priya Shah by 30 September 2026. This is a draft, not a sign-off.

## Anti-patterns

- A best-practice narrative presented as their process.
- Claiming the control operated all year from one interview.
- A certification no one issued.

## Related skills

- `control-design`
- `accounts-payable-control`
- `sox-walkthrough`
