---
name: credit-file-checklist
description: "Checklist a credit file for missing information before a human credit officer decides. Use when the user mentions credit file, loan file checklist, credit memo prep, borrower file, or asks for a credit file checklist. Banking and treasury operations skill by Yasir Jilani."
license: MIT
compatibility: Agent Skills standard. No network access, extra packages, or credentials required.
metadata:
  author: Yasir Jilani
  version: "1.0.0"
  domain: banking
---

<!-- GENERATED FILE - edits here are overwritten by scripts/generate.py.
     Edit the 'credit-file-checklist' entry in source/, then run:
       python3 scripts/generate.py && python3 scripts/validate.py
     See CONTRIBUTING.md. -->

# Credit File Checklist

Checklist a credit file for missing information before a human credit officer decides.

## When to use this skill

Use this skill when the user:

- credit file
- loan file checklist
- credit memo prep
- borrower file

## When not to use this skill

- Falsifying borrower documents
- Unauthorized credit approval

## Professional boundary

This is not a credit decision and not an instruction to move money. Do not request online-banking passwords, one-time codes, or card PINs.

## Operating boundaries

- Use only information the user provides or files they explicitly ask you to read. Do not invent metrics, laws, citations, prices, credentials, or clinical facts.
- Do not ask for passwords, API keys, tokens, seed phrases, one-time codes, or payment card data.
- Do not send data to an external service, install packages, or add network calls as part of this skill.
- Separate facts, assumptions, and recommendations. If a required input is missing, state the assumption or ask one focused question.
- If the user asks you to deceive a person, evade a control, forge a record, or cause harm, stop. Offer a legitimate alternative.
- Work product that affects money, employment, health, safety, or legal rights is a draft for a qualified human to review before it is used.

## Inputs to collect

- Their required list
- Documents present
- The decision owner
- Known gaps

## Workflow


### 1. Step 1

Compare the file to their list.
### 2. Step 2

Mark missing items. Do not fill gaps with estimates presented as facts.
### 3. Step 3

This skill does not approve credit.
### 4. Step 4

Note policy exceptions for the officer.
### 5. Step 5

Minimize personal data in the summary.
### 6. Step 6

Do not help a borrower falsify income or identity documents.

## Output

Deliver a **credit file checklist**.

- Purpose of this credit file checklist, in two sentences.
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

Priya Shah, controller at Northline Studio in Calgary, needs a credit file checklist by 30 September 2026. A file is missing current financials and the draft says the borrower is strong.

### Example data

```text
From: Priya Shah, controller
Organization: Northline Studio, Calgary
Date: 14 September 2026
Needed by: 30 September 2026

A file is missing current financials and the draft says the borrower is strong.

Their required list: Payment run 14 Sep; Account opening file 221; Liquidity ladder
Documents present: one PDF, 2 pages, dated 14 September 2026
The decision owner: Priya Shah, controller
Known gaps: Payment run 14 Sep is missing a source
```

### Example outcome

**Credit file checklist**
Northline Studio · 14 September 2026 · Due 30 September 2026

**Decision**
Leaves the file incomplete and removes the strength claim.

**Checklist**

- [x] **Their required list** — Payment run 14 Sep; Account opening file 221; Liquidity ladder  
      Evidenced in the file
- [x] **Documents present** — one PDF, 2 pages, dated 14 September 2026  
      Evidenced in the file
- [x] **The decision owner** — Priya Shah, controller  
      Evidenced in the file
- [ ] **Known gaps** — Payment run 14 Sep is missing a source  
      Open — nothing in the file closes this

**The gates this list enforces, in order**

1. Compare the file to their list
2. Mark missing items. Do not fill gaps with estimates presented as facts
3. This skill does not approve credit
4. Note policy exceptions for the officer
5. Minimize personal data in the summary

**Deliberately not done**
- A homemade credit approval.
- Falsified income.
- Estimates labeled as statements.

**Stop rule**
Do not mark this pack complete while a box above is open. An open box is a finding, not a formality — it is the thing this checklist exists to catch.

Next: Priya Shah closes the open items before 30 September 2026.

## Anti-patterns

- A homemade credit approval
- Falsified income
- Estimates labeled as statements

## Related skills

- `debt-capacity-screen`
- `outside-counsel-brief`
