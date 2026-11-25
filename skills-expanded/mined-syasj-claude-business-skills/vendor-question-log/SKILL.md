---
name: vendor-question-log
description: "Log vendor questions and publish answers so every bidder sees the same clarification. Use when the user mentions vendor questions, bidder Q&A, tender clarification, RFP questions, or asks for a question log. Procurement skill by Yasir Jilani."
license: MIT
compatibility: Agent Skills standard. No network access, extra packages, or credentials required.
metadata:
  author: Yasir Jilani
  version: "1.0.0"
  domain: procurement
---

<!-- GENERATED FILE - edits here are overwritten by scripts/generate.py.
     Edit the 'vendor-question-log' entry in source/, then run:
       python3 scripts/generate.py && python3 scripts/validate.py
     See CONTRIBUTING.md. -->

# Vendor Question Log

Log vendor questions and publish answers so every bidder sees the same clarification.

## When to use this skill

Use this skill when the user:

- vendor questions
- bidder Q&A
- tender clarification
- RFP questions

## When not to use this skill

- The user wants a different domain's specialist skill.
- The task requires a licensed professional to decide, and the user only needs a referral note rather than a draft.
- The request asks you to deceive, evade a control, or hide material facts.

## Professional boundary

Buying decisions follow the organization's authority limits. Do not steer an award to a supplier for a personal benefit, and do not invent bids.

## Operating boundaries

- Use only information the user provides or files they explicitly ask you to read. Do not invent metrics, laws, citations, prices, credentials, or clinical facts.
- Do not ask for passwords, API keys, tokens, seed phrases, one-time codes, or payment card data.
- Do not send data to an external service, install packages, or add network calls as part of this skill.
- Separate facts, assumptions, and recommendations. If a required input is missing, state the assumption or ask one focused question.
- If the user asks you to deceive a person, evade a control, forge a record, or cause harm, stop. Offer a legitimate alternative.
- Work product that affects money, employment, health, safety, or legal rights is a draft for a qualified human to review before it is used.

## Inputs to collect

- The questions
- The answers they can give
- What must stay confidential
- The publication owner

## Workflow


### 1. Step 1

Log each question.
### 2. Step 2

Draft an answer that does not reveal another bidder's confidential approach.
### 3. Step 3

Publish answers to all bidders when their process requires it.
### 4. Step 4

Do not give one bidder a private hint.
### 5. Step 5

Mark questions you cannot answer yet.
### 6. Step 6

Correct the solicitation if an answer changes it.

## Output

Deliver a **question log**.

- Purpose of this question log, in two sentences.
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

Diane Cho, buyer at Harbor Goods in Airdrie, needs a question log by 30 September 2026. A buyer wants to email the incumbent a clarification the others will not see.

### Example data

```text
From: Diane Cho, buyer
Organization: Harbor Goods, Airdrie
Date: 14 September 2026
Needed by: 30 September 2026

A buyer wants to email the incumbent a clarification the others will not see.

The questions: A buyer wants to email the incumbent a clarification the others will not see
The answers they can give: Quote set, 3 vendors, recorded 14 September 2026. No supporting file attached
What must stay confidential: email and billing address only. They stated no health or payment data
The publication owner: Diane Cho, buyer
```

### Example outcome

**Question log**
To: Diane Cho, buyer, Harbor Goods
Date: 14 September 2026 · Needed by: 30 September 2026

**Decision**
Publishes the clarification to every bidder.

**What the file supports**

| Input | Value | Status |
| --- | --- | --- |
| The questions | A buyer wants to email the incumbent a clarification the others will not see | Needs confirmation |
| The answers they can give | Quote set, 3 vendors, recorded 14 September 2026. No supporting file attached | Carried into the draft |
| What must stay confidential | email and billing address only. They stated no health or payment data | Carried into the draft |
| The publication owner | Diane Cho, buyer | Needs confirmation |

**How this draft was built**

**1. Log each question**

**2. Draft an answer that does not reveal another bidder's confidential approach**

**3. Publish answers to all bidders when their process requires it**

**4. Do not give one bidder a private hint**

**5. Mark questions you cannot answer yet**

**Deliberately not done**
- A private hint to one bidder.
- An answer that leaks another bid.
- A changed requirement left unpublished.

**Open items for a human**
- Confirm every row marked *Needs confirmation* above before this leaves draft.
- Anything absent from the file stayed absent. No figure, date, or name was supplied from outside it.

Next: Diane Cho by 30 September 2026. This is a draft, not a sign-off.

## Anti-patterns

- A private hint to one bidder
- An answer that leaks another bid
- A changed requirement left unpublished

## Related skills

- `sourcing-event-brief`
- `rfi-writer`
