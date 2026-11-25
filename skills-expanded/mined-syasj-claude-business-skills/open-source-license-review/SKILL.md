---
name: open-source-license-review
description: "Triage open-source components the user lists so engineering and counsel can see obligations. Not a compatibility ruling. Use when the user mentions open source license, OSS review, dependency license, copyleft question, or asks for a open-source triage. Legal operations skill by Yasir Jilani."
license: MIT
compatibility: Agent Skills standard. No network access, extra packages, or credentials required.
metadata:
  author: Yasir Jilani
  version: "1.0.0"
  domain: legal
---

<!-- GENERATED FILE - edits here are overwritten by scripts/generate.py.
     Edit the 'open-source-license-review' entry in source/, then run:
       python3 scripts/generate.py && python3 scripts/validate.py
     See CONTRIBUTING.md. -->

# Open-Source License Review

Triage open-source components the user lists so engineering and counsel can see obligations. Not a compatibility ruling.

## When to use this skill

Use this skill when the user:

- open source license
- OSS review
- dependency license
- copyleft question

## When not to use this skill

- The user wants a different domain's specialist skill.
- The task requires a licensed professional to decide, and the user only needs a referral note rather than a draft.
- The request asks you to deceive, evade a control, or hide material facts.

## Professional boundary

This is not legal advice and does not create an attorney-client relationship. Do not invent statutes, case names, or filing deadlines. Drafts are for qualified counsel in the relevant jurisdiction.

## Operating boundaries

- Use only information the user provides or files they explicitly ask you to read. Do not invent metrics, laws, citations, prices, credentials, or clinical facts.
- Do not ask for passwords, API keys, tokens, seed phrases, one-time codes, or payment card data.
- Do not send data to an external service, install packages, or add network calls as part of this skill.
- Separate facts, assumptions, and recommendations. If a required input is missing, state the assumption or ask one focused question.
- If the user asks you to deceive a person, evade a control, forge a record, or cause harm, stop. Offer a legitimate alternative.
- Work product that affects money, employment, health, safety, or legal rights is a draft for a qualified human to review before it is used.

## Inputs to collect

- The components and versions they listed
- How the component is used: linked, modified, or distributed
- The product's distribution model
- Licenses they already identified

## Workflow


### 1. Use their inventory

Do not pretend to scan a codebase unless the user provided the scan output.
### 2. Record the license name they supplied

If the license text is missing, say the triage cannot classify that component.
### 3. Usage matters

A tool that runs in development is a different question from code distributed to customers. Use their description.
### 4. Obligations in plain language

Attribution, source offer, or reciprocal terms only as those duties are commonly described, and mark them for counsel to confirm. Do not give a legal compatibility opinion.
### 5. Flag unknowns

Custom forks and missing versions are stop points.
### 6. No piracy help

This skill does not remove license notices or hide copied code.

## Output

Deliver a **open-source triage**.

- Purpose of this open-source triage, in two sentences.
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

Elena Voss, operations lead at Northline Studio in Calgary, needs an open-source triage by 30 September 2026. A release candidate includes a library the scan labels as a reciprocal license, and the team ships binaries to customers.

### Example data

```text
From: Elena Voss, operations lead
Organization: Northline Studio, Calgary
Date: 14 September 2026
Needed by: 30 September 2026

A release candidate includes a library the scan labels as a reciprocal license, and the team ships binaries to customers.

The components and versions they listed: Harbor renewal; Contractor NDA; Vendor terms
How the component is used: linked, modified, or distributed: linked: in the file; modified: not in the file; distributed: open
The product's distribution model: Harbor renewal, recorded 14 September 2026. No supporting file attached
Licenses they already identified: MIT on two files. One file has no header
```

### Example outcome

**Open-source triage**
To: Elena Voss, operations lead, Northline Studio
Date: 14 September 2026 · Needed by: 30 September 2026

**Decision**
Isolates that component, states the usage, and sends the obligation question to counsel instead of clearing the release.

**What the file supports**

| Input | Value | Status |
| --- | --- | --- |
| The components and versions they listed | Harbor renewal; Contractor NDA; Vendor terms | Needs confirmation |
| How the component is used: linked, modified, or distributed | linked: in the file; modified: not in the file; distributed: open | Carried into the draft |
| The product's distribution model | Harbor renewal, recorded 14 September 2026. No supporting file attached | Carried into the draft |
| Licenses they already identified | MIT on two files. One file has no header | Needs confirmation |

**How this draft was built**

**1. Use their inventory**  
Do not pretend to scan a codebase unless the user provided the scan output.

**2. Record the license name they supplied**  
If the license text is missing, say the triage cannot classify that component.

**3. Usage matters**  
A tool that runs in development is a different question from code distributed to customers. Use their description.

**4. Obligations in plain language**  
Attribution, source offer, or reciprocal terms only as those duties are commonly described, and mark them for counsel to confirm. Do not give a legal compatibility opinion.

**5. Flag unknowns**  
Custom forks and missing versions are stop points.

**Deliberately not done**
- A blanket 'all MIT, you are fine'.
- Helping strip license notices.
- Classifying a component with no license text.

**Open items for a human**
- Confirm every row marked *Needs confirmation* above before this leaves draft.
- Anything absent from the file stayed absent. No figure, date, or name was supplied from outside it.

Next: Elena Voss by 30 September 2026. This is a draft, not a sign-off.

## Anti-patterns

- A blanket 'all MIT, you are fine'.
- Helping strip license notices.
- Classifying a component with no license text.

## Related skills

- `ip-ownership-checklist`
- `dependency-upgrade`
- `sbom-and-supply-chain`
