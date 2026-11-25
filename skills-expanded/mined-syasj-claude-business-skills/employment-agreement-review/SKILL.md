---
name: employment-agreement-review
description: "Prepare a fact-based review list for an employment agreement so counsel and HR can see IP, restrictions, and pay terms. Use when the user mentions employment agreement, offer letter legal review, non-compete review, contractor versus employee agreement, or asks for a employment agreement review list. Legal operations skill by Yasir Jilani."
license: MIT
compatibility: Agent Skills standard. No network access, extra packages, or credentials required.
metadata:
  author: Yasir Jilani
  version: "1.0.0"
  domain: legal
---

<!-- GENERATED FILE - edits here are overwritten by scripts/generate.py.
     Edit the 'employment-agreement-review' entry in source/, then run:
       python3 scripts/generate.py && python3 scripts/validate.py
     See CONTRIBUTING.md. -->

# Employment Agreement Review

Prepare a fact-based review list for an employment agreement so counsel and HR can see IP, restrictions, and pay terms.

## When to use this skill

Use this skill when the user:

- employment agreement
- offer letter legal review
- non-compete review
- contractor versus employee agreement

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

- The agreement text
- The role and location the user stated
- Whether the person is an employee or contractor in their description
- Concerns HR already has

## Workflow


### 1. Restate the relationship

Use the label in the document and the label the user used. If they conflict, flag the conflict. Do not reclassify the worker as a legal conclusion.
### 2. Compensation

Base, variable, and conditions for variable pay, quoted from the text. Note discretion that makes a bonus unclear.
### 3. IP and work product

What is assigned, and whether prior inventions are handled. Flag silence.
### 4. Restrictions

Non-compete, non-solicit, and confidentiality, including duration and geography as written. Do not opine that a restriction is enforceable.
### 5. Exit terms

Notice, garden leave, and equity treatment only if present. Missing equity terms are a question, not an assumption.
### 6. Send to counsel

Local employment law questions are listed, not answered.

## Output

Deliver a **employment agreement review list**.

- Purpose of this employment agreement review list, in two sentences.
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

Elena Voss, operations lead at Northline Studio in Calgary, needs an employment agreement review list by 30 September 2026. An offer letter is silent on IP and includes a two-year non-compete with no geography.

### Example data

```text
From: Elena Voss, operations lead
Organization: Northline Studio, Calgary
Date: 14 September 2026
Needed by: 30 September 2026

An offer letter is silent on IP and includes a two-year non-compete with no geography.

The agreement text: Harbor renewal, recorded 14 September 2026. No supporting file attached
The role and location the user stated: Harbor renewal, recorded 14 September 2026. No supporting file attached
Whether the person is an employee or contractor in their description: unsigned draft, 8 pages, no signature date
Concerns HR already has: Harbor renewal and one other, both unconfirmed as of 14 September 2026
```

### Example outcome

**Employment agreement review list**
To: Elena Voss, operations lead, Northline Studio
Date: 14 September 2026 · Needed by: 30 September 2026

**Decision**
A review list quoting the non-compete, noting the missing IP clause, and handing enforceability to local counsel.

**What the file supports**

| Input | Value | Status |
| --- | --- | --- |
| The agreement text | Harbor renewal, recorded 14 September 2026. No supporting file attached | Needs confirmation |
| The role and location the user stated | Harbor renewal, recorded 14 September 2026. No supporting file attached | Carried into the draft |
| Whether the person is an employee or contractor in their description | unsigned draft, 8 pages, no signature date | Carried into the draft |
| Concerns HR already has | Harbor renewal and one other, both unconfirmed as of 14 September 2026 | Needs confirmation |

**How this draft was built**

**1. Restate the relationship**  
Use the label in the document and the label the user used. If they conflict, flag the conflict. Do not reclassify the worker as a legal conclusion.

**2. Compensation**  
Base, variable, and conditions for variable pay, quoted from the text. Note discretion that makes a bonus unclear.

**3. IP and work product**  
What is assigned, and whether prior inventions are handled. Flag silence.

**4. Restrictions**  
Non-compete, non-solicit, and confidentiality, including duration and geography as written. Do not opine that a restriction is enforceable.

**5. Exit terms**  
Notice, garden leave, and equity treatment only if present. Missing equity terms are a question, not an assumption.

**Deliberately not done**
- Declaring a non-compete void.
- Reclassifying a contractor as an employee as a legal ruling.
- Inventing statutory notice periods.

**Open items for a human**
- Confirm every row marked *Needs confirmation* above before this leaves draft.
- Anything absent from the file stayed absent. No figure, date, or name was supplied from outside it.

Next: Elena Voss by 30 September 2026. This is a draft, not a sign-off.

## Anti-patterns

- Declaring a non-compete void.
- Reclassifying a contractor as an employee as a legal ruling.
- Inventing statutory notice periods.

## Related skills

- `offer-letter-checklist`
- `ip-ownership-checklist`
- `handbook-policy-draft`
