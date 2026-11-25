---
name: harness-create
version: 1.1.0
description: "End-to-end harness creation: interview → spec → runnable project. Two entry points: (A) start from scratch — interviews the user, produces HARNESS_SPEC.md, then builds; (B) start from existing HARNESS_SPEC.md — skips straight to build. Three build modes: document, code, investigation. Triggers: 'plan harness', 'build harness', 'create harness', 'harness', 'define spec', 'generate loop', 'overnight task', 'agent loop', '设计harness', '构建harness', '定义验收条件', '生成迭代脚本', '调查bug', '根因分析', 'root cause', 'investigate'."
---

# Harness Creator

Turn a goal into a running overnight harness — from interview through spec to generated project.

## Self-Review Checklist (read BEFORE and AFTER every phase)

### Planning Phase Guards
- [ ] Did NOT generate any files (harness.sh, prompts/, drafts/) during Phase 1
- [ ] Completed ALL interview questions before producing HARNESS_SPEC.md
- [ ] Got explicit user confirmation before moving to Phase 2

### Build Phase Guards
- [ ] Agent prompt(s) have fresh context warning at top
- [ ] `--allowedTools` set for each `claude -p` invocation
- [ ] Git commits after each step in the orchestrator
- [ ] All exit conditions from the spec are implemented
- [ ] Orchestrator supports `--dry-run`, `--resume`, `--max-cost`, `--step`, `--status`, `--register-dagu`, `--unregister-dagu`
- [ ] Generator writes changelog to a dedicated FILE (not stdout)
- [ ] Evaluator writes report to a dedicated FILE (not stdout)
- [ ] Orchestrator extracts data from files (not stdout)
- [ ] Orchestrator uses state.json for sub-step tracking (jq dependency checked)
- [ ] Orchestrator injects starting-point context per iteration
- [ ] dag.yaml generated with steps matching harness.sh step functions
- [ ] DAGU auto-registration attempted (symlink if dagu installed, skip if not)
- [ ] [Code Mode] Validation step with revert on failure
- [ ] [Code Mode] Frozen file violation gate
- [ ] [Code Mode] Regression detection (revert if score drops > 5)
- [ ] [Investigation Mode] Investigator writes to `evidence/h{N}-{name}.md`
- [ ] [Investigation Mode] Explicit CONFIRMED/ELIMINATED/INCONCLUSIVE judgment
- [ ] [Investigation Mode] Dead-end detection when all hypotheses eliminated
- [ ] Orchestrator has `preflight()` checking all prerequisites from SPEC.md
- [ ] [If health checks defined] Orchestrator has `health_check()` between iterations

---

## Entry Point Detection

Determine which entry point applies:

**Entry A — No spec exists:**
The user has a goal but no HARNESS_SPEC.md. Start with Phase 1 (Planning Interview).

**Entry B — Spec already exists:**
The user has a HARNESS_SPEC.md (or equivalent structured spec). Skip to Phase 2 (Build).

**Detection logic:**
1. If the user says "build harness", "generate loop", "构建harness" AND provides or references a HARNESS_SPEC.md → **Entry B**
2. If the user describes a goal, problem, or task without a structured spec → **Entry A**
3. If unclear, ask: "Do you already have a HARNESS_SPEC.md, or should we start by defining one?"

---

## Phase 1: Planning Interview

> **HARD GATE: Do NOT generate any files during this phase.**
> No harness.sh, no prompts/, no drafts/, no code. Phase 1 produces ONLY a HARNESS_SPEC.md.
> Generating build artifacts here is the #1 failure mode this skill prevents.

### Step 1.0: Task Qualification & Routing

Determine the task mode:

**Route A — Iterative Improvement** (the task is "make X better"):
- Has a measurable quality dimension (score, pass/fail, coverage %)
- A stable target that won't shift during the run
- A clear "done" condition or iteration cap

**Route B — Investigation/Diagnostic** (the task is "why does X happen?"):
- Has an observable symptom that can be described precisely
- Root cause is unknown but can be narrowed via hypothesis testing
- "Done" = root cause confirmed with evidence, not a score threshold

**Unsuitable:** Requires creative direction changes, has no evaluable output and no observable symptom, or depends on unavailable external input. Suggest restructuring.

If borderline, explain routing and let the user confirm.

### Step 1.1: Conduct the Interview

Read `references/planning-interview.md` for the detailed question sequence.

- **Route A**: Phases 1-4 (Task Understanding → Prerequisites → Optimization Target → Agent Architecture → Guardrails)
- **Route B**: Phases 1D-3D (Symptom Description → Prerequisites → Hypothesis Generation → Evidence Collection Plan)

Interview rules:
- Ask questions, wait for answers, then proceed
- Do not skip phases or merge questions — each phase extracts distinct information
- Adapt language to match the user

### Step 1.2: Generate HARNESS_SPEC.md

Read `references/spec-templates.md` for the exact output template.

- **Route A**: Use the Iterative Improvement template
- **Route B**: Use the Investigation template

After generating, review the spec with the user. Confirm each section. Make adjustments.

### Step 1.3: Handoff Gate

Before proceeding to Phase 2, get explicit user confirmation:

> "Your HARNESS_SPEC.md is ready. Want me to build the harness project now, or do you want to review/edit the spec first?"

Only proceed to Phase 2 after the user confirms.

---

## Phase 2: Build

### Step 2.0: Spec Validation

Read the HARNESS_SPEC.md (whether from Phase 1 or provided by user). Verify it contains:
- [ ] Clear artifact description or symptom description
- [ ] Eval rubric with weighted dimensions (Route A) or ranked hypotheses (Route B)
- [ ] Exit conditions
- [ ] Agent architecture (at minimum: roles and responsibilities)

Flag gaps and ask before proceeding. Do not guess missing information.

### Step 2.1: Determine Build Mode

Read `references/design-rules.md` for mode definitions and critical design rules.

Three modes based on the spec:
- **Document Mode** — articles, reports, data files
- **Code Mode** — live source code, UI components
- **Investigation Mode** — bug root cause analysis

### Step 2.2: Generate Project Structure

Read `references/project-structure.md` for directory layout and file roles.

Create the project under `.harness-workspace/{task-name}/`. Create `.harness-workspace/` if it doesn't exist.

Generate all structural files:
- SPEC.md (frozen target extracted from HARNESS_SPEC.md)
- EVAL_CRITERIA.md (Route A only)
- progress.md (initialized with header)
- README.md

### Step 2.3: Generate Agent Prompts

Read `references/prompt-templates.md` for base templates and the tool permission table.

Generate prompts for each agent defined in the spec. Customize templates with task-specific values. Replace ALL placeholders.

### Step 2.4: Generate Orchestrator Script + DAGU DAG

Read `references/orchestrator-templates.md` for bash templates, state.json patterns, and DAGU YAML templates.

Generate `harness.sh` implementing:
- All exit conditions from the spec
- `--dry-run`, `--resume`, `--max-cost`, `--step <name> --iteration <N>`, `--status` flags
- `state.json` sub-step tracking via `jq` (check for `jq` at startup)
- Preflight checks from SPEC.md Prerequisites (fail fast)
- Health checks from SPEC.md Prerequisites (pause on failure, if defined)
- `run_step` wrapper for every sub-step (skip completed, update state on start/success/failure)
- File-based data extraction (not stdout)
- Starting-point injection per iteration
- Git snapshots per step
- Mode-specific patterns (validation+revert for Code Mode, hypothesis tracking for Investigation Mode)

Generate `dag.yaml` implementing:
- One DAGU step per harness sub-step, using `harness.sh --step <name> --iteration ${ITERATION}`
- Correct `depends` chain matching the mode's step sequence
- Retry policies on `generator`/`evaluator`/`investigator` steps
- Replace all `[PLACEHOLDERS]` with task-specific values

After writing `dag.yaml`, call `register_dagu` (Key Patterns §11) to auto-symlink into DAGU's DAGs directory if DAGU is installed locally. Skip silently if not.

### Step 2.5: Prompt DAGU Installation

After harness generation, proactively inform the user about DAGU for progress monitoring:

- **If DAGU is installed**: Print the DAGU UI URL and tell the user the harness is registered. Example:
  > Your harness is registered in DAGU. View progress at http://localhost:8080 (or your configured port).
  > Run `dagu start dag.yaml --params "ITERATION=1"` to start via DAGU, or `bash harness.sh` to run standalone.

- **If DAGU is NOT installed**: Suggest installation. Example:
  > Tip: Install DAGU to monitor harness progress in a web UI — see each step's status, logs, and duration in real time.
  > Install: `brew install dagu-org/brew/dagu` (macOS) or see https://dagu.readthedocs.io
  > After installing, run `bash harness.sh --register-dagu` to register this harness.

### Step 2.6: Self-Review

Re-read the Self-Review Checklist at the top of this file. Verify every applicable item. Fix any violations before presenting the output to the user.

---

## Language & Adaptation Rules

- Match the user's language throughout (interview, spec, generated files)
- Script variables and structural labels (Phase, Dimension, etc.) stay in English for cross-tool compatibility
- If the user switches language mid-conversation, follow the switch

### Domain Adaptations

- **Code artifact**: Use Code Mode. Add validation step (typecheck/test) before eval. Revert on failure.
- **Browser-visible UI**: Add Playwright tools to Generator + Evaluator. Include `screenshots/` directory.
- **Subjective quality**: Weight rubric toward concrete detection methods. Consider human review gate.
- **> 2 agents**: Pipeline extends linearly: Planner → Generator → [Specialist] → Evaluator.
- **Bug investigation**: Use Investigation Mode. Single Investigator agent. Exit = root cause confirmed.

---

## Reference File Index

| Phase | Reference File | Load When |
|-------|---------------|-----------|
| 1.1 | `references/planning-interview.md` | Starting the interview |
| 1.2 | `references/spec-templates.md` | Generating HARNESS_SPEC.md |
| 2.1 | `references/design-rules.md` | Determining build mode and rules |
| 2.2 | `references/project-structure.md` | Creating project directory layout |
| 2.3 | `references/prompt-templates.md` | Writing agent prompts |
| 2.4 | `references/orchestrator-templates.md` | Writing harness.sh + dag.yaml |
