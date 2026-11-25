---
name: site-daily-report
description: "Write a site daily report from observed work, weather, and safety notes, with no invented quantities. Use when the user mentions daily report, site diary, construction daily, superintendent report, or asks for a daily report. Construction skill by Yasir Jilani."
license: MIT
compatibility: Agent Skills standard. No network access, extra packages, or credentials required.
metadata:
  author: Yasir Jilani
  version: "1.0.0"
  domain: construction
---

<!-- GENERATED FILE - edits here are overwritten by scripts/generate.py.
     Edit the 'site-daily-report' entry in source/, then run:
       python3 scripts/generate.py && python3 scripts/validate.py
     See CONTRIBUTING.md. -->

# Site Daily Report

Write a site daily report from observed work, weather, and safety notes, with no invented quantities.

## When to use this skill

Use this skill when the user:

- daily report
- site diary
- construction daily
- superintendent report

## When not to use this skill

- The user wants a different domain's specialist skill.
- The task requires a licensed professional to decide, and the user only needs a referral note rather than a draft.
- The request asks you to deceive, evade a control, or hide material facts.

## Professional boundary

Site safety and contract administration follow the contract and the site rules. Do not tell anyone to skip a safety control. Do not invent quantities.

## Operating boundaries

- Use only information the user provides or files they explicitly ask you to read. Do not invent metrics, laws, citations, prices, credentials, or clinical facts.
- Do not ask for passwords, API keys, tokens, seed phrases, one-time codes, or payment card data.
- Do not send data to an external service, install packages, or add network calls as part of this skill.
- Separate facts, assumptions, and recommendations. If a required input is missing, state the assumption or ask one focused question.
- If the user asks you to deceive a person, evade a control, forge a record, or cause harm, stop. Offer a legitimate alternative.
- Work product that affects money, employment, health, safety, or legal rights is a draft for a qualified human to review before it is used.

## Inputs to collect

- Work performed
- Crew and deliveries they counted
- Safety notes
- Weather they observed

## Workflow


### 1. Step 1

Record only work they observed or documented.
### 2. Step 2

Quantities come from their count. Unknown stays unknown.
### 3. Step 3

Safety incidents and near misses they reported go in plainly.
### 4. Step 4

Delays get a cause they stated.
### 5. Step 5

Note visitors and inspections they named.
### 6. Step 6

Do not backfill a report to hide a delay.

## Output

Deliver a **daily report**.

- Purpose of this daily report, in two sentences.
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

Tom Reilly, site lead at Birch Siteworks in Cochrane, needs a daily report by 30 September 2026. A draft says the slab was poured though the crew was rained out.

### Example data

```text
From: Tom Reilly, site lead
Organization: Birch Siteworks, Cochrane
Date: 14 September 2026
Needed by: 30 September 2026

A draft says the slab was poured though the crew was rained out.

Work performed: Birch site, Cochrane; Takeoff rev C. Both unassigned as of 14 September 2026
Crew and deliveries they counted: 25 in the last period. No prior period attached, so no trend
Safety notes: one file, dated 14 September 2026. No earlier version attached for comparison
Weather they observed: Two-week look-ahead, recorded 14 September 2026. No supporting file attached
```

### Example outcome

**Daily report**
To: Tom Reilly, site lead, Birch Siteworks
Date: 14 September 2026 · Needed by: 30 September 2026

**Decision**
Records the rain delay and leaves the pour unclaimed.

**What the file supports**

| Input | Value | Status |
| --- | --- | --- |
| Work performed | Birch site, Cochrane; Takeoff rev C. Both unassigned as of 14 September 2026 | Needs confirmation |
| Crew and deliveries they counted | 25 in the last period. No prior period attached, so no trend | Carried into the draft |
| Safety notes | one file, dated 14 September 2026. No earlier version attached for comparison | Carried into the draft |
| Weather they observed | Two-week look-ahead, recorded 14 September 2026. No supporting file attached | Needs confirmation |

**How this draft was built**

**1. Record only work they observed or documented**

**2. Quantities come from their count. Unknown stays unknown**

**3. Safety incidents and near misses they reported go in plainly**

**4. Delays get a cause they stated**

**5. Note visitors and inspections they named**

**Deliberately not done**
- Invented quantities.
- A hidden delay.
- A safety note removed to look clean.

**Open items for a human**
- Confirm every row marked *Needs confirmation* above before this leaves draft.
- Anything absent from the file stayed absent. No figure, date, or name was supplied from outside it.

Next: Tom Reilly by 30 September 2026. This is a draft, not a sign-off.

## Anti-patterns

- Invented quantities
- A hidden delay
- A safety note removed to look clean

## Related skills

- `shift-handover`
- `schedule-look-ahead`
