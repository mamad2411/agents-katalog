---
type: Idea
id: idea-005-a-documentation-review-skill
title: A documentation review skill
description: A skill that reviews the documentation a reader outside the repository meets — README, CONTRIBUTING, changelog, help text, API docs — against the code and against the reader it serves.
status: draft
---

# Idea: a documentation review skill

A `/documentation-review` skill that reads the documentation someone outside
the repository meets — `README.md`, `CONTRIBUTING.md`, `CHANGELOG.md`, the
binary's own help, the public API's doc comments — and reports where it has
stopped matching the code or stopped serving its reader. It reports; it does
not rewrite.

## Motivation

`/maintain` audits `knowledge/` and stops at that directory's edge.
`/code-review` reads a diff. Nothing reviews the documentation a user actually
reads, which is where drift is hardest to see from inside: a quick start that
broke two releases ago still parses, still renders, and still looks right to
everyone who already knows the answer.

`templates/processes/documentation-upkeep.md` states the standard already —
sweep for what a change invalidated, verify an example by running it, write
for the reader the document serves. No skill runs it, so it applies when
someone remembers it.

## Sketch

Scope: the repository's outward documentation. `knowledge/` stays with
`/maintain`, and the boundary is stated in both skills rather than assumed.

Checks, in the order their cost rises:

- Every link resolves and every referenced path exists.
- Every documented flag, option and default agrees with the contracts and the
  code.
- The changelog's Unreleased section covers the user-visible changes merged
  since the last release.
- Every fenced command runs, and produces what the document claims it
  produces.
- Each document reads for the audience it names, judged against the
  professionalism standard.

Output is a review report, findings grouped by document, each carrying the
evidence that produced it and separating what the skill verified from what it
judged. It runs at the user's request and as a step before a release.

## Trade-offs

- Verifying an example means running it, which needs a build and a place to
  run it. The cheap checks and the executed ones may have to be separate
  modes.
- It overlaps `/maintain`'s accuracy pass and `/code-review`. Three skills
  reading the same code for different reasons is a real cost, and the split
  has to be written down before a third one exists.
- A prose-quality finding is a judgement. Mixed into a report of verified
  facts it devalues the facts, so the report has to keep them apart.
- Reporting without fixing leaves the work where it started. The upkeep
  process says to fix a line or two in passing, which a review skill would
  either adopt or contradict.

## Open questions

- A skill of its own, or a step inside `/accept` and the release procedure?
- Does it need a `documentation-review` schema for its report, or does
  `code-review`'s serve?
- How much does the CLI contract's binding test already cover? Help text bound
  to a contract needs no review for accuracy, only for register.
- Fix in passing, or report only?

## Next step

Read `templates/processes/documentation-upkeep.md` beside `/maintain` and mark
which of its steps a skill can check mechanically. What is left over decides
whether this is a skill or a checklist inside `/accept`.
