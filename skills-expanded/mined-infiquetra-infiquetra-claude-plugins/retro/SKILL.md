---
name: retro
description: The Infiquetra lifecycle META-IMPROVEMENT ENGINE. The TERMINAL, ADVISORY lifecycle phase downstream of /qa — it reads the work that shipped, gathers evidence (git forensics behind a stale-base/wrong-today BLOCK guard, saga trajectory, gh issues/PRs READ-ONLY, session transcripts), interviews the operator, writes a concise agent-consumable retro doc, PROMOTES generalizable findings into the engineering journal (pure-append, auto), CURATES the journal + auto-memory (staleness / contradiction / dedup / rule-enforcement sweeps, propose-diff-and-wait), MARKS the select cross-repo learnings transcendent for the promote layer (single-repo, propose-diff-and-wait), and runs net-new meta-improvement passes (new-skill detection, refine the lifecycle SKILLs, refine directives, prune memory) — every one gated. It never blocks the chain it follows, never mutates the world, never writes the saga, and never self-applies a non-journal edit. Triggers on "retro", "retrospective", "what did we learn", "leave the system smarter", a /qa hand-in, or the end of a meaningful work loop / PR / deploy.
---

# Retro

`/retro` answers **"What did this work teach us — and how does the system get smarter because of it?"**
It is the lifecycle's **meta-improvement engine**: the terminal phase that turns a finished thread (or a
time window of work) into durable knowledge, curated journal state, and concrete, gated proposals to
improve the lifecycle itself.

This engine is a faithful 3-source merge: the **git forensics + the stale-base/wrong-today BLOCK guard**
come from **gstack `retro`**; the **curation engine (staleness / contradiction sweeps, propose-via-question)**
comes from **gstack `learn`**; and the **compounding frame — "the first time you solve a problem takes
research, the next time is a lookup; knowledge compounds"** comes from **CE `ce-compound`** (plus its
parallel-subagent research pattern for the transcript fan-out).

## Position in the lifecycle

`/retro` is the saga `LIFECYCLE_PHASES` **`retro`** slot — the **terminal** phase, with **`resume-ready`**
maturity (`scripts/saga.py:56`, `:72`):

- `/qa` answers: "Does the shipped thing actually work?" (the acceptance gate)
- **`/retro` answers: "What did we learn, and how does the system get smarter?"** (this engine — terminal)

`/retro` is **ADVISORY**: the chain names it as the step after `/qa` but **never blocks it**
on its output. It is **READ-ONLY on the world** — it reads issues,
PRs, checks, and the board via `gh` and never mutates them (**mission-control owns the SDLC**); it reads git
and the saga and writes **no** saga tick (the `->retro` advance is dead wiring — `/retro` is saga
READ-ONLY). Surfaced follow-ups become a `mission-control` issue or a `QUEUED.md` entry — `/retro` routes
them, it does not file them.

## Core principles

1. **Leave the system smarter (compounding).** Every retro must make the next unit of work easier, not
   harder. A retro **diffs against the last retro** so knowledge accumulates instead of repeating: "first
   time research, next time lookup." A retro that records nothing durable was a wasted retro.
2. **Evidence before narrative, with the stale-base/wrong-today guard.** Never assert system state you have
   not just verified from a current source. For the time-windowed mode, the **stale-base/wrong-today BLOCK
   guard runs first** (Phase 1): if the window would be computed against a stale base or a wrong "today",
   **BLOCK and ask** rather than fabricate a coherent-looking narrative from near-zero commits. Validation
   discipline is load-bearing here — the engine's whole value is that it tells the truth about what
   shipped.
3. **The journal is the durable sink.** The markdown engineering journal — `LEARNINGS.md`, `DECISIONS.md`,
   `QUEUED.md`, `ARCHIVE.md` — is canonical for durable knowledge; `docs/retros/` holds the per-thread
   writeup that links to it. Findings flow **into** the journal, not into a separate store.
4. **Curate, do not just append.** Promotion is additive, but a journal that only grows rots. `/retro`
   runs curation sweeps over the journal and the auto-memory — **staleness** (entries citing deleted
   files / PRs / SHAs), **contradiction** (conflicting entries on the same key), **dedup** (an infiquetra
   addition to the sweep set), and **journal-rule enforcement** (e.g. the `MEMORY.md` ~24.4KB size rule).
5. **Self-modification is gated.** This is the load-bearing contract — see
   **THE TIERED SELF-EDIT SAFETY CONTRACT** below and `references/self-edit-safety.md`. The one-line rule:
   **AUTO-APPLY is ONLY a pure additive append of a NEW journal entry; everything else is
   propose-diff-and-wait.**
6. **Read-only on the world.** `gh` and `git` are used **read-only**; `/retro` never opens, edits, or
   merges an issue or PR, never deploys, and never writes the saga. Follow-ups are **routed**, not run.
   Big multi-file refactors surfaced by a pass are **offered** with a backend (operator-choice), never
   auto-run.
7. **Agent-consumable output.** The deliverable is **structured findings + concrete edit proposals**, not
   a 4500-word essay. A future agent should be able to read the retro doc and the journal entries cold and
   act on them.

## Interaction method

Use `AskUserQuestion` for choices from a known set (scope when several threads match, which curation
proposals to apply, the FAIL routing target, an execution backend for a big refactor). Call `ToolSearch`
with `select:AskUserQuestion` first if its schema is not loaded. Free-form questions stay inline. Ask one
question per turn; never silently skip a question.

In a channel session (`redis-channel` active), `AskUserQuestion` **cannot** be called — inline the choices
in your reply text instead, following the canonical channel-inline convention in
`saga/skills/brainstorm/SKILL.md` (do not duplicate its wording here).

Use **repo-relative paths** in every generated document and proposal. The one deliberate exception is a
GLOBAL/CROSS-PROJECT directive target under `~/.claude/` — an absolute path **on purpose**, because the
file genuinely lives outside this repo (see the contract below).

---

## THE TIERED SELF-EDIT SAFETY CONTRACT

This is the load-bearing safety rule of the engine. Read `references/self-edit-safety.md` for the full
presentation format; the gate itself is:

> **AUTO-APPLY is ONLY a PURE ADDITIVE APPEND of a NEW journal entry (LEARNINGS / DECISIONS / QUEUED /
> ARCHIVE). ANY delete, modify, or move of existing lines is PROPOSE-DIFF-AND-WAIT.**

- **AUTO (no confirmation):** appending one **new** entry to `LEARNINGS.md`, `DECISIONS.md`, `QUEUED.md`,
  or `ARCHIVE.md`. Nothing existing changes — the file only grows by a self-contained block.
- **PROPOSE-DIFF-AND-WAIT (show the diff + `AskUserQuestion` apply / skip / modify; NEVER auto-apply):**
  - any **edit** to an existing journal entry (the curation sweeps);
  - a **QUEUED → ARCHIVE move** — it *deletes* lines from `QUEUED.md`, so it is **propose, not auto**,
    even though the ARCHIVE side is an append;
  - the **`.claude` auto-memory** — `MEMORY.md` and its topic files;
  - **directive files** (the repo `CLAUDE.md`, the global `~/.claude` directives);
  - the **saga SKILLs themselves — INCLUDING `skills/retro/SKILL.md`**: `/retro` may
    *propose* a diff to its own skill, but it **never self-applies** one.

**Directive surfaces are NOT one bucket.** Disambiguate before proposing:

- **(a) IN-REPO** — the repo `CLAUDE.md` and the lifecycle SKILLs. (This plugin has **no `agents/` dir**;
  the convention is **generic agents**, so there is no in-repo agent file to edit.) A normal
  propose-diff-and-wait, repo-relative path.
- **(b) GLOBAL / CROSS-PROJECT** — `~/.claude/CLAUDE.md`, `~/.claude/agents/*.md`, and antigravity
  directives. These live **OUTSIDE this repo and affect EVERY project.** A global/cross-project proposal
  carries an **EXPLICIT warning in the diff header**:
  > **WARNING: this changes your GLOBAL Claude config and affects ALL projects, not just this repo.**

**Never auto-launch** a destructive self-edit or a big refactor. The backend is `inline` — the only
value since issue #1030, per `../../references/operator-choice.md` §1 — so what is put to the
operator is whether to start the work at all, never which backend runs it. Nothing starts without
the operator's pick.

---

## Phase 0 — Enter, scope, restore

Establish what this retro covers before gathering any evidence.

**Parse the input.** Take the target from command arguments or the active artifact:

- a **saga id / issue (`#N`) / branch** → a **thread-scoped** retro (one work thread);
- a **time window** ("last week", "since 2026-05-20") → a **meta-retro** over a span of work;
- bare "retro" with an in-flight thread → thread-scoped on that thread; otherwise ask once: "What should
  I retro — a thread (issue / branch / saga), or a time window?"

**Restore (read-only, never mint).** For a thread-scoped retro, anchor on the saga:

```bash
python3 plugins/saga/scripts/saga.py restore --saga-id <issue-N|task-slug>
```

`restore` is cold and branch-agnostic (saga-spec §7.2). If no saga is found, `/retro` still runs from
`gh` + git + docs. **Never mint a saga** from `/retro` — it is saga READ-ONLY (`saga.py save` is never
called).

**Announce scope.** State the mode (thread-scoped vs meta-retro), the thread / window, and what evidence
will be gathered. The **stale-base guard is a WINDOW freshness check** that runs in Phase 1 for the
time-windowed mode only; a **thread-scoped retro computes no git window**, so instead it verifies the
saga / PR evidence is **at the current HEAD** (a stale-thread analogue of the same discipline).

---

## Phase 1 — Gather evidence (READ-ONLY)

All evidence is read-only. See `references/retro-passes.md` for the exact queries.

**1.1 Time-windowed mode — run the stale-base/wrong-today BLOCK guard FIRST.** Before any window query:
fetch `origin/<default>`, read the latest commit date, and compare it against the window. Compute **today
from the session reminder's `## currentDate`, NEVER from the `date` command** (a containerized clock can
be hours off). If the latest commit predates `(today − window)`, **BLOCK** with an explanation and an
`AskUserQuestion` (confirm today / re-fetch / proceed-anyway), because the window would otherwise
fabricate a narrative from near-zero commits. The graceful, **disclosed** skip paths — no remote, detached
HEAD, offline fetch failure — proceed with the reason carried into the retro narrative
(`references/retro-passes.md`). Thread-scoped retros skip this block and run the HEAD-freshness check
instead.

**1.2 Lean git metrics + diff-vs-last.** Run the **lean** subset of gstack's forensics, **solo-framed**
(the gstack team-performance framing — leaderboard, praise, streaks, tweetable, global, week-over-week —
is **shed**). Report them **in prose** (commits in scope, files / hotspots touched, test-vs-prod balance,
PRs referenced), then **diff vs the last retro** so the retro compounds.

**1.3 Saga trajectory.** Read the whole tick chain, not just the last frame:

```bash
python3 plugins/saga/scripts/saga.py ticks --saga-id <issue-N|task-slug>
python3 plugins/saga/scripts/load_saga_context.py --repo <owner/repo> --issue <N>
```

`ticks` (`saga.py:755`, CLI `:1099`) surfaces how the phase advanced, when blockers cleared, which
questions got answered — the trajectory of the work.

**1.4 PR / issue / check evidence (gh READ-ONLY).** Read the PRs, issues, review decisions, and CI checks
for the thread or window via `gh` — read commands only (`gh pr view`, `gh issue view`, `gh pr checks`).
Never `gh issue create`, never `gh pr merge`.

**1.5 Session-transcript skeletons.** Reuse the transcript-forensics substrate — **file-mediated,
context-safe**. Identify sessions from the saga / branch for a thread-scoped retro, or via
`discover_sessions.py` for the windowed mode; extract each with `extract_session_skeleton.py` to a scratch
dir; an **optional generic-sub-agent fan-out (one per session)** synthesizes them — offered per
operator-choice, **never** via an `agents/` dir (this plugin has none; use generic `Explore` / `Task`).
The orchestrator never reads a raw `.jsonl` or a skeleton file — paths only.

**1.6 R12 orchestration telemetry (read-only).** Run the override-rate reader to surface
backend choice-vs-recommendation signals across all sagas:


This surfaces three R12 signals:

- **Override rate** — fraction of decisions where the operator's explicit pick differed from
  the recommender's suggestion (only sagas where both `orchestration_recommended` and
  `orchestration_operator_choice` are recorded count toward the denominator).
- **Tier direction** — of those overrides, how many escalated to a richer backend
  (over-tier) vs. de-escalated to a cheaper one (under-tier).
- **Budget-exhaustion / capability degradation** — sagas with a non-empty
  `orchestration_downgrade` note (recorded by U12 on off-host resume).

**Zero-data contract**: if no sagas have been recorded with recommendation data yet, the
reader reports "no data yet" rather than a rate. Do not fabricate a narrative from zero data;
carry the "no data yet" state into the retro doc as-is and note that signal accrues over time.

This pass is **read-only** — the reader never writes to disk. Include the output verbatim in
the Phase-1 evidence block. A non-zero override rate or a skew toward over/under-tier is
signal worth surfacing in Phase 2 interview and the Phase-3 retro doc, so any future default
re-weighting is evidence-driven (R12's intent: measure before re-weighting).

**1.6a Gate-divergence telemetry (read-only, issue #399).** Run the gate-divergence reader to
surface per-gate rubber-stamp rates across all sagas, alongside the R12 reader above:


This generalizes the R12 reader shape from one gate (orchestration-backend choice) to the
fleet's other interactive decision gates (mode selection, fix-vs-diagnosis-vs-rethink,
per-expansion opt-in, coordinator-level decisions — see
  the run record, which is where a gate interaction and its outcome are now recorded.
`gate_id`s). For each `gate_id`, it reports the rubber-stamp rate (fraction of interactions
where the operator's answer matched the offered default/recommendation), the interaction count,
and mean latency.

**Zero-data contract**: a `gate_id` (or the reader overall) with no recorded interactions
reports "no data yet" rather than a fabricated rate. Do not fabricate a narrative from zero
data; carry the "no data yet" state into the retro doc as-is and note that signal accrues over
time as instrumented gates fire.

This pass is **read-only** — the reader never writes to disk. Include the output verbatim in
the Phase-1 evidence block. A gate with a high rubber-stamp rate over enough interactions is
signal worth surfacing in Phase 2 interview as an auto-progression candidate — but this reader
produces the evidence only; it never itself widens any allowlist (issue #399's own non-goal).

**1.7 OutcomeOrchestrator realized economics (read-only, R24).** When the retro covers an **outcome**
(a DAG of leaf sagas), read its per-outcome realized-cost rollup — the falsifiable proof of the
cost-vs-operator-time thesis — from whatever cost record the run kept, or live
via `scripts/outcome_costs.py` `rollup(spec, store)`. Surface, in the evidence block:

- **tokens / operator_touches / retries** (per outcome) + **by_executor** (which backends actually ran);
- the **DAG-vs-one-thread** verdict — `wall_seconds_parallel` (critical path) vs `wall_seconds_serial`
  (the one-long-thread sum) and **`beat_one_thread`** — so the retro states, with numbers, whether the
  coordinated DAG actually beat a single inline thread (or did not — both are honest learnings);
- `sunk` (cost of pruned leaves, R33) — work spent then abandoned, a real signal for the interview.

**Zero-data contract** (same as 1.6): an empty rollup is **"no data yet"** — carry it verbatim, never
fabricate a zero. This pass is **read-only**; the leaves produce the telemetry (`record_cost`), the retro
only consumes it.

**1.8 Provenance-manifest signals (read-only, R16/R18).** Run the manifest reader beside the
override-rate reader (1.6) to surface parroting count, disposition rate, and the adjudicated
verified-vs-inferred/not-checked ratio across the manifest tree:

```bash
python3 plugins/saga/scripts/manifest_reader.py --root <saga-manifests-dir> [--json]
```

This surfaces three R7/R16/R18 signals:

- **Parroting count** — claims a producer claimed `verified` that Claude's adjudication refuted
  or found unsupported (R7 taxonomy, defined once in `provenance_manifest.py`, never redefined here).
- **Disposition rate** — the fraction of manifests landing `ran-as-requested` /
  `fell-back-to-claude` / `substituted-engine` (R18).
- **Adjudicated verified ratio** — `verified / (verified + inferred + not-checked)` among
  adjudicated claims (R16), the confidence signal `/qa` also consumes directly (Phase 2.x there).

**Zero-data contract** (same as 1.6/1.7): an empty manifest tree is **"no data yet"** — carry it
verbatim, never fabricate a rate. This pass is **read-only and advisory-only** (R8/R12): a low
verified ratio or a nonzero parroting count is signal for the interview, never a gate.

**1.9 What the run itself recorded (read-only).** Read the run record for this issue —
`uv run python plugins/saga/scripts/run_record.py show <issue>` — and take the run's own account of
what happened: the review cycles and their results, each unit's merge-turn state and merged tip, the
release state with its reviewed head and landed commit, the functional-test scenarios with their
terminal states, and the post-merge cycle count. Read the journal entries the change shipped with
beside it.

The engine-benchmark, calibration, staleness, capability-Elo, control-chart, spend and
tier-efficacy readers that used to sit here are **gone** (issue 1028). They read ledgers and an
engine registry that the simplification removes, and each one produced a proposal nobody applied.
What replaced them is narrower and true: one file per run, written by the run, plus the journal.

This pass is derive-on-read: it writes nothing back to the record and applies no change. Carry what
it finds into the interview and the retro doc as **PROPOSE-DIFF-AND-WAIT** input. `/retro` remains
terminal and advisory: it writes no saga tick, and even an approved proposal must be handed to a
separate authorized implementation path — a proposal is never an authorization to edit, which is
what the retired readers' `approval_required` flag said and what still holds without them.

**Zero-data contract** (same as 1.6/1.7): a run with no record — work done before the record
existed, or outside a saga run — contributes nothing here. Carry that as "no run record for this
work," never a reconstruction.


---

## Phase 2 — Structured interview

Interview the operator, **grounded in the Phase-1 evidence** (not generic prompts). Use **free-form for
substance** and `AskUserQuestion` for routing / choices.

The substance questions (free-form): what shipped · what surprised · what slowed the work · what evidence
actually mattered · what should change. The full bank is in `references/retro-passes.md`. Anchor each
question in something Phase 1 found ("the saga shows round 3 re-opened on a test gate — what was the real
blocker?"), so the answers add signal the evidence cannot.

Channel-session fallback: inline the choices in reply text per the brainstorm convention (cited above) —
do not call `AskUserQuestion`.

---

## Phase 3 — Write the retro doc

Write a **concise, agent-consumable** retro to:

```
docs/retros/<saga-id-or-issue>-<date>.md
```

Structure per `references/retro-report.md`: structured findings linked to the Phase-1 evidence + the
**diff-vs-last** delta, not an essay. This is a **NEW doc → auto-write** — it is a fresh file, not an edit
to existing content, so it is outside the propose-gate.

---

## Phase 4 — Journal promotion, curation + transcendence marking

**PROMOTE (AUTO — pure append, per the contract).** Append **new** entries:

- generalizable findings → `LEARNINGS.md`;
- pattern / convention / tooling decisions → `DECISIONS.md`;
- deferred work → `QUEUED.md`;
- shipped / superseded items → `ARCHIVE.md`.

Each follows the existing journal entry format (the block-quote intros at the top of each file;
`references/retro-report.md` carries the templates). A pure append needs no confirmation.

**CURATE (PROPOSE-DIFF-AND-WAIT — the gstack-`learn` sweeps over the journal).** Run, and for each finding
show a diff + `AskUserQuestion` (apply / skip / modify):

- **staleness** — entries citing deleted files / merged-and-gone PRs / rewritten SHAs (Glob / `gh` check);
- **contradiction** — conflicting entries on the same topic / key (gstack `learn`'s contradiction sweep);
- **dedup** — near-duplicate entries collapsed (the **infiquetra addition** to the sweep set — in gstack
  this was a Stats *display* op, here it is a real Prune sweep);
- **journal-rule enforcement** — e.g. `MEMORY.md` over the ~24.4KB size rule, or an over-long index entry
  that should move detail to a topic file.

A `QUEUED → ARCHIVE` move (an item that shipped this thread) **deletes from `QUEUED.md`**, so it is a
**propose**, not an auto-append.

**MARK transcendence (PROPOSE-DIFF-AND-WAIT — the cross-repo `promote` feeder).** After promoting, look at
the `**Generalizable rule.**` lines this retro just touched (the entries it appended, plus any the
interview surfaced as cross-cutting) and propose a `**Transcendent.**` marker on the **select few** whose
rule would still hold in a repo of a *different stack or domain* — strip the entry's repo-specific nouns
and ask "is this still true and useful elsewhere?" Default to **not** marking: this is the sparing,
human-judgment **declare** feeder, not a bulk harvest — the `promote` skill's recurrence net catches the
latent cross-repo lessons this sweep does not.

- **Form + placement (frozen — do not redefine).** Exactly `**Transcendent.**` on its own line directly
  below the rule it elevates, with an optional one-line reason it crosses. The canonical form, the
  detection anchor, and the `<repo>:<hash>` source key are frozen in
  the promotion contract that lived in the removed `/promote` skill. `/retro` now carries the rule
  itself: a learning is promotable when it is repo-independent, evidence-backed, and stated as a rule
  a future reader could apply without this repository in front of them.
- **Tier.** It **edits an existing entry**, so it is **PROPOSE-DIFF-AND-WAIT** (never the Tier-1 AUTO
  append) — show the one-line insertion as a diff + `AskUserQuestion` (apply / skip / modify the reason).
  Skip any entry that already carries the marker (a human may have written it — idempotent, never
  double-mark).
- **Single-repo boundary (hard).** `/retro` writes the marker into **this** repo's journal and stops. It
  does **not** read other repos, cluster, dedup, or write `infiquetra-context-library` — that cross-repo
  collection and the gated context-library upsert are the separate `promote` skill. The marker simply
  waits in place for the next `promote` run to collect it.

---

## Phase 5 — Meta-improvement passes (net-new; ALL propose-diff-and-wait)

The passes neither source had, all gated (`references/retro-passes.md`):

- **(a) new-skill / plugin detection** — repeated friction that a new skill or plugin would remove →
  propose a `QUEUED.md` entry or a `mission-control` issue.
- **(b) refine-lifecycle** — propose diffs to the saga SKILLs when the thread exposed a
  gap or a wrong instruction (including `skills/retro/SKILL.md` — proposal only, never self-applied).
- **(c) refine-directives** — propose diffs to the **repo `CLAUDE.md`** (in-repo) or the **global
  `~/.claude` directives** (global carries the cross-project warning, per the contract).
- **(d) memory pruning** — propose curation of the `.claude` auto-memory (`MEMORY.md` + topic files) per
  the journal-rule + staleness + contradiction sweeps.

A **big multi-file refactor** surfaced by any pass → **OFFER to start it**, and nothing more: the
backend is `inline`, the only value since issue #1030 (`../../references/operator-choice.md` §1).
**Never auto-run** it.

---

## Phase 6 — Route

Surfaced follow-ups exit to:

- **`mission-control`** — a follow-up that should become an SDLC issue, prepared there;
- **`QUEUED.md`** — a follow-up that is durable backlog, not yet an issue.

`/retro` is terminal: there
is **NO saga write** (the `->retro` advance is dead wiring; `/retro` is saga READ-ONLY).

---

## Hard boundary

`/retro` gathers evidence, interviews, writes the retro doc, appends journal entries, proposes curation +
meta-improvement edits, and routes — then stops. It does **NOT**:

- mutate the world — `gh` / `git` are **read-only**; it never opens / edits / merges an issue or PR, never
  files SDLC issues (mission-control owns the SDLC), never deploys;
- **auto-apply a non-journal edit** — every delete / modify / move (curation, auto-memory, directives,
  lifecycle SKILLs including its own) is propose-diff-and-wait;
- **auto-launch a backend or a destructive self-edit** — backends are offered, never started;
- **write the saga** — terminal phase, saga READ-ONLY, `saga.py save` is never called;
- **mutate the SDLC** — issues / boards / labels belong to mission-control;
- add an `agents/` dir — the transcript fan-out uses **generic** `Explore` / `Task` agents.

It never blocks the router.

---

## Reference files

- `references/retro-passes.md` — the multi-pass procedure: the stale-base guard pre-flight, the lean-metrics
  git queries (team-perf shed, solo-framed) + diff-vs-last, the gstack-`learn` curation sweeps
  (staleness / contradiction / dedup / rule-enforcement), the transcript-review fan-out (reusing the
  transcript-forensics scripts + operator-choice + generic agents), the interview question bank, and the three
  self-refinement passes + memory pruning.
- `references/self-edit-safety.md` — the load-bearing tiered self-edit contract: the auto vs
  propose-diff-and-wait gate, the propose-diff presentation format, the in-repo vs global/cross-project
  directive disambiguation with the cross-project warning, and never-auto-launch.
- `references/retro-report.md` — the `docs/retros/` writeup shape (agent-consumable structured findings,
  links + diff-vs-last) and the journal-promotion entry templates (LEARNINGS / DECISIONS / QUEUED / ARCHIVE).
- `../../references/operator-choice.md` — the execution-backend contract; one value, `inline`,
  since issue #1030 archived the others.
- `../brainstorm/SKILL.md` — the canonical channel-inline convention (cite, never duplicate).
- `../../references/saga-spec.md` — the saga contract (`restore` / `ticks`; `/retro` is read-only).
- `../../scripts/manifest_reader.py` — R7/R16/R18 telemetry reader: scans the provenance-manifest
  tree for parroting count, disposition rate, and the adjudicated verified ratio (Phase 1.8).
  Zero-data reports "no data yet"; read-only and advisory-only (R8/R12); `--json` for
  machine-readable output.
- `../../references/benchmark-loop.md` — the benchmark propose-not-commit gate: suite versioning
  (immutable `suite_id`), threshold semantics, and how a contradiction becomes a Phase-5(f)
  proposal a human applies by hand.
