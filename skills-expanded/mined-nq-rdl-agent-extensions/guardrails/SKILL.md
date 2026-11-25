---
license: CC-BY-4.0
description: >-
  Apply advisory RDL cohort-SQL guardrails when drafting, changing, mapping, validating
  or reviewing request pipelines, SQL and query-builder resolvers. Covers spec
  composition, indexed filters, source timezones, join evidence and researcher
  modelling choices, with pointers to authoritative sources.
argument-hint: '[request, SQL path or resolver]'
user-invocable: true
compatibility: >-
  RDL cohort SQL; DATEADD and sys catalog examples target SQL Server 2022 (16.x).
  record_assumption, record_limitation and isolation_level need query-builder 0.6.0 or later.
  rdl-service-desk/query-builder is the retired legacy org.
  Source patterns from issues 313, 325 and 370 to 389 (2026-09-15 to 2026-09-28).
  Composition examples are schematic; verify pinned library APIs, deployed engine
  and current metadata.
allowed-tools: Read, Glob, Grep, AskUserQuestion
metadata:
  repo: https://github.com/nq-rdl/agent-extensions
---

# Data Request — guardrails (Data Engineer / Data Analyst)

Shared advisory spine for RDL request repos and query-builder: apply to composition and SQL even outside formal review.
Ordinary composition needs no `.sqlreview/` setup; hand SQL needs the lift ledger (experimental hook off).

## Engineer decisions: proceed and flag

Proceed on evidenced technical choices; only unresolved authority questions block dependent work.
Read [references/decision-authority.rst](references/decision-authority.rst) for ownership/provenance, batched questions and narrow scope; no tool permission or confirmation is granted. Read [references/grain.rst](references/grain.rst) to settle grain from intake/prior-delivery/element evidence, preserve finer outputs and report drift once; bare `Patient` is unconfirmed.

## House defaults

The cohort is **Townsville University Hospital**, facility string `00200`, unless the request explicitly changes the cohort's facility set to another facility, the whole HHS or a network-wide cohort.
This house default was confirmed by Data Engineer **JoshKgh** on **2026-09-29** ([#436](https://github.com/nq-rdl/agent-extensions/issues/436)). Apply it without asking; record one upstream-marked assumption, not a new request-specific decision.
Read [references/sources.rst](references/sources.rst) for HBCIS/ePADT fields, ieMR facility-crosswalk verification and exception routing; setup's recurring-decisions reference owns the wording and recorded confirmation.

## Confirm sources before using a fact

Locate the relevant sources in the supplied workspace or connected repositories:
- **dataops `CREATE TABLE` definitions and their comments** are authoritative for schema, field timezone and units;
  inspect DDL/index comments for join rationale. Record the file/table/column and revision read.
- **query-builder column-spec metadata** points to each field's meaning, timezone and units.
  Follow its provenance to the dataops DDL; read the existing resolver's docstring and tests for
  implemented mapping, required joins and their performance or correctness rationale.
- **Current index definitions** establish key order and usable join/filter paths. Use an existing plan
  or authorised read-only plan inspection to check performance. Without SHOWPLAN or VIEW DATABASE STATE,
  use the catalog-metadata route in [references/performance.rst](references/performance.rst).
- **Request and confirmed scope** establish population, grain, anchor, time window and output meaning;
  they do not override storage facts.

dataops covers ieMR only, and many of its comments are empty. When it has no entry
or no comment for a field, use the fallback evidence order in
[references/sources.rst](references/sources.rst): dataops, then query-builder
`schema_extracts/`, then `ColumnMeta`, then an operator probe tagged OBSERVED or
INFERRED with its scope. It also gives the dataops paths and how to cite an uncurated dump.

Search by the actual table/column/resolver names; do not invent a column-spec path,
metadata key, missing sibling implementation or database access. When sources conflict,
show both locations and use dataops as ground truth for storage facts; flag stale
consumer metadata. Library behaviour comes from the pinned implementation and tests.
When evidence is unavailable, label the affected decision unverified and ask only for the missing source/decision needed to proceed. Never fill gaps from a field name.

Verify correctness-critical syntax against the deployed engine's canonical docs
([SQL Server documentation](https://learn.microsoft.com/en-us/sql/t-sql/language-reference))
and storage facts against the current dataops DDL before presenting a result as verified.

## Compose library units in requests

Atomic, testable Layer-1 `Spec`s, `@resolves` resolver handlers and reusable helpers
belong in `nq-rdl/query-builder`. Request pipelines compose those units:
`CohortQuery(resolver).add(spec_a).add(spec_b)` with resolver/spec instances.
A PyPika `TemporaryTableQueryBuilder` pipeline composed over the request's own local
`TypedTable` definitions is also compliant composition, not hand SQL and not
evidence of a library gap.
Before SQL outside the composition API, inspect the actual dependency pin's spec,
resolver and tests. Record a `candidate` in the pipeline's `.sqlreview` lift ledger
with that pin, inspected paths/revisions, need, shortfall and workaround location.
Read `${CLAUDE_PLUGIN_ROOT}/skills/setup/references/lifts.rst` for the record and
publish commands. Capture silently, with no confirmation question mid-draft;
classification and confirmation belong to `/data-request:lift` at close-out.
**No published entry means no hand SQL.** A missing source is not proof of a gap.
The ledger permits a pinned-deadline workaround under this guidance, but does not
override an explicit repository prohibition. Check the request's dependency pin
before using an enhancement.

A mapping run never initialises `.sqlreview/`; stages that own the store (setup,
bootstrap, a writable draft) still `init` a missing one. When the task is read-only, the
repository cannot be written, or a mapping run finds no `.sqlreview/`, use
**proposal-only mode**: return the candidate entry as text in the task output instead
of publishing it. A proposal-only entry authorises no hand SQL: none is committed or
run, except exempt probes, until a writable run publishes the entry.
An operator probe is exempt only when it is aggregate-only, small-cell suppressed and
bounded to a single scan, returns no patient identifier and no staff or person key,
feeds no delivered extract, and records any `NOLOCK` or `READ UNCOMMITTED` use.
`lifts.rst` gives both rules and the `/data-request:lookup` code-discovery probe case in full.

For N related datasets from one cohort, check the pinned `create_temp_table()`,
`register_result()` and `execute_pipeline_results()` implementations first:
materialise the cohort once, then register the related result sets against it.
Do not default to separate lookups that extract IDs and re-scan with `IN()`.
Verify availability/signatures in the pinned core and tests; sufficient existing
units make this request-specific composition, not a library enhancement.

Use [the shared library release discovery policy](references/library.rst) for
current tags and source paths (`clinical/specifications.py`, `clinical/resolver.py`,
`clinical/query.py`, `pypika_queries/queries.py`, `resolvers/iemr/resolver.py`,
`resolvers/hbcis/resolver.py`). The former separate plugins package is archived.
Re-check the pinned implementations and tests before adapting examples; the latest
release does not establish availability in an older pin.

Read the request's pin (`framework_ref`, `pyproject.toml`, lock file) before drafting.
`rdl-service-desk/query-builder` is the retired legacy org. Older scaffold renders
still pin it (scaffold v0.1.3 defaulted to its `v0.1.1`, which also lacks
`register_result`), and GitHub redirects the old path, so an install can still succeed.
Below `v0.6.0`, `record_assumption` and `record_limitation` are absent. Flag a pin on
that org, or on `nq-rdl/query-builder` below `v0.6.0`, as a **blocker**: report the pin
and the missing APIs, and propose a compatible released re-pin before drafting new SQL.
Scaffold v0.5.0 defaulted to query-builder v0.5.0; inspect a fresh render's actual pin
rather than assuming that the current scaffold default has changed. Amending or fixing an already-delivered
enquiry is exempt: it stays on its delivered pin, with no backport. Agents never
re-pin or run `copier update` unasked.

Confirm the applicable rules in the current `.specify/memory/constitution.md`:

- `nq-rdl/query-builder` Constitution:
  core packages must not construct SQL with f-strings or string concatenation.
  Its narrow exception for commented resolver SQL that PyPika cannot express does
  not authorise raw SQL in a request pipeline.
- `nq-rdl/data-analysis-scaffold` Constitution:
  raw f-string SQL construction is prohibited outside template scripts.

The `falls_service_cohort.py` Indigenous-status lookup in
[#325](https://github.com/nq-rdl/agent-extensions/issues/325) illustrates the change:

```python
# Before: _build_indigenous_status_sql(...) hand-builds an SQL f-string.
# After: compose verified library units (schematic; check pinned signatures).
# resolver is a configured IEMRResolver instance.
query = (
    CohortQuery(resolver)
    .add(EncounterIdAnchor(...))
    .add(WithIndigenousStatus(...))
)
```

`nq-rdl/query-builder` issue #109 tracked the active-current and display-resolution
enhancement behind this example; it closed for the v0.6.0 release.
The issue is a discovery pointer, not proof that a request's installed version has it.

## Record assumptions and limitations where the logic makes them

With query-builder 0.6.0 or later, call `pipeline.record_assumption(text, rationale=...)`
beside the join, filter, exclusion or source read that commits to one reading of the
request or source data, and `pipeline.record_limitation(text, consequence=...)` where
the code accepts a known weakness. Resolver handlers record on the `pipeline` they
receive. `finalize()` / `build()` render the records as the SQL's leading comment header,
which `/data-request:analyse` reads as review evidence, so do not keep them in a separate
notes file. Write text an analyst can confirm or reject. A plugin that assembles SQL
without `finalize()` puts `pipeline.analysis_header()` first. Below 0.6.0 the API is
absent: report the items in the task output and recommend the pin bump; never
hand-write the header. Verify behaviour against the installed version and the
[analysis-notes contract](https://github.com/nq-rdl/query-builder/blob/main/docs/ANALYSIS_NOTES.md).

For a stated decision use `Engineer decision (<login>, <date>), flagged for the data analyst` in the rationale/consequence.
Use the actual human handle and original date/UTC instant, never role labels or invented approval; preserve independent origin/source.
Advisory: flag a filter, join or exclusion settling an ambiguous request or accepting a source weakness with no nearby record.

## Performance: shift the anchor

Keep a filtered indexed column bare. In the incident behind #313, wrapping
`PERFORMED_DT_TM` in `DATEADD` prevented an index-friendly range predicate.
Transform the bounds into the column's stored timezone instead. Illustrative T-SQL
using [DATEADD](https://learn.microsoft.com/en-us/sql/t-sql/functions/dateadd-transact-sql),
**only after confirming UTC storage and fixed UTC+10 anchors**:

```sql
WHERE ce.PERFORMED_DT_TM >= DATEADD(hour, -10, @window_start_aest)
  AND ce.PERFORMED_DT_TM <  DATEADD(hour, -10, @window_end_aest)
```

The half-open interval is illustrative: preserve agreed boundaries; do not silently replace inclusive endpoints,
choose nine months or use fixed offsets where daylight-saving applies. Check bound types/implicit conversions;
a bare column alone does not prove an index seek.
Render datetime bounds as `'YYYY-MM-DDTHH:MM:SS'`; `'YYYYMMDD'` is safe only for midnight bounds. A `DATETIME` column
reads `'YYYY-MM-DD'` by the login's language ([SET DATEFORMAT](https://learn.microsoft.com/en-us/sql/t-sql/statements/set-dateformat-transact-sql)), and day-first logins misread it.

A table with no usable index (only a clustered key, or a `mart_v` view, which has no
index metadata) gets no benefit from a bare column. Bound it by date, scan it once
into a `#temp` table, and work from `#temp`. Read
[references/performance.rst](references/performance.rst) for this route, the no-plan
metadata probes and the probe design rules.

## Read isolation

Record any `NOLOCK` or `READ UNCOMMITTED` use, in probes and extracts alike. Uncommitted
reads are not reproducible, so never make them the default for a final research
extract. Whenever an extract reads uncommitted data, record an assumption that says so.
query-builder exposes `isolation_level` from v0.6.0 (ADR 0001); inspect the request's
pin for per-table `WITH (NOLOCK)` hints (ADR 0004), rather than assuming absence. Read
[references/performance.rst](references/performance.rst) and the request repo's own
`docs/READ_ISOLATION.md` where it has one.

## Timezone and source system

The seed incident involved **BI-Reporting AEST** and **ieMR/emr UTC**. Treat these as
source-level clues to verify, not a per-field truth table. Confirm each participating
field and anchor via its DDL comments and column spec before comparing timestamps.
Reconcile into the filtered column's timezone by transforming the anchor; avoid
double conversion when a view or resolver already normalises it. Record the verified
source and conversion in the task output, rather than copying field facts into this skill.

## Join and index patterns

For any spec/resolver that requires a join, make the requirement and its rationale
discoverable in the resolver's docstring/tests, column-spec metadata and dataops
DDL/index comments. Inspect those sources for the actual tables and pinned resolver;
cite which locations and revisions you checked, what each establishes, and any
missing evidence. When changing a resolver, document and test its join requirement
and flag missing or stale metadata/comments for the owning repository.

For person-level clinical-event selection, start with the known RDL pattern
**`CLINICAL_EVENT → ENCOUNTER → person`**: the seed environment has no person-leading
index on `CLINICAL_EVENT`. Confirm current key order, encounter/person keys and
cardinality in DDL/index definitions before choosing the exact join. Do not infer
that a person identifier's presence makes direct person filtering efficient.

Every source needs its own grain check; the pattern above does not transfer. ieMR
`SCH_APPT` holds one row per role per appointment, and a flat table such as
BI-Reporting `OPD_Appointments` has no encounter join at all. For HBCIS–ieMR joins
(the `mart_iemr_hbcis_mapping_*` views and their uniqueness guard) and the
`CLINICAL_EVENT` `VALID_UNTIL_DT_TM` currency caveat, read
[references/sources.rst](references/sources.rst).

Check whether multiple encounters/events multiply the intended output grain. Choose
joins or existence checks from the requested population and verified relationships;
do not conceal an incorrect join with `DISTINCT`. If current indexes justify a
different path, explain the evidence rather than treating the seed as timeless.

## Leave modelling choices to the researcher

The library supplies atomic, verified facts and flags known intrinsic data-quality
caveats. The researcher chooses how those facts define an outcome or exposure;
encode that choice in the request's spec composition, not an implicit resolver default.

- **Patient identity:** use the raw HBCIS episode MRN as the URN unless the request asks for merged identities. Then use `HBCISResolver(canonicalize_mrn=True)` (query-builder 0.6.0 or later, #150, ADR 0003), not a hand-written merge chain.
- **Mortality:** supply date of death with its source limitation.
  `nq-rdl/query-builder` issue #79 describes an ieMR source that undercounts deaths
  outside hospital and over longer follow-up
  without death-registry linkage. Verify the current source and limitation; do not
  assume the proposed automatic annotation mechanism is installed. Record the caveat
  with `record_limitation()` where the date is read, or carry it into the task output.
  HBCIS `DeathDate` (`mart_patient_view`, `mart_episodedetail_view`) and the episode's
  separation mode (discharge status) are an alternative source to offer; verify them
  in the pinned `schema_extracts/` and record which source was used.
  Turning that date into **30-day mortality**, including the anchor and window boundaries, is the researcher's
  modelling choice, expressed in the request's own spec composition.
- **Suburb/postcode:** latest address and address at the time of an encounter answer
  different questions. Leave that choice and its temporal anchor to the researcher/spec;
  verify whether the source supports it rather than silently substituting latest data.
- **Cohort sequence or transition date:** a "first X, then later Y" definition, and
  which event states count on each side, is a modelling choice. Supply the dated
  events and their states; the researcher sets the ordering and state rules.
- **Ethnicity:** RDL sources hold no ethnicity field. By RDL convention an "ethnicity"
  request gets Indigenous status from ieMR `PERSON_INFO`, with country of birth and
  preferred language as optional surrogates, and a limitation that ethnicity is not held.

Read [references/modelling.rst](references/modelling.rst) for a worked sequence example
and the ethnicity sources.

When request logic crosses this boundary, flag the modelling decision and its effect.
Use an already-confirmed scope choice where available; otherwise ask the researcher
to settle the affected choice and continue work that does not depend on it. Do not
treat source limitations as permission to choose a model or promise unavailable facts.

## Review hand SQL

Check hand SQL, and any hand-edited generated SQL, against the defect checklist in
[references/checklist.rst](references/checklist.rst). Each of its seven patterns has a
symptom and a fix. Report each finding with its SQL location.

## Release conventions

At map and draft time, read [references/delivery.rst](references/delivery.rst) for workbook limits, per-output row estimates, text length bands and engineer delivery choices flagged for the analyst; near-limit estimates remain undecided.
Build all requested elements, including identifiers and free text, even when approval is unchecked;
the analyst checks coverage during review. Known restrictions still apply. For build/commit/push permission,
raw/derived dates, validation listings, study IDs and suppression, read [references/release.rst](references/release.rst).
Keep validation listings and the study-ID link table out of the delivery run. Use the
`-- @extract: <name> internal` marker only after confirming that the child's pinned
`scripts/run_extract.py` supports it: released scaffold runners (v0.5.0 and earlier)
deliver a batch so marked. Delivered aggregates follow the assessment/approval.
For probe and handover/open prose, read [Probe disclosure control](references/release.rst).
Clinician and resource names are not personal information (governance ruling,
2026-09-28); patient identifiers are. See "Personal information" in `release.rst`.

## Carry evidence into the task

Report each rule's SQL/evidence location and result: supported, concern or unverified; static review is not runtime evidence.
Keep business decisions apart from storage facts; never claim human confirmation from an autonomous run. Future domain rules need a concrete incident and an authoritative source.
