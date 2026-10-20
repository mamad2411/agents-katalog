---
name: analyze-source
description: Use when analyzing a data source (REST, GraphQL, SDK, or CLI) for the AppSec connector framework — for example SAST tools (SonarQube, Semgrep), SCA tools (Dependency-Track), secret scanners (TruffleHog), DAST scanners (OWASP ZAP), WAF (AWS WAF), SCM platforms (GitHub, GitLab), or CMDB systems (ServiceNow). Use when a per-connector documentation page is needed.
---

# analyze-source

## Overview

This skill produces a six-section per-connector documentation page from a source's official API documentation. The page lives at `mkdocs/docs/connectors/<category>/<source-slug>.md` and feeds the downstream `provision-source`, `generate-connector`, and `validate-implementation` skills. The Reference section captures the seven API facts the framework needs to mechanically derive a connector module; the Implementation log section opens the lifecycle audit trail that the next three skills extend.

This skill is the analysis stage. It does not write any Python, YAML, or test code; it only writes Markdown. Category-specific facts (applicable REQ-IDs, default severity, HWM preference, dedup key shape, target Silver tables, auth norms, ingestion-tooling preference, quirks) live in `references/<category>.md` and MUST be read for the source's category before drafting Reference.

## Inputs

- **Source name** and homepage URL.
- **Official API documentation URL** (fetched via WebFetch).
- **AppSec category** — one of `cmdb`, `scm`, `sast`, `sca`, `secrets`, `dast`, `waf`. Determines which `references/<category>.md` to load and the output directory.
- **Optional**: live API credentials for fixture generation. Skip if unavailable.

## Output

A single Markdown page emitted at `mkdocs/docs/connectors/<category>/<source-slug>.md` where `<category>` matches the input and `<source-slug>` is a kebab-case slug of the source name. The page has six top-level sections:

1. **Overview** — what this connector does, its role in the platform, and which Silver table(s) it populates. For sources outside MVP scope, include the `!!! info "Not in MVP scope"` admonition.
2. **Prerequisites** — how to set up the external service and extract credentials (API keys, OAuth apps, PATs).
3. **Reference** — the seven API facts (see the bullet list under Procedure).
4. **Setup** — configuration, bundle deployment, first-run commands. Stub with `!!! info "Not implemented in MVP"` if out-of-scope.
5. **Validation** — always stubbed on first emit with `!!! info "Pending validation"`; `validate-implementation` populates this later.
6. **Implementation log** — a Markdown table with four rows. Row 1 is filled by this skill (see Implementation log row template below). Rows 2, 3, and 4 are placeholders marked `(pending)` for `provision-source`, `generate-connector`, and `validate-implementation` to fill in.

## Lakeflow Connect managed-source catalogue

Last refreshed: 2026-04-01 from https://docs.databricks.com/aws/en/ingestion/lakeflow-connect/

| Source name | AppSec category in scope | LFC API surface |
|---|---|---|
| ServiceNow | cmdb | Table API v2 |
| Salesforce | (n/a — not in MVP categories today) | REST API |
| SQL Server | (n/a) | Change-tracking |
| Google Analytics | (n/a) | Reporting API |

Refresh obligation: re-fetch https://docs.databricks.com/aws/en/ingestion/lakeflow-connect/ (a) before any `analyze-source` run that targets a source not previously in the catalogue, and (b) at minimum once per skill release branch. The trigger is event-bound rather than calendar-bound — staleness shows up as a missed LFC opportunity for a new source, not a silent drift over time.

The table drives `databricks_runtime.ingestion_path` resolution per the procedure step below.

### Resolution precedence

When the source name matches a row above AND the category is in scope, set `ingestion_path: lakeflow_connect`. Otherwise, apply the four-step precedence:

1. **LFC managed-source catalogue match** → `lakeflow_connect` (above).
2. **Category-canonical CLI/artefact pin** → `artifact_path` when the category reference flags the source's path as CLI-based or artefact-driven (per the SAST/secrets/DAST CLI exception documented in `references/<category>.md`).
3. **Maintained Python SDK catalogue match** → `sdk` plus `python_sdk_module={module}` (see "## Maintained Python SDK catalogue" below).
4. **Otherwise** → `dlt`.

`AskUserQuestion` is reserved for future categories where the choice is genuinely ambiguous; today no category triggers it.

## Maintained Python SDK catalogue

Last refreshed: 2026-04-26 from per-source vendor / community SDK landing pages.

| Source | SDK | Decision | Rationale |
|---|---|---|---|
| GitHub | PyGitHub | sdk | Community but de facto standard; `PaginatedList` + `GithubRetry` meet framework concerns. |
| GitLab | python-gitlab | sdk | Community; effectively the standard, GitLab links to it from its own DevSecOps blog. |
| AWS WAF | boto3 (`wafv2`) | sdk | First-party, official. |
| OWASP ZAP | zaproxy | artifact_path (primary) | Framework's primary DAST pattern is CI/CD step + JSON-report consumption. |
| Dependency-Track | owasp-dependency-track-client | dlt | "Inofficial" per its own README; framework prefers a thin dlt rest-source. |
| SonarQube | python-sonarqube-api | dlt | No actively-maintained generic SDK (Snyk flags Inactive). |
| Semgrep AppSec Platform | none | dlt | No first-party Python client; only relevant for SaaS tier (CI mode is artifact_path). |
| TruffleHog | none | artifact_path | Go CLI scanner; not an "API source". |
| ServiceNow | n/a | lakeflow_connect | (Resolved upstream by LFC catalogue.) |

Refresh discipline: reviewers update this table when adding a new source whose category does not pin `artifact_path` or `lakeflow_connect`. Maintained SDK criteria: (a) actively-maintained PyPI package (SemVer, recent release, no Snyk inactive flag); (b) covers every framework-consumed endpoint; (c) handles pagination / rate-limit / auth via library APIs. The trigger is event-bound rather than calendar-bound — staleness shows up as a missed SDK opportunity for a new source.

### PySpark Data Source caveat (future work)

The `sdk` branch runs as a single-task notebook job — one driver, one worker process, one library client. SDKs with connection pools, authenticated sessions, or thread-local state behave correctly under that model. If the framework later adopts the Lakeflow Community Connector (Spark Python Data Source) pattern, SDK choice becomes more delicate — caching / session state misbehaves under serialization across executors. PyGitHub in particular caches aggressively, which is a feature in a script and a footgun in a distributed worker. Caveat does not apply to the current `sdk` branch.

## Procedure

1. Read `references/<category>.md` for category-specific facts that influence the Reference section's seven API facts — applicable REQ-IDs, default severity, HWM preference, dedup key shape, target Silver tables, auth norms, ingestion-tooling preference, quirks.

   ALSO read the "## Lakeflow Connect managed-source catalogue" AND "## Maintained Python SDK catalogue" subsections above. The two catalogues plus the category reference together drive `ingestion_path` resolution (and conditionally `python_sdk_module`) in the new step 9 below.
2. Fetch the source's API documentation via WebFetch from the input URL. Cache the fetched content for citations.
3. Identify the authentication mechanism the source supports; cross-check against the category's auth norm in `references/<category>.md`. If the source supports multiple auth modes, select the one matching the category convention.
4. Enumerate the endpoints required to populate the Silver tables assigned to the source's category. Cross-reference the Silver Table Ownership table at `mkdocs/docs/platform/reference/catalog.md` and the canonical schemas at `mkdocs/docs/platform/reference/canonical-mapping.md`.
5. Select the incremental strategy per the preference order in `references/<category>.md` (typical order: webhook > native HWM column > full reload; some categories override).
6. Extract a consumed-field schema excerpt — only fields the connector actually reads — matching the canonical Silver fields from `mkdocs/docs/platform/reference/canonical-mapping.md` (entities or findings schema, whichever applies to the category).
7. Produce severity and status lookup proposals per the canonical enumeration models at `mkdocs/docs/platform/reference/canonical-mapping.md`. For categories where severity or status do not apply (CMDB, secrets-status), record the N/A explicitly.
8. Document quirks: deviations from category norms, format surprises, per-source handling policies. Cross-check `references/<category>.md` for category quirks the source may inherit.
9. **Resolve `databricks_runtime.ingestion_path` (and conditionally `python_sdk_module`) and write to `operational.yml`.** Apply the four-step precedence:

   (a) **LFC catalogue match** → `ingestion_path: lakeflow_connect`.
   (b) **Category-canonical CLI/artefact pin** (per the SAST/secrets/DAST CLI exception in `references/<category>.md`) → `ingestion_path: artifact_path`.
   (c) **Maintained Python SDK catalogue match** → `ingestion_path: sdk` PLUS `python_sdk_module: <module>` (e.g. `PyGitHub`, `python-gitlab`, `boto3`).
   (d) **Otherwise** → `ingestion_path: dlt`.

   `AskUserQuestion` only when the category reference flags the choice as ambiguous (today no category does). Write the chosen value(s) to `src/connectors/{source}/operational.yml` under `databricks_runtime.ingestion_path` (and `databricks_runtime.python_sdk_module` when step (c) applies). If `operational.yml` does not yet exist, stage the value as a Reference-section note for `generate-connector` to consume.

   When the chosen value is `lakeflow_connect`, append one sentence to the Reference section's API surface fact: "Lakeflow Connect supports {source} as a managed connector via {api_surface} (per the analyze-source LFC managed-source catalogue, refreshed {date}); this connector chooses the `lakeflow_connect` ingestion path."

   When the chosen value is `sdk`, append one sentence to the Reference section's API surface fact: "The {source} ingestion uses {python_sdk_module} as the Python client (per the analyze-source Maintained Python SDK catalogue, refreshed {date}); the connector contract delegates auth, pagination, and rate-limit handling to the library."
10. Assemble the six-section Markdown page and emit to the output path.
11. Stub the Implementation log section with the row for this skill (date, inputs, outputs, skill repo ref via `git rev-parse --short HEAD`); leave rows for `provision-source`, `generate-connector`, and `validate-implementation` marked `(pending)`.

The seven API facts captured under Reference are:

- **API surface** — REST / GraphQL / SDK / CLI; endpoints consumed; authentication mechanisms.
- **Pagination and rate limits** — strategy and quotas.
- **Incremental hook** — webhook, native HWM column, scan-id, or full reload (per `references/<category>.md`).
- **Resource schema excerpt** — Markdown table with columns Field / Type / Meaning, scoped to fields the connector reads.
- **Enumerations** — severity and status mappings against the canonical models.
- **Quirks** — deviations from category norms; format surprises.

Authentication is folded into the API surface fact; that is six visible facts but the framework documentation calls it seven. Preserve the seven-fact wording when writing Reference, matching the existing baselines.

## Invariants

- Every official documentation URL used MUST be cited inline or in a References list at the bottom of the page. No fabricated facts: every claim about the source's API MUST be traceable to fetched documentation or to `references/<category>.md`.
- The severity and status lookups MUST cover every documented source value; undocumented values default to the configured fallback with a data-quality warning noted inline.
- The page slug and category directory MUST match the AppSec category input exactly; do not invent a new category.
- The Implementation log table MUST have row 1 populated; rows 2, 3, and 4 MUST exist with the `(pending)` marker so downstream skills have a target to overwrite.
- Output is Markdown only. Do not write Python, YAML, or test files in this skill.

Category-specific invariants (applicable REQ-IDs, default severity convention, HWM preference, dedup key shape, target Silver tables, auth norms, ingestion-tooling preference, category quirks) live in `references/<category>.md`. Read the file matching the input category before drafting Reference.

## Implementation log row template

Append exactly one row to the Implementation log table for this skill's invocation. Use this row shape verbatim, replacing the bracketed placeholders with the four data cells:

```
| Source analysis | analyze-source ({category}) | name={source}; url={doc_url}; category={category}; ingestion_path={value}{; python_sdk_module={python_sdk_module} when ingestion_path == sdk} | mkdocs/docs/connectors/{category}/{slug}.md §1–§3 | {YYYY-MM-DD} | {git_short_sha} ({branch}) |
```

- `{category}` — the AppSec category input (`cmdb`, `scm`, `sast`, `sca`, `secrets`, `dast`, or `waf`).
- `{value}` — the resolved `databricks_runtime.ingestion_path` (`lakeflow_connect`, `sdk`, `dlt`, or `artifact_path`).
- `{python_sdk_module}` — the resolved `databricks_runtime.python_sdk_module` (e.g. `PyGitHub`, `python-gitlab`, `boto3`). Included in the inputs cell only when `ingestion_path == sdk`; omitted otherwise.
- `{source}` — the source name input.
- `{doc_url}` — the official API documentation URL input.
- `{slug}` — the kebab-case slug used in the output filename.
- `{YYYY-MM-DD}` — the run date in ISO format.
- `{git_short_sha}` — output of `git rev-parse --short HEAD` on the skill's repo.
- `{branch}` — output of `git rev-parse --abbrev-ref HEAD`.

Rows 2, 3, and 4 of the Implementation log table must be present and marked `(pending)` so that `provision-source`, `generate-connector`, and `validate-implementation` can overwrite them on their respective runs. On re-emit, row 1 is overwritten in place rather than appended; the table never exceeds 4 rows. The first-emit history of any overwritten row lives in git rather than in the table itself. The standard placeholder rows are:

```
| Source provisioning | provision-source ({category}) | (pending) | (pending) | (pending) | (pending) |
| Module generation | generate-connector ({category}) | (pending) | (pending) | (pending) | (pending) |
| Validation | validate-implementation ({category}) | (pending) | (pending) | (pending) | (pending) |
```
