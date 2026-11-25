---
name: testing
description: >
  Methodology and formats for test-case design and execution
  across the entire SSDLC. Code tests, logic, processes, specs,
  constraints. Domain-specific eval patterns: testing/eval_patterns/.
  Triggers when test cases must be designed or executed (build prepare test-design, fix verify); NOT for ad-hoc manual checks without a test plan.
status: active
relevant_for: ["tester"]
invocation:
  primary: workflow-step
  secondary: [user-facing, sub-skill]
disable-model-invocation: false
modes: [design, execution]
uses: [convergence_loop]
---

Read and follow `framework/work-principle.md` before taking up work.
Resolve this reference against the framework root; retain the consumer CWD.
Without Buddy (plugin): if this session holds no Buddy boot entry, run `python3 <root>/scripts/forge_setup.py offer-check` once, as its own call (`<root>`: two levels above this skill's folder); if it prints a line, pass that offer to the user in one sentence, then continue with this skill.


# Skill: testing

Agent: `agents/tester.md`. Detail mechanics (format details, skeleton
templates, eval methodology, retest gate) and the cross-project
infrastructure discipline (§Infrastructure): `REFERENCE.md`.

## 6-level test pyramid

| Level | What | Trigger |
|-------|------|---------|
| L0 Structural | Dead refs, schema, invariants | Every commit |
| L1 Logic / Semantic | Process gaps, spec consistency, DRY, simulation | Spec / process change |
| L2 Unit | Function / module level | Code change |
| L3 Integration | Agent handoffs, API contracts, event schemas | Interface change |
| L4 E2E | Full workflows (boot, delegation, save) | Workflow change, periodic |
| L5 Adversarial | Stale context, drift, chaos, properties | Milestone, periodic |

**Regression rule:** L4 / L5 check STRUCTURE / TYPE. L3 checks
CONTRACTS. L2 checks BEHAVIOUR / VALUES. Lower levels must never
break when higher ones are added — on a break: abstract the
assertion, do not delete the test.

## Test-case design (core task)

Test cases are designed BEFORE implementation. No delegation
without a test plan.

### Test design from the change

A test plan covers what the change changes, and nothing else.

- Each changed behaviour that an AC names gets one test that fails
  without the change (§Meaningful pre-fix witness).
- A negative case is added only where the AC or change spec names a refusal.
- Unchanged behaviour gets no new test and no speculative edge cases;
  a real gap surfaces later as a defect with its own test.
- For text an outside agent runs on a user's machine (install, setup,
  removal) an AC names the live run in `skills/_protocols/evidence-author-claims.md`
  §8.5. Other instruction text is not a test subject: an AC met by it alone
  names its consistency or generator check in the coverage matrix instead
  of a TC (`run-strategy.md` §Test selection, light path).
- The adversary test plan and the skeleton writer run only when the
  change touches a safety floor (`skills/adversary_test_plan/SKILL.md`
  §When to call).

**How many tests.** The count is fixed before code, as the coverage
matrix's rows: one row per behaviour the change promises (each AC, and
each edge row the change spec names: an input class, a limit, a
refusal), plus an L1+ spec's §Test-Strategy rows and the
§Mechanism-Lifecycle cells its generator does not reach
(`test-design.md`), deduplicated by bug class; on an L1+ spec an edge
row maps to a catalog bug class. A limit the change spec states gets the edge row in
which that limit alone decides. A row added later enters only through
the adversary test plan on a safety floor or a review finding about
behaviour a consumer relies on that no existing test reaches (one row
per class), and amends the matrix. A row is covered
only when its test ran and passed in this run (§Meaningful pre-fix
witness). A bug fix gets one test that reproduces the bug (a
class: §Meaningful pre-fix witness) and fails before the fix (`workflows/runbooks/fix/WORKFLOW.md`, test-plan step);
a refactoring adds no tests and keeps
the existing ones green. Source of the edge-row matrix:
BMAD-METHOD (MIT License, © 2025 BMad Code, LLC); Forge's register of adopted methods.

Each new test, whatever its source, names its consumer in its docstring or plan row: who
relies on the behaviour it guards. A combination grid justifies each
axis: an axis stays only where its values change an assertion or the
code path under test, and combinations that assert nothing new are not
written. A plan never obliges anyone to keep every cell of a grid ("do
not omit cells"); dropping a cell that changes nothing is correct. A
review finding becomes a test when it names behaviour a consumer relies
on and no test reaches its path; otherwise that test is strengthened
(`lean-suite.md`). A test the normal suite cannot
execute (one that waits for external evidence, a native session or a
manual run) is not written as a permanent test. Run that acceptance once
and record its verdict, or write its mechanical part as an ordinary
test.

### Lean, parallel suites

Each test covers one distinct behaviour or risk, every test runs in
parallel with every other, and after a change only the tests it touches
run. When designing a test plan, ordering tests in a brief or fix brief,
writing a test, checking the tests a change adds, retiring a mechanism
that has tests, or setting up a test runner: read and follow
`skills/testing/lean-suite.md` (the rules each test is checked against
and who removes one, parallel safety, change-scoped runs, the full gate).

### Meaningful pre-fix witness

For an intended behavior change, execute a behavior assertion before implementation
that fails on the relevant unfixed or unimplemented behavior and identifies the
intended change. Retain the command, observed failure and reason. Missing fixtures,
skipped placeholders, unrelated import errors or `assert False` do not establish
that witness. Unavailable prerequisites remain unverified, not RED.

A RED whose only failure is that the interface under test does not exist yet (an
import, attribute or name error, or a missing key, for the module, function or field
the change adds) shows that the behaviour is missing; it does not test the
assertion's expected value or the fixture. The skeleton return lists each such TC as
`oracle unverified`, with the missing interface, apart from the REDs that reached an
assertion.

Existing regression tests, positive controls and already-satisfied behavior may
pass; retain and explain them rather than making them fail. Investigate an
unexpected pass for supposedly missing behavior: the behavior may already exist or
the assertion may miss it. After implementation, execute the witness and required
regression, negative and control cases; all applicable required cases must pass.
A result claim covers only what executed: acceptance reported as `unexecuted`, or
skipped for missing execution evidence, is unverified and named as such, never
counted as passing or "green".
Findings of one class share one test from the first fix pass on
(`lean-suite.md`); a repeated class (`same_class: yes`) takes its class
witness, a generator red on each known finding before its fix
(`skills/convergence_loop/simplify-before-patch.md` §Class witness).
Pure preservation/refactor work demonstrates its unchanged contract without
fabricating a missing-behavior failure. This is a testing rule for behavior changes,
not a test ceremony for ordinary prose or every activity.

### Derivation, execution-faithfulness and oracle discipline

In design mode, before deriving test cases from the spec: read and follow `skills/testing/test-design.md`
(derivation from specs, from a §Test-Strategy catalog and from a §Mechanism-Lifecycle matrix; bug-class dedup;
execution-faithfulness for producer seams, pooled resources and golden corpora; oracle discipline; L1 logic /
semantic checks and the iteration protocol).

## Coverage matrix (MUST output)

An AC without a TC, or without the named check that verifies
instruction text, is a GAP. An empty row is an invalid state.

| Spec element | TC IDs | bug_class | Level | AC quality | Eval status |
|---|---|---|---|---|---|

**bug_class** (required when spec has §Test-Strategy): noun phrase
naming the defect class this TC guards against. Must be present in
the spec catalog (else: spec amendment first, see `test-design.md` "Derivation from
§Test-Strategy catalog"). Duplicate bug_class across rows = drop one.

**AC quality** (required): **clear** / **vague** (annotate what's
missing) / **contradictory** (which contradiction). Vague /
contradictory → spec review BEFORE execution. No opt-out.

Persistence: section in `docs/tasks/<NNN>.md`. Update on a spec
change, do not recreate.

## Contract

**INPUT:** spec with ACs (or process definition for L1), `spec_ref`
for spec-freshness check. Optional: existing plan (delta updates).
Context: REFERENCE.md.

**OUTPUT:** test plan + coverage matrix (spec element × TC × bug_class
× level × AC quality × eval status) + AC-quality assessment + run
strategy (persisted per §Coverage matrix).

**DOES NOT:** test execution in design mode (plan only); spec fixes
(reports vague/contradictory ACs); code skeletons in design mode
(execution-mode `tester` does that).

**DONE:** coverage matrix complete (every AC ≥1 TC, no empty rows);
AC quality assessed; vague/contradictory → spec-review signal; run
strategy decided; plan persisted.

**FAIL handling:** coverage gaps → convergence-loop pass 2-3 rising
threshold. Vague/contradictory ACs → ESCALATE to spec review (no
opt-out). Spec-freshness mismatch (`spec_version` ≠ `test_plan_spec_ref`)
→ ABORT, design first.

## Spec-freshness check (MUST before execution)

`spec_version == test_plan_spec_ref`? Yes → continue. No → STOP,
design first. Fields missing → warning.

## Run strategy

When deciding a test plan's run strategy, before running tests in an implementation round, fix pass, review or
verification, and before reusing an already executed check as evidence: read and follow
`skills/testing/run-strategy.md` (run scope per trigger, qualified execution evidence, and §Test selection: the
single home of the suite-scope rule, with the selector, the light path, when the broad run is due, no rerun after a
hash-checked transfer, test runs as rounds, shared fixtures).

## Boundary

- **No linting / syntax check** — that is
  `python_code_quality_enforcement` and the pre-commit hooks.
- **No infrastructure details inline** — fixtures, markers,
  docker-compose conventions → `REFERENCE.md` §Infrastructure.
- **No structural repo check** — dead refs, orphan files →
  `consistency_check`.
- **No board review** — multi-perspective spec review →
  `spec_board`.

## Anti-patterns

- **NOT** L4/L5 assertions too specific. INSTEAD STRUCTURE/TYPE only
  at L4/L5 (specific assertions break on every L2/L3 refactor).
- **NOT** tests after implementation. INSTEAD skeletons BEFORE
  (red-phase tautology guard).
- **NOT** horizontal slice (all tests then all impl). INSTEAD vertical
  slice / tracer bullet (one test → one impl → repeat). Horizontal
  produces tests of imagined behaviour, not actual.
- **NOT** wave through vague/contradictory ACs. INSTEAD trigger spec
  review first (TCs on vague ACs = guessing).
- **NOT** assert on the content of a PM/workflow artifact
  (`docs/tasks/*.yaml`, `.workflow-state/*`, test-plan files). INSTEAD
  assert on code behaviour or code structure only. "Is hazard X
  documented / is decision Y recorded" is process-discipline — its home
  is the spec/ADR + `consistency_check`, not `pytest` (a `tests/` file
  that reads `docs/tasks/` breaks CI the moment the artifact is archived).

Extended anti-patterns (eval script persistence, run-strategy scope
discipline): REFERENCE.md.

## References

Python tooling (pytest config, ruff, conventions):
`skills/python_code_quality_enforcement/SKILL.md`.
