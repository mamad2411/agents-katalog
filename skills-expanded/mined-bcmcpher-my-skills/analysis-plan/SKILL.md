---
name: analysis-plan
description: >
  Design a new repeated statistical or computational analysis script from scratch using
  the five-layer modular architecture: constants → data loading → atomic functions →
  output functions → orchestrator (run_one). Use this skill when a user wants to write
  a new analysis script that applies the same procedure across multiple combinations of
  inputs, asks how to structure code that loops over outcomes, predictors, conditions,
  timepoints, ROIs, cohorts, or other dimensions, or invokes /analysis-plan. This skill
  works in any scripting language (R, Python, Julia, MATLAB, shell, etc.) and for any
  kind of repeated analysis — statistical models, image processing pipelines, feature
  extraction loops, simulation sweeps, etc. If the user already has a working but
  disorganized script they want to clean up, suggest /analysis-refactor instead.
argument-hint: <description of the analysis you want to run>
user-invocable: true
---

# Skill: analysis-plan

Structure a repeated analysis before writing a single function. The discipline that
makes this work: write the orchestrator pseudocode first. That forces you to name what
every step returns before you implement it, which reveals the right function boundaries.

---

## Phase 0: Identify the unit of analysis

Before any design work, get the user to complete this sentence:

> "I want to run [PROCEDURE] for every combination of [DIMENSION A] × [DIMENSION B]."

The dimensions can be anything that varies across runs:

| Type | Examples |
|---|---|
| Metrics / features | FA, FW, MD; activation amplitudes; biomarkers |
| Outcomes / predictors | behavioral scores, clinical ratings, demographics |
| Conditions / groups | treatment arms, diagnostic categories, timepoints |
| Spatial units | ROIs, brain regions, voxel clusters, sensors |
| Data splits | cohorts, sites, subjects, folds |
| Models / pipelines | preprocessing variants, estimator configurations |

The "procedure" is whatever is repeated: fitting a model, computing a statistic,
generating a figure, running a transformation, extracting features.

If the user can't complete the sentence, ask one focused question:
**"What is one unit of work — the smallest thing you'd run once, then repeat for every combination?"**

If that still doesn't yield clarity, ask: "What is the smallest meaningful result you
want to produce? Who or what does each result belong to?" Do not proceed to Phase 1
until the unit-of-work sentence is clear. Everything else follows from it.

---

## Phase 1: Name the constants

Write the iteration dimensions and fixed configuration choices at the top of the file,
before any function. Every list being iterated over, and every parameter that is a
scientific or methodological decision (not a per-call argument), belongs here.

```
# What we iterate over
DIMENSION_A = [...]   # e.g., metrics, conditions, models
DIMENSION_B = [...]   # e.g., outcomes, ROIs, subjects

# Fixed choices that apply to every run
COVARIATES  = [...]   # e.g., age, sex, site
THRESHOLD   = 0.05    # e.g., significance cutoff, filter value
OUTPUT_DIR  = "results/my_analysis"
```

Ask the user:
1. What are the levels of Dimension A?
2. What are the levels of Dimension B?
3. What fixed methodological or scientific choices apply to all runs?

> **The buried-constants rule:** Any list that appears hardcoded inside a function
> belongs here instead. If you find yourself writing a list of conditions or outcomes
> inside a fitting or processing function, stop — that's a constant.

---

## Phase 2: Sketch the orchestrator pseudocode first

Write `run_one()` — or the equivalent orchestrator function in the user's language —
**before** implementing any of its components. This is counterintuitive but essential:
it forces you to name what each step returns before you've written it.

Structure the pseudocode as a sequence of named steps. For each step, annotate:
- What it **returns** (in one noun phrase)
- Whether it has **side effects** (writing files, updating state)

```
run_one(data, dim_a, dim_b, config):
    subset    ← prepare_data(data, dim_a, dim_b, config)     # returns: cleaned data for this pair
    result    ← fit_or_compute(subset, dim_a, dim_b, config) # returns: model/result object
    summary   ← summarize(result)                            # returns: table of key statistics

    save summary to output_path(dim_a, dim_b, "summary")     # side effect: writes file

    plot      ← make_plot(subset, result, dim_a, dim_b)      # returns: plot object
    save plot to output_path(dim_a, dim_b, "plot")           # side effect: writes file
```

Work through this with the user. For each step, ask:
- "What does this return?" If you can't answer in one noun phrase, the step is doing two things — split it.
- "Does this write a file or produce other side effects?" File-writing belongs in `run_one()` directly, or in dedicated output functions. Computation functions should be pure.

The pseudocode names your atomic functions before you implement them. Don't skip it.

---

## Phase 3: Define function contracts

From the pseudocode, make a contract for each function:

| Function | Inputs | Returns | Side effects? |
|---|---|---|---|
| `prepare_data()` | full data, dim_a, dim_b, config | filtered/cleaned subset | none |
| `fit_or_compute()` | subset, dims, config | result object | none |
| `summarize()` | result | statistics table | none |
| `make_plot()` | subset, result, dims, out_path | plot object | writes file |

Rules:
- Computation functions are pure — they return a value and touch nothing outside their scope.
- Output functions (saving figures, writing files) are the only ones with side effects.
- `run_one()` is the only function that knows the output path. It constructs paths and passes them to output functions — output functions never construct their own paths.

Confirm this table with the user before writing implementation. Design changes are
cheap here; they're expensive after functions are implemented and tested.

---

## Phase 4: Implement atomic functions, bottom-up

Implement starting from the innermost function (usually the core computation) and
work outward toward the orchestrator. For each function:

1. Write the signature with argument types documented clearly
2. Implement only what the contract specifies — nothing extra
3. Test interactively with a single (dim_a, dim_b) pair before moving on

Pause after each function and confirm with the user before proceeding. Resist wiring up
`run_one()` until the component functions are individually verified.

---

## Phase 5: Wire up the entry point last

The outer loop is the last thing written. It should look intentionally simple — all
complexity has been pushed into `run_one()` and its components.

```
create output directory if it doesn't exist

for each a in DIMENSION_A:
    for each b in DIMENSION_B:
        log("  a / b ...")
        try:
            run_one(data, a, b, config)
        except any error:
            log("  SKIPPED: " + error message)
            continue
```

The error-catching wrapper is not optional. One failure — a degenerate input, missing
data, a singular matrix, an unconverged model — should not abort the entire run.
Failed pairs are logged and skipped; the rest continue.

If the entry point looks non-trivial, that's a signal that complexity hasn't been
pushed far enough into `run_one()`.

---

## Output naming convention

Before writing any file-saving code, agree on the output path pattern:

```
results/{analysis_name}/{dim_a}_{dim_b}_{output_type}.{ext}
```

Consistent naming makes it easy to reload all outputs of a given type after the run:

```
# all summary tables
files matching: results/my_analysis/*_summary.csv

# all plots for one metric
files matching: results/my_analysis/fa_*_plot.png
```

Agree on this before any output exists — it's far easier to get right upfront than to
rename files after hundreds have been written.

---

## Design rules to maintain throughout

- Unit-of-work sentence → constants → orchestrator pseudocode → function contracts → implementation → entry point. Always in this order.
- If a list is hardcoded inside a function, it belongs in constants.
- If a function does two things, split it.
- If the entry point loop looks non-trivial, push complexity down.
- One failure must never abort the whole run.
- Output functions receive paths from the caller — they never construct their own.
- If the user already has a working script they want to improve, redirect to `/analysis-refactor`
  instead of planning from scratch.
- For parallel execution (dask, joblib, futures), the architecture still applies — the
  `run_one()` function becomes the unit submitted to the parallel executor. Note this to
  the user when they mention parallel processing.
