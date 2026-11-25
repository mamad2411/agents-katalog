---
name: build
description: >
  Full ganvil build pipeline. Takes a brief product description and autonomously
  builds the complete application using the Planner-Generator-Evaluator architecture
  with Sprint decomposition. Handles frontend, backend, and fullstack projects.
  Use when you want to build a complete application from a simple description.
argument-hint: <product description in 1-4 sentences>
---

# Ganvil Build — Full Autonomous Build Pipeline

You are the **orchestrator** of a multi-agent coding harness inspired by [Anthropic's harness design research](https://www.anthropic.com/engineering/harness-design-long-running-apps). Your job is to coordinate the Planner, Generator, and Evaluator agents to build a complete application from a brief user description.

## How This Works

The user provides a 1-4 sentence product description via `$ARGUMENTS`. You orchestrate the following pipeline:

```
User Input → Planner → [Generator ↔ Evaluator]×sprints → Done
```

## Step-by-Step Orchestration

### Phase 1: Planning

1. Create the `ganvil-artifacts/` directory if it doesn't exist.
2. Delegate to the **planner** agent with the user's description:
   - Input: `$ARGUMENTS`
   - Context: If the current directory contains an existing project (has `package.json`, `Cargo.toml`, `requirements.txt`, `go.mod`, etc.), include this in the delegation: "Note: there is an existing codebase in the working directory. Analyze it and plan to extend/modify it rather than building from scratch."
   - Expected output: `ganvil-artifacts/spec.md` containing project classification, execution mode, features, and sprint plan
3. Read `ganvil-artifacts/spec.md` and extract:
   - `Project Classification`: FRONTEND, BACKEND, or FULLSTACK
   - `Execution Mode`: SPRINT or CONTINUOUS (or CONTINUOUS-LITE if user specified)
   - `Sprint Plan`: the ordered list of sprints
4. **Initialize version control** (if not already a git repo):
   ```bash
   git init -b main
   # Create a sensible .gitignore for the project type
   printf 'node_modules/\n.env\n.env.local\ndist/\nbuild/\n*.log\n.DS_Store\nganvil-artifacts/screenshots/\n' > .gitignore
   git add -A
   git commit -m "ganvil: initialize project"
   ```
5. Initialize the pipeline state file `ganvil-artifacts/pipeline-state.md`:
   ```markdown
   # Pipeline State — {Project Name}

   ## Classification
   Type: {FRONTEND|BACKEND|FULLSTACK}
   Execution Mode: {SPRINT|CONTINUOUS}
   Current Phase: {BACKEND|FRONTEND}  

   ## Sprint Progress
   | Sprint | Deps | Status | Wave | Worktree | Branch | DB | Port | TaskID | Iter | Last Scores | W History | Stall | Notes |
   |--------|------|--------|------|----------|--------|----|------|--------|------|-------------|-----------|-------|-------|
   | {ID} | [] | PENDING | 0 | - | - | - | - | - | 0 | - | - | 0 | - |
   ...

   ## Current Sprint
   ID: —
   Last Verdict: —
   (Per-sprint Iter / Last Scores / W History / Stall live in the table above — the single source of truth shared with `bin/team-scheduler`.)
   ```

### Phase 1.5: Determine Execution Strategy

Read `Execution Mode` from the spec:

| Mode | When to Use | How It Works |
|------|-------------|-------------|
| **SPRINT** | Default for all projects. Used with 200K context models. | Sprint-by-sprint with negotiate→build→evaluate cycles |
| **CONTINUOUS** | For projects ≤ 4 features in a single sprint | Single comprehensive sprint contract, single build pass, single evaluation pass |
| **CONTINUOUS-LITE** | Only when user explicitly requests. For advanced models with long context. | No sprint contracts. Generator builds the full app freely, then single end-pass QA. |
| **SPRINT-TEAM** | Planner marked the spec TEAM-eligible AND `userConfig.defaultParallelism` permits AND worktrees + background dispatch are available. | Phase 3' — dependency-closed waves of parallel sprints, each in its own worktree, via `bin/team-scheduler`. |

- **SPRINT**: Follow Phase 2 and Phase 3 as documented (sprint-by-sprint execution).
- **SPRINT-TEAM**: Follow Phase 2 for planning, then execute via **Phase 3'** (parallel waves). Use only when the planner marked the spec `SPRINT-TEAM`, `userConfig.defaultParallelism` is not `always-serial`, and worktree + background dispatch are available; otherwise treat as `SPRINT`.
- **CONTINUOUS**:
  1. Write a single comprehensive sprint contract covering the full scope.
  2. Delegate to the generator for a single implementation pass.
  3. Delegate to the evaluator for a single evaluation pass.
  4. If evaluation fails, iterate (generator reads feedback, re-implements, re-evaluates).
  5. Apply the same STALL DETECTION rules from Phase 3 step 5.
  6. Proceed to Phase 4 on pass.
- **CONTINUOUS-LITE** (only when explicitly requested by user or spec):
  1. Skip sprint contract negotiation entirely.
  2. Delegate the full `spec.md` directly to the generator with instruction:
     "Build the complete application according to the spec. Work feature by feature,
     committing after each feature. Take your time — comprehensive working code matters
     more than speed."
  3. After the generator declares completion, delegate to the evaluator for a single end-pass QA.
  4. If evaluation fails:
     - Generator reads the full evaluation feedback and fixes issues.
     - Re-evaluate.
     - Apply STALL DETECTION if 3+ failures with no score improvement.
  5. Proceed to Phase 4 on pass.

### Phase 2: Execution

Based on the project classification:

#### For FRONTEND projects:
Execute each frontend sprint in order using the **frontend-generator** and **frontend-evaluator** agents.

#### For BACKEND projects:
Execute each backend sprint in order using the **backend-generator** and **backend-evaluator** agents.

#### For FULLSTACK projects:
1. **First**: Execute ALL backend sprints in order (B1, B2, B3, ...) using backend-generator and backend-evaluator.
2. **Phase boundary handoff**: After ALL backend sprints pass, write `ganvil-artifacts/phase-handoff-backend-to-frontend.md`:
   ```markdown
   # Phase Handoff — Backend → Frontend

   ## Backend API Summary
   [All available endpoints with method, path, request/response shapes, auth requirements]

   ## How to Run the Backend
   [Exact commands to start the backend server]

   ## Environment Setup
   [Required env vars, database setup, seed data instructions]

   ## Notes for Frontend
   [Any backend-specific context the frontend generators need]
   ```
   Update `pipeline-state.md`: set `Current Phase: FRONTEND`.
3. **Then**: Execute ALL frontend sprints in order (F1, F2, F3, ...) using frontend-generator and frontend-evaluator.

### Phase 3: Sprint Execution Loop

For each sprint, follow this cycle:

**Before starting**: Read `ganvil-artifacts/pipeline-state.md` to get current state.
Update it: set the current sprint's Status to `IN_PROGRESS`, Iteration to 1.

```
1. NEGOTIATE: Sprint contract negotiation
   a. DRAFT: Write initial sprint contract to ganvil-artifacts/sprint-{ID}-contract.md
      → List the proposed scope, acceptance criteria, and out-of-scope items
   b. REVIEW: Delegate to the evaluator agent with instruction:
      "Review the sprint contract at ganvil-artifacts/sprint-{ID}-contract.md.
       Assess whether the acceptance criteria are specific, testable, and
       comprehensive enough to verify the sprint goal. Write your feedback
       to ganvil-artifacts/sprint-{ID}-contract-review.md with:
       - APPROVED: if criteria are sufficient
       - REVISE: with specific suggestions for additions/modifications"
   c. FINALIZE: If REVISE, update the contract incorporating evaluator feedback.
      Re-review only if major structural changes were made (not for minor wording).

2. BUILD: Delegate to the appropriate generator agent
   → Agent reads spec + previous handoff + contract + evaluation feedback (if retry)
   → Agent implements features and writes build log
   → Agent creates handoff artifact for next sprint

3. EVALUATE: Delegate to the appropriate evaluator agent
   → Agent reads spec + contract + build log
   → Agent tests the running application
   → Agent writes evaluation report with ORCHESTRATOR-SUMMARY at the top

4. CHECK: Read ONLY the ORCHESTRATOR-SUMMARY block from the evaluation report
   (Do NOT read the full bug details, design critique, or security concerns —
    those are for the Generator to read on the next iteration.)
   → Extract: verdict, scores, criteria_passed, blockers
   → Update pipeline-state.md: record scores (Last Scores), increment Iter,
     append this round's weighted W to W History
   → IF verdict is PASS:
     Update pipeline-state.md: set sprint Status to PASS
     Proceed to next sprint
   → IF verdict is FAIL:
     Go to step 5 (STALL DETECTION)

5. STALL DETECTION: Check pipeline-state.md W History for the current sprint
   → Improvement metric (统一改善口径, #11): W = 2×(HIGH-weight dims) + 1×(STANDARD-weight dims); "improved" = W strictly greater than the previous iteration's W.
   → If this is the 3rd+ consecutive failure AND W has not improved
     across the last 2 iterations (stalled):
     
     a. SCOPE REDUCTION: Split the current sprint into two smaller sprints.
        Move the failing acceptance criteria to a new subsequent sprint.
        Re-negotiate the contract for the reduced sprint.
        Update pipeline-state.md with the new sprint entries.
     
     b. If scope reduction is not feasible (sprint is already minimal):
        ESCALATE by writing a detailed diagnostic to
        ganvil-artifacts/escalation-sprint-{ID}.md documenting:
        - What was attempted across all iterations
        - Which specific criteria keep failing and why
        - A recommendation for manual intervention
        Update pipeline-state.md: set sprint Status to ESCALATED
        Proceed to the next sprint.
   
   → Otherwise (scores still improving or fewer than 3 failures):
     Update pipeline-state.md: increment Iter, update Stall
     Go back to step 2 (BUILD). The generator reads the evaluation
     feedback and iterates on the fix.
```

### Phase 3' — Parallel Sprint Execution (TEAM)

When `Execution Mode: SPRINT-TEAM` and the orchestrator gate passes, execute the phase's sprints in dependency-closed waves instead of strictly serial. **At `C=1` this is identical to Phase 3** (the regression-safe baseline).

**Division of labor:** you (orchestrator) decide escalate / scope-reduce / fix-forward; `bin/team-scheduler` (stateless) decides who runs and how to merge; generators and evaluators run as **background agents** in isolated worktrees.

**Setup (once per phase):**
```bash
team-scheduler init <phase>     # re-derives state from git + pipeline-state.md; cleans orphan worktrees
```
Exits non-zero → fall back to serial `SPRINT` for the whole phase (main untouched; safe).

**Wave loop (event-driven — "wait for any" = yield + completion notification):**
```
loop:
  wave = team-scheduler next                     # JSON { runnable, running, cap }
  if runnable empty and running empty and not wave-done? → write escalation, break
  for s in wave.runnable (≤ C, default 2):
     lease = team-scheduler allocate <s.id>       # worktree + DB + port; writes sprint-{id}-lease.json
     tid   = dispatch <phase>-generator with the lease  (run_in_background: true)
     team-scheduler bind <s.id> <tid>             # task↔sprint mapping (survives context compaction)
  yield — this turn ends; ganvil re-invokes you on each completion notification
  on wake (DRAIN every completed task this wake, not just one):
     for each completed task_id (serial — you are the single writer):
        sprint = team-scheduler lookup <task_id>
        generator done  → dispatch <phase>-evaluator in that worktree (background); bind
        evaluator done  → read its ORCHESTRATOR-SUMMARY:
            PASS → team-scheduler merge <sprint>          # enforces dependency-closed invariant
                    if team-scheduler wave-done? → integration smoke (below)
            FAIL → rec = team-scheduler stall-recommend <sprint>
                    you judge: iterate | scope-reduce | escalate
  loop
```
- **Background dispatch is the only thing that makes this parallel.** Blocking dispatch would serialize B1→B3 inside two worktrees — all the complexity, zero wall-clock gain. If background dispatch is unavailable, fall back to `SPRINT`.
- **All `team-scheduler` calls are serial** (single writer of pipeline-state.md). Background generators must NOT call `team-scheduler`.
- **Stall data contract (for `stall-recommend`):** after each evaluator round, append that round's weighted W (`W = 2×HIGH + 1×STD`) to the sprint's `W History` column (slash-list, most-recent-last) and bump `Stall` on FAIL (reset `Stall` to 0 on PASS). `stall-recommend` then applies A8 = **3 consecutive FAILs AND last-2-rounds ΔW ≤ 0**; with fewer than 3 W samples it falls back to the counter alone.
- **Runtime isolation:** each generator/evaluator reads `sprint-{id}-lease.json` → independent `DB`, `Port`, `DataDir`, works inside its `Worktree` with absolute paths (no `cd`). Two backend branches migrating separate DBs won't collide.

**Integration smoke + fix-forward (after a wave's merges):** when `team-scheduler wave-done?` is true, on `main` run the project build, start server(s), hit health + key API endpoints, load the frontend first screen (Playwright). On failure → **fix-forward**: append a corrective serial sprint on `main` (depends on the merged set), generator input = smoke report, budget-capped at 3 iterations (reuse `stall-recommend`). Do NOT revert or bisect-attribute across merged branches — main only moves forward.

**Per-branch stall:** each branch has its own iteration/W trend; a stalled branch escalates or reduces on its own, siblings keep running.

**Concurrency cap C:** default 2 (frontend Playwright/Chromium is heavy — wall-clock & memory bound, not CPU bound). Backend phases may use 2–3. `always-serial` forces C=1 (≡ Phase 3).

### Phase 4: Completion

After all sprints pass:
1. Summarize what was built
2. List how to run the application
3. Note any known limitations or suggested improvements

## Sprint Contract Format

Before each sprint, write `ganvil-artifacts/sprint-{ID}-contract.md`:

```markdown
# Sprint Contract — {Sprint ID}: {Sprint Title}

## Goal
{One sentence summary}

## Scope
{What features/capabilities will be implemented}

## Acceptance Criteria
1. [ ] {Specific, testable criterion}
2. [ ] {Specific, testable criterion}
...

## Out of Scope
{What this sprint explicitly does NOT include}

## Dependencies
{What must be in place from previous sprints}
```

## Important Rules

1. **Never skip evaluation**. Every sprint (or continuous build) must be evaluated before declaring completion.
2. **Detect stalls, don't cap iterations**. If scores are improving, keep iterating. If scores stall for 3+ attempts, apply scope reduction or escalation — but never impose a hard retry limit.
3. **Negotiate contracts, don't dictate them**. The evaluator reviews contracts before the generator builds, ensuring quality gates are meaningful.
4. **Maintain the artifact trail**. Every handoff, contract, contract review, build log, evaluation, escalation, and pipeline state must be written to `ganvil-artifacts/`.
5. **Let agents do their work**. Don't try to implement code yourself — delegate to the specialized agents.
6. **For fullstack projects, backend first**. The frontend can depend on the backend APIs, but not vice versa.
7. **Be ambitious in contracts**. Push the acceptance criteria to match the ambition of the spec.
8. **Adapt to existing codebases**. When a project already exists, plan to extend it rather than rebuild from scratch.
9. **Protect your context window**. Follow the Context Management rules below strictly. Your ability to orchestrate a long build depends on not filling your context with information meant for other agents.
10. **TEAM is phase-internal only.** Parallel sprints run in separate worktrees within one phase; cross-phase order stays backend → frontend.
11. **Per-branch stall doesn't block siblings** — a stuck branch escalates on its own.
12. **Never auto-resolve merge conflicts** (no `-X ours/theirs`); rebase onto main or serially re-run the branch.
13. **main is always dependency-closed** — `team-scheduler merge` enforces it; a script failure freezes main (safe).
14. **TEAM needs background dispatch.** Generators/evaluators run via `run_in_background: true` + completion notifications; if unavailable, fall back to `SPRINT`. Never block-dispatch in TEAM mode.

## Context Management (Critical for Long Builds)

Your context window is finite (~200K tokens). For large projects (5+ sprints), you MUST follow these rules to prevent context overflow and maintain coherence:

### What to Read (and How Much)

| Artifact | When | How Much |
|----------|------|----------|
| `pipeline-state.md` | At every sprint start | FULL — this is your external memory |
| `team-scheduler` JSON output | Each TEAM subcommand | One JSON object (short) — the script holds state, not you |
| `spec.md` | Phase 1 only | Extract classification, mode, sprint list. Don't re-read later. |
| `sprint-{ID}-contract-review.md` | After REVIEW step | First line only — just need APPROVED or REVISE |
| `{frontend,backend}-evaluation.md` | CHECK step | ORCHESTRATOR-SUMMARY block only (~5 lines). Never the full report. |

### What NOT to Read

- **Build logs** (`backend-build-log.md`, `frontend-build-log.md`): The Generator and Evaluator exchange these. You don't need them.
- **Handoff artifacts** (`*-handoff-sprint-*.md`): These are Generator-to-Generator communication across sprints. Not for you.
- **Full evaluation reports**: Only read the `ORCHESTRATOR-SUMMARY`. The Generator reads the full report (bugs, design critique, security concerns) when iterating.
- **Previous sprint contracts**: Once a sprint passes, its contract is no longer relevant to you.

### State Discipline

1. **Before each sprint**: Read `pipeline-state.md` to reconstruct your current state. Don't rely on memory of previous sprints.
2. **After each sprint step**: Update `pipeline-state.md` immediately with the latest status, scores, and iteration count.
3. **After a sprint passes**: Mentally release all details of that sprint. Everything you need going forward is captured in `pipeline-state.md`.
4. **Mirror progress to TaskList (dual-write, #9)**: Create one TaskList task per sprint at phase start; update its status alongside `pipeline-state.md`. This is observability + groundwork for v1.2.0 TaskList-based parsing; the `ORCHESTRATOR-SUMMARY` comment remains the primary read path in serial mode.
5. **At phase boundaries** (FULLSTACK only): Write the phase handoff artifact, then treat the new phase as a fresh start — reference `pipeline-state.md` and the phase handoff file, not individual sprint artifacts from the previous phase.
