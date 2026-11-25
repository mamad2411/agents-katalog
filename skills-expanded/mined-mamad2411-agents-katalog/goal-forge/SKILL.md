---
name: goal-forge
description: Turn a rough coding or repo idea into a spec, executable plan, and long-running Codex /goal contract. Use when the user wants to create a coding spec, spec out a repo feature, tighten a coding spec, turn an implementation idea into a /goal-ready plan, prepare for autonomous coding, forge a goal, start a /goal, generate GOAL.md, prepare measurable done_when criteria, or check Codex config readiness.
---

# Goal Forge

Goal Forge converts a rough coding idea into an executable Codex `/goal` contract.

Default pipeline:

1. Interview rough intent into `SPEC.md`.
2. Tighten `SPEC.md` until scope, scoring, feedback, and verification are concrete.
3. Compile `SPEC.md` into `GOAL.md`.
4. Check Codex config readiness before running `/goal`.

Use this skill for coding and repo work first. If the task is mostly exploratory, research-only, security-critical, or lacks verifiable completion criteria, keep the user in the loop instead of compiling a `/goal`.

Long-running goals need a runtime harness, not just a task description. Every `/goal` contract should make four things explicit:

- **Scorecard**: how Codex repeatedly scores progress toward the goal.
- **Feedback loop**: the fastest representative check Codex can run while iterating.
- **Working memory**: markdown files Codex maintains so multi-hour runs do not rely only on conversation context.
- **Human control surface**: small, task-specific knobs and sidecar inputs the user can inspect or adjust while the goal runs.

## Modes

Choose the smallest mode that satisfies the request.

- **Interview**: User gives a rough idea, asks to create a spec, or the spec lacks user-approved success criteria.
- **Tighten**: User has a `SPEC.md` and wants it challenged, clarified, or made executable.
- **Compile**: User has a good enough `SPEC.md` and wants a `/goal` prompt or `GOAL.md`.
- **Check config**: User asks whether their Codex setup can run long goals.

## Interview Mode

When the user gives a rough idea or asks to create a spec:

1. Read the existing `SPEC.md` if present. Otherwise treat the rough idea as the interview seed; do not draft `SPEC.md` until step 6.
2. Interview the user in detail before finalizing the spec.
3. Ask about anything relevant: technical implementation, UI/UX, architecture, data model, edge cases, tradeoffs, rollout, scoring, feedback-loop speed, verification, risks, and non-goals.
4. Do not ask obvious checklist questions. Ask questions that force decisions or expose hidden ambiguity.
5. Continue interviewing until the spec is complete enough to compile into an executable `/goal`.
6. Then write or update `SPEC.md`.

Use structured user-question tooling when available. If it is not available, ask concise batches of questions in chat. Keep each batch focused on unresolved blockers.

Hard gate: do not compile a `/goal` prompt until `done_when` contains concrete, user-approved success criteria. After the interview has covered scope, architecture, scoring, and verification, Codex may propose candidate `done_when` criteria as a starting point. The user must confirm or edit product and acceptance criteria before the spec is considered complete.

For long-running or exploratory goals, also identify:

- the primary score or checklist Codex should optimize
- the threshold or stop condition that means the goal is complete
- the fastest useful check Codex can run repeatedly while working
- the slower final check required before completion
- whether Codex should create or maintain `PLAN.md`, `ATTEMPTS.md`, and `NOTES.md`
- what the user may need to observe or tune while the goal runs, such as phase/status visibility, scope limits, resource budgets, review gates, sidecar inputs, or pivot approvals

## Tighten Mode

Read `SPEC.md` skeptically before any execution prompt is created.

For each ambiguity:

- explain why it matters
- give two distinct interpretations
- recommend the interpretation that produces the more maintainable result
- ask the user when the choice defines product intent
- update the spec only after the choice is clear

Do not add scope. Remove or mark anything that cannot be verified. Preserve clear existing decisions.

The tightened spec should include:

- goal and non-goals
- user-visible behavior
- architecture and implementation constraints
- files, modules, or systems likely involved
- explicit edge cases
- risk boundaries
- scorecard with metric, threshold, regression checks, and stop condition
- fast feedback loop with expected runtime and proxy validity
- working-memory files for long-running goals
- a minimal human control surface when the user may need visibility or steering during the run
- verification commands or manual checks
- user-approved `done_when` criteria

## Compile Mode

Compile `SPEC.md` into `GOAL.md` using the block structure in `references/goal_prompt_blocks.md`. Load `references/standard_execution_rules.md` for default `<execution_rules>` content. If scaffolding long-run tracking files, load `references/working_memory_templates.md`. If the goal benefits from human steering during a long run, load `references/control_surface_templates.md`.

Before writing `GOAL.md`, reject weak specs that lack:

- measurable `done_when`
- a scorecard for how Codex evaluates progress during the run
- scope boundaries or non-goals
- a fast feedback loop, or an explicit reason one is impossible
- concrete verification commands or checks
- enough context for an agent to start reading the repo

If the spec is weak, route the user back to Interview or Tighten mode with a specific list of missing decisions. Do not write `GOAL.md` until the gaps are resolved.

Concrete gate: each `done_when` item must name a command, file artifact, or user-observable behavior. Otherwise mark it as weak and ask for clarification.

Scorecard gate: each `scorecard` must name the primary metric or checklist, the passing threshold, regression checks, the scoring command or inspection path, and the stop condition. If the score is model-judged, require a checklist or rubric that makes the judgment auditable.

Feedback-loop gate: each `feedback_loop` must name a fast check, expected runtime, run cadence, why the proxy is representative enough, and the slower escalation or final check. If the only available check is slow, say so explicitly and adjust the workflow cadence.

Working-memory gate: if the goal may run for hours, involves repeated experiments, or has high context churn, include a `working_memory` block. Prefer `PLAN.md`, `ATTEMPTS.md`, and `NOTES.md` unless the repo already has equivalent files. If no working-memory files are needed, state why the goal is short and linear enough to skip them.

Human-control gate: if a goal may run while the user or another Codex session reviews in parallel, may consume scarce resources, may require strategic pivots, or may benefit from human priority changes, include a `human_control_surface` block and scaffold a compact `CONTROL.md`. Keep `CONTROL.md` small: only include knobs relevant to this goal. Do not create a second `GOAL.md` full of static instructions.

Map the spec into the goal blocks:

- spec summary -> `<goal>`
- relevant files/modules/discovery commands -> `<context>`
- architecture rules, non-goals, anti-patterns -> `<constraints>`
- scoring metric, threshold, regression checks, stop condition -> `<scorecard>`
- acceptance criteria -> `<done_when>`
- fast iterative check and slower escalation check -> `<feedback_loop>`
- implementation phases -> `<workflow>`
- long-run tracking files and update cadence -> `<working_memory>`
- user-visible status, tunable knobs, sidecar inputs, and pivot/resource gates -> `<human_control_surface>`
- test/build/manual checks -> `<verification_loop>`
- `references/standard_execution_rules.md` plus repo-specific rules -> `<execution_rules>`
- final artifacts and completion signal -> `<output_contract>`

After writing `GOAL.md`, self-check it:

- `done_when` is measurable and user-approved
- `scorecard` tells Codex how to score progress and stop
- `feedback_loop` is fast enough to run repeatedly, or its limits are explicit
- `working_memory` is present for long-running or exploratory work
- `human_control_surface` is present when the user needs visibility or tuning knobs during a long run, and absent when it would be ceremony
- context names files or discovery commands
- constraints prevent obvious shortcuts
- verification is executable or explicitly manual
- the task is execution-oriented enough for `/goal`

## Config Check

Use `scripts/inspect_codex_config.py` for a read-only report:

```bash
python3 ~/.codex/skills/goal-forge/scripts/inspect_codex_config.py --project-path /path/to/project
```

Run it from the target project root, or pass `--project-path`. The script reports the installed Codex version, selected config keys, trusted-project status, and gaps against the autonomous `/goal` configuration.

Before telling the user a long-running `/goal` is ready, verify the config against `references/config_checklist.md`. The important autonomous settings are:

- `model = "gpt-5.5"`
- `model_context_window = 1050000`
- `model_auto_compact_token_limit = 997500`
- `model_reasoning_effort = "high"`
- `plan_mode_reasoning_effort = "xhigh"`
- `approval_policy = "never"`
- `sandbox_mode = "danger-full-access"`
- `[features] goals = true`

Do not edit `~/.codex/config.toml` unless the user explicitly asks for config changes. If asked to change config, prefer applying the dangerous `approval_policy = "never"` and `sandbox_mode = "danger-full-access"` settings only for explicitly trusted project paths rather than globally.

Read `references/config_checklist.md` when explaining config tradeoffs.

## Output

Depending on the request, produce one or more of:

- updated `SPEC.md`
- generated `GOAL.md`
- optional `PLAN.md`, `ATTEMPTS.md`, and `NOTES.md` scaffolds for long-running goals
- optional `CONTROL.md` scaffold for long-running goals that need human visibility or tuning knobs
- config readiness report
- the exact `/goal` prompt body to paste into Codex

When the user asks to run the goal, verify that their Codex version supports `/goal` first.
