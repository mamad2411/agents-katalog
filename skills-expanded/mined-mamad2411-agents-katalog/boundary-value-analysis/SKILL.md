---
name: boundary-value-analysis
description: >-
  Design and implement boundary value tests for numeric ranges, dates, string
  lengths, collection sizes, and pagination limits. Use when: "boundary value,"
  "境界値," "edge cases for input validation," "off-by-one," or whenever the user
  is testing any input with a min/max, length limit, or range — even if they
  don't say "boundary." Produces both a test-case design table (design mode) and
  executable parameterized tests (implementation mode). Not for: choosing which
  inputs to partition first — use equivalence-partitioning. Related:
  equivalence-partitioning, decision-table-testing.
license: MIT
metadata:
  version: "1.0"
  istqb: "CTFL v4.0 §4.2.2"
  iso25010: [functional-suitability]
  mode: [design, implementation]
---

# Boundary Value Analysis

Systematically test at boundaries, where off-by-one errors, overflow, and empty-input
defects concentrate.

## Objective

Produce a complete boundary test set for each constrained input: a traceable design
table (design mode) and/or parameterized test code (implementation mode). The failure
mode this prevents: suites that test 0 and "a typical value" but never max, max+1, or
empty — exactly where production defects hide.

## Context Discovery

Infer from the conversation and codebase before asking:

- What are the inputs and their constraints? (read validation code, schemas, DB column
  types, API specs — constraints in code beat constraints in memory)
- 2-value or 3-value BVA? Default to 3-value (boundary, just inside, just outside) for
  risk-critical inputs; 2-value elsewhere.
- Implementation mode only: which test framework and language? (detect from the repo:
  pytest/Jest/Vitest/JUnit/Playwright)

## Instructions

1. **Enumerate constrained inputs**: For each input, document type, valid range, and
   the *source* of the constraint (requirement, schema, code). If code and requirement
   disagree, flag it — that is a defect finding, not a test-design detail.

2. **Derive boundary values**: For each constraint produce: min−1, min, min+1, max−1,
   max, max+1. For strings/collections: empty, length 1, max length, max+1. For dates:
   epoch edges, month/year rollovers, leap day (Feb 29), timezone boundaries.

3. **Cover invalid boundaries deliberately**: Every invalid value needs an expected
   *behavior* (specific error code/message), not just "should fail." A test asserting
   only "throws" passes even when the wrong error is thrown.

4. **Combine boundaries across parameters** (risk-based): For multi-parameter inputs,
   test corner combinations (all-min, all-max, min×max) only for parameters that
   interact. Full combinatorial coverage explodes; use pairwise if more than 3
   interacting parameters.

5. **Trace back**: Tag each test case with the requirement/constraint ID so coverage
   is auditable.

## Output Format

### design mode

| TC-ID | Input | Value | Class | Expected Result | Trace |
|---|---|---|---|---|---|
| BVA-001 | age | 17 | invalid (min−1) | 400 AGE_OUT_OF_RANGE | REQ-12 |
| BVA-002 | age | 18 | valid (min) | accepted | REQ-12 |

### implementation mode

Use the repo's framework and its parameterized-test idiom. Canonical shape (pytest):

```python
@pytest.mark.parametrize("age,expected_status,expected_code", [
    (17, 400, "AGE_OUT_OF_RANGE"),  # min-1
    (18, 201, None),                # min
    (19, 201, None),                # min+1
    (64, 201, None),                # max-1
    (65, 201, None),                # max
    (66, 400, "AGE_OUT_OF_RANGE"),  # max+1
])
def test_age_boundaries(client, age, expected_status, expected_code):
    ...
```

One parameterized test per input; comment each row with its boundary class.

## Anti-Patterns

- **Happy-path bias** — LLMs generate valid-side boundaries and skip invalid ones.
  **Guard:** every constraint must yield at least two invalid-side cases (below min,
  above max) before the set is considered complete.
- **Asserting "error" without specificity** — passes even when the wrong error fires.
  **Guard:** assert error code/message, not just status or exception type.
- **Boundaries from memory, not from code** — testing limits the model *assumes*
  (e.g. 255 chars) rather than what the schema enforces. **Guard:** cite the file/line
  or spec where each constraint is defined; if it can't be cited, ask.
- **Combinatorial explosion** — generating every corner combination for 5+ params.
  **Guard:** combinations only for interacting parameters; pairwise beyond 3.

## Related Skills

- `equivalence-partitioning` — run first to identify the classes whose edges BVA tests.
- `decision-table-testing` — when behavior depends on combinations of conditions, not ranges.

## References

- ISTQB CTFL v4.0 Syllabus §4.2.2 (Boundary Value Analysis)
- ISO/IEC 25010:2023 — Functional Suitability (functional correctness)
