---
name: blog-source-note
description: "List what the post may cite, and what has to come out. Use when the user mentions blog sources, fact check a post, citation check, what can we cite, or asks for a source note. Blog and editorial skill by Yasir Jilani."
license: MIT
compatibility: Agent Skills standard. No network access, extra packages, or credentials required.
metadata:
  author: Yasir Jilani
  version: "1.0.0"
  domain: blog
---

<!-- GENERATED FILE - edits here are overwritten by scripts/generate.py.
     Edit the 'blog-source-note' entry in source/, then run:
       python3 scripts/generate.py && python3 scripts/validate.py
     See CONTRIBUTING.md. -->

# Blog Source Note

List what the post may cite, and what has to come out.

## When to use this skill

Use this skill when the user:

- blog sources
- fact check a post
- citation check
- what can we cite

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

- The claims
- The links or notes
- What is behind a login
- What is someone else's wording

## Workflow


### 1. Step 1

Match each claim to a note.
### 2. Step 2

A claim with no note comes out.
### 3. Step 3

Do not cite a page you cannot open.
### 4. Step 4

Mark wording that is too close to another article.
### 5. Step 5

Separate their receipts from a public dataset.
### 6. Step 6

Do not invent a citation.

## Output

Deliver a **source note**.

- Purpose of this source note, in two sentences.
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

The grocery draft cites a StatCan table Maya has not opened, and four receipts she has on the counter.

### Example data

```text
claim: food total $52 — source: her receipts
claim: pharmacy excluded — source: her note
claim: Calgary food up 4.2 percent — source line says StatCan, table not opened
wording: one paragraph is close to a news brief she saved
login-only PDF: not in the folder
```

### Example outcome

**Source note**
May cite: the four receipts and her pharmacy note.
Pull: the 4.2 percent sentence. The table was not opened.
Pull: the paragraph that tracks the saved news brief. Rewrite from her receipts or cut it.
Do not add the login-only PDF. It is not in the folder.
No replacement citation gets invented in this note.

## Anti-patterns

- A citation to a page they did not open
- A lifted paragraph
- A dataset they do not have

## Related skills

- `citation-hygiene`
- `blog-edit`
