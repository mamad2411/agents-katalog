---
name: superrefine
description: Use when an eligible upfront-v1 stage needs bounded executable preparation from current source, code, predecessor delivery, and contract evidence without changing its approved commitments.
license: MIT
related skills: superstage, superauthor, supertraverse, superreplan
---

# Superrefine

`superrefine <root> <stage-id>` is the docs-only author for one unstarted upfront stage identity. It turns
an approved stage contract into an executable prepared plan only when current evidence supports its
existing commitments. It is not a general planner, executor, or repair tool.

The dispatching controller assigns `PLAN_REFINER` and its model/effort. A standalone invocation runs
under the current session and must say that it cannot change its own model pin. Do not dispatch
children, invoke a panel, or call another heavy skill: author and review this bounded change directly.
The controller counts this as its one heavy skill for the tick.

## Input and entry gate

Require the absolute root-plan path and one stable stage ID. Do not infer either from the working
directory. Resolve mode and the active stage map through superstage S1 in **active** context, then
apply S2. The root must resolve exactly to `upfront-v1`; incremental and unmarked roots retain their
existing superplan lifecycle. Return **BLOCKED** for an invalid graph, an active replan barrier, a
missing/duplicate/retired stage ID, or unreadable required evidence.

Standalone superrefine may validate S1–S5 directly; use the explicit requested stage ID rather than
asking traversal to select a second target. Resolve it from S1's active map and apply S3/S5 evidence
predicates without recursively calling S3's receipt classification.

Before drafting, require all of the following:

- The active stage identity is unstarted and has no closeout, execution report, code PR, CI recovery
  packet, or `executed — PR open` / partial-execution state of its own. For a published C8 successor,
  distinguish its generation, plan path and revision from the predecessor execution identity. A
  predecessor's open PR and partial closeout do not block preparation when the published C8 record
  explicitly maps that predecessor to this successor with `resume-existing`, preserves the old
  PR/branch/worktree and task history, and leaves the successor without its own execution attempt.
  Verify the mapping and identities from tracked evidence; a row label alone is insufficient.
  Existing execution of the active identity continues through task-loop/CI recovery instead of
  preparation. Never overwrite predecessor task history or treat its CI as successor evidence.
- Each declared prerequisite has S3's verified delivery evidence for the contract revision consumed:
  integrated code/delivery receipt and tracked closeout, or the stated verified non-code discovery
  evidence. An open, closed-unmerged, declined, missing, or contradictory provider does not qualify.
- The authoritative source agreement/revision, current code baseline, predecessor delivery receipts,
  consumed/produced contract revisions, applicable findings, and current stage revision are readable.

First triage verified differences in that evidence through S4. A readable, verified source/acceptance,
scope, dependency, provider, or shared-contract difference is **REPLAN-REQUIRED** even if it means
the old prerequisite cannot satisfy the stage: publish the evidence finding and preserve the approved
leaf rather than swallowing it as an eligibility failure. Evidence that is missing, malformed,
ambiguous, or contradictory without a verified authoritative resolution is **BLOCKED**. A stage whose
prerequisites are merely not delivered yet is dependency-blocked, not a reason to speculate or refine
it early.

## Prepare from evidence

Read the approved stage in full enough to retain its goal, scope in/out, chosen approach, acceptance
ownership, dependency edges, shared `Consumes` / `Produces` behavior, assumptions, and scenarios.
Read the actual predecessor outcomes and source requirements, inspect the current code baseline, and
resolve only the bounded details that those sources decide: file placement, helper/signature detail,
task order, test setup, concrete test code, and executable verification.

Write a candidate leaf and report to scratch outside the goal folder. The prepared leaf meets
superauthor A2/A3's prepared-plan standard: exact file ownership, actionable tasks, code where it
clarifies the implementation, distinguishing test details, and verification tied to the current
evidence. It must be executable without another architecture or requirements decision. Do not invent
unobserved predecessor facts to make it look detailed.

**Check feasibility against what providers actually deliver.** For each acceptance case that needs
a specific result from a provider — a success, a complete verdict, a supported scope — cite the
provider evidence that it returns that result on the case's input: a delivered test, a closeout row,
or the code path. A provider closeout limitation that excludes the input, or no such evidence at all,
makes the outcome **REPLAN-REQUIRED** now, before execution: the finding names the case, the provider
and the limitation, and lists superreplan's remedies (*Prefer the smallest unblocking change*) with
which apply. Delivered is not the same as able to deliver what this stage needs.

Any restriction the prepared leaf adds beyond the approved stage — a budget, a ban, a required order,
an excluded evidence source — carries the origin tag `[planner]`; one carried from the stage keeps its
`[source: …]` or `[owner: …]` tag (superreplan's origin rule). Never add a restriction that forbids
the fix current evidence points to.

Classify the observed change with superstage S4 before publication:

- **PREPARED** only when acceptance, scope boundaries, chosen approach, dependency edges, provider
  ownership, and shared contract semantics all remain unchanged. A content amendment increments
  `Stage revision`; attaching a first receipt with no plan-body change does not.
- **REPLAN-REQUIRED** when evidence would change any of those commitments, including an acceptance or
  source change, scope expansion, topology change, or contract behavior/revision — or when an
  acceptance case needs a provider result the feasibility check cannot cite. Preserve the
  approved leaf, write a precise finding with evidence and affected contracts/stages, and do not mark
  any row ready.
- **BLOCKED** when the needed evidence cannot support either classification. Do not guess, publish a
  partial prepared leaf, or manufacture a receipt.

## Receipt and review

For a PREPARED candidate, create a durable preparation report that satisfies superstage S5. It records
the root path/generation; stage ID/revision; lowercase SHA-256 of the exact UTF-8 leaf bytes with only
the complete `**Preparation:** ...` line and its newline omitted; examined code commit; authoritative
source/revision; every consumed contract and provider-delivery receipt; relevant findings/revisions;
and an explicit amendment classification:

```markdown
**Outcome:** PREPARED
**Amendment kind:** none | content-amendment | compatible-baseline-revalidation
**Content amendments:** none | <evidence-grounded summary>
**Baseline revalidation:** none | <prior receipt and focused comparison>
**Provider results each acceptance case depends on:** none | <case → provider → evidence>
```

Use `content-amendment` only for a plan-body detail change and list it. Use
`compatible-baseline-revalidation` only after a focused comparison finds an unrelated baseline/HEAD
advance compatible; it preserves the stage revision and writes a refreshed validation receipt rather
than silently treating the prior receipt as current. `none` means first preparation attached no
plan-body amendment. A docs-only publication commit may advance internal-vault `HEAD` without making
the examined code baseline stale; compare relevance rather than requiring raw `HEAD` equality.

Self-review the candidate directly under superauthor A4 and verify all of these against the approved
stage, not merely against prose intent:

1. Acceptance IDs/conditions, scope in/out, approach, dependency edges, and contract IDs/revisions
   are unchanged.
2. Every prepared task/file/test detail follows current source, code, and predecessor evidence.
3. The sole Preparation pointer is the only omitted digest line; every other plan byte is bound.
4. S1/S2 and S5 pass in candidate context through the explicit intended-vault-path-to-scratch-path
   map, including report readability. Candidate validity authorizes atomic publication only.
5. Every restriction the leaf adds is tagged `[planner]`, and none is presented as owner authority.

If preservation review finds a commitment mismatch, return **REPLAN-REQUIRED** with a finding; it
never becomes a local refiner ruling. Correct a candidate-only digest/path/detail mistake and rerun
review before publication; a missing or ambiguous evidence source is **BLOCKED**. Do not change scope,
acceptance, edge, shared-contract, or architecture decisions during refinement.

## Publish and report

For a clean result, use superauthor A6/A7 to publish in one docs-only change: the leaf, receipt, and
immediate parent row set to `PLAN WRITTEN — ready to execute`. Revalidate S1/S2/S5 in active context
after publication before claiming readiness. Preserve the previous receipt as history whenever a
refreshed validation supersedes it. A no-op/revalidation publication remains docs-only and does not
claim code integration or change root Plan generation.

For REPLAN-REQUIRED, publish only the evidence finding through the established docs lifecycle; keep
the stage unprepared and parent row `PLAN WRITTEN — needs refinement`. For BLOCKED, do not publish
false readiness. Preserve confirmation, vault, C9, legacy, and A7 rules throughout.

Return exactly this report shape, using `none` for absent artifacts:

```text
**Outcome:** PREPARED | REPLAN-REQUIRED | BLOCKED
**Root plan:** <path>
**Stage ID:** <id>
**Stage revision:** <integer>
**Preparation:** <report path or none>
**Finding:** <report path or none>
**Files changed:** <explicit paths>
**Integration:** <docs PR or vault commit>
```
