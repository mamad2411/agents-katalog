---
name: data-quality-check
description: "Check a dataset or pipeline for freshness, completeness, and a tie-out before anyone presents the number. Use when the user mentions data quality, can we trust this number, pipeline check, freshness check, or asks for a data quality check. Data and analytics skill by Yasir Jilani."
license: MIT
compatibility: Agent Skills standard. No network access, extra packages, or credentials required.
metadata:
  author: Yasir Jilani
  version: "1.0.0"
  domain: data
---

<!-- GENERATED FILE - edits here are overwritten by scripts/generate.py.
     Edit the 'data-quality-check' entry in source/, then run:
       python3 scripts/generate.py && python3 scripts/validate.py
     See CONTRIBUTING.md. -->

# Data Quality Check

Check a dataset or pipeline for freshness, completeness, and a tie-out before anyone presents the number.

## When to use this skill

Use this skill when the user:

- data quality
- can we trust this number
- pipeline check
- freshness check

## When not to use this skill

- The user wants a different domain's specialist skill.
- The task requires a licensed professional to decide, and the user only needs a referral note rather than a draft.
- The request asks you to deceive, evade a control, or hide material facts.

## Professional boundary

Do not invent numbers. If a source file is missing, say so. Distinguish observation from inference. Do not re-identify private data to make a point.

## Operating boundaries

- Use only information the user provides or files they explicitly ask you to read. Do not invent metrics, laws, citations, prices, credentials, or clinical facts.
- Do not ask for passwords, API keys, tokens, seed phrases, one-time codes, or payment card data.
- Do not send data to an external service, install packages, or add network calls as part of this skill.
- Separate facts, assumptions, and recommendations. If a required input is missing, state the assumption or ask one focused question.
- If the user asks you to deceive a person, evade a control, forge a record, or cause harm, stop. Offer a legitimate alternative.
- Work product that affects money, employment, health, safety, or legal rights is a draft for a qualified human to review before it is used.

## Inputs to collect

- The dataset and the expected grain
- The freshness they expect
- A tie-out target if they have one
- Known upstream changes

## Workflow


### 1. Step 1

Check grain and freshness first. A stale table cannot support today's decision.
### 2. Step 2

Tie a total to a source they trust. A mismatch is the finding, not a footnote.
### 3. Step 3

Look for duplicates, null keys, and sudden row-count jumps using the evidence they gave.
### 4. Step 4

Separate a pipeline break from a real business movement. Do not guess which without evidence.
### 5. Write the user impact

which dashboard or decision is unsafe.
### 6. Step 6

Recommend a block, a caveat, or a fix, with an owner.

## Output

Deliver a **data quality check**.

- Purpose of this data quality check, in two sentences.
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

Noah Berger, data lead at Fieldnote in Edmonton, needs a data quality check by 30 September 2026. Monday's revenue dashboard is empty and the draft note says the business had zero revenue.

### Example data

```text
From: Noah Berger, data lead
Organization: Fieldnote, Edmonton
Date: 14 September 2026
Needed by: 30 September 2026

Monday's revenue dashboard is empty and the draft note says the business had zero revenue.

The dataset and the expected grain: orders_daily, recorded 14 September 2026. No supporting file attached
The freshness they expect: orders_daily, recorded 14 September 2026. No supporting file attached
A tie-out target if they have one: 150
Known upstream changes: requested 14 September 2026. Not yet approved
```

### Example outcome

**Data quality check**
To: Noah Berger, data lead, Fieldnote
Date: 14 September 2026 · Needed by: 30 September 2026

**Decision**
Treats empty as late or broken until a tie-out says otherwise, and names the decision to pause.

**What the file supports**

| Input | Value | Status |
| --- | --- | --- |
| The dataset and the expected grain | orders_daily, recorded 14 September 2026. No supporting file attached | Needs confirmation |
| The freshness they expect | orders_daily, recorded 14 September 2026. No supporting file attached | Carried into the draft |
| A tie-out target if they have one | 150 | Carried into the draft |
| Known upstream changes | requested 14 September 2026. Not yet approved | Needs confirmation |

**How this draft was built**

**1. Check grain and freshness first. A stale table cannot support today's decision**

**2. Tie a total to a source they trust. A mismatch is the finding, not a footnote**

**3. Look for duplicates, null keys, and sudden row-count jumps using the evidence they gave**

**4. Separate a pipeline break from a real business movement. Do not guess which without evidence**

**5. Write the user impact**  
which dashboard or decision is unsafe.

**Deliberately not done**
- Presenting a number that failed its tie-out.
- Inventing a row count.
- A quality check with no decision impact.

**Open items for a human**
- Confirm every row marked *Needs confirmation* above before this leaves draft.
- Anything absent from the file stayed absent. No figure, date, or name was supplied from outside it.

Next: Noah Berger by 30 September 2026. This is a draft, not a sign-off.

## Anti-patterns

- Presenting a number that failed its tie-out
- Inventing a row count
- A quality check with no decision impact

## Related skills

- `dashboard-spec`
- `anomaly-investigation`
