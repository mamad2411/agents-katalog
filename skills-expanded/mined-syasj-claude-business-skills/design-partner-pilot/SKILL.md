---
name: design-partner-pilot
description: "Scope a pilot with the partner, the success test, and the end date. Use when the user mentions design partner, pilot scope, paid pilot, first pilot, or asks for a pilot note. Entrepreneurship skill by Yasir Jilani."
license: MIT
compatibility: Agent Skills standard. No network access, extra packages, or credentials required.
metadata:
  author: Yasir Jilani
  version: "1.0.0"
  domain: entrepreneurship
---

<!-- GENERATED FILE - edits here are overwritten by scripts/generate.py.
     Edit the 'design-partner-pilot' entry in source/, then run:
       python3 scripts/generate.py && python3 scripts/validate.py
     See CONTRIBUTING.md. -->

# Design Partner Pilot

Scope a pilot with the partner, the success test, and the end date.

## When to use this skill

Use this skill when the user:

- design partner
- pilot scope
- paid pilot
- first pilot

## When not to use this skill

- The user wants a different domain's specialist skill.
- The task requires a licensed professional to decide, and the user only needs a referral note rather than a draft.
- The request asks you to deceive, evade a control, or hide material facts.

## Professional boundary

Startup advice is a set of choices, not a promise of funding or growth. Do not invent traction, customers, or investor interest.

## Operating boundaries

- Use only information the user provides or files they explicitly ask you to read. Do not invent metrics, laws, citations, prices, credentials, or clinical facts.
- Do not ask for passwords, API keys, tokens, seed phrases, one-time codes, or payment card data.
- Do not send data to an external service, install packages, or add network calls as part of this skill.
- Separate facts, assumptions, and recommendations. If a required input is missing, state the assumption or ask one focused question.
- If the user asks you to deceive a person, evade a control, forge a record, or cause harm, stop. Offer a legitimate alternative.
- Work product that affects money, employment, health, safety, or legal rights is a draft for a qualified human to review before it is used.

## Inputs to collect

- The partner
- The success test
- The end date
- What is free

## Workflow


### 1. Step 1

Name the partner.
### 2. Step 2

Write the test in a number they can observe.
### 3. Step 3

Set the end date.
### 4. Step 4

Say what is free and what is paid.
### 5. Step 5

Do not call it a success before the date.
### 6. Step 6

A pilot with no end is a finding.

## Output

Deliver a **pilot note**.

- Purpose of this pilot note, in two sentences.
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

Harbor Goods agreed to try the export for 30 days starting 16 September. A draft calls Northline validated. Nothing is free beyond that export. They already pay $49.

### Example data

```text
partner: Harbor Goods, Diane Cho, agreed 14 Sep 2026
test: she uses the Saturday export on 20 Sep and 27 Sep
end: 16 Oct 2026
paid: $49 a month already
free: the export setup only
```

### Example outcome

**Pilot**
Partner: Harbor Goods. End: 16 October 2026.
Test: she uses the export on 20 September and 27 September. Success is those two uses, not a feeling.
Paid: $49, already. Free: the setup only.
Do not call the company validated. The test has not happened.
If 16 October passes with no use, the pilot failed. It does not extend itself.

## Anti-patterns

- An open-ended free build
- A success declared in week one
- A partner who has not agreed

## Related skills

- `first-ten-customers`
- `mvp-scope`
