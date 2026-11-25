---
name: blog-assignment
description: "Assign a post with the reader, the question, the source, and the date. Use when the user mentions blog assignment, post brief, assign an article, blog brief, or asks for a assignment. Blog and editorial skill by Yasir Jilani."
license: MIT
compatibility: Agent Skills standard. No network access, extra packages, or credentials required.
metadata:
  author: Yasir Jilani
  version: "1.0.0"
  domain: blog
---

<!-- GENERATED FILE - edits here are overwritten by scripts/generate.py.
     Edit the 'blog-assignment' entry in source/, then run:
       python3 scripts/generate.py && python3 scripts/validate.py
     See CONTRIBUTING.md. -->

# Blog Assignment

Assign a post with the reader, the question, the source, and the date.

## When to use this skill

Use this skill when the user:

- blog assignment
- post brief
- assign an article
- blog brief

## When not to use this skill

- The user wants a different domain's specialist skill.
- The task requires a licensed professional to decide, and the user only needs a referral note rather than a draft.
- The request asks you to deceive, evade a control, or hide material facts.

## Professional boundary

Do not copy another publication's article. Do not invent sources, quotes, or results. Label an update when a post is refreshed.

## Operating boundaries

- Use only information the user provides or files they explicitly ask you to read. Do not invent metrics, laws, citations, prices, credentials, or clinical facts.
- Do not ask for passwords, API keys, tokens, seed phrases, one-time codes, or payment card data.
- Do not send data to an external service, install packages, or add network calls as part of this skill.
- Separate facts, assumptions, and recommendations. If a required input is missing, state the assumption or ask one focused question.
- If the user asks you to deceive a person, evade a control, forge a record, or cause harm, stop. Offer a legitimate alternative.
- Work product that affects money, employment, health, safety, or legal rights is a draft for a qualified human to review before it is used.

## Inputs to collect

- The reader
- The question
- Sources already in hand
- The due date

## Workflow


### 1. Step 1

Write the question the post answers.
### 2. Step 2

Name the reader.
### 3. Step 3

List sources they have. A post with no source does not get a date.
### 4. Step 4

Set a due date they can hit.
### 5. Step 5

Say what the post will not claim.
### 6. Step 6

Do not assign a copied angle from another site.

## Output

Deliver a **assignment**.

- Purpose of this assignment, in two sentences.
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

Maya wants a Friday post on Calgary grocery prices. She has four receipts from 10 to 14 September and no index, no StatCan table, and no store permission.

### Example data

```text
reader: Calgary home cooks who shop once a week
question: what did one kitchen spend on food this week
sources in hand: 4 receipts, 10-14 Sep 2026, food total $52
not in hand: a price index, a store comment, another household
due asked: Friday 19 Sep 2026
will not claim: a city trend
```

### Example outcome

**Assignment**
Question: what did this kitchen spend on food in the week of 14 September?
Reader: a Calgary home cook comparing their own week, not a policy audience.
Sources: the four receipts. Food total $52. Pharmacy line excluded.
Due: 19 September, only if the post stays inside those receipts.
Not assigned: a city trend, a store ranking, a percent change.
If the draft grows past the receipts, the date slips. Do not fill the hole with an unread table.

## Anti-patterns

- A due date with no source
- A copied outline
- A claim bigger than the notes

## Related skills

- `blog-outline`
- `blog-source-note`
