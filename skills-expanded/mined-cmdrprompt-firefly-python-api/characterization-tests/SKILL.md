---
name: characterization-tests
description: "Use when adding tests to previously untested code, before any refactoring or bug fixing. Defines how to document existing behavior as-is with pytest and Hypothesis, and what must not happen during characterization. Keywords: characterization test, golden master, legacy code, untested code, document behavior."
---

# Characterization tests

Characterization tests document what code currently does - not what it
should do. They are the mandatory first step before refactoring or fixing
previously untested behavior.

## Procedure

1. Read the target function or module in full. Trace all code paths:
   normal, edge, and error conditions.
2. Write tests that pin the current behavior as-is, even where it looks
   wrong. Behavior that looks incorrect or inconsistent with the
   requirements document is flagged in the report, never silently fixed.
3. Run the suite and verify the new tests pass against the unchanged code.

## Conventions

- Use `pytest`. Use `@given` / `@settings` from Hypothesis for all parsing,
  date handling, and data transformation functions - no exceptions.
- Place tests in `tests/unit/test_<module>.py`. Name functions
  `test_<behavior>` after the behavior they pin, not the implementation.
- Mock only true external boundaries (network, API calls, subprocess,
  filesystem outside `tmp_path`), not internal collaborators.
- Coverage must not drop; verify with `make test`.

## What must NOT happen during characterization

- Never fix a bug, however obvious - a fix requires a confirmed requirement
  and its own task via the normal spec-driven flow.
- Never assert the behavior you think is correct; assert the behavior the
  code actually exhibits.
- Never skip Hypothesis for parsing or data transformation functions.

## Output

Report, in plain language: what the code does, which behaviors were pinned
by which tests, and every behavior that looks incorrect or surprising (with
the relevant requirement, if one exists) as candidates for bug-fix tasks.
