---
name: internal-links
description: "Plan internal links from pages that exist to pages that answer the next question. Use when the user mentions internal links, site links, link plan, related pages, or asks for a link plan. Search skill by Yasir Jilani."
license: MIT
compatibility: Agent Skills standard. No network access, extra packages, or credentials required.
metadata:
  author: Yasir Jilani
  version: "1.0.0"
  domain: seo
---

<!-- GENERATED FILE - edits here are overwritten by scripts/generate.py.
     Edit the 'internal-links' entry in source/, then run:
       python3 scripts/generate.py && python3 scripts/validate.py
     See CONTRIBUTING.md. -->

# Internal Link Plan

Plan internal links from pages that exist to pages that answer the next question.

## When to use this skill

Use this skill when the user:

- internal links
- site links
- link plan
- related pages

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

- The source pages
- The target pages
- The anchor words they will use
- Pages they do not want linked

## Workflow


### 1. Step 1

Link only to URLs they listed.
### 2. Step 2

Anchors must match the target, not a keyword they wish they ranked for.
### 3. Step 3

Do not add a link on every paragraph.
### 4. Step 4

Skip pages they marked no.
### 5. Step 5

Say which links are in the body, not the footer spam block.
### 6. Step 6

Do not recommend buying links or a link scheme.

## Output

Deliver a **link plan**.

- Purpose of this link plan, in two sentences.
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

Diane wants the furnace page to link to oil changes. A draft anchor says 'emergency plumber'. The oil-change page is about oil changes. She does not want a link to the blog test.

### Example data

```text
source: /services/furnace
target she wants: /services/oil-change
anchor in the draft: emergency plumber
blog: /blog/*, noindex, do not link
other target: none
```

### Example outcome

**Link plan**
One body link, not a footer dump.

From /services/furnace to /services/oil-change.
Anchor: oil changes, or synthetic oil change. Not 'emergency plumber'. That is a different job, and she has no plumber page.
No links to /blog/ while the test noindex is on.
No links to other domains.

## Anti-patterns

- A link scheme
- Anchors that misstate the target
- Links to URLs that are not theirs

## Related skills

- `keyword-map`
- `information-architecture`
