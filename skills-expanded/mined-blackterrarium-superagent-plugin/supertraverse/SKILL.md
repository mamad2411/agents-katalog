---
name: supertraverse
description: Use when traversing a tree of seed/master/implementation plans — descending a progress-report table's Plan links to find the next task (planning mode = next available task to plan; execution mode = next written-but-unexecuted leaf plan), or ascending from a leaf plan to the root updating ancestor statuses. Shared by superplan, superrun, and superfinish.
license: MIT
---

# Supertraverse

The single source of truth for **plan-tree navigation**. A goal folder's plans form a tree: a
seed/master plan's **progress-report table** lists its steps, each step's `Plan` link points *down*
to that step's child plan, and every plan carries a parent-seed reference pointing *up*. This skill
defines how to walk that tree — **down** (descent: find the next available task to plan) and **up**
(ascent: update ancestor statuses) — plus the schema, link-inference, and status vocabulary the walk
depends on.

**Consumers:** `superplan` invokes this for **descent** (to find the task to plan) and **ascent in
planning mode** (to mark ancestors in-progress). `superrun` invokes execution descent. `superfinish`
invokes **ascent in completion mode** (to flip ancestors complete). Upfront consumers also invoke
`superstage` and apply S1–S3 before acting on traversal. These skills are the only places these
mechanics are defined — consumer skills must not restate or fork them.

This skill **describes algorithms the calling agent carries out inline** with its file tools (Read /
Edit). It does not itself write source code, run anything, or commit. The consumer skill owns reading
the result, writing files, and committing.

> **Subroutine contract — read before running the algorithm.** When `superplan`, `superrun`, or
> `superfinish` invokes this skill via the Skill tool, you (the calling agent) are running
> supertraverse as **one step inside the caller's workflow**, not as a standalone task. After you
> compute the algorithm's result (target + path, `none`, `not-traversable`, or the list of touched
> ancestor files), you **MUST return control to the calling skill and immediately continue executing
> the caller's next section** — do NOT end your turn, do NOT wait for user input, do NOT print a
> "supertraverse complete" report. supertraverse has no Final Report of its own; the caller writes
> the only user-facing report.

## C1. The progress-report table schema

A seed/master/sub-master plan carries a progress-report table with these columns:

```
| Step | Status | Plan | PR | Comments |
|------|--------|------|----|----------|
```

- **Step** — the name of the step.
- **Status** — the step's purpose + state, drawn from the **status vocabulary** (C2).
- **Plan** — a vault wikilink to the plan generated for this step: **either** a child master/seed plan
  (an *internal node* — itself carries a progress-report table) **or** an implementation plan (a *leaf*
  — carries no table). **Blank when no plan exists yet** — a blank `Plan` on a not-completed row is
  what marks an ordinary step an *available task to plan*. C8 repair requests are also eligible.
- **PR** — one or more pull requests associated with the step.
- **Comments** — notes; for a completed step, a one-line close-out summary plus a
  `Closeout: [[…reports/…]]` link. The plan link lives in the **Plan** column, **not** here.

**Leaf rule (load-bearing):** an implementation plan is a tree **leaf** and **MUST NOT contain a
progress-report table**. The table's presence is precisely what marks a plan as an *internal node*
that descent recurses into; a leaf has no children, so no table. (Implementation plans track their own
work with task checkboxes / a verification matrix — never a progress-report table.)

**Recognizing a progress-report table (vs. an orchestration table).** A plan may contain several
tables; only one tracks *progress*. A **progress-report table** has a **Status** column (or
status-like state in its cells) **and/or** carries per-step **Plan** / `Plan: [[…]]` / `Closeout: [[…]]`
links — i.e. it records both *which step* and *how far along*. A table that only describes
*granularity*, *dispatch*, or *sequencing* — columns such as `Granularity`, `Action required`,
`Session`, `Why split`, or a gate/verdict matrix — with **no** status/plan/closeout signal is **not** a
progress-report table: it has no down-links to follow and no completion state to read. Do not walk it
as one. A plan whose only step-tracking structure is such an orchestration table (and which has no
step-tracking bullet list either) is **not traversable** — see C6.

## C2. Status vocabulary (shared)

Use these exact spellings; both consumer skills depend on them:

- `incomplete` — not started.
- `in progress (planning underway)` — a descendant of this step now has a plan, but **no descendant has executed yet** (set by planning-mode ascent).
- `in progress (partially executed)` — at least one descendant row has reached a closed state
  (`completed-and-merged` / `done` / `completed-local` / `executed — PR open` / `deferred` /
  `declined` / `out-of-scope`),
  at least one other is still `incomplete`, `PLAN WRITTEN — needs refinement`,
  `PLAN WRITTEN — ready to execute`, or
  `in progress (planning underway)` (set by completion-mode ascent on partial ancestors). The
  parenthetical accurately describes the state: execution has started but is not finished.
- `PLAN WRITTEN — needs refinement` — an upfront stage contract exists but has no current verified
  preparation receipt. It is planned, unexecuted, and not an execution target.
- `PLAN WRITTEN — ready to execute` — this step's *own* plan exists but is not executed (set by
  legacy superplan or by successful upfront preparation on the immediate-parent row).
- `executed — PR open` — this step's plan ran end-to-end and a closeout report exists, but the code
  PR has not yet been squash-merged to `main` (set by completion-mode ascent / superfinish when the
  code PR is still open). A follow-up superfinish (or manual update) flips this to
  `completed-and-merged` once the code is on `main`.
- `deferred` / `declined` / `out-of-scope` — intentionally not pursued; **non-blocking** for the
  "all children merged-on-main" check in completion-mode ascent.
- `completed-and-merged` / `done` — closed, code on `main` (set by completion-mode ascent /
  superfinish when the code PR has been merged).
- `completed-local` — closed only for a `SUPER_GIT_MODE=none` goal after a validated local receipt;
  it is never merge evidence in `github`.

**State-progression invariant.** A row only ever moves "rightward" along the lifecycle:

```
incomplete  →  in progress (planning underway)  →  PLAN WRITTEN — needs refinement
                                                →  PLAN WRITTEN — ready to execute
            →  in progress (partially executed)  (only at internal nodes — leaves skip this)
            →  executed — PR open  →  completed-and-merged
            →  completed-local                 (local mode only)
```

`deferred` / `declined` / `out-of-scope` are terminal off-ramps available from any earlier state.
Both ascents are forbidden from downgrading a row to a state earlier in this sequence.
Superstage S5 invalidation is the one readiness correction: an **unstarted** upfront row whose receipt
or relevant evidence no longer validates moves from `PLAN WRITTEN — ready to execute` back to
`PLAN WRITTEN — needs refinement`, preserving the old receipt as history. Never apply that correction
to a running or completed stage; those retain their execution/closeout history and use recovery or
explicit corrective work.
**Authorized repair is a separate transition (C8):** `repair requested` marks an adopted
repair awaiting a successor plan. C8 alone may reopen the affected row and ancestors;
ordinary ascent never does. `repair requested` is neither closed nor merged-on-main.

## C3. Inferring a row's child-plan link (legacy-compatible — REQUIRED)

Tables do **not** need a `Plan` column — every progress-report table in the vault today predates it
and records the child-plan link inside the **Comments** cell. To find a row's child-plan link, try in
order:

1. If a dedicated **Plan** column exists and its cell is non-empty → use that link.
2. Else scan the row's cells (the **Comments** cell especially) for a `Plan: [[<link>]]` marker — the
   convention current superplan writes — and use that link.
3. Else scan the row for any wikilink / relative path into a `master-plans/` or `plans/` subfolder (a
   `.md` plan file) and use it.
4. Else look **outside the table row**, elsewhere in the same plan, for prose tied to this step — a
   section heading that names the step (e.g. `### Sub-PR #2 …`) or a callout/blockquote under it such
   as `> **Detailed step-level plan:** [[…]]` — and scan that for a child-plan link by the same rules.
   (Older plans summarise steps in a table but embed each step's plan link in a per-step section, not
   the table cell.)
5. If none found → the row has **no child plan** (treat as blank). A broken or missing link is also
   treated as blank — a dangling link must **never** silently halt traversal.

In every case **ignore** `Repair:`, `Previous plan:`, `Supersedes:` and `Historical closeout:`
links (and links inside the repair record); these are history, never active child plans.
Also ignore links into `reports/` (closeouts) and `findings/`, and ignore PR refs
(`#NNN`, GitHub URLs) — those are not child plans.

## C4. Detecting closed rows & the leaf/internal test

Two predicates — used at different points in the walk. The distinction matters because
`executed — PR open` rows are *past consideration* for descent (the work is done) but **not yet
merged on `main`** for the completion-mode parent-flip check.

Apply the **repair override first**: a `repair requested` row with its adopted C8 record
is open for planning regardless of old Plan/Closeout links or a predecessor banner.
A missing/invalid repair record is BLOCKED, never permission to execute the old plan.
Status matching below means affirmative state in the Status cell, not substrings in
comments (`not merged` is not `merged`). A closeout proves an attempt ended, not integration.
These status predicates control navigation only. They never prove integration or satisfy an upfront
dependency: superstage S3 and C9 require the underlying PR/commit, closeout, contract-delivery, and
disposition evidence. In particular, an approved provider decline/defer is not evidence that its
live consumer received the contract.

- **Closed-for-descent row** (descent skip rule, C6): its **Status** text contains any of
  `completed-and-merged` / `done` / `merged` / `shipped` / `closed-out` / `executed — PR open` /
  `deferred` / `declined` / `out-of-scope`, **or** the row carries a `Closeout: [[…reports/…]]`
  link. Skip these rows during descent — the work is past consideration for both planning and
  execution targets. (Shipped seed rows commonly carry both signals.)
  In effective mode `none`, a `completed-local` row is closed only after validating its receipt.
  In effective mode `github`, it is neither closed nor integrated and must be reported BLOCKED.
- **Merged-on-`main` row** (completion-mode "all children done" check, C7): its **Status** text
  contains `completed-and-merged` / `done` / `merged` / `shipped` / `closed-out` (i.e. the code is
  on `main`). `deferred` / `declined` / `out-of-scope` rows count as merged-on-`main` for this
  check ("done for our purposes"). **`executed — PR open` does NOT count** — the code is not yet on
  `main`, so the parent cannot yet be flipped to `completed-and-merged`.
- **Leaf vs internal:** read the plan the row's `Plan` link resolves to (C3) — if it **contains a
  progress-report table** (per C1's recognition test — an orchestration table does **not** count) it
  is an **internal node** (descend into it); if it **does not**, it is a **leaf** (an already-planned
  implementation plan; skip it).

## C5. Parent chaining (the "up" links)

Every plan superplan writes carries an explicit **parent-seed reference** near its top — a wikilink to
the plan it was derived from. Ascent follows these references upward:

```
leaf plan → immediate parent → … → root
```

The **root** is the plan with **no** parent-seed reference (the top of the initiative). Parent chaining
is the inverse of the `Plan`-column "down" links: descent walks down `Plan` links; ascent walks up
parent-seed references.

## C6. DESCENT — find the deepest target row (mode-parameterized)

**Input:** a root plan file and a **mode** — `planning` (default) or `execution`. First invoke
`superstage` and apply S1 in **active** context:

- For an explicit incremental or unmarked legacy root, preserve the C1–C9 algorithm below exactly;
  current environment defaults do not change it.
- For `upfront-v1`, apply S2 to the complete active graph before selecting anything. Invalid metadata,
  links, stage IDs/contracts, dependency cycles, unreachable work, incomplete coverage, or a bad tree
  review returns **BLOCKED**. A blank Plan cell in active upfront scope is a broken publication, never
  an incremental planning target. An active replan also blocks selection.
- **Upfront selection recipe:** after S1/S2 validate the active graph and no replan barrier exists,
  walk active leaves in priority DFS order. Skip a
  closed stage only with S3/C9 verified integration or authorized terminal-disposition evidence;
  never trust a row label or closeout alone. Require S3 delivery evidence for every prerequisite.
  An unsatisfied dependency makes that leaf ineligible, but does not stop the walk: continue to a
  later independent eligible stage.

  For each dependency-eligible unstarted leaf, apply S5 directly. A missing receipt returns
  **`NEEDS-REFINEMENT`** with root, stage ID/path, and the missing evidence; neither `superplan` nor
  `superrun` edits or executes it under the wrong role. A receipt whose only possible change is an
  unrelated code baseline/HEAD advance returns **`NEEDS-REFINEMENT`** marked *bounded
  revalidation*, so PLAN_REFINER records a fresh compatible validation receipt. A source, stage,
  predecessor, contract, or finding mismatch is **`REPLAN-REQUIRED`** with its evidence and affected
  stage; it must enter the decision/replanning path rather than being repaired during selection.
  Missing or contradictory evidence is **BLOCKED**. The first valid prepared eligible leaf is an
  execution target in execution mode; planning mode skips it. If no executable target exists while
  active work still has unsatisfied dependencies, return **BLOCKED** with the incomplete dependency
  evidence, never `none`/DONE.

Descent is one
pre-order DFS whose *target predicate* is selected by mode (symmetric with C7's `planning` /
`completion` ascent modes); everything else — the DFS walk, C1 schema, C3 link inference, C4
leaf/internal + completed-row tests, and `not-traversable` root handling — is shared.

- **planning mode** (consumer: `superplan`) finds **the deepest available task *to plan*** — the
  first not-done row with **no** child plan. **Output:** the **target row** plus the **descent
  path** — the ordered chain of `(plan-file, row)` from the root down to the **immediate parent**
  (the deepest plan that *directly contains* the target row), which planning-mode ascent (C7)
  consumes.
- **execution mode** (consumer: `superrun`) finds **the deepest written-but-unexecuted leaf plan
  *to execute*** — the first not-done row whose child plan is a leaf that is itself incomplete.
  **Output:** the **target leaf plan file path** (no descent path is needed — superrun does no
  planning-mode ascent; `superfinish` performs completion-mode ascent later via parent-seed
  chaining, C5/C7).

For upfront roots, both modes may return **`none`** only when all active obligations are resolved,
**`NEEDS-REFINEMENT`** for the first
dependency-eligible unprepared/stale stage, **`REPLAN-REQUIRED`** for a relevant broken assumption,
**BLOCKED** for incomplete dependency evidence, or an eligible prepared execution target.
Incremental traversal continues to return **BLOCKED** for invalid repair state, **`none`** when no
target exists, and **`not-traversable`** when the root is not a progress-report tree.

Pre-order DFS, honoring priority order (top-to-bottom = highest rank first):

0. At the root plan, **identify its progress-report table** using C1's recognition test. If the root
   has **no** progress-report table — only orchestration tables (granularity / dispatch / gate
   matrices) and no step-tracking bullet list — it is **not traversable**: return
   **`not-traversable`** (distinct from "none") so the caller can report that the root is not
   maintained as a progress-report tree, rather than guess a stale target from an orchestration table.
   For an upfront root this condition is BLOCKED under S2. For an incremental root, the
   `not-traversable` outcome only arises at the **root**: a child is only descended into when
   C4's leaf/internal test already confirmed it carries a progress-report table; a node reached via a
   `Plan` link that turns out to lack one is a **leaf**, skipped, not an error.
1. Walk that progress-report table's rows top to bottom.
2. For each row, first handle `repair requested` per C8: **planning → target this row**,
   **execution → skip** (the predecessor is not executable again). Validate its repair record;
   if absent/inconsistent return BLOCKED with the row and reason. For an upfront root, apply S3 and
   C9 evidence before skipping a leaf or subtree as completed; status text alone does not short-circuit
   that check. For an incremental root, **skip** a closed-for-descent row (C4). Otherwise apply the
   mode's per-row rule; the S3 upfront leaf rule above precedes the legacy completeness predicate:
   - **planning mode:** if the row has **no child-plan link** (C3) → **this is the target.** Stop.
     (The first not-done row with no child plan, in DFS order, is the highest-priority unplanned
     task.) If it links to a plan, apply the leaf/internal test (C4): **internal → recurse into
     that plan** (descend); **leaf → skip** (already planned) and continue to the next row.
   - **execution mode:** if the row has **no child-plan link** (C3) → **skip** (nothing is written
     to execute yet — that is a planning gap for `superplan`, not an execution target). If it links
     to a plan, apply the leaf/internal test (C4): **internal → recurse into that plan** (descend);
     **leaf →** check the leaf's completeness (see completeness note below): **incomplete leaf →
     this is the target.** Stop. **complete leaf → skip** and continue to the next row.
3. A recursion that returns a target propagates it straight up, unchanged (priority preserved).
4. If no row at a node yields a target, that node is fully resolved for the mode → return **"none"**
   to the caller.
5. If the root returns "none", **no target exists for this mode** — the caller reports this and exits.
   (planning: nothing left to plan; execution: no incomplete implementation plan to run.)

**Completeness note (execution mode only).** A leaf plan is **complete enough to skip from
execution** when **either** its parent row reads as a closed-for-descent status (C4 — including
`executed — PR open`, since the work has been executed even if the code is not yet on `main`) **or**
the leaf plan file's opening blockquote carries a closeout banner (e.g.
`✅ CLOSED OUT … IMPLEMENTED, CI-GREEN & MERGED`). A leaf whose row is
`PLAN WRITTEN — ready to execute` and whose file shows no closeout banner is **incomplete** — the
execution target. Reading the leaf's own banner (not the row alone) handles the idempotent case
where a plan was executed but its parent row was not yet flipped, so a re-run does not re-execute
finished work.

**Bullet-list node** (a plan that tracks steps as a bullet list, not a table): treat each bullet as a
row and apply the mode's per-row rule (step 2) to it, inferring each bullet's child-plan link from its
text by the same C3 rule. Prefer the progress-report table where both a table and a list exist.

**In planning mode**, record the descent path as you go — the planning-mode ascent (C7) consumes it.
The **immediate parent** is the last (deepest) plan in the path; note that it may be a *descendant* of
the root, not the root itself. (Execution mode returns only the target leaf path and needs no descent
path.)

**Return-and-continue.** Once descent has produced its result — a target (+ descent path in planning
mode, or leaf path in execution mode), `NEEDS-REFINEMENT`, `REPLAN-REQUIRED`, BLOCKED, `none`, or
`not-traversable` — return that result to the calling
skill (`superplan` for planning mode, `superrun` for execution mode) and immediately continue
executing the caller's next section. Do NOT end your turn after the descent. Do NOT print a
"descent complete" summary as if it were a final answer; the caller's Final Report is the user's only
checkpoint.

## C7. ASCENT — update ancestor rows up to the root

**Input:** a starting node, the path up to the root, and a **mode**. For **planning mode** the start is
the immediate parent and the path is the descent path (C6) reversed. For **completion mode** the start
is the executed leaf and the path is the parent chain obtained by following parent-seed references
(C5) upward.

At each **ancestor** along the path, locate the row whose **active** child-plan link (C3) points
at the child you just came from. For completion ascent, a `repair requested` row or a row
whose active Plan now points to a successor MUST NOT be advanced by the predecessor's
closeout. Record historical evidence only and return without changing active rows or ancestors.
Never match a row through its repair history. If the predecessor actually merged, first record its
delivery/contracts and PR disposition in the C8 history; it stays completed history and any needed
correction is fresh work. A late predecessor closeout never closes the successor. Otherwise apply the
mode's update:

- **Planning mode** (superplan, after a new plan is written): set that row's **Status** →
  `in progress (planning underway)` **only if** it was previously not-started / `incomplete`. **Never
  downgrade** a more-advanced status; **never mark it complete** (completion is superfinish's job).
  Leave **Plan**, **PR**, and **Comments** unchanged — the `Plan` link already exists (it is how
  descent reached the child).

- **Completion mode** (superfinish, after a leaf is executed): the leaf row itself and ancestors
  are updated separately because they answer different questions.
  - **Local mode (`SUPER_GIT_MODE=none`):** set the active leaf to `completed-local` only after
    reopening its receipt and required command/review/acceptance evidence. Roll an ancestor to
    `completed-local` only when every active descendant has valid local completion evidence or an
    authorized disposition and no unresolved repair. Otherwise retain/advance partial progress.
    Never fill a PR column or infer a merge. Then skip the GitHub leaf/ancestor rules below.
  - **Leaf-row update** (the row pointing at the executed implementation plan): set the row's
    Status based on the leaf's authoritative closeout record at superfinish time. For upfront work,
    first verify its execution snapshot (generation, Stage ID/revision, historical preparation
    receipt/digest and reviewed revisions) and the claimed outcome. A partial record binds the verified
    open PR/head/CI evidence but is non-delivered and non-consumable; a delivery receipt additionally
    verifies delivered contract revisions and actual integration. The
    S5 digest is checked against the recorded pre-execution vault blob, not the closeout-annotated
    current plan. A completed stage is not reclassified by applying the unstarted-stage preparation
    predicate to its annotated bytes. Then —
    - `executed — PR open` if the code PR is still open (closeout exists; main does not yet have
      the code).
    - `completed-and-merged` (or `done`) if the code PR has been squash-merged to `main`.
    - For a discovery stage with no code PR, `completed-and-merged` / `done` only when its specified
      evidence and documented decision are tracked and verified and its delivered discovery contracts
      are identified.
    In each case, write a one-line rollup + `Closeout: [[…]]` link in Comments. Record the code PR
    number (`#NNN`) for code work. For evidence-only discovery, leave the PR cell blank (or explicit
    `none`) and keep its A7 evidence/decision publication in the closeout Comments/report. A later
    superfinish invocation flips `executed — PR open`
    to `completed-and-merged` once the PR merges (idempotent re-run).
  - **Ancestor-row update** (rows above the leaf, walked up via parent-seed references): read the
    child plan's progress-report table and apply the "all children merged-on-`main`" test (C4 —
    treating `deferred` / `declined` / `out-of-scope` as non-blocking; treating
    `executed — PR open` as NOT-yet-merged-on-`main`, i.e. blocking).
    - If every row is delivery-verified under C9 (including no-PR discovery rows), flip the ancestor's row → `completed-and-merged` (or
      `done`) and write a one-line rollup + `Closeout: [[…]]` link in Comments.
    - Otherwise set the ancestor's row to `in progress (partially executed)` — but **only if the
      row was previously `incomplete`, `PLAN WRITTEN — needs refinement`,
      `PLAN WRITTEN — ready to execute`, or
      `in progress (planning underway)`**; never downgrade a row already at
      `in progress (partially executed)` / `executed — PR open` / `completed-and-merged` / `done`.
      Then **stop flipping completes** higher up (you may still walk to the root, but only flip
      rows all of whose children are merged-on-`main`).
  - **Preserve the Plan link** when updating.

**Idempotency** (both modes): a row already at its target state (planning: already
`in progress (planning underway)` or more-advanced; completion: already at the state matching the
current child evidence — `in progress (partially executed)` when ancestors are partial,
`executed — PR open` when the leaf's PR is still open, `completed-and-merged` when the PR has
merged) is left untouched. Re-running superfinish after the code PR merges is the supported way to
flip `executed — PR open` → `completed-and-merged` (and propagate the parent rollup upward).

Stop at the **root**. If the starting node has no identifiable parent at all, there are no ancestors —
return immediately. Record every plan file touched (the calling skill's later commit step adds them via
explicit `git add`; supertraverse itself never commits). **After the ascent, return control to the
calling skill (`superplan` in planning mode, `superfinish` in completion mode) and continue executing
its next section without printing a separate report.**


## C8. Authorized repair — durable request and successor publication

**Consumers:** superagent applies an adopted re-plan decision; superreplan authors and publishes the
repair under REPLANNER. This is an explicit repair transition, not a relaxation of ordinary C4/C7
idempotency. Resolve mode through superstage S1: unmarked/incremental roots use the legacy single-leaf
form; `upfront-v1` roots use one generation-scoped batch. Do not convert one form into the other.

Superreplan is already the tick's one heavy skill. For a legacy repair it applies the single-leaf
authoring clauses below directly; it does not invoke superplan, dispatch a child, or consume a second
heavy operation. The supervisor routes every adopted legacy repair to it under REPLANNER; an upfront
batch uses the same REPLANNER route.

### Upfront batch request (superagent, before replanning dispatch)

One pending batch is an execution barrier for the whole goal, including unaffected stages and direct
superrun calls. Before any REPLANNER dispatch:

1. Read the adopted panel/user decision, its triggering finding/evidence, authoritative source
   agreement/revision, current root generation, S1 active map, S2 contracts, code/vault baselines, and
   every originating stage. Use superstage S4 to derive the candidate transitive dependent closure.
   Ambiguous authority, origin, generation, or evidence is **BLOCKED**.
2. Create one durable `findings/<timestamp>-replan-<topic>.md` record with exactly one stable
   **Decision ID**. Record at least: authority, rationale, source agreement revision; root path and
   from-generation; code and vault baselines; origin stages and initial candidate dependency closure;
   final semantic affected set and expansion reasons (both initially `pending`); every active
   path/revision; an initially unassessed per-stage `retain` / `revise` / `completed-history` /
   authorized disposition table with evidence slots; every predecessor PR/branch/worktree and
   integration disposition; for an executing/CI-pending stage, its execution snapshot, run ids,
   current PR/head and an initially unresolved merge disposition; draft paths, successor paths, and retired-ID replacement mapping
   (initially `none` or `pending`);
   **Resolution** (`pending`, later `published`, `superseded`, or `declined`); published generation;
   publication decision marker; and resolved publication PR/commit evidence. Do not omit a field
   because it is initially `none`. At this request boundary the final semantic set and expansion
   reasons stay `pending`, and the disposition table stays unassessed. Superreplan, not the
   controller, populates them during S4 assessment before candidate review/publication.
3. In the same A7 change, set the root's sole `Active replan` field to this record. Preserve every
   active Plan link, status, completed stage, closeout, PR reference, and preparation receipt at this
   request boundary. For protected-main internal vaults the docs PR must be merged to authoritative
   main; when A7 permits direct internal integration, or for an external vault, the complete change
   must be committed on the configured authoritative branch. Only committed, synchronized
   authoritative state counts. Then, and only then, may the controller persist `WAITING FOR PLAN`
   and the Decision ID/record recovery hints.

An adopted decision interrupted before step 3 is not discarded and does not authorize execution.
Reconcile the persisted decision authority, create or finish this same request, and keep execution
paused; a loop log alone does not authorize REPLANNER. Once the committed root points at the pending
record, the next heavy operation is `superreplan <root> <record>` under REPLANNER.

If the request catches a stage in CI wait, let the run finish or remain queued without treating it as
authority: preserve the packet and actual PR/branch/worktree history in the record, stop post-CI merge,
and require superreplan to assign `resume-existing`, `replace`, or another adopted disposition. Never
discard that history and never merge obsolete work merely because it was queued first.

There is at most one active upfront batch per goal. A later finding joins an unpublished batch only
through an explicit adopted record revision that updates origins, closure, baselines, and authority;
otherwise it waits for a subsequent batch after publication. Superseding or declining a pending batch
requires recorded adopting authority. Clear the barrier with no generation increment only in one A7
change that records the `superseded`/`declined` resolution and proves the still-active tree and every
live consumer remain valid; otherwise the unresolved structural obligation stays paused/BLOCKED.

### Upfront batch reconciliation and replay

Always reconcile from the authoritative committed/integrated tree and Git history before trusting
loop hints or working-tree contents:

- **Pending request, no unique draft:** dispatch/resume superreplan with the same record.
- **Pending request, one unique scratch batch referencing the Decision ID:** resume that batch. Draft
  candidates never become active Plan links and are never executable.
- **Published record and active root at its published generation, with `Active replan: none`:** locate
  exactly one complete old-to-new A7 publication transition by its Decision ID marker and tracked
  artifact changes, then resume the new tree. Request/checkpoint and later evidence-resolution commits
  may repeat that ID; they are not publication transitions. Stale `PLANNING`/old-generation loop hints
  are repaired without republishing.
- **Relevant source, code, vault, path, stage, contract, PR, or worktree baseline changed before
  publication:** reassess the affected set under S4 and update the pending record/drafts before any
  activation. Do not bless stale candidates.
- **Missing referenced record, duplicate live records claiming one Decision ID, multiple unretired
  draft successor sets, divergent successors, mismatched generation, multiple matching publication
  transitions, or mixed/partial publication:** **BLOCKED** until authoritative evidence uniquely
  reconciles the state.

For callers that report the artifact handler separately from C6 selection, use these exact results.
`outcome: continue` means the adopted request can be durably created, resumed, reassessed, or
reconciled; `outcome: BLOCKED` means contradictory/missing evidence prevents that handler. Report
`publication: scratch` only for one unique resumable draft/checkpoint, `publication: vault` only for a
verified authoritative published generation, and `publication: none` otherwise. A relevant baseline
change with one unique draft is `continue` / `scratch` with replay action `reassess`, never permission
to publish stale work. `dispatch: none` applies until the request commit and root barrier are
authoritative; afterward a valid pending record names `dispatch: superreplan`.

One unique complete internal publication candidate in an open, unmerged A7 docs PR is
`outcome: continue` / `publication: none`: resume and reconcile that same PR while the committed
pending barrier remains authoritative. It is not a published tree and never authorizes execution.
Return **BLOCKED** instead when the PR candidate is partial, divergent, stale without a resolvable
reassessment, or otherwise ambiguous.

A7 writes files before it commits them, so a dirty root that appears to clear the barrier or expose a
new generation is still the committed pending generation. An internal docs branch/open PR does not
activate a code-root tree before merge to authoritative main; a configured direct-internal or
external-vault edit does not activate until its complete batch is committed on the authoritative
branch. Never validate selection against those uncommitted or unmerged candidate contents. Keep the
pending barrier in force, resume the same Decision ID where unique, and block if the mixed state is
ambiguous.

Publication evidence is not self-referential. The atomic batch records its stable Decision ID as the
publication marker and can leave resolved publication PR/commit evidence pending. After integration,
find the unique commit from that marker plus its tracked artifact set; a later reconciliation/report
may write the resolved SHA. Never require a commit to contain its own future hash.

A late predecessor closeout after publication is historical evidence. If the active row now points to
its successor, C7 must not update that row or ancestors from the predecessor closeout. Reconcile any
real delivered work through the record and successor; never close the successor by inference.

### Legacy single-leaf request (superagent, before replanning dispatch)

1. Identify the affected active leaf, immediate-parent row and ancestor path. Read its finding,
   closeout, PR/branch/worktree and the adopted panel/user decision. If the target or authority
   is ambiguous, return BLOCKED for escalation; never reopen unrelated completed work.
2. Write a durable `findings/<timestamp>-repair-<topic>.md` record. Required fields: **Decision ID**
   (stable across replay), **Decision** (adopter, date, rationale, authorized corrections),
   **Root**, **Parent and step**, **Previous plan**, **Previous closeout**, **Code PR / branch /
   worktree** (or explicitly absent), **Successor** (initially `pending`), **Disposition**
   (initially `pending`), **Resolution** (initially `active`; later `integrated`, `superseded`
   with the next decision/record link, or `declined`/`deferred` with adopted disposition).
   Capture the decision itself here, not only in the gitignored loop.
3. Set that step's Status to `repair requested` and Comments to include `Repair: [[record]]`.
   Keep the existing active Plan, PR and closeout links until successor publication. Reopen
   ancestors along this path to `in progress (partially executed)`; move stale ancestor Closeout
   links/banners into the repair record so they cannot hide the path. This is the only authorized
   backward transition; preserve unaffected siblings and the original leaf/closeout files.
4. Persist the repair record and tree edits under superauthor A7 (`none`: write/reopen/verify local
   files; `github`: external-vault commit or internal docs PR), then verify all are present in the
   authoritative tree. Only then set
   `plan_exhausted: false`, `status: WAITING FOR PLAN`. Persist the decision ID and record link
   in the loop's Decisions entry. A log-only decision is not an applied repair.

**Replay/fresh tick:** before dispatch, reconcile adopted decisions against the tree. If a
legacy Decisions entry has no record, create the C8 request using that recorded authority;
if it cannot uniquely identify the target, escalate. An existing record with `Successor: pending`
resumes the same request. If the record names a successor and the active link agrees, continue
from that plan's current state; do not reset the row or create another successor. For repeated
repairs, follow recorded successor → next repair links to the current active plan: a verified
chain `P0 → P1 → P2` resolves the earlier decision as historical, not contradictory. Mark the
previous record `superseded` with the next decision link when adopting a new repair. Process
only the latest unresolved request after validating the chain; cycles, divergent successors or
missing adopted authority are BLOCKED. An `integrated` or authorized `declined`/`deferred`
resolution with matching evidence is settled and must not reopen work, even if Successor was
still pending when declined. Reconcile missing resolution annotations from verified publication
or disposition evidence; do not infer resolution from a status word alone. A partial
publication must be reconciled from files and commit evidence before dispatch; contradictory
links or multiple successors are BLOCKED. Reuse the decision ID; do not duplicate records on retry.

### Legacy single-leaf publication (superreplan)

For the selected repair row, superreplan applies superauthor A2/A3/A6/A7 and superplan's legacy
self-review, routing, parent-row, and reporting clauses directly without invoking superplan. Read the
C8 record, predecessor, finding and closeout. Write a
**new implementation plan** in `plans/` with a fresh filename and parent reference to the same
immediate parent. Include `Supersedes: [[predecessor]]`, `Repair: [[record]]`, explicit corrections,
remaining work, regression checks and integration disposition. Preserve the predecessor unchanged.
Do not copy its closeout banner or checked-off tasks into the successor.

The integration disposition must state whether to resume the existing PR/worktree or create a
replacement. When reusing it, verify its branch/head and rerun the required review/test gates after
correction. When replacing it, explicitly resolve the old PR (with authority to close it, if needed)
and account for its changes. An old open PR is not silently forgiven by supersession.

Publish together: successor file; record's **Successor** link and planned **Disposition**;
row's active **Plan** link to successor and Status `PLAN WRITTEN — ready to execute`. Move the
row's predecessor Plan/Closeout markers into the repair record; retain only `Repair: [[record]]`
as historical navigation in Comments. Preserve PR provenance in the record; the row's PR column
identifies the PR being reused or is blank pending replacement. Apply the same rules to bullet rows.
Persist/verify before returning success (`none`: reopen local artifacts under inherited ownership;
`github`: commit/sync under A7). On interruption, reuse the record's named successor
or the unique draft referencing this Decision ID; never generate a second one blindly.

A successor is now an ordinary active leaf for execution and closeout. Its closeout records how
the predecessor PR was resolved and the actual integration evidence; C9 checks that evidence.

## C9. Completion audit — empty queues are not completion

**Consumers:** superagent before any transition to DONE; superrun when execution descent is `none`.
Return **complete**, **incomplete** (eligible planning/execution work), or **BLOCKED** with concrete
rows, PRs and missing evidence. This audit is read-only; reconcile via the owning skills.

Resolve mode with superstage S1. For `upfront-v1`, validate the complete active graph with S2 and
include every active stage, dependency, contract delivery, preparation pointer, and active-replan
barrier in the audit. Inspect the synchronized authoritative root, not loop hints or an unmerged docs
candidate. A non-`none` barrier, missing/malformed record, or partial publication is BLOCKED/incomplete
according to C8 and can never be DONE. An invalid graph is BLOCKED. Incremental and unmarked roots
retain the legacy audit below.

1. Read the synchronized authoritative tree from the root. Visit active child links recursively
   even when internal rows carry closed status or closeout banners. Track visited paths: cycles,
   unreadable/missing active plans, non-traversable roots and ambiguous links are BLOCKED. An
   unmarked legacy root means `github`; if that disagrees with the effective mode, return BLOCKED
   for mode mismatch before any git/GitHub action. A marked root whose mode or physical project root
   differs from the loop/effective context is likewise BLOCKED and cannot claim integration. An
   intentionally declined/deferred/out-of-scope subtree with recorded authority and disposition
   need not be descended into. A root banner alone never proves completion.
2. At each active leaf/step, accept only (a) completed-and-merged/done or affirmative legacy
   merged/shipped/closed-out state **with verified integration evidence**, or (b) a recorded
   authorized declined/deferred/out-of-scope disposition. For PR work, verify PR state MERGED,
   its merge commit in the code repository's main history and tracked closeout. For direct/no-PR
   work, verify the recorded integration commit on main (local main when no remote) and closeout.
   Documentation-only work uses its tracked committed deliverable on the authoritative main/vault
   branch. A docs closeout commit alone never substitutes for the code integration evidence.
   In `SUPER_GIT_MODE=none`, instead accept `completed-local` only with a valid receipt whose
   root/active-leaf identity, mode, before/result manifests, changed/deleted paths, command results,
   required reviews, acceptance coverage, outstanding obligations, and timestamp all validate.
   A label or report without those files is BLOCKED. In `github`, `completed-local` is not integrated.
   An upfront implementation delivery receipt must bind its execution-entry root generation,
   Stage ID/revision, historical preparation receipt/digest, reviewed code/source revisions, actual
   merge/direct-integration identity, and every produced contract revision. Verify the preparation
   digest against the recorded historical plan blob, not the closeout-annotated current file. For a
   discovery stage, accept no-code completion only when its specified evidence and documented decision
   are tracked and verified and its delivered discovery contracts are identified.
   In upfront mode, verify that delivered evidence identifies every produced contract revision
   consumed by active stages. A provider's approved decline/defer/out-of-scope disposition can close
   its own obligation but cannot satisfy a consumer; that live consumer keeps the goal incomplete or
   BLOCKED pending an adopted replan.
3. Re-evaluate every dependency edge from delivery receipts. A closed ancestor cannot hide a live
   consumer whose prerequisite delivery is absent, declined, at the wrong contract revision, or only
   open/CI-pending; report that path BLOCKED. Revised stages after a generation publication require a
   new preparation. A retained stage keeps preparation only with the focused new-generation
   revalidation required by S4/S5. Old-generation preparation alone is an active obligation, not
   completion evidence.
4. Inspect findings, closeouts and C8 records that name active contract/assumption IDs. Routine verified
   findings that preserve commitments create no planning obligation. A verified contradiction keeps
   affected unfinished preparation non-executable and requires the decision/adoption path; an
   unverified finding is never proof. Any adopted-but-unpublished request, unresolved batch/repair,
   conflicting disposition, or unresolved affected consumer prevents completion.
5. If the audit discovers unfinished work hidden by an ancestor's closed-for-descent status
   or closeout marker, return **BLOCKED** with that path for authorized reconciliation.
   Returning `incomplete` without restoring reachability would repeat the same empty queues.
   Otherwise, `executed — PR open`, closed-but-unmerged PR, pending CI, unresolved repair or BLOCKED finding,
   missing/unverifiable integration evidence, or inconsistent state => **BLOCKED**, even if a
   report also says `none`. Ordinary unplanned/ready work => **incomplete**. A valid pending C8
   request => **incomplete** with its repair planning target; invalid repair state => **BLOCKED**.
6. For repair history, verify each predecessor PR's disposition: reused and now merged, or
   explicitly replaced/closed with authority, or intentionally declined/deferred with reason.
   Historical closeout links never suppress active repair work. Supersession alone does not
   satisfy an unresolved predecessor PR. Do not execute or reopen finished predecessors.
7. **complete** requires the root barrier to be clear; the active graph valid; every active stage and
   prerequisite delivery resolved; every implementation/discovery delivery receipt verified; all
   predecessor PR/integration history accounted for; and no unresolved finding, repair, batch, CI wait,
   or other active obligation. Report checked rows, contracts, receipts and integration/disposition
   evidence to the caller. Empty traversal queues are only the trigger for this audit. Unknown evidence
   => BLOCKED, never optimistic completion.
   Delayed predecessor closeouts remain historical and cannot complete or overwrite a successor.
