---
name: blog-edit
description: "Edit a draft against the notes, and mark claims that the notes do not support. Use when the user mentions edit this post, blog edit, line edit, claims check, or asks for a edit note. Blog and editorial skill by Yasir Jilani."
license: MIT
compatibility: Agent Skills standard. No network access, extra packages, or credentials required.
metadata:
  author: Yasir Jilani
  version: "1.0.0"
  domain: blog
---

<!-- GENERATED FILE - edits here are overwritten by scripts/generate.py.
     Edit the 'blog-edit' entry in source/, then run:
       python3 scripts/generate.py && python3 scripts/validate.py
     See CONTRIBUTING.md. -->

# Blog Edit

Edit a draft against the notes, and mark claims that the notes do not support.

## When to use this skill

Use this skill when the user:

- edit this post
- blog edit
- line edit
- claims check

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

- The draft
- The notes
- The assignment
- Words they must not add

## Workflow


### 1. Step 1

Check each factual sentence against the notes.
### 2. Step 2

Mark unsupported sentences. Do not replace them with your own facts.
### 3. Step 3

Cut repetition.
### 4. Step 4

Keep the writer's voice.
### 5. Step 5

Confirm the close matches the assignment.
### 6. Step 6

Do not add a product pitch that was not assigned.

## Output

Deliver a **edit note**.

- Purpose of this edit note, in two sentences.
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

Maya's draft is 680 words. One sentence says grocery prices in Calgary are up 18 percent. The notes have the four receipts and no index.

### Example data

```text
draft sentence: "Grocery prices in Calgary are up 18 percent this year."
notes: four receipts, food total $52, dates 10-14 Sep 2026
assignment: one kitchen, no city trend
other sentences: match the receipts
voice: hers, short
```

### Example outcome

**Edit note**
Cut: "Grocery prices in Calgary are up 18 percent this year." The notes do not have a percent or a city index. Do not replace it with a different percent.

Keep: the four stops, the pharmacy exclusion, the $52, the dates.
Do not add a provincial comparison to fill the cut.
The close still has to say this is one kitchen. If that sentence is missing, add her words, not a new fact.
Word count is fine. The 18 percent is the block.

## Anti-patterns

- New facts inserted by the editor
- A tone rewrite that changes a number
- Ignoring the notes

## Related skills

- `blog-source-note`
- `blog-outline`
