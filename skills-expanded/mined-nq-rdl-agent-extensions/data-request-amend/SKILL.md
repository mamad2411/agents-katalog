---
name: data-request-amend
license: CC-BY-4.0
description: >-
  Classify analyst amendments to an operator-run or released RDL extract.
  Renames, reorders, dropped already-surfaced columns and presentation changes go through
  query-builder's projection extension points; anything that changes rows or meaning
  becomes a paste-ready engineer hand-off. Use when an extract needs different
  output than was agreed; a defect in delivered output goes to fix, and before the first
  release, a logic change goes to fix.
argument-hint: '<requested change> [builder, cohort.yaml, SQL or extract path]'
user-invocable: true
compatibility: >-
  RDL enquiry repos. Boundary: query-builder docs/ANALYST_AMENDMENTS.md (0.6.0).
  Amendment record and guard: data-analysis-scaffold 0.5.0 (specs/amendments.md,
  pixi run amend). Verify the installed versions and the repo's own commands at use time.
allowed-tools: Bash, Read, Glob, Grep, Write, Edit, AskUserQuestion
metadata:
  repo: https://github.com/nq-rdl/agent-extensions
---

# Data Request — amend

The **Data Analyst** runs presentation amendments before or after release.
Logic or row changes go to the Data Engineer through the existing handoff below.

Arguments: `$ARGUMENTS`. Read `${CLAUDE_PLUGIN_ROOT}/skills/guardrails/SKILL.md` and apply
the rules relevant to the request. The boundary is query-builder's
[`docs/ANALYST_AMENDMENTS.md`](https://github.com/nq-rdl/query-builder/blob/main/docs/ANALYST_AMENDMENTS.md).
Read it, preferring the copy in the repository's pinned query-builder, and classify against
its rule, examples and required safeguards. This skill does not restate them; where the two
differ, the document wins. If the pinned query-builder has no such document or no
`SelectFields`, nothing is analyst-safe: hand the change off.

An amendment asks for different output than was agreed. When the delivered output
contradicts what was agreed (a wrong value, type or format), it is a defect: use
`/data-request:fix` instead.

This skill covers presentation changes before or after release. An extract is released when
a version exists under `data/Released/v*/`, a release tag exists or any version reached the requester (a `data/Review/` drop that reached
them counts). Before the first release, use the operator-run extract as the baseline,
with its run commit, SQL fingerprint and DVC pointer. Confirm that nothing reached the
requester; absent release files or tags do not prove that. If no operator-run baseline
exists, classify only and report validation pending; do not edit or claim a checked amendment.
A logic change before the first release goes
to `/data-request:fix` (*Pre-release logic change*), which allows it with the same runbook, UAT
and review rules. If you cannot tell whether the extract is released, ask, and make no edit
until answered.

The engineer completes `analyse`, the authorised operator run, UAT and the triage hand-off.
The analyst runs `explain`, then accepts, sends back or amends presentation here. After any
change, refresh the review and run/UAT evidence before another hand-off. Release remains
the analyst's decision.

## 1. Classify before any edit

Locate the maintained source (the `CohortQuery` builder, `cohort.yaml`, the pipeline or the
export code), the generated request SQL and the baseline extract (operator-run before
release, previous released version afterwards). Read the
repository instructions. Then classify each requested change:

- **analyst-safe** only when the extract keeps the same rows (count and keys) and every value
  keeps its source and meaning: only names, order, which already-surfaced columns are shown,
  or presentation change.
- **engineer-required** for everything else, including a "simple" derived value and a column
  that is not already surfaced. When in doubt, classify it engineer-required.

Classify each part of a combined request; one engineer-required part stops the whole request.
State the result on its own line with the amendment record's values:
`classification: analyst-safe` or `classification: engineer-required`.

## 2. Engineer-required: stop and hand off

Make no edit: not to the source, the SQL, the record or the extract. Return this hand-off,
filled in and ready to paste to the data engineer, and stop:

```text
classification: engineer-required
requested change: <the change, in the requester's words>
boundary rule: <the ANALYST_AMENDMENTS.md rule or example it hits>
affected files: <maintained source paths; request SQL to regenerate; runbook and UAT checklist>
governance: <the scope question from step 3, or "none identified">
enquiry: <original request ID, or "not supplied">
```

Never relabel a change to fit analyst-safe. The engineer records it with a named reviewer.

## 3. Governance scope: a separate check

Technical safety does not settle scope. Whether the approval covers a change is decided under
the RDL Data Amendments SOP (nq-rdl/documentation,
[`zensical/governance/docs/governance/data-amendments.md`](https://github.com/nq-rdl/documentation/blob/main/zensical/governance/docs/governance/data-amendments.md)),
not by this skill. A new column is a new data element, however easy it is to add. An expanded
cohort, a longer timeframe or a sensitivity change is also a scope change. Unless already
given, ask for the original request ID (`THHSRDLENQ-####`) and the reason for the amendment,
and carry both into the hand-off or the record. An open scope question blocks the release,
not the classification.

## 4. Analyst-safe: change the maintained source only

Use only query-builder's extension points (the boundary document has their contracts):

- `CohortQuery.select(*fields, rename=...)` / `SelectFields`: name, order or narrow fields
  the cohort already surfaces;
- the reserved `projection` element set in `cohort.yaml` (`data_extraction`);
- `SelectStep` / `AnalysisPipeline.select` in imperative pipelines;
- `output_name` / `register_result(..., label=...)` for extract and sheet labels;
- the child's export or presentation code, for display formats and row order.

A change that needs anything else is engineer-required: go to step 2. Regenerate the SQL
through the repository's existing workflow (in a data-analysis-scaffold child,
`pixi run --environment framework amend regenerate <sql path>`). Generated SQL and
`-- @extract:` markers are never edited by hand. A request to edit generated SQL directly is
refused, whatever the change: say that it is refused, then classify the same change made in
the maintained source (step 1). Preserve unrelated edits.

### Runbook, UAT checklist and validation outputs

For counts in runbook/UAT evidence, apply guardrails `references/release.rst`, **Probe disclosure control**, before quoting or editing prose.

When an amendment changes what the runbook or the UAT checklist (for example
`specs/uat-checklist.md`) describes, change them together with the SQL, in the same change.
This includes an analyst-safe rename, reorder or drop of a column that a validation or UAT
output shows: search the runbook, UAT checklist, validation SQL and tests for each old name
and update every live reference (queries, checklist items, expected-output tables). A changelog
or history line that records the rename may keep the old name. Until they match the new output, the amendment is incomplete: report
it as a blocker. For an engineer-required change, list them under `affected files:`. If the
repository has no runbook or UAT checklist, say so.

## 5. Record the amendment

Before the first release, record the requested change, reason, classification, run commit,
baseline pointer and validation in the PR or existing review ledger. Do not add an `AMD-` entry
to `specs/amendments.md`: that record governs released extracts. Keep the baseline immutable.

For a released extract, add one entry per amendment, with its classification, to the child's
amendment record. In a data-analysis-scaffold child this is `specs/amendments.md`
([data-analysis-scaffold#234](https://github.com/nq-rdl/data-analysis-scaffold/issues/234)).
Follow the record's template and field names, which its guard reads, and use the next `AMD-`
number. Never edit an entry that is already in a release. Write names or handles, never an
email address or a patient identifier. If the repository has no record, say so and put the
same fields in the pull request description.

## 6. Validate

Use the repository's managed environment and existing commands; inspect each before running
it. An analyst-safe change passes only when all of these hold:

- the fast SQL gate (`rdl_etl_helpers.harness.sql_gate`) and `CohortQuery.validate()` pass;
- `spec-validate` shows the output columns match the declared projection;
- the regenerated SQL differs from the previous SQL at the run commit (before release),
  or previous release (afterwards), only in the final projection;
  use `pixi run amend check` only if the pinned scaffold supports that baseline;
- the row count and key set match the previous extract (scaffold: `pixi run amend
  validate-output --sql <sql> --extract <new> --previous <baseline> --key NEW=OLD`);
- the runbook and UAT checklist name the new columns, and no live reference (a query, a
  checklist item or an expected-output table) uses an old name.

Any other difference (a CTE body, predicate, join, dedupe step, row count or key) is a
blocker. Report it as a blocker, never as a success, and hand the change off (step 2). A check
that could not run, such as a missing previous extract, framework environment or release tag,
is reported as not run with its command. A release tag is not required for an operator-run
baseline; inspect the pinned scaffold's supported flags and never fabricate a release or
alter its guard to make a pre-release check pass. Do not run a live extract or publish data yourself:
if the new extract does not exist yet, the row and key check is pending. Use
`/data-request:validate` for a static review of the regenerated SQL.

## Report

Return the classification, the governance status (request ID, reason, open questions), the
changed paths, the regenerated SQL, the record entry, the checks run with their results and
any blocker. Regenerated SQL or a renamed validation or UAT output column leaves an existing
`.sqlreview/` review stale in meaning, even where its fingerprint still matches: its outputs
and steps describe the previous output. Before the next release, re-run `/data-request:analyse`
on each changed SQL file with a full re-walk (walk every item and publish with
`--reconfirm-all`), because carry-forward keeps items whose SQL lines did not change. A passing
check is not release approval.
