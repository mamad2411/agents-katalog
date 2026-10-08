---
name: unslop-coder
description: Apply unslop-reviewer findings as targeted in-scope code edits in pass order; do not run discovery/scanning in this skill.
agents:
  - coder
---

# Unslop Coder

**Purpose**: apply a pre-computed findings list from an `unslop-reviewer` sidekick review.

This skill is implementation-only: it **edits files** to apply listed findings.
It is not a scanning skill.

## What You'll Be Fixing

Apply only the categories and priorities provided by `unslop-reviewer`; treat that
review output as the canonical slop taxonomy for each run.

## Input Format

The calling prompt provides a findings list in the format produced by `unslop-reviewer`:

```
1. F-1 | src/auth.ts | pass:1 | dead-code | S | Unused `lodash` import at line 3 | Delete line 3
2. F-2 | src/auth.ts | pass:3 | naming | S | Variable named `data` at line 47 | Rename to `userRecord`
…
```

Each finding must use: `F-id | relative-file-path | pass:1-4 | category | size | description | fix`.
Valid categories are `dead-code`, `duplication`, `abstraction`, `boundary`, `naming`,
`error-handling`, and `test`; sizes are `S`, `M`, or `L`.

Apply **only** listed findings. Before editing, confirm the referenced code still exists and the
proposed fix still matches it. Do not scan for additional slop or apply fixes not present in the
list. Skip stale, conflicting, or ambiguous findings and report why.

---

## Application Mechanics

- Apply findings strictly in **pass order**: pass 1 → pass 2 → pass 3 → pass 4.
- Within each pass, process findings by **file path**. For conflicting findings in the same file,
  apply only the safer, independently valid finding; report the other as skipped.
- Never touch files outside caller-provided scope.
- Apply only the requested fix; do not add opportunistic refactors.

## Non-Negotiable Constraints

- **Preserve observable behavior**. Slop cleanup is a scalpel, not a rewrite.
- Prefer deletion over addition, but never delete speculatively.
- **Test-before-delete**: if deletion may affect side effects, lock behavior with a test
  first, then delete. When test writing is not active, skip and report that finding instead.
- This skill **always edits files**; it is not for read-only review.

---

## Test-Writing Behavior

Test writing is **opt-in**. Only write new tests when the calling prompt explicitly
states that **test-writing override is active**.

When active: for each pass-4 finding, write targeted tests that lock the described
behavior. Every test must assert a meaningful outcome (not only "no error thrown").
Co-locate tests with existing project test files.

When not active: skip pass-4 implementation. Report those findings as deferred gaps.

---

## Reduction Override

When the caller explicitly states that reduction mode is active, optimize for **net code-size reduction** within the listed findings.

- Favor the smallest safe implementation that removes lines or symbols.
- Allowed examples: inline pass-through wrappers, consolidate exact duplicates, remove useless comments, and delete redundant locals/imports/guards.
- Skip rename-only or stylistic cleanup that does not materially shrink the code.
- Never add a broader abstraction if it increases code size.

---

## Orchestrator Validation Contract

When called from `/unslop-loop` Orchestrator mode with a validation rule, this skill must:

1. Detect test runner using the caller-provided order and set `test_cmd`.
2. If a runner is available, execute `test_cmd` after edits.
3. Report `tests: pass` or `tests: fail`.
4. When `tests: fail`, include failing test names in output.

If no runner is available, report `test_cmd: none`.

---

## Output (≤ 300 tokens)

- **Files touched** — list modified files
- **Applied findings** — one line per finding: `F-id: <what was done>`
- **Skipped findings** — each skipped finding with reason (out of scope, ambiguous fix,
  unsafe change, etc.)
- **Pass-4 gaps** — when override is not active, list deferred pass-4 findings
- **Risks** — remaining risk areas that could not be safely cleaned in-scope
- **Validation status** — `test_cmd: <command|none>` and `tests: pass|fail`; include failing test names when status is fail
