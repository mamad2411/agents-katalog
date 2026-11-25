---
name: audit-prep-pbc
description: "Build a provided-by-client list that answers the auditor's request without dumping the entire file room. Use when the user mentions PBC list, audit preparation, auditor request, provided by client, or asks for a PBC list and evidence index. Accounting skill by Yasir Jilani."
license: MIT
compatibility: Agent Skills standard. No network access, extra packages, or credentials required.
metadata:
  author: Yasir Jilani
  version: "1.0.0"
  domain: accounting
---

<!-- GENERATED FILE - edits here are overwritten by scripts/generate.py.
     Edit the 'audit-prep-pbc' entry in source/, then run:
       python3 scripts/generate.py && python3 scripts/validate.py
     See CONTRIBUTING.md. -->

# Audit PBC Preparation

Build a provided-by-client list that answers the auditor's request without dumping the entire file room.

## When to use this skill

Use this skill when the user:

- PBC list
- audit preparation
- auditor request
- provided by client

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

- The auditor's request list, if any
- Systems and owners
- Known difficult areas
- The period under audit

## Workflow


### 1. Restate each request

What evidence answers it, who owns it, and the period it covers. A request you do not understand gets a clarifying question, not a random export.
### 2. Prefer system reports

Name the report and the parameters. A spreadsheet recreation is a last resort and should be labeled.
### 3. Tie-out notes

For key numbers, say which report ties to the trial balance. Auditors will ask anyway.
### 4. Sensitive access

Provide exports, not shared logins. Do not hand over production credentials.
### 5. Track status

Open, provided, and follow-up. A list without status is a wish.
### 6. Flag judgment areas

Revenue, inventory, and estimates need the memo, not only the number. Do not write a fake memo that invents the auditor's conclusion.

## Output

Deliver a **PBC list and evidence index**.

- Purpose of this PBC list and evidence index, in two sentences.
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

Priya Shah, controller at Northline Studio in Calgary, needs a PBC list and evidence index by 30 September 2026. The external auditor asked for revenue samples and the team is about to export every invoice with no index.

### Example data

```text
From: Priya Shah, controller
Organization: Northline Studio, Calgary
Date: 14 September 2026
Needed by: 30 September 2026

The external auditor asked for revenue samples and the team is about to export every invoice with no index.

The auditor's request list, if any: Operating cash; Undeposited funds; Sales tax payable
Systems and owners: Priya Shah, controller
Known difficult areas: Undeposited funds. Stated in the ask, not documented anywhere else
The period under audit: month ending 14 September 2026
```

### Example outcome

**Pbc list and evidence index**
To: Priya Shah, controller, Northline Studio
Date: 14 September 2026 · Needed by: 30 September 2026

**Decision**
An indexed PBC with owners, report parameters, tie-out notes, and no shared passwords.

**What the file supports**

| Input | Value | Status |
| --- | --- | --- |
| The auditor's request list, if any | Operating cash; Undeposited funds; Sales tax payable | Needs confirmation |
| Systems and owners | Priya Shah, controller | Carried into the draft |
| Known difficult areas | Undeposited funds. Stated in the ask, not documented anywhere else | Carried into the draft |
| The period under audit | month ending 14 September 2026 | Needs confirmation |

**How this draft was built**

**1. Restate each request**  
What evidence answers it, who owns it, and the period it covers. A request you do not understand gets a clarifying question, not a random export.

**2. Prefer system reports**  
Name the report and the parameters. A spreadsheet recreation is a last resort and should be labeled.

**3. Tie-out notes**  
For key numbers, say which report ties to the trial balance. Auditors will ask anyway.

**4. Sensitive access**  
Provide exports, not shared logins. Do not hand over production credentials.

**5. Track status**  
Open, provided, and follow-up. A list without status is a wish.

**Deliberately not done**
- Sending a login instead of an export.
- A data dump with no tie-out.
- Inventing an audit conclusion in the cover note.

**Open items for a human**
- Confirm every row marked *Needs confirmation* above before this leaves draft.
- Anything absent from the file stayed absent. No figure, date, or name was supplied from outside it.

Next: Priya Shah by 30 September 2026. This is a draft, not a sign-off.

## Anti-patterns

- Sending a login instead of an export.
- A data dump with no tie-out.
- Inventing an audit conclusion in the cover note.

## Related skills

- `internal-controls-walkthrough`
- `revenue-recognition-review`
- `financial-close-checklist`
