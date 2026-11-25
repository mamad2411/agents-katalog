---
name: data-request-fix
license: CC-BY-4.0
description: >-
  Fix a defect or make a decided pre-release logic change in RDL request SQL and Python:
  query results, transformations, identifier types, export formatting, keys, joins and
  filters. Use for a defect with a concrete expected result, released or not, and for a
  logic change confirmed to come before an extract's first release. A request for
  different output from a released extract goes to amend.
argument-hint: '<issue description> [SQL or Python path]'
user-invocable: true
compatibility: >-
  RDL request repos; verify the repository's SQL dialect, Python environment and installed library versions at use time.
  record_assumption/record_limitation need query-builder 0.6.0 or later.
allowed-tools: Bash, Read, Glob, Grep, Write, Edit, AskUserQuestion
metadata:
  repo: https://github.com/nq-rdl/agent-extensions
---

# Data Request — fix

The **Data Engineer** applies technical fixes and settled pre-release changes.
The Data Analyst resolves any missing research decision with the requester.

Arguments: `$ARGUMENTS`. Read `${CLAUDE_PLUGIN_ROOT}/skills/guardrails/SKILL.md`
and apply the rules relevant to the affected SQL or source mappings. This action
works without `.sqlreview/`; a small correction does not require setup, bootstrap
or a formal review before editing.

Locate the reported file and trace the affected output back through SQL aliases,
casts and joins, Python loaders and transformations, and the final serializer or
spreadsheet writer. Read repository instructions and the relevant request, schema,
column specs and tests. Follow generated SQL to its generator or resolver; fix the
maintained source and regenerate through the repository's existing workflow.

Establish the observed and expected values at the boundary where they diverge.
Inspect only the evidence needed for this defect; unrelated source metadata need
not block a formatting fix. If the file or expected meaning cannot be identified,
ask for the missing detail while continuing independent investigation. Implement
settled requirements directly; ask before choosing a different population, grain
or business meaning.

A reported “defect” that is really a presentation change request goes to `/data-request:amend`
before or after release. Other released change requests use amend's engineer hand-off;
before the first release, a logic change uses *Pre-release logic change* below.
If you cannot tell whether it is released, ask, and make no edit in either skill until answered.

## Pre-release logic change

An extract is released when a version exists under `data/Released/v*/`, a release tag
exists or any version of it reached the requester. A `data/Review/` pointer is a release
candidate, not a release; if its data reached the requester, for UAT or otherwise, the
extract is released. Treat an extract as unreleased only on positive confirmation: the
human, or the service-desk issue, says that nothing was delivered. Absent signals do not
prove it: legacy or seed repositories and manual deliveries leave no `data/Released/v*/`
or tag. If you cannot tell, ask, and make no edit here or in `/data-request:amend` until
answered: the release state determines the amendment baseline and record.

While no release exists, a full logic change is allowed here: population, keys, grain,
joins, filters, deduplication or source mappings. Make it only for a settled decision,
such as a recorded decision ID with its reason; do not choose the new meaning yourself.
Approval scope still applies: a new data element, a wider cohort or a longer timeframe is
a governance question (`/data-request:amend` step 3). If the change moves the grain, keys
or population in an existing `scope.json`, update it with `/data-request:bootstrap --update`.
Change the maintained source and regenerate the SQL; never hand-edit generated SQL.
Then verify it as in *Verify the correction*.

For counts in runbook/UAT evidence, apply guardrails `references/release.rst`, **Probe disclosure control**, before quoting or editing prose.
Change the runbook and the UAT checklist (for example `specs/uat-checklist.md`) together
with the SQL, in the same change. This includes a renamed validation or UAT output column:
search the runbook, UAT checklist, validation SQL and tests for each old name and update
every live reference (queries, checklist items, expected-output tables). A changelog or
history line that records the rename may keep the old name. An SQL change without its runbook and UAT checklist changes is incomplete;
report it as a blocker. If the repository has no runbook or UAT checklist, say so. Do not
add an `AMD-` entry to `specs/amendments.md`, which records changes to released extracts;
put the decision and its reason in the pull request.

The existing `.sqlreview/` review is stale in meaning: its purpose, grain, outputs,
assumptions and limitations describe the old logic, even where a fingerprint still matches.
Before the first release, re-run `/data-request:analyse` on each changed SQL file with a
full re-walk: walk every item and publish with `--reconfirm-all`. Carry-forward would
otherwise keep items whose SQL lines did not change, although their meaning did. A passing
local check or `/data-request:validate` does not replace it.

## Identifier and export defects

For a request such as “`Encounter_id`, `Test_encounter_id` and `Event_id` appear as
`123,456,789`; output `123456789`”, check whether commas exist in the serialized
value or only in the viewer's numeric format. Check the SQL result type, Python
dtype, formatter and export settings before selecting the correction. A screenshot
or grouped display alone does not establish that the stored identifier is wrong.

Treat identifiers according to the output contract, not as quantities to format.
Remove grouping at the responsible boundary; do not change database column types,
join keys or every numeric column to solve a presentation defect. Preserve leading
zeroes where meaningful, exact large identifiers, and nulls without turning them
into literal `"nan"`, `"None"` or `"<NA>"`. Avoid float round-trips: if precision or
leading zeroes were already lost upstream, fix ingestion from an authoritative
source rather than attempting to reconstruct the original ID. Do not strip all
punctuation from opaque IDs unless the contract establishes that it is formatting.

Child tests must check item identifier lists and must not pin revision numbers in scope/review records.

## Verify the correction

**Name the constant, never its value** in scope/review prose, drafts, logic descriptions,
questions, change summaries, runbooks and UAT notes (for example, `EVENT_CD`). A code value
in prose is a defect; never add it to `.pii-code-values` or suppress the PII gate to clear it.
When updating a scope/review draft, run
`bash "${CLAUDE_PLUGIN_ROOT}/skills/setup/scripts/sqlreview.sh" lint --ste "<draft path>"`
before presenting it. `code-value` reports each maximal run of 8 to 10 digits by item/field,
without the value; validated machine metadata is exempt (SQL path/bound slug, fingerprints
and ISO timestamps at known locations). Preserve that metadata; never reword it to clear lint.
Reworded confirmed items need fresh human confirmation via bootstrap
or analyse; do not edit final JSON or create `.sqlreview/` just for a small correction.

Make the smallest source change that resolves the reported defect, preserving
unrelated edits. When the fix changes a filter, join or meaning in pipeline or
resolver code, add or update its `record_assumption()` / `record_limitation()` call
at that point (guardrails); remove a record whose logic the fix removes. Use the
repository's managed environment and existing checks. For a genuinely stated engineer
decision, use `Engineer decision (<login>, <date>), flagged for the data analyst` in the
rationale/consequence, retaining the actual human handle and original date or UTC ISO
precision. Never substitute a role label, recorder or invented approval. Preserve separate
origin/source evidence; changes need fresh review, not backdated confirmation.
Inspect test/export commands before running them; exercise the affected path with
local synthetic fixtures, without querying a live database or publishing exports
as part of a code fix. Verify correctness-critical API behavior against the
installed version's canonical documentation when local code/tests do not settle it.

For an identifier correction, check the actual serialized value and, where relevant,
cell type/number format for an ordinary ID, a leading-zero ID, a null and an ID
beyond floating-point exactness. Confirm unrelated numeric outputs retain their
formats and row counts/keys are unchanged. Add a focused regression test when the
repository has a suitable test path. For SQL logic changes, use
`/data-request:validate` for the applicable static checks.

Report the cause, changed paths, resulting behavior, checks run and remaining gaps.
Preserve `.sqlreview/` snapshots, JSON confirmations and history; a code fix cannot
approve a review or clear stale state. Existing review fingerprints cover SQL only:
a Python-only change may affect delivered data without marking the review stale.
Call out that impact and recommend `/data-request:analyse` when a refreshed formal
handoff is needed (a pre-release logic change requires it; see above); do not claim
release approval from a passing local check.

After correction, the engineer refreshes `analyse`, the authorised operator run and UAT,
then uses the triage hand-off to the analyst. The analyst runs `explain`, accepts, sends
back or amends presentation, then prepares and publishes the release.
