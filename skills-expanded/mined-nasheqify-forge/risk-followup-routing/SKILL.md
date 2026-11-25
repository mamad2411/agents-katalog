---
name: risk-followup-routing
description: >
  Route a chief verdict's `remaining_findings:` entries by their `target:`
  annotation (instead of one task per finding). Triggers when a chief verdict
  carries remaining_findings: to route (build close, fix close); NOT for
  creating tasks directly (use task_creation).
status: active
invocation:
  primary: workflow-step
  secondary: []
disable-model-invocation: false
spec_ref: docs/specs/306-brief-architect.md
uses: [task_creation]
---

Read and follow `framework/work-principle.md` before taking up work.
Resolve this reference against the framework root; retain the consumer CWD.


# Skill: risk-followup-routing

## Purpose

Dispatch each `remaining_findings:` entry from a chief verdict to
the correct downstream destination based on its `target:` field.
Replaces the legacy `risk-followup-task` step which created one
task per finding (wrong granularity for the actual mix of finding
types).

## When to call

- Build workflow `close-bookkeeping` gate, after chief verdict.
- Fix workflow analogous gate, after chief verdict.
- Review workflow analogous gate, after chief verdict.

The chief is responsible for annotating every entry with `target:`
per the 7-value enum (spec 306 §4.7 + `code_review_board/verdict.md` §5).
This skill assumes that annotation exists; if any entry has empty
`target:`, the skill fails with a clear error and surfaces back to
the chief for re-emit.

## Input

- Path to chief verdict file (e.g.
  `docs/reviews/board/<id>-consolidated.md`).
- Path to consumer's `context/risk-watch.md` (created if absent
  per `skills/_protocols/risk-watch-template.md`).

## Process

1. Parse the chief verdict's `remaining_findings:` block. Validate
   that every entry has a `target:` field. On missing field: FAIL
   with `target_missing_on_<id>`.
2. Group entries by `target:` value:
   - `spec_text`: collect all into a single batch.
   - `new_task`: each entry filed independently.
   - `watch_item`: collect for risk-watch append.
   - `accept`: the verdict entry is the record (accepted
     limitation — distinct from `absorb_next`: no future fix
     implied).
   - `absorb_next`: the verdict entry is the record; the next review
     brief for a touched file names it (`code_review_board/brief-and-team.md` §2).
   - `closes_with: <id>`: validate referenced finding exists in
     same verdict.
   - `re_review: <reviewer>`: collect for re-dispatch.
3. Dispatch per group:
   - **spec_text batch:** if non-empty, dispatch
     `agents/spec-text-drift-batch.md` once with the full list
     (per spec 306 §4.8). If chief verdict is FAIL and MCA
     fix-pass dispatches in parallel, fire both in one tool message
     (the parallel-dispatch invariant is in §4.8).
   - **new_task per entry:** dispatch `task_creation` skill per
     entry. When called from this routing, skip the
     duplicate-check step of `task_creation` (the chief verdict
     already deduped at finding-level).
   - **watch_item:** if `context/risk-watch.md` doesn't exist,
     create from `skills/_protocols/risk-watch-template.md`. Append
     each entry verbatim under `## Entries`.
   - **accept:** no file, no fix, no task, no trigger; the verdict
     entry records the known accepted limitation.
   - **absorb_next:** no immediate action; the verdict entry stays
     the record until a later change to that file closes it.
   - **closes_with:** assert the referenced finding exists in the
     same verdict. On miss: FAIL with `closes_with_target_missing`.
     On hit: no further action.
   - **re_review:** dispatch the named reviewer with the finding
     cluster as scoped focus. The re-review's verdict appends to
     the existing chief verdict (not a new pass). One-shot — if
     uncertainty persists, escalate to council per existing
     cross-layer-decision pattern.
4. Aggregate routing report: `<N> entries routed (<count> spec_text,
   <count> new_task, <count> watch_item, <count> accept,
   <count> absorb_next, <count> closes_with, <count> re_review)`.

## Output

DELIVERS:
- Spec-text patches applied (via spec-text-drift-batch sub-agent
  return, when spec_text entries exist).
- Tasks filed (via task_creation per entry).
- Risk-watch append (one or more entries).
- accept / absorb_next / closes_with: the verdict entry is the record (no file).
- Re-review dispatched for re_review entries.

DOES NOT DELIVER:
- No semantic edit of finding content. The routing applies what
  the chief decided; it does not re-decide.
- No task duplicate-check (delegated to chief verdict's
  finding-level dedup; explicit skip-flag passed to task_creation).

ENABLES:
- Bulk-task-bloat avoidance (vs the legacy `risk-followup-task`
  which filed one task per finding regardless of type).
- Mechanical traceability (every finding ends up in a known
  location: applied diff / task / risk-watch / verdict).

## Failure modes

- **Missing `target:` field:** chief verdict didn't annotate all
  entries. FAIL — return to chief for re-emit.
- **`closes_with: <id>` references non-existent finding:** chief
  emit error. FAIL with locator.
- **`re_review: <reviewer>` references unknown reviewer:** the
  reviewer name is not in the framework's persona registry. FAIL
  with reviewer name + suggestion to use a known persona.
- **spec-text-drift-batch returns PARTIAL:** some entries skipped.
  Surface the skip reasons to user; the routing succeeds for the
  applied entries but flags partial-completion.

## Replaces

- Legacy `risk-followup-task` step in build / fix / review
  WORKFLOW.md. The legacy step's name is preserved as a deprecated
  alias for one release cycle to avoid breaking in-flight runs;
  new dispatches use `risk-followup-routing`.
