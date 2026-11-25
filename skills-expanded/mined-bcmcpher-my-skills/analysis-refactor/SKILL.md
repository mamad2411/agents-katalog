---
name: analysis-refactor
description: >
  Refactor an existing "linear" or copy-paste analysis script into the five-layer
  modular architecture: constants → data loading → atomic functions → output functions →
  orchestrator (run_one). Use this skill when a user has a working but unstructured
  script — code written chronologically, with variables overwritten in place, constants
  buried inside functions, or blocks copy-pasted for each outcome or condition — and
  wants to restructure it for reuse, extensibility, and clarity. Also use when a user
  says "this script is getting out of hand", "I want to add another outcome and it's
  getting messy", "help me clean up this analysis", or /analysis-refactor. Works in
  any scripting language. If the user is starting from scratch, suggest /analysis-plan
  instead.
argument-hint: <path to existing script or paste script contents>
user-invocable: true
---

# Skill: analysis-refactor

Restructure an existing sequential analysis script into the five-layer modular
architecture. The goal is not to change what the script computes — only how it is
organized, so the analysis is easier to extend, debug, and reuse without copy-pasting.

---

## Phase 0: Read the script and identify the repeating unit

If the user is starting from scratch rather than refactoring an existing script, redirect
to `/analysis-plan` instead.

Read the full script before proposing any changes. Find the implicit loop structure —
most linear analysis scripts have one, even if it isn't written as a loop.

Signs that a repeating unit exists:
- Variables overwritten in sequence (`result_fa <- ...; result_fw <- ...`)
- Copy-pasted blocks that differ only in one string or variable name
- Comments like `# now do the same for fw` or `# repeat for UPDRS_2`
- A section that would need to be duplicated to add a new outcome or condition

Complete this sentence and confirm it with the user before proceeding:

> "This script runs [PROCEDURE] for every [DIMENSION] — currently written out
> manually rather than in a loop."

If there are two nested dimensions (e.g., metric × outcome), name both:

> "This script runs [PROCEDURE] for every [DIMENSION A] × [DIMENSION B]."

This sentence is the anchor for all refactoring decisions that follow.

---

## Phase 1: Extract constants

Scan the entire script for hardcoded values that represent scientific or methodological
choices. These should move to a constants block at the top of the file — visible,
auditable, and changeable in one place.

Look for:
1. **Lists inside functions or loops** — any `c(...)`, `[...]`, or equivalent that
   enumerates outcomes, conditions, metrics, covariates, or file paths
2. **Repeated string literals** — the same column name or file path appearing in
   multiple places
3. **Implicit configuration** — filter criteria, thresholds, covariate choices, model
   specifications that are buried inside function bodies

Propose a constants block, for example:

```
# What we iterate over
DIMENSION_A = [...]   # e.g., metrics, pipelines
DIMENSION_B = [...]   # e.g., outcomes, ROIs, conditions

# Fixed methodological choices
COVARIATES  = [...]
THRESHOLD   = ...
INPUT_PATH  = "..."
OUTPUT_DIR  = "results/my_analysis"
```

Then ask the user: "Are there any choices here that should vary per call rather than
being fixed globally? Anything I've missed?"

---

## Phase 2: Isolate data loading

Find where data is loaded and globally cleaned. In a linear script, this is often
tangled with the first analysis step or scattered across multiple locations.

Extract it into a single clean block that:
- Reads from disk once
- Applies structural transformations (type casting, factor encoding, joins)
- Applies global filters that apply to **all** analyses (e.g., filtering to a specific
  shell, modality, time window, quality threshold)

Leave per-analysis subsetting (filtering to complete cases for a specific outcome,
selecting rows for one condition) inside `run_one()`, not here. Global cleaning is
auditable; per-pair cleaning is encapsulated.

---

## Phase 3: Atomize computation functions

Extract the computational operations from the linear script into pure functions.
"Pure" means: given the same inputs, always returns the same output, and touches
nothing outside its scope (no file writes, no global state mutation).

For each function, verify the single-responsibility rule with this test:
> Can you describe what this function **returns** in one noun phrase?
- ✓ "a fitted model object"
- ✓ "a table of test statistics"
- ✗ "fits the model and also writes the results CSV" — this is two things

For each extracted function:
- Name it by what it returns or computes (not by what it does to the script's flow)
- Remove any file-writing or plotting side effects — those move to `run_one()` or to
  dedicated output functions
- Ensure it takes only what it needs as arguments — no reaching into global scope

Show the user a proposed function inventory before implementing:

| Function | Inputs | Returns |
|---|---|---|
| `prepare_data()` | full data, dims, config | cleaned subset |
| `compute()` | subset, dims, config | result object |
| `summarize()` | result | statistics table |

---

## Phase 4: Separate output functions

Output functions are the only functions permitted to have side effects (writing files,
rendering figures). For each:

- Signature includes an `out_path` argument — the **caller** (run_one) constructs the
  path; the output function receives it
- The function builds the output (figure, table, serialized object) and saves to `out_path`
- Returns the output object if useful for interactive inspection, otherwise nothing

If a plot or save call is currently buried inside a computation function, extract it:
the computation returns a data object; a separate output function writes it.

---

## Phase 5: Write run_one() and the entry point

`run_one()` is the only function that knows the output path prefix. It assembles
results from atomic functions, constructs file paths, writes outputs, and calls
output functions.

```
run_one(data, dim_a, dim_b, config):
    # 1. Subset (complete cases for this pair)
    subset = prepare_data(data, dim_a, dim_b, config)
    if too few rows: raise informative error

    # 2. Compute
    result = compute(subset, dim_a, dim_b, config)

    # 3. Summarize and save
    summary = summarize(result)
    prefix = path.join(config.output_dir, f"{dim_a}_{dim_b}")
    save(summary, prefix + "_summary.csv")

    # 4. Plot and save
    plot = make_plot(subset, result, dim_a, dim_b, prefix + "_plot.png")
```

Then the entry point — which should look trivial:

```
create output directory

for each a in DIMENSION_A:
    for each b in DIMENSION_B:
        log(f"  {a} / {b} ...")
        try:
            run_one(data, a, b, config)
        except any error:
            log("SKIPPED: " + error)
            continue
```

The error wrapper is not optional. One degenerate input should not abort the whole run.

---

## Refactoring checklist

Before finalizing, verify each item:

- [ ] All iteration dimensions are in the constants block at the top of the file
- [ ] Data is loaded and globally cleaned once, before any function definition or loop
- [ ] Every computation function returns one thing and writes nothing
- [ ] Every output function receives `out_path` as an argument — it does not construct paths
- [ ] `run_one()` is the only function that constructs file paths
- [ ] The entry point loop is trivial — all complexity is inside `run_one()` and its components
- [ ] The entry point has error handling that logs failures and continues
- [ ] Output files follow a consistent `{dim_a}_{dim_b}_{type}.{ext}` naming pattern

---

## What not to change

Refactoring is structure-preserving. Do not silently change:

- The statistical model or algorithm specification
- Covariate or hyperparameter choices
- Data filtering or exclusion logic (move it, but don't modify it)
- The order of operations within a computation
- Result column names or output formats the user may already depend on

If you notice a potential bug or questionable choice while refactoring, flag it to the
user as a separate, explicit issue. Never fix it silently inside a structural change.

If the existing script has tests, preserve them. Flag any test that would break due to
the refactoring, but do not delete tests — they document prior behavior.

If the script is already well-modularized (each function < 30 lines, no repeated blocks,
clear entry point), note this to the user and confirm refactoring is still desired
before proceeding.

After the refactored structure is in place, suggest adding tests with `/retrofit-tests`
to validate the extracted functions.
