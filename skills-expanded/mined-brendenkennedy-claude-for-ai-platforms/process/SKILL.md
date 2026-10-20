---
name: process
description: >
  The project operating system — phases with exit gates per `PROCESS.md` (repo root): P1 problem →
  P2 data discovery (+labeling) → P3 architecture → P4 features → P5 modeling/eval → P6
  delivery/retro → P7 monitoring. Carries the operating loop: live state in
  `.claude/memory/process/` (project-definition, phase-state, risk register, scope ledger, decision
  log), enforcement via `/gate` (no forward phase transition without a passed review), and the
  phase→skill map. Load when kicking off a project or phase, before starting to model, when scope or
  risk comes up, or when closing toward delivery. Triggers: what phase are we in, gate, gate review,
  gate debt, kick off, new project, problem statement, kill criteria, ready to model, start
  modeling, scope, scope creep, parking lot, risk, risk register, compute budget, experiment budget,
  retro, ship it, milestone, project plan, PROCESS.md, CRISP-DM.
---

# process — the phase-gate operating loop

> On-demand: load this when starting/advancing/closing a phase, or when scope, risk, or "where are
> we" comes up. The **canon is `PROCESS.md` at the repo root** — phases, gates, templates, and
> rationale live THERE (single source of truth; it wins on any conflict). This skill is the map of
> how that document runs *in this repo*: where state lives, what enforces it, and who does what.
> Never restate gate checklists here — read them from `PROCESS.md`.

## The pieces
| Piece | Where | Role |
|---|---|---|
| Canon | `PROCESS.md` (repo root) | phases P1–P7, exit gates, templates T1–T8, principles — the process itself |
| Project definition | `.claude/memory/process/project-definition.md` | archetype + lane fit, T1, challenged decisions, setup implications — written by `/intake` step 0; most of P1's gate evidence |
| Phase state | `.claude/memory/process/phase-state.md` | current phase, gate history, gate debt — written by `/gate` only |
| Risk register | `.claude/memory/process/risk-register.md` | live risks (T4); reviewed at every gate; new risks logged the moment they're found |
| Scope ledger | `.claude/memory/process/scope-ledger.md` | the v1 contract; the parking lot **is** `.claude/memory/roadmap.md` (one backlog, not two) |
| Decision log | `.claude/memory/process/decision-log.md` | append-only process-level decisions (scope, metric, kill/pivot, gate judgment calls) — via the `governance` protocol |
| Resource matrix | `.claude/memory/process/resources.md` | every service/store/endpoint the stack touches — env keys + credential references; kept in sync with `.env.example`; written by the infra lanes |
| Enforcement | `/gate` command | walks the current gate demanding evidence; records PASS or gate debt; refuses to advance otherwise |

## The operating loop
1. **Session start:** read `phase-state.md` — the current phase frames what work is in-bounds. Gate
   debt listed there is visible work, not history.
2. **During a phase:** work normally; the phase's domain skills carry the how (map below). When a
   risk appears → log it in the risk register *now*. When scope is proposed → parking lot
   (`roadmap.md`) by default; promotion needs the written gate (§3.3) and a decision-log line.
   When an experiment is proposed → it gets a written question + time/compute budget first (§3.6).
3. **Phase boundary:** run `/gate`. Evidence, not assent. BLOCKED verdicts leave gate debt — keep
   working the phase, don't slide forward.
4. **Session end:** `/wrapup` records the current phase + open gate debt in the session note.
5. **After shipping (P6):** the retro edits `PROCESS.md` itself and bumps its version — the process
   is a versioned artifact (Part V).

## Projects gate; ad-hoc asks don't
The loop above governs the **project thread**. A one-off analytical ask — "plot this CSV", "is
there a correlation here", "summarize this table" — is served directly: `eda`/`visualization`/
`statistics` still apply (they're about honesty, not ceremony), but no phase check, no gate, no
records beyond the conversation. The boundary: the moment ad-hoc work starts informing the
project's modeling decisions or produces artifacts the project will reuse, it enters the process
(findings recorded, splits respected). Unsure which mode the user is in? Ask — never
bureaucratize a quick question.

## Phase → skill map (who carries the "how" of each phase)
| Phase | Lean on |
|---|---|
| P1 Problem definition | `/intake` step 0 runs this interview → `project-definition.md` (most of the P1 gate evidence); `evaluation` for metric choice; `governance` for the decision log |
| P2 Data discovery | `eda` (the first-look audit), `data-acquisition` (APIs/scraping ingest), `datasets` (provenance, formats), `annotation` (when producing labels), `data-dvc`, `governance` → `data-governance` (licensing/PII) |
| P3 Data architecture | `datasets` (layout, manifest), `data-dvc` (versioning), `env-uv` (pinned env); the *shape* comes from `/bootstrap`, not P3's generic diagram |
| P4 Features / input representation | `datasets` (preprocessing vs augmentation, stats-on-train-only), `sql` (leakage-safe feature queries) + `wrangling` (dataframe work) when in those lanes, `config-hydra` (choices flow through config) |
| P5 Modeling & evaluation | `training`, `evaluation`, `statistics` (is the difference real), the tracker (the experiment log **is** the tracker), `pipelines` for cascades, `testing` before claiming anything works |
| P6 Delivery & retro | `reporting` + `/report` (the deliverable, evidence-cited), `visualization` (its figures), `serving` (if it ships as a scorer/endpoint), `testing` (clean rerun), `memory` (`/wrapup`), retro edits `PROCESS.md` |
| P7 Monitoring | `monitoring` (flip it on in `skillOverrides` at first deploy — drift, reference windows, retrain triggers), `evaluation`, the tracker + registry |

## Who runs this — deliberately NO project-manager agent
Same design call as `governance`'s "no governance-manager agent": process is applied **where the work
happens**, by the main session, because gates need the *user* in the loop (evidence, sign-off,
kill/pivot calls) and subagents can't interview the user. The main session wears the project-lead
hat; `/gate` is the moment it does so deliberately (PROCESS.md §3.7's hat-switching, made
mechanical). Specialist agents (`data-engineer`, `ml-engineer`, …) do phase *work* and flag
gate-relevant findings back up; they never advance phases.

## Gotchas
- **The phase-state file is written by `/gate` only.** Editing it by hand to advance a phase is the
  deliberate human override — never do it on the user's behalf; surface the blocked gate instead.
- **Iteration backward is free; skipping forward is not.** P5 results sending you back to P2/P4 is
  the process working. Starting P5 work while P4's gate is open is the process failing.
- **Don't duplicate the artifacts.** Experiment log = MLflow; parking lot = `roadmap.md`; feature
  hypotheses = the feature dictionary. One home each — a second copy is how one goes stale.
