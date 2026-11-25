---
name: tax-calendar
description: "Build an internal calendar of tax and filing dates the user already knows they must meet, with owners. Not tax advice. Use when the user mentions tax calendar, filing calendar, compliance dates, when are filings due, or asks for a internal tax calendar. Accounting skill by Yasir Jilani."
license: MIT
compatibility: Agent Skills standard. No network access, extra packages, or credentials required.
metadata:
  author: Yasir Jilani
  version: "1.0.0"
  domain: accounting
---

<!-- GENERATED FILE - edits here are overwritten by scripts/generate.py.
     Edit the 'tax-calendar' entry in source/, then run:
       python3 scripts/generate.py && python3 scripts/validate.py
     See CONTRIBUTING.md. -->

# Tax Calendar

Build an internal calendar of tax and filing dates the user already knows they must meet, with owners. Not tax advice.

## When to use this skill

Use this skill when the user:

- tax calendar
- filing calendar
- compliance dates
- when are filings due

## When not to use this skill

- Tax advice or invented statutory deadlines

## Professional boundary

This is not an audit opinion, compilation, or tax advice. Do not invent accounting standards. Use the policy, framework, and chart of accounts the organization actually follows.

## Operating boundaries

- Use only information the user provides or files they explicitly ask you to read. Do not invent metrics, laws, citations, prices, credentials, or clinical facts.
- Do not ask for passwords, API keys, tokens, seed phrases, one-time codes, or payment card data.
- Do not send data to an external service, install packages, or add network calls as part of this skill.
- Separate facts, assumptions, and recommendations. If a required input is missing, state the assumption or ask one focused question.
- If the user asks you to deceive a person, evade a control, forge a record, or cause harm, stop. Offer a legitimate alternative.
- Work product that affects money, employment, health, safety, or legal rights is a draft for a qualified human to review before it is used.

## Inputs to collect

- Jurisdictions they operate in, as they list them
- Filings they already know about
- Owners
- Last year's late items

## Workflow


### 1. Use their list

Record filings they know they have. Do not invent a filing obligation or a statutory deadline from memory.
### 2. Ask them to confirm dates

Where a date is uncertain, mark it unconfirmed rather than filling in a confident wrong day.
### 3. Add preparation lead time

The internal due date is earlier than the external date so review can happen.
### 4. Owner and reviewer

One prepares, another reviews. A calendar with no names will slip.
### 5. Evidence

What is saved when a filing is submitted. No credentials in the calendar.
### 6. Hand off advice

Unusual positions, nexus questions, and interpretations go to their tax advisor. Say that explicitly.

## Output

Deliver a **internal tax calendar**.

- Purpose of this internal tax calendar, in two sentences.
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

Priya Shah, controller at Northline Studio in Calgary, needs an internal tax calendar by 30 September 2026. A company added a second state and the controller wants a calendar, but is unsure which filings apply.

### Example data

```text
From: Priya Shah, controller
Organization: Northline Studio, Calgary
Date: 14 September 2026
Needed by: 30 September 2026

A company added a second state and the controller wants a calendar, but is unsure which filings apply.

Jurisdictions they operate in, as they list them: Operating cash; Undeposited funds; Sales tax payable
Filings they already know about: Undeposited funds. Partly documented: the what is written down, the who is not
Owners: Priya Shah, controller
Last year's late items: Sales tax payable, last reviewed 14 September 2026. No owner named since
```

### Example outcome

**Internal tax calendar**
Northline Studio · 14 September 2026 · Due 30 September 2026

**Decision**
A calendar of known filings, unconfirmed items marked as such, internal lead times, and a clear handoff to their tax advisor for the new state.

**Checklist**

- [x] **Jurisdictions they operate in, as they list them** — Operating cash; Undeposited funds; Sales tax payable  
      Evidenced in the file
- [x] **Filings they already know about** — Undeposited funds. Partly documented: the what is written down, the who is not  
      Evidenced in the file
- [x] **Owners** — Priya Shah, controller  
      Evidenced in the file
- [ ] **Last year's late items** — Sales tax payable, last reviewed 14 September 2026. No owner named since  
      Open — nothing in the file closes this

**The gates this list enforces, in order**

1. Use their list
2. Ask them to confirm dates
3. Add preparation lead time
4. Owner and reviewer
5. Evidence

**Deliberately not done**
- Inventing deadlines.
- Giving a tax opinion.
- Storing portal passwords in the calendar.

**Stop rule**
Do not mark this pack complete while a box above is open. An open box is a finding, not a formality — it is the thing this checklist exists to catch.

Next: Priya Shah closes the open items before 30 September 2026.

## Anti-patterns

- Inventing deadlines.
- Giving a tax opinion.
- Storing portal passwords in the calendar.

## Related skills

- `compliance-calendar`
- `payroll-accounting-review`
- `audit-prep-pbc`
