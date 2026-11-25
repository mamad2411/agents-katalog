---
name: spec-board
description: >
  Multi-perspective review of whether an EXISTING spec is rebuild-ready —
  could an implementer rebuild it 1:1 from the spec alone? Use when a spec
  needs a quality check after writing and before build (completeness /
  consistency / contract / dependency gaps); reach for it instead of
  eyeballing a spec yourself. NOT for authoring a new spec (use
  spec_authoring) or syncing a spec to code (use retroactive_spec_update).
status: active
verification_tier: 1
evidence_layout: per_finding
invocation:
  primary: workflow-step
  secondary: [user-facing, sub-skill]
disable-model-invocation: false
modes: [standard, deep, ux]
uses: [_protocols/plan-review, _protocols/discourse, _protocols/context-isolation, _protocols/content-preservation, _protocols/dispatch-template, _protocols/consolidation-preservation, _protocols/piebald-budget, _protocols/skill-guardrails, _protocols/analysis-mode-gate, convergence_loop, _protocols/evidence-pointer-schema, _protocols/mechanism-model, _protocols/finding-verification]
---

Read and follow `framework/work-principle.md` before taking up work.
Resolve this reference against the framework root; retain the consumer CWD.
Without Buddy (plugin): if this session holds no Buddy boot entry, run `python3 <root>/scripts/forge_setup.py offer-check` once, as its own call (`<root>`: two levels above this skill's folder); if it prints a line, pass that offer to the user in one sentence, then continue with this skill.


# Skill: spec-board

Buddy checklist. Detail: `REFERENCE.md`. Agent protocols:
`agents/_protocols/reviewer-base.md` + `spec-reviewer-protocol.md`.

Rebuild-ready means buildable from the spec together with the test matrix or the tests it names: behaviour at
contract level in the spec, its cases in the matrix or tests (`framework/spec-engineering.md` §Convention: spec
carriers).

Section numbers are skill-wide: §0, §3, §5 and §7–§10 here, §1–§2 in `depth-and-team.md`, §4–§4b in
`checklist-and-dispatch.md`, §3a and §6–§6a in `post-pass.md` (the stubs below say when to read each).

## 0. Plan + review (required without a frame)

Without a frame: plan scope from project intent and local objective (owner: framework/invariants.md §Intent-driven),
plus tool and alternatives. Self-review and dispatch `plan-adversary` on non-trivial plans. With a frame: reference it.
Templates: `_protocols/plan-review.md`.

## Mandatory adoption ownership

Before initiating a software review intended to satisfy a mandatory result,
readiness or completion boundary, load `skills/_protocols/evidence-pointer-schema.md`
§9. Resolve one exact owner and capture before dispatch. Declare code subject
state/output exclusions before enumeration and check that they omit no required
reviewed inputs. Use persisted-success capture stdout for producer metadata and
pass each assigned slot, scope/focus and history neutrally. Preserve complete
returns verbatim with actual actors, paths and raw-byte digests before consumption.
A canonical verdict path is only a locator; retain prior payloads before replacing
it. Buddy's explicit current decision selects the current reports of the final
applicable review and names any history; it answers each adoption diagnostic. Adopt it through `evidence-pointer-schema.md` §9, then check the applicable policy before any
mandatory result/readiness write or completion. Current negative evidence supports
repair; it grants no success permission. Identity does not replace substantive
coverage, source interpretation, severity/risk rules or authorization.

Standalone execution owns `agent-dispatch`; receive a caller-supplied exact owner
for nested execution and do not create another capture. Pass
`review_owner_workflow_id` and `review_owner_step_id` into the readiness consumer;
a separately tracked child retains its existing explicit parent identity.

## Process — common

1. Decide scope + depth (incl. foundation flag).
2. Assemble role-based team.
3. Dispatch context-isolated reviews; consolidate via chief.
4. Close NEEDS-WORK via fix-loop until 0C+0H.
5. Post-pass checks + task / commit / deploy cleanly closed.

## 1.–2. Depth mode and team composition

When deciding scope and depth mode and assembling the team, before dispatching the board and before each later
pass's team: read and follow `skills/spec_board/depth-and-team.md` (§1 depth mode: §1.0 proportionality gate with
the override floor and the pre-gate FAILs, §1.1 scoped pre-check and 4 checks; §2 team composition with the
architect-roots and implementer triggers and the cold seat after a mechanism redesign).

## 3. Flow

**Standard:** dispatch → chief (+ optional discourse) → chief synth
→ post-convergence check → SAVE → 0C+0H DONE; else escalate Deep.

**Post-convergence check (required after chief synth):** chief
answers in consolidated: (1) "Weakest point in PASS — what tips it?"
(2) "Which single-agent finding was downweighted the most — rightly so?"

**Deep:** pass 1 (7) → chief → DISCOURSE → chief → SAVE; pass 2+
(4) → chief → discourse → SAVE → fix → next; final (2) → Buddy direct.
Every fix from pass 2 on is preceded by the §4 step 10
Simplify-before-patch check.

Chief consolidation: analysis-mode gate
(`_protocols/analysis-mode-gate.md`) before findings classification.

### 3a. Delta-verify (standard mode, post-fix re-check)

After every relevant fix in standard mode, before re-checking: read and follow `skills/spec_board/post-pass.md` (§3a
delta-verify: exact-owner retry and fresh capture, the 2-agent delta re-check trigger, team and acceptance).

## Process — mode deep

Same flow as above; starts with pass 1 (7) and loops through pass 2+
(4) until convergence.

## Process — mode ux

UX review is not a separate skill. For UI-heavy specs `spec_board` runs in
`mode=ux` with UX personas (`board-ux-heuristic`, `board-ux-ia`,
`board-ux-interaction`) as extended team variant. Functional + UX
findings in same consolidated. When the change has a look and an
experience contract (`skills/ux_authoring/SKILL.md`), each UX seat's
prompt names both files with the behaviour spec as the review subject.

## 4.–4b. Buddy checklist, cross-task ACs and mechanism cells

Before the first board round for a state/transition-table spec, have its author run a small script that derives
each state × operation result from the invariants using the governing states and operations (§4b). Give seats
the current output with gaps and contradictions against the table as review input.

When assembling prompts and dispatching reviewers, when the spec carries cross-subsystem ACs or a
`§Mechanism-Lifecycle` section in scope, and before a fix pass: read and follow
`skills/spec_board/checklist-and-dispatch.md` (§4 Buddy checklist for dispatch, including C-VERIFY and the
Simplify-before-patch check before fix pass ≥ 2; §4a cross-task AC validation; §4b mechanism cells as the review
unit, MUST before PASS).

## 5. Discourse

Deep: ALWAYS after chief. Standard: Buddy decision (proportional).
Mechanic: `_protocols/discourse.md`.

## 6.–6a. Post-pass and risk carry-forward

After each pass's consolidation, before closing the pass, and when unfixed findings are carried forward: read and
follow `skills/spec_board/post-pass.md` (§6 post-pass checklist, NON-NEGOTIABLE; §6a risk carry-forward, MANDATORY on
user-override / cherry-pick / valve-hit / ESCALATE-accepted).

## 7. Output paths

Reviews: `docs/reviews/board/{spec-name}-{role}-pass{N}.md`
Consolidated: `docs/reviews/board/{spec-name}-consolidated-pass{N}.md`
(task-qualified `{spec-name}-consolidated-task{id}-pass{N}.md` when
another task already owns the plain namespace). Pass files are history:
never rewrite their pointers after a spec amendment.

**Adoption verdict (the completion artifact):** for an applicable supported decision
(including NEEDS-WORK for evidence/repair),
Buddy writes `docs/reviews/board/{task_id}-spec-verdict.md` (build, and
review runs with a task); a task-less review run falls back to
`docs/reviews/board/{spec-name}-verdict.md`. Frontmatter `schema_version: 1`,
`adopted_from:` (the consolidated pass file), `reviewed_revision:` (commit of the
adopted spec) and an evidence block holding the verdict's pivotal pointers. Buddy
re-checks those pointers against the adopted spec himself (C-VERIFY); adoption
does not check the decision's own pointers mechanically. Include the §9 run/subject, explicit decision and current_reports slot/path/
digest/actor references; answer the adoption diagnostics in the decision.
Adopt before current use; `spec_success` permits only PASS without an unresolved mediator
audit marker in a captured file. Canonical copies must be
byte-identical to the retained decision; preserve earlier payloads before replacement.

## 7a. Review-mode variants

**Standard (default):** agents review per role; findings grouped by agent.
**5-dimensions (corpus sweeps):** agents additionally review along 5
quality dimensions; chief consolidates per dimension. Use after
`spec_update` or pre-launch sweep. Mechanics:
`spec_board/5-dimensions-review.md`.

## 8. Contract

**INPUT:** spec file, SPEC-MAP read; exact mandatory owner when nested. Optional: frame
report, engine context. Context: protocols (reviewer-base, spec-
reviewer-protocol, dispatch-template, consolidation-preservation,
piebald-budget).

**OUTPUT:** board verdict (PASS 0C+0H or NEEDS-WORK with severity
distribution), consolidated findings, tracking table on NEEDS-WORK,
`board_result` (machine-readable), review files under
`docs/reviews/board/`.

**DOES NOT:** fixes (Buddy/MCA work), code, spec authoring.

**DONE:** final applicable current decision adopted and spec_success checked;
verdict 0C+0H every required pass; tracking table complete;
merge + minority checks executed; all findings fixed; Delta-Verify
done if triggered; Task YAML updated; result persisted. Commit/push/deploy
follow `framework/process-map.md` §Authorization; retain any authorized
missing publication as an unresolved obligation. Local completion grants
no publication authority.

**FAIL handling:** NEEDS-WORK → fix → next pass (max 3 via
`convergence_loop`). Standard → Deep on ≥1C or ≥3H. After max →
ESCALATE.

## 9. Boundary

- Code review → `code_review_board`.
- Pre-code plan review → `impl_plan_review`.
- Legacy UX board → `mode=ux` here.
- As-is spec update → `spec_update` (writes before board reviews).

## 10. Anti-patterns

- **NOT** pass findings on without chief consolidation. INSTEAD
  check chief signal + tracking table (silent-loss prevention).
- **NOT** close standard without discourse when findings diverge.
  INSTEAD trigger discourse.
- **NOT** start spec fix as new full pass. INSTEAD scoped pre-check
  + delta review (pass inflation = wasted tokens).
- **NOT** dispatch agents without context isolation. INSTEAD every
  agent gets ONLY the spec (anchoring bias).
- **NOT** run §1.1's 4 checks before §1.0's proportionality gate.
  INSTEAD §1.0 first; security + full-path remain hard overrides.
- **NOT** skip the §Module-Decomposition OR §Test-Strategy pre-gate
  on a NEW L1+ spec by assuming legacy. INSTEAD verify creation-date
  or section-history before silent-skipping.


### Observational workflow checks

Navigation/recovery never execute commands. Use existing authorized tools for
actions and observe their actual current outcome. The manual action checkpoints
require nonblank evidence supplied with the current `--complete --evidence`
invocation, including force. Missing/failed/timed-out/unknown outcomes stay open
with the concrete blocker; no-new-commit save still requires current persistence
observations for applicable project/user roots and required remotes. Completion
is agent-confirmed, never engine proof of free-text truth or remote correctness.
See `framework/workflow-engine-cookbook.md` for the retained completion contract.
