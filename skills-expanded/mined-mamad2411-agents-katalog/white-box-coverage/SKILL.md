---
name: white-box-coverage
description: >-
  Design and measure statement and branch coverage per ISTQB CTFL v4.0 §4.3 — white-box
  testing that exercises the code's structure. Use when: "white-box," "statement
  coverage," "branch coverage," "code coverage," "ホワイトボックス," "カバレッジ,"
  "which lines/branches aren't tested," "coverage target," or reasoning about structural
  test thoroughness. Produces a coverage plan and gap analysis (design mode) and tests
  that hit uncovered branches + a CI coverage gate (implementation mode). Not for:
  judging whether tests ASSERT meaningfully — use maintainability-review (mutation
  testing); or spec-based case design — use equivalence-partitioning. Related:
  maintainability-review, equivalence-partitioning.
license: MIT
metadata:
  version: "1.0"
  istqb: "CTFL v4.0 §4.3 (§4.3.1–4.3.3)"
  iso25010: [functional-suitability]
  mode: [design, implementation]
---

# White-box Coverage

Exercise the code's structure — statements and branches — so untested paths are
visible and measurable, not assumed away by "we have tests."

## Objective

Statement and branch coverage measured against risk-based targets, with the untested
paths identified and the technique's limits understood. Per CTFL v4.0 §4.3.2, **branch
coverage subsumes statement coverage** — 100% branch implies 100% statement, not vice
versa — so branch is the stronger target. The failure mode this prevents: a suite that
runs the happy path (high statement coverage) but never takes the error branch where
the bug lives.

## Organization-specific inputs (fill these in)

- **Coverage targets by module**: which modules require what branch/statement % (risk-
  and criticality-driven; 100% everywhere is rarely the right call).
- **Coverage tool** and how it's wired (coverage.py, Istanbul/nyc, JaCoCo, etc.).
- **Gate policy**: does coverage below target fail the build, or warn?
- **Exclusions**: generated code, vendored code — documented, not silent.

## Context Discovery

- Is coverage already measured? What's the current statement/branch coverage, and where
  are the gaps? (read the coverage report before writing tests)
- Which modules are risk-critical enough to warrant branch coverage targets?
- Language/framework and coverage tool present in the repo.

## Instructions

1. **Statement coverage** (§4.3.1): ensure every executable statement is exercised at
   least once. Coverage = statements exercised ÷ total executable statements, as a %.

2. **Branch coverage** (§4.3.2): exercise every branch — both outcomes of each decision
   (true/false). Coverage = branches exercised ÷ total branches, as a %. Prefer branch
   as the target since it subsumes statement.

3. **Target by risk** (org input): set the % per module by criticality; don't chase
   100% everywhere. Read the coverage report to find the specific uncovered branches and
   write tests that take them (the error/exception/guard branches usually).

4. **Know the limits** (§4.3.3): white-box uses the actual implementation, so it finds
   defects even when the spec is vague or outdated — BUT it cannot find **defects of
   omission** (a requirement never implemented has no code to cover). Always pair with
   spec-based (black-box) techniques.

5. **Measure in CI and gate**: fail (or warn) when coverage drops below the target;
   report per-module, not one aggregate number.

> Scope: Foundation-level white-box is **statement + branch only**. Path, condition/
> decision, and MC-DC coverage are out of CTFL v4.0 scope (used in some safety/mission-
> critical contexts) — call them out as a separate effort if a regulated domain needs them.

## Output Format

### design mode

```
# Coverage Plan: {module}
## Targets (statement / branch %, per module, with rationale)
## Gap analysis (uncovered branches → the case that would exercise each)
   | Location | Uncovered branch | Test to add |
## Limits noted (defects of omission — which black-box tests cover the spec side)
```

### implementation mode

Coverage config + a test that takes a previously-uncovered branch; gate in CI:

```bash
# e.g. pytest + coverage.py — fail under the branch target
pytest --cov=src --cov-branch --cov-fail-under=85
```

```python
def test_hits_error_branch():           # the branch statement coverage missed
    with pytest.raises(ValueError):
        parse("")                        # exercises the empty-input guard branch
```

## Anti-Patterns

- **Coverage % as a quality metric** — 100% branch coverage with weak/absent assertions
  proves the code *ran*, not that it's *correct*. **Guard:** pair coverage with mutation
  testing (see maintainability-review); coverage is necessary, not sufficient.
- **Statement-only target** — misses untaken branches (the error paths). **Guard:**
  target branch coverage, which subsumes statement.
- **Chasing 100% everywhere** — expensive tests on trivial/low-risk code. **Guard:**
  risk-based per-module targets.
- **Ignoring defects of omission** — trusting white-box to find missing features.
  **Guard:** white-box can't cover code that doesn't exist; complement with black-box.
- **Silent exclusions** — quietly excluding files to hit the number. **Guard:** document
  every exclusion.

## Related Skills

- `maintainability-review` — mutation testing judges whether the covering tests actually
  assert; coverage tells you what ran, mutation tells you what would be caught.
- `equivalence-partitioning`, `boundary-value-analysis` — black-box counterparts that
  cover the specification side (defects of omission).

## References

- ISTQB CTFL v4.0 Syllabus §4.3 (White-Box Test Techniques): §4.3.1 statement, §4.3.2
  branch (branch subsumes statement), §4.3.3 the value of white-box testing
- ISO/IEC 25010:2023 — Functional Suitability (functional correctness)
