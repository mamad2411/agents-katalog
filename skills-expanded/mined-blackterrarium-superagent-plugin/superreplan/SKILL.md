---
name: superreplan
description: Use when an adopted repair must revise an upfront-v1 stage generation or publish a legacy C8 single-leaf successor from durable decision evidence.
license: MIT
related skills: superstage, superauthor, supertraverse, superplan
---

# Superreplan

`superreplan <root> <record>` is the docs-only repair author for one adopted C8 decision. For an
`upfront-v1` root it assesses and publishes one reviewed replacement generation. For an incremental
or unmarked root it preserves C8's single-leaf successor behavior. It never executes code or treats
unadopted evidence as authority to change commitments.

The dispatching controller assigns `REPLANNER` and its model/effort. A standalone invocation runs
under the current session and must say that it cannot change its own model pin. Author and self-review
directly: do not dispatch children, invoke an author/refiner/replanner, call superplan as another
skill, or consume a second heavy operation. The controller counts this as its one heavy skill for the
tick. Apply superauthor A1–A8 and supertraverse C8 inline, with the repair-specific routing and report
below.

## Resolve the durable request

Require an absolute root-plan path and durable record path. Do not infer either from the working
directory or a loop log. Resolve the root through superstage S1 in **active** context and reconcile
the record through supertraverse C8 before authoring. Read the adopted authority and rationale,
triggering evidence/finding, source agreement/revision, from-generation, code/vault baselines,
originating stages, candidate dependency closure, active paths/revisions, PR/branch/worktree state,
draft/successor paths, ID mappings, resolution, and publication evidence.

Return **BLOCKED** for absent or ambiguous authority; a missing/malformed referenced record;
duplicate live records claiming one Decision ID; divergent successors; a record for another
root/generation; contradictory source, Git, PR, or worktree evidence; multiple active batches; or a
dirty/partial state that cannot be reconciled uniquely. Repeated Decision-ID markers in the request,
checkpoint, publication, and evidence-resolution history are expected and are not duplicate live
records. Never manufacture a request from an informal prompt. An authorized source or acceptance
change remains bound to its adopting authority; replanning cannot silently weaken or reinterpret the
approved agreement.

## Label every constraint by origin

Guarding acceptance against weakening is half the rule; the other half is not inventing authority.
Every restriction a successor or replacement stage states — a ban, a budget, a required order, an
excluded evidence source — carries one origin tag where it is written:

- `[source: <cited project document or protected surface>]`;
- `[owner: <Decision ID or recorded answer>]`;
- `[planner]` — added by this replan, or by an earlier planner, refiner or replanner, on its own
  judgment.

Re-derive the tag for every restriction you carry forward. One you cannot trace to a cited source or a
recorded owner answer is `[planner]`, whatever an earlier generation called it. Then:

- Never carry a `[planner]` constraint forward as if it were `[owner]`, and never describe it as a
  limit only the owner can lift.
- Never add a constraint that forbids the fix the request's own evidence points to. If the evidence
  quotes a step hitting a configured timeout, the successor addresses that limit — or, when the limit
  is a protected surface, says so and leaves the owner question to the ladder — and never bans
  raising it.
- Diagnostic budgets (attempt counts, evidence lanes, observation passes) are always `[planner]`.
  Exhausting one produces a cap summary (superbuild B5), not an owner pause.
- A `[planner]` constraint may later be relaxed by an executor B5 ruling or by the L7 panel without
  the owner, ledgered with its reason. `[source]` and `[owner]` constraints cannot be relaxed that
  way.
- A directive that arrives with the request from the L7 panel — an analysis to run, an artifact to
  build, an approach to take — is `[planner]`, not owner authority. You may set it aside with a
  recorded reason, and you must when it adds deliverables, analyses or proofs outside the stage's
  acceptance and scope.

## Prefer the smallest unblocking change

"Cannot silently weaken" means **ask**, not **avoid**. When a stage cannot meet an acceptance case as
written, list these remedies in this order in the request record and in your report, and state for
each why it does or does not apply:

1. **Test-scoped substitute** inside the stage's own test seams — a fixture, a stub, a test-registered
   provider result. It applies only when the case's acceptance text does not itself require the real
   provider or an end-to-end path; when it does, a substitute changes acceptance and is remedy 2. No
   owner approval is needed unless a `[source]` or `[owner]` rule forbids it. A
   rule against caller-supplied results on a public interface protects production callers; it does
   not by itself forbid a test-registered result, but say so explicitly when you rely on that reading.
   It lives only in tests: never in a production path, never through a public interface that refuses
   caller-supplied results. The successor records it as a **limitation** that the stage's closeout
   must carry, and it is never end-to-end evidence.
2. **Narrow the case** to inputs the delivered providers support. This changes acceptance, so it is a
   yes/no owner question (superloop L7 protected-change shape, with the recommendation first).
3. **Postpone the case** to a named later stage or goal that owns the missing capability. Also a
   yes/no owner question. (Distinct from declining or deferring the whole step, which is the
   escalation ladder's decline/defer option.)
4. **Change an upstream provider** — a new or corrective stage, never work inside this stage.
5. **New research or proof work** — only when 1–4 are each shown not to apply.

**A genuine gap is not a remedy 4–5 problem.** When the case turns on a reading the sources leave open
and remedies 1–3 do not apply, return **BLOCKED** naming the gap, the acceptance case that depends on
it, and two to four candidate values with a recommendation. Never take remedy 4 or 5 to settle a
specification gap.

Take the first remedy that applies. When it is remedy 1, publish the successor with the substitute
and its limitation. When it is 2 (narrow) or 3 (postpone), do not choose a costlier route to avoid asking: return
**BLOCKED** with that remedy named as the recommended owner question, and the remedies list attached
so the ladder can put it to the owner as a yes/no question. A replan that ends BLOCKED for any reason
includes the list.

Reconcile before drafting:

- A pending record with one unique scratch batch resumes those paths and the same stable Decision ID.
- A published record whose generation, active tree, cleared barrier, marker, and unique A7 history
  agree is already published. Return the active result and repair stale loop hints; do not republish.
- A relevant source, code, vault, active-path, contract, finding, PR, or worktree baseline change
  requires a fresh S4 assessment and recorded update before publication.
- A missing record, mismatched/multiple publication, or divergent candidate is **BLOCKED**.

Only authoritative committed/integrated files count. Ignore dirty working-tree edits that appear to
clear `Active replan` or expose successors. An internal docs branch/open PR is a candidate until it is
merged to authoritative main; an external-vault batch is a candidate until committed on the
authoritative branch. Keep execution paused while the committed root still names the pending record.

## Upfront-v1 impact assessment

For `upfront-v1`, require the root's `Active replan` to point to this pending record and its Plan
generation to equal the record's from-generation. Read the complete S1 active map and apply S2 to the
committed current generation. The active barrier intentionally prevents execution; it does not waive
graph validation or authorize incremental gap filling.

Apply superstage S4 from every originating stage through the graph-derived transitive dependent
closure as the initial assessment set. Compare old and proposed contract behavior at every edge, then
expand the final semantic affected set with any independently invalidated stage outside that closure
and record the evidence/reason for each expansion. Replace the request record's pending final-set,
expansion-reason, and per-stage disposition fields with this assessment before candidate review or
publication. Give every stage one disposition in the record:

- `revise` for unfinished affected work, with the evidence and exact
  acceptance/scope/approach/edge/contract/outcome change;
- `retain` for unfinished work outside the final semantic affected set, with evidence that its
  boundary remains fulfillable, including the contract where impact propagation stops;
- `completed-history` for delivered work, with verified delivery/integration evidence, preserved
  plan/closeout/contracts, and its effect on current consumers; or
- an authorized terminal disposition and its effect on every consumer.

Do not include completed-history stages in the retained unfinished set. A local file/helper/test-detail
change that preserves commitments belongs to superrefine and creates no batch; report that mismatch
instead of structurally rewriting it. A changed provider interface does not imply rewriting every
descendant: stop at the first output contract whose behavior/revision remains valid. Conversely,
expand beyond the graph closure when shared foundational evidence invalidates an otherwise independent
unfinished branch.

Preserve delivered stages and their history. If delivered behavior needs correction, add fresh stage
IDs for corrective work and rewire consumers; do not reopen or rewrite the completed stage. A split or
merge requires a total explicit old-ID to fresh-ID mapping, no reused retired ID, and no remaining
active dependency on a retired ID. For partially executed unmerged work, preserve the old plan,
closeout/task history, PR/branch/worktree and completed evidence. The replacement states remaining
tasks and records either verified reuse with repeated review/tests or an authorized replacement
disposition. This skill does not merge, close, delete, or forgive the predecessor PR.

## Draft the replacement generation

Draft outside active navigation. Use unique scratch paths and an explicit S1 intended-vault-path map.
Do not change any active Plan link while drafting. Author directly under superauthor A2/A3:

1. For each `revise` stage, write a replacement stage contract at the maturity required by S2. Keep
   the stable stage ID and increment Stage revision unless an authorized split/merge/correction
   retires it for mapped fresh IDs. Set `Preparation: none`; revised leaves require later refinement.
2. Write grouping/root candidates with all authorized Plan-link, dependency, contract, status, and
   retired-ID mapping changes. Preserve completed rows, their closeouts, accepted dispositions, and
   unrelated history. A retained stage file stays byte-identical except for its sole `Preparation`
   pointer to a recorded proposed-generation revalidation; readiness status changes belong in its
   parent row. Any other leaf-content change is a `revise` disposition, increments Stage revision,
   and requires a new receipt after later refinement.
3. Revalidate retained preparations for the proposed generation through S5. Preserve readiness only
   with a focused recorded revalidation proving the stage body/revision, source, relevant code,
   consumed contracts, provider receipts, findings, and other evidence unchanged. Otherwise set the
   stage to `PLAN WRITTEN — needs refinement`; an old-generation receipt alone is insufficient.
4. Write one new whole-tree review report for the proposed generation. It covers revised and retained
   stages, source/acceptance ownership, full scope, S4 dispositions, compatible interfaces,
   dependency order, topology mappings, completed/partial history, and preparation validity.

Checkpoint interruption state in the same pending record: unique draft paths, intended vault paths,
completed assessment/review items, and outstanding work. A checkpoint keeps `Resolution: pending`,
the old generation, and the Active replan barrier; publish that record-only checkpoint through A7 if
durability is needed. Never expose an individual draft through an active link or mark it ready.

## Review the whole candidate

Self-review directly under superauthor A4; do not dispatch a reviewer. Re-run superstage S2 in
**candidate** context against the complete proposed tree, including retained stages, through the
explicit path map. Require all of the following before publication:

1. Every stage has exactly one evidenced `revise`, `retain`, `completed-history`, or authorized
   terminal disposition; completed stages are reported separately from retained unfinished stages,
   every expansion beyond the initial graph closure is justified, and each propagation stop cites a
   preserved contract.
2. The candidate preserves delivered work and acceptance/source authority. Corrective work,
   split/merge mappings, consumer rewiring, and partial-PR dispositions are complete.
3. Every revised stage is contract-valid with `Preparation: none`; every retained ready stage has a
   generation-bound S5 revalidation. No draft successor is reachable from the committed old tree.
4. The new whole-tree review passes and S2 validates every candidate path, ID, edge, contract, and
   active obligation. Revalidate request baselines immediately before publication; relevant drift
   returns to assessment.
5. Every restriction in a revised stage carries an origin tag; none tagged `[planner]` is presented
   as owner authority; and none forbids the fix the request's evidence points to.
6. When an acceptance case could not be met as written, the remedies list is present, the first
   applicable remedy was taken or named, no remedy 4–5 work was added while 1–3 applied, and a
   genuine specification gap was returned with candidate values rather than worked around.

A candidate failure stays in scratch/pending state. Do not publish a partial batch, clear the barrier,
or claim readiness.

## Publish one generation

Use superauthor A6/A7 to publish one complete tracked change containing all replacement/new stages;
all grouping/root active-link and dependency edits; total retired-ID mappings; any retained
preparation revalidation receipts/statuses; the new whole-tree review; and the record's final
per-stage dispositions, successor paths, `Resolution: published`, and published generation. Increment
the root generation exactly once, point `Tree review` to the new report, and set `Active replan: none`
in that same change. Preserve every superseded plan, finding, closeout, receipt, and PR reference.

Use the stable Decision ID as the **publication decision marker** in the record and A7 commit/PR
description. Do not require the record to contain its own commit hash. Its resolved publication
PR/commit field may say `pending resolution from <Decision ID> marker and tracked artifact set` in the
containing change; after integration, reconciliation locates exactly one publishing commit from Git
history and a later report/record update may store the resolved evidence.

A file write is not publication. For an internal vault under protected-main A7, merge the complete
docs PR to authoritative main and synchronize it before activation. When A7 permits a direct internal
commit, or for an external vault, commit the complete batch on the configured authoritative branch
and verify that commit there. Then re-run S1/S2 in **active** context and reconcile the marker,
generation, record, review, links, and cleared barrier from authoritative committed history. Until all
checks pass, the old pending generation remains the only authoritative active view, and it is
non-executable under the pending barrier. Require exactly one history change that performs the
complete old-to-new publication transition. Request, checkpoint, or later evidence-resolution commits
may repeat the Decision ID and do not count as publications. A mixed tree, multiple matching
publication transitions, mismatched generation, or missing artifact is **BLOCKED**.

After verified publication, repair stale loop recovery hints to the published generation. Do not run
or refine a stage in this authoring invocation. A crash before loop update resumes the verified new
tree without another publication.

## Incremental/legacy single-leaf wrapper

For an incremental or unmarked root, require a valid legacy C8 record and one `repair requested` row.
Apply supertraverse C8's legacy publication, superauthor A2/A3/A6/A7, and superplan's legacy
self-review, routing, parent-row, and reporting clauses directly. Do not invoke superplan or add
upfront generation, stage-ID, preparation, or batch fields.

Write one fresh implementation leaf with `Supersedes` and `Repair` links, authorized corrections,
remaining work, regression checks, and the explicit predecessor PR/worktree disposition. Preserve the
predecessor and completed evidence. Atomically publish the successor link, legacy record fields, row
status/PR/comments, and history under C8. Replays reuse the Decision ID and unique successor; missing,
divergent, or partial evidence is **BLOCKED**. This wrapper changes the authoring role to REPLANNER but
does not change legacy tree shape, source agreement, integration duties, or C9 completion rules.

## Report

Return exactly this shape, using `none` for absent values and listing every file changed:

```text
**Outcome:** PUBLISHED | ALREADY-PUBLISHED | REFINEMENT-ONLY | BLOCKED
**Root plan:** <path>
**Decision ID:** <id>
**Record:** <path>
**From generation:** <integer or none>
**Published generation:** <integer or none>
**Revised stages:** <ids or none>
**Retained stages:** <ids or none>
**Completed stages:** <ids or none>
**Retired/replacement mapping:** <mapping or none>
**Review:** <path or none>
**Predecessor PR dispositions:** <entries or none>
**Files changed:** <explicit paths or none>
**Integration:** <merged docs PR, authoritative vault commit, or none>
**Publication marker:** <Decision ID or none>
**Resolved publication evidence:** <PR/commit or pending marker reconciliation>
**Remedies considered:** <for each acceptance case not met as written: remedy 1–5 — applies / does not (why); the one taken or recommended; for a genuine gap, the candidate values and the recommendation — or none>
```
