---
name: blog-outline
description: "Outline a post from the assignment and the notes, with headings the writer can draft from. Use when the user mentions blog outline, post structure, article outline, heading plan, or asks for a outline. Blog and editorial skill by Yasir Jilani."
license: MIT
compatibility: Agent Skills standard. No network access, extra packages, or credentials required.
metadata:
  author: Yasir Jilani
  version: "1.0.0"
  domain: blog
---

<!-- GENERATED FILE - edits here are overwritten by scripts/generate.py.
     Edit the 'blog-outline' entry in source/, then run:
       python3 scripts/generate.py && python3 scripts/validate.py
     See CONTRIBUTING.md. -->

# Blog Outline

Outline a post from the assignment and the notes, with headings the writer can draft from.

## When to use this skill

Use this skill when the user:

- blog outline
- post structure
- article outline
- heading plan

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

- The assignment
- The notes
- The length
- What must be cited

## Workflow


### 1. Step 1

Open with the question.
### 2. Step 2

One heading per point they have notes for.
### 3. Step 3

Mark a heading with no note as a hole.
### 4. Step 4

Put the sources under the headings.
### 5. Step 5

Close with what the reader can do.
### 6. Step 6

Do not add a study you did not read.

## Output

Deliver a **outline**.

- Purpose of this outline, in two sentences.
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

Maya has the assignment and the four receipts. She also sketched a heading called 'the provincial trend' with no note under it.

### Example data

```text
assignment: one kitchen, week of 14 Sep, $52 food
notes: Co-op $18.40, Co-op $22.10, market $11.50, pharmacy excluded
length: 700 words
blank heading: the provincial trend
must cite: each receipt date
```

### Example outcome

**Outline**
H1: What this kitchen spent on food, week of 14 September

H2: The four stops — notes exist
H2: What was not food — pharmacy line, notes exist
H2: The $52 total — her sum, notes exist
H2: What this does not show — one kitchen, one week

Cut: 'the provincial trend'. No note, no heading.
Close: the reader can lay their own receipts next to this. They cannot learn a city rate from it.
Each receipt date goes under the first H2.

## Anti-patterns

- Headings with no notes
- A fake study
- An outline of someone else's post

## Related skills

- `blog-assignment`
- `blog-edit`
