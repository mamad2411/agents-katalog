---
name: expense-policy
description: "Draft a usable expense policy: what is allowed, who approves, and what evidence is required. Use when the user mentions expense policy, T&E policy, employee expenses, reimbursement rules, or asks for a expense policy draft. Accounting skill by Yasir Jilani."
license: MIT
compatibility: Agent Skills standard. No network access, extra packages, or credentials required.
metadata:
  author: Yasir Jilani
  version: "1.0.0"
  domain: accounting
---

<!-- GENERATED FILE - edits here are overwritten by scripts/generate.py.
     Edit the 'expense-policy' entry in source/, then run:
       python3 scripts/generate.py && python3 scripts/validate.py
     See CONTRIBUTING.md. -->

# Expense Policy Draft

Draft a usable expense policy: what is allowed, who approves, and what evidence is required.

## When to use this skill

Use this skill when the user:

- expense policy
- T&E policy
- employee expenses
- reimbursement rules

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

- Current pain: late claims, unclear limits, or abuse concerns
- Approval limits
- Categories they want covered
- Local rules they already know apply

## Workflow


### 1. Write the purpose

Fair reimbursement of business spend, not a surveillance program.
### 2. Define allowed and not allowed

Use categories they named. Where they are unsure, mark a decision for leadership rather than inventing a moral rule.
### 3. Evidence

Receipt threshold, attendees for meals if they want that, and the business reason. Do not require excessive personal data.
### 4. Approvals

Manager plus a second look above a limit they set. Self-approval is called out as a gap.
### 5. Timing

How soon a claim is submitted and paid. A policy nobody can follow will be ignored.
### 6. Exceptions

Who can approve an exception and how it is logged. Quiet exceptions become the real policy.

## Output

Deliver a **expense policy draft**.

- Purpose of this expense policy draft, in two sentences.
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

Priya Shah, controller at Northline Studio in Calgary, needs an expense policy draft by 30 September 2026. Managers are approving their own travel after the fact, and finance wants a one-page policy.

### Example data

```text
From: Priya Shah, controller
Organization: Northline Studio, Calgary
Date: 14 September 2026
Needed by: 30 September 2026

Managers are approving their own travel after the fact, and finance wants a one-page policy.

Current pain: late claims, unclear limits, or abuse concerns: late claims: in the file; unclear limits: not in the file; abuse concerns: open
Approval limits: Undeposited funds. Partly documented: the what is written down, the who is not
Categories they want covered: Operating cash, recorded 14 September 2026. No supporting file attached
Local rules they already know apply: their one-page rule dated 2 Mar 2026. No exception log since
```

### Example outcome

**Expense policy draft**
To: Priya Shah, controller, Northline Studio
Date: 14 September 2026 · Needed by: 30 September 2026

**Decision**
A draft with limits, evidence, a ban on self-approval above a threshold, and a logged exception path. Tax treatment is left to their advisor.

**What the file supports**

| Input | Value | Status |
| --- | --- | --- |
| Current pain: late claims, unclear limits, or abuse concerns | late claims: in the file; unclear limits: not in the file; abuse concerns: open | Needs confirmation |
| Approval limits | Undeposited funds. Partly documented: the what is written down, the who is not | Carried into the draft |
| Categories they want covered | Operating cash, recorded 14 September 2026. No supporting file attached | Carried into the draft |
| Local rules they already know apply | their one-page rule dated 2 Mar 2026. No exception log since | Needs confirmation |

**How this draft was built**

**1. Write the purpose**  
Fair reimbursement of business spend, not a surveillance program.

**2. Define allowed and not allowed**  
Use categories they named. Where they are unsure, mark a decision for leadership rather than inventing a moral rule.

**3. Evidence**  
Receipt threshold, attendees for meals if they want that, and the business reason. Do not require excessive personal data.

**4. Approvals**  
Manager plus a second look above a limit they set. Self-approval is called out as a gap.

**5. Timing**  
How soon a claim is submitted and paid. A policy nobody can follow will be ignored.

**Deliberately not done**
- A punitive policy that reads like a trap.
- No exception path.
- Inventing tax deductibility rules.

**Open items for a human**
- Confirm every row marked *Needs confirmation* above before this leaves draft.
- Anything absent from the file stayed absent. No figure, date, or name was supplied from outside it.

Next: Priya Shah by 30 September 2026. This is a draft, not a sign-off.

## Anti-patterns

- A punitive policy that reads like a trap.
- No exception path.
- Inventing tax deductibility rules.

## Related skills

- `accounts-payable-control`
- `gifts-and-entertainment`
- `payroll-accounting-review`
