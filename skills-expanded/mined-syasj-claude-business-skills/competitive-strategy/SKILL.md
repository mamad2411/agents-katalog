---
name: competitive-strategy
description: "Explain how you win against a named alternative, including the status quo, without inventing competitor secrets. Use when the user mentions competitive strategy, how do we win, competitor response, against the status quo, or asks for a competitive strategy note. Strategy and leadership skill by Yasir Jilani."
license: MIT
compatibility: Agent Skills standard. No network access, extra packages, or credentials required.
metadata:
  author: Yasir Jilani
  version: "1.0.0"
  domain: strategy
---

<!-- GENERATED FILE - edits here are overwritten by scripts/generate.py.
     Edit the 'competitive-strategy' entry in source/, then run:
       python3 scripts/generate.py && python3 scripts/validate.py
     See CONTRIBUTING.md. -->

# Competitive Strategy

Explain how you win against a named alternative, including the status quo, without inventing competitor secrets.

## When to use this skill

Use this skill when the user:

- competitive strategy
- how do we win
- competitor response
- against the status quo

## When not to use this skill

- The user wants a different domain's specialist skill.
- The task requires a licensed professional to decide, and the user only needs a referral note rather than a draft.
- The request asks you to deceive, evade a control, or hide material facts.

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

- The customer and the job to be done
- Alternatives the buyer actually considers, including doing nothing
- Proof the user has
- Where you refuse to compete

## Workflow


### 1. Name the real alternative

Include 'do nothing' and internal tools, not only famous vendors. Use competitor facts the user supplied.
### 2. Find the deciding job

State the job the buyer hires a product to do, in their words if you have them.
### 3. Choose where to be different

Recommend one difference that is costly for the alternative to copy. A longer feature list is not a strategy.
### 4. Say where you will lose

Name the buyer for whom you are the wrong choice. That protects the team from bad deals.
### 5. Define proof

What evidence would make a skeptical buyer believe the difference. If the user has no proof, the next step is to get it, not to claim it.
### 6. Avoid dirty tricks

Do not draft deception, fake switching campaigns, or attacks you cannot substantiate.

## Output

Deliver a **competitive strategy note**.

- Purpose of this competitive strategy note, in two sentences.
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

Mara Chen, founder at Northline Studio in Calgary, needs a competitive strategy note by 30 September 2026. A team keeps losing to spreadsheets, not to the named software rival, and wants a strategy note.

### Example data

```text
From: Mara Chen, founder
Organization: Northline Studio, Calgary
Date: 14 September 2026
Needed by: 30 September 2026

A team keeps losing to spreadsheets, not to the named software rival, and wants a strategy note.

The customer and the job to be done: the shopper solving one task in one trip. Not segmented further in the file
Alternatives the buyer actually considers, including doing nothing: two deals cited from memory. Neither has a written loss reason
Proof the user has: one customer email, 14 September 2026, no attachment beyond that
Where you refuse to compete: Lumen Ledger, recorded 14 September 2026. No supporting file attached
```

### Example outcome

**Competitive strategy note**
To: Mara Chen, founder, Northline Studio
Date: 14 September 2026 · Needed by: 30 September 2026

**Decision**
Treats the spreadsheet as the main alternative, names the buyer you will not chase, and lists the proof still missing.

**What the file supports**

| Input | Value | Status |
| --- | --- | --- |
| The customer and the job to be done | the shopper solving one task in one trip. Not segmented further in the file | Needs confirmation |
| Alternatives the buyer actually considers, including doing nothing | two deals cited from memory. Neither has a written loss reason | Carried into the draft |
| Proof the user has | one customer email, 14 September 2026, no attachment beyond that | Carried into the draft |
| Where you refuse to compete | Lumen Ledger, recorded 14 September 2026. No supporting file attached | Needs confirmation |

**How this draft was built**

**1. Name the real alternative**  
Include 'do nothing' and internal tools, not only famous vendors. Use competitor facts the user supplied.

**2. Find the deciding job**  
State the job the buyer hires a product to do, in their words if you have them.

**3. Choose where to be different**  
Recommend one difference that is costly for the alternative to copy. A longer feature list is not a strategy.

**4. Say where you will lose**  
Name the buyer for whom you are the wrong choice. That protects the team from bad deals.

**5. Define proof**  
What evidence would make a skeptical buyer believe the difference. If the user has no proof, the next step is to get it, not to claim it.

**Deliberately not done**
- Inventing a competitor's revenue, roadmap, or weakness.
- Competing on a checklist of features with no tradeoff.
- Trash-talk copy that the user cannot defend.

**Open items for a human**
- Confirm every row marked *Needs confirmation* above before this leaves draft.
- Anything absent from the file stayed absent. No figure, date, or name was supplied from outside it.

Next: Mara Chen by 30 September 2026. This is a draft, not a sign-off.

## Anti-patterns

- Inventing a competitor's revenue, roadmap, or weakness.
- Competing on a checklist of features with no tradeoff.
- Trash-talk copy that the user cannot defend.

## Related skills

- `competitive-battlecard`
- `positioning-statement`
- `market-entry-assessment`
