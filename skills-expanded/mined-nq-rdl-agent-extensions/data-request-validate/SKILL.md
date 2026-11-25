---
name: data-request-validate
license: CC-BY-4.0
description: >-
  Validate RDL request or cohort SQL against its requirements, column specs and shared
  guardrails; report technical findings and evidence without creating a confirmed review.
argument-hint: '<sql path> [scope path] [--autonomous|--co-develop]'
user-invocable: true
compatibility: RDL cohort SQL; verify deployed SQL dialect/version and current dataops schema/index metadata.
allowed-tools: Bash, Read, Glob, Grep, AskUserQuestion
metadata:
  repo: https://github.com/nq-rdl/agent-extensions
---

# Data Request — validate

The **Data Engineer** runs technical validation. Research questions belong to
the Data Analyst and retain analyst attribution through the scope handoff.

Read `${CLAUDE_PLUGIN_ROOT}/skills/guardrails/SKILL.md` first. Arguments: `$ARGUMENTS`.
Read the SQL, request and available scope; validate the actual SQL bytes, not a stale
review snapshot. This action needs no `.sqlreview/` setup and creates no review record.

Trace population, exclusions, grain, window boundaries and output columns against the
request. Follow column-spec provenance to dataops DDL comments for timezone/units and
check current index definitions for filter and join choices. Inspect resolver code
and tests when SQL is generated. Apply each relevant guardrail with file/line evidence.

Use an existing repository lint/parser command when its dialect is configured and
it is a local, read-only check. Inspect the command before running it; do not install
a new lint stack, execute SQL against a database or modify data as a side effect.
When no suitable tool is available, perform a static review and say so. Parser success
does not establish cohort correctness, and a static index assessment is not a plan.

## Pre-run plausibility: operator proposals only

Read guardrails `references/performance.rst`, **Pre-run plausibility**. Return a proposed
count-only probe for **each label column** across all final outputs, using its inventory table;
show exclusions or unresolved metadata explicitly. Include expected raw labels/format from the
scope and data dictionary, SQL location, bounds/cost and suppression parameter. Propose an
age-band probe only for expensive requests with cited cost evidence; otherwise state why omitted.

This stage runs **no SQL** and must not connect to a database, inspect live catalogs or invoke
an extract runner, even to test a proposed probe. Database-capable clients, credentials and an
operator proposal are not execution authorisation. Mark every probe **proposed, not executed**;
static validation does not establish plausibility. Check proposals and any cited results
against **Probe disclosure control** in
`${CLAUDE_PLUGIN_ROOT}/skills/guardrails/references/release.rst`, including the
boundary table and probe-sentence lint contract. The authorised operator runs approved probes
before the delivery run; retain unresolved thresholds/bounds as reasons not to run.

Return findings with severity, SQL location, rule/requirement, observed evidence,
effect on the result and a proposed correction. Distinguish **observed problems**,
**unverified facts** and **checks passed**, and list commands actually run with their
results. Missing DDL/column specs or an unresolved population definition prevents a
fully verified conclusion; report the gap without claiming the SQL is correct.

**Autonomous:** finish every check supported by available evidence and return remaining
questions. **Co-develop:** discuss ambiguous intent or competing corrections with the
human and update the findings. Infer mode from the request when omitted. Do not edit
SQL or carry an unanswered question forward as confirmation.

Use `/data-request:fix` for targeted corrections or `/data-request:draft` to develop SQL.
`/data-request:amend` classifies an analyst amendment to a released extract.
`/data-request:analyse` remains the separate
human-confirmed handoff: this technical validation does not approve assumptions,
advance snapshots or clear stale review state.
