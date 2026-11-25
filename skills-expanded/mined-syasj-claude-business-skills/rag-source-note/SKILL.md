---
name: rag-source-note
description: "Decide which documents may sit in a retrieval set and which are stale or out of bounds. Use when the user mentions RAG sources, what can the bot search, knowledge base for AI, retrieval set, or asks for a source pack note. AI in the business skill by Yasir Jilani."
license: MIT
compatibility: Agent Skills standard. No network access, extra packages, or credentials required.
metadata:
  author: Yasir Jilani
  version: "1.0.0"
  domain: ai
---

<!-- GENERATED FILE - edits here are overwritten by scripts/generate.py.
     Edit the 'rag-source-note' entry in source/, then run:
       python3 scripts/generate.py && python3 scripts/validate.py
     See CONTRIBUTING.md. -->

# RAG Source Note

Decide which documents may sit in a retrieval set and which are stale or out of bounds.

## When to use this skill

Use this skill when the user:

- RAG sources
- what can the bot search
- knowledge base for AI
- retrieval set

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

- The collection list
- The as-of date of each doc
- Topics the bot must not answer
- The owner of the set

## Workflow


### 1. Step 1

List documents with dates. Undated is a gap.
### 2. Step 2

Cut documents the user says are drafts or superseded.
### 3. Step 3

Name topics the bot should refuse rather than guess.
### 4. Step 4

Say who updates the set.
### 5. Step 5

Do not add web pages they did not approve.
### 6. Step 6

Recommend a review date.

## Output

Deliver a **source pack note**.

- Purpose of this source pack note, in two sentences.
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

The support bot's folder has a 2023 refund policy and the 2026 policy, plus a draft price list marked 'do not share'. Jonah needs the set cut down.

### Example data

```text
files: refund-policy-2023.pdf, refund-policy-2026-03.pdf, price-draft-2026-08 marked do not share, shipping-faq undated
owner: Jonah Park
topics the bot must not answer: legal threats, medical, card numbers
review date wanted: 1 Oct 2026
```

### Example outcome

**Source pack**
In the set: refund-policy-2026-03.pdf only, for refund questions.
Out: the 2023 policy. Out: the August price draft.
Shipping FAQ: out until someone dates it.
Refuse rather than guess: legal threats, medical questions, anything with a card number.
Owner: Jonah. Review the set on 1 October 2026.
Do not add web pages to fill a gap.

## Anti-patterns

- An undated policy treated as current
- The open web as a silent source
- No owner

## Related skills

- `ai-data-note`
- `knowledge-base-article`
