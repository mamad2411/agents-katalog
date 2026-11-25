---
name: first-ten-customers
description: "List the first customers they can name, and the ones that are still wishes. Use when the user mentions first customers, who will buy, design partners, early customer list, or asks for a customer list. Entrepreneurship skill by Yasir Jilani."
license: MIT
compatibility: Agent Skills standard. No network access, extra packages, or credentials required.
metadata:
  author: Yasir Jilani
  version: "1.0.0"
  domain: entrepreneurship
---

<!-- GENERATED FILE - edits here are overwritten by scripts/generate.py.
     Edit the 'first-ten-customers' entry in source/, then run:
       python3 scripts/generate.py && python3 scripts/validate.py
     See CONTRIBUTING.md. -->

# First Ten Customers

List the first customers they can name, and the ones that are still wishes.

## When to use this skill

Use this skill when the user:

- first customers
- who will buy
- design partners
- early customer list

## When not to use this skill

- The user wants a different domain's specialist skill.
- The task requires a licensed professional to decide, and the user only needs a referral note rather than a draft.
- The request asks you to deceive, evade a control, or hide material facts.

## Professional boundary

Startup advice is a set of choices, not a promise of funding or growth. Do not invent traction, customers, or investor interest.

## Operating boundaries

- Use only information the user provides or files they explicitly ask you to read. Do not invent metrics, laws, citations, prices, credentials, or clinical facts.
- Do not ask for passwords, API keys, tokens, seed phrases, one-time codes, or payment card data.
- Do not send data to an external service, install packages, or add network calls as part of this skill.
- Separate facts, assumptions, and recommendations. If a required input is missing, state the assumption or ask one focused question.
- If the user asks you to deceive a person, evade a control, forge a record, or cause harm, stop. Offer a legitimate alternative.
- Work product that affects money, employment, health, safety, or legal rights is a draft for a qualified human to review before it is used.

## Inputs to collect

- Names they have talked to
- Who paid
- Who said no
- The offer

## Workflow


### 1. Step 1

Split paid, talking, and no.
### 2. Step 2

A wish with no conversation is not a prospect.
### 3. Step 3

Use their words for why someone paid.
### 4. Step 4

Do not add logos.
### 5. Step 5

Say what the offer was.
### 6. Step 6

Count only rows they named.

## Output

Deliver a **customer list**.

- Purpose of this customer list, in two sentences.
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

A deck says ten customers. Four shops pay. Six names are on a whiteboard. Mara has not spoken to those six. The offer is $49 a month.

### Example data

```text
paid: Harbor Goods, Cedar Clinic front desk, Lantern Inn shop, a fourth shop she named as Birch Books
wish list: 6 names, no conversation logged
offer: $49 a month
why Harbor pays: Saturday list, Mara's note of their words
```

### Example outcome

**Customers**
Paying: four. Harbor Goods, Cedar Clinic front desk, Lantern Inn shop, Birch Books.
Harbor's reason, in her note: the Saturday list. Do not invent reasons for the other three.
The six names are not customers and not a pipeline. No conversation is logged.
The deck's ten is wrong. The count is four.

## Anti-patterns

- Logos they did not earn
- A wish counted as a pipeline
- A reason they invented

## Related skills

- `design-partner-pilot`
- `customer-discovery-sprint`
