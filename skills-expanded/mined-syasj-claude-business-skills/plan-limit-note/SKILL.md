---
name: plan-limit-note
description: "Write the limit a plan enforces, and the message the user sees when they hit it. Use when the user mentions usage limit, plan limit, fair use, quota message, or asks for a limit note. SaaS skill by Yasir Jilani."
license: MIT
compatibility: Agent Skills standard. No network access, extra packages, or credentials required.
metadata:
  author: Yasir Jilani
  version: "1.0.0"
  domain: saas
---

<!-- GENERATED FILE - edits here are overwritten by scripts/generate.py.
     Edit the 'plan-limit-note' entry in source/, then run:
       python3 scripts/generate.py && python3 scripts/validate.py
     See CONTRIBUTING.md. -->

# Plan Limit Note

Write the limit a plan enforces, and the message the user sees when they hit it.

## When to use this skill

Use this skill when the user:

- usage limit
- plan limit
- fair use
- quota message

## When not to use this skill

- The user wants a different domain's specialist skill.
- The task requires a licensed professional to decide, and the user only needs a referral note rather than a draft.
- The request asks you to deceive, evade a control, or hide material facts.

## Professional boundary

Do not invent churn, revenue, retention, or a security certification. If the export is missing, say so.

## Operating boundaries

- Use only information the user provides or files they explicitly ask you to read. Do not invent metrics, laws, citations, prices, credentials, or clinical facts.
- Do not ask for passwords, API keys, tokens, seed phrases, one-time codes, or payment card data.
- Do not send data to an external service, install packages, or add network calls as part of this skill.
- Separate facts, assumptions, and recommendations. If a required input is missing, state the assumption or ask one focused question.
- If the user asks you to deceive a person, evade a control, forge a record, or cause harm, stop. Offer a legitimate alternative.
- Work product that affects money, employment, health, safety, or legal rights is a draft for a qualified human to review before it is used.

## Inputs to collect

- The limit in the product
- The plan name
- The message they want
- What happens at the limit

## Workflow


### 1. Step 1

Use the limit in the product.
### 2. Step 2

Write the message a person sees at the limit.
### 3. Step 3

Say whether the action blocks or warns.
### 4. Step 4

Do not promise an overage price they have not set.
### 5. Step 5

Match the pricing page.
### 6. Step 6

Name who changes the limit.

## Output

Deliver a **limit note**.

- Purpose of this limit note, in two sentences.
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

Pro blocks an export at 5,000 rows. The message in the product still says 'You can export everything on Pro'. There is no overage price.

### Example data

```text
plan: Pro
limit: 5000 rows, then the export button stops
current message: You can export everything on Pro
overage price: none set
who changes the limit: Jonah
```

### Example outcome

**Limit**
Pro blocks at 5,000 rows. The button stops. It does not bill an overage. None is set.

Message: This export stops at 5,000 rows on Pro. It does not say unlimited.
Who changes the limit: Jonah. The pricing page has to say the same number.

## Anti-patterns

- A message that says unlimited
- An overage price invented
- A limit that does not match the page

## Related skills

- `pricing-page-note`
- `activation-gap`
