---
name: blog-refresh
description: "Update an old post with what changed, and label the update. Use when the user mentions update this post, refresh an article, blog update, evergreen edit, or asks for a update note. Blog and editorial skill by Yasir Jilani."
license: MIT
compatibility: Agent Skills standard. No network access, extra packages, or credentials required.
metadata:
  author: Yasir Jilani
  version: "1.0.0"
  domain: blog
---

<!-- GENERATED FILE - edits here are overwritten by scripts/generate.py.
     Edit the 'blog-refresh' entry in source/, then run:
       python3 scripts/generate.py && python3 scripts/validate.py
     See CONTRIBUTING.md. -->

# Blog Refresh

Update an old post with what changed, and label the update.

## When to use this skill

Use this skill when the user:

- update this post
- refresh an article
- blog update
- evergreen edit

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

- The old post
- What changed
- The new source
- The date of the old claims

## Workflow


### 1. Step 1

List claims that are now wrong or undated.
### 2. Step 2

Replace only what the new source supports.
### 3. Step 3

Put an update line with the date at the top.
### 4. Step 4

Do not leave a stale price unlabeled.
### 5. Step 5

Say what you could not recheck.
### 6. Step 6

Keep the original date as well as the update date.

## Output

Deliver a **update note**.

- Purpose of this update note, in two sentences.
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

A March 2024 post on Harbor Goods' site still says a sidewalk-display permit is $50. Diane has a 2026 town fee sheet that says $75. She wants the post updated without pretending it was always $75.

### Example data

```text
old post: 12 Mar 2024, "Sidewalk display permit: $50"
new source: town fee sheet, effective 1 Jan 2026, display permit $75
what she could not recheck: the inspection wait time, still written as "about a week"
update date: 20 Sep 2026
```

### Example outcome

**Update**
Add at the top: Updated 20 September 2026. The fee below was corrected. The 12 March 2024 date stays on the post.

Replace $50 with $75, tied to the fee sheet effective 1 January 2026.
Leave the inspection sentence, and mark it unchecked: "about a week" was not on the 2026 sheet.
Do not delete the 2024 date. Do not write that the fee was always $75.

## Anti-patterns

- A silent change of a number
- A new claim with no source
- Deleting the original date

## Related skills

- `blog-edit`
- `content-refresh-seo`
