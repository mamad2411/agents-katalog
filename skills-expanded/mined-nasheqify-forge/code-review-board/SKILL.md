---
name: code-review-board
description: >
  Multi-perspective code review. 2 levels: L1 (focused) + L2 (board for
  safety triggers, sized by open questions).
  Triggers when a code diff needs multi-perspective review before merge (build verify, fix L1); NOT for PR-level checks (use /review) and NOT for spec review (use spec_board).
status: active
verification_tier: 1
evidence_layout: per_finding
invocation:
  primary: workflow-step
  secondary: [user-facing]
disable-model-invocation: false
cc_wrapper: true
modes: [l1, l2]
uses: [_protocols/discourse, _protocols/context-isolation, _protocols/content-preservation, _protocols/dispatch-template, _protocols/consolidation-preservation, _protocols/evidence-pointer-schema, _protocols/mechanism-model, _protocols/finding-verification]
---

Read and follow `framework/work-principle.md` before taking up work.
Resolve this reference against the framework root; retain the consumer CWD.
Without Buddy (plugin): if this session holds no Buddy boot entry, run `python3 <root>/scripts/forge_setup.py offer-check` once, as its own call (`<root>`: two levels above this skill's folder); if it prints a line, pass that offer to the user in one sentence, then continue with this skill.


# Skill: code-review-board

Buddy checklist. Detail: REFERENCE.md. Protocols:
`agents/_protocols/reviewer-base.md` + `code-reviewer-protocol.md`.

Section numbers are skill-wide: §1 and §6–§10 here (§1.0a in `live-path.md`), §2–§3 in `brief-and-team.md`, §4–§4a in
`checklist-and-dispatch.md`, §5–§5a in `verdict.md`, §11 in `review-package.md` (the stubs below say when to read each).

## Same-turn DIRECT check

A check on DIRECT work that closes in its turn runs as `framework/direct-eligibility.md` §The DIRECT run says, and
nothing else in this skill applies to it: no review brief, package, capture, persisted review or verdict file. Every
other review follows the sections below.

## Mandatory capture and current decision

Before initiating a software review intended to satisfy a mandatory result,
readiness or completion boundary (a workflow step, a task's close, or DIRECT
work that does not close in its turn, `framework/direct-eligibility.md`
§The DIRECT run), load `skills/_protocols/evidence-pointer-schema.md`
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

Use family `code`. Capture slots name every planned producer, including light
`code-verification`; do not invent a Chief at levels where Buddy consolidates.
A relevant fix retries the owner and receives a fresh scoped capture before the
existing reproduction verifier and any §4 mechanism reviewers run. Retain original
findings as exact history; record verification limits in the current explicit decision.

## 1. Level choice

### 1.0 Proportionality gate (MANDATORY — runs before table)

Safety floors are evaluated first. Security/auth/secrets, schema/data
migration and public or cross-component contract changes exclude `light`.
Live infrastructure is sized by the fix's effect: check §1.0a first; when it
holds, the level is `light`; when it does not, live infrastructure excludes
`light` and is the L2 trigger of §1.1. No count or majority can cancel a safety
floor. Include the actual authorization and impact, not merely LOC.
Which floor selects L2 is named in §1.1 (L2 triggers), with its roster
sized in §3; the other floor surfaces run L1 with the matching trigger lens
(§3).

Below those floors, ALL DIRECT criteria in `framework/process-map.md` plus
an executed regression/behavior check allow `light` (single independent
`code-verification`). New local behavior is allowed when bounded and verified.
Otherwise use the level table; resolve missing facts rather than inventing
certainty. Pure typo/format-only changes need a diff check on the reviewed path (none on quick),
not this board.

### 1.0a Small fix on a live path

When live infrastructure is the change's only safety floor, before choosing the level: read and follow
`skills/code_review_board/live-path.md` (when the level is light, what is recorded, when the level is set again).

### 1.1 Level-choice table

```
light:   (1) all DIRECT criteria + executed relevant tests (red→green),
         no safety-floor surface, or (2) a small fix on a live path that
         meets §1.0a (review package) → single code-verification: on DIRECT work
         that closes in its turn, with the record, the implementer's return
         and the diff in its prompt and an inline return
         (`framework/direct-eligibility.md` §The DIRECT run); otherwise on
         the review package (§11). Also the re-verify after a fix pass (re-runs the
         reproductions; plus a scoped code-adversary unless the fix is
         line-local, §4).
L1:      above light, no L2 trigger → core team + Buddy checklist +
         trigger lenses (§3); consolidation per §1.3. DEFAULT for
         bounded engine / contract builds — file count, new module, new
         state vocabulary, error taxonomy, internal cross-component
         contract or effort alone do NOT escalate.
L2:      only on a named trigger: new public API or wire (external
         consumer or cross-process: REST / SSE / CLI / event / published
         package); security / auth / secrets / consent / crypto; real
         migration doubt (stored data must be read or rewritten under the
         new shape, strict read-path decoders included); new subsystem
         (§1.2); live infrastructure where §1.0a does not hold → L2 roster per §3 (trigger
         perspective always; Chief at four or more reviewers, §1.3, §4a).
Unclear: whether an L2 trigger applies → resolve the fact; still
         unclear → L2 for that trigger (its perspective joins the roster).
```

### 1.2 Counting + triggers

- **Spec amendments:** bookkeeping = no trigger; public API / wire or a
  schema break with real migration doubt = L2 trigger; new state-vocab,
  invariant or internal contract = L1 (architect-roots is in its core).
- **NEW MODULE vs NEW SUBSYSTEM:** file in existing dir = MODULE (L1);
  new top-level dir at subsystem depth = SUBSYSTEM (L2).
- **`code-architect-roots` REQUIRED on L2** when `effort: L|XL OR
  pattern-replacement OR LD-count ≥ 6` AND change introduces new
  exported contract or replicable-downstream pattern. Shape-preserving
  extractions: idle on L2 (see `agents/code-architect-roots.md`). On L1
  it is core and always dispatched; on shape-preserving work its focus
  narrows to the diff's own contracts.

Detail (incl. post-MCA-return trigger consequence): REFERENCE.md.

### 1.3 Consolidation

At every level, with at most three reviewers Buddy reads the complete
reports directly and consolidates (and enforces the checked-scope section a
Chief would check): keep/refute triage per §5, reports
persisted verbatim before reading, verdict at the §7 path. With four or
more reviewers a Chief consolidates their persisted returns. One roster
covers one reviewed change; splitting a change to stay below this threshold
is not allowed. Buddy owns the verdict and verifies pivotal
claims in either case. Reviewer count controls consolidation overhead,
never safety-floor selection or evidence requirements.

## 2.–3. Review brief and team composition

After the level choice and before any reviewer dispatch: read and follow
`skills/code_review_board/brief-and-team.md` (§2 review brief, MUST before dispatch; §3 team composition, L1
trigger lenses and L2 sizing).

## 4.–4a. Buddy checklist and L2 dispatch

When assembling prompts and dispatching reviewers, when running the L2 pre-board frame check, and before a fix pass
or re-verify: read and follow `skills/code_review_board/checklist-and-dispatch.md` (§4 Buddy checklist, including
the re-verify table and the simplify-before-patch gate; §4a L2 dispatch with the pre-board frame check); each seat and the chief is called per
`skills/_protocols/role-dispatch.md`. Before a
fix after a review in which every seat passed, read `review-package.md` §Small fix after a passing review first; where
it applies, it replaces the re-verify.

## 5.–5a. Verdict and re-review

When reviewer returns are in and a verdict is consolidated or decided, and before dispatching a multi-reviewer
re-review: read and follow `skills/code_review_board/verdict.md` (§5 verdict: reality first, then disposition;
§5a re-review two-phase).

## 11. Review package

Before a change that will be reviewed starts (BASE), before any reviewer dispatch, a re-review after a fix pass
included, and when persisting a seat's return or writing the verdict: read and follow `skills/code_review_board/review-package.md` (§11 BASE, the package recipe, what each seat
receives, the fix range, the Range line in the persisted review).

## 6. Discourse

L2: optional (Buddy). L1: none. Mechanic: `_protocols/discourse.md`.

## 7. Output paths

Agent reviews: `docs/reviews/code/{task-id}-{role}.md`.
Verdict: `docs/reviews/code/{task-id}-verdict.md` — the **canonical
engine-facing pointer** (task-id, undated; a `[DISCIPLINE]` write-canonical
convention, updated in place on re-review). The `[WORKFLOW]` completion gate's
`pointer_check` checks exact retained decision bytes and current owner/subject
under `code_success`, including with force. Canonical names do not confer identity.
Preserve earlier selected payloads before replacing this locator. No mechanical rename-to-canonical exists (a fuzzy task-id glob was
rejected; see `framework/enforcement-registry.md`). On L2 the chief also writes
`{task-id}-consolidated.md`; the gate keys on the **verdict only**.

## 8. Contract

**INPUT:** the review package (§11), L0 PASS, MCA return summary.
Optional: spec_ref, delegation file.

**OUTPUT:** verdict, brief, per-agent reviews under `docs/reviews/code/`.
On FAIL: findings + severity + locators + fix hints.

**DOES NOT:** code fixes, spec review (→ `spec_board`), lint/type (→ L0).

**DONE:** explicit current decision adopted, code_success checked for forward
readiness, verdict decided, brief written, reviews persisted, L2 chief
tracking table present, SAVE done.

## 9. Boundary

- Spec review → `spec_board`.
- Pre-code plan review → `impl_plan_review`.
- UX board → `spec_board` (mode=ux).
- Lint / type → L0 (ruff, mypy before L1).

## 10. Anti-patterns

- **NOT** dispatch without brief. INSTEAD run 5 steps first.
- **NOT** L1 on an L2 trigger (public API / wire, security, real
  migration doubt, new subsystem, live infrastructure where §1.0a does not
  hold). INSTEAD when unclear → L2 for that trigger. Equally **NOT** L2 on file count or new
  state vocabulary alone — that is L1 — and **NOT** the whole L2 roster by
  habit: size it per §3.
- **NOT** route LOW to `new_task` or write cost-justification escape.
  INSTEAD `accept` or re-classify MEDIUM with named defect. Text
  justifications hallucinate; only mechanical rule enforces.

Extended (L0-after-fix, tracking-table preservation, single-reviewer
pass-1.5, scope-files in fix-pass brief): REFERENCE.md.
