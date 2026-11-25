---
name: ai-output-check
description: "Check a model draft against the source text the user supplied. Use when the user mentions check the AI draft, hallucination check, did the model add facts, output QA, or asks for a output check. AI in the business skill by Yasir Jilani."
license: MIT
compatibility: Agent Skills standard. No network access, extra packages, or credentials required.
metadata:
  author: Yasir Jilani
  version: "1.0.0"
  domain: ai
---

<!-- GENERATED FILE - edits here are overwritten by scripts/generate.py.
     Edit the 'ai-output-check' entry in source/, then run:
       python3 scripts/generate.py && python3 scripts/validate.py
     See CONTRIBUTING.md. -->

# AI Output Check

Check a model draft against the source text the user supplied.

## When to use this skill

Use this skill when the user:

- check the AI draft
- hallucination check
- did the model add facts
- output QA

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

- The source text
- The draft
- The claims that matter
- Who will send it

## Workflow


### 1. Step 1

Line each material claim to a sentence in the source.
### 2. Step 2

Mark claims with no source as added.
### 3. Step 3

Do not 'fix' the draft by adding facts you know from elsewhere.
### 4. Step 4

Say whether it can be sent, sent after cuts, or redone.
### 5. Step 5

Keep the source quote short.
### 6. Step 6

If the source is missing, stop.

## Output

Deliver a **output check**.

- Purpose of this output check, in two sentences.
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

Jonah has ticket 4418 and a model reply. The reply says the order shipped on 12 September and offers a $15 credit. The ticket does not say either.

### Example data

```text
ticket 4418: "charged twice on 12 Sep, order 4418. Please look."
draft: "Your order shipped on 12 September. I have applied a $15 credit."
claims that matter: ship date, credit
sender if approved: Rita
```

### Example outcome

**Output check**
Do not send.

| Draft claim | In the ticket? |
| --- | --- |
| Charged twice | Yes, customer said it |
| Order 4418 | Yes |
| Shipped 12 September | No |
| $15 credit | No |

Cut both added lines. A person may say they will look. They may not add a ship date or a credit from this check.
Next: Rita sends her own sentence, or a draft with those two lines gone.

## Anti-patterns

- Filling gaps from general knowledge
- A pass with unmatched claims
- Editing the source to match the draft

## Related skills

- `ai-eval-plan`
- `prompt-revision`
