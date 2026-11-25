---
name: index-coverage
description: "Read an index export and say which URLs are out and why the export says so. Use when the user mentions index coverage, not indexed, coverage report, pages not in search, or asks for a index note. Search skill by Yasir Jilani."
license: MIT
compatibility: Agent Skills standard. No network access, extra packages, or credentials required.
metadata:
  author: Yasir Jilani
  version: "1.0.0"
  domain: seo
---

<!-- GENERATED FILE - edits here are overwritten by scripts/generate.py.
     Edit the 'index-coverage' entry in source/, then run:
       python3 scripts/generate.py && python3 scripts/validate.py
     See CONTRIBUTING.md. -->

# Index Coverage

Read an index export and say which URLs are out and why the export says so.

## When to use this skill

Use this skill when the user:

- index coverage
- not indexed
- coverage report
- pages not in search

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
- The URLs they care about
- A noindex they know about
- Who can change the template

## Workflow


### 1. Step 1

Count from the export.
### 2. Step 2

Group by the reason in the export.
### 3. Step 3

A test noindex they know about is a finding, not a mystery.
### 4. Step 4

Do not promise indexation.
### 5. Step 5

Name the owner of the template.
### 6. Step 6

Ignore URLs they said do not matter.

## Output

Deliver a **index note**.

- Purpose of this index note, in two sentences.
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

Diane exported coverage on 18 September. 30 URLs are excluded. 9 are the blog, reason noindex. The other 21 are old tag URLs she says do not matter.

### Example data

```text
export date: 18 Sep 2026
excluded: 30
reason noindex: 9, all /blog/
reason crawled not indexed: 21, all /tag/
she cares about: the 9 blog URLs
she does not care about: /tag/
template owner: Sam
known test: blog noindex added in March
```

### Example outcome

**Index note**
The 9 blog URLs are out because of noindex. That matches the March test. Remove it.
The 21 tag URLs are in the export and out of scope. Do not spend the month on them.
This note does not say the blog will rank after the tag is removed. Indexing is not a rank.
Owner: Sam. Diane rechecks one blog URL after the Friday deploy.

## Anti-patterns

- A promise that a page will rank once indexed
- Reasons not in the export
- Panic over URLs they do not care about

## Related skills

- `technical-seo-note`
- `blog-refresh`
