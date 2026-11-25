---
name: contract-risk-review
description: "Review a contract the user provides and list commercial risks for counsel, without declaring it enforceable. Use when the user mentions review this contract, contract risks, redline issues, vendor agreement review, or asks for a contract risk memo. Legal operations skill by Yasir Jilani."
license: MIT
compatibility: Agent Skills standard. No network access, extra packages, or credentials required.
metadata:
  author: Yasir Jilani
  version: "1.0.0"
  domain: legal
---

<!-- GENERATED FILE - edits here are overwritten by scripts/generate.py.
     Edit the 'contract-risk-review' entry in source/, then run:
       python3 scripts/generate.py && python3 scripts/validate.py
     See CONTRIBUTING.md. -->

# Contract Risk Review

Review a contract the user provides and list commercial risks for counsel, without declaring it enforceable.

## When to use this skill

Use this skill when the user:

- review this contract
- contract risks
- redline issues
- vendor agreement review

## When not to use this skill

- A request to hide terms from a counterparty
- A request for a formal legal opinion

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

- The contract text or a faithful summary the user pasted
- Which side the user is on
- The deal they think they are making
- Must-have points they already know

## Workflow


### 1. Confirm the text

Review only language the user supplied. If a clause is missing from what they pasted, say you cannot see it. Do not invent a clause.
### 2. State the deal

In plain language, what each side gives and gets, based on the text.
### 3. Flag asymmetry

Renewal, termination, liability caps, indemnity, assignment, and unilateral change rights. Quote the short phrase you are reacting to.
### 4. Separate legal from commercial

Mark issues a business owner can decide and issues that need qualified counsel in their jurisdiction.
### 5. Do not declare enforceability

You do not say a clause is legal, illegal, or 'standard for the market' from memory.
### 6. Propose questions, not fake redlines

Suggested questions and fallback positions the user can take to counsel. Do not present a redline as legally sufficient.

## Output

Deliver a **contract risk memo**.

- Purpose of this contract risk memo, in two sentences.
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

Elena Voss, operations lead at Northline Studio in Calgary, needs a contract risk memo by 30 September 2026. A founder pasted a vendor SaaS agreement and wants to know what could hurt them before signing.

### Example data

```text
From: Elena Voss, operations lead
Organization: Northline Studio, Calgary
Date: 14 September 2026
Needed by: 30 September 2026

A founder pasted a vendor SaaS agreement and wants to know what could hurt them before signing.

The contract text or a faithful summary the user pasted: unsigned draft, 8 pages, no signature date
Which side the user is on: Vendor terms. Stated in the ask, not documented anywhere else
The deal they think they are making: Harbor renewal, recorded 14 September 2026. No supporting file attached
Must-have points they already know: A founder pasted a vendor SaaS agreement and wants to know what could hurt them before signing. Stated once, in the ask. Not written down anywhere else
```

### Example outcome

**Contract risk memo**
To: Elena Voss, operations lead, Northline Studio
Date: 14 September 2026 · Needed by: 30 September 2026

**Decision**
A memo quoting specific clauses, separating business choices from counsel questions, with no enforceability opinion.

**What the file supports**

| Input | Value | Status |
| --- | --- | --- |
| The contract text or a faithful summary the user pasted | unsigned draft, 8 pages, no signature date | Needs confirmation |
| Which side the user is on | Vendor terms. Stated in the ask, not documented anywhere else | Carried into the draft |
| The deal they think they are making | Harbor renewal, recorded 14 September 2026. No supporting file attached | Carried into the draft |
| Must-have points they already know | A founder pasted a vendor SaaS agreement and wants to know what could hurt them before signing. Stated once, in the ask. Not written down anywhere else | Needs confirmation |

**How this draft was built**

**1. Confirm the text**  
Review only language the user supplied. If a clause is missing from what they pasted, say you cannot see it. Do not invent a clause.

**2. State the deal**  
In plain language, what each side gives and gets, based on the text.

**3. Flag asymmetry**  
Renewal, termination, liability caps, indemnity, assignment, and unilateral change rights. Quote the short phrase you are reacting to.

**4. Separate legal from commercial**  
Mark issues a business owner can decide and issues that need qualified counsel in their jurisdiction.

**5. Do not declare enforceability**  
You do not say a clause is legal, illegal, or 'standard for the market' from memory.

**Deliberately not done**
- A fake 'this contract is fine' conclusion.
- Inventing market standard language.
- Helping conceal a term from the other side's required approver.

**Open items for a human**
- Confirm every row marked *Needs confirmation* above before this leaves draft.
- Anything absent from the file stayed absent. No figure, date, or name was supplied from outside it.

Next: Elena Voss by 30 September 2026. This is a draft, not a sign-off.

## Anti-patterns

- A fake 'this contract is fine' conclusion.
- Inventing market standard language.
- Helping conceal a term from the other side's required approver.

## Related skills

- `nda-triage`
- `vendor-contract-playbook`
- `outside-counsel-brief`
