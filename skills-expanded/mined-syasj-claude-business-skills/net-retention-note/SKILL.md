---
name: net-retention-note
description: "Compute net retention only from the starting and ending revenue they provide for the same accounts. Use when the user mentions net retention, NRR, net revenue retention, expansion and churn, or asks for a retention note. SaaS skill by Yasir Jilani."
license: MIT
compatibility: Agent Skills standard. No network access, extra packages, or credentials required.
metadata:
  author: Yasir Jilani
  version: "1.0.0"
  domain: saas
---

<!-- GENERATED FILE - edits here are overwritten by scripts/generate.py.
     Edit the 'net-retention-note' entry in source/, then run:
       python3 scripts/generate.py && python3 scripts/validate.py
     See CONTRIBUTING.md. -->

# Net Retention Note

Compute net retention only from the starting and ending revenue they provide for the same accounts.

## When to use this skill

Use this skill when the user:

- net retention
- NRR
- net revenue retention
- expansion and churn

## When not to use this skill

- The user wants a different domain's specialist skill.
- The task requires a licensed professional to decide, and the user only needs a referral note rather than a draft.
- The request asks you to deceive, evade a control, or hide material facts.

## Professional boundary

Do not invent churn, revenue, retention, or a security certification. If the export is missing, say so.

## Operating boundaries

- Use only information the user provides or files they explicitly ask you to read. Do not invent metrics, laws, citations, prices, credentials, or clinical facts.
- Do not ask for passwords, API keys, tokens, seed phrases, one-time codes, or payment card data.
- Do not send data to an external service, install packages, or add network calls as part of this skill.
- Separate facts, assumptions, and recommendations. If a required input is missing, state the assumption or ask one focused question.
- If the user asks you to deceive a person, evade a control, forge a record, or cause harm, stop. Offer a legitimate alternative.
- Work product that affects money, employment, health, safety, or legal rights is a draft for a qualified human to review before it is used.

## Inputs to collect

- Starting revenue for the cohort
- Ending revenue for the same accounts
- What is excluded
- The period

## Workflow


### 1. Step 1

Use the same accounts at the start and the end.
### 2. Step 2

Do not add new logos to the ending number.
### 3. Step 3

Show expansion and churn only if they split them.
### 4. Step 4

If they did not split them, give one ratio and say it is not split.
### 5. Step 5

Do not annualize.
### 6. Step 6

Do not borrow a benchmark.

## Output

Deliver a **retention note**.

- Purpose of this retention note, in two sentences.
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

A board slide says NRR is 120 percent. The file has total MRR for two months and a list of new logos. It does not identify the same accounts at the start and the end.

### Example data

```text
slide: NRR 120 percent
file: August MRR 40500, September week MRR 42000
new logos: 6, revenue not split
same-account cohort: not in the file
expansion versus churn: not split
```

### Example outcome

**Retention note**
Do not use 120 percent. The file is not a same-account cohort.
New logos do not belong in that ratio, and their revenue is not even split out.
Ending and starting totals are a company MRR change, not NRR.
What would make the number possible: the same accounts, August revenue and current revenue, with new logos excluded.
Until that sheet exists, the cell stays blank.

## Anti-patterns

- New logos in the NRR math
- A benchmark
- A split they did not provide

## Related skills

- `saas-weekly-metrics`
- `expansion-play`
