---
name: run-research
description: Execute a research roadmap by spawning an agentic team (planner, engineer, tester, runner, analyst) that reads the roadmap, writes code, tests it, runs experiments, and produces reports
argument-hint: "<roadmap-path> <scope> [--project=path] [--skip=role,...] [--rerun]"
allowed-tools: Read, Write, Edit, Bash, Glob, Grep, Agent, WebSearch, WebFetch, TaskCreate, TaskUpdate, TaskGet, TaskList, AskUserQuestion, mcp__pal__codereview
---

# Run Research Skill

Orchestrate a multi-agent research team to execute phases from a research roadmap. The team reads the roadmap, plans the work, writes code, tests it for correctness and data leakage, runs experiments, and writes comprehensive reports — all coordinated from a single `/run-research` invocation.

**Design principle:** Each agent role has a clear scope and handoff. The orchestrator (this skill) sequences them, passing artifacts between stages. All agents write to the project folder; reports go back to the vault next to the roadmap.

## Input

- **$0** (required): Path to the roadmap `.md` file, relative to `$VAULT_VAULT` or cwd
  - Example: `1-Project/2026-GraphFANS/Roadmap-Hypotheses-Validation.md`
- **$1** (required): Scope — which phases to execute
  - Examples: `"phase0"`, `"phase0 and phase1a"`, `"phase2"`, `"all"`
  - Parsed case-insensitively; matches against phase headings in the roadmap
- **--project=\<path\>** (optional): Absolute path to project code folder
  - Default: inferred from roadmap location — looks for a `code_dir` or `project_dir` field in the roadmap frontmatter, or asks the user
- **--skip=\<roles\>** (optional): Comma-separated roles to skip
  - Valid roles: `planner`, `engineer`, `tester`, `runner`, `analyst`
  - Example: `--skip=engineer,tester` to only plan, run existing code, and analyze
- **--rerun** (optional): Skip planner+engineer, re-run existing code and regenerate reports

## Workflow

### Step 0: Parse Arguments & Resolve Paths

1. Parse `$0` as `roadmap_path`. Resolve relative to `$VAULT_VAULT` if set, otherwise cwd.
2. Parse `$1` as `scope`. Normalize to lowercase. Split on "and", commas, spaces to get a list of phase identifiers (e.g., `["phase0", "phase1a"]`).
3. Parse `--project=<path>` if present. If absent:
   a. Check roadmap frontmatter for `project_dir` field
   b. If not found, search for a `pyproject.toml`, `Cargo.toml`, or `package.json` in common locations: `~/projects/<roadmap-folder-name-lowered>`, `~/projects/<project-name>`
   c. If still not found, ask the user with `AskUserQuestion`
4. Parse `--skip` and `--rerun` flags.
5. Read the roadmap file. Extract:
   - Phase sections matching the scope (by heading text containing the phase identifier)
   - Go/No-Go gate definitions
   - Success criteria
   - Resource requirements (libraries, datasets)
   - Timeline/dependency info

### Step 1: Validate Project Folder

1. Check if `project_dir` exists:
   - **Exists**: Read `pyproject.toml` / `Cargo.toml` / `package.json` to understand the project setup
   - **Does not exist**: Ask user:
     ```
     Project folder not found at <path>.
     Options:
     1. Create it now (choose: uv / poetry / pip+venv / cargo / npm)
     2. Specify a different path
     3. Connect to an existing GitHub repo (provide URL)
     ```
2. If user chooses GitHub:
   - Run `git clone <url> <project_dir>`
   - Verify clone succeeded
3. If user chooses create:
   - `mkdir -p <project_dir>`
   - Initialize with chosen package manager
   - `git init` and set up `.gitignore`
4. Verify project folder has the expected structure (source dirs, tests dir, etc.)
5. Install dependencies if a lockfile or requirements file exists

### Step 2: Planner Agent

**Skip if:** `--skip` includes `planner`, or `--rerun` is set, or a valid `plan.md` already exists in `<project_dir>/plans/`

Launch an Agent (subagent_type: Plan) with the following task:

> You are the **Planner** for a research project. Read the roadmap and create a detailed execution plan.
>
> **Roadmap file:** `<roadmap_path>`
> **Scope:** `<scope>`
> **Project folder:** `<project_dir>`
>
> Your tasks:
> 1. Read the roadmap file completely
> 2. Read existing code in the project folder to understand what's already implemented
> 3. For each phase in scope, create a detailed execution plan with:
>    - **Objective**: What this phase proves/disproves
>    - **Prerequisites**: What must exist before this phase runs
>    - **Implementation tasks**: Ordered list of code modules to write/modify
>    - **Data requirements**: Datasets, generators, parameters
>    - **Test plan**: What tests verify correctness (unit tests, integration tests, sanity checks)
>    - **Data leakage risks**: Specific patterns to watch for (train/test contamination, information from future timesteps, circular dependencies between metrics and training)
>    - **Run configuration**: Command to execute, expected runtime, output artifacts
>    - **Success criteria**: Quantitative thresholds from the roadmap's go/no-go gates
>    - **Analysis plan**: What plots, tables, and statistics to produce
> 4. Save the plan to `<project_dir>/plans/<scope-slug>-plan.md`
>
> Output the plan file path when done.

After the planner completes, read the plan and display a brief summary to the user. Ask for approval before proceeding:

```
Plan created: <path>
Phases: <list>
Estimated modules to write: <count>
Proceed? [Yes / Edit plan first / Abort]
```

### Step 3: Engineer Agent

**Skip if:** `--skip` includes `engineer` or `--rerun` is set

Launch an Agent with the following task:

> You are the **Engineer** for a research project. Write production-quality code according to the plan.
>
> **Plan file:** `<project_dir>/plans/<scope-slug>-plan.md`
> **Project folder:** `<project_dir>`
>
> **Critical rules:**
> - **No data leakage:** Never use test data during training or metric computation. Keep train/val/test splits strictly separated. Never compute evaluation metrics on the same data used to fit models or derive parameters.
> - **No circular references:** Metrics must not depend on the process being evaluated. Band boundaries must be computed independently of the signal being profiled.
> - **No hardcoded results:** Every number in output must come from actual computation.
> - **Reproducibility:** All random operations must accept and propagate seeds. Default seeds must be documented.
> - **Logging:** Use Python `logging` module. Log key intermediate values.
>
> Your tasks:
> 1. Read the plan file completely
> 2. Read existing code to avoid duplicating work
> 3. Implement each module from the plan:
>    - Write source files in the appropriate package directories
>    - Write unit tests for each module in `tests/`
>    - Write the run script(s) as described in the plan
>    - Write visualization code that saves both `.png` and companion `.md` files
> 4. After writing all code, run the tests: `cd <project_dir> && uv run pytest tests/ -v`
> 5. Fix any test failures
> 6. Report: list of files created/modified, test results

### Step 4: Tester Agent

**Skip if:** `--skip` includes `tester`

Launch an Agent (using critique-code agent profile) with the following task:

> You are the **Tester/Reviewer** for a research project. Your job is to verify the code matches the plan and contains no data leakage or scientific validity issues.
>
> **Plan file:** `<project_dir>/plans/<scope-slug>-plan.md`
> **Project folder:** `<project_dir>`
>
> Perform these checks:
>
> **1. Plan conformance:**
> - Every implementation task in the plan has corresponding code
> - Every test in the test plan has a corresponding test function
> - Run configurations match what the plan specifies
>
> **2. Data leakage audit:**
> - Search for patterns where test/validation data flows into training or parameter estimation
> - Check that spectral profiles are computed on training data only, not on the data being evaluated
> - Verify train/test splits are created before any data-dependent computation
> - Check for information leakage through shared random seeds between train and test generation
> - Look for metrics computed on the same data used to derive model parameters
>
> **3. Circular reference audit:**
> - Check that evaluation metrics are independent of the training process
> - Verify band boundaries are not derived from the same signal being band-decomposed
> - Check for self-referential comparisons (comparing a model to itself)
>
> **4. Scientific validity:**
> - Verify statistical tests use appropriate corrections (Bonferroni, etc.)
> - Check that confidence intervals / error bars are computed with enough samples
> - Verify that success criteria from the roadmap are correctly implemented as assertions or checks
>
> **5. Run all tests:** `cd <project_dir> && uv run pytest tests/ -v`
>
> Write a review report to `<project_dir>/plans/<scope-slug>-review.md` with:
> - PASS/FAIL status for each check category
> - Specific findings with file:line references
> - Severity ratings: CRITICAL (blocks execution), MAJOR (must fix), MINOR (nice to fix)
> - Suggested fixes for CRITICAL and MAJOR findings
>
> If any CRITICAL findings exist, clearly state: "BLOCKED: Do not proceed to runner."

After the tester completes:
- If **CRITICAL findings** exist: show them to the user, ask whether to fix and re-test or abort
- If CRITICAL findings exist, send them back to the Engineer agent for fixing, then re-run the Tester
- If only MAJOR/MINOR: show summary, proceed to runner

### Step 5: Runner Agent

**Skip if:** `--skip` includes `runner`

Launch an Agent with the following task:

> You are the **Runner** for a research project. Execute the experiment code and collect results.
>
> **Plan file:** `<project_dir>/plans/<scope-slug>-plan.md`
> **Project folder:** `<project_dir>`
>
> Your tasks:
> 1. Read the plan to find the run command(s) for each phase in scope
> 2. For each phase:
>    a. Run the command (e.g., `cd <project_dir> && uv run python -m graph_fans.phase0.run_profiling`)
>    b. Capture stdout/stderr
>    c. Check for errors — if the run fails, report the error and stop
>    d. Verify output artifacts exist (result files, plots, JSON)
>    e. Read the go/no-go decision files and report the gate result
> 3. Write a run log to `<project_dir>/plans/<scope-slug>-runlog.md` with:
>    - Command executed
>    - Runtime
>    - Output summary
>    - Gate decisions
>    - List of artifacts produced

### Step 6: Analyst Agent

**Skip if:** `--skip` includes `analyst`

Launch an Agent with the following task:

> You are the **Analyst** for a research project. Write a comprehensive report from the experiment results.
>
> **Roadmap file:** `<roadmap_path>`
> **Plan file:** `<project_dir>/plans/<scope-slug>-plan.md`
> **Run log:** `<project_dir>/plans/<scope-slug>-runlog.md`
> **Results folder:** `<project_dir>/results/`
> **Report destination:** `<vault_dir>/<roadmap-parent-folder>/`
>
> Your tasks:
> 1. Read the roadmap to understand hypotheses and success criteria
> 2. Read the run log for gate decisions and artifact locations
> 3. Read all result files (CSVs, JSONs) and examine result plots (PNGs)
> 4. For each phase in scope, write a report markdown file:
>    - **Frontmatter**: tags, created date, phase, gate, decision
>    - **Goal**: From the roadmap
>    - **Method**: What was done (parameters, graph families, seeds, etc.)
>    - **Results**: Tables with key numbers, embedded plots using `![[attachment-path]]`
>    - **Key Findings**: Numbered findings with analysis (what surprised, what confirmed, what complicates the next phase)
>    - **Implications**: How findings affect the next phases and the overall thesis
>    - **Code & Data**: Pointers to code and result directories
>    - **Next Step**: Link to the next phase in the roadmap
> 5. Copy result PNGs to `<vault_dir>/attachments/project-<project-name>/`
> 6. Save each report as `Report-<PhaseN>.md` in the roadmap's parent folder
> 7. Update the project `Index.md` to link to the new reports and mark phases as complete
>
> Reports should be publication-quality: precise numbers, proper statistical language, no vague claims. Every claim must reference a specific number from the results.

### Step 7: Final Summary

After all agents complete:

1. Display a summary:
   ```
   Research execution complete.

   Phases executed: <list>
   Gate decisions: <phase>: <GO/NO-GO>, ...
   Reports: <list of report paths>

   Key findings:
   - <top 3 findings across all phases>
   ```

2. If any gate returned NO-GO, highlight the fallback action from the roadmap.

3. If `--project` has a git remote, ask whether to commit and push.

## Error Handling

- **Roadmap not found**: Print error with path tried, suggest alternatives via Glob
- **Scope not matched**: List available phases from the roadmap, ask user to clarify
- **Project folder not found**: Trigger Step 1 creation flow
- **Dependency installation fails**: Show error, suggest manual fix, do not proceed
- **Engineer tests fail after 2 fix attempts**: Show failures, ask user to intervene
- **Tester finds CRITICAL issues after 2 fix cycles**: Show all findings, ask user to intervene
- **Runner experiment fails**: Show error output, check if it's OOM/timeout vs code bug, suggest fix
- **Analyst can't find results**: Check if runner was skipped, suggest `--skip` adjustment

## Examples

### Full run
```
/run-research 1-Project/2026-GraphFANS/Roadmap-Hypotheses-Validation.md "phase0 and phase1a" --project=~/projects/graph-fans
```

### Re-run experiments and regenerate reports only
```
/run-research 1-Project/2026-GraphFANS/Roadmap-Hypotheses-Validation.md "phase0" --project=~/projects/graph-fans --rerun
```

### Skip engineering, just plan and analyze existing results
```
/run-research 1-Project/2026-GraphFANS/Roadmap-Hypotheses-Validation.md "phase2" --project=~/projects/graph-fans --skip=engineer,tester,runner
```

### New project from scratch (will prompt for setup)
```
/run-research 1-Project/2026-NewProject/roadmap.md "phase0" --project=~/projects/new-project
```

## Notes

- The skill uses `Agent` tool to spawn subagents for each role. Each agent gets full context (roadmap + plan + prior artifacts).
- Agents run sequentially by design — each depends on the prior's output. The tester-engineer loop is the only case where agents may iterate.
- All intermediate artifacts (plans, reviews, runlogs) are saved in `<project_dir>/plans/` for auditability.
- Reports are written in Obsidian-compatible markdown with wikilink image embeds.
- The skill is idempotent — re-running with `--rerun` skips planning/engineering and re-executes experiments.
