---
name: investment-memo
description: "Write an internal memo for spending scarce cash on a bet, with the downside written in the same size font as the upside. Use when the user mentions investment memo, should we fund this bet, internal investment paper, resource bet memo, or asks for a internal investment memo. Finance skill by Yasir Jilani."
license: MIT
compatibility: Agent Skills standard. No network access, extra packages, or credentials required.
metadata:
  author: Yasir Jilani
  version: "1.0.0"
  domain: finance
---

<!-- GENERATED FILE - edits here are overwritten by scripts/generate.py.
     Edit the 'investment-memo' entry in source/, then run:
       python3 scripts/generate.py && python3 scripts/validate.py
     See CONTRIBUTING.md. -->

# Internal Investment Memo

Write an internal memo for spending scarce cash on a bet, with the downside written in the same size font as the upside.

## When to use this skill

Use this skill when the user:

- investment memo
- should we fund this bet
- internal investment paper
- resource bet memo

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

- The bet
- Cash and people required
- Evidence already in hand
- What failure looks like

## Workflow


### 1. State the bet

Customer, offer, and the result that would make this a success, in the user's terms.
### 2. Show evidence and gaps

What has been seen, and what is still a hope. Do not promote hope to evidence.
### 3. Cost the full load

People, cash, and the work that will be delayed. Opportunity cost is part of the price.
### 4. Write the downside

The likely way it fails and the cash already spent by then. Include a stop rule.
### 5. Recommend fund, stage, or decline

Staging is the default when evidence is thin.
### 6. Keep valuation language out unless the user is pricing an external instrument

This is an internal allocation memo, not a stock tip.

## Output

Deliver a **internal investment memo**.

- Purpose of this internal investment memo, in two sentences.
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

Mara Chen, founder at Northline Studio in Calgary, needs an internal investment memo by 30 September 2026. A product leader wants headcount for a new segment and has three design-partner conversations, none paid.

### Example data

```text
From: Mara Chen, founder
Organization: Northline Studio, Calgary
Date: 14 September 2026
Needed by: 30 September 2026

A product leader wants headcount for a new segment and has three design-partner conversations, none paid.

The bet: Operating cash, recorded 14 September 2026. No supporting file attached
Cash and people required: Payroll 15 September. Partly documented: the what is written down, the who is not
Evidence already in hand: one PDF, 2 pages, dated 14 September 2026
What failure looks like: Operating cash, first seen 14 September 2026. No root cause recorded yet
```

### Example outcome

**Internal investment memo**
To: Mara Chen, founder, Northline Studio
Date: 14 September 2026 · Needed by: 30 September 2026

**Decision**
Calls the conversations evidence of interest, not of demand, and stages spend behind a paid pilot.

**What the file supports**

| Input | Value | Status |
| --- | --- | --- |
| The bet | Operating cash, recorded 14 September 2026. No supporting file attached | Needs confirmation |
| Cash and people required | Payroll 15 September. Partly documented: the what is written down, the who is not | Carried into the draft |
| Evidence already in hand | one PDF, 2 pages, dated 14 September 2026 | Carried into the draft |
| What failure looks like | Operating cash, first seen 14 September 2026. No root cause recorded yet | Needs confirmation |

**How this draft was built**

**1. State the bet**  
Customer, offer, and the result that would make this a success, in the user's terms.

**2. Show evidence and gaps**  
What has been seen, and what is still a hope. Do not promote hope to evidence.

**3. Cost the full load**  
People, cash, and the work that will be delayed. Opportunity cost is part of the price.

**4. Write the downside**  
The likely way it fails and the cash already spent by then. Include a stop rule.

**5. Recommend fund, stage, or decline**  
Staging is the default when evidence is thin.

**Deliberately not done**
- A pitch that only has an upside case.
- Ignoring the projects the bet will delay.
- Dressing an internal spend as if it were a public-market recommendation.

**Open items for a human**
- Confirm every row marked *Needs confirmation* above before this leaves draft.
- Anything absent from the file stayed absent. No figure, date, or name was supplied from outside it.

Next: Mara Chen by 30 September 2026. This is a draft, not a sign-off.

## Anti-patterns

- A pitch that only has an upside case.
- Ignoring the projects the bet will delay.
- Dressing an internal spend as if it were a public-market recommendation.

## Related skills

- `capex-business-case`
- `ma-screening`
- `experiment-design`
