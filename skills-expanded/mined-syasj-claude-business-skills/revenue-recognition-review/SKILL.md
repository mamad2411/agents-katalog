---
name: revenue-recognition-review
description: "Prepare questions and a fact pattern for a revenue-recognition issue without pretending to issue an accounting opinion. Use when the user mentions revenue recognition, can we book this revenue, deferred revenue question, contract accounting question, or asks for a revenue recognition fact pattern. Finance skill by Yasir Jilani."
license: MIT
compatibility: Agent Skills standard. No network access, extra packages, or credentials required.
metadata:
  author: Yasir Jilani
  version: "1.0.0"
  domain: finance
---

<!-- GENERATED FILE - edits here are overwritten by scripts/generate.py.
     Edit the 'revenue-recognition-review' entry in source/, then run:
       python3 scripts/generate.py && python3 scripts/validate.py
     See CONTRIBUTING.md. -->

# Revenue Recognition Review

Prepare questions and a fact pattern for a revenue-recognition issue without pretending to issue an accounting opinion.

## When to use this skill

Use this skill when the user:

- revenue recognition
- can we book this revenue
- deferred revenue question
- contract accounting question

## When not to use this skill

- Issuing an audit opinion

## Professional boundary

This is not investment, tax, or financial advice. Do not invent rates of return, tax rates, or valuation multiples. A qualified finance professional must review any decision that moves money.

## Operating boundaries

- Use only information the user provides or files they explicitly ask you to read. Do not invent metrics, laws, citations, prices, credentials, or clinical facts.
- Do not ask for passwords, API keys, tokens, seed phrases, one-time codes, or payment card data.
- Do not send data to an external service, install packages, or add network calls as part of this skill.
- Separate facts, assumptions, and recommendations. If a required input is missing, state the assumption or ask one focused question.
- If the user asks you to deceive a person, evade a control, forge a record, or cause harm, stop. Offer a legitimate alternative.
- Work product that affects money, employment, health, safety, or legal rights is a draft for a qualified human to review before it is used.

## Inputs to collect

- The contract facts the user can share
- What was delivered and what was billed
- The framework the company claims to use
- The decision they need from finance or the auditor

## Workflow


### 1. Write the fact pattern

Parties, promises, price, delivery, and acceptance, in the user's words. Do not upgrade vague facts into certainty.
### 2. Separate billing from revenue

Cash collected and revenue recognized are different questions. Keep them apart.
### 3. Identify the judgment

What is actually in dispute: number of promises, timing, or variable price. One sentence.
### 4. List questions for the policy owner

What the accountant or auditor must answer. Do not answer GAAP or IFRS questions from memory as if they were rulings.
### 5. Flag the management pressure

If the user wants a number in this period, note that the timing desire is not evidence.
### 6. Hand off

Recommend the internal accounting owner. This skill does not close the books.

## Output

Deliver a **revenue recognition fact pattern**.

- Purpose of this revenue recognition fact pattern, in two sentences.
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

Mara Chen, founder at Northline Studio in Calgary, needs a revenue recognition fact pattern by 30 September 2026. Sales wants a multi-year contract fully booked this quarter because the customer signed, but implementation has not started.

### Example data

```text
From: Mara Chen, founder
Organization: Northline Studio, Calgary
Date: 14 September 2026
Needed by: 30 September 2026

Sales wants a multi-year contract fully booked this quarter because the customer signed, but implementation has not started.

The contract facts the user can share: unsigned draft, 8 pages, no signature date
What was delivered and what was billed: Payroll 15 September, last reviewed 14 September 2026. No owner named since
The framework the company claims to use: the draft sentence is broader than the note
The decision they need from finance or the auditor: Sales wants a multi-year contract fully booked this quarter because the customer signed, but implementation has not started
```

### Example outcome

**Revenue recognition fact pattern**
To: Mara Chen, founder, Northline Studio
Date: 14 September 2026 · Needed by: 30 September 2026

**Decision**
Separates signing, billing, and delivery, plus questions for the accounting owner rather than a homemade ruling.

**What the file supports**

| Input | Value | Status |
| --- | --- | --- |
| The contract facts the user can share | unsigned draft, 8 pages, no signature date | Needs confirmation |
| What was delivered and what was billed | Payroll 15 September, last reviewed 14 September 2026. No owner named since | Carried into the draft |
| The framework the company claims to use | the draft sentence is broader than the note | Carried into the draft |
| The decision they need from finance or the auditor | Sales wants a multi-year contract fully booked this quarter because the customer signed, but implementation has not started | Needs confirmation |

**How this draft was built**

**1. Write the fact pattern**  
Parties, promises, price, delivery, and acceptance, in the user's words. Do not upgrade vague facts into certainty.

**2. Separate billing from revenue**  
Cash collected and revenue recognized are different questions. Keep them apart.

**3. Identify the judgment**  
What is actually in dispute: number of promises, timing, or variable price. One sentence.

**4. List questions for the policy owner**  
What the accountant or auditor must answer. Do not answer GAAP or IFRS questions from memory as if they were rulings.

**5. Flag the management pressure**  
If the user wants a number in this period, note that the timing desire is not evidence.

**Deliberately not done**
- Declaring that revenue 'can be recognized' as a final opinion.
- Inventing a standard paragraph number.
- Letting a sales target decide the accounting.

**Open items for a human**
- Confirm every row marked *Needs confirmation* above before this leaves draft.
- Anything absent from the file stayed absent. No figure, date, or name was supplied from outside it.

Next: Mara Chen by 30 September 2026. This is a draft, not a sign-off.

## Anti-patterns

- Declaring that revenue 'can be recognized' as a final opinion.
- Inventing a standard paragraph number.
- Letting a sales target decide the accounting.

## Related skills

- `journal-entry-review`
- `financial-close-checklist`
- `contract-risk-review`
