---
name: auto
description: "Autonomously execute research cycles. Specify the cycle limit as an argument (e.g., /auto 2). Default: 5."
user-invocable: true
---

# /auto — Research Cycle Scheduler

`/auto` is the **thin scheduler** that drives research forward. It owns no scientific judgment of its own. Each cycle, it dispatches the agent team in a fixed sequence; every substantive decision (what to investigate, what to record, what to verify) is delegated.

The team and who owns what:

| Role | Agent | Owns |
|---|---|---|
| **Direction challenge** | `direction-challenger` | Pre-direction opposition: challenges value, goal, necessity, frame, scale, authority, and inertia anchors before the direction hardens |
| **Direction** | `research-planner` | `research/focus.md` — reads the tree, decides the next question, expresses it as a cursor + dispatch plan + tree directives; may create a minimal child node when immediate dispatch needs that structure |
| **Tree transaction** | `curator` | Graph/lifecycle/placement, pre-worker readiness transactions, structural closure for planner-created children, state.md absorbed evidence, map.md / plan.md consistency, child presentation transactions, conventions/checks placement, analysis-material preservation/promotion, retraction, `dead_ends.md`, and admitted findings.md materialisation |
| **Verification** | `critic` | Independent Provisional Review of every review-eligible worker submission and Durable Surface Review of findings/analysis surfaces requested by curator |
| **Execution** | researcher / simulator / reader / scout / engine-builder / concept-checker / self-check | Bounded tasks producing provisional worker submissions in `_reviews/` plus raw process logs as specified by their agent prompt |
| **Human oversight guide** | `guide-writer` | `research/**/guide.md` — session-end sweep over scheduler-supplied target nodes; writes human-facing oversight guides from durable surfaces without deciding research claims or direction |
| **Session boundary** | scheduler + `.scripts/close-session.mjs` | Transactional close of research planner's close-session packet into session log / focus / last_session / node-scoped backlog.md / agenda; beacon deletion; manifest-scoped commit + push |

`/auto` itself owns only: the cycle loop, the resume beacon, pre-direction challenge dispatch, parallel worker dispatch, auto-attaching Provisional Review to each worker submission, running the optional one-repair loop, dispatching curator with the right inputs, dispatching Durable Surface Review when curator requests it, detecting parent-ascent presentation boundaries, maintaining an in-memory guide-target set from scheduler-known node paths, dispatching guide-writer at Session End, collecting the session-owned stage manifest, and closing the session through `.scripts/close-session.mjs`. It does not create nodes itself; if research planner creates a minimal child before returning `focus.md`, the scheduler simply parses the new cursor/worker target and curator closes the structure later in the cycle. When research planner writes `### Pre-Worker Tree Directives`, `/auto` runs curator before workers as an inserted readiness transaction, then continues the ordinary cycle unless curator reports that the planned worker dispatch was invalidated.

## Constraints

- **Write all prose in japanese.** Applies to `research/focus.md`, `_reviews/`, `.logs/`, `agenda.md`, curator's tree writes, all worker submissions. Technical terms, proper nouns, LaTeX mathematics, file/folder slugs, frontmatter keys, and the structural `##` headings documented in `.codex/research-tree.md` and here may stay in English. The rule is about body prose, not structural tokens.
- `request_user_input` and all other user-input solicitations are prohibited. Users are often away during `/auto`; asking blocks the session.
- Do not initiate user-facing progress messages during a valid active session. The only scheduler-initiated user-facing message during an active session is the final draft emitted at Session End. Startup precondition failures may emit their specified stop message. If the user initiates communication mid-session, respond briefly and continue. Corrections from the user take precedence over scheduled dispatches.
- **`exec_command("sleep ...")` is prohibited; polling via `exec_command("ls ...")` file-existence checks is prohibited.** For waiting on agent completion use only Pattern A or Pattern B as defined in `phases/dispatch.md`.
- Full paper text is acquired only from arXiv so source provenance stays reproducible and full-text licensing/source drift does not enter the research tree. Metadata, bibliographic records, abstracts, and non-full-text discovery may use other sources when the relevant agent prompt allows it.
- **Paper writing is NOT `/auto`'s responsibility.** Writing is handled by the `/write` skill. `/auto` drives research only.

## Turn-Yielding Discipline

`/auto` is an autonomous loop: the user is not present between cycles, and a closing-tone message mid-session stalls the session waiting for input that never arrives. Any mid-session message that summarizes progress and waits for user confirmation is a stall, regardless of the exact wording.

- **Never end a turn mid-session with a user-facing progress draft.** Between cycles, the next action is a tool call — the next direction-challenger dispatch, the next research planner dispatch, the next worker batch, or Session End. If you are tempted to draft "I have finished cycle N of M; continuing with cycle N+1?", that is the stall — replace it with the actual next dispatch.
- The **only** user-facing closing message is the final Session End draft, emitted when `MAX_CYCLES` is exhausted or the scheduler exits for an unrecoverable failure. `research/focus.md` status labels are research-state records, not scheduler stop signals.
- Compaction / reconnect / crash do not terminate a session. The `.logs/.auto-active` beacon (written at the start of every cycle) and the `SessionStart` hook jointly ensure the next session resumes the loop without a greeting. See `phases/session-lifecycle.md` § Resume for the mechanics and the fallback.
- Progress summaries that genuinely belong somewhere go into `.logs/{timestamp}_auto.md` (session log, written by `.scripts/close-session.mjs` from research planner's close-session packet) or `research/focus.md § Context` (research planner's next-cycle direction). Neither is a yielded turn.

## Arguments

`/auto {N}` — cycle limit. Default: 5. Hereafter `MAX_CYCLES`.

## Terminology

| Term | Meaning |
|---|---|
| **Session** | One `/auto` execution — from start to final draft |
| **Ordinary Cycle** | One iteration of the normal scheduler loop (direction-challenger → research planner → optional pre-worker curator readiness transaction → workers → Provisional Review → optional one repair loop → curator → optional Durable Surface Review → curator follow-up) |
| **Presentation-Boundary Cycle** | A cycle with a child-to-parent ascent. The child presentation transaction runs before workers; it replaces worker dispatch only when curator invalidates the planned dispatch or research planner intentionally left `Worker Dispatches` empty |
| **Task** | One `spawn_agent` tool call |
| **Presentation Boundary** | A child-to-parent cursor ascent where curator first makes the child readable as a parent component, usually by updating parent `map.md` / state / plan, before any parent-level workers use that context |
| **Child Presentation Judgment** | Research planner's meaning judgment at the boundary: what the child was for, what it achieved or failed to achieve, and what the parent should now see |
| **Child Presentation Transaction** | Curator's tree update at the boundary: applying the judgment to status, Current Board, parent map/plan/state, durable surfaces, archive/reframe mechanics, and link hygiene |
| **Guide target set** | In-memory Set of node paths the scheduler already touched or observed this session; used only at Session End to tell guide-writer which guides to inspect |

One session = `MAX_CYCLES` cycles unless a startup precondition fails, the user explicitly stops the session, or the scheduler reaches an unrecoverable failure. Multiple tasks can run in parallel within a cycle.

---

## Phase Index

Detail lives in two phase files; read on demand, not all at once.

| File | Loaded when | Purpose |
|---|---|---|
| `phases/dispatch.md` | When launching workers or critic | Pattern A / B launch methods, prompt template, Provisional Review, Durable Surface Review, per-agent dynamic data |
| `phases/session-lifecycle.md` | Session Start and Session End | Resume check, initial sanity check, scheduler-owned session-end mechanical steps (simulation housekeeping, final sweeps), close-session packet handoff |

The research information model (tree structure, file roles, context scoping, convention ledger, provenance taxonomy) is canonical in `.codex/research-tree.md` — direction-challenger, research planner, and curator read it at every dispatch. `/auto` itself does not need it in working memory; `/auto` reads `research/focus.md` (the dispatch-spec file — treat it as the scheduler's interface with research planner, not as "tree content") only to extract the fields it dispatches on. `/auto` never reads node-level files directly. Node-level files are read by direction-challenger in its narrow local challenge scope, by research planner for direction-setting, and by curator for tree writing.

---

## Session Start

Read `phases/session-lifecycle.md` § Session Start. Key outcomes:

- Beacon-based resume decision (fresh vs. resume mid-cycle)
- Initial sanity gates: `research/state.md` must exist (else emit the stop message specified in `phases/session-lifecycle.md` and stop); `concepts/` exists; `.gitignore` covers `.logs/.auto-active`
- `research/focus.md` existence check (if missing, the first research planner dispatch initialises it after direction-challenger runs — see session-lifecycle)

`/auto` does **not** read node-level tree files at session start. The ancestor-chain read is research planner's responsibility and happens at the start of every cycle (so research planner's context always reflects the post-cycle state, not a stale session-start snapshot).

---

## Cycle Loop

Repeat up to `MAX_CYCLES`. At each iteration:

### 0. Beacon

Overwrite `.logs/.auto-active` with:

```json
{"remaining": <MAX_CYCLES - cycles_done>, "max_cycles": <MAX_CYCLES>}
```

This is the resume beacon read at Session Start (see `phases/session-lifecycle.md`). Writing it every cycle (not just at session start) means that after a mid-cycle compaction, `remaining` reflects what is owed.

Maintain a session-local `guide_targets` Set throughout the loop. Add `research/` at session start. During each cycle, add every scheduler-known node path without doing research interpretation:

- current `Cursor`
- `Previous cursor` when present
- every worker dispatch `Target: research/{path}/`
- curator dispatch cursor
- presentation-boundary parent and child
- every Durable Surface Review target's owning node
- final cursor ancestors at Session End

This Set is not written to disk and is not a change detector. It is only the scheduler's mechanical record of where this session looked or acted, so guide-writer can refresh human oversight entrypoints at Session End without curator deciding guide staleness.

### 1. Direction-Challenger Dispatch — Pre-Direction Opposition

```

spawn_agent(prompt="""
Read and follow `.codex/agents/direction-challenger.md` as your role definition. Treat the rest of this prompt as task-specific input.

## Task
Obtain a path via `bash .scripts/log-path.sh direction-challenge`, write the pre-direction challenge for this cycle to that file, and return it as `DONE: {path}`.


## Previous-Cycle Material
Critic flags: {REVISE-BLOCKING / OPAQUE / REJECT flags from Provisional Review or REVISE / REJECT flags from Durable Surface Review in the previous cycle, if any; do not include raw transaction paths unless needed to identify the flag}
Curator flags: {flagged-for-research planner-review items from the previous curator sweep, including any pending Durable Surface Review requests not drained in-cycle}
Curator sweep summary: {short summary or path, if available}

## Context
Session cycle: {cycle_number} of {MAX_CYCLES}
""")
```

The challenger reads only its narrow local scope and returns `DONE: {path}`. Append each returned direction-challenge path to the session's in-memory evidence list for Session End. If it returns `FAILED:`, continue to research planner with `Direction Challenge: unavailable — {failure}`. The challenge is helpful but not load-bearing; research planner owns the decision.

### 2. Research planner Dispatch — Direction

Before dispatching research planner, read the current `research/focus.md` if it exists and capture the **Previous cursor** from its `Cursor:` line. Also run `node .scripts/literature-status.mjs --limit=8` if `literature/catalog.jsonl` exists. Pass the output verbatim in `## Literature Status`. This is scheduler-owned context condensation: research planner should see unread/read/fetch pressure automatically without spending direction-setting attention parsing the full catalog unless the summary makes literature decisive.

```

spawn_agent(prompt="""
Read and follow `.codex/agents/research-planner.md` as your role definition. Treat the rest of this prompt as task-specific input.

## Task
Update research/focus.md for the next cycle.


## Direction Challenge
{path returned by direction-challenger, or unavailable note}

## Recent Deliverables
{paths to worker submissions / review transactions produced in the previous cycle, if any}

## Critic Verdicts
{paths to Provisional Review and Durable Surface Review outputs from the previous cycle, if any}

## Curator Sweep
{path to curator's output from the previous cycle, if any}

## Literature Status
{output of `node .scripts/literature-status.mjs --limit=8`, or "No literature catalog present"}
""")
```

On the very first cycle of a session, `Recent Deliverables` / `Critic Verdicts` / `Curator Sweep` are empty (no previous cycle); the research planner initialises from `research/focus.md` and the tree. If `research/focus.md` does not yet exist, include a note in the prompt: `focus.md missing — initialise at research/ root`.

Research planner returns `DONE: research/focus.md`. If it returns `FAILED: cursor target {path} missing — scheduler must reinitialise focus.md`, re-dispatch once with the failure message appended and the instruction: `Recovery: initialise the cursor at research/ root; this scheduler recovery does not count as a research-planner cursor move.` If it returns any other `FAILED:`, re-dispatch once with the failure message appended to the prompt. If the second attempt also fails, exit to Session End with a partial draft — deciding *why* a failure is recoverable is research judgment, so the scheduler bounds the loop mechanically rather than classifying the failure.

### 3. Parse `research/focus.md`

Read the new `research/focus.md`. Extract:

- **Cursor** — the path into the tree (for context when forming worker prompts)
- **Previous cursor** — carried from the pre-dispatch read above
- **Status** — `active` or `session_complete` as a research-state label only
- **Pre-Worker Tree Directives** — list of curator directives that must land before worker dispatch
- **Worker Dispatches** — list of `{agent}: {task}` entries
- **Tree Directives** — list of directives for curator
- **Naming Decisions** — reusable-name routing proposals from research planner, possibly empty
- **Blockers** — informational

If an older `focus.md` lacks `### Pre-Worker Tree Directives`, treat that section as empty for this cycle and let research planner regenerate the full format on its next write.

Do not use `Status: session_complete` to exit the loop. The planner may record that no current research frontier is visible, but `/auto` still owns the user-requested cycle budget. Continue the ordinary cycle mechanics: if dispatch and directive sections are empty, the cycle is a recorded no-op/think-cycle and still counts toward `MAX_CYCLES`.

The scheduler does not auto-remediate cursor jumps. If research planner violates its one-edge cursor discipline, the next research planner dispatch must repair the direction; the scheduler only parses fields and continues.

### 3a. Presentation Boundary — Child Presentation Transaction

If **Previous cursor** is a direct child of the new **Cursor**, the research planner has floated up from child to parent. Treat this as a presentation boundary readiness step before ordinary parent work, not as a mandatory workerless parent cycle.

Run curator immediately, before launching any workers:

```

spawn_agent(prompt="""
Read and follow `.codex/agents/curator.md` as your role definition. Treat the rest of this prompt as task-specific input.

## Task
Child Presentation Transaction. The cursor has just ascended from the child below to its parent. Apply research planner's Child Presentation Judgment from the Tree Directives, plus your normal transaction mechanics, so the child is readable from the parent before parent-level workers or planning use the parent context: status, Current Board, parent map/plan/state, extracted durable surfaces, dead-end/draft/findings/guide placement, archive/reframe needs, and link hygiene. Return whether the planned Worker Dispatches remain valid after this presentation transaction.


## Boundary
Parent cursor: {cursor path from focus.md}
Child being presented: {previous cursor path}

## Child Presentation Judgment / Tree Directives (from research planner, this cycle)
{verbatim copy of focus.md § Tree Directives}

## Naming Decisions (from research planner, this cycle)
{verbatim copy of focus.md § Naming Decisions}

## Planned Worker Dispatches (for validity check only)
{verbatim copy of focus.md § Worker Dispatches}

## New Evidence This Cycle
(none — this is a presentation-boundary transaction before parent-level workers run)

## Context
Session cycle: {cycle_number} of {MAX_CYCLES}
Presentation boundary: true
""")
```

This curator call executes the presentation-boundary transaction and returns a summary. Record that summary as the cycle's presentation curator summary. If it explicitly returns `Dispatch readiness: invalidated`, skip worker dispatch, Provisional Review, and the ordinary curator dispatch for this cycle; carry the summary and the full unexecuted directive set into the next research planner prompt so the planner can re-plan from the repaired parent. Do not execute ordinary `Tree Directives` in an invalidated readiness cycle; the premise for this cycle's plan has changed.

Otherwise continue toward the normal Worker Dispatch step in this same cycle. Presentation makes the parent readable; it does not by itself consume a cycle. If `Worker Dispatches` is non-empty, launch them after the presentation transaction so parent-level work can proceed from the updated `map.md` / state / plan. If `Worker Dispatches` is empty, run step 6 only when there are remaining non-presentation `Tree Directives`; otherwise proceed to Cycle End after any requested Durable Surface Review.

If the presentation-boundary curator return contains `Durable Surface Review needed:`, always drain that review before launching workers. Use the presentation-boundary durable-review follow-up path: dispatch critic per step 6a, then re-dispatch curator with the review result, the presentation curator summary, `New Evidence This Cycle: (none — worker dispatch has not run yet)`, and the instruction to apply only the presentation-boundary durable review before returning to step 3b / step 4. This avoids scheduler-side content judgment about whether the review affects worker context.

Research planner may list parent-level workers on an ascent cycle when the next research question is already clear and the presentation transaction is only a readiness repair. The scheduler should not discard those workers solely because the cursor ascended.

### 3b. Pre-Worker Curator Readiness Transaction

If `### Pre-Worker Tree Directives` is non-empty, dispatch curator before launching workers:

```

spawn_agent(prompt="""
Read and follow `.codex/agents/curator.md` as your role definition. Treat the rest of this prompt as task-specific input.

## Task
Pre-Worker Readiness Transaction. Execute the pre-worker tree directives below so workers read a valid active-memory context. Perform content-preserving routing work only: repair graph/lifecycle/context-route surfaces, compress residue, relocate/archive/demote/re-link material, create/close/reframe placement when authorized, and return whether the planned worker dispatch remains valid. Do not perform content audit, substantive findings/analysis edits, provenance closure, or Durable Surface Review requests in this pre-worker transaction.


## Pre-Worker Tree Directives (from research planner, this cycle)
{verbatim copy of focus.md § Pre-Worker Tree Directives}

## Naming Decisions (from research planner, this cycle)
{verbatim copy of focus.md § Naming Decisions}

## Planned Worker Dispatches (for validity check only)
{verbatim copy of focus.md § Worker Dispatches}

## New Evidence This Cycle
(none — this transaction prepares active memory before evidence-producing work)

## Context
Cursor: {cursor path from focus.md}
Session cycle: {cycle_number} of {MAX_CYCLES}
Pre-worker readiness: true
""")
```

Record the returned summary as the cycle's pre-worker curator summary. The pre-worker pass must not request or launch Durable Surface Review. The normal path then continues to Worker Dispatch. Only if curator explicitly returns `Dispatch readiness: invalidated` should the scheduler skip worker dispatch, Provisional Review, and the ordinary curator pass for this cycle, then proceed to Cycle End; carry the curator summary and the full unexecuted ordinary `Tree Directives` into the next cycle's `Curator Sweep` so research planner can re-plan from the repaired tree. `Dispatch readiness: invalidated` means the memory repair showed that the planned worker target or task requires non-routing work before workers can honestly proceed, not that curator has chosen a new research direction. Do not execute ordinary `Tree Directives` after an invalidated readiness transaction; the cycle's premise has changed.

If there are no `Pre-Worker Tree Directives`, skip this step. Do not synthesize a readiness pass from ordinary `Tree Directives`; timing is research planner's judgment.

### 4. Worker Dispatch — Parallel

If `Worker Dispatches` is non-empty, launch all workers in parallel per `phases/dispatch.md` (Pattern A by default).

Each worker's prompt follows the template in `phases/dispatch.md` § Prompt Template — the scheduler fills in task-specific fields from the research planner's dispatch entries, plus the cursor path for context.

If `Worker Dispatches` is empty, skip this step. A structural-review cycle (only Tree Directives) is legitimate.

### 5. Critic — Provisional Review

For every review-eligible worker submission returned in step 4, dispatch a critic (Provisional Review — separate judgment in the same `_reviews/{slug}/` transaction) per `phases/dispatch.md` § Provisional Review Rule. Critic runs in blind mode by default for submissions that are mechanical/mathematical (researcher attempts, simulator runs), source-audit mode for reader submissions, and contextual mode when the submission's soundness depends on the research narrative (scout surveys, concept proposals). The rule for mode selection is in `phases/dispatch.md`.

Worker submissions skipped from critic: `self-check` by fixed rule, because self-check is itself a review; otherwise none by default. Research planner may in rare cases mark a dispatch as "no-critic" in `### Worker Dispatches` (e.g., an engine-builder refactor with no substantive claim to verify); honour such markings.

Critic writes `critic.md` in the same `_reviews/{slug}/` directory. For `REVISE-BLOCKING` or `OPAQUE`, apply the optional one-repair loop in `phases/dispatch.md` only when the repair is cheap and bounded. Collect the transaction directory, worker submission path, final critic review path, and final verdict for step 6.

### 6. Curator Dispatch — Execute Tree Changes

Dispatch curator once per cycle with:

```

spawn_agent(prompt="""
Read and follow `.codex/agents/curator.md` as your role definition. Treat the rest of this prompt as task-specific input.

## Task
Execute the tree directives below and absorb the new evidence (worker review transactions) into the tree per your own operating rules.


## Tree Directives (from research planner, this cycle)
{verbatim copy of focus.md § Tree Directives}

## Naming Decisions (from research planner, this cycle)
{verbatim copy of focus.md § Naming Decisions}

## Pre-Worker Curator Summary
{DONE summary from step 3a presentation transaction and/or step 3b pre-worker readiness transaction, or "(none)"}

## New Evidence This Cycle
- {transaction directory} — worker: {worker.md or repair.md}; critic review: {critic.md or critic_rereview.md}; verdict: {ACCEPT / REJECT / REVISE-NONBLOCKING / REVISE-BLOCKING / OPAQUE}
- ...

## Durable Surface Reviews
(none — first curator pass this cycle)

## Context
Cursor: {cursor path from focus.md}
Session cycle: {cycle_number} of {MAX_CYCLES}
""")
```

If there are no worker review transactions and no remaining non-presentation `Tree Directives`, skip this ordinary curator pass. Otherwise curator reads the review transactions and tree state; executes the directives; absorbs admitted content into state.md without `_reviews/` or `.logs/` links; updates map.md / plan.md / conventions.md / admitted findings.md materialisations / status / _materials/analyses/*.md / checks / dead_ends.md per its operating rules; returns `DONE: {summary}`. Curator does not write guide.md.

On a presentation-boundary cycle where step 3a already executed the Child Presentation Judgment, do not ask curator to re-execute the same presentation directives in step 6. Pass the step 3a summary as pre-worker curator summary and set `Tree Directives` to any remaining non-presentation directives only; if there are none, write `(presentation directives already executed in step 3a)`. The ordinary curator pass still runs after workers when there is worker evidence to absorb.

If curator returns with unresolved `REVISE-BLOCKING`, `OPAQUE`, or `REJECT` Provisional Reviews, curator flags these in its return. The scheduler records the flag; direction-challenger and research planner see the flagged transactions in the next cycle's prompts, and research planner decides whether to re-dispatch, pivot, or close.

### 6a. Critic — Durable Surface Review (curator-requested)

Read curator's return. If it contains a `Durable Surface Review needed:` block, dispatch critic once per requested findings/analysis surface per `phases/dispatch.md` § Durable Surface Review Rule. This is scheduler-owned orchestration; curator requested the review but does not launch critic itself.

Collect each durable review path and verdict. Critic writes these review files under the target node's `checks/` directory, not under `.logs/`.

If there are no durable review requests, skip to Cycle End.

### 6b. Curator Follow-up — Apply Durable Surface Reviews

When Durable Surface Review ran in step 6a, re-dispatch curator with the review results:

```

spawn_agent(prompt="""
Read and follow `.codex/agents/curator.md` as your role definition. Treat the rest of this prompt as task-specific input.

## Task
Apply the Durable Surface Reviews below. Fix, demote, remove, or close provenance metadata per your own operating rules. Do not re-absorb worker evidence already handled in this cycle.


## Tree Directives
(none — durable-review follow-up)

## New Evidence This Cycle
(none — worker evidence already absorbed in the first curator pass)

## Durable Surface Reviews
- {findings/analysis path} — critic review: {checks/critic_... path}; verdict: {ACCEPT / REVISE / REJECT}; requested scope: {scope}
- ...

## Context
Cursor: {cursor path from focus.md}
Session cycle: {cycle_number} of {MAX_CYCLES}
Durable-review follow-up: true
""")
```

If this follow-up returns another `Durable Surface Review needed:` block for the same surface, carry it into the next cycle's Curator Sweep rather than looping indefinitely. A repeated request means curator's fix materially changed the durable surface; research planner should see the pending review, and the affected claim must not be treated as confirmed until the review is drained. At Session End, the scheduler must drain pending durable reviews before the close-session transaction unless the same surface has already gone through two review/fix rounds.

### 7. Cycle End

Increment `cycles_done`. If `cycles_done < MAX_CYCLES`, loop to step 0 regardless of the `Status` label in `research/focus.md`. If `cycles_done == MAX_CYCLES`, overwrite `.logs/.auto-active` once more with `{"remaining": 0, "max_cycles": <MAX_CYCLES>}` before proceeding to Session End, so a crash between the final cycle and the close-session transaction does not resume phantom work.

---

## Session End

Read `phases/session-lifecycle.md` § Session End. Summary:

1. **Simulation housekeeping decision** — if simulator ran, research planner may identify superseded scripts in final `research/focus.md` Tree Directives. Do not move them in the scheduler.
2. **Final curator sweep** — dispatch curator once more with the final Tree Directives plus a compact list of this session's worker-submission / critic-review paths and prior curator summaries for coherence review. Do not ask curator to re-absorb already absorbed review transactions or raw logs. Curator executes any `archive superseded script {path}` directives by moving the script and its companion `.md` to `_materials/src/archive/`.
3. **Drain pending Durable Surface Reviews** — if the final curator sweep or an earlier cycle carried pending durable review requests, dispatch those reviews and re-dispatch curator to apply them, subject to the two-round cap in `phases/dispatch.md`.
4. **Guide-writer sweep** — dispatch guide-writer with the session-local guide target set after curator has finished tree transactions and durable reviews. guide-writer updates `guide.md` only where the human oversight entrypoint is missing or stale.
5. **Final research planner dispatch (session-end mode)** — research planner writes the close-session packet (path obtained via `bash .scripts/log-path.sh close-session-packet` and returned as `DONE: {path}`), using the final curator sweep, guide-writer sweep, and this session's direction-challenge files as evidence for the next session's Focus and any `## Agenda` items. Capture the returned path for step 6.
6. **Close-session transaction** — write the session-owned stage manifest, then run `node .scripts/close-session.mjs --packet {packet path} --kind {auto|steer} --stage-manifest {manifest path}`. The script validates the packet, writes `research/focus.md` / `.logs/last_session.md` / the session log / node-scoped `backlog.md` files / `agenda.md`, deletes `.logs/.auto-active`, stages script-touched paths plus manifest-listed session paths, commits, and pushes. It returns `DONE: committed {hash} and pushed`, `DONE: no changes to commit`, or `FAILED: {reason}`.
7. **Final draft to user** — emit the session summary to the user. This is the **only** user-facing closing message (per Turn-Yielding Discipline). Yield after emitting.
