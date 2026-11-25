---
name: team-prd
description: Product requirements document (PRD) writing methodology. Scope, out of scope, user stories, acceptance criteria and success metrics. The playbook of the pm role.
---

# Writing a PRD

## What a PRD is for

A PRD is not a document, it is a **contract**. Its purpose: everyone agrees on what will and will not be done in version 1.

That is why the most valuable section is **Out of Scope**. When someone says "let's also do this", the out-of-scope list is consulted.

## 1. Summary

3 sentences. Who, which problem, how we solve it. Do not write an introductory paragraph.

## 2. Problem and target audience

- Problem: the measurable pain the user experiences today.
- Target audience: **one** primary segment. Not "small businesses", but "agencies with 5-20 employees".
- Why now: a timing rationale.

## 3. Scope / Out of scope

Two lists, of equal length.

**In scope** items:
- One sentence, starting with a verb ("The user can upload an invoice")
- Each item is an observable behavior
- Testable ("visible" / "not visible" can be answered)

**Out of scope** items:
- Things that will not be done in version 1
- A "for now" rationale (under which condition it is reconsidered)
- This list is a later negotiation tool

The out-of-scope items that are written down are the things everyone says "maybe" to. If you do not write them down, they will be added later.

## 4. User stories and acceptance criteria

Format:

```
Story: As a <role> I want <behavior>, so that <value>.

Acceptance criteria:
- [ ] <testable statement>
- [ ] <testable statement>
```

An acceptance criterion must be testable. Not "the user will be happy". "The list loads in under 2 seconds at 500 rows" can be answered with yes or no — that one is.

**Split a story that contains more than one "and".** A story with two acceptance criteria is sometimes two stories.

Number of stories: 8-15. More means surprise; fewer covers the scope incompletely.

## 5. Success metrics

Measurable conditions for the product to be considered successful. For each one:

| Metric | Baseline | Target | How it is measured |
|---|---|---|---|
| Weekly active users | ? | ? | ? |

Do not make up numbers. If you do not know the target, say "target to be determined" and mark it as an open question. Writing an estimated target and presenting it as real becomes a source of later discussion.

## 6. Risks and open questions

- Risk: what happens, probability, impact, mitigation
- Open question: a question without an answer, waiting for a decision. Who will answer it?

## Common mistakes

| Mistake | The right way |
|---|---|
| Writing the solution ("store it with PostgreSQL") | Write the need ("should be able to store the invoice") |
| 40 stories | 8-15 stories, at most |
| An unmeasurable success metric | Write a number or say "to be determined" |
| Not writing out of scope | Always write it |
| Embedding technical design | Architecture is a separate stage |
| More than one target audience | Pick a single segment |

## Output format

Markdown. Sections: Summary / Problem and target audience / Scope / Out of scope / User stories + acceptance criteria / Success metrics / Risks and open questions.

In the user's language (Turkish or English).
