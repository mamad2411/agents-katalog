---
name: code-review
description: Review code for correctness, readability, design, tests, security, and style. Produce actionable, kind, prioritized feedback.
category: development
aliases:
- review
- pr-review
- peer-review
triggers:
- review this code
- review this python code
- review this python code for security problems
- review my PR
- code review
- look at this diff
- is this code good
keywords:
- review
- pr
- diff
- feedback
- critique
- comment
- approve
dependencies: []
risk: low
version: 1.0.0
source: custom
enabled: true
author: Mr-Nobody-Anonymous
tags:
- code
- development
- diff
- feedback
- review
compatibility:
  claude-code: '>=1.0'
  skillhub: '*'
  cursor: '>=0.40'
  codex: '*'
network_access: false
filesystem_access: read
credential_access: false
destructive_operations: false
---

# Code Review

## Purpose

Provide a thorough, prioritized, kind code review covering correctness, design, readability,
tests, and security. Output is structured, actionable feedback — not a rewrite.

## When to Use

- User asks for a code review or PR review
- User wants feedback on a snippet before merging
- User wants to learn what to look for

## When NOT to Use

- The code is suspected to have a security flaw (route to `secure-coding` for depth)
- The user wants a full rewrite (use `coding`)

## Capabilities

- Catch correctness bugs
- Suggest clearer names, smaller functions, better structure
- Spot missing tests
- Flag suspicious patterns (input validation, error handling, race conditions)
- Note style / lint issues if egregious

## Inputs

- The diff or full code
- Context (what does the code do, what are the constraints)
- Risk tolerance (production? prototype?)

## Workflow

1. **Read for purpose.** What is this code trying to do? Is it the right thing?
2. **Read for correctness.** Does it actually do that? Edge cases? Errors?
3. **Read for design.** Is the structure right? Boundaries clean?
4. **Read for clarity.** Will the next reader understand this in 6 months?
5. **Read for tests.** Are the important cases covered?
6. **Read for security.** If relevant: input validation, secrets, auth, injection.
7. **Prioritize.** Blocking → suggestion → nit. Lead with blocking issues.

## Output format

Organize feedback as:

- **Blocking** (must fix): correctness, security, broken tests
- **Strong suggestions** (should fix): design, clarity, performance
- **Nits** (optional): style, naming micro-tweaks

For each item: one paragraph, one suggested change, no rewrites of working code.

## Safety

- Be kind. Critique code, not the author.
- Don't demand rewrites when refactoring will do.
- Don't pile on — pick the few things that matter.

## Source

Custom skill, written for this library.

## Notes

Pairs with:
- `secure-coding` (security-specific depth)
- `refactoring` (after review)
- `testing` (when tests are missing)

## Tools

- No mandatory tool unless declared in frontmatter.
- Use only project-approved tools and documented optional dependencies.

## Examples

Requests that should activate this skill include: "review this code"; "review my PR"; "code review".
