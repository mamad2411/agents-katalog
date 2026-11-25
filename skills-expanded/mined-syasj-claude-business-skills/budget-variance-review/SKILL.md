---
name: budget-variance-review
description: "Explain what moved versus budget in a way an operator can act on, separating timing from true misses. Use when the user mentions budget variance, why are we off budget, actual versus plan, monthly variance, or asks for a budget variance review. Finance skill by Yasir Jilani."
license: MIT
compatibility: Agent Skills standard. No network access, extra packages, or credentials required.
metadata:
  author: Yasir Jilani
  version: "1.0.0"
  domain: finance
---

<!-- GENERATED FILE - edits here are overwritten by scripts/generate.py.
     Edit the 'budget-variance-review' entry in source/, then run:
       python3 scripts/generate.py && python3 scripts/validate.py
     See CONTRIBUTING.md. -->

# Budget Variance Review

Explain what moved versus budget in a way an operator can act on, separating timing from true misses.

## When to use this skill

Use this skill when the user:

- budget variance
- why are we off budget
- actual versus plan
- monthly variance

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

- Budget and actuals for the period
- The user's explanation of one-off items
- Materiality threshold
- Who needs the review

## Workflow


### 1. Set materiality

Ignore noise under the threshold the user names. If they name none, propose one and label it as a proposal.
### 2. Bridge the gap

Start at budget and walk to actual in a few drivers. Volume, price, timing, and one-offs are the usual buckets. Use only drivers you can support.
### 3. Separate timing

A bill that landed early is not the same as a cost that will repeat. Say which variances reverse.
### 4. Find the forecast impact

Which variances should change the outlook, and which should not.
### 5. Ask for an action

Each material miss gets an owner and a response, or an explicit decision to accept it.
### 6. Write for the reader

A CEO gets the bridge and the decisions. A department lead gets their lines, not the whole company essay.

## Output

Deliver a **budget variance review**.

- Purpose of this budget variance review, in two sentences.
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

Mara Chen, founder at Northline Studio in Calgary, needs a budget variance review by 30 September 2026. Marketing is 18 percent over budget and the CMO says it is timing of an event invoice.

### Example data

```text
From: Mara Chen, founder
Organization: Northline Studio, Calgary
Date: 14 September 2026
Needed by: 30 September 2026

Marketing is 18 percent over budget and the CMO says it is timing of an event invoice.

Budget and actuals for the period: month ending 14 September 2026
The user's explanation of one-off items: Operating cash, recorded 14 September 2026. No supporting file attached
Materiality threshold: their one-page rule dated 2 Mar 2026. No exception log since
Who needs the review: Mara Chen, founder
```

### Example outcome

**Variance note**
Northline Studio · period ending 14 September 2026

Decision: treat the gap as a miss against the file, not as a formatting issue. Do not call it timing unless the invoice date is in the file.

| Line | Plan | Actual | Gap |
| --- | --- | --- | --- |
| Main driver | 130 | 80 | 50 |
| One-off named in the file | — | not supplied | leave open |
| Full-period outlook | unchanged until the one-off is dated | | |

Isolates the invoice timing, states whether the full-year outlook changes, and names any remaining true overspend.
Next action: Mara Chen marks the gap as timing or as a real miss by 30 September 2026.

## Anti-patterns

- A line-by-line dump with no bridge.
- Treating every timing difference as a performance failure.
- Inventing a 'market' explanation without evidence.

## Related skills

- `forecast-accuracy`
- `management-reporting-pack`
- `cash-flow-forecast`
