---
name: qualification-meddic
description: "Qualify an opportunity with MEDDIC-style evidence so the forecast is not a mood. Use when the user mentions MEDDIC, is this deal real, qualification review, sales qualification, or asks for a qualification brief. Sales skill by Yasir Jilani."
license: MIT
compatibility: Agent Skills standard. No network access, extra packages, or credentials required.
metadata:
  author: Yasir Jilani
  version: "1.0.0"
  domain: sales
---

<!-- GENERATED FILE - edits here are overwritten by scripts/generate.py.
     Edit the 'qualification-meddic' entry in source/, then run:
       python3 scripts/generate.py && python3 scripts/validate.py
     See CONTRIBUTING.md. -->

# MEDDIC Qualification

Qualify an opportunity with MEDDIC-style evidence so the forecast is not a mood.

## When to use this skill

Use this skill when the user:

- MEDDIC
- is this deal real
- qualification review
- sales qualification

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

- The opportunity notes
- The economic buyer if known
- The decision process as told by the buyer
- The close date the seller hopes for

## Workflow


### 1. Metrics

What measurable result does the buyer expect, and who measured the baseline. If nobody measured it, say the metric is unproven.
### 2. Economic buyer

Name the person who can fund the change. A coach is not an economic buyer.
### 3. Decision criteria

Write the criteria the buyer stated, not the criteria you wish they had.
### 4. Decision process

Steps, dates, and paper. A close date with no process is a wish.
### 5. Identify pain and champion

Pain must be theirs. A champion must have power and a reason to act. Do not label a friendly user a champion without evidence.
### 6. Gaps

List the missing letters. Recommend the next question, not a stage upgrade.

## Output

Deliver a **qualification brief**.

- Purpose of this qualification brief, in two sentences.
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

Samir Qureshi, account executive at Fieldnote in Edmonton, needs a qualification brief by 30 September 2026. A deal is forecast for this month, and the only contact is a manager who likes the product but cannot sign.

### Example data

```text
From: Samir Qureshi, account executive
Organization: Fieldnote, Edmonton
Date: 14 September 2026
Needed by: 30 September 2026

A deal is forecast for this month, and the only contact is a manager who likes the product but cannot sign.

The opportunity notes: one file, dated 14 September 2026. No earlier version attached for comparison
The economic buyer if known: Harbor Goods, recorded 14 September 2026. No supporting file attached
The decision process as told by the buyer: A deal is forecast for this month, and the only contact is a manager who likes the product but cannot sign
The close date the seller hopes for: 30 September 2026
```

### Example outcome

**Qualification brief**
To: Samir Qureshi, account executive, Fieldnote
Date: 14 September 2026 · Needed by: 30 September 2026

**Decision**
Marks economic buyer and process as missing and refuses to call the deal committed.

**What the file supports**

| Input | Value | Status |
| --- | --- | --- |
| The opportunity notes | one file, dated 14 September 2026. No earlier version attached for comparison | Needs confirmation |
| The economic buyer if known | Harbor Goods, recorded 14 September 2026. No supporting file attached | Carried into the draft |
| The decision process as told by the buyer | A deal is forecast for this month, and the only contact is a manager who likes the product but cannot sign | Carried into the draft |
| The close date the seller hopes for | 30 September 2026 | Needs confirmation |

**How this draft was built**

**1. Metrics**  
What measurable result does the buyer expect, and who measured the baseline. If nobody measured it, say the metric is unproven.

**2. Economic buyer**  
Name the person who can fund the change. A coach is not an economic buyer.

**3. Decision criteria**  
Write the criteria the buyer stated, not the criteria you wish they had.

**4. Decision process**  
Steps, dates, and paper. A close date with no process is a wish.

**5. Identify pain and champion**  
Pain must be theirs. A champion must have power and a reason to act. Do not label a friendly user a champion without evidence.

**Deliberately not done**
- Filling every MEDDIC box with hope.
- Moving a stage because the quarter needs it.
- Calling a friendly user a champion.

**Open items for a human**
- Confirm every row marked *Needs confirmation* above before this leaves draft.
- Anything absent from the file stayed absent. No figure, date, or name was supplied from outside it.

Next: Samir Qureshi by 30 September 2026. This is a draft, not a sign-off.

## Anti-patterns

- Filling every MEDDIC box with hope.
- Moving a stage because the quarter needs it.
- Calling a friendly user a champion.

## Related skills

- `pipeline-review`
- `forecast-call`
