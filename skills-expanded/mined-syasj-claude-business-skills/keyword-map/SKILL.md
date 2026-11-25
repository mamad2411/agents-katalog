---
name: keyword-map
description: "Map queries to pages the user already has, using only queries they exported or listed. Use when the user mentions keyword map, query mapping, which page for this query, SEO map, or asks for a query map. Search skill by Yasir Jilani."
license: MIT
compatibility: Agent Skills standard. No network access, extra packages, or credentials required.
metadata:
  author: Yasir Jilani
  version: "1.0.0"
  domain: seo
---

<!-- GENERATED FILE - edits here are overwritten by scripts/generate.py.
     Edit the 'keyword-map' entry in source/, then run:
       python3 scripts/generate.py && python3 scripts/validate.py
     See CONTRIBUTING.md. -->

# Keyword Map

Map queries to pages the user already has, using only queries they exported or listed.

## When to use this skill

Use this skill when the user:

- keyword map
- query mapping
- which page for this query
- SEO map

## When not to use this skill

- The user wants a different domain's specialist skill.
- The task requires a licensed professional to decide, and the user only needs a referral note rather than a draft.
- The request asks you to deceive, evade a control, or hide material facts.

## Professional boundary

Do not draft cloaking, doorway pages, hidden text, fake reviews, or link schemes. Use only queries and pages the user can show.

## Operating boundaries

- Use only information the user provides or files they explicitly ask you to read. Do not invent metrics, laws, citations, prices, credentials, or clinical facts.
- Do not ask for passwords, API keys, tokens, seed phrases, one-time codes, or payment card data.
- Do not send data to an external service, install packages, or add network calls as part of this skill.
- Separate facts, assumptions, and recommendations. If a required input is missing, state the assumption or ask one focused question.
- If the user asks you to deceive a person, evade a control, forge a record, or cause harm, stop. Offer a legitimate alternative.
- Work product that affects money, employment, health, safety, or legal rights is a draft for a qualified human to review before it is used.

## Inputs to collect

- The queries they listed
- The pages
- The page that already answers each
- Queries with no page

## Workflow


### 1. Step 1

One query, one page.
### 2. Step 2

If two pages answer it, pick the one they want and say the other should not compete.
### 3. Step 3

A query with no page is a gap, not a reason to invent a page today.
### 4. Step 4

Do not add queries from memory.
### 5. Step 5

Mark intent in their words.
### 6. Step 6

Do not recommend hidden text or a doorway page.

## Output

Deliver a **query map**.

- Purpose of this query map, in two sentences.
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

Diane listed eight queries for Harbor Goods. The site has a furnace page and an oil-change page. Two queries match neither.

### Example data

```text
pages: /services/furnace, /services/oil-change
queries she listed 18 Sep 2026:
furnace repair Airdrie -> furnace page
furnace tune-up Airdrie -> furnace page
emergency furnace Airdrie -> furnace page
oil change Airdrie -> oil-change page
synthetic oil change -> oil-change page
oil change price -> oil-change page
plumber Airdrie -> no page
roof repair -> no page
```

### Example outcome

**Query map**
| Query | Page |
| --- | --- |
| furnace repair Airdrie | /services/furnace |
| furnace tune-up Airdrie | /services/furnace |
| emergency furnace Airdrie | /services/furnace |
| oil change Airdrie | /services/oil-change |
| synthetic oil change | /services/oil-change |
| oil change price | /services/oil-change |

Gaps, not new doorway URLs: plumber Airdrie, roof repair. She does not do that work. Do not make pages for them.
Do not point furnace queries at the oil-change page.

## Anti-patterns

- Queries they did not list
- Two pages aimed at one query
- A doorway page

## Related skills

- `search-intent`
- `seo-content-brief`
