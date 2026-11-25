---
name: technical-seo-note
description: "Turn crawl findings the user exported into a fix list a developer can accept or reject. Use when the user mentions technical SEO, crawl errors, index issues, site audit, or asks for a technical note. Search skill by Yasir Jilani."
license: MIT
compatibility: Agent Skills standard. No network access, extra packages, or credentials required.
metadata:
  author: Yasir Jilani
  version: "1.0.0"
  domain: seo
---

<!-- GENERATED FILE - edits here are overwritten by scripts/generate.py.
     Edit the 'technical-seo-note' entry in source/, then run:
       python3 scripts/generate.py && python3 scripts/validate.py
     See CONTRIBUTING.md. -->

# Technical SEO Note

Turn crawl findings the user exported into a fix list a developer can accept or reject.

## When to use this skill

Use this skill when the user:

- technical SEO
- crawl errors
- index issues
- site audit

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

- The export
- The template they use
- Who deploys
- What they will not change this month

## Workflow


### 1. Step 1

Use rows from the export.
### 2. Step 2

Group by template, not by every URL.
### 3. Step 3

Cut findings they said are out of scope.
### 4. Step 4

Do not invent a ranking lift.
### 5. Step 5

Name the owner.
### 6. Step 6

Separate a blocked page from a slow page if the export shows which.

## Output

Deliver a **technical note**.

- Purpose of this technical note, in two sentences.
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

A crawl of 40 Harbor Goods URLs on 18 September shows 12 service URLs with an empty title and every /blog URL marked noindex. Diane says the blog block was a March test.

### Example data

```text
export: 40 URLs, 18 Sep 2026
empty title: 12 URLs, all under /services/
noindex: 9 URLs, all under /blog/
out of scope this month: a redesign
deploy owner: her contractor, Sam, Fridays
```

### Example outcome

**Fix list**
1. Title template on /services/. 12 URLs, one template, not 12 projects.
2. Remove the March test noindex on /blog/. 9 URLs.

Not this month: a redesign.
No ranking lift is claimed. The export does not show ranks.
Owner: Sam, Friday deploy. Diane checks one service URL and one blog URL after.

## Anti-patterns

- A ranking promise
- Findings not in the export
- A rewrite of the whole site

## Related skills

- `index-coverage`
- `technical-design-doc`
