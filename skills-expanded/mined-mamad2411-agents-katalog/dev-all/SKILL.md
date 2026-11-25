---
name: dev-all
description: Orchestrate the /dev methodology across ALL phases of a feature spec via a background ultracode run, one fresh agent per bounded (sub-)phase, sequentially. Handles the DB migration itself, splits oversized phases, monitors progress, recovers from agent overruns, independently certifies each block, and reconciles the spec. Encodes the failure modes seen in practice so they do not recur.
model: opus
argument-hint: spec=<path> [from=<phase>] [to=<phase>] [env=dev|dev+prod]
---

**YOU ARE EXECUTING THE `/dev-all` SKILL.** The user triggered this skill. Follow ALL instructions below step by step. Do NOT treat this as a freeform conversation - execute the runbook.

Follow CLAUDE.md rules.

This skill runs a whole `*_FEATURE.md`-style spec to "done & green", phase by phase, with the user doing only the final review. You are the **orchestrator**: you author and launch a background **ultracode run** that runs each phase as a separate fresh agent, you monitor it, you recover when an agent overruns, and you **independently certify** the result (never trust an agent's self-reported `build=pass`). You do NOT hand-write the feature code; its agents do.

## Arguments

- `spec=<path>` (required): the feature spec, e.g. `docs/plan-features/YOUR_FEATURE.md`.
- `from=<phase>` / `to=<phase>` (optional): run a sub-range (e.g. resume `from=6`). Default: all phases.
- `env=dev|dev+prod` (optional): where to apply migrations. **Default `dev`** (dev only; never prod unless explicitly asked).

---

## Golden rules (these prevent the failures listed at the bottom)

1. **YOU own migrations, not the agents.** Apply to DEV up front, save the file, then tell every agent "migration already applied, do not re-apply, do not touch prod."
2. **Split oversized phases into bounded sub-phases.** A single agent has a finite turn/token budget. Any phase that touches more than ~3 files of real code, or says "all N clients/providers", or "several usecases", MUST be split so each agent does ~2-3 files + tests. This is the #1 lever.
3. **Sequential, fresh context each.** `await` each (sub-)phase before the next; later phases see earlier edits on disk. Never parallelize interdependent phases.
4. **Trust nothing's `build=pass`.** Agents sometimes report green from a stale build. After each backend block and at the very end, run the gates YOURSELF.
5. **Never edit files while the ultracode run is live.** Concurrent edits race with a live agent and create confusing half-states. Stop the run first, or wait for the phase to finish.
6. **A returned partial beats a dead agent.** Bake "return-discipline" into the prompt and wrap each `agent()` in try/catch so an overrun stops the run cleanly instead of looping.
7. **Nothing gets committed.** Leave everything in the working tree for the user's review.

---

## Runbook

### Step 0: Read the spec, plan the phases
- Read `spec`. Enumerate every phase and its checklist items. Note per phase: scope (backend / frontend), files to create/modify, and which numbered phase each maps to.
- Read `.claude/skills/dev/SKILL.md` once to stay faithful to the /dev methodology (explore -> implement+tests -> verify -> tick spec).

### Step 1: Migration FIRST (you, not the agents)
- If the spec defines a migration: write the SQL file into your migrations directory (e.g. `migrations/<ts>_<name>.sql`), matching the format of a recent sibling migration, with a header comment noting DEV-applied + PROD-deferred.
- Apply to dev via your DB MCP server's `apply_migration` tool (dev project `your_dev_project_id`). Verify the column/table with `execute_sql`. Run `get_advisors` (security) and confirm no NEW findings from your change.
- Only if `env=dev+prod`: apply to prod (project `your_prod_project_id`), otherwise leave prod as an explicit TODO.

### Step 2: Pre-flight (cheap, high-value)
- Verify the spec's "files to modify" anchors actually exist; locate any that are mis-referenced (e.g. a port defined inline in a usecase rather than under `ports/`). Capture these as per-phase **hints**, they save the agent a wrong turn.
- Confirm the baseline is green (`cd backend && go build ./...`; `npm run -s -C frontend test:run` if quick) so any later red is attributable to the work, not the starting point.

### Step 3: Split oversized phases
- Decide the sub-phase list. Typical splits that proved necessary:
  - "Application usecases" (builder + several new usecases + scheduler) -> `6a` builder+first usecase, `6b` second usecase, `6c` third usecase, `6d` scheduler+config.
  - "Presentation + wiring" -> `7a` handlers/DTOs, `7b` routes + DI wiring.
  - "Multiple external client integrations" -> one sub-phase per ~2 clients + their config/tests.
- Assign each config key to its **first consumer** sub-phase (that sub-phase adds it to `app.yaml` + the config struct + runs the project's config-sync step if it has one; later phases just verify). This avoids "phase 5 needs a key phase 7 was supposed to add".

### Step 4: Author and launch the ultracode run
- Copy `.claude/skills/dev-all/templates/workflow-template.js`. Edit the 5 marked sections: `meta.phases`, `PHASE_TITLES`, `SPEC`, `PRIOR_DONE`, `PHASES` (+ per-phase `hints`). Backend -> `golang-backend-developer`, frontend -> `frontend-feature-developer`.
- Launch with the `Workflow` tool (inline `script`, or `scriptPath` after editing the file). It runs in the background and notifies you on completion/stop.

### Step 5: Monitor
- Start a persistent `Monitor` on the run's `journal.jsonl` (under the transcript dir printed by Workflow) that emits one line per new `"type":"result"` entry. Relay each (sub-)phase result to the user; `PushNotification` only on a block.

### Step 6: Independent certification per block
- After the last backend sub-phase (and again at the very end), run YOURSELF: `cd backend && go build ./... && go vet ./... && golangci-lint run ./internal/... && go test ./...`. For frontend: `cd frontend && npm run test:run && npm run build`. These, not the agents' self-reports, are the source of truth.
- Frontend phases never touch Go, so you can run Go gates while frontend phases run (no collision). Do NOT run Go-file edits while a backend phase is live.

### Step 7: Recovery playbook (when a phase blocks or the run stops)
1. **Stop the run** if it is looping (`TaskStop`). Read the run's `journal.jsonl` (NOT the multi-hundred-KB agent `*.jsonl` transcripts) to see what each phase reported.
2. **Inspect the working tree**: `git status --short`; `go build ./...`; `go vet ./internal/.../...`; grep for the methods/files the phase was supposed to produce.
3. **Most overruns left the work DONE on disk** (the agent just ran out of turns before calling StructuredOutput). If `build/vet/test/lint` are green and the deliverables are present: tick the spec boxes for that phase yourself and **continue** with the remaining phases (a fresh ultracode run whose `PRIOR_DONE` includes the recovered phase), do not re-run it.
4. If the tree is genuinely broken: either fix the small breakage yourself (only when no agent is running) or clean up and re-run that phase **split smaller**.
5. Resuming: `resumeFromRunId` re-runs only the first non-cached `agent()` onward, but it cannot "skip" a phase that never returned a cached result, so for recovered phases prefer a **new** ultracode run covering just the remaining phases (set `PRIOR_DONE` accordingly).

### Step 8: Final certification + reconcile + report (no commit)
- Run the full gates yourself (Step 6) and the project's config-sync check (if it has one).
- i18n em-dash scan: confirm the spec's NEW i18n keys and any new frontend files contain no em-dashes (`U+2014`) or en-dashes (`U+2013`); fix only NEW occurrences (do not churn pre-existing ones). Tip: `python3` scan for those two codepoints.
- Reconcile the spec's Execution Plan: tick the phase-summary lines and the verification commands you actually ran; annotate deferred items (prod migration, manual owner steps) honestly.
- Report: what shipped, the certified gate results, what you did vs the agents, and what remains (prod migration, manual/owner actions, E2E QA). Do NOT commit, offer to commit/PR on request.

---

## Problems encountered in practice (and how this skill avoids each)

These are real failures from a full run of this orchestration. The template + runbook above encode the fixes.

| # | Problem observed | Root cause | Fix encoded here |
|---|---|---|---|
| 1 | Ultracode run crashed instantly: `ReferenceError: meta is not defined` | The `export const meta` literal is NOT in scope in the script body. | Template uses a local `PHASE_TITLES` array; never reference `meta.*` in the body. |
| 2 | A big phase (5-6 clients + tests) ran ~21 min, hit its turn budget, **errored without returning**, and the ultracode run **retried it 3x in a loop**, each retry inheriting a half-edited tree. | One agent given too much work; a thrown `agent()` with no guard gets retried indefinitely. | (a) **Split** oversized phases into bounded sub-phases; (b) **return-discipline** prompt (return a partial, never run to death); (c) **try/catch** around each `agent()` so a throw STOPS the run cleanly. |
| 3 | Another big phase did **all** the work (100+ tool calls) but never called StructuredOutput -> error. | Same budget overrun, just after finishing. | Recovery insight in the runbook: the work is usually **already on disk**, verify green + tick boxes instead of re-running. Plus splitting prevents it. |
| 4 | An agent reported `build=pass` but had left a **compile error** (referenced a struct field it forgot to add). | Agents self-report from a stale build; the stop-on-block guard trusted the report. | Orchestrator runs **independent** `go build/vet/test` after each backend block and at the end. Never trust self-reported green for the final gate. |
| 5 | A transient broken-test diagnostic appeared mid-run (a constructor signature changed but its test not yet updated). | A file-edit **race**: reading/seeing the tree while an agent was mid-edit. | Rule: **never edit (and distrust transient diagnostics of) the tree while the ultracode run is live.** Stop first, or wait for the phase to finish, then verify the settled state. |
| 6 | A config key was needed by phase 5 but the spec "added" it in phase 7. | Cross-phase config dependency. | Assign each config key to its **first consumer** sub-phase, which adds it + runs the config-sync step; later phases only verify. |
| 7 | Risk of agents running DB migrations / hitting prod. | Migration left to a phase agent. | **You** apply the migration up front (DEV only by default), save the file, and tell every agent "already applied, do not re-apply, do not touch prod." |
| 8 | New test `describe()` labels used em-dashes (matching a pre-existing codebase convention), violating the hard rule. | Agents match surrounding code, which already breaks the rule. | Final **em-dash scan** on i18n + new files; fix only NEW occurrences; do not churn pre-existing ones. |
| 9 | When a phase was split or hand-recovered, the spec's Execution-Plan **summary checkbox** was left unticked. | No sub-agent owns the summary line. | Orchestrator **reconciles** spec checkboxes in Step 8. |
| 10 | `go test ./...` recompiles the whole module; agents re-running it after every edit burned their budget. | Inefficient verification loop. | **Efficiency** rule in the prompt: targeted tests during dev, full gate ONCE at the end. |

---

## Notes

- Ultracode (dynamic multi-agent orchestration) requires explicit opt-in; this skill IS that opt-in (the user invoked it). Author the workflow script, launch it via the `Workflow` tool, monitor, recover, certify.
- Inspect the run via the printed `journal.jsonl`, NOT the per-agent `*.jsonl` transcripts (those are huge and will flood context).
- Phase agents MAY spawn their own exploration sub-agents (e.g. `Explore` / `explore-codebase`) to parallelize discovery, one per distinct concern with no fixed cap. Encouraged on larger sub-phases: it keeps the phase agent's own context lean (it gets summaries back instead of reading everything inline), which directly mitigates the budget-overrun failure mode. Inline Grep/Glob/Read stays fine for a small sub-phase. Make sure each phase agent knows it has this option.
- DB projects: dev `your_dev_project_id`; prod `your_prod_project_id` (only with `env=dev+prod`). Replace these placeholders with your actual project IDs and MCP tool names.
