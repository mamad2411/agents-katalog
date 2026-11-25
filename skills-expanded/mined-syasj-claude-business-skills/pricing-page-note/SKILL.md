---
name: pricing-page-note
description: "Check a pricing page against the plans and the limits they actually enforce. Use when the user mentions pricing page, plan page, public pricing, pricing copy, or asks for a page note. SaaS skill by Yasir Jilani."
license: MIT
compatibility: Agent Skills standard. No network access, extra packages, or credentials required.
metadata:
  author: Yasir Jilani
  version: "1.0.0"
  domain: saas
---

<!-- GENERATED FILE - edits here are overwritten by scripts/generate.py.
     Edit the 'pricing-page-note' entry in source/, then run:
       python3 scripts/generate.py && python3 scripts/validate.py
     See CONTRIBUTING.md. -->

# Pricing Page Note

Check a pricing page against the plans and the limits they actually enforce.

## When to use this skill

Use this skill when the user:

- pricing page
- plan page
- public pricing
- pricing copy

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

- The plans
- The limits in the product
- The page copy
- A claim they cannot support

## Workflow


### 1. Step 1

Match each plan to the limit in the product.
### 2. Step 2

Cut a limit the page states that the product does not enforce.
### 3. Step 3

Do not add a competitor's price.
### 4. Step 4

A discount needs an end date they set.
### 5. Step 5

Say who edits the page.
### 6. Step 6

Do not hide a limit in a footnote they did not write.

## Output

Deliver a **page note**.

- Purpose of this page note, in two sentences.
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

The public page says Pro includes unlimited exports. The product blocks an export at 5,000 rows. Jonah can edit the page. There is no competitor price in the file.

### Example data

```text
plan: Pro
page: unlimited exports
product: blocks at 5000 rows
discount on the page: none
editor: Jonah Park
competitor price: not in the file
```

### Example outcome

**Page note**
Change 'unlimited exports' to 5,000 rows. The product blocks there.
Do not add a competitor's price. None is in the file.
No discount line. None was set.
Editor: Jonah. The page and the product have to match before the next ad runs.

## Anti-patterns

- A limit the product does not enforce
- A fake comparison
- A discount with no end

## Related skills

- `plan-limit-note`
- `marketing-claims-review`
