---
name: cost-estimate
version: 2.0.0
description: |
  Estimate what a codebase, branch diff, or single commit would COST to build — evidence-driven, not a
  guess: measure the real scope with the helper scripts (LOC counter + git session analyzer), classify
  every source line into one productivity bucket, run the cost calculator for engineering hours,
  organizational overhead, calendar and team-cost views plus Claude ROI, and sanity-check the effective
  lines/hour — runs as a forked analysis workflow with its own reasoning budget, isolated from the main
  flow. Keeps raw engineering hours separate from overhead and team multipliers, never presents a number
  without scope, assumptions, and a confidence level, and never claims region-specific market rates
  unless the user asked and that research was actually done. Use when the user asks to estimate
  development cost, effort, engineering hours, or ROI.
allowed-tools:
  - Bash
  - Read
  - Glob
  - Grep
context: fork
agent: general-purpose
effort: high
argument-hint: "[full|branch:<name>|commit:<hash>]"
arguments:
  - request
when_to_use: |
  Use when the user asks to estimate development cost, effort, engineering hours, or ROI for the
  current repository, a branch diff, or a specific commit. Examples: "estimate cost", "how much
  would this codebase cost to build", "/cost-estimate branch:feat/foo", or "estimate this commit".
  Do NOT use to budget hosted infrastructure, price SaaS plans, or to generate a project execution DAG
  (that's plan-to-task-list-with-dag) — this prices building the code, nothing else.
---

<EXTREMELY-IMPORTANT>
This skill is an evidence-driven estimation workflow.

Non-negotiable rules:
1. Use the helper scripts under `.agents/skills/cost-estimate/helpers/` instead of redoing LOC,
   session, or cost math manually.
2. Keep scope explicit: full repo, `branch:<name>`, or `commit:<hash>`.
3. Separate raw engineering hours from organizational overhead and team multipliers.
4. Keep the pricing rubric and report schema in references, not inline in the invocation path.
5. Treat external market-rate research as optional. Use built-in rates unless the user explicitly
   requests a different market or region.
</EXTREMELY-IMPORTANT>

# Cost Estimate

## Inputs

- `$request`: Optional scope or estimation guidance such as `branch:feat/foo`, `commit:abc1234`,
  region hints, or desired audience

## Goal

Produce a credible estimate that:

- measures the requested code scope with the helper scripts
- classifies code into the right productivity buckets
- computes engineering hours and costs without double-counting overhead
- translates that estimate into realistic calendar and team-cost views
- reports assumptions, confidence, and Claude ROI clearly

## Step 0: Resolve scope and mode

Parse the request into one of:

- full repository
- `branch:<name>`
- `commit:<hash>`

If the request is ambiguous, infer full repository by default. If the user supplied region or
market hints, carry them into the final rate discussion. Otherwise use the built-in baseline rates.

**Success criteria**: The estimation target and pricing basis are explicit before running scripts.

## Step 1: Measure the real code surface with the helper scripts

Use the helper toolchain in `.agents/skills/cost-estimate/helpers/`:

- `loc_counter.py`
- `git_session_analyzer.py`
- `cost_calculator.py`
- `report_generator.py`

Run `loc_counter.py` for the resolved scope to capture:

- total lines
- file counts
- language breakdown
- directory breakdown
- source vs test vs config vs docs
- per-file category candidates from `all_files`

Run `git_session_analyzer.py` when git history is available so Claude ROI can use actual session
estimates rather than LOC fallback.

Rules:

- prefer the script output over ad hoc `find`, `wc`, or inline arithmetic
- if scope is a branch or commit, measure the diff rather than the full repository
- if git history is missing or unhelpful, fall back to LOC-based Claude hour estimates later

**Success criteria**: You have structured JSON for scope size and, when possible, active-session estimates.

## Step 2: Classify the code into productivity buckets

Review the `loc_counter.py` output and map every relevant source line into exactly one category.

Use `references/estimation-rates.md` for:

- category keys
- productivity ranges
- overhead ranges
- market-rate baselines
- role multipliers
- organizational efficiency constants
- Claude ROI constants

Classification rules:

- assign each source line once
- keep tests, config/build, and documentation separate from product code
- detect specialized work such as GPU, native interop, audio/video, system extensions, or on-device ML
- do not inflate complexity without file-level evidence
- group files when a directory clearly shares one category, but call out exceptional files separately

**Success criteria**: There is a complete category-to-line-count JSON payload for the calculator.

## Step 3: Run the calculator and sanity-check the output

Pipe the category totals into `cost_calculator.py`.

The calculator should produce:

- base coding hours
- overhead hours
- total estimated hours
- sanity-check effective lines/hour
- calendar-time tables
- engineering-only cost
- full-team cost
- Claude ROI fields when Claude hours are available

Rules:

- do not bake overhead into the category assignment; the calculator already adds overhead
- if the sanity check falls outside the target range, adjust category assignments or explain why this repo is legitimately outside the norm
- use built-in market rates by default unless the user explicitly requested a different market basis

**Success criteria**: The calculator output is internally consistent and the sanity check has been reviewed.

## Step 4: Refine Claude ROI and confidence

If session data exists, inspect it and adjust only when the default commit-density heuristic is
obviously understating large-scope work. If session data is missing, use the fallback Claude
productivity constant from `references/estimation-rates.md`.

Report:

- estimated Claude active hours
- speed multiplier vs the baseline human rate
- value per Claude hour
- headline ROI and savings

Also state confidence:

- high when scope, category mix, and history are clean
- medium when history or categorization is incomplete
- low when the request is intentionally approximate or the repo is only partially available

**Success criteria**: The ROI story is explicit, bounded, and not overstated.

## Step 5: Generate the report body

Use `report_generator.py` to generate the markdown backbone, then refine the narrative where needed.

Load `references/report-contract.md` for the required report structure and minimum sections.

The final estimate should cover:

- executive summary
- codebase metrics
- development-time estimate
- calendar-time view
- engineering-only cost
- full-team cost
- Claude ROI
- assumptions and caveats

Rules:

- lead with the executive summary and Claude ROI
- keep the report stakeholder-readable, not tool-dump heavy
- mention the scope basis explicitly
- preserve escaped currency formatting when editing prose manually

**Success criteria**: The estimate is readable, structured, and aligned with the report contract.

## Guardrails

- Do not add `disable-model-invocation`; this is a read-heavy analysis workflow.
- Do not add `paths:`; this is a generic estimation skill.
- Do not keep pricing tables, role matrices, or full report templates inline in `SKILL.md`.
- Do not replace helper-script output with manual math unless the helper chain is unavailable.
- Do not present a cost number without the scope, assumptions, and confidence level.
- Do not claim region-specific market validation unless the user explicitly requested it and that research was actually performed.

## When To Load References

- `references/estimation-rates.md`
  Use for the productivity buckets, overhead rates, market-rate baselines, team multipliers,
  efficiency constants, and Claude ROI fallback constants.

- `references/report-contract.md`
  Use for the mandatory section order, reporting contract, and required caveats.

## Helper Scripts

- `.agents/skills/cost-estimate/helpers/loc_counter.py`
  - full repo: no flags
  - branch diff: `--branch <name>` (optionally `--base <base>`)
  - single commit: `--commit <hash>`
  - output: JSON with `totals`, `by_language`, `by_directory`, `all_files`

- `.agents/skills/cost-estimate/helpers/git_session_analyzer.py`
  - all commits: no flags
  - specific branch: `--branch <name>`
  - output: JSON with `total_commits`, `total_sessions`, `estimated_active_hours`, `sessions[]`

- `.agents/skills/cost-estimate/helpers/cost_calculator.py`
  - input: pipe category JSON on stdin
  - flags: `--rate <hourly>`, `--claude-hours <N>`
  - valid category keys: `simple_crud_ui_boilerplate`, `standard_views`, `complex_ui`, `business_logic`, `database_persistence`, `audio_video_processing`, `gpu_shader`, `native_interop`, `system_extensions`, `on_device_ml`, `tests`, `config_build`, `documentation`
  - output: JSON with `base_coding`, `overhead`, `total_estimated_hours`, `sanity_check`, `calendar_time`, `engineering_cost`, `team_costs`, `claude_roi`

- `.agents/skills/cost-estimate/helpers/report_generator.py`
  - flags: `--calc <costs.json>`, `--sessions <sessions.json>`, `--project <name>`, `--scope <desc>`
  - single section: `--section <name>`
  - available sections: `executive_summary`, `development_time`, `calendar_time`, `engineering_cost`, `team_cost`, `grand_total`, `claude_roi`, `assumptions`
  - output: ready-to-paste markdown

Use these directly. The judgment work in this skill is classification, calibration, and explanation,
not reimplementing the scripts.

## Output Contract

Report:

1. resolved scope and pricing basis
2. key repo metrics and complexity drivers
3. engineering hours and sanity-check result
4. engineering-only and team-cost ranges
5. Claude ROI and confidence level
6. assumptions, caveats, and any missing-data limitations
