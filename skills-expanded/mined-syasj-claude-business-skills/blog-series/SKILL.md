---
name: blog-series
description: "Plan a series where each post can stand alone and the writer has notes for each part. Use when the user mentions blog series, content series, multi-part post, series plan, or asks for a series plan. Blog and editorial skill by Yasir Jilani."
license: MIT
compatibility: Agent Skills standard. No network access, extra packages, or credentials required.
metadata:
  author: Yasir Jilani
  version: "1.0.0"
  domain: blog
---

<!-- GENERATED FILE - edits here are overwritten by scripts/generate.py.
     Edit the 'blog-series' entry in source/, then run:
       python3 scripts/generate.py && python3 scripts/validate.py
     See CONTRIBUTING.md. -->

# Blog Series

Plan a series where each post can stand alone and the writer has notes for each part.

## When to use this skill

Use this skill when the user:

- blog series
- content series
- multi-part post
- series plan

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

- The parts
- Notes for each
- The publishing days
- The reader

## Workflow


### 1. Step 1

Cut parts that have no notes.
### 2. Step 2

Make each post useful alone.
### 3. Step 3

Order them by what the reader needs first.
### 4. Step 4

Set dates the writer can hit.
### 5. Step 5

Name the internal links.
### 6. Step 6

Do not promise a part that is not sourced.

## Output

Deliver a **series plan**.

- Purpose of this series plan, in two sentences.
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

Diane wants a four-part series for Harbor Goods: pricing, hiring, taxes, and ads. She has notes on her own prices and on the one hire she made. She has no tax notes and no ad results.

### Example data

```text
reader: a shop owner in Airdrie
parts asked: pricing, first hire, taxes, ads
notes: price list 2026, hire notes for Sam in June
no notes: tax, ads
days she can publish: Tuesday
```

### Example outcome

**Series**
Two posts. The other two are not scheduled.

| Part | Standalone promise | Date |
| --- | --- | --- |
| What she charges, from the 2026 list | a reader can compare a price | Tue 23 Sep |
| The June hire, hours and wage she recorded | a reader sees one real hire | Tue 30 Sep |

Taxes and ads: no notes, no date, no 'part 3 of 4' tease.
Each post makes sense if the reader never sees the other.

## Anti-patterns

- A five-part promise with notes for two
- Cliffhangers that hide the answer
- Copied series titles

## Related skills

- `blog-assignment`
- `content-calendar`
