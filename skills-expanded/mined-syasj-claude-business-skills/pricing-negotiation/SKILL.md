---
name: pricing-negotiation
description: "Prepare a negotiation around price and tradeoffs, with a walk-away and no deceptive concessions. Use when the user mentions pricing negotiation, discount request, procurement pushback, give-get, or asks for a negotiation plan. Sales skill by Yasir Jilani."
license: MIT
compatibility: Agent Skills standard. No network access, extra packages, or credentials required.
metadata:
  author: Yasir Jilani
  version: "1.0.0"
  domain: sales
---

<!-- GENERATED FILE - edits here are overwritten by scripts/generate.py.
     Edit the 'pricing-negotiation' entry in source/, then run:
       python3 scripts/generate.py && python3 scripts/validate.py
     See CONTRIBUTING.md. -->

# Pricing Negotiation

Prepare a negotiation around price and tradeoffs, with a walk-away and no deceptive concessions.

## When to use this skill

Use this skill when the user:

- pricing negotiation
- discount request
- procurement pushback
- give-get

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

- List price and floor the user authorized
- What the buyer asked for
- Tradeables: term, scope, timing, reference
- Walk-away condition

## Workflow


### 1. Separate price from value

Restate the outcome the buyer said they wanted before discussing a discount.
### 2. Give-get

Every concession has a get. A discount for nothing trains the next discount.
### 3. Floor

Do not go below the authorized floor. If the floor is missing, stop and ask. Do not invent one.
### 4. Multi-issue

Trade term, scope, or start date rather than only price, when the user can actually deliver those trades.
### 5. Walk away

Write the sentence the seller can say if the deal is below the floor. No fake competing offers.
### 6. Record

What was offered, by whom, and when it expires. No silent side letters.

## Output

Deliver a **negotiation plan**.

- Purpose of this negotiation plan, in two sentences.
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

Samir Qureshi, account executive at Fieldnote in Edmonton, needs a negotiation plan by 30 September 2026. Procurement asked for 20 percent off, and the seller's floor is 8 percent with a two-year term available as a trade.

### Example data

```text
From: Samir Qureshi, account executive
Organization: Fieldnote, Edmonton
Date: 14 September 2026
Needed by: 30 September 2026

Procurement asked for 20 percent off, and the seller's floor is 8 percent with a two-year term available as a trade.

List price and floor the user authorized: CAD 180
What the buyer asked for: Procurement asked for 20 percent off, and the seller's floor is 8 percent with a two-year term available as a trade. Stated once, in the ask. Not written down anywhere else
Tradeables: term, scope, timing, reference: term: in the file; scope: not in the file; timing: open; reference: in the file
Walk-away condition: Harbor Goods, last reviewed 14 September 2026. No owner named since
```

### Example outcome

**Negotiation plan**
To: Samir Qureshi, account executive, Fieldnote
Date: 14 September 2026 · Needed by: 30 September 2026

**Decision**
Offers the term trade, holds the floor, and includes a walk-away line with no fake competitor.

**What the file supports**

| Input | Value | Status |
| --- | --- | --- |
| List price and floor the user authorized | CAD 180 | Needs confirmation |
| What the buyer asked for | Procurement asked for 20 percent off, and the seller's floor is 8 percent with a two-year term available as a trade. Stated once, in the ask. Not written down anywhere else | Carried into the draft |
| Tradeables: term, scope, timing, reference | term: in the file; scope: not in the file; timing: open; reference: in the file | Carried into the draft |
| Walk-away condition | Harbor Goods, last reviewed 14 September 2026. No owner named since | Needs confirmation |

**How this draft was built**

**1. Separate price from value**  
Restate the outcome the buyer said they wanted before discussing a discount.

**2. Give-get**  
Every concession has a get. A discount for nothing trains the next discount.

**3. Floor**  
Do not go below the authorized floor. If the floor is missing, stop and ask. Do not invent one.

**4. Multi-issue**  
Trade term, scope, or start date rather than only price, when the user can actually deliver those trades.

**5. Walk away**  
Write the sentence the seller can say if the deal is below the floor. No fake competing offers.

**Deliberately not done**
- Inventing a competing bid.
- Discounting before understanding the ask.
- Unauthorized side deals.

**Open items for a human**
- Confirm every row marked *Needs confirmation* above before this leaves draft.
- Anything absent from the file stayed absent. No figure, date, or name was supplied from outside it.

Next: Samir Qureshi by 30 September 2026. This is a draft, not a sign-off.

## Anti-patterns

- Inventing a competing bid.
- Discounting before understanding the ask.
- Unauthorized side deals.

## Related skills

- `deal-desk-review`
- `proposal-writer`
