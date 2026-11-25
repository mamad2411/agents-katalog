---
name: first-employee-note
description: "List what an owner must decide before a first hire, without inventing employment law. Use when the user mentions first hire, first employee, should I hire, hiring a helper, or asks for a hire note. Small business skill by Yasir Jilani."
license: MIT
compatibility: Agent Skills standard. No network access, extra packages, or credentials required.
metadata:
  author: Yasir Jilani
  version: "1.0.0"
  domain: small-business
---

<!-- GENERATED FILE - edits here are overwritten by scripts/generate.py.
     Edit the 'first-employee-note' entry in source/, then run:
       python3 scripts/generate.py && python3 scripts/validate.py
     See CONTRIBUTING.md. -->

# First Employee Note

List what an owner must decide before a first hire, without inventing employment law.

## When to use this skill

Use this skill when the user:

- first hire
- first employee
- should I hire
- hiring a helper

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

- The hours
- The wage they can pay
- The work
- What they have not checked

## Workflow


### 1. Step 1

State the hours and the wage they named.
### 2. Step 2

List the work.
### 3. Flag checks they have not done

tax account, insurance, a contract review.
### 4. Step 4

Do not invent a legal requirement.
### 5. Step 5

Say what stays the owner's job.
### 6. Step 6

Recommend a pause if the wage is not in the cash file.

## Output

Deliver a **hire note**.

- Purpose of this hire note, in two sentences.
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

Diane wants a Saturday helper from 9 to 5 at $18 an hour. She has not opened a payroll account and has not asked her insurer. The cash file shows Saturday till money, not a wage reserve.

### Example data

```text
hours: Saturday 09:00-17:00
wage she named: $18 an hour
work: front counter, not the oil bay
payroll account: not opened
insurer asked: no
cash reserve for the wage: not in the file
```

### Example outcome

**Hire note**
Not a yes. The wage is not in the cash file, and two checks are open.

Open, and not invented as law: payroll account, insurer. She has not done them. This note does not say which statute applies.
Work: front counter. The oil bay stays hers until she writes that down.
Pause the offer until the $18 is in the weekly cash huddle as a bill, not as a hope.
This note is not a contract and not an employment-law opinion.

## Anti-patterns

- Invented employment law
- A hire the cash file cannot show
- The owner assuming the person knows the rules

## Related skills

- `owner-cash-huddle`
- `job-description-writer`
