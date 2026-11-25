---
name: local-supplier-pick
description: "Pick between quotes the owner has, on price, lead time, and the terms on the page. Use when the user mentions pick a supplier, compare quotes, local vendor, which quote, or asks for a supplier pick. Small business skill by Yasir Jilani."
license: MIT
compatibility: Agent Skills standard. No network access, extra packages, or credentials required.
metadata:
  author: Yasir Jilani
  version: "1.0.0"
  domain: small-business
---

<!-- GENERATED FILE - edits here are overwritten by scripts/generate.py.
     Edit the 'local-supplier-pick' entry in source/, then run:
       python3 scripts/generate.py && python3 scripts/validate.py
     See CONTRIBUTING.md. -->

# Local Supplier Pick

Pick between quotes the owner has, on price, lead time, and the terms on the page.

## When to use this skill

Use this skill when the user:

- pick a supplier
- compare quotes
- local vendor
- which quote

## When not to use this skill

- The user wants a different domain's specialist skill.
- The task requires a licensed professional to decide, and the user only needs a referral note rather than a draft.
- The request asks you to deceive, evade a control, or hide material facts.

## Professional boundary

Not legal, tax, or employment advice. Do not invent license rules, tax rates, or a local bylaw.

## Operating boundaries

- Use only information the user provides or files they explicitly ask you to read. Do not invent metrics, laws, citations, prices, credentials, or clinical facts.
- Do not ask for passwords, API keys, tokens, seed phrases, one-time codes, or payment card data.
- Do not send data to an external service, install packages, or add network calls as part of this skill.
- Separate facts, assumptions, and recommendations. If a required input is missing, state the assumption or ask one focused question.
- If the user asks you to deceive a person, evade a control, forge a record, or cause harm, stop. Offer a legitimate alternative.
- Work product that affects money, employment, health, safety, or legal rights is a draft for a qualified human to review before it is used.

## Inputs to collect

- The quotes
- Lead times
- Return terms
- A supplier they will not use

## Workflow


### 1. Step 1

Compare only quotes in the file.
### 2. Step 2

Note lead time and returns, not just price.
### 3. Step 3

A missing term is a gap.
### 4. Step 4

Do not invent a quality score.
### 5. Step 5

Honor a supplier they said they will not use by leaving them out.
### 6. Step 6

Recommend one, with the reason.

## Output

Deliver a **supplier pick**.

- Purpose of this supplier pick, in two sentences.
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

Diane has two quotes for oil. Redline is $4.10 a litre, 14 days, no return term on the page. A local yard is $4.40, 2 days, returns within 30 days. She will not use a third supplier who missed August.

### Example data

```text
quote A: Redline, $4.10/L, 14 days, return term not on the page
quote B: local yard, $4.40/L, 2 days, returns in 30 days
excluded: the August miss supplier
quality scores: none
```

### Example outcome

**Pick**
| Quote | Price | Lead | Returns |
| --- | --- | --- | --- |
| Redline | $4.10 | 14 days | not on the page |
| Local yard | $4.40 | 2 days | 30 days |

Recommend the local yard if she needs oil inside a week. The cheaper quote does not say she can send it back.
The August supplier stays out, as she asked.
No quality score. None was in the file.

## Anti-patterns

- A quality score from memory
- A quote that is not in the file
- Ignoring returns

## Related skills

- `supplier-scorecard`
- `books-handoff`
