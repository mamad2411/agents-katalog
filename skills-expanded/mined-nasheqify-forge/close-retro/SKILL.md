---
name: close-retro
description: >
  Close-phase distill — a dedicated read-only agent reads a work-unit's
  artifacts (brief, review verdict, spec-drift, ACs, optional friction-log)
  into a retro 1-pager (§Stale-Decisions T0×T1 + §Patterns-Emerged +
  §Framework-Feed) that the close emit-steps consume (distill→emit). Triggers
  when a workflow's close-bookkeeping fires on FULL, or STANDARD with a
  new-pattern signal; NOT on DIRECT / routine-STANDARD / sub-fix (skip). SoT:
  docs/specs/374-close-retro.md.
status: active
relevant_for: ["buddy"]
invocation:
  primary: workflow-step
  secondary: [sub-skill]
disable-model-invocation: false
uses: []
---

Read and follow `framework/work-principle.md` before taking up work.
Resolve this reference against the framework root; retain the consumer CWD.


# Skill: close-retro

Upgrades the `workflow retro` close sub-step from a missed-entry backstop
into a **systematic distill**. The dedicated read-only `close-retro` agent
(`agents/close-retro.md`) executes it in fresh context; Buddy dispatches at
close-bookkeeping and writes the returned retro 1-pager, which the other
close emit-steps then consume.

SoT for the contract: `docs/specs/374-close-retro.md`. This skill is the
operational checklist.

## When it fires (conditional, skip-eligible)

- **FULL path** → fires.
- **STANDARD path** → fires when the brief surfaced a new-pattern LD
  (pattern-class `new-class-*`, `agents/brief-architect.md` §3) OR the
  work-unit is decision-heavy (orchestrator judgment).
- **DIRECT / AUTHORITY-ONLY / sub-fix**, and any STANDARD build without a
  new-pattern signal → **skip** with a one-line rationale (the replaced
  `workflow retro` sub-step is already skip-eligible).

A mandated every-close fire is a rote ritual whose why thins and which frays.
Fire on signal-bearing work-units only.

## Inputs (all present at close as a natural consequence of the workflow)

| Input | Source | Required |
|---|---|---|
| Brief (build) / RCA root-cause (fix) / frame report (solve) | gate artifact | yes |
| RETURN-SUMMARY | MCA (build/fix) | when present |
| Review verdict (incl. `remaining_findings:`) | code-review-board chief | yes (may be empty) |
| Spec-drift diff | spec-drift-check | yes (may be empty) |
| Task ACs | `docs/tasks/<id>.{md,yaml}` | yes |
| Friction-log `docs/<workflow>/<slug>-observations.md` | opportunistic | optional — read if present |

## 4 stages

1. **orient** — read the inputs end-to-end; reconstruct the work-unit's arc.
2. **gather** — collect candidate findings: emergent patterns, decisions
   whose premise later shifted, framework-feed candidates.
3. **consolidate** — distill into the output template; each finding carries a
   class + evidence pointer (`gate / artifact / file:line`).
4. **prune** — discard noise (absorb-next-touch trivia, duplicates,
   low-signal). Short retro beats complete.

## Output — the retro 1-pager

Written by Buddy to `docs/<workflow>/<slug>-retro.md` (`<slug>` = the active
workflow state-file's slug). Sections:

- **§Stale-Decisions** (the novel core). A stale-decision = a **T0** decision
  (from the brief / RCA — made before implementation) that a **T1** artifact
  (review verdict / spec-drift / RETURN-SUMMARY — made during/after) shifted
  or invalidated. Each row: `Decision (T0)` + `Invalidated-by (T1, file:line)`
  + `Action: supersede | amend-spec | re-open-task | accept-shift | no-action`.
  A row **without** a cited T1 invalidator is NOT a stale-decision — it is a
  pattern (→ §Patterns-Emerged). The cross-temporal link is artifact-derived,
  not session-memory. **Invalidator, not mention:** the cited T1 statement
  must assert a fact that makes the T0 decision *wrong* (or moots it) — a
  verdict that merely comments on the decision's topic or area is not an
  invalidator (that is a pattern, not a stale-decision).
- **§Patterns-Emerged** — `Pattern` + `Evidence (file:line)`. → consumed by
  `knowledge_processor` (mode=process) as its `information` input.
- **§Framework-Feed** — forge-feed-format candidate entries (pre-write filter
  per `docs/dogfood-learnings/README.md`). This IS the replaced retro
  sub-step's output, now systematic. NOT the review-finding router.

## distill → emit

close_retro replaces the `workflow retro` sub-step; its three sections feed
the workflow's **existing** close sub-steps (per `docs/specs/374` §8 table):

- §Stale-Decisions → `documentation_and_adrs` ADR-triple (build/solve close;
  fix has no ADR sub-step → §Stale-Decisions stays noted in the retro). In
  build and solve, a row whose action is not an ADR reaches its owner in the
  same close: `re-open-task` → the task's notes or a new task
  (`task_creation`), `amend-spec` → the spec's amendment path, `supersede` →
  a new entry in the record that holds the T0 decision (decision record or
  ADR), not an edit of the brief. `accept-shift` and `no-action` stay in the
  retro.
- §Patterns-Emerged → `knowledge_processor` (`information`, mode=process).
- §Framework-Feed → forge-feed entries (the replaced sub-step's output).
- `risk_followup_routing` (review `remaining_findings:`) — **untouched**;
  orthogonal to close_retro's lessons.

When close_retro is **skipped**, the sub-step reverts to its `workflow retro`
safety-net behaviour (capture-now missed entries) — no regression.

## Dispatch (Buddy)

1. Decide fire vs skip (trigger above). Skip → one-line rationale, done.
2. Dispatch `agents/close-retro.md` (read-only, fresh-context) with the input
   set + the target workflow (build/solve/fix — narrows the artifact set).
3. Agent returns the retro 1-pager inline (read-only — no write target).
4. Buddy writes it to `docs/<workflow>/<slug>-retro.md`.
5. The close emit sub-steps consume it per the §8 mapping; in build and solve,
   route each non-ADR §Stale-Decisions row to its owner (§distill → emit).

## Boundary

- NOT the review-finding router (`risk_followup_routing`) — orthogonal.
- NOT a parallel forge-feed store/router — §Framework-Feed = forge-feed
  entries via the replaced sub-step.
- NOT EXEC-007 (task_status_update atomic terminal-close) — separate task.

## Anti-patterns

- **NOT** "the brief says the decision held" → that is not evidence. The T1
  artifacts are ground truth for what actually happened. Cite the T1
  artifact, not a restatement.
- **NOT** a §Stale-Decisions row without a T0×T1 cross-temporal link →
  reclassify as a pattern.
- **NOT** fire on a trivial work-unit → rote noise; skip below the trigger.
- **NOT** call/duplicate `risk_followup_routing` for §Framework-Feed →
  forge-feed format via the replaced sub-step.
