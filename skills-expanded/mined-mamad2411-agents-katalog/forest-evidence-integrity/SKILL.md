---
name: forest-evidence-integrity
description: "Preserve FOREST source-bound evidence across run lineage, verification, Goal applicability, comparison, figures, and manuscripts. Use for evidence-facing frontend/client changes or stale-result diagnosis; not as a substitute for scientific judgment or experimentation."
---

# FOREST evidence integrity integration

Keep every displayed measurement and acceptance claim attributable to the actual
run, revision, artifact, and declared scope that supports it.

## Read the relevant evidence path

Read [repository-map.md](references/repository-map.md) for the changed evidence
consumer, source owners, risk states, and regression cases before implementation.
It records inspected HEAD `ff16c3f656f94d053d1bba65c6b3a07a5feaccde`;
recheck affected source at the target HEAD. Source paths are FOREST-root relative.
Follow the changed binding through verification and its immediate consumers;
extend only when a concrete current-versus-historical question is unresolved.

Preserve canonical `research/agents/skills/` policies for autonomous research,
judgment, experimentation, and academic writing. This skill governs frontend
evidence representation and transport; it cannot redefine scientific validity,
experimental design, completion, or acceptance criteria.

## Keep four decisions separate

1. Execution status: was this task actually completed?
2. Source-bound verification: did declared checks pass for these bound artifacts?
3. Goal applicability: is that execution usable for the current scoped Goal?
4. Purpose acceptance: are the declared handoff's additional conditions satisfied?

Do not compress them into a single green success badge. Compilation, a generated
figure, manuscript metrics eligibility, or an operational publication audit is
another distinct result; none certifies a scientific discovery or venue acceptance.

## Preserve identity and scope

- Retain run/project/node/branch IDs, node_revision/current_node_revision,
  latest_run identity, result revision/current flags, input dependencies, saved
  method/configuration, artifact paths, and relevant execution context.
- Run lineage `current` describes its revision/result flags; it is not semantic
  correctness and must not be upgraded to independent verification.
- Preserve every metric's original run ID, exact JSON pointer, units, statistical
  unit, condition/split/seed, uncertainty definition, and source scope when present.
- Keep unknown or null measurements/accounting unknown; do not display them as
  zero, fabricate a curve, or fill missing trial values from a demonstration.
- Preserve unknown data/configuration keys and complete bindings when editing.
  Generic resource PATCH shallow-merges data; nested supplied keys replace values.
- Missing/deleted historical sources remain inspectable as missing; never
  silently bind a newer run or recreated node to the old claim.

## Read authoritative verification

Use `/api/runs/{ident}/verification`, not an editable artifact's reported pass.
At the inspected HEAD, verdicts are `unverified`, `accepted`, `rejected`, or
`inconclusive`; preserve raw unfamiliar values and check-level details.
Show the bound producer/verifier identities, reason, `check_scope_paths`, and
`numerical_scope`. Accepted checks cover their named scope, not all run outputs.
Numerical handoff requires every transmitted numeric leaf to be checked against
the actual artifact and consistent with recorded metrics where enforced.

When offering a verifier, read [repository-map.md](references/repository-map.md)
for the six actual check kinds and service-owned fields. Enqueue returns a Run,
not a verdict. Independent-repeat checks require successful execution receipts;
equal files or prepared pass JSON alone do not establish an independent rerun.
Changed source/config/verifier revision or artifact bytes can revoke acceptance.
Refetch after edits and surface the resulting reason rather than retaining a badge.

## Handle changed Goals and dependencies

Use applicability readback separately from computational verification. Statuses
are `current`, `approved`, `excluded`, `needs_review`, or `unknown`; only current/
approved are ready. A Goal edit preserves prior computation and can require
`reuse`/`exclude` with a scientific reason and the reviewed project revision.
Keep scoped direction and goal-contract version identity, including multi-Goal
execution history. Reuse approves relevance, not an unchecked measurement.

Structured bindings carry precise affected metric/claim/figure/manuscript locations.
Retain `dependency_bindings`, `stale_dependencies`, and their source/target paths.
A prose mention of an ID does not create a dependency. Explain actual stale
locations; neither invalidate unrelated documents nor conceal affected content.

## Respect handoff, figure, and manuscript contracts

Read [repository-map.md](references/repository-map.md) when touching acceptance,
comparisons, figure outputs, paper generation, or export. Purposes are
`exploratory`, `raw_data`, `comparison`, and `major_claim`; inspect failures and
source_checks rather than reconstructing readiness in the browser.
Preserve raw observations and contrary evidence alongside interpretations.
Figures retain source data and real output paths; a schematic is conceptual.
Manuscript generation selects explicit completed runs with finite numeric metric
artifacts, retains bindings, and rechecks source measurements. Current PDF export
requires compiled_revision equal to paper revision. Queued generation/compile
does not create an immediately available artifact.

## Verify the affected integrity invariant

Use targeted cases in [repository-map.md](references/repository-map.md): stale
retry/current revision, artifact edits, partial numeric scope, unrelated verifiers,
Goal applicability, structured stale locations, real metrics, and current PDF.
Unit fixtures can check isolated display logic. Integrated changes require an
isolated real local backend/worker workflow and actual evidence artifacts as
guided by the browser-testing skill; fixture-only data cannot establish that path.
Do not start the user's existing tasks or call an unauthorized paid provider.
Report observed behavior and unexecuted checks plainly.
Source attribution establishes provenance; keep the limits of a check visible
without adding new scientific gates or replacing expert judgment.
