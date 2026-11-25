---
name: busy-season-plan
description: "Plan the busy weeks from last year's pattern and this year's staff. Use when the user mentions busy season, holiday rush, season plan, peak weeks, or asks for a season plan. Small business skill by Yasir Jilani."
license: MIT
compatibility: Agent Skills standard. No network access, extra packages, or credentials required.
metadata:
  author: Yasir Jilani
  version: "1.0.0"
  domain: small-business
---

<!-- GENERATED FILE - edits here are overwritten by scripts/generate.py.
     Edit the 'busy-season-plan' entry in source/, then run:
       python3 scripts/generate.py && python3 scripts/validate.py
     See CONTRIBUTING.md. -->

# Busy Season Plan

Plan the busy weeks from last year's pattern and this year's staff.

## When to use this skill

Use this skill when the user:

- busy season
- holiday rush
- season plan
- peak weeks

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

- The weeks
- Last year's volume if they have it
- Staff they can roster
- Stock they have

## Workflow


### 1. Step 1

Use their last-year figures if they have them.
### 2. Step 2

Match staff to those weeks.
### 3. Step 3

A stock gap is a finding.
### 4. Step 4

Do not promise a volume they did not have.
### 5. Step 5

Name the week they will not discount.
### 6. Step 6

Cut a plan that needs people who are not hired.

## Output

Deliver a **season plan**.

- Purpose of this season plan, in two sentences.
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

Last December Saturdays did about 40 cars when four techs were on. This December she has two techs. She has not hired the Saturday helper. Stock of filters is 18.

### Example data

```text
last year: about 40 cars each December Saturday, 4 techs, her memory not a printout
this year staff: 2 techs
Saturday helper: not hired
filters on hand: 18
weeks: 6, 13, 20 Dec 2026
```

### Example outcome

**Season plan**
Do not plan for 40. That was four techs, and it is her memory, not a printout.
Size the three Saturdays to two techs. She has not named that number. Leave the car count blank until she writes what two techs finished on a recent Saturday.
Filters: 18 on hand. That is a gap if those Saturdays are busy. It is not a purchase order yet.
The unhired helper is not on the roster.

## Anti-patterns

- A peak plan with no staff
- Invented last-year sales
- A discount that wipes the busy week

## Related skills

- `local-service-offer`
- `workforce-plan`
