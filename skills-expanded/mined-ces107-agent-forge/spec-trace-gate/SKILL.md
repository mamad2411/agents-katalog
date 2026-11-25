---
name: spec-trace-gate
description: Machine-checks that every requirement in a spec is covered by a task and every task is verified by a test that actually exists (spec to task to test traceability), failing on any dropped requirement, phantom reference or missing test. Use when writing acceptance criteria, breaking a spec into tasks, checking whether an implementation really closes over its spec, or adding a requirements-coverage gate to CI.
argument-hint: "[spec path] [tasks path] [tests dir]"
---

# Spec ↔ task ↔ test traceability gate

Spec-driven workflows (GitHub Spec Kit, AWS Kiro, BMAD) give you *Specify → Plan → Tasks → Implement*,
but nothing proves the finished code closed over the spec. Drift is caught by a human, if at all.
This skill turns that proof into a pass/fail command.

## The contract

Three inputs:

1. **Spec**: acceptance criteria, each tagged with a stable id `AC-N` and written in EARS
   (`references/ears.md`).
2. **Tasks**: one block per task:

   ```
   ## T-3 — Race-safe idempotency under concurrent duplicates
   Serialise the check-then-insert so N concurrent duplicates yield exactly one result.
   covers: AC-3
   verified_by: test_concurrent_duplicate_key_single_posting
   ```

3. **Tests directory** of the project (Python, TS/JS, Go, Java/Kotlin, Ruby and C# file
   conventions are recognised by default; override with `--test-glob`).

The gate fails on any of:

| Violation | Meaning |
|---|---|
| UNCOVERED acceptance criterion | An `AC-N` in the spec that no task `covers:`. A requirement was dropped. |
| ORPHAN task reference | A task `covers:` an `AC-N` that is not in the spec. Phantom work, or a typo. |
| UNVERIFIED task | A `verified_by:` name that does not appear, as a whole identifier, in any test file. |

## Procedure

1. **Find or write the spec.** If the user has none, draft one from their request with
   `assets/spec-template.md` and show it to them before going on. Each AC states one observable
   behaviour, uses an EARS pattern, and keeps its id forever (never renumber; retire ids instead).
2. **Write the tasks file** with `assets/tasks-template.md`. Small, single-responsibility tasks,
   ordered so earlier ones unblock later ones. If a test does not exist yet, name the exact test
   that must be written and say so in the task body.
3. **Structure check, right after planning** (no tests needed yet):

   ```bash
   python <this-skill-dir>/scripts/trace_gate.py --spec <spec.md> --tasks <tasks.md> \
       --tests-dir <tests/> --structure-only
   ```

4. **Full check, after implementation**: the same command without `--structure-only`.
5. **On FAIL, fix the cause, never the report:**
   - uncovered AC → add or extend a task; only drop the AC if the user explicitly agrees;
   - orphan reference → correct the id, or add the missing AC to the spec with the user;
   - unverified task → write the named test, or point `verified_by:` at the real test name.
     Never shorten a selector to a generic fragment just to make it match.
6. **Report** the verdict line exactly as printed (`TRACE: PASS` / `TRACE: FAIL`) together with
   the violation lines. Do not paraphrase a gate result.
7. **CI (optional, ask the user first):** `assets/ci-github-actions.yml` runs the full gate on every
   push and pull request.

## Notes

- `scripts/trace_gate.py` needs Python 3.10+ and the standard library only. It reads the three
  inputs, prints a report and exits 0 or 1. It writes nothing and makes no network calls.
- Matching is by whole identifier: `test_replay` does not match `test_replay_across_restart`.
- A spec with no `AC-N` ids passes trivially. If you see `acceptance criteria: 0`, the spec is not
  in the expected shape; fix that first.
- For non-standard test layouts pass one or more `--test-glob` patterns (e.g. `--test-glob '*.rs'`).
