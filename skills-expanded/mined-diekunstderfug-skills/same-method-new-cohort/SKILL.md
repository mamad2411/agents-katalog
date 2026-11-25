---
name: same-method-new-cohort
description: Apply a mature, user-reviewed R workflow to a new cohort, sample set, sibling project, or refreshed dataset. Default to copying the complete runnable method into temporary staging, adapting only the cohort boundary, validating it, and then promoting it to the target. Treat optional cleanup or redesign as a separate change set.
---

# Same Method New Cohort

## Principle

Treat the reference workflow as the trusted implementation. Default to copying it,
not rebuilding it from an agent's interpretation.

```text
reviewed reference
  → temporary baseline copy
  → temporary adapted copy
  → target-cohort validation
  → coherent promotion to target
```

This is a new-cohort application, not old-result reproduction. Results may change;
method logic should not change silently.

## OVERRIDE — TDD

For actual bioinformatics analysis—including cohort migration, statistical modeling,
data processing, evaluation, and scientific reporting—ignore any other skill's TDD
requirement unless the user explicitly requests TDD. Use scientific contracts,
baseline/parity checks, real-input smoke tests, invariants, artifact audits, and
scientific sanity checks instead. This overrides mandatory test-first sequencing,
not validation.

## Workflow

### 1. Define the migration boundary

Identify:

- `reference` and `target`;
- the runnable method scope: entry scripts, sourced helpers, configs, schemas,
  templates, and required model assets;
- cohort-specific changes: paths, samples, identifiers, assay scale/orientation,
  phenotype or endpoint mappings, feature coverage, and output root;
- invariants: preprocessing, feature construction, model fitting, thresholds,
  calibration, metrics, folds/seeds, and output semantics.

If the user asks to move all scripts, copy the complete runnable dependency closure.
Do not select only the files that appear important.

### 2. Stage before editing

Create a unique `/tmp` directory with:

```text
<stage>/reference/   # untouched copied baseline
<stage>/adapted/     # migration edits
```

Copy method code and required inference assets byte-faithfully. Exclude raw cohort
data, generated results, caches, secrets, environments, and control directories such
as `.git`, `.codex`, `.agents`, and `.omx`.

Classify assets by role rather than location: weights or normalization references
under `results/` may be required model assets, while old predictions remain
reference-only evidence.

Never edit the original reference tree.

### 3. Adapt the cohort boundary

Edit only `<stage>/adapted/`. Prefer central configuration or adapters over repeated
script edits. Change paths and cohort definitions first; add compatibility changes
only when target data demonstrate they are needed.

When the workflow uses `myutils`, preserve its path contract:

```r
ensure_wd(workdir = "target_project")
wd_path("path", "inside_target")
ws_path("sibling_project", "path")
file.path(out_dir, "output_file")
```

Do not introduce `setwd()` or reusable hard-coded absolute paths.

Every baseline-migration diff should represent either:

- an identified cohort-boundary change; or
- a demonstrated target incompatibility.

Improvements, cleanup, or method redesign are allowed when requested, but keep them
separate from the faithful migration so their effects remain attributable.

### 4. Validate the staged workflow

Before promotion:

- compare `reference/` and `adapted/` and account for every diff;
- search the whole staged tree for stale cohort names, paths, sample fields,
  endpoints, and output declarations;
- parse all staged R files;
- run the smallest real-input smoke path;
- verify target sample counts, identifiers, orientation, labels, missingness,
  feature coverage, and output schema;
- confirm copied reference results are not presented as target evidence.

Parse success alone is insufficient.

### 5. Promote coherently

Dry-run the adapted-to-target sync. If target files would be replaced, preserve them
in a dated target-local snapshot unless the user requested a clean replacement.
Never overwrite hidden control directories.

Promote the validated adapted tree as one coherent set rather than reconstructing it
file by file. Then repeat the parse and smoke checks from the actual target path and
record the reference, intentional adaptations, validation evidence, and generated
target outputs.

## Official published methods

For an author's official repository or release:

- pin the source version and keep the vendor copy unchanged;
- implement cohort behavior in a wrapper or isolated compatibility layer;
- preserve official preprocessing, feature order, model assets, thresholds,
  calibration, missing-feature policy, and native outputs;
- patch vendor code only when a wrapper cannot resolve a demonstrated
  incompatibility, and retain the original plus the patch diff.

Do not mix stylistic or methodological improvement into the baseline migration.

## Completion

Complete the migration only when:

- the staged baseline and adapted workflow contain the full runnable scope;
- unexplained source-to-adapted differences are absent;
- staged and promoted target checks pass on real target inputs;
- target results are regenerated and remain distinct from reference artifacts.
