---
name: supercoverage
description: Use when drafting or revising a PRD and its acceptance criteria, to advise on test coverage, distinguish requirements from examples, and resolve verification ambiguities before implementation.
license: MIT
---

# Supercoverage

Advise the PRD author on what should be verified. The author approves the acceptance
checklist; implementation review verifies delivery against that approved checklist.
This skill produces advice and draft text, not product code or an implementation gate.

## Draft the coverage agreement

Read the proposed requirements and the author's decisions. Produce:

1. A draft acceptance checklist with stable IDs, source clauses, required cases or general
   behavior, observable expected results, verification method, and owning C/J check IDs.
2. A separate list of optional test suggestions and unresolved questions. Mark suggestions
   as unapproved. Resolve ambiguous outcomes with the author before declaring readiness.

Use this table under `## Acceptance checklist` in `evaluation.md` when called by
`superagent:superprd`. A standalone invocation returns the draft to the author; it does
not write or approve a project folder.

| Id | Source | Required case or rule | Expected result | Verification and check ids |
|---|---|---|---|---|
| AC1 | prd.md SC1 | Invalid input | Destination bytes remain unchanged | Assert byte equality before/after rejected operation; J1 inspects assertion, C1 executes suite |

The row is an example of form, not a requirement for every project. Use existing check
IDs where available; label proposed new checks as drafts until their commands/criteria
are resolved. Never claim a command was run or a test exists from this planning artifact.

## Coverage decisions

- Expand combinations explicitly required by the source. “Both formats, each with empty,
  single-record and malformed input” requires six cases, which may share a parameterized test.
- Preserve broad rules separately from example fixtures. “Unicode names, e.g. accented Latin”
  retains general Unicode behavior; it does not require every script or only Latin.
- Specify what an assertion must distinguish, not just a test name or input. For preserving
  a destination, checking existence alone does not establish unchanged contents.
- Suggest boundaries and failure cases with their rationale. Extra partitions, new supported
  formats, and exhaustive combinations become mandatory only through author approval.
- Choose a suitable verification method: executable assertion, command result, or concrete
  evidence inspection. Documentation obligations need not become artificial product tests.

## Approval and later changes

In superprd, present the checklist and separate suggestions at its existing confirmation
step. Record the user's approval of that concrete revision; unresolved required outcomes
prevent READY. A general instruction to automate implementation does not settle an
unspecified product behavior. Explicit prior approval of the same revision remains valid.

The approved checklist is a verification agreement, not proof of exhaustive coverage or
permission to weaken the PRD. If it conflicts with a source requirement, resolve the conflict
with the author. Later scope changes return to PRD revision, preserve prior versions, and
receive approval before becoming acceptance conditions. Reviewers may report newly found
risks, but do not silently turn suggestions into release requirements.
