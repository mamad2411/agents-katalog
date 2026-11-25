---
name: books-handoff
description: "Hand a bookkeeper the accounts, the open items, and the access that is not a shared password. Use when the user mentions bookkeeper handoff, catch up the books, accountant package, monthly books, or asks for a handoff. Small business skill by Yasir Jilani."
license: MIT
compatibility: Agent Skills standard. No network access, extra packages, or credentials required.
metadata:
  author: Yasir Jilani
  version: "1.0.0"
  domain: small-business
---

<!-- GENERATED FILE - edits here are overwritten by scripts/generate.py.
     Edit the 'books-handoff' entry in source/, then run:
       python3 scripts/generate.py && python3 scripts/validate.py
     See CONTRIBUTING.md. -->

# Books Handoff

Hand a bookkeeper the accounts, the open items, and the access that is not a shared password.

## When to use this skill

Use this skill when the user:

- bookkeeper handoff
- catch up the books
- accountant package
- monthly books

## When not to use this skill

- The user wants a different domain's specialist skill.
- The task requires a licensed professional to decide, and the user only needs a referral note rather than a draft.
- The request asks you to deceive, evade a control, or hide material facts.

## Professional boundary

Not legal, tax, or employment advice. Do not invent license rules, tax rates, or a local bylaw.

## Operating boundaries

- Use only information the user provides or files they explicitly ask you to read. Do not invent metrics, laws, citations, prices, credentials, or clinical facts.
- Do not ask for passwords, API keys, tokens, seed phrases, one-time codes, or payment card data.
- Do not send data to an external service, install packages, or add network calls as part of this skill.
- Separate facts, assumptions, and recommendations. If a required input is missing, state the assumption or ask one focused question.
- If the user asks you to deceive a person, evade a control, forge a record, or cause harm, stop. Offer a legitimate alternative.
- Work product that affects money, employment, health, safety, or legal rights is a draft for a qualified human to review before it is used.

## Inputs to collect

- The period
- Accounts that do not tie
- Documents missing
- How they will share access

## Workflow


### 1. Step 1

Name the period.
### 2. Step 2

List accounts that do not tie, from their words.
### 3. Step 3

List missing documents.
### 4. Step 4

Share access by a user of their own, not a shared password.
### 5. Step 5

Do not ask the bookkeeper to invent a receipt.
### 6. Step 6

State the due date.

## Output

Deliver a **handoff**.

- Purpose of this handoff, in two sentences.
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

August does not tie. The till was $180 short on the 12th and $40 long on the 28th. Two supplier bills are missing. Diane offered her bank password so the bookkeeper could 'just look'.

### Example data

```text
period: August 2026
till: 12 Aug short 180, 28 Aug long 40
missing: supplier invoice 188, supplier invoice 204
access offered: her bank password
due: 25 Sep 2026
```

### Example outcome

**Handoff**
Period: August 2026.
Does not tie: till, 12 August short $180, 28 August long $40.
Missing documents: invoices 188 and 204. Do not invent them.
Access: a separate user the bank can issue. Not her password.
Due: 25 September. The bookkeeper does not close August by guessing the two bills.

## Anti-patterns

- A shared password
- A missing receipt invented
- A period with no open-item list

## Related skills

- `month-end-close`
- `owner-cash-huddle`
