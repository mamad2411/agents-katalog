---
name: seo-content-brief
description: "Brief a page that answers a real query, with search intent and substantiation, without keyword stuffing. Use when the user mentions SEO brief, content brief, rank for this keyword, search intent, or asks for a search content brief. Marketing skill by Yasir Jilani."
license: MIT
compatibility: Agent Skills standard. No network access, extra packages, or credentials required.
metadata:
  author: Yasir Jilani
  version: "1.0.0"
  domain: marketing
---

<!-- GENERATED FILE - edits here are overwritten by scripts/generate.py.
     Edit the 'seo-content-brief' entry in source/, then run:
       python3 scripts/generate.py && python3 scripts/validate.py
     See CONTRIBUTING.md. -->

# SEO Content Brief

Brief a page that answers a real query, with search intent and substantiation, without keyword stuffing.

## When to use this skill

Use this skill when the user:

- SEO brief
- content brief
- rank for this keyword
- search intent

## When not to use this skill

- The user wants a different domain's specialist skill.
- The task requires a licensed professional to decide, and the user only needs a referral note rather than a draft.
- The request asks you to deceive, evade a control, or hide material facts.

## Professional boundary

Do not invent testimonials, reviews, metrics, or claims the user cannot support. Do not draft spam, cloaking, fake scarcity, or impersonation.

## Operating boundaries

- Use only information the user provides or files they explicitly ask you to read. Do not invent metrics, laws, citations, prices, credentials, or clinical facts.
- Do not ask for passwords, API keys, tokens, seed phrases, one-time codes, or payment card data.
- Do not send data to an external service, install packages, or add network calls as part of this skill.
- Separate facts, assumptions, and recommendations. If a required input is missing, state the assumption or ask one focused question.
- If the user asks you to deceive a person, evade a control, forge a record, or cause harm, stop. Offer a legitimate alternative.
- Work product that affects money, employment, health, safety, or legal rights is a draft for a qualified human to review before it is used.

## Inputs to collect

- The query or topic
- What the searcher is trying to do
- Proof and sources the company has
- The page's business job

## Workflow


### 1. Intent

State the job of the searcher. If the user only has a keyword and no intent, say the brief is incomplete.
### 2. Promise

The page answers that job in the title and the first screen. No bait headline.
### 3. Outline

Sections that answer the query, plus what you will not cover so the page stays focused.
### 4. Evidence

Facts need a source the user can point to. No invented statistics or fake reviews.
### 5. Internal path

Where the reader goes next if they are a fit. One path.
### 6. Measurement

The query and the on-page action, reviewed after publication. Rankings are not ordered into existence by repetition.

## Output

Deliver a **search content brief**.

- Purpose of this search content brief, in two sentences.
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

Lena Ortiz, marketing lead at Fieldnote in Edmonton, needs a search content brief by 30 September 2026. A team wants a page targeting a high-volume keyword that does not match the product.

### Example data

```text
From: Lena Ortiz, marketing lead
Organization: Fieldnote, Edmonton
Date: 14 September 2026
Needed by: 30 September 2026

A team wants a page targeting a high-volume keyword that does not match the product.

The query or topic: Fall service page, recorded 14 September 2026. No supporting file attached
What the searcher is trying to do: Local search ad, last reviewed 14 September 2026. No owner named since
Proof and sources the company has: one customer email, 14 September 2026, no attachment beyond that
The page's business job: Fall service page, recorded 14 September 2026. No supporting file attached
```

### Example outcome

**Search content brief**
To: Lena Ortiz, marketing lead, Fieldnote
Date: 14 September 2026 · Needed by: 30 September 2026

**Decision**
Either resets the intent or recommends not writing the page, instead of stuffing the keyword.

**What the file supports**

| Input | Value | Status |
| --- | --- | --- |
| The query or topic | Fall service page, recorded 14 September 2026. No supporting file attached | Needs confirmation |
| What the searcher is trying to do | Local search ad, last reviewed 14 September 2026. No owner named since | Carried into the draft |
| Proof and sources the company has | one customer email, 14 September 2026, no attachment beyond that | Carried into the draft |
| The page's business job | Fall service page, recorded 14 September 2026. No supporting file attached | Needs confirmation |

**How this draft was built**

**1. Intent**  
State the job of the searcher. If the user only has a keyword and no intent, say the brief is incomplete.

**2. Promise**  
The page answers that job in the title and the first screen. No bait headline.

**3. Outline**  
Sections that answer the query, plus what you will not cover so the page stays focused.

**4. Evidence**  
Facts need a source the user can point to. No invented statistics or fake reviews.

**5. Internal path**  
Where the reader goes next if they are a fit. One path.

**Deliberately not done**
- Keyword stuffing.
- Invented data to look authoritative.
- A brief that ignores intent.

**Open items for a human**
- Confirm every row marked *Needs confirmation* above before this leaves draft.
- Anything absent from the file stayed absent. No figure, date, or name was supplied from outside it.

Next: Lena Ortiz by 30 September 2026. This is a draft, not a sign-off.

## Anti-patterns

- Keyword stuffing.
- Invented data to look authoritative.
- A brief that ignores intent.

## Related skills

- `content-calendar`
- `marketing-claims-review`
