---
name: sql-review
description: "Review a query for correctness, grain, and safety, without running it against a database you were not given. Use when the user mentions review this SQL, query review, is this query correct, SQL critique, or asks for a SQL review. Data and analytics skill by Yasir Jilani."
license: MIT
compatibility: Agent Skills standard. No network access, extra packages, or credentials required.
metadata:
  author: Yasir Jilani
  version: "1.0.0"
  domain: data
---

<!-- GENERATED FILE - edits here are overwritten by scripts/generate.py.
     Edit the 'sql-review' entry in source/, then run:
       python3 scripts/generate.py && python3 scripts/validate.py
     See CONTRIBUTING.md. -->

# SQL Review

Review a query for correctness, grain, and safety, without running it against a database you were not given.

## When to use this skill

Use this skill when the user:

- review this SQL
- query review
- is this query correct
- SQL critique

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

- The query
- The intended grain and metric
- The tables they say exist
- Whether the query will mutate data

## Workflow


### 1. Step 1

Restate the intended grain and metric.
### 2. Step 2

Check joins and filters against that intent. A fan-out that double-counts is a finding.
### 3. Step 3

Flag non-deterministic filters, missing time zones, and unbounded scans if visible in the text.
### 4. Step 4

If the query mutates or deletes data, require a WHERE and a stated backup. Do not suggest disabling safeguards.
### 5. Step 5

Do not invent table schemas. Mark assumptions.
### 6. Step 6

Recommend a tie-out query they can run, but do not ask for production credentials.

## Output

Deliver a **SQL review**.

- Purpose of this SQL review, in two sentences.
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

Noah Berger, data lead at Fieldnote in Edmonton, needs a SQL review by 30 September 2026. A revenue query joins invoices to line items and sums invoice totals.

### Example data

```text
From: Noah Berger, data lead
Organization: Fieldnote, Edmonton
Date: 14 September 2026
Needed by: 30 September 2026

A revenue query joins invoices to line items and sums invoice totals.

The query: orders_daily, recorded 14 September 2026. No supporting file attached
The intended grain and metric: plan 160, actual 95
The tables they say exist: orders_daily, recorded 14 September 2026. No supporting file attached
Whether the query will mutate data: orders_daily. Partly documented: the what is written down, the who is not
```

### Example outcome

**Sql review**
To: Noah Berger, data lead, Fieldnote
Date: 14 September 2026 · Needed by: 30 September 2026

**Decision**
Flag the double count, asks for the grain, and does not request database passwords.

**What the file supports**

| Input | Value | Status |
| --- | --- | --- |
| The query | orders_daily, recorded 14 September 2026. No supporting file attached | Needs confirmation |
| The intended grain and metric | plan 160, actual 95 | Carried into the draft |
| The tables they say exist | orders_daily, recorded 14 September 2026. No supporting file attached | Carried into the draft |
| Whether the query will mutate data | orders_daily. Partly documented: the what is written down, the who is not | Needs confirmation |

**How this draft was built**

**1. Restate the intended grain and metric**

**2. Check joins and filters against that intent. A fan-out that double-counts is a finding**

**3. Flag non-deterministic filters, missing time zones, and unbounded scans if visible in the text**

**4. If the query mutates or deletes data, require a WHERE and a stated backup. Do not suggest disabling safeguards**

**5. Do not invent table schemas. Mark assumptions**

**Deliberately not done**
- Approving a double-count join.
- Suggesting a credential share.
- An unbounded delete with no predicate.

**Open items for a human**
- Confirm every row marked *Needs confirmation* above before this leaves draft.
- Anything absent from the file stayed absent. No figure, date, or name was supplied from outside it.

Next: Noah Berger by 30 September 2026. This is a draft, not a sign-off.

## Anti-patterns

- Approving a double-count join
- Suggesting a credential share
- An unbounded delete with no predicate

## Related skills

- `metric-definition`
- `data-quality-check`
