---
name: future-experimental-design
version: 0.0.5
description: >
  Design experiments and research protocols before data collection — select design type, randomization, blocking, treatment combination layout,
  and ensure experimental results are interpretable. For planning studies, assigning subjects/samples to groups, randomization, blocking, stratification,
  controls, factorial/fractional factorial designs, DOE, screening multiple factors, response surface optimization, crossover/repeated measures/split-plot designs,
  cluster randomization, Latin squares, well-plate layouts, batch/run order effects, replication vs. pseudoreplication, and sequential/adaptive designs.
category: methodology
metadata:
  requires:
    bins: ["python3"]
origin: K-Dense-AI/scientific-agent-skills (MIT license)
allowed-tools: Bash(future:*)
---

# Experimental Design

## Overview

Research design — how experimental units are assigned to conditions, what is held constant, what is manipulated, and in what structure —
determines what questions the data can answer. No amount of analysis can rescue a confounded or pseudoreplicated design.
This skill focuses on decisions made **before** data collection: selecting designs that isolate the target effect, supporting causal inference through randomization,
removing known noise variation through blocking, and constructing multi-factor experiments so effects are estimable rather than entangled.

The three principles behind nearly every good design (Fisher's three principles):
- **Randomization** — Randomly assign treatments so known and unknown confounders balance in expectation. This is the foundation that turns comparisons into causal inference.
- **Replication** — Independent repeats at the correct level to estimate variability. The most common fatal error is **pseudoreplication**: treating multiple measurements on the same unit as independent replicates.
- **Blocking / local control** — Group similar units (by batch, date, location, litter), randomize within blocks, and remove noise variation from the error term.

This skill helps you choose a design type, generate reproducible randomization or DOE layouts, and avoid structural errors that make data uninterpretable.

## When to Use This Skill

- Planning any comparative experiment or trial and deciding how to allocate experimental units
- Randomizing subjects/samples to groups (simple, block, stratified, or cluster randomization)
- Removing noise variation through blocking or stratification
- Designing multi-factor experiments: full factorial or fractional factorial, screening designs
- Optimizing responses for continuous factors (response surface designs)
- Within-subject/repeated measures, crossover, split-plot, or Latin square designs
- Cluster/group-randomized designs (sites, clinics, classrooms, litters)
- Determining the number and level of replicates, avoiding pseudoreplication
- Sequential, group sequential, or adaptive designs with interim analyses
- Well-plate/batch layouts and randomized run orders to avoid drift

## Dependencies

No installation is needed for a conceptual design discussion. For script execution,
first check the available interpreter and dependencies. If installation is needed,
load `future-software-install`, reuse the user's authorization and use a task-local
virtual environment with this skill's `requirements.txt` (resolve its absolute path).
Do not install unpinned packages into the user's global Python environment.

`pyDOE3` is the maintained fork of pyDOE/pyDOE2, providing full factorial, fractional factorial, Plackett-Burman,
central composite, Box-Behnken, and Latin Hypercube generators. Accompanying scripts wrap these capabilities,
returning design matrices with named columns in actual factor units and randomized run orders.

---

## Choosing a Design

Start from the research question and the structure of the experimental units, not from a favorite design.

```
What do you want to learn?
│
├─ Compare a few pre-defined conditions (A vs B vs C)?
│   ├─ Units are independent, with possible known noise factors (date, batch, site)?
│   │     → Completely randomized (no noise) or randomized block design.
│   ├─ Each unit can receive each condition in sequence (with washout)?
│   │     → Crossover/repeated measures design (potential precision gain; assess carryover).
│   └─ Only groups can be randomized, not individuals (schools, clinics)?
│         → Cluster-randomized design (account for clustering; see pseudoreplication).
│
├─ Screen many factors (5+), finding the vital few?
│     → Fractional factorial or Plackett-Burman screening design.
│
├─ Quantify main effects and interactions for a few factors?
│     → Full 2^k factorial design.
│
├─ Find settings that optimize a response (curvature matters)?
│     → Response surface design: central composite or Box-Behnken.
│
└─ Explore a continuous space for simulation/computer models?
      → Space-filling design: Latin Hypercube.
```

Detailed guides for each branch:
- **Randomization, blocking, stratification, controls** → `references/randomization_and_blocking.md`
- **Factorial, fractional factorial, screening, response surface, DOE concepts (aliasing, resolution)** → `references/factorial_and_doe.md`
- **Crossover, repeated measures, split-plot, Latin square, cluster, nested designs** → `references/design_types.md`
- **Sequential, group sequential, and adaptive designs (interim analysis)** → `references/sequential_and_adaptive.md`

---

## Generating Designs

Three scripts generate allocation and design layouts. Validate their invariants before use in a real study. Run from this skill's `scripts/` directory or add to `sys.path`.
Use the compatible versions in `requirements.txt` in a task-local virtual environment. Record script/skill and dependency versions, inputs and seed with the allocation schedule. A seed alone does not preserve output across code changes; never rerandomize an enrolled study merely because the helper was upgraded. Before changing these scripts, run `python -m unittest discover -s tests -v` from this skill directory. Tests cover seed reproducibility, sample counts, unit identity, matrix rank and invalid inputs.

### Randomization/Allocation Schemes — `scripts/randomization.py`

```python
from randomization import (
    simple_randomization, block_randomization,
    stratified_block_randomization, cluster_randomization,
    assign_factorial_runs, arm_balance,
)

# Permuted blocks keep arms balanced throughout enrollment (good for n < ~100 or sequential enrollment — simple randomization can drift unbalanced at small sample sizes)
sched = block_randomization(n=60, arms=["treatment", "control"], seed=42)

# Balance known prognostic variables by randomizing within each stratum
sched = stratified_block_randomization({"siteA": 30, "siteB": 30},
                                       arms=["drug", "placebo"], ratio=(2, 1), seed=42)

# Randomize entire groups, not individuals (groups are the experimental units)
sched = cluster_randomization(["clinic1", "clinic2", "clinic3", "clinic4"], seed=42)

arm_balance(sched)            # Check that group counts are reasonable
sched.to_csv("allocation_schedule.csv", index=False)
```

How to choose: **Simple randomization** is fine for large samples but may be imbalanced for small ones; **block randomization** preserves the ratio within complete blocks (a final partial block can be imbalanced);
**stratified block randomization** additionally balances known prognostic factors; **cluster randomization** is required when the intervention is delivered at the group level.
See `references/randomization_and_blocking.md`.

### DOE Matrices — `scripts/doe_designs.py`

```python
from doe_designs import (
    full_factorial, two_level_factorial, fractional_factorial,
    plackett_burman, central_composite, box_behnken, latin_hypercube,
)

# Factors defined with actual (low, high) ranges -> design returns actual units
factors = {"temp_C": (20, 60), "conc_mM": (1, 10), "pH": (6, 8)}

# Full 2^3: all main effects + all interactions (8 runs), run order randomized
design = two_level_factorial(factors, seed=42)

# 2^(4-1) fractional factorial: 4 factors in only 8 runs (generator uses Yates notation)
f4 = {"A": (10, 50), "B": (100, 200), "C": (0.1, 1.0), "D": (5, 25)}
design = fractional_factorial(f4, generator="a b c abc", seed=42)
# See "Yates notation quick reference" below for generator parameter details

# Low-cost screening of 7 factors (min_runs=12 provides residual degrees of freedom;
# interpreting these as error still assumes the omitted effects are negligible)
many = {f"factor_{i}": (0, 1) for i in range(7)}
design = plackett_burman(many, seed=42, min_runs=12)

# Central composite design: default face='inscribed' keeps axial points within factor ranges
# (Legacy default 'circumscribed' extends axial points outside ranges, no longer recommended)
design = central_composite({"temp_C": (20, 60), "conc_mM": (1, 10)}, seed=42)

design.to_csv("experimental_runs.csv", index=False)
```

**Yates notation quick reference** (for the `generator` parameter of `fractional_factorial`):
```text
'a b'         = 2^2 full factorial, 4 runs
'a b c'       = 2^3 full factorial, 8 runs
'a b c abc'   = 2^(4-1) fractional factorial (resolution IV), D aliased with ABC interaction
'a b c ab ac' = 2^(5-2) fractional factorial (resolution III), 8 runs
```
Each lowercase letter defines a factor column; multi-letter tokens (e.g., `abc`) alias that factor with an interaction effect.
Higher resolution means less aliasing. See `references/factorial_and_doe.md` for details.

Run order is randomized by default to prevent confounding factors with time/drift (equipment warm-up, reagent aging).
See `references/factorial_and_doe.md` for how to choose generators, interpret alias structures, and select resolution.

### Advanced Designs — `scripts/experimental_designs.py`

```python
from experimental_designs import (
    crossover_design, latin_square_design,
    repeated_measures_design, randomize_run_order,
)

# Cyclic Latin crossover: period-balanced for complete sets of k subjects.
# NOT a carryover-balanced Williams design; assess washout and period effects.
cross = crossover_design(["DrugA", "DrugB", "Placebo"], n_subjects=12, seed=42)

# Latin square design: simultaneously controls two blocking factors (rows and columns)
square = latin_square_design(["A", "B", "C", "D"], seed=42)

# Repeated measures: exact subject count; randomized between-subject assignment.
# Time order stays pre -> 1mo -> 3mo. Use randomize_within=True only for
# exchangeable treatments, never for chronological measurement times.
rm = repeated_measures_design(
    between_subject_factors={"group": ["drug", "placebo"]},
    within_subject_factors={"time": ["pre", "1mo", "3mo"]},
    n_subjects=20, seed=42
)
```

⚠️ Assess carryover, washout feasibility and period effects before choosing crossover.
The cyclic Latin helper does not balance ordered treatment pairs; incomplete sets may
also lose period balance. For repeated measures use a dependence-aware analysis
(e.g. mixed models, GEE or an appropriate paired analysis), not independent-observation tests.

---

## Mistakes That Ruin Studies

These are structural — they cannot be fixed at the analysis stage, only avoided at the design stage.

1. **Pseudoreplication.** Treating repeated measurements on one unit as independent replicates: 3 mice with 100 cells measured each —
   for the treatment applied to the mice, n = 3 (mice), not n = 300 (cells).
   Replication must occur at the level where treatment is randomized. This error has invalidated a large number of published experiments.
   Randomize and replicate at the correct level; respect the nested structure in analysis (mixed models). See `references/design_types.md`.
2. **Noise variable confounding.** All treatment samples run on Monday, all controls on Tuesday — treatment is completely confounded with date.
   Randomize or block against every noise factor you can name (batch, date, plate, technician, instrument, location).
3. **Missing or broken randomization.** Convenience allocation (first arrivals → treatment group) lets confounders in. Use a seeded scheme and follow it strictly.
4. **Missing proper controls.** Without parallel controls (and associated vehicle/sham and blinding),
   you cannot separate the treatment effect from time, placebo, or procedural effects.
5. **Batch effects mistaken for biological effects.** Especially in omics, process samples across batches in randomized/blocked order;
   never align batch with condition.
6. **Plate edge/position effects.** Evaporation and temperature gradients make plate edge positions different.
   Randomize or block sample positions; don't put all controls in column 1.
7. **Ignoring aliasing in fractional factorials.** Low-resolution fractional factorial designs confound main effects with interactions;
   understand your alias structure before asserting a factor "has no effect."
8. **Curvature without response surface.** Two-level factorial designs cannot detect curved responses; you'll miss internal optima.
   Use response surface designs.

---

## Workflow

1. **State the research question, experimental unit, and response variable.** What is being randomized? What is being measured? At what level are the true independent replicates? This determines everything that follows.
2. **List noise factors** (batch, date, location, operator, position) — plan to block, stratify, or randomize against each.
3. **Use the decision tree and reference files to choose a design.**
4. **Determine the number of replicates at the correct level** (use standard power analysis methods to calculate required sample size n for the chosen design).
5. **Generate the layout using `randomization.py` / `doe_designs.py`**, with a fixed seed.
6. **Randomize the run/treatment order** and well-plate/batch positions.
7. **Document** the design, seed, and protocol (pre-register when possible) so the analysis is confirmatory and the layout is auditable. In human trials, restrict access to the seed and future allocation schedule to preserve allocation concealment; a reproducible public seed must not reveal assignments to recruiters.
8. **Match analysis to design** — blocks, strata, clusters, and nesting must be reflected in the model (reflect blocking, stratification, clustering, and nesting structure in the analysis model).

---

## Resources

### Scripts
- `scripts/randomization.py` — Seeded allocation schemes: `simple_randomization`,
  `block_randomization`, `stratified_block_randomization`, `cluster_randomization`,
  `assign_factorial_runs`, `arm_balance`.
- `scripts/doe_designs.py` — DOE matrices in actual units: `full_factorial`,
  `two_level_factorial`, `fractional_factorial` (requires Yates notation generator), `plackett_burman` (supports min_runs to avoid saturated designs),
  `central_composite` (default face='inscribed' to avoid axial points going out of bounds), `box_behnken`, `latin_hypercube`.
- `scripts/experimental_designs.py` — Advanced experimental designs: `crossover_design`,
  `latin_square_design`, `repeated_measures_design` (repeated measures / split-plot), `randomize_run_order`.

### Reference Documents
- `references/randomization_and_blocking.md` — Randomization methods, blocking, stratification, controls, blinding, batch/plate layouts.
- `references/factorial_and_doe.md` — Factorial and fractional factorial designs, resolution and aliasing, screening and response surface methodology.
- `references/design_types.md` — Completely randomized, randomized block, crossover, repeated measures, split-plot, Latin square, cluster, and nested designs; deep dive into pseudoreplication.
- `references/sequential_and_adaptive.md` — Group sequential designs, alpha spending, interim stopping, and adaptive sample size re-estimation.

### Classic References
- Fisher, R. A. (1935). *The Design of Experiments*.
- Montgomery, D. C. (2019). *Design and Analysis of Experiments* (10th ed.).
- Hurlbert, S. H. (1984). Pseudoreplication and the design of ecological field
  experiments. *Ecological Monographs*, 54(2), 187–211.
- Lazic, S. E. (2016). *Experimental Design for Laboratory Biologists*.
