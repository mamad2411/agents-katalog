---
name: brainstorm-prd
description: "The product requirements document, docs/plan/PRD.md: the problem, who it is for, goals and non-goals, the first version's scope by priority, numbered requirements each with acceptance criteria a checker can run, non-functional needs, content and placeholders, open questions and the decisions log. Read when writing or updating a PRD."
---

# PRD.md: what is built, and how each piece is accepted

A PRD answers three questions for every agent that will touch the work:
what are we building, what is out, and how do we know a piece is done.
The naive one is a page of marketing ("a modern, seamless platform that
empowers users") with no scope line, requirements nobody can test, and
users the model invented. This template keeps it to decisions.

## 1. The template

```markdown
# <Product or feature>: PRD

Status: draft | agreed <date> | building | shipped
Source: <where the decisions came from: the conversation on <date>, a brief the user pasted>

## Problem
<Two to four lines: what is wrong or missing today, for whom, in the user's terms.>

## Users
- <Who uses it and what they come to do. Only people the user named or the product plainly serves.>

## Goals
- <What the first version must make possible. Outcomes, not features.>

## Non-goals
- <What it deliberately does not do yet. As important as the goals: it stops scope creep in every brief.>

## Scope
| Priority | Includes |
|---|---|
| Must (v1) | ... |
| Should (v1 if time allows) | ... |
| Later | ... |

## Requirements
### FR-1 <short name>
<One or two lines: what the user can do.>
Acceptance:
- Given <state>, when <action>, then <observable result>.
- ...

### FR-2 ...

## Non-functional
- Platforms and sizes: <phones first; 360 to 1440px>
- Accessibility: <WCAG 2.2 AA; keyboard use>
- Language: <Indonesian copy; dates as 29 Sep 2026>
- Performance, security, privacy: <only what applies>

## Content and data
- <Where content comes from: the user's text, a CMS, an import. What is a placeholder, listed.>

## Open questions
- <What only the user can decide, and what depends on it.>

## Decisions
- <date> <decision>, <by whom / why>
```

## 2. Writing each part

- **Problem and users** come from the conversation. When the user did not
  say who it is for, write the plain reading ("people booking a table at
  this restaurant") and never a persona with an invented name, age and
  job.
- **Goals are outcomes** ("a customer can book and get a confirmation"),
  not features ("booking module"). Three to five.
- **Non-goals** name what someone might assume is included: accounts,
  payments, an admin panel, dark mode, other languages, mobile apps.
- **Scope by priority.** Must is the smallest version the user would call
  done. When the user asked for everything, Must is still the first slice;
  say so in the summary.
- **Requirements are numbered and testable.** One `FR-n` per capability a
  user can see. Acceptance in Given/When/Then, each line something `test`
  or `review` can check in a browser or with a request:

```markdown
### FR-3 Filter the catalogue by category
A shopper narrows the product grid to one category.
Acceptance:
- Given the catalogue with products in "Shoes" and "Bags", when the shopper picks "Shoes", then only shoes show and the URL has `?category=shoes`.
- Given a filtered URL opened directly, then the same filter is applied.
- Given a category with no products, then the grid says "Belum ada produk di kategori ini" and offers to clear the filter.
```

- **Edge states belong in acceptance**: empty, loading, error, too long,
  none found, not allowed. They are where generated software breaks.
- **Non-functional** lines only for what applies, with numbers where the
  user or the platform gives them. Not a wish list.
- **Metrics** only when the user named them; a PRD for a portfolio has
  none.
- **Open questions** are real: each is something only the user can decide,
  with what it blocks. Ask them with `ask` rather than leaving them for the
  specialists to guess.

## 3. For a feature in an existing product

Shorter: Problem, Scope, the new `FR-n`, what existing behaviour must not
change ("existing orders keep their prices"), Decisions. Number new
requirements after the last one in an existing PRD, or start a new file
named for the feature (`docs/plan/PRD-invoices.md`) when there is none.

## 4. After it is written

- Briefs cite requirements by number; `review` and `test` check the
  acceptance lines.
- A change of scope is a new line under Decisions and an edit to Scope and
  the requirements, never a silent drift in a brief.

## Check it

- Every `FR-n` has acceptance lines that can be checked by someone who did
  not write the code.
- Non-goals exist and name the likely assumptions.
- Nothing in it is invented: users, numbers, prices and content trace to
  the user or are marked as placeholders.
- It fits on a few screens.

## Avoid

Marketing prose; invented personas and metrics; requirements without
acceptance; "the system should be fast and secure"; a Must list with
everything in it; open questions the orchestrator could have asked.
