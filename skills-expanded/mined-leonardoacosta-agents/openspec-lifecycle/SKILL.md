---
name: openspec-lifecycle
description: "Openspec change lifecycle: draft -> implementation -> closure -> archive -> promotion. Use for multi-session work."
metadata:
  type: workflow
---

# OpenSpec Change Lifecycle

Planned work in this repo runs through `openspec/`. The tree:

```text
openspec/
├── changes/<slug>/            # active proposals
│   ├── proposal.md            # why + scope (required)
│   ├── design.md              # technical design (only when the design is non-obvious)
│   ├── tasks.md               # checkbox waves / phases (required)
│   └── specs/<domain>/spec.md # requirement deltas this change introduces (when applicable)
├── changes/archive/YYYY-MM-DD-<slug>/   # completed or wontfix'd changes
└── specs/<domain>/spec.md     # canonical long-lived requirements
```

## 0. Does this work need a proposal?

| Work | Route |
| --- | --- |
| Single-session fix, <=3 files, no requirement change | No proposal. Bead + conventional commit is enough |
| Multi-session, multi-file, or changes a documented behavior/requirement | Proposal |
| Fleet-wide pass (every satellite, every module) | Proposal, with the fleet enumerated in tasks.md so progress is checkable |
| Emergency fix during an incident | Fix first; backfill a bead. Write a proposal only if follow-up waves remain |

When in doubt: if you cannot state the "done" criterion in one sentence, it needs a proposal.

## 1. Draft

1. Create the bead first: `bd create` (or claim the existing one) — the proposal commit cites it.
2. `openspec/changes/<slug>/proposal.md` — slug is kebab-case and imperative
   (`slim-wholesale-bicep-module-params`, `fix-sql-publicna-drift`). Contents:
   - **Why** — the problem, with evidence (a run ID, an audit finding, a docs/notes/ report)
   - **What changes** — scope boundary, explicitly including what is OUT of scope
   - **Impact** — which envs, which pipelines, migration/rollback notes if destructive
3. `tasks.md` — numbered phases, each a checkbox list. Phases must be independently
   verifiable; a phase whose completion cannot be evidenced is mis-cut. Link beads inline
   with `[beads:ws-xxxx]` markers on the task lines.
4. `design.md` — only when there is a real design decision (alternatives + trade-offs).
   A design.md restating the proposal is noise; delete it.
5. Commit: `spec(<scope>): draft proposal — <summary> (ws-xxxx)`.

A proposal is NOT a license to expand scope later. Scope changes get a proposal edit in its
own commit, with the why.

## 2. Implement in phases

- One phase at a time, in order. Cross-phase drive-by edits break the evidence chain.
- Implementation commits carry the phase and slug:
  `feat(bicep): port wholesale/data/* onto satellite-database inference pattern (Phase 2, <slug>)`
- Each phase ends with a bookkeeping commit: `docs(<slug>): close Phase N ...` that ticks the
  boxes in tasks.md AND names the evidence.

### The evidence bar for "done"

A checkbox is ticked only with **runtime evidence**, never "it compiles":

| Change class | Required evidence |
| --- | --- |
| Bicep behavior change | Deploy run ID + the predicted-vs-actual what-if delta |
| Bicep refactor (params/comments/consolidation) | `what-if` showing ZERO resource-property drift in EVERY env the module deploys to |
| Pipeline change | A green run of the changed pipeline (run ID), including the stage the change touched |
| Sync-lane / data-plane change | The lane's converge output (counts applied/skipped) |
| Docs change | The page rendering in the docs-site build |
| Deletion/retirement | Proof the retired path is dead (no remaining callers — grep output; the retired def disabled) |

Degenerate closures are legitimate and get named honestly:
`close Phase 0 as vacuous`, `close Phase 3 (already satisfied)` — with one line of proof.

## 3. Ship: apply and archive

When all phases are closed:

1. Final commit: `feat(<slug>): apply and archive`.
2. Move the folder: `openspec/changes/<slug>/` -> `openspec/changes/archive/YYYY-MM-DD-<slug>/`
   (date = archive date).
3. Promote requirement deltas: fold `changes/<slug>/specs/*` into the canonical
   `openspec/specs/<domain>/spec.md` so the long-lived spec reflects post-change reality.
4. Post-archive verification is allowed and encouraged as a follow-up commit when the real
   deploy lands later: `docs(<slug>): post-archive real-deploy verification` with the run ID.
5. Close the beads; update CLAUDE.md/skills if the change altered a documented behavior
   (dated correction — delete the stale claim in the same commit).

## 4. Abandon honestly

Proposals that will not ship get archived, not deleted and never left rotting:

- `openspec: archive N abandoned proposals (wontfix)` — move to `archive/` with a one-line
  wontfix reason added to the proposal header.
- A proposal overtaken by events ("effectively done" by other work) archives with that note:
  `openspec: archive 2 effectively-done proposals`.
- Close the linked beads with the same disposition.

Anything sitting in `changes/` is claiming to be in-flight. If it has not moved in weeks and
no bead is in_progress, it is a candidate for §4 — flag it.

## 5. Session hygiene inside a change

- Start of session: read the change's `proposal.md` + `tasks.md` BEFORE reading code. The
  next unchecked box is your task; do not cherry-pick a later, more interesting one.
- End of session mid-phase: commit what is coherent, tick nothing you cannot evidence, and
  leave a `docs(<slug>):` breadcrumb commit or bead note stating exactly where the phase
  stands and the next probe/step.
- Never tick a box in the same commit that implements it unless the evidence is already in
  hand (run already green). Ticking-in-advance is the most common corruption of the record.
