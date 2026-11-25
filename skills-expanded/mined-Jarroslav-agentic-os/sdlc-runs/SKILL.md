---
name: sdlc-runs
description: >-
  Read-only inspector and resumer for agentic-sdlc heavy-pipeline runs kept
  under docs/superpowers/runs/. Invoke when the user asks what a run's status
  is, wants to list or drill into past pipeline runs, needs to pick back up an
  interrupted run, or is on a skill-only host (for example, Codex) that has no
  `sdlc:status` slash command and needs the same behavior exposed as a skill.
  Trigger phrases: "sdlc status", "what's the run status", "list sdlc runs",
  "resume the pipeline", "resume run <id>", "is the run stuck", "sdlc:status".
  Never mutates a completed run, and never resumes an aborted one without an
  explicit yes. Not for: starting new runs (sdlc-guided / sdlc-auto),
  editing run artifacts, or lightweight task flows — inspection and explicit
  resume handoff only.
version: 0.1.0
license: Apache-2.0
discoverable: true
author: agentic-os
---

# sdlc-runs

## What this does

Inspects `sdlc-engine` heavy-mode runs and, on explicit confirmation, hands off
a resume request to `sdlc-engine`. It is a stand-in for the legacy `sdlc:status`
slash command on hosts that only support skills (Codex is the reference example) —
same information, same resume gate, exposed through the skill interface instead
of a command.

This skill never executes or re-runs a pipeline phase itself. It decides *what*
should resume and *why*, then delegates the actual execution to `sdlc-engine`.

> Default posture is read-only. When `.agentic/state/runtime.sqlite3` exists,
> it is the authority. Query it with `run.status`; use `legacy.export` only to
> regenerate compatibility views. Never repair authoritative state by editing
> exports, legacy JSONL, or human documents. When SQLite is absent, the legacy
> reconciliation rules below apply. Anything that restarts pipeline work
> requires clear user intent; ambiguous requests require a direct question.

## When to invoke

- The user asks for the status of an SDLC run, all runs, or a specific run ID.
- The user wants to resume a run that stopped mid-phase.
- The user is on a host without slash-command support and asks for `sdlc:status`.
- Another skill or the orchestrator needs a run's current phase/state before
  deciding whether to dispatch further work.

## Guardrails

| Rule | Effect |
|---|---|
| Completed runs are immutable | Never mutate a run whose authoritative state is `completed`, `failed`, or `cancelled`. |
| Aborted runs need explicit consent | Never resume a legacy run marked `aborted` without the user answering yes to a direct prompt. |
| Legacy event log is append-only | For runs without SQLite, never rewrite or truncate `events.jsonl`; corrections are additive appends. For SQLite-managed runs, record events through runtime operations and regenerate exports. |
| Legacy log beats snapshot | Only when SQLite is absent, treat `events.jsonl` as ground truth over `meta.json` and correct the snapshot. For managed runs, SQLite is authoritative. |
| Resume outcome comes from runtime state | After a failed or unclear SQLite resume, re-read `run.status` and report its actual state; never assume `interrupted`, force a state, or retry blindly. |

Blast-radius shape of this skill's own actions:

| Action | Tag | Notes |
|---|---|---|
| List runs, render catalog, compute status line | R0 | Read-only, no writes. |
| Correct `meta.json` phase fields, append `status.repaired` / `work_item.reconciled`, mirror JSONL ledgers, add a Markdown history row | R1 | Confined to run artifacts under `docs/superpowers/runs/` and `docs/superpowers/work-items/`. |
| Hand off a confirmed resume to `sdlc-engine` | R2/R3 (downstream) | This skill doesn't perform the repo writes or external side effects itself — it only issues the confirmed handoff. The resumed phase may touch tracked files (R2) or trigger external sync (R3); that's why the resume prompt is a hard gate. |

## Reading a project's own pipeline state

When `.agentic/agentic-sdlc/config.json` names a neutral state file, read it alongside this package's run
ledger. For whatever the project's pipeline is currently running, that file is
the authority: active pipeline, current role, which roles may come next,
serialized gate results, changed files and blockers all come from there rather
than from anything inferred here.

Status stays read-only unless the user explicitly asks to resume — and a resume
re-enters the project's orchestrator, never one of its fleet workers.

## Inputs

- Optional run selector: a run ID, `latest`, or nothing (list mode).
- Optional resume intent, expressed by the user after seeing a run's status.
- The on-disk run corpus under `docs/superpowers/runs/` (see below).
- The work-item ledger quartet (canonical + run-local, Markdown + JSONL).

## Records read and written

| Record | Path | Role |
|---|---|---|
| Run directory | `docs/superpowers/runs/<run_id>/` | Enumerate all run directories; sort by directory name descending (newest first) for list mode. |
| Mutable snapshot | `meta.json` | Per-run status snapshot. Fields referenced: `meta.status`, `meta.started_at`, `meta.json.phases`, `phases[N].completed_at`, `meta.json.current_phase`, `meta.json.work_item.canonical_path`, `meta.json.work_item.run_mirror`, `meta.json.task_input`. |
| Event log | `events.jsonl` | Append-only run history, one JSON object per line. Authoritative on any conflict with `meta.json`. |
| Requirements doc | `requirements.md` | Per-run; show only the first 10 lines. |
| Complexity doc | `complexity.json` | Per-run; show formatted in full. |
| QA report | `qa-report.md` | Per-run; show only the last 20 lines, and only if the file exists. |
| Gate ledger | `decisions.jsonl` | One row per gate, formatted. |
| Run-local work item | `<run_dir>/work-item.md` | Run-local Markdown mirror of the work item. |
| Run-local work-item ledger | `<run_dir>/work-item-events.jsonl` | Run-local append-only work-item history. |
| Canonical work-item ledger | `docs/superpowers/work-items/work-item-events.jsonl` | Global append-only work-item history across all runs. |
| Canonical work item | path from `meta.json.work_item.canonical_path` | Canonical Markdown work item, outside any single run's directory. |

This skill never talks to the external ticket/MR backend directly — it only
reads and reconciles these local ledger mirrors. Adapter sync into and out of
these files is somebody else's job; this skill just trusts the append-only
layers over the mutable ones when they disagree.

## Operating steps

If `.agentic/state/runtime.sqlite3` exists, inspect the run through the versioned runtime status/export operations first. Do not infer authoritative state from an older snapshot or event log, and do not apply the legacy repair procedures below.
If any required runtime operation is missing, stop with a blocked status.

### SQLite-backed run inspection and resume

1. Send `run.status` for the selected run ID. Its state, revision, coordinator
   lease epoch, and metadata are authoritative. Use `run.export` to inspect
   assignments, messages, events, evidence, and dispatch reservations. If the
   user needs the fixed display catalog below, call `legacy.export` first; its
   regenerated files are for display only, never authority.
2. If the run is `running`, report its state and do not acquire another lease.
   Before a planned host restart or interruption, the current coordinator must
   transition the run to `interrupted` with `run.transition`, then verify that
   state with `run.status` before stopping. If the coordinator stopped
   unexpectedly and left the run `running`, this bundle has no lease-expiry
   takeover operation: report the run as blocked and do not steal its lease.
   For `interrupted`, `waiting_for_user`, or `reconciliation_required`, proceed
   only after the confirmation rule below is satisfied. If `waiting_for_user`
   represents an unresolved gate, inspect `run.export` for its gate ID and
   artifact reference, verify the current artifact hash, and obtain the user's
   decision on that specific artifact/action. A resume request alone is not
   gate approval. Carry the gate ID, artifact reference/hash, and exact user
   response into the handoff. If the pending gate or current artifact cannot be
   established, stop and ask rather than advancing. Never resume a terminal run
   or infer a resume from a stale export.
3. Before acquiring a lease, preflight both required handoff inputs using the
   authoritative `run.status` metadata and `run.export` events already read:
   require a non-empty `task_input` and select exactly one incomplete phase
   from coordinator-owned runtime phase events. If either check fails or phase
   selection is ambiguous, stop for reconciliation while leaving the current
   lifecycle state unchanged. Do not call `run.resume` and do not source either
   value from a compatibility export.
4. Send `run.resume` with the same run ID and a new coordinator ID. Immediately
   query `run.status` again and retain its revision and lease epoch for every
   subsequent mutation. If resume fails or its outcome is unclear, query
   `run.status` again and report the actual state; never assume it remains
   interrupted or retry blindly. A missing database blocks the handoff; do not
   fall back to legacy files.
5. Re-read `run.export` after acquiring the lease and verify that the selected
   incomplete phase still matches the preflight result. If it changed or is no
   longer unambiguous, transition to `interrupted` under the newly acquired
   lease, verify with `run.status`, then stop for reconciliation. If the prior state was
   `reconciliation_required`, resolve each external action's real outcome with
   `external.reconcile`, using the newly returned coordinator ID, lease epoch,
   and current revision. Do this before redispatch. If the outcome is unknown,
   record it as `uncertain`, leave the run blocked in reconciliation, and never
   repeat the action or infer success.
6. Resume existing assignment IDs with their recorded owners and acceptance
   criteria. Do not create replacement assignments to make stale work appear
   complete. If an owner is unavailable or work cannot be mapped unambiguously
   to its assignment, record the limitation and escalate rather than altering
   the assignment history.
7. Dispatch/resume work under the persisted run and assignment budgets. Record
   actual dispatch outcomes with `task.result`, and assignment state changes
   with `assignment.transition`, using current revisions and lease fencing. Do
   not mark work complete from a worker's narrative alone; validate its owned-
   path diff and acceptance evidence first.
8. Before reporting the resumed work complete or handing off, query authoritative
   state again. Any pending, running, waiting, or escalation-required assignment
   blocks a completion claim. If this host's adapter cannot produce the trusted
   claims required by `run.complete`, leave the run active and state that host
   limitation.
9. Emit the status line using lifecycle state and metadata from `run.status`,
   and phase from the runtime phase events selected above. Use the recorded
   branch/precondition; render any missing display field as `unknown` rather
   than filling it from a compatibility export.

User-owned files, including checkpoint/fixture inputs, are immutable evidence: preserve them byte-for-byte. Store mutable orchestration progress only in managed runtime state and its regenerable exports. A checkpoint file may identify a run but cannot authorize changes to SQLite or be rewritten to reflect resumed progress.

### Legacy-file operating steps (SQLite absent only)

Use the following numbered operating steps only when `.agentic/state/runtime.sqlite3` does not exist. When it exists, follow the SQLite-backed sequence above and do not read legacy snapshots or event logs as authority.

1. **Enumerate.** List `docs/superpowers/runs/`, sorted by directory name
   descending. If no run was specified, show the list (or the newest run's
   summary) and stop unless the user picks one.
2. **Load.** For the selected run, read `meta.json` and `events.jsonl`.
   - If `events.jsonl` is missing or contains malformed lines, surface an
     audit warning and continue using `meta.json` alone — don't block on a
     broken log.
3. **Detect staleness.** If `meta.status` reads `running`, apply the stale-run
   check (below) and reclassify to `interrupted` if it fires.
4. **Reconstruct phase state.** Whenever `meta.json.current_phase` or
   `meta.json.phases` is missing, stale, or was never populated for a phase,
   derive the real phase state from `events.jsonl`: pair each phase's
   `phase.started` event with whichever terminal event (`phase.completed`,
   `phase.failed`, `phase.interrupted`) follows it.
5. **Reconcile snapshot vs. log**, if steps 3–4 surfaced a disagreement (see
   below).
6. **Emit the status line** (verbatim format below).
7. **If inspecting a specific run**, render the catalog in the fixed order
   below.
8. **If the user asks to resume a legacy run**, do not hand it to `sdlc-engine`.
   The engine requires a SQLite-backed run and there is no supported legacy-state
   migration path in this bundle. Report that resume is blocked until a
   supported migration exists; never fabricate a database run from JSON files.

## Reconciliation rules

These legacy repair procedures apply only when `.agentic/state/runtime.sqlite3`
is absent. With SQLite present, use the coordinator-fenced runtime operations
and regenerate compatibility files with `legacy.export`. If a required
operation is unavailable, block and report it rather than editing exported
state.

### Stale-"running" detection

Reclassify a run's status from `running` to `interrupted` when **both** hold:

- `meta.started_at` is more than 1 hour in the past, **and**
- no `phases[N].completed_at` timestamp falls within the last 30 minutes.

### Missing or malformed event log

Surface an audit warning and continue with `meta.json` alone. Don't attempt
partial reconstruction from a log you can't fully parse.

### Snapshot vs. reconstructed event history

> Append-only history can't be half-written by a crash the way a mutable
> snapshot file can. When the two disagree, the log wins — always correct
> the snapshot toward the log, never the reverse.

1. Confirm the discrepancy and the intended fix with the user.
2. Rewrite only `meta.json`'s phase-status fields to match the reconstructed
   state.
3. Append a `status.repaired` event to `events.jsonl`, with the changed
   fields in its data payload.
4. If the append itself fails: warn, and require explicit user confirmation
   before continuing any further action on this run.

### Work-item ledger conflicts

Trust priority, highest first:

1. Run event log (`events.jsonl`)
2. Canonical work-item JSONL (`docs/superpowers/work-items/work-item-events.jsonl`)
3. Run-local work-item JSONL (`<run_dir>/work-item-events.jsonl`)
4. Canonical Markdown work item (`meta.json.work_item.canonical_path`)
5. Run-local Markdown work item (`<run_dir>/work-item.md`)

Repair procedure:

1. Confirm the repair with the user before touching anything.
2. Update the Markdown snapshots (canonical and/or run-local) and the mutable
   snapshot (`meta.json.work_item.*`) to match the highest-priority source.
3. Append the outcome to `events.jsonl` as a `work_item.reconciled` event —
   its payload distinguishes which of the two reconciliation directions fired
   (canonical-sourced vs. run-local-sourced) and which fields changed.
4. Mirror the change into whichever JSONL ledgers exist (canonical and/or
   run-local).
5. Add one row under the `## History` marker in the affected Markdown file(s).
6. Proceed with whatever the user originally asked for (typically: resume).

### External-sync adapter receipts

| Adapter receipt | Markdown state | Action |
|---|---|---|
| Success, recorded in JSONL | Still shows pending | Update Markdown, mirror the change. No user confirmation needed — this is forward sync, not conflict repair. |
| Failure, recorded in JSONL | Shows failure already | Leave the failure in Markdown history as-is. Do not force a reconciliation. Leave the run resumable. |

## Resume confirmation

An unambiguous, current user instruction that explicitly names the run and asks
to resume it (for example, “resume run `<id>”) is confirmation for that resume
only; it does not approve an unresolved gate, authorize a separate external
action, or increase a budget. Do not ask for a second confirmation in that
case unless the planned resume would repeat an external action with an
uncertain outcome; reconcile that action first. A generic “continue”, a status
question, or an instruction that does not identify the run is not sufficient:
show the target phase and overwritten outputs with this prompt and wait for an
explicit yes. A legacy `aborted` status remains non-resumable in this bundle
even after explicit yes; approval cannot replace the missing migration path.
High-risk or external actions still use their own approval gates.

Use this exact template when intent is ambiguous for a SQLite-managed run:

```text
Resume by re-running Phase <N> (<phase-name>)? It will overwrite that phase's outputs and continue. (yes/no)
```

On anything other than an explicit yes, stop — do not hand off.

### Handoff

For SQLite-managed runs only, hand off after `run.resume` with:

- the run's original mode (hitl or autonomous),
- `task_input` sourced from authoritative runtime metadata. New runs preserve
  the original input at creation. If an older managed run lacks it, stop; do
  not recover it from a mutable compatibility snapshot,
- the existing `run_id`,
- the exact `coordinator_id`, `lease_epoch`, and revision returned by `run.resume`,
- any pending gate ID, current artifact reference/hash, and the user's exact gate response,
- a resume hint naming Phase `<N>`.

If a resume attempt fails, re-read and report the actual runtime state. Do not
force it to `interrupted` or mark it `aborted`; only retry after diagnosing the
failed operation and confirming that no partial state change occurred.

## Outputs

- **Status line** (machine-parsed, verbatim format):

  ```text
  <run_id>  <mode>  phase=<n>  status=<pending|running|waiting_for_user|interrupted|reconciliation_required|completed|failed|cancelled|aborted>  branch=<branch>
  ```

- **Catalog display**, for a specific run, in this fixed order:

  1. `requirements.md` summary — first 10 lines.
  2. `complexity.json` — formatted, in full.
  3. `meta.json.phases` table — status + timestamps per phase.
  4. `events.jsonl` — one row per event, with malformed-line warnings inline.
  5. `decisions.jsonl` — one row per gate.
  6. `qa-report.md` summary — last 20 lines, only if the file exists.

- **Audit trail**: for legacy runs without SQLite, reconciliation appends
  `status.repaired` and/or `work_item.reconciled` events to `events.jsonl` —
  never a rewrite, always a new line. For managed runs, record changes through
  coordinator-fenced runtime operations and regenerate compatibility exports.

- **Resume handoff**: a single dispatch to `sdlc-engine` per the Handoff
  section above, or no handoff at all if the user declines.

> Report only what the ledgers actually contain. Never infer or guess a
> phase's status when both `meta.json` and `events.jsonl` are silent on it —
> surface it as unknown instead.

## References

This skill has no bundled `references/` tree. Its scope is narrow enough —
parse two ledger formats, apply a fixed set of deterministic reconciliation
rules, hand off to exactly one downstream skill — that keeping the full
contract inline in this file is cheaper for a host to load than splitting it
out. Contrast with skills that fold a larger reference set in in (for example,
`code-review-orchestrator`'s `references/review-lenses.md`): this skill has no
equivalent, by design.

## Cross-references

- `sdlc-engine` — the orchestrator this skill resumes into. It is the
  mode-dependent phase runner for both hitl and autonomous runs; this skill
  never duplicates its phase logic, only decides where to re-enter it.
- Legacy command superseded: `sdlc:status`. This skill exists specifically for
  skill-only hosts (Codex is the example given) that can't expose that
  command directly.

## Non-goals

- Does not execute or re-run pipeline phases itself — it only decides what to
  resume and delegates to `sdlc-engine`.
- Does not modify a completed run, under any circumstance.
- Does not resume an aborted run without explicit user confirmation.
- Does not rewrite or truncate `events.jsonl` — corrections are additive
  appends only.
- Does not silently trust the mutable snapshot when the event log disagrees —
  always reconciles via the append-only source first, with user confirmation
  before any repair-write.
