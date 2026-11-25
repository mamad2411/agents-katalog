---
name: adversary-test-plan
description: >
  Adversary extension of a test plan BEFORE implementation — a code-adversary
  adds the edge-case tests the implementer's bias systematically misses (RED
  tests as a required pre-fix gate). Triggers when the change touches a safety
  floor (security/auth/secrets, schema/state-format/data migration, public
  contract, live infrastructure) and a tester design output exists (build
  prepare); NOT for post-implementation review (use code_review_board).
status: active
relevant_for: ["main-code-agent"]
invocation:
  primary: workflow-step
  secondary: [user-facing]
disable-model-invocation: false
uses: [_protocols/dispatch-template, _protocols/context-isolation, _protocols/evidence-pointer-schema]
---

Read and follow `framework/work-principle.md` before taking up work.
Resolve this reference against the framework root; retain the consumer CWD.


# Skill: adversary-test-plan

## Purpose

Tester is spec-derivative — implementer's cognitive bias systematically
misses the same edge cases (compensation-action shares-bug-class,
cycle-entry-point sensitivity, cleanup-tx silent-ack). A soft-prompt
mitigation in the MCA brief replicates the failure across iterations.

Adversary-driven test plan BEFORE implementation: the code-adversary
persona challenges and refines the tester design output and its oracles,
adding edge-case TCs where they cover gaps the spec-derivative tester would miss. RED tests
are the mechanical pre-fix gate — MCA's definition of done requires
every adversary test green.

Mechanism > prompt discipline. Detail / pattern lessons / case
studies / full schemas: `REFERENCE.md`.

## When to call

**Trigger: the change touches a safety floor.** The floors are
security/auth/secrets, schema/state-format/data migration (DB, API,
event or persisted-state schema), a public contract, and live
infrastructure. This is the one home of the trigger; the build
`test-design` step and `skills/testing/SKILL.md` point here. The test
skeleton writer runs under the same trigger. AC count, cross-module
impact and sub-build are not triggers.

No safety floor: skip with a one-line rationale. `on_fail: warn` —
Buddy discipline.

**Bedrock (why this trigger):** facets per
`agents/buddy/multi-perspective.md` —
primarily **blind-spot compensation** (implementer cognitive bias
systematically misses what adversary targets) and **reversibility**
(test gaps on a safety floor are expensive or impossible to recover
from). Elsewhere the change's own tests and the review carry it.

**Position in the workflow:** between `test-design` (tester writes
v1) and `delegation-artefact` (Buddy writes MCA brief). Extended
test plan v2 is input for `test-skeleton-writer` +
`delegation-artefact`.

## Who runs it

Buddy (orchestrator). Spawns code-adversary persona with: spec,
tester test plan, pattern-lessons list (`testing/REFERENCE.md`
§Adversary patterns). Returns: extended test plan v2 + coverage
rationale.

## Process

Section numbers are skill-wide: §1–§2 here, §3–§6 in `challenge-and-integration.md` (the stub below says when to
read it).

### 1. Prepare input

`spec_ref`, `test_plan_ref`, `output_path`, `pattern_refs`
(defaults: `testing/REFERENCE.md` + 388 dogfooding patterns).

### 2. Spawn persona (per `_protocols/dispatch-template.md`)

Context-isolated — adversary sees ONLY spec + test plan +
pattern-lessons, NO implementation code.

### 3.–6. Challenge, output, integration and definition of done

Before spawning the persona, and when the challenged test plan v2 returns, before integrating it and writing the MCA
brief: read and follow `skills/adversary_test_plan/challenge-and-integration.md` (§3 Augenmaß discipline with the
per-TC value-floor; §3a grounding the tester's mechanism-claims; §4 required output format and coverage rationale;
§5 Buddy integration with the post-return Augenmaß check; §6 MCA definition of done).

## Red flags

Skill-violations (full list with detail: `REFERENCE.md`):

- "Looks fine" without substantive coverage and oracle scrutiny — adversary
  mindset not active, regardless of the number of additions.
- No `pattern_class` annotation — no pattern discipline.
- All happy-path variations — "smart-but-wrong" not active.
- TC inflation: ratio >2x without active rationale.
- `patterns_chosen` contains all ~7 classes ritualistically.
- `patterns_excluded` empty — selection act invisible.
- Consolidation without rationale — silent deletion.

## Anti-patterns

- **NOT** trigger without a safety floor. INSTEAD skip with a one-line rationale.
  Because: token overhead without benefit.
- **NOT** TC inflation without Augenmaß. INSTEAD justify each addition or
  refinement; zero additions may be sufficient with evidence. Ratio >2x invites
  stop-and-think + active defence in `proportional_check`, not a target count.
  Because: many + diluted drives MCA into
  workaround patterns (the 41-TC / 6-delta anti-case).
- **NOT** walk pattern classes ritualistically. INSTEAD per class
  check code trigger; no trigger → `patterns_excluded` with
  rationale. Because: pattern-enforcement drives inflation.
- **NOT** merge adversary output unchecked. INSTEAD Buddy verifies
  coverage rationale + ratio + `patterns_excluded` filled. Because:
  ritualistic TCs without pattern links.
- **NOT** skip `test-skeleton-writer`. INSTEAD assertions cover all planned
  adversary TCs, with meaningful pre-fix witnesses for intended behavior changes
  under `skills/testing/SKILL.md`. Retain valid green controls and regressions;
  neither skipped placeholders nor unrelated errors establish the failure witness.
  Because: the witness demonstrates the missing behavior before implementation,
  while controls guard behavior that already works.
- **NOT** treat adversary TCs as optional in the MCA brief. INSTEAD
  first-class definition of done. Because: optional == ignored in
  80% of cases.
- **NOT** silent deletion of tester TCs. INSTEAD consolidate with
  `consolidations` entry + rationale. Because: reduction needs
  audit trail.
- **NOT** "include in case it's needed" default. INSTEAD on
  uncertainty: leave out. Because: default-to-include is the
  TC-inflation root.
- **NOT** generate a TC that asserts on the content of a PM/workflow
  artifact (`docs/tasks/*.yaml`, `.workflow-state/*`, test-plan files).
  INSTEAD assert on code behaviour or structure only. Because: "is the
  hazard documented" is process-discipline (home: spec/ADR +
  `consistency_check`), not a code test — and a doc-presence "theater"
  TC breaks CI on a fresh tree the moment the artifact is archived.

## Boundary

- Not code review (= `code_review_board`, post-implementation).
- Not spec review (= `spec_board`, pre-test-design).
- Not test-plan author (= `testing` skill design mode).
- Not RED skeleton author (= `test-skeleton-writer` downstream).
- Not plan review (= `impl_plan_review`, post-MCA-plan).

## Contract

### INPUT
- **Required:** `spec_ref`, `test_plan_ref`, `output_path`.
- **Optional:** `pattern_refs` (default:
  `testing/REFERENCE.md` + 388 dogfooding).

### OUTPUT

**DELIVERS:** challenged test plan v2 (refined/consolidated where applicable +
any justified adversary TCs with `pattern_class`) + coverage rationale block.
Adversary TCs are first-class definition of done for the MCA brief.

**DOES NOT DELIVER:** RED skeletons (downstream
`test-skeleton-writer`), implementation hints (context-isolated),
silent deletion of tester TCs (consolidation with rationale only).

**ENABLES:** `test-skeleton-writer` input; `delegation-artefact`
pattern coverage as MUST constraint; future pre-commit gate for
ADV-TC pass-rate.

### DONE
- Adversary dispatched + returned.
- Test plan v2 written to `output_path`.
- Coverage rationale block filled (all 6 fields).
- Substantive coverage and oracle scrutiny evidenced, with refinements or
  sufficient existing coverage explained; identified defects resolved.
- Augenmaß visible: additions pass the value floor; >2x ratio has active
  defence. Counts/ratios are descriptive, not success quotas.

### FAIL
- **Retry:** missing substantive challenge, only happy-path scrutiny or an
  unresolved identified coverage/oracle defect → re-dispatch with explicit
  pattern-lessons list (max 2 retries; exhausted → Escalate). Zero additions
  alone do not trigger retry.
- **Escalate:** fundamental spec gap (assumption not testable) →
  STOP, Buddy escalates to user for spec correction.
- **Abort:** trigger fired but no risk (purely declarative) →
  one-sentence rationale, `--skip`.

## Bind rule

- `delegation-artefact`: ADV-TCs as MUST constraints
  (`pattern_class` + count).
- `mca-implementation`: definition of done = ALL ADV-TCs PASS.
- `code-review-board`: reviewers check ADV-TCs PASS + production
  shape (not test shape) covered.
