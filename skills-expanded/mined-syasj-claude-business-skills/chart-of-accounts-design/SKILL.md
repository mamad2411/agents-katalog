---
name: chart-of-accounts-design
description: "Design a chart of accounts people can code to, with enough detail to manage and not so much that nobody agrees. Use when the user mentions chart of accounts, GL structure, account coding, too many accounts, or asks for a chart of accounts proposal. Accounting skill by Yasir Jilani."
license: MIT
compatibility: Agent Skills standard. No network access, extra packages, or credentials required.
metadata:
  author: Yasir Jilani
  version: "1.0.0"
  domain: accounting
---

<!-- GENERATED FILE - edits here are overwritten by scripts/generate.py.
     Edit the 'chart-of-accounts-design' entry in source/, then run:
       python3 scripts/generate.py && python3 scripts/validate.py
     See CONTRIBUTING.md. -->

# Chart of Accounts Design

Design a chart of accounts people can code to, with enough detail to manage and not so much that nobody agrees.

## When to use this skill

Use this skill when the user:

- chart of accounts
- GL structure
- account coding
- too many accounts

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

- Entities and departments that must report
- Decisions the accounts must support
- Current pain: miscoding or useless detail
- External reporting framework they claim to use

## Workflow


### 1. Start from decisions

Which margins, locations, or funding sources must be visible without a side spreadsheet.
### 2. Separate posting accounts from reporting groups

People post to stable accounts. Reports roll them up. Do not make every report slice a new account.
### 3. Write definitions

Each new or changed account gets a one-line definition and an example of what does not belong in it.
### 4. Cap the depth

Recommend a department or class dimension instead of exploding the natural account list, when their system supports it. If you do not know the system, ask before redesigning.
### 5. Plan the map

Old account to new account. Unmapped balances are how conversions fail.
### 6. Name the owner

Someone approves new accounts. A chart without an owner decays in a quarter.

## Output

Deliver a **chart of accounts proposal**.

- Purpose of this chart of accounts proposal, in two sentences.
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

Priya Shah, controller at Northline Studio in Calgary, needs a chart of accounts proposal by 30 September 2026. A growing firm has 400 accounts and still cannot see gross margin by service line.

### Example data

```text
From: Priya Shah, controller
Organization: Northline Studio, Calgary
Date: 14 September 2026
Needed by: 30 September 2026

A growing firm has 400 accounts and still cannot see gross margin by service line.

Entities and departments that must report: one file, dated 14 September 2026. No earlier version attached for comparison
Decisions the accounts must support: A growing firm has 400 accounts and still cannot see gross margin by service line
Current pain: miscoding or useless detail: miscoding: in the file; useless detail: not in the file
External reporting framework they claim to use: the draft sentence is broader than the note
```

### Example outcome

**Chart of accounts proposal**
To: Priya Shah, controller, Northline Studio
Date: 14 September 2026 · Needed by: 30 September 2026

**Decision**
Uses a dimension for service line, defines the accounts that change, and maps old balances forward.

**What the file supports**

| Input | Value | Status |
| --- | --- | --- |
| Entities and departments that must report | one file, dated 14 September 2026. No earlier version attached for comparison | Needs confirmation |
| Decisions the accounts must support | A growing firm has 400 accounts and still cannot see gross margin by service line | Carried into the draft |
| Current pain: miscoding or useless detail | miscoding: in the file; useless detail: not in the file | Carried into the draft |
| External reporting framework they claim to use | the draft sentence is broader than the note | Needs confirmation |

**How this draft was built**

**1. Start from decisions**  
Which margins, locations, or funding sources must be visible without a side spreadsheet.

**2. Separate posting accounts from reporting groups**  
People post to stable accounts. Reports roll them up. Do not make every report slice a new account.

**3. Write definitions**  
Each new or changed account gets a one-line definition and an example of what does not belong in it.

**4. Cap the depth**  
Recommend a department or class dimension instead of exploding the natural account list, when their system supports it. If you do not know the system, ask before redesigning.

**5. Plan the map**  
Old account to new account. Unmapped balances are how conversions fail.

**Deliberately not done**
- A hundred new accounts with no definitions.
- Redesigning the chart to match a blog diagram.
- No mapping from the old balances.

**Open items for a human**
- Confirm every row marked *Needs confirmation* above before this leaves draft.
- Anything absent from the file stayed absent. No figure, date, or name was supplied from outside it.

Next: Priya Shah by 30 September 2026. This is a draft, not a sign-off.

## Anti-patterns

- A hundred new accounts with no definitions.
- Redesigning the chart to match a blog diagram.
- No mapping from the old balances.

## Related skills

- `management-accounting-pack`
- `journal-entry-review`
- `month-end-close`
