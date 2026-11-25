---
name: explore-dataset
description: Reproducible exploratory analysis before any model is trained — detect the language and ecosystem in play (Python/pandas, Java data mining, R, SQL-only), profile shape and types, quantify missingness and outliers, check correlations, hunt target and temporal leakage, and reach an explicit verdict on whether the dataset can answer the stated question. Use when starting a new analysis or ML project, when someone hands over a dataset with no documentation, before any modelling pipeline is built on top of it, or when a model's suspiciously high accuracy needs an explanation. Produces docs/data/<dataset>.profile.md and a leakage checklist.
allowed-tools: Read Grep Glob Bash Write Edit
argument-hint: "[dataset-path] [--question \"...\"]"
user-invocable: true
context: fork
agent: foundry-data:data-analyst
model: sonnet
effort: medium
background: false
metadata:
  foundry.vertical: data
  foundry.io: "requirement.v1 -> plan.v1 + docs/data/<dataset>.profile.md"
license: Apache-2.0
---

# Explore a dataset

One dataset, one documented, checkable answer to "can this data support the question that was asked".
The deliverable is not a wall of plots — it is a profile document someone else can reread in six
months and a verdict they can act on without re-running anything.

The order below matters: leakage found in step 7 routinely overturns conclusions drawn in steps
3–6, and the honest verdict in step 8 is worthless if it is written before the leakage check.

## When not to use this

- **The profile already exists and the extract is unchanged** (same hash, same row count) —
  re-run only the steps affected by what changed, do not regenerate from scratch.
- **The question is a routine aggregate answerable by a dashboard or a single query.** This skill
  exists to feed a modelling decision; for reporting, use the BI tool or
  `foundry-dev:optimise-query` instead.
- **There is no static extract yet**, only a live stream. Freeze a dated sample first — exploring
  a moving target produces conclusions that are stale before anyone reads them.
- **A model already exists and the question is about its performance**, not the data → use
  `evaluate-model`.
- **The artefact under audit is a text corpus for retrieval**, not tabular/feature data →
  `foundry-ai:build-rag-pipeline` step 1 covers that shape of audit better.

## Step 1 — detect the ecosystem before choosing tools

Do not assume pandas. The same repository may hold a Python notebook pipeline and a Java
data-mining module (regression trees, pattern mining) over the same or a related dataset, and the
right diagnostic tool depends on where the code actually runs.

Probe every marker in the table in `references/ecosystem-detection.md`, and probe the whole tree:
a depth cap hides `src/main/resources/*.arff` and `models/**/*.sql`, which is how a mixed
repository gets reported as single-stack.

```bash
scan() { find . \( -name .git -o -name node_modules -o -name .venv -o -name venv \
                   -o -name target -o -name build -o -name dist \) -prune -o "$@" -print; }

# Python / notebook
scan \( -iname "pyproject.toml" -o -iname "requirements*.txt" -o -iname "environment*.yml" \
        -o -iname "Pipfile" -o -iname "*.ipynb" \)
# JVM build files, then the ARFF extracts and the Weka/Smile imports that prove data mining
scan \( -iname "pom.xml" -o -iname "build.gradle*" -o -iname "libs.versions.toml" \)
scan -iname "*.arff" | head -20
grep -rlE '^[[:space:]]*import[[:space:]]+(weka|smile)\.' --include='*.java' . 2>/dev/null
# R — a repository of loose scripts usually has no DESCRIPTION and no .Rproj
scan \( -iname "DESCRIPTION" -o -iname "*.Rproj" \); scan -iname "*.R" | head -20
# SQL / warehouse / dbt
scan -iname "dbt_project.yml"; scan -iname "*.sql" | head -20
```

Record which stack is present, and if more than one is, which one the dataset in scope actually
feeds — do not profile with pandas a dataset that will be consumed by a Java `weka.core.Instances`
pipeline and vice versa; the type-inference and missing-value conventions differ. Ecosystem
detection details and the tool-equivalence table (profiling call in pandas vs. the Weka/Smile/R
equivalent): `references/ecosystem-detection.md`.

**Gate:** if the ecosystem is ambiguous or genuinely mixed, say so in the profile doc rather than
picking one silently.

## Step 2 — establish shape and provenance

- Row count, column count, file size, format, encoding, delimiter, and the timezone of any
  timestamp column.
- How the extract was produced (the query, export job or API call) and when. An extract with no
  recorded provenance and date is not reproducible — treat producing that record as part of the
  deliverable, not an afterthought.
- Compute and record a content hash and row count for the extract; every later reference to "the
  dataset" in the profile doc means this exact hash.

## Step 3 — profile every column

- Inferred type vs. declared type: numeric-looking strings, mixed types inside one column,
  booleans stored as `0/1/Y/N` inconsistently.
- Cardinality for categoricals, and a judgement on which columns are genuine categories vs. free
  text vs. identifiers that merely look numeric (order ids, hashed keys).
- Distribution shape for numeric columns (skew, multi-modality, a plausible unit).
- Date/time columns validated for range sanity and monotonicity where monotonicity is expected.

## Step 4 — quantify missingness

- Percent missing per column, and a stated hypothesis on the mechanism — missing completely at
  random, missing at random given another column, or missing not at random (missingness depends on
  the unobserved value itself). State which hypothesis was tested and how, not just the percentage
  — and note that MCAR and MAR are testable on the extract while MNAR is not, so MNAR is recorded
  as a domain judgement and a disclosed limitation, never as a mechanism that was checked.
- If missingness correlates with the target, decide explicitly whether that is a genuine signal
  (the business process itself skips a field for a reason related to the outcome) or a leakage
  artefact (the field is only populated *because* the outcome already happened) and record which.

Method and diagnostics per data type: `references/missing-and-outliers-recipes.md`.

## Step 5 — quantify outliers

- Choose the method per column family and state the choice: IQR fences, z-score, domain-specific
  bounds (a negative age, a percentage over 100). Applying one method uniformly to every numeric
  column without checking it fits is the most common way this step produces nonsense.
- Distinguish data-entry errors (impossible values) from genuine extreme events (legitimate rare
  cases the model must still see). Only the former gets removed or capped by default.

Method and diagnostics: `references/missing-and-outliers-recipes.md`.

## Step 6 — correlations and redundancy

- Pairwise correlation among features: Pearson for linear numeric pairs, Spearman for monotonic
  ones, Cramér's V for categorical pairs. State which was used per pair type — a Pearson matrix
  over categoricals encoded as integers is a common and silent error.
- Near-duplicate or fully duplicate columns, and duplicate rows — count them, and separately count
  duplicates that straddle any grouping (customer, session, patient) that will later define a
  train/test split, because that count feeds step 7.

## Step 7 — leakage detection, the step most skipped

Work through the full catalogue — target leakage, temporal leakage, group/entity leakage, proxy or
identifier leakage, and pipeline leakage from preprocessing fit before a split. Each entry names
the symptom, the check, and the fix: `references/leakage-patterns.md`.

**Gate:** for every feature whose correlation with the target exceeds the threshold stated in the
profile doc, write one sentence explaining why that feature would legitimately be available at the
moment the prediction is actually needed. A feature that cannot pass that sentence is dropped, or
flagged and excluded from the "sufficient" verdict in step 8 until it is resolved.

## Step 8 — the honest verdict

Write an explicit judgement — **SUFFICIENT**, **INSUFFICIENT**, or **SUFFICIENT WITH CAVEATS** —
against the stated question, reasoned from: sample size vs. the granularity the question needs
(a question about a rare subgroup needs rows in that subgroup, not just rows overall); class
imbalance vs. the cost of the decision at stake; missingness vs. which fields are actually
necessary to answer the question; and every leakage finding from step 7. Write it as a sentence a
non-technical stakeholder can read and act on, not as a list of statistics.

If no question was stated, do not skip this step — write "cannot be judged without a stated
question" explicitly and stop; profiling without end is not a deliverable.

## Step 9 — write it down

`docs/data/<dataset>.profile.md`, in this order: ecosystem detected; provenance, extract date and
hash; shape; per-column profile table; missingness findings and mechanism judgement; outlier
method and decisions per column family; correlation and duplication findings; the leakage
checklist with a verdict per flagged feature; the final SUFFICIENT/INSUFFICIENT/CAVEATS verdict
against the stated question; open risks; review date ≤ 90 days.

Emit `plan.v1` to `.foundry/blackboard/<wave>/explore-dataset.json` with `outOfScope` naming every
column, segment or time range deliberately excluded from the analysis.

## Exit criteria

1. Ecosystem detected and recorded from actual marker files, never assumed.
2. Shape, provenance, extract date and content hash recorded.
3. Every column profiled: inferred vs. declared type, cardinality or distribution, missing %.
4. Missingness mechanism reasoned about and stated, not only tabulated.
5. Outlier method stated per column family, applied, and spot-checked by hand on flagged rows.
6. Correlation matrix computed with the method stated per pair type; duplicate rows counted,
   including duplicates across any future split boundary.
7. Every feature above the stated correlation threshold passed the "legitimately available at
   prediction time" sentence test, or is explicitly dropped/flagged.
8. An explicit SUFFICIENT / INSUFFICIENT / SUFFICIENT WITH CAVEATS verdict is recorded against the
   stated question, or explicitly deferred because no question was given.
9. `docs/data/<dataset>.profile.md` exists; `plan.v1` validates with a non-empty `outOfScope`.

## Degradation

- **No stated question yet** → do not fabricate one to complete step 8; record the deferral and
  stop, so nobody downstream mistakes profiling activity for an answer.
- **Dataset too large to load in memory** → sample deliberately, stratified on the target if one is
  known, and state the sample size, method and seed in the profile doc. Note explicitly that this
  lowers confidence in findings about rare classes or rare segments.
- **`superpowers` installed** → use `superpowers:systematic-debugging` when an anomaly cannot be
  explained immediately (an unexplained spike, a leak, a drift between two extracts): one
  hypothesis at a time, each falsified with a query before moving to the next. If it is not
  installed, apply the same one-hypothesis-at-a-time discipline by hand and record the reasoning
  trail in the profile doc regardless — the discipline is what matters, not the tool.

## Deliberately not covered

Feature engineering and model training (`train-model`), model performance metrics and error
analysis (`evaluate-model`), production monitoring of a shipped model (`productionise-notebook`),
text-corpus audit for a retrieval index (`foundry-ai:build-rag-pipeline`), and database schema or
query-level optimisation (`foundry-dev:optimise-query`).

## Bundled references

- `references/ecosystem-detection.md` — marker files per stack and the tool-equivalence table
  (pandas/scikit-learn, Java data-mining stacks such as Weka or Smile, R, SQL-only).
- `references/leakage-patterns.md` — target, temporal, group, proxy and pipeline leakage, each
  with its symptom, its diagnostic and the fix.
- `references/missing-and-outliers-recipes.md` — missingness-mechanism tests and outlier methods
  per data type, with the diagnostic to run before choosing one.
