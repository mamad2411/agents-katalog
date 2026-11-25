---
name: pandera-validate
description: >-
  Build, review, and debug Pandera dataframe validation schemas and pipeline
  checks. Use when adding DataFrameSchema or DataFrameModel contracts, diagnosing
  SchemaErrors, or fixing pandas/Polars validation that silently misses bad data.
license: CC-BY-4.0
compatibility: Pandera 0.33.0 API baseline; behaviour verified on 0.33.0 and 0.33.1 on 2026-09-29; Python with the target dataframe backend installed in the project's environment
metadata:
  repo: https://github.com/nq-rdl/agent-extensions
---

# Pandera validation

Before changing a contract, identify the installed Pandera version, dataframe
backend, and validation call site. Keep the project's schema/model style and
dependency manager. The compatibility pin is a documentation baseline, not an
instruction to upgrade a project's dependencies.

Verify version-sensitive behavior against the [canonical documentation](https://pandera.readthedocs.io/en/stable/)
when being wrong would mislead; use matching versioned docs or upstream source
when the installed version differs.

## Select the backend before writing checks

- For pandas, use `import pandera.pandas as pa`. The top-level pandas schema
  imports are deprecated. A base Pandera install does not supply every backend;
  use the project's dependency manager to select `pandera[pandas]` or
  `pandera[polars]` when needed.
- For Polars, use `import pandera.polars as pa`. Do not port pandas callbacks
  verbatim. Native custom checks receive `PolarsData` with `lazyframe` and `key`
  and produce a LazyFrame of boolean results; prefer expressions to Python
  element-wise callbacks. See the [Polars guide](https://pandera.readthedocs.io/en/stable/polars.html).
- Other backends need their own supported-feature checks; do not convert to
  pandas merely to reuse a schema unless that materialization fits the task.

## Preserve the intended contract

Resolve these independently; do not loosen one to hide a failure in another:

- **Presence versus nulls:** `required=False` permits an absent column;
  `nullable=True` permits null cells. Neither supplies a missing column.
- **Integer nulls:** `nullable=True` cannot make NumPy `int64` hold nulls.
  For pandas nullable integers, use an extension dtype such as `pd.Int64Dtype()`
  and test coercion with real missing values.
- **Coercion:** schema-level `coerce=True` overrides column-level `coerce=False`.
  Keep coercion at column scope when only selected fields should change.
- **Extra columns:** `strict=True` rejects them; `strict="filter"` removes them.
  Filtering, adding missing columns, and dropping invalid rows are data
  transformations: use them only when the requested contract calls for them.

See [schema semantics](https://pandera.readthedocs.io/en/stable/dataframe_schemas.html).
Pass the returned validated frame downstream: coercion or filtering may have
changed it. Do not assume the original object now satisfies the contract.

## Close silent validation gaps

- A `DataFrameModel` annotation alone does not run validation. Locate an actual
  `Model.validate(...)` call or a suitable runtime decorator such as
  `@pa.check_types`; verify both input and output boundaries when requested.
  See [pipeline decorators](https://pandera.readthedocs.io/en/stable/decorators.html).
- Pandas column checks drop nulls by default. Dataframe checks differ by output
  shape: in 0.33.0, a row-indexed boolean Series can mask all-null rows, while a
  boolean DataFrame can mask individual null cells. Do not assume every row
  containing a null is skipped. For missingness or cross-column null rules, set
  `ignore_na=False`, define the null behavior, and test partly/all-null rows.
  See [check semantics](https://pandera.readthedocs.io/en/stable/checks.html).
- Polars `LazyFrame` validation defaults to schema-only checks. For value
  checks, prefer an explicit `schema.validate(lf.collect())` boundary when
  materialization is acceptable. `SCHEMA_AND_DATA` validation depth also
  materializes data internally; it is not a free lazy check. State whether
  values were actually checked.
- Pandera's `lazy=True` means aggregate validation failures, not deferred
  dataframe execution. It does not by itself enable Polars value checks.

## Diagnose and demonstrate the fix

Use `schema.validate(frame, lazy=True)` and inspect
`pandera.errors.SchemaErrors.failure_cases` to separate dtype/coercion failures,
missing columns, and failed checks. Fail-fast checks normally raise
`SchemaError`, but pandas dataframe coercion can raise `SchemaErrors` even
without `lazy=True`; catch both at a boundary that handles validation failures.
Summarize relevant failures rather than
dumping the entire input. See [lazy validation](https://pandera.readthedocs.io/en/stable/lazy_validation.html).

For a changed contract, run a valid fixture and a deliberately invalid fixture
through the real pipeline boundary. Include the edge case behind the change
(null, absent column, duplicate key, coercion, or extra column), and assert the
returned values/dtypes when transformation is intended. For Polars value rules,
include invalid values with valid dtypes so schema-only validation cannot make
the test pass accidentally. Report the backend/version and what executed.
