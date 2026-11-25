---
name: content-refresh-seo
description: "Decide whether an old URL should be updated, from the query and the stale claim. Use when the user mentions update this URL, content refresh SEO, stale page, refresh versus new URL, or asks for a refresh note. Search skill by Yasir Jilani."
license: MIT
compatibility: Agent Skills standard. No network access, extra packages, or credentials required.
metadata:
  author: Yasir Jilani
  version: "1.0.0"
  domain: seo
---

<!-- GENERATED FILE - edits here are overwritten by scripts/generate.py.
     Edit the 'content-refresh-seo' entry in source/, then run:
       python3 scripts/generate.py && python3 scripts/validate.py
     See CONTRIBUTING.md. -->

# Search Refresh

Decide whether an old URL should be updated, from the query and the stale claim.

## When to use this skill

Use this skill when the user:

- update this URL
- content refresh SEO
- stale page
- refresh versus new URL

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

- The URL
- The query
- The stale sentence
- The new fact they can source

## Workflow


### 1. Step 1

Keep the URL if the query still matches the page's job.
### 2. Step 2

Replace the stale sentence only with the sourced fact.
### 3. Step 3

Put the update date.
### 4. Step 4

A new URL is for a new job, not for a date change.
### 5. Step 5

Do not add a city or a price they cannot source.
### 6. Step 6

Do not cloak the old content for bots.

## Output

Deliver a **refresh note**.

- Purpose of this refresh note, in two sentences.
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

The page /permits/sidewalk still ranks for a query Diane wants. It says the fee is $50. The 2026 fee sheet says $75. Someone suggested a new URL so the old one can stay.

### Example data

```text
url: /permits/sidewalk
query she still wants: sidewalk display permit Airdrie
stale sentence: fee is $50
new fact: town fee sheet, 1 Jan 2026, $75
new URL suggested: /permits/sidewalk-2026
```

### Example outcome

**Refresh note**
Keep /permits/sidewalk. The query is the same job.
Replace $50 with $75 and cite the fee sheet. Add: updated 20 September 2026.
Do not make /permits/sidewalk-2026. A new URL is a new job. This is not one.
Do not show the old fee to people and the new fee to crawlers. One page, one fee.

## Anti-patterns

- A new URL for the same job
- A silent price change
- Cloaking

## Related skills

- `blog-refresh`
- `keyword-map`
