---
name: test-shield
description: Pre-sweep coverage gate for behaviour-preserving work (/optimize, /audit refactor + perf verbs). "Refactor, tests stay green" is only proof of preservation if a test actually exercises the touched branch — on an UNCOVERED branch a structural fix can silently change behaviour and still show green. Before such a fix, this skill detects the touched-but-uncovered branches in scope and pins current behaviour with a characterization test (dispatching /add-test) BEFORE the fix lands, or halts the row. Reuses testing/skills/coverage-gap/SKILL.md for detection.
kind: skill
pack: code-quality
allowed-tools: [Read, Write, Edit, Grep, Glob, Bash]
---

# Skill: test-shield

## Purpose

A behaviour-preserving fix (refactor, dedup, dead-code, parallelize, cache) is only *safe* if the green suite actually covers the code it touches. On an **uncovered branch**, "tests still pass" proves nothing — the fix can flip behaviour and no test notices. `test-shield` makes the guarantee real: it **pins current behaviour with a test BEFORE the fix**, so any post-fix divergence turns the suite red.

This is the pre-sweep counterpart to `smoke-verify` (which runs after). Dead-code removal is already gated by `dead-code-scan`'s removal proof (pin, delete, boot); this closes the same gap for the refactoring + perf verbs.

## When to use

- Dispatched in **Phase 0** of `/optimize` and `/audit` (before any structural/perf fix), per in-scope file set.
- On demand: `pin coverage before refactoring <area>`.
- N/A for pure additive work (new feature, new file) — there's no existing behaviour to preserve.
- **Never for a behaviour-changing class.** A swallowed error (`silent-catch`; `error-handling-scan` § 1–§ 7), a failure returned as success, a correctness smell (`correctness-smell-scan`), a boundary cast with no validator (`type-safety-scan` § 1), a dead check that hid an intended refusal (`dead-code-scan` § 3), a copy that diverged (`duplication-scan` § 1–§ 2), and every security fix change what the caller observes on purpose. A characterization test pins today's behaviour *bugs included*, so pinning one of these pins the defect, and the fix then turns the pin red. Those rows skip this skill with `shield: skipped (behaviour-changing: <class>)` and go to `/quality-fix` (or the owning fix command), whose proof is a failing-first test written against the intended behaviour.

## Procedure (stack-conditional via PROJECT_KIND + project test runner)

1. **Determine the touched set**: the files/functions the planned fix will modify (from the optimize/audit finding's scope). First drop every row whose class is behaviour-changing (§ When to use): it is not shielded, it is proved failing-first elsewhere.
2. **Measure coverage** of that set using the project's coverage tool (reuse `testing/skills/coverage-gap/SKILL.md`; runner from `ai/stack.md` § Scripts — `pytest --cov` / `vitest --coverage` / `jest --coverage` / `go test -cover` / etc.).
3. **For each touched branch with no covering test**:
   - Dispatch `/add-test` to write a **characterization test** that asserts the CURRENT (pre-fix) observable behaviour — inputs → outputs/side-effects as they are TODAY, bugs included (this is a pin, not a correctness judgement).
   - Re-run; confirm the new test is green against current code.
   - If the branch genuinely cannot be characterized (true side-effect-only, external dependency, non-deterministic) → **HALT** that finding with `status: blocked` + reason; do NOT apply the structural fix to an un-pinnable branch.
4. **Gate**: only after every touched branch is covered (pre-existing or freshly pinned) may the sweep apply its fix. Coverage measured here is the floor `/optimize` step 7's "coverage must not drop" compares against.

### If the testing pack is not installed

Steps 2 and 3 name `coverage-gap` and `/add-test`, which ship in the **testing** pack. A project without it must not silently skip this gate — a skipped shield reads as "covered" when nothing was checked, which is the failure this skill exists to prevent. Degrade in this order:

1. **Coverage still measurable without the skill.** The skill is a reading procedure, not the measurement: run the project's own coverage flag (`vitest --coverage` / `pytest --cov` / `go test -cover` / `cargo tarpaulin`) and intersect its `0`-hit lines with the touched set by hand. This loses none of the gate's strength.
2. **No coverage tooling at all.** Fall back to the weaker but real check: for each touched function, grep the test tree for its symbol. No reference at all is an uncovered branch with certainty; a reference is only *evidence* of coverage, not proof. Record the finding as `shielded [grep-only]` so the reader knows which rows rest on the weaker check.
3. **Writing the characterization test without `/add-test`.** The test is an ordinary test — capture today's observable output for a representative input (bugs included) and assert on it. What `/add-test` adds is sibling-shape mirroring and the mutation gate, not the ability to write the file.
4. **Neither available.** The finding is `blocked [unshieldable]` with the reason. Never `applied`.

**Never silently skip the axis.** Record the substitution (`inline:coverage-gap`, `manual-characterization`) in the sweep's report.
## Verify (the check on the check)

- The added characterization tests are GREEN against current code (a red pin = the pin is wrong; fix it before proceeding).
- The touched branches are demonstrably covered now (re-measure, don't assume).
- Any un-pinnable branch left a `blocked` finding with an explicit reason — never a silent skip.

## Anti-patterns this prevents

- **The Coverage Mirage** — "behaviour preserved, tests green" on a branch no test exercises.
- **The Silent Coverage Drop** — a fix removes the only path exercising a downstream branch; coverage drops unnoticed in a large suite (test-shield's pre-measure is the baseline that catches it).
- **The Absent-Shield Mirage** — the testing pack is not installed, the skill no-ops, and the sweep reports "behaviour preserved" having verified nothing. A missing dependency must degrade (above), never disappear.

## See also

- `testing/skills/coverage-gap/SKILL.md` — the coverage detection this reuses.
- `code-quality/skills/dead-code-scan/SKILL.md` — the analogous gate for dead-code removal: its removal proof pins with this skill, then boots with `smoke-verify`.
- `code-quality/skills/smoke-verify/SKILL.md` — the post-sweep counterpart (boot-check).
- `/add-test` — the command that writes the characterization tests.
