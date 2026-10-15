---
name: loop-skill
description: Design and create traceable loop systems for user tasks. Use when the user invokes /loop-skill or asks to build, design, scaffold, run, or improve an iterative workflow with generations, audits, rewrites, logs, validators, max iterations, and explicit exit conditions.
---

# Loop skill

## Purpose

Create task-specific loop systems from user intent. A loop system is not a stronger prompt; it is a filesystem-backed workflow with state, iteration artifacts, audit results, rewrite plans, logs, and exit rules.

Use one universal structure for every task, then add task-specific criteria, profile packs, evidence, and validators.

## Workflow

1. Orient
   - If the task targets an existing codebase or project, inspect the repo before asking questions.
   - If the task is a fresh content/research/planning task, skip repo scanning unless the user asks.

2. Interview
   - Ask only for missing information that changes the loop design.
   - Prefer 2-4 multiple-choice options plus a free-form option when possible.
   - Generate choices dynamically from the user's task. Do not rely on a fixed question bank.
   - Read `references/interview-logic.md` when the task is ambiguous or broad.

3. Propose the loop blueprint
   - Use a short, confirmable blueprint by default.
   - Include only: goal, inputs, output contract, objective criteria, judgment criteria, required artifacts, max iterations, and exit condition.
   - Put longer rationale in `blueprint.md` after confirmation; do not make the chat blueprint so long that it slows the user down.
   - For UI, game, design, or interactive tasks, define quality gates before implementation. Do not treat build success as product quality.
   - Say clearly: max iterations are a budget, not a success guarantee.
   - Get user confirmation before creating files unless the user explicitly asked to proceed directly.

4. Scaffold the loop system
   - Use `scripts/init_loop.py` to create `.loops/systems/<slug>` and `.loops/runs/<timestamp>-<slug>`.
   - Treat target count as a required objective check for every mode, not only content loops.
   - For structured content such as checklists, SOPs, tables, QA rubrics, or categorized lists, use `--structured-output` and explicit `--required-field` values.
   - Do not require a CTA question unless the user's task actually asks for CTA-style writing.
   - Keep reusable rules in the system folder and execution evidence in the run folder.

5. Execute the loop
   - Use `scripts/run_loop.py next <run_dir>` to create the next iteration and enforce the audit gate.
   - Read `iteration-N/generation-instructions.md` after `next`; it is the short checklist for what must be filled before validation.
   - Produce `iteration-N/output.json`.
   - Do not leave generated templates empty. After `next`, immediately fill `output.json` or state the blocker before validating.
   - If the loop has judgment criteria, fill `iteration-N/judgment-audit.json` with evidence-backed AI or human review.
   - If `judgment-audit.json` is missing entries after output is filled, `validate_loop.py` may add pending `needs_review` entries. It does not decide subjective checks for you.
   - Run `scripts/validate_loop.py <run_dir>` to write `iteration-N/audit.json`.
   - Read `iteration-N/rewrite-plan.json` before starting the next rewrite.
   - Rewrite only failed, missing, or needs-review items unless a run-level issue requires broader changes.
   - Store screenshots, browser checks, asset manifests, command logs, playtest notes, or other quality evidence under `artifacts/` when the blueprint calls for them.
   - Repeat until the audit passes, max iterations is reached, or the loop is blocked.

6. Report
   - Use `scripts/render_report.py <run_dir>` to create a human-readable report.
   - Treat `final.md` as the evidence report: it proves the run status, audit result, accepted output, remaining issues, and event history.
   - Let the report renderer show validated outputs, including structured fields; do not manually rewrite `final.md` unless an external artifact is unavailable to the renderer.
   - After `final.md` exists, use `scripts/render_delivery.py <run_dir>` to create the standard delivery bundle:
     - `reader-report.md`: a clean reader-facing report based on the accepted output and audit state.
     - `interactive-dashboard.html`: a self-contained interactive HTML view of the accepted output, audit counts, and detected categories.
   - Treat `interactive-dashboard.html` as a visible deliverable, not just a stored file. If an in-app browser tool is available, open the dashboard before the final reply. If the browser cannot be opened, include the dashboard path and `file://` URL in the final reply.
   - If the user needs a client-ready, executive, memo, or presentation-style deliverable, create a separate reader-facing derivative file in the run folder. Preserve the evidence chain and state which accepted iteration it came from.
   - Delivery artifacts are presentation derivatives. They should make the result easier to read, but they must not replace `final.md`, `output.json`, `audit.json`, or `judgment-audit.json`.
   - Do not treat delivery polish as validation failure by default. Reopen the loop with feedback only when the accepted output violates the user's criteria, not merely because a different presentation format is needed.
   - Final answers must cite the run folder, `reader-report.md`, `interactive-dashboard.html`, dashboard URL/open status, and final audit state.

## Hard Rules

- Do not claim an iteration happened unless an iteration folder, output file, audit file, and event log entry exist.
- Do not overwrite previous iteration folders.
- Do not silently change goal, criteria, validator rules, or max iterations after the run starts.
- Do not add task-specific checks to the core validator script. Put semantic checks in `loop.json` as judgment criteria and record results in `judgment-audit.json`.
- Do not label a requirement as objective unless it uses a supported deterministic check in `loop.json`. If it needs language understanding, make it a judgment criterion.
- If a criterion is subjective, require explicit evidence in `judgment-audit.json`; if no evidence exists, mark it needs review.
- If the user rejects a `passed` result, record it with `run_loop.py feedback`; that feedback supersedes the previous pass and reopens the loop.
- Stop honestly when max iterations is reached.
- A skill cannot create background autonomy by itself. Automatic looping works only while an agent, script runner, automation, or external scheduler keeps invoking the next step.

## Statuses

- `created`: run exists but no iteration has started.
- `awaiting_generation`: an iteration folder exists and output must be filled.
- `needs_rewrite`: validation found failed objective or judgment checks.
- `needs_user_review`: only judgment evidence is missing or unresolved.
- `passed`: all required checks passed.
- `stopped_max_iterations`: the iteration budget ended before passing.
- `blocked`: required inputs or external systems are missing.

Only `passed`, `stopped_max_iterations`, and `blocked` are final statuses.

## Audit Model

Use a hybrid audit:

- Objective checks are supported deterministic script checks such as item count, required fields, length, artifact existence under the run's `artifacts/` folder, and question endings.
- Judgment checks are AI or human semantic checks with reason, evidence, and optional confidence.

The validator merges both. It does not invent semantic pass/fail decisions.

## Quality Gates

For tasks where quality depends on real usage, add a quality profile and evidence matrix:

- `content`: text quality, specificity, tone, CTA, structure.
- `code`: tests, lint, build, behavior verification.
- `research`: source quality, citations, freshness, synthesis.
- `web-app`: browser smoke tests, screenshots, responsiveness, console errors.
- `interactive`: controls, user flow, media/assets when relevant, screenshots, runtime behavior.
- `design`: visual hierarchy, brand fit, screenshots, human/AI visual judgment.

Runtime profile definitions live in `assets/profiles/*.json`. Add or edit profile packs there; do not hard-code task domains into shared scripts. Aliases such as `coding`, `qa`, and `game` may resolve to generic profiles for backward compatibility.

## Resource Routing

- Read `references/loop-design-rules.md` when designing a new loop structure.
- Read `references/interview-logic.md` when deciding what to ask the user.
- Read `references/validator-patterns.md` when choosing objective checks, evidence-backed checks, or external command checks.
- Read `references/quality-profiles.md` when the task involves product quality, UI, interactive tools, design, research, or other subjective acceptance criteria.
- Read `references/report-profiles.md` when the user asks for a client-ready report, executive summary, one-page memo, presentation outline, or says a passed `final.md` is not the report they expected.
- Read `references/visualization-delivery.md` when creating `reader-report.md`, `interactive-dashboard.html`, or any extra human-facing delivery artifact after a loop has passed.
- Use `assets/profiles/*.json` as runtime quality profile packs. Create a new JSON profile only when the default profiles cannot describe the task's quality evidence.
- Use `assets/templates/universal-loop/` as the base shape for generated loop systems.

## Common Commands

Initialize a content loop:

```bash
python loop-skill/scripts/init_loop.py \
  --root . \
  --slug linkedin-post-loop \
  --mode content \
  --quality-profile content \
  --goal "Generate 10 LinkedIn posts about AI tools and Hong Kong SMEs" \
  --target-count 10 \
  --word-min 150 \
  --word-max 200 \
  --max-iterations 4 \
  --judgment-criterion hook="First sentence resonates with the reader or raises a relevant question" \
  --judgment-criterion tone="Professional but conversational, not marketing-heavy"
```

Initialize a structured content loop:

```bash
python loop-skill/scripts/init_loop.py \
  --root . \
  --slug qa-checklist-loop \
  --mode content \
  --quality-profile content \
  --structured-output \
  --goal "Generate a traceable QA checklist" \
  --target-count 8 \
  --required-field category \
  --required-field check \
  --required-field example \
  --required-field pass_signal \
  --max-iterations 3 \
  --judgment-criterion usefulness="Each item helps a reviewer make a practical decision"
```

Start or continue a run:

```bash
python loop-skill/scripts/run_loop.py next .loops/runs/<run-id>
```

Validate the current iteration:

```bash
python loop-skill/scripts/validate_loop.py .loops/runs/<run-id>
```

Render a report:

```bash
python loop-skill/scripts/render_report.py .loops/runs/<run-id>
```

Render reader-facing delivery artifacts:

```bash
python loop-skill/scripts/render_delivery.py .loops/runs/<run-id>
```

Record user feedback that should reopen a passed loop:

```bash
python loop-skill/scripts/run_loop.py feedback .loops/runs/<run-id> \
  --severity fail \
  --note "The result technically passed, but the controls do not feel usable."
```
