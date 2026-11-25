---
name: owner-draw-note
description: "Separate an owner draw from wages and from money the business still owes. Use when the user mentions owner draw, owner pay, can I take money out, draw versus wage, or asks for a draw note. Small business skill by Yasir Jilani."
license: MIT
compatibility: Agent Skills standard. No network access, extra packages, or credentials required.
metadata:
  author: Yasir Jilani
  version: "1.0.0"
  domain: small-business
---

<!-- GENERATED FILE - edits here are overwritten by scripts/generate.py.
     Edit the 'owner-draw-note' entry in source/, then run:
       python3 scripts/generate.py && python3 scripts/validate.py
     See CONTRIBUTING.md. -->

# Owner Draw Note

Separate an owner draw from wages and from money the business still owes.

## When to use this skill

Use this skill when the user:

- owner draw
- owner pay
- can I take money out
- draw versus wage

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

- Cash after bills
- Draws already taken
- Bills still due
- What their bookkeeper calls a draw

## Workflow


### 1. Step 1

Start from cash after the bills they listed.
### 2. Step 2

List draws already taken.
### 3. Step 3

Do not label a draw as a wage.
### 4. Step 4

Do not skip a tax bill to fund a draw.
### 5. Step 5

If they have no bookkeeper rule, say the label is unset.
### 6. Step 6

Recommend an amount only from the cash that is left.

## Output

Deliver a **draw note**.

- Purpose of this draw note, in two sentences.
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

Diane wants $2,000 for herself on Thursday. Rent of $3,000 is unpaid. The bookkeeper labels these transfers as draws, not wages. The till count is $4,200.

### Example data

```text
wanted: 2000 draw, Thu 18 Sep 2026
rent unpaid: 3000
till: 4200
label in the books: draw, not wage
tax bill Friday: 800
```

### Example outcome

**Draw note**
Hold the $2,000. Rent is unpaid, and Friday's $800 tax bill is still due.
A draw is not a wage. Do not relabel it.
Cash after rent would be $1,200 before tax. That is not a draw week.
Next: revisit after rent and the tax bill are paid, not before.

## Anti-patterns

- A draw that skips a tax bill
- A draw called a wage to look cleaner
- No cash figure

## Related skills

- `owner-cash-huddle`
- `first-employee-note`
