---
name: forecast-call
description: "Produce a sales forecast from evidence categories, not from a sum of hope. Use when the user mentions sales forecast, commit forecast, forecast call, what will we close, or asks for a forecast call note. Sales skill by Yasir Jilani."
license: MIT
compatibility: Agent Skills standard. No network access, extra packages, or credentials required.
metadata:
  author: Yasir Jilani
  version: "1.0.0"
  domain: sales
---

<!-- GENERATED FILE - edits here are overwritten by scripts/generate.py.
     Edit the 'forecast-call' entry in source/, then run:
       python3 scripts/generate.py && python3 scripts/validate.py
     See CONTRIBUTING.md. -->

# Forecast Call

Produce a sales forecast from evidence categories, not from a sum of hope.

## When to use this skill

Use this skill when the user:

- sales forecast
- commit forecast
- forecast call
- what will we close

## When not to use this skill

- The user wants a different domain's specialist skill.
- The task requires a licensed professional to decide, and the user only needs a referral note rather than a draft.
- The request asks you to deceive, evade a control, or hide material facts.

## Professional boundary

Sell honestly. Do not invent customer proof, discounts, or competitor facts. Do not write deceptive, phishing, or high-pressure scripts.

## Operating boundaries

- Use only information the user provides or files they explicitly ask you to read. Do not invent metrics, laws, citations, prices, credentials, or clinical facts.
- Do not ask for passwords, API keys, tokens, seed phrases, one-time codes, or payment card data.
- Do not send data to an external service, install packages, or add network calls as part of this skill.
- Separate facts, assumptions, and recommendations. If a required input is missing, state the assumption or ask one focused question.
- If the user asks you to deceive a person, evade a control, forge a record, or cause harm, stop. Offer a legitimate alternative.
- Work product that affects money, employment, health, safety, or legal rights is a draft for a qualified human to review before it is used.

## Inputs to collect

- Opportunities proposed for commit
- Evidence for each
- Historical slippage the user admits
- The number leadership already hopes for

## Workflow


### 1. Define categories

Commit, best case, and pipeline, in the user's definitions. If they have none, propose simple evidence rules and label them as a proposal.
### 2. Test commit

A commit needs a buyer process and a date the buyer influenced. Seller optimism is not commit.
### 3. Slippage

If they historically slip, show a haircut as their own history, not as a punishment. Do not invent a history.
### 4. Range

Give a range and the deals that swing it. A single number hides the risk.
### 5. Hope gap

If leadership's target exceeds the evidence, say so plainly. Do not backfill fake deals.
### 6. Actions

The two inspections that would change the number this week.

## Output

Deliver a **forecast call note**.

- Purpose of this forecast call note, in two sentences.
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

Samir Qureshi, account executive at Fieldnote in Edmonton, needs a forecast call note by 30 September 2026. Leadership wants a number that is 30 percent above the deals with a real buyer process.

### Example data

```text
From: Samir Qureshi, account executive
Organization: Fieldnote, Edmonton
Date: 14 September 2026
Needed by: 30 September 2026

Leadership wants a number that is 30 percent above the deals with a real buyer process.

Opportunities proposed for commit: Harbor Goods, last reviewed 14 September 2026. No owner named since
Evidence for each: one PDF, 2 pages, dated 14 September 2026
Historical slippage the user admits: Harbor Goods. Partly documented: the what is written down, the who is not
The number leadership already hopes for: Harbor Goods, recorded 14 September 2026. No supporting file attached
```

### Example outcome

**Forecast call note**
To: Samir Qureshi, account executive, Fieldnote
Date: 14 September 2026 · Needed by: 30 September 2026

**Decision**
A forecast range, a clear gap to the hoped-for number, and two inspections, with no fake deals added to close the gap.

**What the file supports**

| Input | Value | Status |
| --- | --- | --- |
| Opportunities proposed for commit | Harbor Goods, last reviewed 14 September 2026. No owner named since | Needs confirmation |
| Evidence for each | one PDF, 2 pages, dated 14 September 2026 | Carried into the draft |
| Historical slippage the user admits | Harbor Goods. Partly documented: the what is written down, the who is not | Carried into the draft |
| The number leadership already hopes for | Harbor Goods, recorded 14 September 2026. No supporting file attached | Needs confirmation |

**How this draft was built**

**1. Define categories**  
Commit, best case, and pipeline, in the user's definitions. If they have none, propose simple evidence rules and label them as a proposal.

**2. Test commit**  
A commit needs a buyer process and a date the buyer influenced. Seller optimism is not commit.

**3. Slippage**  
If they historically slip, show a haircut as their own history, not as a punishment. Do not invent a history.

**4. Range**  
Give a range and the deals that swing it. A single number hides the risk.

**5. Hope gap**  
If leadership's target exceeds the evidence, say so plainly. Do not backfill fake deals.

**Deliberately not done**
- Sandbagging or inflating to please a room.
- A single-point forecast with no swing deals.
- Inventing historical win rates.

**Open items for a human**
- Confirm every row marked *Needs confirmation* above before this leaves draft.
- Anything absent from the file stayed absent. No figure, date, or name was supplied from outside it.

Next: Samir Qureshi by 30 September 2026. This is a draft, not a sign-off.

## Anti-patterns

- Sandbagging or inflating to please a room.
- A single-point forecast with no swing deals.
- Inventing historical win rates.

## Related skills

- `pipeline-review`
- `qualification-meddic`
