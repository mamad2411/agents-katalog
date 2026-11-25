---
name: blog-title-pack
description: "Write title options that the draft can support, with no borrowed viral headline. Use when the user mentions blog titles, headline options, post title, H1 options, or asks for a title options. Blog and editorial skill by Yasir Jilani."
license: MIT
compatibility: Agent Skills standard. No network access, extra packages, or credentials required.
metadata:
  author: Yasir Jilani
  version: "1.0.0"
  domain: blog
---

<!-- GENERATED FILE - edits here are overwritten by scripts/generate.py.
     Edit the 'blog-title-pack' entry in source/, then run:
       python3 scripts/generate.py && python3 scripts/validate.py
     See CONTRIBUTING.md. -->

# Blog Title Pack

Write title options that the draft can support, with no borrowed viral headline.

## When to use this skill

Use this skill when the user:

- blog titles
- headline options
- post title
- H1 options

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

- The draft's actual result
- Words they will not use
- The search query if they have one
- The title they hoped to copy

## Workflow


### 1. Step 1

Write options from the result in the draft.
### 2. Step 2

Cut a title that promises a number the draft does not have.
### 3. Step 3

If a query is in the file, use it only if the draft answers it.
### 4. Step 4

Reject a copied viral headline.
### 5. Step 5

Give three options, not thirty.
### 6. Step 6

Pick one and say why.

## Output

Deliver a **title options**.

- Purpose of this title options, in two sentences.
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

Maya hoped to title the post 'Grocery prices up 18 percent in Calgary'. The draft does not contain 18 percent. It contains $52 and four receipts.

### Example data

```text
draft result: $52 food, four receipts, one kitchen, week of 14 Sep
query in a notebook: calgary grocery prices
title she hoped to copy: a news headline about an 18 percent jump
words she will not use: crisis, shocking
```

### Example outcome

**Titles**
1. What I spent on food this week: $52
2. Four receipts, one Calgary kitchen, week of 14 September
3. This is not a grocery index

Use 1. It is the number in the draft.
No on 'Grocery prices up 18 percent in Calgary'. The draft cannot support it.
The notebook query is not a reason to promise a city answer. The post does not answer that query.

## Anti-patterns

- A title with a fake percent
- A copied headline
- A title that answers a different post

## Related skills

- `blog-edit`
- `headline-check`
