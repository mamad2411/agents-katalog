---
name: ai-cost-note
description: "Estimate the cost of a proposed AI workflow from the user's prices and volumes. Use when the user mentions AI cost, model bill, token budget, what will this automation cost, or asks for a cost note. AI in the business skill by Yasir Jilani."
license: MIT
compatibility: Agent Skills standard. No network access, extra packages, or credentials required.
metadata:
  author: Yasir Jilani
  version: "1.0.0"
  domain: ai
---

<!-- GENERATED FILE - edits here are overwritten by scripts/generate.py.
     Edit the 'ai-cost-note' entry in source/, then run:
       python3 scripts/generate.py && python3 scripts/validate.py
     See CONTRIBUTING.md. -->

# AI Cost Note

Estimate the cost of a proposed AI workflow from the user's prices and volumes.

## When to use this skill

Use this skill when the user:

- AI cost
- model bill
- token budget
- what will this automation cost

## When not to use this skill

- The user wants a different domain's specialist skill.
- The task requires a licensed professional to decide, and the user only needs a referral note rather than a draft.
- The request asks you to deceive, evade a control, or hide material facts.

## Professional boundary

Do not write prompts or workflows that weaken safety rules, hide required disclosure, or invent model scores. This is not a certification and not a reason to send private data to a vendor.

## Operating boundaries

- Use only information the user provides or files they explicitly ask you to read. Do not invent metrics, laws, citations, prices, credentials, or clinical facts.
- Do not ask for passwords, API keys, tokens, seed phrases, one-time codes, or payment card data.
- Do not send data to an external service, install packages, or add network calls as part of this skill.
- Separate facts, assumptions, and recommendations. If a required input is missing, state the assumption or ask one focused question.
- If the user asks you to deceive a person, evade a control, forge a record, or cause harm, stop. Offer a legitimate alternative.
- Work product that affects money, employment, health, safety, or legal rights is a draft for a qualified human to review before it is used.

## Inputs to collect

- Their price per call or token
- Monthly volume they can show
- Human minutes saved, if measured
- What is not in the price

## Workflow


### 1. Step 1

Use their price sheet. A remembered price is labeled a guess.
### 2. Step 2

Multiply by the volume they showed.
### 3. Step 3

Keep human review time in the cost if they still review.
### 4. Step 4

Do not count saved minutes they have not measured.
### 5. Step 5

Show a low and a high if volume is a range.
### 6. Step 6

Recommend a cap.

## Output

Deliver a **cost note**.

- Purpose of this cost note, in two sentences.
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

A vendor demo says the bot will save $40,000 a month. Jonah has a price of $0.01 per call and last month's ticket count. He has not measured minutes saved.

### Example data

```text
price: $0.01 CAD per call, quote dated 2 Sep 2026, not a signed order
volume: 3,200 tickets in August 2026
calls per ticket if they draft once: 1
human review: still required, minutes not measured
claimed savings: $40,000 a month, no worksheet
cap they can stomach: $100 a month
```

### Example outcome

**Cost note**
August calls at one draft each: 3,200 x $0.01 = $32. Under the $100 cap if they stay at one call and this quote.

The $40,000 savings is not in this note. Minutes saved were not measured.
Not in the price: retries, a second model, or a seat fee. None were on the quote.
High case: if they call the model three times per ticket, $96. Still under the cap, still not a savings claim.
Next: Jonah does not repeat the $40,000 figure.

## Anti-patterns

- A vendor's sample price treated as their contract
- Saved-time dollars with no study
- No cap

## Related skills

- `ai-use-case`
- `saas-weekly-metrics`
