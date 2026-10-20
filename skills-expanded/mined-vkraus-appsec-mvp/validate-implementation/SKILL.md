---
name: validate-implementation
description: Use after generate-connector to run the connector's pytest suite, emit the Validation table per REQ-ID (PASS/FAIL/N/A), produce a fix list for failing REQs, and update the Validation and Implementation log sections of mkdocs/docs/connectors/{category}/{source}.md. Inputs are source name, category (cmdb, scm, sast, sca, secrets, dast, or waf), and connector module path.
---

# validate-implementation

## Overview

This skill runs `pytest tests/connectors/{source}/`, summarises outcomes into a per-REQ-ID Validation table, emits a fix list for failing REQs, and updates the Validation and Implementation log sections of the connector page at `mkdocs/docs/connectors/{category}/{source}.md`. It is observational over the codebase: it modifies only the per-connector Markdown page.

## Inputs

- **Source name** — determines the test directory `tests/connectors/{source}/` and the connector page filename slug.
- **AppSec category** — one of `cmdb`, `scm`, `sast`, `sca`, `secrets`, `dast`, `waf`. Determines which `references/<category>.md` to load. The category-applicable REQ-ID set, with explicit N/A reasons drawn from `mkdocs/docs/platform/reference/catalog.md`, lives in `references/<category>.md` and is the load-bearing per-category artefact for this skill.
- **Connector module path** — `src/connectors/{source}/`. Used to resolve the per-source code under test for the fix list and as input for the Implementation log row.

Preconditions:

- The connector module and test suite at `src/connectors/{source}/` and `tests/connectors/{source}/` exist (typically emitted by `generate-connector`).
- The connector page at `mkdocs/docs/connectors/{category}/{source}.md` exists with a stub Validation section (an `!!! info "Pending validation"` admonition emitted by `analyze-source`) and an Implementation log table whose row 4 is marked `(pending)`.

## Output

- The Validation section of `mkdocs/docs/connectors/{category}/{source}.md` is updated: the stub admonition is replaced with a populated REQ-ID table whose rows are exactly the category's applicable REQ-IDs (in catalog order), each cell carrying `PASS`, `FAIL`, or `N/A` (`N/A` for REQ-IDs the category excludes per `references/<category>.md`).
- A fix list is appended below the table as plain text: for each `FAIL` row, the failing test file path and a one-line summary of the failure.
- The Implementation log section row 4 (`validate-implementation`) is updated with the run date, inputs (the connector module path), outputs (the connector page §5), and the skill repo ref (`git rev-parse --short HEAD`).

No file outside the connector page is modified by this skill.

## Procedure

1. **Read `references/<category>.md` to get the category's applicable REQ-ID set and N/A reasons.** This is the load-bearing per-category artefact for this skill — it lists which REQ-IDs bind to tests for connectors in this category, in catalog order, with explicit N/A reasons quoted from `mkdocs/docs/platform/reference/catalog.md` and `mkdocs/docs/connectors/<category>/index.md`. Also read `operational.yml.databricks_runtime.ingestion_path`. Apply any per-`ingestion_path` N/A overrides documented in the category reference (e.g., `lakeflow_connect` sources flip `REQ-ING-PAG`, `REQ-ING-RL`, `REQ-ING-HWM` to `N/A` on the cmdb branch with rationale "delegated to Lakeflow Connect").
2. Run `pytest tests/connectors/{source}/ -v --tb=short`. Treat timeouts as failures (not skips). Capture stdout/stderr; preserve the wall-clock duration for the run summary.
3. Collect every test function carrying a `@pytest.mark.requirement("REQ-...")` marker and its outcome (`passed` / `failed` / `skipped` / `timed-out`).
4. For each REQ-ID in the category's applicable set (from step 1, in the order they appear in `mkdocs/docs/platform/reference/catalog.md`), record: is there a bound test? did it pass? what is the test path? For REQ-IDs marked N/A by the category reference, record `N/A` with no bound test path.
5. Emit the Markdown table with one row per REQ-ID using `PASS`, `FAIL`, or `N/A`. The table columns match the example at `mkdocs/docs/connectors/cmdb/servicenow.md` § "## Validation" (`Requirement | Bound test | Outcome`). For N/A rows, the bound-test cell is `—`.
6. Emit the fix list as plain text below the table: for each `FAIL` row, one line listing the failing test file path (`tests/connectors/{source}/test_*.py::test_name`) and a one-line summary of the failure drawn from the pytest `--tb=short` output. Omit the fix list entirely if there are no failures.
7. Replace the stub admonition in the **Validation** section of `mkdocs/docs/connectors/{category}/{source}.md` with the table from step 5 and the fix list from step 6 (if any). Append a one-line summary noting how many requirement-bound tests were collected, the wall-clock duration, the pass / fail / N/A split, and the N/A rationale for the category (sourced from `references/<category>.md`).
8. Update the connector page's Implementation log section row 4 (`validate-implementation`) with the run date, inputs (the connector module path `src/connectors/{source}/`), outputs (the connector page §5), and the skill repo ref via `git rev-parse --short HEAD`. Use the row template below.
9. Record the per-source aggregator row data in the run report — Source name, Category, four skill-run dates from the connector page's Implementation log section, Status `Generated`. The controller appends this to the platform-level aggregator table during a separate consolidation step. Do not edit `mkdocs/docs/platform/reference/connector-skills.md` from this skill.

## Invariants

- No production code is modified by this skill. It is purely observational; the only file written is the connector page at `mkdocs/docs/connectors/{category}/{source}.md`.
- Test timeouts are treated as failures, not skips. A timed-out test contributes a `FAIL` row.
- The Validation table always has exactly the REQ-IDs in the category's applicable set as rows, in the order they appear in `mkdocs/docs/platform/reference/catalog.md` § "Requirement catalog". REQ-IDs the category excludes per `references/<category>.md` appear as `N/A` rows, not as omissions.

Category-specific invariants (which REQ-IDs apply, the canonical N/A reason for each excluded REQ-ID, and the test-suite assertions a category's tests must verify) live in `references/<category>.md`. Read the file matching the input category before drafting the Validation table.

## Implementation log row template

Overwrite the `(pending)` placeholder for `validate-implementation` (row 4) in the connector page's Implementation log table. Use this row shape verbatim, replacing the bracketed placeholders:

```
| Validation | validate-implementation ({category}) | module path=src/connectors/{source}/ | mkdocs/docs/connectors/{category}/{source}.md §5 | {YYYY-MM-DD} | {git_short_sha} ({branch}) |
```

- `{category}` — the AppSec category input (`cmdb`, `scm`, `sast`, `sca`, `secrets`, `dast`, or `waf`).
- `{source}` — the source name input.
- `{YYYY-MM-DD}` — the run date in ISO format.
- `{git_short_sha}` — output of `git rev-parse --short HEAD` on the skill's repo.
- `{branch}` — output of `git rev-parse --abbrev-ref HEAD`.

Rows 1 (`analyze-source`), 2 (`provision-source`), and 3 (`generate-connector`) MUST remain untouched.
