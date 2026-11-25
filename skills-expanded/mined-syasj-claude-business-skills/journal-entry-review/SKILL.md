---
name: journal-entry-review
description: "Review manual journals for purpose, support, and unusual patterns without accusing anyone on a hunch. Use when the user mentions journal entry review, manual journals, unusual entries, JE support, or asks for a journal entry review. Accounting skill by Yasir Jilani."
license: MIT
compatibility: Agent Skills standard. No network access, extra packages, or credentials required.
metadata:
  author: Yasir Jilani
  version: "1.0.0"
  domain: accounting
---

<!-- GENERATED FILE - edits here are overwritten by scripts/generate.py.
     Edit the 'journal-entry-review' entry in source/, then run:
       python3 scripts/generate.py && python3 scripts/validate.py
     See CONTRIBUTING.md. -->

# Journal Entry Review

Review manual journals for purpose, support, and unusual patterns without accusing anyone on a hunch.

## When to use this skill

Use this skill when the user:

- journal entry review
- manual journals
- unusual entries
- JE support

## When not to use this skill

- The user wants a different domain's specialist skill.
- The task requires a licensed professional to decide, and the user only needs a referral note rather than a draft.
- The request asks you to deceive, evade a control, or hide material facts.

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

- Population of manual journals
- Materiality
- Who can post
- Known top-side entries

## Workflow


### 1. Define the population

Manual versus system-generated, for the period. Do not review a sample and call it the population.
### 2. Support test

Each sampled entry needs a purpose and a source. Missing support is the finding, even if the amount looks ordinary.
### 3. Unusual items

Round numbers, late posting, entries to cash or revenue, and entries by people who rarely post. Unusual means 'review', not 'misconduct'.
### 4. Top-side entries

Management adjustments need the estimate memo. A verbal reason is a gap.
### 5. Segregation

Note if the preparer and poster are the same person for material entries, using their described process.
### 6. Write questions, not charges

The output is a review list for the controller. Do not allege fraud.

## Output

Deliver a **journal entry review**.

- Purpose of this journal entry review, in two sentences.
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

Priya Shah, controller at Northline Studio in Calgary, needs a journal entry review by 30 September 2026. Several round-dollar journals hit revenue on the last day of the quarter.

### Example data

```text
From: Priya Shah, controller
Organization: Northline Studio, Calgary
Date: 14 September 2026
Needed by: 30 September 2026

Several round-dollar journals hit revenue on the last day of the quarter.

Population of manual journals: Operating cash. Stated in the ask, not documented anywhere else
Materiality: Undeposited funds, recorded 14 September 2026. No supporting file attached
Who can post: Priya Shah, controller
Known top-side entries: Undeposited funds. Stated in the ask, not documented anywhere else
```

### Example outcome

**Journal entry review**
To: Priya Shah, controller, Northline Studio
Date: 14 September 2026 · Needed by: 30 September 2026

**Decision**
Flag those entries for support and purpose, without alleging misconduct.

**What the file supports**

| Input | Value | Status |
| --- | --- | --- |
| Population of manual journals | Operating cash. Stated in the ask, not documented anywhere else | Needs confirmation |
| Materiality | Undeposited funds, recorded 14 September 2026. No supporting file attached | Carried into the draft |
| Who can post | Priya Shah, controller | Carried into the draft |
| Known top-side entries | Undeposited funds. Stated in the ask, not documented anywhere else | Needs confirmation |

**How this draft was built**

**1. Define the population**  
Manual versus system-generated, for the period. Do not review a sample and call it the population.

**2. Support test**  
Each sampled entry needs a purpose and a source. Missing support is the finding, even if the amount looks ordinary.

**3. Unusual items**  
Round numbers, late posting, entries to cash or revenue, and entries by people who rarely post. Unusual means 'review', not 'misconduct'.

**4. Top-side entries**  
Management adjustments need the estimate memo. A verbal reason is a gap.

**5. Segregation**  
Note if the preparer and poster are the same person for material entries, using their described process.

**Deliberately not done**
- Calling an unusual entry fraud.
- A sample described as a full review.
- No interest in support as long as the amount is small but over their threshold.

**Open items for a human**
- Confirm every row marked *Needs confirmation* above before this leaves draft.
- Anything absent from the file stayed absent. No figure, date, or name was supplied from outside it.

Next: Priya Shah by 30 September 2026. This is a draft, not a sign-off.

## Anti-patterns

- Calling an unusual entry fraud.
- A sample described as a full review.
- No interest in support as long as the amount is small but over their threshold.

## Related skills

- `internal-controls-walkthrough`
- `revenue-recognition-review`
- `month-end-close`
