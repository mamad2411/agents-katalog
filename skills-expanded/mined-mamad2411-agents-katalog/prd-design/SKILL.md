---
name: prd-design
description: Use when writing, reviewing, refining, or structuring product requirement documents, feature specs, release plans, scope docs, or requirement outlines, especially when clarifying goals, users, assumptions, non-goals, success metrics, acceptance criteria, risks, dependencies, and open questions
license: MIT
metadata:
  author: vowdemon
  version: "1.0"
---

# PRD Design

## Overview

Structure PRDs so they are clear, scoped, reviewable, and useful for implementation. A good PRD explains the problem, who it is for, what success looks like, what is in scope, what is not, and what must be true before building.

## First Pass

Before writing or revising a PRD, answer briefly:

1. What problem are we solving?
2. Who is this for?
3. Why now?
4. What outcome defines success?
5. What is explicitly out of scope?
6. What assumptions or constraints might change the plan?
7. What is still unknown?

If the answer to any of these is unclear, ask first instead of filling gaps with vague prose.

## Required Sections

A solid PRD usually includes these sections, adapted to the project size:

- Title and short summary
- Problem statement
- Goals
- Target users / personas
- User scenarios or use cases
- Scope
- Non-goals / out of scope
- Requirements
- Acceptance criteria
- Success metrics
- Assumptions and constraints
- Risks and dependencies
- Open questions
- Rollout / release notes when relevant

Not every PRD needs every section, but every PRD should make scope, success, and non-goals explicit.

## Writing Rules

- Write for alignment, not for decoration.
- Prefer concrete statements over abstract aspirations.
- Separate goals from solutions.
- Separate requirements from implementation details.
- Use plain language that product, design, engineering, and QA can all read.
- Make terms consistent; if a concept matters, name it once and reuse the same wording.
- Write requirements so they can be checked, demonstrated, or tested.
- Use `must`, `should`, and `may` carefully when the distinction matters.
- Keep each requirement atomic when possible.
- Avoid empty phrases like "user-friendly", "robust", "efficient", or "seamless" unless they are defined.

## Scope Rules

A PRD is too broad when it tries to do any of these at once:

- Define the product vision and the implementation plan in the same depth
- Mix multiple unrelated user problems in one document
- Cover several release phases without separating them
- Describe both business requirements and technical architecture in full detail
- Leave no room for non-goals or tradeoffs

Split the document when necessary. A good split usually follows one of these lines:

- One problem, one PRD
- One release, one PRD
- One major user journey, one PRD
- One epic, one PRD

## Requirement Quality

Good requirements are:

- Specific
- Testable
- Traceable
- Unambiguous
- Feasible within the stated constraints

Weak requirements are:

- Vague
- Opinion-based
- Impossible to verify
- Hidden inside examples
- Mixed with implementation decisions

Convert weak requirements into measurable ones whenever possible.

## Review Checklist

Before finalizing a PRD, check that it answers these questions:

- What problem is being solved?
- Who benefits?
- What does success look like?
- What is not included?
- What assumptions are being made?
- What does the team need to build or change?
- How will we know it worked?
- What risks or dependencies might block delivery?
- What questions still need decisions?

## Red Flags

Stop and revise when you notice:

- Goals and solutions are mixed together.
- The document has no non-goals.
- Success is described only as a feeling.
- Requirements are vague enough to interpret multiple ways.
- The PRD contains implementation detail that belongs in a design doc.
- The PRD tries to describe too many unrelated problems.
- Unknowns are hidden instead of called out.
- The document would require a long meeting to explain.

## Common Mistakes

| Mistake | Correction |
| --- | --- |
| Writing a feature wish list | Rewrite around one problem, one user, one outcome |
| Mixing product and technical design | Keep implementation details out unless they are explicit constraints |
| Omitting non-goals | State what this PRD will not cover |
| Using vague success language | Convert to measurable outcomes or acceptance criteria |
| Overloading one document | Split by release, epic, or user journey |
| Treating assumptions as facts | Mark them clearly and revisit when evidence changes |
