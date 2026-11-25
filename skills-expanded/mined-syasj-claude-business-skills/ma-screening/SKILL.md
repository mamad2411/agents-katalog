---
name: ma-screening
description: "Screen an acquisition or partnership idea before anyone spends serious diligence money. Use when the user mentions acquisition screen, should we buy, M&A idea, partnership versus build, or asks for a M&A screening memo. Strategy and leadership skill by Yasir Jilani."
license: MIT
compatibility: Agent Skills standard. No network access, extra packages, or credentials required.
metadata:
  author: Yasir Jilani
  version: "1.0.0"
  domain: strategy
---

<!-- GENERATED FILE - edits here are overwritten by scripts/generate.py.
     Edit the 'ma-screening' entry in source/, then run:
       python3 scripts/generate.py && python3 scripts/validate.py
     See CONTRIBUTING.md. -->

# M&A Screening

Screen an acquisition or partnership idea before anyone spends serious diligence money.

## When to use this skill

Use this skill when the user:

- acquisition screen
- should we buy
- M&A idea
- partnership versus build
- diligence kickoff

## When not to use this skill

- A request to hide the deal from required approvers
- Valuation advice presented as a fairness opinion

## Professional boundary

Strategy work recommends a direction. It does not guarantee market outcomes.

## Operating boundaries

- Use only information the user provides or files they explicitly ask you to read. Do not invent metrics, laws, citations, prices, credentials, or clinical facts.
- Do not ask for passwords, API keys, tokens, seed phrases, one-time codes, or payment card data.
- Do not send data to an external service, install packages, or add network calls as part of this skill.
- Separate facts, assumptions, and recommendations. If a required input is missing, state the assumption or ask one focused question.
- If the user asks you to deceive a person, evade a control, forge a record, or cause harm, stop. Offer a legitimate alternative.
- Work product that affects money, employment, health, safety, or legal rights is a draft for a qualified human to review before it is used.

## Inputs to collect

- The target or partner, as the user described it
- The strategic gap this would fill
- Known price range or the fact that price is unknown
- Constraints: cash, talent, regulation

## Workflow


### 1. State the gap

What customer, capability, or time problem is this meant to solve. If the gap is unclear, stop and say the screen cannot proceed.
### 2. Compare alternatives

Buy, partner, or build. Recommend the path that fits the gap, not the most exciting one.
### 3. List what must be true

Five things that must be true for the deal to be rational, and how a later diligence workstream would test each one.
### 4. Flag walk-away issues

Customer concentration, key-person risk, unclear IP, or a price that only works with a fantasy synergy. Use only issues the user raised or that follow directly from their facts.
### 5. Do not invent valuation

If you illustrate a range, label every multiple as the user's assumption. Never present a number as a fair price.
### 6. Define the next step

A cheap question to answer before hiring advisors, not a full diligence plan disguised as a screen.

## Output

Deliver a **M&A screening memo**.

- Purpose of this M&A screening memo, in two sentences.
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

Mara Chen, founder at Northline Studio in Calgary, needs a M&A screening memo by 30 September 2026. A CEO received a teaser for a small competitor and wants to know if it is even worth a conversation.

### Example data

```text
From: Mara Chen, founder
Organization: Northline Studio, Calgary
Date: 14 September 2026
Needed by: 30 September 2026

A CEO received a teaser for a small competitor and wants to know if it is even worth a conversation.

The target or partner, as the user described it: 130
The strategic gap this would fill: Harbor & Co is missing a source
Known price range or the fact that price is unknown: CAD 180
Constraints: cash, talent, regulation: cash: in the file; talent: not in the file; regulation: open
```

### Example outcome

**M&a screening memo**
To: Mara Chen, founder, Northline Studio
Date: 14 September 2026 · Needed by: 30 September 2026

**Decision**
A screening memo with the strategic gap, buy-versus-build, five must-be-true tests, and a single next question before advisors are hired.

**What the file supports**

| Input | Value | Status |
| --- | --- | --- |
| The target or partner, as the user described it | 130 | Needs confirmation |
| The strategic gap this would fill | Harbor & Co is missing a source | Carried into the draft |
| Known price range or the fact that price is unknown | CAD 180 | Carried into the draft |
| Constraints: cash, talent, regulation | cash: in the file; talent: not in the file; regulation: open | Needs confirmation |

**How this draft was built**

**1. State the gap**  
What customer, capability, or time problem is this meant to solve. If the gap is unclear, stop and say the screen cannot proceed.

**2. Compare alternatives**  
Buy, partner, or build. Recommend the path that fits the gap, not the most exciting one.

**3. List what must be true**  
Five things that must be true for the deal to be rational, and how a later diligence workstream would test each one.

**4. Flag walk-away issues**  
Customer concentration, key-person risk, unclear IP, or a price that only works with a fantasy synergy. Use only issues the user raised or that follow directly from their facts.

**5. Do not invent valuation**  
If you illustrate a range, label every multiple as the user's assumption. Never present a number as a fair price.

**Deliberately not done**
- Building a synergy model from imagined revenue.
- Acting as an investment bank or fairness-opinion writer.
- Ignoring build and partner options because a banker sent a teaser.

**Open items for a human**
- Confirm every row marked *Needs confirmation* above before this leaves draft.
- Anything absent from the file stayed absent. No figure, date, or name was supplied from outside it.

Next: Mara Chen by 30 September 2026. This is a draft, not a sign-off.

## Anti-patterns

- Building a synergy model from imagined revenue.
- Acting as an investment bank or fairness-opinion writer.
- Ignoring build and partner options because a banker sent a teaser.

## Related skills

- `investment-memo`
- `competitive-strategy`
- `decision-log`
