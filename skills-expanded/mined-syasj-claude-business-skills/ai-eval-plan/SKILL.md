---
name: ai-eval-plan
description: "Plan an evaluation from examples the user already has, with a pass rule they can apply. Use when the user mentions AI eval, test the model, evaluation set, how will we know it works, or asks for a eval plan. AI in the business skill by Yasir Jilani."
license: MIT
compatibility: Agent Skills standard. No network access, extra packages, or credentials required.
metadata:
  author: Yasir Jilani
  version: "1.0.0"
  domain: ai
---

<!-- GENERATED FILE - edits here are overwritten by scripts/generate.py.
     Edit the 'ai-eval-plan' entry in source/, then run:
       python3 scripts/generate.py && python3 scripts/validate.py
     See CONTRIBUTING.md. -->

# AI Eval Plan

Plan an evaluation from examples the user already has, with a pass rule they can apply.

## When to use this skill

Use this skill when the user:

- AI eval
- test the model
- evaluation set
- how will we know it works

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

- Ten or more real examples they can share
- What a pass looks like
- Who labels
- What they will not test yet

## Workflow


### 1. Step 1

Use their examples. Do not invent gold answers.
### 2. Step 2

Write the pass rule as something a reviewer can mark.
### 3. Step 3

Separate a smoke test from a full eval.
### 4. Step 4

Name who labels and how disagreements are kept.
### 5. Step 5

State what this plan does not prove.
### 6. Step 6

Do not publish a score from a plan that has not been run.

## Output

Deliver a **eval plan**.

- Purpose of this eval plan, in two sentences.
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

A slide says the support draft model is 95 percent accurate. Jonah has 12 real tickets and no labels. He needs a plan, not the slide.

### Example data

```text
examples on hand: tickets 4401-4412, exported 14 Sep 2026
labels: none
pass rule the lead will accept: no invented refund, no date that is not in the ticket
labeler: Rita, 2 hours on 22 Sep
will not test yet: tone score, legal advice, other languages
```

### Example outcome

**Eval plan**
The 95 percent comes off the slide. Nothing has been labeled.

Pass on each ticket: every dollar amount and date in the draft appears in the ticket. If not, fail.
Who labels: Rita, 22 September, tickets 4401-4412.
This is a 12-ticket smoke test. It does not prove a rate for the whole queue.
Not in this plan: tone, legal questions, languages other than the English in these tickets.
Next: Jonah does not quote a percent until Rita's marks are in a sheet.

## Anti-patterns

- Invented test cases presented as customer data
- A score with no labeled set
- A pass rule that is 'looks good'

## Related skills

- `ai-output-check`
- `prompt-revision`
