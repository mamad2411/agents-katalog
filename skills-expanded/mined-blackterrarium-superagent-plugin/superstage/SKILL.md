---
name: superstage
description: Use when a plan-tree consumer must resolve planning mode, validate an upfront stage graph, determine preparation or execution eligibility, classify refinement versus structural replanning, or verify a preparation receipt.
license: MIT
---

# Superstage

The shared contract for upfront plan trees. `supergoal`, `supertraverse`, `superrefine`,
`superreplan`, `superrun`, `superfinish`, and `superagent` apply clauses S1–S5 inline; they do not
copy or weaken them. Superstage is a clause library: it has no standalone dispatch, writes, report,
or user-facing outcome. The consumer supplies the root and evidence, performs the reads and writes,
and continues its own workflow after applying the clauses.

Dependency edges augment the Markdown plan tree. Tree links express decomposition and remain the
authoritative work structure; dependencies express prerequisites. Do not create a second scheduling
database or change supertraverse's five-column progress table.

## S1. Resolve mode and the active stage graph

Read the root itself before consulting environment or defaults. The consumer declares one validation
context:

- **active** — resolve links in the authoritative vault. Every required root, plan, review, receipt,
  and record is readable and tracked on the authoritative branch; active validation is the only
  context that can authorize selection or execution.
- **candidate** — validate an unpublished scratch tree using an explicit one-to-one map from every
  intended vault path/link to its scratch path. Links must resolve through that map and the candidate
  graph/contracts must be complete. The review path may be reserved while the review is being
  produced; re-run candidate validation with the readable review draft and passing verdict before
  publication. A candidate result can authorize publication review, never execution, readiness, or
  integration claims. Missing, duplicate, or unmapped intended paths are **BLOCKED**.

- `**Planning mode:** upfront-v1` selects this contract. An upfront root carries these exact fields
  immediately below its title and before its progress table:

  ```markdown
  **Planning mode:** upfront-v1
  **Plan generation:** 1
  **Active replan:** none
  **Tree review:** [[reports/<review-file>]]
  ```

  `Plan generation` is a positive integer. `Active replan` is `none` or one unambiguous replan-record
  link. In active context that record is tracked; in candidate context it resolves through the scratch
  map. `Tree review` resolves to the review for the generation under validation (subject to the
  candidate review-production rule above).
- `**Planning mode:** incremental` selects the existing incremental contract and resolves the mode
  value as exactly `incremental`. The upfront-only root and stage fields are not required.
- A root with no Planning mode field is **legacy incremental**, regardless of the current value of
  `SUPER_PLANNING_MODE`; its resolved mode value is exactly `incremental`. Do not rewrite or
  auto-convert it.
- Any other marker, duplicate marker, malformed upfront field, missing referenced review, or missing
  or malformed active-replan record is **BLOCKED**. An active replan is a durable execution barrier.

For `upfront-v1`, walk active Plan links using supertraverse C1/C3. A linked node with a progress
table is a grouping node; a linked node without one is a stage leaf. Ignore historical predecessor,
repair, supersession, closeout, finding, and report links. Resolve the current path for every active
stage ID. A terminal row with an authorized `declined` / `deferred` / `out-of-scope` disposition is
not active work; every other declared active scope row must have a readable Plan link. Return to the
consumer a resolved mode, generation, active-replan value, review, ordered active stage map, and the
tree path for each stage. This is derived state, never an independently persisted scheduler graph.

## S2. Validate publication and stage contracts

An upfront graph is valid only when all checks below pass. Report every concrete fault and return
**BLOCKED**; do not repair a published graph by invoking incremental gap filling.

### Stage identity and graph

Every active leaf begins with exactly one of each field:

```markdown
**Stage ID:** S02
**Stage revision:** 1
**Stage kind:** implementation
**Depends on:** S01
**Preparation:** none
```

- Stage IDs use `S` plus digits, are unique in the active tree, survive renames and successor
  publication, and are never reused. Stage revision is a positive integer. Stage kind is exactly
  `implementation` or `discovery`. `Depends on` is `none` for an empty set or a list of active stage
  IDs. `Preparation` is `none` or one preparation-report link.
- Grouping sub-masters do not become executable stages. Active stage paths and Plan links are unique
  and readable. Missing links, duplicate IDs, self-dependencies, duplicate edges, unknown or retired
  dependency targets, cycles, and active work unreachable from the root are **BLOCKED**.
- A split or merge retires old IDs with an explicit replacement mapping and gives each replacement a
  fresh ID. Historical successors and repair plans are not dependency targets.
- Each consumed contract resolves to exactly one active provider and semantic revision. Its provider
  is in the consumer's declared dependency closure, and the provider's matching `Produces` entry is
  behaviorally compatible. Missing, ambiguous, or incompatible consumed contracts are **BLOCKED**.

### Required stage content

Every stage states all of the following:

1. Goal; scope in and out; a chosen approach; and the relevant components or currently known paths.
2. Acceptance IDs and conditions with the authoritative source revision, or explicit legacy-source
   requirements when no acceptance checklist exists. Acceptance ownership remains visible.
3. Dependencies plus `Consumes` and `Produces`. Cross-stage contracts have a stable contract ID, a
   positive semantic revision, provider stage ID, behavior, and constraints, including data/schema
   and ordering assumptions rather than only function signatures. Use this shape:

   ```markdown
   ### Consumes
   - C-INGEST@1 from S01: UTF-8 records with stable record IDs; malformed input is rejected.
   ### Produces
   - C-STORE@1: records are persisted atomically; duplicate IDs do not duplicate records.
   ```

4. Verification scenarios with distinguishing inputs, expected observations, and the evidence
   method. Scenarios must distinguish the commitment from its plausible wrong implementation.
5. Assumptions with evidence, bounded unresolved details, their resolution method, and invalidation
   triggers. Predicted predecessor filenames and signatures are predictions, not observed facts.
6. A task outline concrete enough to prepare for execution once predecessor evidence is available.

An upfront stage may defer predecessor-dependent internal filenames, helper names, exact future line
numbers, and complete test bodies when each unknown is bounded and has a stated resolution method.
It may not defer scope, architecture, acceptance, dependency ownership, shared contract behavior, or
the chosen approach. A mandated algorithm or signature remains binding when the source specifies it.
A discovery stage states its experiment, evidence, decision criteria, and downstream assumptions it
can invalidate; "decide later" is not a discovery contract. Unbounded foundational uncertainty makes
the upfront graph invalid.

Whole-tree publication also requires complete active-scope coverage, preserved acceptance ownership,
compatible interfaces and dependency order, no blank active Plan cells, and a passing review linked by
the root. Before publication, validate the complete candidate through its explicit path map. After the
single publication change, validate again in active context and require every artifact, including the
review, to be tracked. Candidate validity alone never satisfies that post-publication check. Contract
validity means the initiative is fully planned at contract maturity; it does not make an unprepared
stage executable.

## S3. Classify maturity and execution eligibility

Use evidence, not a row label, to classify each active stage:

- **contract-valid / needs refinement:** S2 passes but `Preparation: none`, the receipt is invalid, or
  relevant evidence has changed. The parent row is `PLAN WRITTEN — needs refinement`. The stage is
  not executable. Its next operation is `refine` under `PLAN_REFINER` when its dependencies provide
  the evidence preparation needs; otherwise it remains dependency-blocked.
- **prepared:** S2 passes and S5 verifies the preparation pointer, report, identity, and evidence.
  The parent row may be `PLAN WRITTEN — ready to execute`.
- **executed / integration pending:** verified closeout and an open or CI-pending code PR bound to
  the active stage identity prove that execution attempt already occurred, so do not prepare or
  execute it again. It is not done and does not satisfy consumers; retain its integration/CI
  recovery path. A published C8 successor with a different generation, plan path or revision and
  an explicit `resume-existing` mapping is a separate unstarted identity. Preserve its predecessor's
  PR, closeout and task history as non-delivered evidence while classifying the successor for fresh
  refinement. Do not infer the mapping from an open PR or row label alone.
- **executed/done:** C9 verifies integrated delivery or the authorized terminal disposition. Status
  text or a closeout alone is never integration proof.

A dependency is satisfied only by verified integrated delivery of the contract revision the consumer
names. For PR-based code, verify the provider PR is merged, its merge commit is in authoritative
`main`, the closeout is tracked, and the delivery evidence identifies the produced contract. For an
authorized direct/no-PR integration, verify the recorded integration commit in authoritative local
`main`, the tracked closeout, and the same contract-delivery evidence. An open, closed but unmerged,
blocked, or merely approved PR is unsatisfied. An authorized provider decline/defer closes
that provider obligation only; it does **not** prove delivery to a live consumer. The consumer remains
non-executable and the goal is not done until an adopted replan removes or replaces the dependency.
For discovery, explicit verified non-code evidence may satisfy the dependency when its contract says
so. Unknown, missing, or contradictory evidence is unsatisfied.

An upfront stage is executable only when all of these are true: S1/S2 pass; no active replan exists;
all dependencies are satisfied; S5 verifies a current `PREPARED` receipt; and the active stage
identity is unstarted and ready. A C8 `resume-existing` successor remains unstarted until its own
execution snapshot is captured, even when its predecessor has an open PR and partial closeout.
Failing any gate returns `executable: false` with the failed evidence. In
particular, a written leaf without a valid preparation receipt returns needs-refinement/BLOCKED to the
calling entry point; it never falls through to the legacy "written but incomplete" predicate.
Incremental and unmarked legacy roots continue to use their existing authoring, traversal, C8 repair,
execution, and C9 behavior without preparation metadata.

Already-running stages recover through the existing execution/CI workflow. Never overwrite their task
history with an in-place preparation. An unrelated code `HEAD` advance triggers a focused relevance
check; it does not automatically invalidate preparation. A relevant source, stage, predecessor,
contract, or finding change does invalidate it. Lost or contradictory evidence is **BLOCKED**.

## S4. Classify refinement versus structural replanning

Classify the evidence before selecting a role:

- `operation: refine`, `role: PLAN_REFINER` when the stage can keep its acceptance, scope boundaries,
  chosen approach, dependency edges, and shared contract semantics. Refinement may resolve bounded
  predecessor-dependent filenames, helpers, task ordering, test setup and executable task detail;
  update evidenced assumptions; and make verification steps actionable.
- `operation: replan`, `role: REPLANNER` when verified evidence requires changing any commitment:
  acceptance or source ownership, scope, foundational/chosen architecture, dependency topology,
  provider ownership, shared contract behavior or semantic revision, stage split/merge, or an active
  stage's required outcome. Missing architecture at initial publication is invalid under S2 rather
  than a routine refinement opportunity.
- Return **BLOCKED** when evidence needed to decide is absent or inconsistent. Do not guess under
  either role.

For replanning, use the originating stage and graph-derived transitive dependent closure as the
**initial assessment set**, not a cap. At every dependency boundary, compare the old and proposed
contract: revise a consumer only when its commitment or evidence changes; retain it with recorded
evidence when the consumed contract remains fulfillable. Stop propagation at a preserved contract.
Expand the semantic affected set with any stage outside the initial closure whose verified shared
foundational assumption, acceptance, approach, or contract is independently invalidated, and record
why each expansion occurred. A foundational change may therefore affect an otherwise independent
unfinished branch. Completed work stays completed; corrections become explicit new work with consumer
rewiring. Supersession never merges, closes, deletes, or forgives an old PR.

The impact assessment is a complete accounting, not just a list of files to rewrite. Record the root
generation and each active stage path/revision at assessment time, then assign every stage exactly one
disposition:

- `revise` when its acceptance, scope, approach, dependency, required outcome, consumed evidence, or
  produced contract must change and the stage is unfinished;
- `retain` when an unfinished stage lies outside the final semantic affected set and current evidence
  proves its approved boundary remains fulfillable; cite the preserved consumed/produced contract and
  why propagation stops there;
- `completed-history` when verified delivery evidence proves the stage is completed; preserve its
  plan, closeout, contracts and integration evidence, and record the effect on current consumers; or
- an authorized terminal disposition with the adopting authority and its effect on every consumer.

This accounts for the whole active graph without folding completed history into the retained unfinished
set. A local implementation detail that preserves all commitments stays refinement and does not create
a structural batch. A semantic change to a provider is not automatically a rewrite of every descendant:
propagate across each dependency edge only until an unchanged output contract makes the next consumer
valid. Classify as retained only stages outside the final semantic affected set, after all verified
independent shared-assumption expansions.

Do not revise delivered history in place. If completed work needs correction, keep its stage and
delivery evidence completed, assign fresh stage IDs to explicit corrective work, and rewire affected
consumers. A split or merge likewise requires a total old-ID to fresh-ID replacement mapping; retired
IDs are never reused or left as live dependency targets. For partially executed unmerged work, preserve
the predecessor plan, task history, PR/branch/worktree and closeout evidence. A successor states the
remaining tasks and an explicit verified `resume existing` or authorized `replace` integration
disposition. Replanning itself never closes, merges, deletes, or forgives that PR.

After a generation change, a revised stage always needs refinement. A retained preparation is current
only when a focused recorded revalidation proves the stage body/revision, source, relevant code,
consumed contracts, provider receipts, findings, and other S5 evidence unchanged and binds that result
to the new generation. Otherwise the retained stage is `needs refinement`; an old-generation receipt
alone is never current.

Legacy C8 single-leaf repair remains supported. An adopted repair is structural authoring under
`REPLANNER`, while its existing durable decision, predecessor, PR disposition, publication, and replay
rules remain binding.

## S5. Validate preparation receipts and revisions

A preparation report is durable, tracked evidence and records at least:

- outcome `PREPARED`;
- root path and Plan generation;
- Stage ID and Stage revision;
- lowercase SHA-256 digest of the prepared stage plan;
- code commit examined during preparation;
- authoritative source agreement and revision;
- every consumed contract ID/revision and provider delivery receipt;
- relevant findings and their revisions;
- preparation amendments (or explicit `none`).

Its amendment metadata distinguishes three evidence states; do not collapse them into a generic
"updated" note:

- `none` — initial preparation attached a receipt but made no plan-body amendment. The Stage revision
  is unchanged.
- `content-amendment` — preparation changed bounded executable detail in the stage body while S4's
  commitments survived. List the evidence-grounded details and increment Stage revision.
- `compatible-baseline-revalidation` — a focused comparison after an unrelated baseline/HEAD advance
  found the stage, source, code, predecessors, contracts, and findings compatible. Link the prior
  receipt and the new validation receipt; preserve Stage revision. It is not a silent reuse of old
  evidence.

This metadata is part of the receipt evidence. A report that cannot tell a content amendment from a
compatible baseline revalidation is incomplete and therefore not a current PREPARED receipt.

Compute the digest over the exact UTF-8 bytes of the whole stage plan after omitting the one complete
`**Preparation:** ...` metadata line, including that line's newline when present. Do not normalize
other bytes or omit any other field. Excluding only the pointer prevents a circular digest; the digest
proves identity, not semantic correctness.

To validate an active receipt, resolve the stage's sole Preparation link and require a tracked readable
report with `PREPARED`. During preparation publication, a consumer may validate the candidate stage
and report through S1's explicit intended-vault-path-to-scratch-path map; candidate receipt validity
can authorize the atomic publication only and never execution. After publication, revalidate in active
context before marking or selecting the stage as ready. Recompute the digest and match root generation, stage ID/revision, source revision,
consumed contract revisions, provider receipts, code baseline, findings, and amendments against current
evidence. Reapply S1/S2 plus S3's active-replan, dependency-delivery, active-identity/unstarted, and
evidence predicates; do not recursively invoke S3's preparation-receipt classification. For a C8
`resume-existing` successor, verify its published predecessor mapping and distinct identity, keep
the predecessor PR/closeout historical, and require this successor's own generation-bound receipt;
the predecessor's receipt, reviews and CI do not transfer. A row's readiness text,
an approved disposition, or the existence of a report without these matches is insufficient. Any
mismatch makes the stage unprepared; missing or contradictory evidence is **BLOCKED** rather than
guessed.

Stage IDs remain stable across rename and revision. Increment the Stage revision when preparation or
replanning changes stage content; changing only the Preparation pointer does not increment it because
the pointer is receipt attachment, not plan semantics. Increment a contract's semantic revision only
when its behavior or constraints change, then assess consumers under S4. Refinement that preserves
commitments does not advance root Plan generation. Only publication of an adopted structural replan
advances that generation.

When a focused check finds an unrelated baseline advance compatible, record a refreshed validation
receipt tied to the new baseline; do not silently edit the old evidence. When current stage content or
relevant evidence changes, clear readiness, require a new preparation report, and preserve old receipts
as history. A retained preparation may cross a new root generation only when a recorded revalidation
proves the stage, consumed contracts, and all relevant evidence unchanged.

Compare the code, source, dependency, contract, and finding evidence since the recorded baseline; do
not require raw repository `HEAD` equality. In an internal vault, the preparation publication's own
goal-document commit necessarily advances `HEAD`. That docs-only advance may retain the examined code
baseline when the focused check finds no relevant code, source, predecessor, contract, or stage change;
it must not trigger an endless receipt refresh cycle.
