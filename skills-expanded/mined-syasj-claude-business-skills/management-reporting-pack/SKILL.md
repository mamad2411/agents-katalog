---
name: management-reporting-pack
description: "Design a short monthly pack that tells leaders what changed, what it means, and what decision is due. Use when the user mentions monthly pack, management report, board finance pack, FP&A pack, or asks for a management reporting pack outline. Finance skill by Yasir Jilani."
license: MIT
compatibility: Agent Skills standard. No network access, extra packages, or credentials required.
metadata:
  author: Yasir Jilani
  version: "1.0.0"
  domain: finance
---

<!-- GENERATED FILE - edits here are overwritten by scripts/generate.py.
     Edit the 'management-reporting-pack' entry in source/, then run:
       python3 scripts/generate.py && python3 scripts/validate.py
     See CONTRIBUTING.md. -->

# Management Reporting Pack

Design a short monthly pack that tells leaders what changed, what it means, and what decision is due.

## When to use this skill

Use this skill when the user:

- monthly pack
- management report
- board finance pack
- FP&A pack

## When not to use this skill

- The user wants a different domain's specialist skill.
- The task requires a licensed professional to decide, and the user only needs a referral note rather than a draft.
- The request asks you to deceive, evade a control, or hide material facts.

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

- Who reads it
- Decisions the pack should trigger
- Numbers the team can produce reliably
- What is currently ignored in the old pack

## Workflow


### 1. Choose the reader

A pack for the CEO is not a pack for every cost-center manager. Say which one you are designing.
### 2. Lead with changes

Page one is cash, outlook versus plan, and exceptions. Activity belongs later or nowhere.
### 3. Limit the pages

Recommend a handful of pages. Every chart needs a sentence that says so-what.
### 4. Define sources

Each number has an owner and a close date. A pack that depends on heroic spreadsheets will be late or wrong.
### 5. Add a decision log

Items needing a decision this month, not a gallery of KPIs.
### 6. Retire pages

Name pages from the old pack to drop. Addition without subtraction is how packs become novels.

## Output

Deliver a **management reporting pack outline**.

- Purpose of this management reporting pack outline, in two sentences.
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

Mara Chen, founder at Northline Studio in Calgary, needs a management reporting pack outline by 30 September 2026. The CEO stopped reading the monthly pack because it arrives late and repeats the chart dump.

### Example data

```text
From: Mara Chen, founder
Organization: Northline Studio, Calgary
Date: 14 September 2026
Needed by: 30 September 2026

The CEO stopped reading the monthly pack because it arrives late and repeats the chart dump.

Who reads it: Mara Chen, founder
Decisions the pack should trigger: The CEO stopped reading the monthly pack because it arrives late and repeats the chart dump
Numbers the team can produce reliably: two people on shift, one off
What is currently ignored in the old pack: Payroll 15 September, last reviewed 14 September 2026. No owner named since
```

### Example outcome

**Management reporting pack outline**
To: Mara Chen, founder, Northline Studio
Date: 14 September 2026 · Needed by: 30 September 2026

**Decision**
A short pack outline with page-one exceptions, source owners, and the old pages to retire.

**What the file supports**

| Input | Value | Status |
| --- | --- | --- |
| Who reads it | Mara Chen, founder | Needs confirmation |
| Decisions the pack should trigger | The CEO stopped reading the monthly pack because it arrives late and repeats the chart dump | Carried into the draft |
| Numbers the team can produce reliably | two people on shift, one off | Carried into the draft |
| What is currently ignored in the old pack | Payroll 15 September, last reviewed 14 September 2026. No owner named since | Needs confirmation |

**How this draft was built**

**1. Choose the reader**  
A pack for the CEO is not a pack for every cost-center manager. Say which one you are designing.

**2. Lead with changes**  
Page one is cash, outlook versus plan, and exceptions. Activity belongs later or nowhere.

**3. Limit the pages**  
Recommend a handful of pages. Every chart needs a sentence that says so-what.

**4. Define sources**  
Each number has an owner and a close date. A pack that depends on heroic spreadsheets will be late or wrong.

**5. Add a decision log**  
Items needing a decision this month, not a gallery of KPIs.

**Deliberately not done**
- A 40-page pack with no ask.
- Charts with no source and no sentence.
- Different numbers for the same metric in two sections.

**Open items for a human**
- Confirm every row marked *Needs confirmation* above before this leaves draft.
- Anything absent from the file stayed absent. No figure, date, or name was supplied from outside it.

Next: Mara Chen by 30 September 2026. This is a draft, not a sign-off.

## Anti-patterns

- A 40-page pack with no ask.
- Charts with no source and no sentence.
- Different numbers for the same metric in two sections.

## Related skills

- `budget-variance-review`
- `kpi-tree-finance`
- `executive-one-pager`
