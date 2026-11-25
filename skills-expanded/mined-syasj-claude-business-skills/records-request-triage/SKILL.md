---
name: records-request-triage
description: "Triage a records request for scope, search, and exemptions their officer must decide. Use when the user mentions records request, FOI triage, public records request, information request, or asks for a records request triage. Public sector skill by Yasir Jilani."
license: MIT
compatibility: Agent Skills standard. No network access, extra packages, or credentials required.
metadata:
  author: Yasir Jilani
  version: "1.0.0"
  domain: public-sector
---

<!-- GENERATED FILE - edits here are overwritten by scripts/generate.py.
     Edit the 'records-request-triage' entry in source/, then run:
       python3 scripts/generate.py && python3 scripts/validate.py
     See CONTRIBUTING.md. -->

# Records Request Triage

Triage a records request for scope, search, and exemptions their officer must decide.

## When to use this skill

Use this skill when the user:

- records request
- FOI triage
- public records request
- information request

## When not to use this skill

- Destroying records
- Evading a lawful request

## Professional boundary

Public work should be accurate, even-handed, and suitable for the record. Do not draft deceptive communications, voter manipulation, or surveillance programs.

## Operating boundaries

- Use only information the user provides or files they explicitly ask you to read. Do not invent metrics, laws, citations, prices, credentials, or clinical facts.
- Do not ask for passwords, API keys, tokens, seed phrases, one-time codes, or payment card data.
- Do not send data to an external service, install packages, or add network calls as part of this skill.
- Separate facts, assumptions, and recommendations. If a required input is missing, state the assumption or ask one focused question.
- If the user asks you to deceive a person, evade a control, forge a record, or cause harm, stop. Offer a legitimate alternative.
- Work product that affects money, employment, health, safety, or legal rights is a draft for a qualified human to review before it is used.

## Inputs to collect

- The request
- Systems that may hold records
- Their exemption list if any
- The officer

## Workflow


### 1. Step 1

Restate the scope. Ask one clarifying question if it is too broad to search.
### 2. Step 2

List likely locations. Do not search systems the user did not authorize.
### 3. Step 3

Flag exemptions as questions for the officer. Do not withhold records on a homemade theory.
### 4. Step 4

Note personal data that may need redaction by the officer.
### 5. Step 5

Do not destroy records because a request arrived.
### 6. Step 6

Give a realistic search plan, not a promise of a legal deadline you invented.

## Output

Deliver a **records request triage**.

- Purpose of this records request triage, in two sentences.
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

Pat Nguyen, clerk at Town of Airdrie in Airdrie, needs a records request triage by 30 September 2026. A manager wants to delete drafts because a request might cover them.

### Example data

```text
From: Pat Nguyen, clerk
Organization: Town of Airdrie, Airdrie
Date: 14 September 2026
Needed by: 30 September 2026

A manager wants to delete drafts because a request might cover them.

The request: Council agenda item 6, recorded 14 September 2026. No supporting file attached
Systems that may hold records: one file, dated 14 September 2026. No earlier version attached for comparison
Their exemption list if any: Council agenda item 6; Posted comment period; Records request 92
The officer: Council agenda item 6, recorded 14 September 2026. No supporting file attached
```

### Example outcome

**Records request triage**
To: Pat Nguyen, clerk, Town of Airdrie
Date: 14 September 2026 · Needed by: 30 September 2026

**Decision**
Forbids deletion and lists locations for the officer to decide.

**What the file supports**

| Input | Value | Status |
| --- | --- | --- |
| The request | Council agenda item 6, recorded 14 September 2026. No supporting file attached | Needs confirmation |
| Systems that may hold records | one file, dated 14 September 2026. No earlier version attached for comparison | Carried into the draft |
| Their exemption list if any | Council agenda item 6; Posted comment period; Records request 92 | Carried into the draft |
| The officer | Council agenda item 6, recorded 14 September 2026. No supporting file attached | Needs confirmation |

**How this draft was built**

**1. Restate the scope. Ask one clarifying question if it is too broad to search**

**2. List likely locations. Do not search systems the user did not authorize**

**3. Flag exemptions as questions for the officer. Do not withhold records on a homemade theory**

**4. Note personal data that may need redaction by the officer**

**5. Do not destroy records because a request arrived**

**Deliberately not done**
- Destroying records after a request.
- A homemade exemption ruling.
- An invented legal deadline.

**Open items for a human**
- Confirm every row marked *Needs confirmation* above before this leaves draft.
- Anything absent from the file stayed absent. No figure, date, or name was supplied from outside it.

Next: Pat Nguyen by 30 September 2026. This is a draft, not a sign-off.

## Anti-patterns

- Destroying records after a request
- A homemade exemption ruling
- An invented legal deadline

## Related skills

- `records-retention`
- `legal-hold-notice`
