---
name: third-party-risk
description: "Screen a third party for the risk created by the access and data you will give them. Use when the user mentions third-party risk, vendor risk, supplier risk review, outsourcing risk, or asks for a third-party risk note. Risk and compliance skill by Yasir Jilani."
license: MIT
compatibility: Agent Skills standard. No network access, extra packages, or credentials required.
metadata:
  author: Yasir Jilani
  version: "1.0.0"
  domain: risk
---

<!-- GENERATED FILE - edits here are overwritten by scripts/generate.py.
     Edit the 'third-party-risk' entry in source/, then run:
       python3 scripts/generate.py && python3 scripts/validate.py
     See CONTRIBUTING.md. -->

# Third-Party Risk

Screen a third party for the risk created by the access and data you will give them.

## When to use this skill

Use this skill when the user:

- third-party risk
- vendor risk
- supplier risk review
- outsourcing risk

## When not to use this skill

- The user wants a different domain's specialist skill.
- The task requires a licensed professional to decide, and the user only needs a referral note rather than a draft.
- The request asks you to deceive, evade a control, or hide material facts.

## Professional boundary

Risk work prioritizes uncertainty. It is not a certification. Do not claim SOC 2, ISO, HIPAA, or similar compliance unless the user has evidence of it.

## Operating boundaries

- Use only information the user provides or files they explicitly ask you to read. Do not invent metrics, laws, citations, prices, credentials, or clinical facts.
- Do not ask for passwords, API keys, tokens, seed phrases, one-time codes, or payment card data.
- Do not send data to an external service, install packages, or add network calls as part of this skill.
- Separate facts, assumptions, and recommendations. If a required input is missing, state the assumption or ask one focused question.
- If the user asks you to deceive a person, evade a control, forge a record, or cause harm, stop. Offer a legitimate alternative.
- Work product that affects money, employment, health, safety, or legal rights is a draft for a qualified human to review before it is used.

## Inputs to collect

- The service
- Data and access involved
- Their evidence
- The business owner

## Workflow


### 1. Step 1

Rate inherent risk from access and data, in plain tiers you label as a proposal if they have no method.
### 2. Step 2

Review only evidence they collected. A missing questionnaire is a gap.
### 3. Step 3

Recommend a lighter review for low access and a deeper one for sensitive data.
### 4. Step 4

Name the business owner who accepts residual risk.
### 5. Step 5

Tie contract questions to the legal and security skills. Do not duplicate a fake certification.
### 6. Step 6

Re-review on a date or when the service changes.

## Output

Deliver a **third-party risk note**.

- Purpose of this third-party risk note, in two sentences.
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

Priya Shah, controller at Northline Studio in Calgary, needs a third-party risk note by 30 September 2026. A design tool and a payroll processor are put through an identical unread checklist.

### Example data

```text
From: Priya Shah, controller
Organization: Northline Studio, Calgary
Date: 14 September 2026
Needed by: 30 September 2026

A design tool and a payroll processor are put through an identical unread checklist.

The service: the one named in the ask. Version and owner not recorded
Data and access involved: Control 7.2 access review. Partly documented: the what is written down, the who is not
Their evidence: one PDF, 2 pages, dated 14 September 2026
The business owner: Priya Shah, controller
```

### Example outcome

**Third-party risk note**
To: Priya Shah, controller, Northline Studio
Date: 14 September 2026 · Needed by: 30 September 2026

**Decision**
Deepens the payroll review, lightens the design-tool review, and names the owner.

**What the file supports**

| Input | Value | Status |
| --- | --- | --- |
| The service | the one named in the ask. Version and owner not recorded | Needs confirmation |
| Data and access involved | Control 7.2 access review. Partly documented: the what is written down, the who is not | Carried into the draft |
| Their evidence | one PDF, 2 pages, dated 14 September 2026 | Carried into the draft |
| The business owner | Priya Shah, controller | Needs confirmation |

**How this draft was built**

**1. Rate inherent risk from access and data, in plain tiers you label as a proposal if they have no method**

**2. Review only evidence they collected. A missing questionnaire is a gap**

**3. Recommend a lighter review for low access and a deeper one for sensitive data**

**4. Name the business owner who accepts residual risk**

**5. Tie contract questions to the legal and security skills. Do not duplicate a fake certification**

**Deliberately not done**
- The same heavy review for every vendor regardless of data.
- A pass with no evidence.
- No business owner.

**Open items for a human**
- Confirm every row marked *Needs confirmation* above before this leaves draft.
- Anything absent from the file stayed absent. No figure, date, or name was supplied from outside it.

Next: Priya Shah by 30 September 2026. This is a draft, not a sign-off.

## Anti-patterns

- The same heavy review for every vendor regardless of data
- A pass with no evidence
- No business owner

## Related skills

- `vendor-security-review`
- `vendor-ops-review`
