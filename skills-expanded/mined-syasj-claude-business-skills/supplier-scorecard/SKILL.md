---
name: supplier-scorecard
description: "Score a supplier on the outcomes in the agreement, using evidence rather than the last meeting's mood. Use when the user mentions supplier scorecard, vendor scorecard, supplier performance, supplier review, or asks for a supplier scorecard. Supply chain skill by Yasir Jilani."
license: MIT
compatibility: Agent Skills standard. No network access, extra packages, or credentials required.
metadata:
  author: Yasir Jilani
  version: "1.0.0"
  domain: supply-chain
---

<!-- GENERATED FILE - edits here are overwritten by scripts/generate.py.
     Edit the 'supplier-scorecard' entry in source/, then run:
       python3 scripts/generate.py && python3 scripts/validate.py
     See CONTRIBUTING.md. -->

# Supplier Scorecard

Score a supplier on the outcomes in the agreement, using evidence rather than the last meeting's mood.

## When to use this skill

Use this skill when the user:

- supplier scorecard
- vendor scorecard
- supplier performance
- supplier review

## When not to use this skill

- The user wants a different domain's specialist skill.
- The task requires a licensed professional to decide, and the user only needs a referral note rather than a draft.
- The request asks you to deceive, evade a control, or hide material facts.

## Professional boundary

Inventory and supplier recommendations depend on the user's lead times and service targets. Do not invent supplier performance.

## Operating boundaries

- Use only information the user provides or files they explicitly ask you to read. Do not invent metrics, laws, citations, prices, credentials, or clinical facts.
- Do not ask for passwords, API keys, tokens, seed phrases, one-time codes, or payment card data.
- Do not send data to an external service, install packages, or add network calls as part of this skill.
- Separate facts, assumptions, and recommendations. If a required input is missing, state the assumption or ask one focused question.
- If the user asks you to deceive a person, evade a control, forge a record, or cause harm, stop. Offer a legitimate alternative.
- Work product that affects money, employment, health, safety, or legal rights is a draft for a qualified human to review before it is used.

## Inputs to collect

- The contracted outcomes
- Recent evidence
- Volumes
- The internal owner

## Workflow


### 1. Step 1

Score only contracted outcomes they can evidence.
### 2. Step 2

Separate a one-off miss from a trend.
### 3. Step 3

Include the buyer's own late forecasts if those caused the miss.
### 4. Step 4

Recommend a conversation, a corrective plan, or a sourcing question.
### 5. Step 5

Do not invent a penalty.
### 6. Step 6

Share the score with the supplier only if the user wants a supplier-facing version, and keep it factual.

## Output

Deliver a **supplier scorecard**.

- Purpose of this supplier scorecard, in two sentences.
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

Diane Cho, supply lead at Harbor Goods in Airdrie, needs a supplier scorecard by 30 September 2026. A supplier is blamed for shortages after the forecast doubled with no notice.

### Example data

```text
From: Diane Cho, supply lead
Organization: Harbor Goods, Airdrie
Date: 14 September 2026
Needed by: 30 September 2026

A supplier is blamed for shortages after the forecast doubled with no notice.

The contracted outcomes: unsigned draft, 8 pages, no signature date
Recent evidence: one PDF, 2 pages, dated 14 September 2026
Volumes: 25 in the last period. No prior period attached, so no trend
The internal owner: Diane Cho, supply lead
```

### Example outcome

**Supplier scorecard**
Harbor Goods · 14 September 2026 · Due 30 September 2026

**Decision**
Records the forecast change as a buyer cause and limits the supplier miss to evidenced gaps.

| Item | Figure in the file | Call | Why |
| --- | --- | --- | --- |
| Cedar Clinic | plan 120, actual 90 | Use | Both sides of the comparison are in the file |
| Fieldnote | score 62 | Report, do not benchmark | One score is a reading, not a baseline |
| Missing export | Not in the file | Stop | The cell stays blank until the export arrives |

**How these calls were made**

1. Score only contracted outcomes they can evidence
2. Separate a one-off miss from a trend
3. Include the buyer's own late forecasts if those caused the miss
4. Recommend a conversation, a corrective plan, or a sourcing question
5. Do not invent a penalty

**Deliberately not done**
- A mood score.
- Invented penalties.
- Ignoring buyer-caused misses.

**Open items**
- The missing export is the binding constraint. No figure was estimated to fill its place.
- Any row marked *Report, do not benchmark* needs a second period before it can carry a trend.

Next: Diane Cho attaches the missing export, or the cell stays blank. Due 30 September 2026.

## Anti-patterns

- A mood score
- Invented penalties
- Ignoring buyer-caused misses

## Related skills

- `vendor-ops-review`
- `shortage-playbook`
