---
name: serp-gap
description: "Compare the user's page to what they can see on the results page, without inventing ranks. Use when the user mentions SERP gap, why are we not ranking, results page review, competitor page, or asks for a gap note. Search skill by Yasir Jilani."
license: MIT
compatibility: Agent Skills standard. No network access, extra packages, or credentials required.
metadata:
  author: Yasir Jilani
  version: "1.0.0"
  domain: seo
---

<!-- GENERATED FILE - edits here are overwritten by scripts/generate.py.
     Edit the 'serp-gap' entry in source/, then run:
       python3 scripts/generate.py && python3 scripts/validate.py
     See CONTRIBUTING.md. -->

# SERP Gap

Compare the user's page to what they can see on the results page, without inventing ranks.

## When to use this skill

Use this skill when the user:

- SERP gap
- why are we not ranking
- results page review
- competitor page

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

- The query
- Their page
- What they personally see on the results page
- What they will not copy

## Workflow


### 1. Step 1

Describe only the results they looked at, with the date.
### 2. Step 2

Do not invent a rank or a search-volume number.
### 3. Step 3

Say what those pages answer that theirs does not.
### 4. Step 4

Recommend a factual gap to fill, not a copy.
### 5. Step 5

Do not copy another site's text.
### 6. Step 6

If they did not look, say so.

## Output

Deliver a **gap note**.

- Purpose of this gap note, in two sentences.
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

Diane searched 'furnace repair Airdrie' on 18 September and looked at the top three results she saw. She did not write down a rank for her own page. Those three pages show a city, a phone, and hours. Hers does not.

### Example data

```text
query: furnace repair Airdrie
date looked: 18 Sep 2026
her page has: origin story
pages she saw: three local service pages with city, phone, hours
her rank: not recorded
volume: not in any export
will not copy: their wording
```

### Example outcome

**Gap note**
No rank. She did not record one. No volume. None was exported.

Gap she can see: those pages state city, phone, and hours. Her furnace page does not.
Fill with her own facts: Airdrie, 403-555-0148, Mon-Sat 08:00-17:00, closed Sunday.
Do not copy their sentences. Do not add a review count she does not have.

## Anti-patterns

- A fake rank
- A copied paragraph
- Volume numbers from memory

## Related skills

- `keyword-map`
- `local-seo-note`
