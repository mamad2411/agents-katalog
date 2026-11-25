---
name: nxd-generate-data-product
description: CONSTRUCTION SPECIALIST, not an entry point. Generates the COMPLETE runnable Python-only data-product closure for lean-desktop Nextdata OS from an ALREADY-SETTLED plan (intent, inferred model, connector config): spec.py + models.py + infra-profile.yaml + transform/main.py + requirements + the connector wiring (local file, live database, or REST API), ready to boot into a queryable DuckDB result. Supervisor compiles spec.py into the kernel definition YAML, so never hand-write deployment-spec / manifest / models YAML. Use when the plan is settled and the closure needs constructing. End-to-end requests to build a data product from a source start in nxd-run-job-loop, which gathers intent, source, questions and any supplied procedure and runs the policy read-back FIRST; arriving here directly means that handoff is absent, so return there first. Pairs with nxd-build-semantic-data-product, which INFERS the model this skill PLACES. Not for k8s — use nxd-build-data-product.
allowed-tools:
  - Bash
  - Read
  - Write
  - Edit
  - MultiEdit
  - Glob
  - Grep
  - AskUserQuestion
  - Agent
  - Task
metadata:
  author: nextdata
  version: 0.76.0
---

# nxd-generate-data-product skill

## Overview

This skill assembles the **complete Python-only definition closure** for a local
(desktop) data product from: the **approved `dp-blueprint.md`** — the user-editable IR
carrying intent, questions, the model plan and every ruling, which this skill
*compiles*, never re-derives; the **inferred semantic model** — the per-column
roles produced by **nxd-build-semantic-data-product**'s inference mode, which this
skill *places*, never redesigns; and the **connector config(s)** naming where
each source lives and its **connector type** (never invent connection details or credentials).

**If the intent carries a procedure** — a rubric, gates, thresholds, a verdict
vocabulary — the Workflow's **policy read-back gate** runs before any file is
written. A closure whose scoring policy the user never saw is the one failure
this skill treats as unrecoverable.

Compile faithfully: keep every Model and Output name exactly as approved and cover every clause of every Questions entry; never rename or drop either. If a clause cannot be implemented, return to `nxd-run-job-loop` for an explicit scope decision. Add no Decision from source rows, contracts, or evidence absent from the approved blueprint.

**Connector types** — see the [source types index](reference/source-types.md) for the canonical source matrix and source-specific recipes. Names are for exactly one instance of a type; for 2+, label each per `reference/multi-source.md`.

For `api-source`, the only absent companion is the endpoint map from public `endpoint_<model>` profile attributes; additionally require the closure-local `connectivity_check.py` probe. For a legacy literal credential profile, make it pass before dependent authoring when source access is available. When source access is available, until the probe has inspected every configured endpoint successfully, do not write `infra-profile.yaml`, `.gitignore`, `SENSITIVE`, `spec.py`, `models.py`, `transform/`, `requirements.txt`, or `README.md` on that legacy path. Missing credentials permit structural authoring from the settled plan only: mark payload inspection and connectivity **not run** and **unverified**, leave the closure incomplete, and never claim source validation or invent an intake workaround. With a Desktop-local `attributesSecretRef`, defer credentialed connectivity and payload inspection to the admitted source fetch; the closure-local probe must not read the reference or request a key directly. Mark static binding as deferred and a merely stored connection as unverified. When the source refuses valid credentials (401/403 with no auth challenge) or the API is unfamiliar before the first build, read its own documentation (root and any advertised path such as `/docs`) with the session's fetch tool, without credentials, and set required client headers through `header_*` attributes, per [custom request headers](reference/api-source.md#custom-request-headers). Specialized API profiles keep the `api-source` service name and nonsecret `source_kind`; verify pagination, authorization, row shape, and fetch evidence through the admitted path. The **desktop supervisor** compiles `spec.py` into kernel definition YAML, pins and boots the output directory, runs the transform, verifies staging, and stands up the semantic MCP endpoint. Return facts and a structured handoff to `nxd-run-job-loop`; the owning loop translates status, failures, costs, and publication state into plain chat without copying raw internal output; see [user-facing language](../nxd-run-job-loop/reference/user-facing-language.md).
## The closure layout

Choose and normalize one absolute `<dp-root>` — the exact directory submitted through the supervisor's returned `capture` action — **BEFORE authoring any artifact**. Move or recreate existing closure files into it before creating/checking another. Every closure artifact must be inside `<dp-root>`: root-level artifacts are direct children, nested artifacts are descendants. This includes `spec.py`, `models.py`, `transform/`, `requirements.txt`, `infra-profile.yaml`, and connector artifacts. A declared custom contract additionally requires exactly one verifier under `contracts/expectations/` or `contracts/promises/` plus its matching `spec.py` wiring. For a Desktop-local referenced `api-source`, author the public topology service after plan consent, connect through the native prompt, and let admitted validation fetch the source. A standalone `connectivity_check.py` may remain as a diagnostic artifact, but must defer credentialed execution for a local ref. Record payload inspection and connectivity as **not run** and **unverified** until the admitted fetch succeeds. For legacy literal credentials, follow the existing probe sequence in [reference/api-source.md](reference/api-source.md#payload-inspection-gate--before-authoring).
If a self-check demands `.gitignore` or `SENSITIVE`, add them and say so in the build notes; never ask the user. Never place credentials, `SENSITIVE`, `.gitignore`, or executable closure artifacts beside/above `<dp-root>`; split executable artifacts must be consolidated first. The sole profile exception is a dedicated source-preparation sibling, never a parent or ancestor, containing only public topology and an opaque local reference before plan consent. After plan approval, copy only that public profile into the canonical closure, preserve its exact bound service identity, and inspect compatibility at the final root before reuse. This sibling is not an executable closure and must not be submitted for capture. Use this same root for capture; supervisor capture owns reserved metadata and trusted checks.

The author emits **executable closure inputs only**. Supervisor capture
materializes and verifies the reserved snapshots, lock, build record, and
trusted checker:

```
…/nxd-jobs/<workflow>/
├── dp-blueprint.md              # the approved IR — INPUT, outside the closure. Never emitted here.
├── source-preparation/          # optional public topology + opaque reference only; no executable inputs
└── closure/                     # <dp-root>: what the v2 capture action receives
    ├── spec.py                  # generated closure wiring: models + transform + output port
    ├── models.py                # semantic models + placed semantic roles
    ├── infra-profile.yaml       # the desktop-local profile: duckdb + python-compute + csv-source
    ├── transform/
    │   └── main.py              # the dlt-through-port ingest (standalone entrypoint)
    ├── requirements.txt         # proven pins (below)
    ├── dp-blueprint.approved.md # supervisor capture: byte copy of approved IR
    ├── dp-blueprint.lock.json   # supervisor capture: canonical hash + compiler version
    ├── build-record.json        # supervisor capture: stages, attempts, concessions, blockers
    ├── README.md                # author output: reopen recipe + credentials block ONLY; declared contracts/ verifiers are exact, not placeholders
    ├── csv-source-path          # one line: relative path to the CSV export root
    └── data/                    # the connector export: data/<base_model>/*.csv
        └── <base_model>/…       # base models only — derived models have no data dir
```
_(CSV layout, the proven default; other types swap the companion artifact per the [source types index](reference/source-types.md). For 2+ labeled CSV sources, `reference/multi-source.md` also requires a root-level `companion-files` manifest for each non-empty labeled export root and a desktop supervisor with directory-companion support. `data/` is the CSV/file input layout, not a universal closure requirement. A `db-source`/`api-source` closure has no connector-owned file export; `data/` may be absent or may contain separately approved reference data that the transform explicitly reads through its own `@dlt.resource`. It is never an implicit database or API input. See `reference/database-source.md` and `reference/api-source.md`.)_

**The author NEVER writes `deployment-spec.yaml`, `manifest.yaml`, or
`models.yaml`.** The supervisor compiles those three from `spec.py` +
`models.py` when it pins the DP — including the `model_tables` identity map, the
staging-path placeholder, and the compiled semantic roles the semantic child
reads. It owns their shape and will overwrite them; your source of truth is the
Python.

---

## THE NAMING INVARIANT (the correctness spine — protect it everywhere)

One lowercase, unquoted, snake_case name per model, agreed on by the **authored
surfaces** below (the supervisor derives the compiled-YAML `models.yaml` name
and the `model_tables` identity map from these — you do not author them):

| Surface | Where the name appears | Base | Derived |
|---|---|---|---|
| `models.py` | `semantic_model("<name>")` | yes | yes |
| `spec.py` | `.promise(<name>)` for required models; `.model(<name>)` for optional-empty physical models | yes | yes |
| `transform/main.py` | listed in `PHYSICAL_MODELS` | yes | yes |
| the physical table | what dlt writes: `main.<name>` | yes | yes |
| the connector's per-model reference | `data/<name>/` for a file connector (CSV/JSON/JSONL/Parquet); a `db-source-tables` entry for a database connector; an `endpoint_<name>` infra-profile attribute for a REST API connector | yes — **except** reference data the closure lands itself on a `db-source`/`api-source` connector, which has no connector-owned export: do NOT invent one (`reference/api-source.md` § "Landed reference data in an API closure"); the API closure still requires its separate `connectivity_check.py` probe | **no** |

`PHYSICAL_MODELS` is the set of **landed-table identities**, not data directories: base models (`data/<name>/`) **plus** derived models (Step 3a).
Required physical models use `.promise(...)`; optional-empty physical models use
`.model(...)`; both appear in `model_tables`. `OPTIONAL_EMPTY_MODELS` is a
literal subset whose dlt resource may yield zero rows and leave no table. An optional source or output that must remain a valid header-only CSV is still an optional physical base model: keep it in `Models`, register it with `.model(...)`, and include it in both `PHYSICAL_MODELS` and `OPTIONAL_EMPTY_MODELS`. Never change it to `.promise(...)` or omit the model to work around an absent zero-row table.
Semantic views use `.model(...)` only and never enter `PHYSICAL_MODELS`; assert
dlt output against declared physical models, not the whole `model_tables` map.
Base attribute names are byte-exact post-dlt headers; derived ones are resource
keys.

## Workflow

When the connected desktop supervisor advertises v2 execution, the owning job-loop must use its capability-gated construction sequence in the nxd-run-job-loop skill's `reference/workflow-v2.md`: call `get_workflow_capabilities` and `prepare_workflow`, relay `session_decision` exactly, capture and review retained paths, report through `report_requirement`, and follow `next_actions` through admitted `start_run`. This skill never supplies a legacy construction fallback.
Use [current Desktop generation](reference/desktop-generation.md) to select the source, mapper and approved-inventory references once; the existing compiler consumes authored Python, not a turnkey scaffold.
**Workflow-v2 contract inventory is a hard generation invariant.** Every typed-v3
Input expectation and Output promise (and every proposal contract derived from
them) produces exactly one verifier script under `contracts/` and exactly one
matching `custom(...)` wiring at its declared attachment and phase. Carry its
name, attachment, model, phase, guarantee, rule, and fields through unchanged;
ordinary `.promise(model)` does not satisfy a custom contract. Add no extra
custom contract, placeholder, or decorative unwired script: supervisor capture
and preflight reject both missing and extra inventory. For an API source, a
custom input expectation is unsupported on the CSV-first runtime; stop the current
inventory rather than emitting an unwired decorative contract or omitting it.
A phase/guarantee change requires an explicit recorded scope decision and fresh
prepare/consent; never offer a live API-to-CSV workaround. Wire each output promise when its runtime is supported;
do not invent contracts from inferred schema facts.
The nxd-run-job-loop handoff MUST carry `job_helper_dir`, an already-resolved absolute installed-skill directory. Set `JOB_HELPER_DIR` to that exact value; if it is absent, return to nxd-run-job-loop — never reconstruct it from the closure or this skill's cwd.
**Selective-install dependency:** this skill needs **nxd-run-job-loop** at runtime for the approved-spec validator, lock writer, and build-record helpers. A selective install must include both skills; installing `nxd-generate-data-product` alone is not a supported substitute for that handoff. For any `api-source`, follow the single authoring gate in [reference/api-source.md](reference/api-source.md#payload-inspection-gate--before-authoring): the closure-local stdlib probe is retained. On the legacy literal route it is authored first and, when credentials are available, runs before the remaining closure artifacts. On the Desktop-local reference route it defers credentialed execution; the admitted source fetch provides validation evidence. Missing credentials permit structural authoring from the settled plan only; payload inspection and connectivity are then **not run** and **unverified**, so source validation and the complete happy path must not be claimed.
### Step 1 — Collect the inputs

- **The approved `dp-blueprint.md`** is the primary input when one exists — the
  user-editable IR **nxd-run-job-loop** authors at its Step 1b, beside the closure
  at `…/nxd-jobs/<workflow>/dp-blueprint.md`. **Compile it; do not re-derive it**:
  its `Models` and `Transform` sections are the plan, its explicit `Outputs`
  are the only user-visible products, and `Decisions` becomes `data/nxd_decisions/nxd_decisions.csv` through the one-to-one mechanical projection in [reference/pre-capture-audit.md](reference/pre-capture-audit.md): typed `locked` becomes ledger `confirmed`, typed `proposed` remains `proposed`, and `provenance` comes from authorship rather than lifecycle.
  Procedures resolve from Transform steps or
  reference Models, never from the Decisions ledger. The v3-capable
  `"$JOB_HELPER_DIR/scripts/validate_dp_spec.py"` remains supported; skip repeat standalone validation only for the exact unchanged already prepared and consented blueprint/proposal. A changed plan or plan-invalidating error needs current validation, fresh prepare and fresh consent. Treat any closure value appearing in no spec section as one
  the user never approved. Schema and compile map: **nxd-run-job-loop**'s
  `reference/dp-blueprint.md`. **Never write it into the closure**: it is upstream,
  and a closure file pointing at `../dp-blueprint.md` is the escaping reference Phase
  C fails; supervisor capture copies the approved revision and creates its lock
  as described in Step 6a; the author does not create either surface.
- The intent (the spec's `name` / `intent` / `questions`) gives the DP `name`,
  description, and which questions the semantic layer must answer.
- The inferred model gives each base model's primary key, dimensions, joins,
  PII flags, metrics, and column types. Base roles and metric views are
  different authored objects — see Step 2. `pii=True` and a roleless field control semantic discovery; they do not mask a column in the physical DuckDB table or direct SQL. For a file source, omit personal-data columns the approved blueprint does not need through the declared projection before landing. If an approved derived key needs a personal-data value, derive the non-identifying key in memory before landing and omit the raw value. No supported physical output may retain a dropped value. When an approved Decision suppresses or withholds values below a grain (for example department-months under five people), never land rows below that grain (such as a person-level roster): read the projected export inside the transform, compute in memory, and land only models that apply the rule, so nothing landed can recount a suppressed value. Place that projected export outside `data/` (for example `source/<name>/`), declare the root in the root-level `companion-files` manifest, and read it below `os.environ["NXD_TRANSFORM_ROOT"]`, failing closed; a `data/` directory without a base model fails `struct.base_models_vs_data_dirs`. Say so in the blueprint. Every non-empty model, field, metric, and contract description must be copied from the relevant approved blueprint section; do not invent a paraphrase that is unreachable from the approved plan. If new wording is needed, amend and re-approve the blueprint before capture.
- Each connector config names a **connector type** (CSV / other local file /
  database / REST API) plus its location. For non-CSV types follow
  `reference/file-source.md` / `database-source.md` / `api-source.md`; for
  database/API confirm real connection details — never invent them (the spec
  names credential KEYS only; the values reach you separately).
- **Read the export's shape; land it unchanged by default.** After the policy
  gate below, file exports use model subdirectories or flat `*.csv` files named
  from their snake_cased filenames, landed as exact byte copies. The only
  exception is a declared projection of unneeded personal-data columns, with
  its allow-list, drop reasons and digest evidence. See
  [reference/file-source.md](reference/file-source.md) and
  [the source-materialization guide](../nxd-run-job-loop/reference/source-materialization.md).
  Never merge files, rename or add headers, or reshape rows; read headers either way.
- Every data directory MUST have a base model (a below-grain source under an approved suppression rule lives outside `data/`, above); a promised model with **no** data
  directory is a **derived** model (Step 3a), not a missing export. An
  optional-empty base model listed in `OPTIONAL_EMPTY_MODELS` may have no source
  directory until its first rows are supplied.

### Gate — confirm the policy with the user before writing anything

**Fires when** the request supplies a procedure (rubric, gates, weights,
thresholds, scales, a verdict vocabulary, a selection rule) with a gap changing
a score, verdict, gate outcome, or which rows land: a scale defining only some
levels (5 and 1 given, 2/3/4 absent); named verdicts with no score→verdict
mapping or precedence; a qualitative modifier that must become a rule ("unless
exceptional"); a gate whose UNKNOWN/missing/inferred value could change the
outcome; evidence with no provenance or missing-evidence rule.

**Then, until the user replies, do NOT**: create the closure directory, copy
source data into it, write any closure file, generate transform code, create
tables, score rows, or invoke a build. Reading the source and its headers is
allowed, as is writing `dp-blueprint.md` itself — it lives OUTSIDE the closure, so it
is not part of the build. Asking technical delivery questions is allowed and
**does not satisfy this gate**; a delivery answer is not policy approval, and
your own recommended defaults are not a reason to proceed.

**Where the answer goes is fixed too**: a resolved threshold, band or scale level is a landed model declared in the plan's `Models` (see **nxd-run-job-loop**'s `reference/dp-blueprint.md` § "Procedures are landed, not described"), never a literal this skill supplies later. **The read-back artifact is `dp-blueprint.md`**, validated with
`"$JOB_HELPER_DIR/scripts/validate_dp_spec.py"`, which finds those gap classes deterministically.
It must ENUMERATE every gate with its UNKNOWN handling, every criterion weight,
**every anchor you propose for an incomplete scale**, the score aggregation, the
**proposed verdict bands and precedence**, and the provenance and
missing-evidence behaviour — never a summary of a procedure the user must check.
Show it, name every value you authored, and wait. A validator pass is not
approval, and `status: approved` is the user's to set.

**"Use your judgement" is not approval** — it licenses authoring the proposal,
then showing it and waiting again. A fully specified procedure still gets one
short confirming turn; no procedure at all means this gate does not fire.

**Invoked directly**, without an nxd-run-job-loop handoff, **return to
nxd-run-job-loop immediately**. Do not run the read-back, materialize a closure, or serve; nxd-run-job-loop owns the user-facing read-back and approval.
**Invoked as a generation subagent**, the user turn is the
orchestrator's and you never open one, and the gate is **not a rubber stamp**:
re-run the "fires when" criteria and **bounce** (`gap_found: <what and why>`,
writing nothing) on an element absent from the enumeration, or one a profiling
finding makes ambiguous or conditional. You hold no credential — placeholder
the `attributes`, return `credential_slots` (key names only), dry-run **not run**.

The complete gate — every clause, the subagent return contract, and the
credential boundary — is [reference/policy-gate.md](reference/policy-gate.md).

### Step 1a — Plan the derivation before authoring anything

The semantic layer used here cannot express derivation — no dimension
expressions, no default filters, no row generation/removal, and no
`Agg.EXPRESSION` shortcut for business rulings. **Every business ruling
therefore has to be materialized as a physical column or row by the transform**,
before the semantic layer sees it. So plan the models by backward-chaining from
the user's QUESTIONS, not forward from the source headers — **an approved
`dp-blueprint.md`'s `Models` and `Transform` sections ARE this plan**, already backward-chained and
approved: validate it, don't redo it.
[reference/derivation-plan.md](reference/derivation-plan.md) has the worked
method, base-vs-derived test, `Agg.EXPRESSION` boundary, and mandatory
reference-data handling, including per-entity **agent** judgements —
[reference/llm-judgments.md](reference/llm-judgments.md).

### Gate — validate primary keys before authoring

Every physical model, required or optional, base **and** derived, needs one or more `primary_key()` fields. Missing it fails as `struct.no_primary_key`; settle it before capture, because fixing it after capture forces a reset and a new review round. A `dp-blueprint.md` states each model's `grain` and `key` —
**validate those against the source rather than inventing your own**; a spec key
that does not hold is a `gap_found`, not something to quietly replace. The rule
differs by kind:

**Base models — use an existing source column; never synthesize.** Validate
existing columns whose non-null value tuple is unique **across the complete
supplied export** (all files together). Prefer one source column; use a
composite only when it is the defensible entity key. Never use row numbers,
measures, or altered source data. If the evidence is absent, stop and ask for
the source entity/event key; a unique sample is not proof for a future export.
(This replace-only flow excludes append/upsert semantics.)

**Derived models — declare the key the derivation's grain implies.** A derived
model can exist at a grain no source column names (an amortization schedule at
invoice × month), so demanding a pre-existing source key would be wrong. Its key
is **defined by the grain**, **constructed deterministically** from source values
and the grain's ordinal only (a stable `f"{invoice_id}-{period:02d}"`, never a
UUID, a timestamp hash, or an order depending on file arrival), and **asserted
unique in-transform** (Step 3b) rather than assumed. A row-preserving enrichment
or a row-removing dedupe keeps its **source** key — those rows are still the
source entities. Only a regrain declares a new composite.

### Step 2 — `models.py`: place the inferred roles with the public DSL

Author `models.py` with the **real public semantic DSL**
(`from nxd.spec import semantic_model, field, primary_key, dimension, join`;
types from `nxd.spec.data_types`). Place the table roles, then one semantic view
per set of metrics over that table:

- `semantic_model("<name>")` — the bare lowercase physical table name.
- `.schema({...})` maps each column to `field(<type>(), <role>())`. A column with no role
  produces no metric, dimension or join and is absent from `describe_models` — unqueryable.
- **Declare only physical output models in `models.py`.** Every `semantic_model(...)` must be a required `.promise(...)` or optional `.model(...)` in `spec.py` and
  `PHYSICAL_MODELS`; never add a source-only/staging-only model just to document
  rows the transform reads but does not land — keep those rows as transform data, or
  land and promise the model explicitly.
- **Base models carry ONLY `primary_key()`, `dimension(...)`, or `join(...)`** — a metric there RAISES.
  Roles COMPOSE, and a bare `primary_key()` is **not groupable**: pair every key with a `dimension(...)`.
- A metric belongs on `semantic_view("<base>_metrics", <base>)` with
  `metric_field(<type>(), metric(Agg.<AGG>, of=<base>.field("<column>"), ...))` —
  query-time, not a physical table.
- **A row-level ratio is not an aggregate metric.** Never expose a row-level ratio (such as per-campaign CPA) through `metric(Agg.AVG, ...)` or any other reduction. For aggregate queries, expose additive numerator and denominator metrics separately and calculate the ratio from those query results. The allowed row-grain alternative is a derived ratio column validated with `assert_row_ratios`; expose it only at that row grain, without a reducing metric over the ratio column.
- **A distinct count landed per bucket is not additive.** Never `Agg.SUM` a per-bucket distinct count (accounts active per week) across buckets: it counts one entity once per bucket. Land the bucket column on the event-level model and define `Agg.COUNT_DISTINCT` over the entity key in a `semantic_view` over that model, or declare `non_additive_over` on every bucket dimension where the installed `metric()` accepts it.
- **Aggregate-only outputs still need a governed count.** Add
  `metric_field(number(), metric(Agg.COUNT, column="*", name="<model>_row_count", ...))`
  (or count a non-null key) in a semantic view. Metric names are global across
  the registry: a bare `row_count` on two views fails spec compilation and register it with
  `data_product_output().model(view)`. This supports `describe_models` and
  grouped aggregate queries without record-level rows or placeholder data.
- **Every query-facing promised model needs a semantic view.** Define the view
  over that model and register it with `.model(...)` in `data_product_output()`;
  a physical table without one may build but cannot be selected by
  `run_semantic_query`.

Role builders: `field(number(), primary_key(), dimension(name=...), description="...")` — key roles compose with a dimension, and `grain` is deprecated; `field(string(), dimension(name=..., pii=<flag>), description="...")`; `field(number(), join(to="<model>", to_column="<col>"))` — `to=`, NOT `to_model=`. **Timestamp types are parameterized:** import `DurationUnit` from `nxd.spec.data_types` (`models.py` may import only from `nxd.spec.*`) and use `timestamp(unit=DurationUnit.Milliseconds)` (or the source's required precision); never emit bare `timestamp()`, which raises `TypeError` during supervisor spec compilation. See [reference/nxd-spec-api.md](reference/nxd-spec-api.md) for the full type surface. `primary_key()` contributes no dimension; the paired `dimension(name=...)` is unique across every model in the spec, joined or not, so a key column shared by two models needs a model-qualified dimension name on one of them.

**Every field takes a role, except a measure a metric aggregates.** A field carrying a dimension or metric needs a `description=` on the field (the role inherits it); `primary_key()`/`join()` take none. Every `semantic_model` needs `.description(...)`, and a `join(...)` needs a `dimension(...)` on the same field. The semantic view must carry a metric — a bare `COUNT` will do — or the model is unqueryable (`struct.model_not_queryable`); a bare key is likewise not groupable. `describe_models` is all a later consumer sees, so a bare column is invisible and a bare name unusable. Put descriptions on `field()`/`metric_field()` so the dimension or metric inherits the same text shown by the catalog. A dimension a **ruling** created must state that ruling.
Metrics stay question-driven: a numeric no question aggregates is a `number` dimension. For an approved row-level output, every projected value — including numeric amounts — remains a dimension and must be selected in `dimensions[]`; do not create or query a `total_<field>` metric in place of those record values. If the catalog exposes only an aggregate for a promised row-level field, repair the semantic roles before querying rather than presenting aggregate rows as records. Name each promised output field, landed column and `dimension(name=...)` exactly as the request or approved plan names it (`stage`, never `deal_stage`): consumers, contracts and later releases query those names, so add no entity prefix and rename nothing. Tag only the non-promised dimensions of the registry with their model; when two promised names collide, return to the plan instead of renaming either. No marker model: produce-verification is `.transform-complete`.
`reference/models-example.md` shows the shape.

**Derived models are authored identically** — same DSL, role vocabulary and
`.schema({...})` shape; only their schema keys (the transform's yielded dict
keys, not source headers) and possibly a grain-derived composite `primary_key()`
differ. Nothing in `models.py` marks a model as derived.

Worked examples: `reference/models-example.md` (base) and [reference/derived-models.md](reference/derived-models.md) (derived). Every verified DSL signature and the inferred→`nxd.spec.data_types` mapping are pinned in `reference/nxd-spec-api.md` — trust it over re-reading source.

### Step 3 — `transform/main.py`: the dlt-through-port ingest

The transform receives the typed **output port handle** (`DuckDbOutput`: `path`,
`schema`, `model_tables`) and connector secrets, streams base and derived rows
through dlt in one run, then asserts the produced tables. The handle is named
**`duckdb`** to match Step 4. Declare `PHYSICAL_MODELS` from required
`.promise(...)` calls plus optional-empty `.model(...)` registrations, with base
names first; resolve names only through `duckdb.model_tables` (semantic views
may also be present there). The complete template is in
[reference/transform-template.md](reference/transform-template.md).
For 2+ labeled CSV/file sources, use the canonical pinned-root dataflow in
[reference/multi-source.md](reference/multi-source.md#canonical-transform-dataflow).

Contract facts baked into that template — keep every one (each is restated in the Invariants, where the full reasoning lives):

- The `duckdb` param MUST be typed `DuckDbOutput` — untyped gets a raw context with no `path`/`model_tables`.
- `PHYSICAL_MODELS` names exactly the landed physical models: required models
  passed to `.promise(...)` plus optional-empty models passed to `.model(...)`;
  `OPTIONAL_EMPTY_MODELS` is a literal subset. Do **not** iterate
  `duckdb.model_tables`, which can include semantic views with no table.
- The connector config arrives in `secrets` (Overview table) — for
  `db-source`/`api-source` the supervisor's **FLAT** merge of every service's
  `attributes` keys, service name not among them: `secrets["base_url"]`, never nested.
  Never hard-code an absolute path. Writes go **through the port**
  (`dlt.destinations.duckdb(credentials=duckdb.path)` + `dataset_name=duckdb.schema`),
  never raw `duckdb.connect(...)`, DDL, or a hardcoded staging path.
- `write_disposition="replace"` — reruns must be idempotent, not duplicating. An
  append-only source goes incremental ONLY via
  [reference/incremental-transforms.md](reference/incremental-transforms.md). A
  per-row provider/mapper call loop keeps its own deadline under the prepared
  time budget and lands finished rows, and a capped or versioned refresh follows
  that file's [refresh replay](reference/incremental-transforms.md#refresh-replay-settle-backlog-and-history-in-the-plan) rules.
- The read-back-and-assert block and the `.transform-complete` touch are
  MANDATORY: the first enforces the physical-model allowlist (only an absent
  optional-empty table is tolerated), the second is what the readiness gate
  polls.

**Windows source files.** Files written by Windows PowerShell 5.1 may carry a UTF-8 BOM; read source text with `encoding="utf-8-sig"` (dlt's `read_csv(...)` forwards `encoding` to pandas, as the templates show; never pass that encoding to DuckDB `read_csv`, which rejects it).

### Step 3a — Derived models: computed rows through the SAME port

A **derived model** is a physical model with no `data/<name>/` directory: rows computed in Python from the base sources, landed through the same
port. Every ruling the semantic layer cannot express lives here — dedupe,
amortization, normalization, classification.

**The DDL ban (Step 3) is preserved, not relaxed**: still written by dlt through
the `duckdb` port, still NO `duckdb.connect(...)` write, NO `CREATE TABLE` /
`CREATE VIEW`, NO direct file write into staging. The only new thing is where the
rows come from — a `@dlt.resource` generator instead of a CSV reader. Every
clause below is mandatory and each is restated in the Invariants:

- **Yield plain FLAT dicts** — no pyarrow in the pinned venv, so a DataFrame
  raises (`df.to_dict(orient="records")`), and a nested value spawns a
  `parent__field` child table that fails the assert.
- **Same list, same run** — appended to the SAME `resources` list as the CSV
  readers, landed by ONE `pipeline.run(..., write_disposition="replace")`.
- **Named from `model_tables`** (`@dlt.resource(name=duckdb.model_tables["<derived>"])`)
  and listed in `PHYSICAL_MODELS` via `DERIVED_MODELS`.
- **Read the sources yourself** with stdlib `csv` and `sorted()` over the glob:
  dlt's reader streams to the destination and cannot hand rows back to Python.
- **Deterministic**, and confined to the fixed venv (`pandas`, `duckdb`, stdlib);
  `requirements.txt` is **never installed at runtime**.

### Step 3b — In-memory asserts: the durable derived-row check

**Transform asserts are the durable derived-row check; custom contracts never
replace them.** A contract states what the **user guaranteed**; an assert proves
what the **transform produced**. One helper per derived model, invoked between
deriving and yielding, each an **invariant over the source-vs-derived
relationship** — the thing no verifier sees — over the complete derived set
before rows are yielded. Restating the transform's own arithmetic proves
nothing. **Mandatory tiers:**

- **Tier 1 — every derived model, always:** (a) the **declared key is unique**
  over the complete derived set, and (b) the **row count computed from the
  grain** matches source rows **read independently** from the base CSVs.
- **Tier 2 — whenever the model carries a MEASURE column:** the **signed measure
  total must reconcile** against the signed total read independently from the
  base CSVs, **every intentional divergence itemized as its own named term**
  (`- refund_pairs_total`), in `Decimal`, **per source currency BEFORE any FX
  conversion**. Dropped roll-ups, unmatched codes and skipped blanks are EACH a
  term; the source side is the UNFILTERED total (never the model's own filter); a
  blank adds 0, so also a COUNT term (landed rows == non-null source cells - dropped rows; blank-cell count reported on its own). Counts never replace the
  signed sum, even for rates and yields: sum them as a checksum.

Raise `RuntimeError` whose message carries actual-vs-expected and, for a rejected value, the offending values with their counts; a bare or generic raise reaches the user as an opaque failure. An itemized exclusion means a **removal**, not an enrichment, and carries extra invariants; classification totality alone can pass while every monetary answer is overstated — both, with worked code, in [reference/derived-models.md](reference/derived-models.md).

**Other connector types**: Step 3 is identical except the `readers=[...]` body and `secrets[...]` key — take those from `reference/` (`file-source.md`, `database-source.md`, `api-source.md`); when an API returns a metadata envelope, select its row array with the resource endpoint's `data_selector` before landing. For a credentialed REST API, `auth_type = secrets.get("auth_type")` is mandatory: branch on it to assemble structured `client_config["auth"]` from the flat `secrets` fields and raise for unsupported non-`None` values; never hard-code only the scheme today's profile uses. Implement only auth modes declared by the approved source contract, so a bearer-only contract gets a bearer branch plus unsupported-mode failure, not speculative API-key or OAuth flows. Steps 3a/3b are connector-independent. For an API profile with `auth_refresh_path`, copy/adapt the refresh-aware session in [`reference/api-source.md`](reference/api-source.md#expiring-credentials-refresh-on-the-session-never-on-a-custom-auth-class) or [`scripts/api_source_refresh_session.py`](scripts/api_source_refresh_session.py) into the self-contained closure: override `send()`, not `request()` (dlt calls `send()`), allow at most one refresh/replay after 401 and one bounded `Retry-After`/backoff replay after 429, then fail with a bounded diagnostic; never claim resilience without this state machine. Preserve load-bearing JSON numeric lexemes before dlt parses them (see the `response_actions` recipe in `reference/api-source.md`), keep money as `Decimal` through the transform and yield, and declare `decimal(precision, scale)` matching the approved source scale; `Decimal(str(float_value))` after ordinary JSON parsing is not an exactness proof. Never silently coerce missing/null source values to semantic defaults such as `0` or `""`; reject them when required or preserve null when the approved plan allows it, and never use `row.get("amount", 0)` to make incomplete data look valid. Any field excluded by the approved physical/output contract—including an internal filter field such as tombstone `status`—must be filtered in memory before any resource yields or pipeline writes; roleless/PII flags do not redact raw DuckDB.

### Step 4 — `spec.py`: models + transform + the `duckdb` output port

`spec.py` is the author-facing source compiled into deployment YAML: it declares
the infra profile, transform, every landed physical model, and query-time views.
Bind service references by relative `infra-profile.yaml` paths. The v3 prose
proposal's `Inputs`, `Models`, `Transform`, and `Outputs` are compiled here;
custom contracts are closure-side wiring ([reference/custom-contracts.md](reference/custom-contracts.md)). Worked `spec.py`: [reference/models-example.md](reference/models-example.md).

Before handing the executable closure to the job loop for capture, run the
[pre-capture audit](reference/pre-capture-audit.md). Resolve the approved
Models, Outputs, physical-surface limits, README claims, and typed-v3 to
`nxd_decisions` projection before capture seals the inputs.

`Outputs` is authoritative for user-facing projections, questions, and delivery channels. DuckDB still publishes all landed physical models, including internal support relations; do not call one user-facing unless listed in `Outputs`.

Contract facts baked into that shape — keep every one:

- **The output port is named `duckdb`** (`.port("duckdb", storage(...))`, never
  `"output"`) matched by the transform param (Step 3), and
  **`infra_profile="desktop-local"`** on `data_product(...)` matches
  `infra-profile.yaml`'s `metadata.name`.
- **`script("transform/main.py")`**, not `code(transform)` — the standalone
  entrypoint the compute driver executes, registering itself via
  `@data_product.on_transform()`. `.compute(...)` binds `python-compute`;
  `.secrets([...])` delivers the connector config as the transform's `secrets`.
- Promise exactly the **required** landed physical models — **base and derived
  alike** — and register optional-empty physical models with `.model(model)` so
  they reach `model_tables` without a contract for an absent table. Register
  every metric view via `.model(view)`, never `.promise(view)`: views are
  query-time only.
- **No `.semantic_tools(...)`.** The supervisor's semantic child builds the MCP
  catalog from compiled model roles, and the proven closure serves all three tools
  without it. `.semantic_tools()` emits a kernel RPC port needing a live RPC
  driver — a k8s artifact with no local equivalent: a port nothing serves.

**Other connector types**: only the variable name and service path change; for
2+ of one type, `.secrets([...])` takes one labeled variable per instance
(`reference/multi-source.md`).

### Step 5 — `infra-profile.yaml`: the desktop-local profile (emitted prerequisite)

For a CSV source, the desktop closure ships the three local
services the spec references (`duckdb`, `python-compute`, `csv-source`). Emit that CSV profile
**verbatim** from [reference/infra-profile.md](reference/infra-profile.md);
`metadata.name` is `desktop-local` and MUST match `infra_profile=` in `spec.py`.
Copy the fixed driver IDs exactly: `duckdb` = `nxd:local/duckdb/storage:0.1.0`,
`python-compute` = `nxd:local/python/compute:0.1.0`, and `csv-source` =
`nxd:local/file/storage:0.1.0`; never shorten them to a bare local driver.
The `csv-source` service (driver `nxd:local/file/storage:0.1.0`) delivers the
**relative** `csv-source-path` into `secrets[...]` (an absolute path escapes the
pinned snapshot and fails).

**Other connector types** use their source-specific recipe instead of CSV artifacts; never add a dummy `csv-source-path` or export. They change the third service's name and its
`attributes` — the rules, and what derived models do not change, are in
[reference/infra-profile.md](reference/infra-profile.md).

### Step 6 — `requirements.txt`: the proven pins

```
nxd.data_product[spec]
dlt[duckdb]==1.28.2
duckdb==1.5.4
pandas==2.3.3
```

`dlt[duckdb]==1.28.2` + `duckdb==1.5.4` are proven against the S0 supervisor — do not float them; `pandas` is required by dlt's `read_csv`; Python `>=3.12,<3.13`. These pins describe runtimes that install the closure's `requirements.txt`. The Desktop runtime does not install that file; it supplies database drivers (an NXD `dlt[sql_database]` + PostgreSQL driver change is in flight). This file is for other runtimes; see `reference/` for connector-specific additions.

### Step 6a — Declare the capture-owned snapshots

For workflow-v2, `nxd-run-job-loop` writes and validates the exact typed proposal
beside `dp-blueprint.md`, parses it, and passes the complete object inline as
`typed_proposal` in `prepare_workflow`.
The shellless generator emits only the executable closure and authored README.
It must not run `dp_diagnostics.py lock write`, initialize reserved records, or
hand-author `dp-blueprint.approved.md`, `dp-blueprint.proposal.approved.json`,
`dp-blueprint.lock.json`, or a copy of `self_check.py` before capture. The
supervisor materializes and verifies those surfaces during its returned capture
action. See [reference/closure-record.md](reference/closure-record.md) for the
capture contract; `build-record.json` remains generated, never hand-authored.
### Step 6b — Defer adversarial review to the job loop after capture
Under workflow-v2, call the `check_data_product` MCP tool on the authoring
closure before returning it and fix every failing finding, following the
[preflight before capture](reference/pre-capture-audit.md#preflight-before-capture); after the review the job loop runs a fresh full check (structural only for a mapper closure) on the exact closure it publishes (an earlier check is stale after any edit).
The developer self-check recipes are optional evidence outside this activated Desktop route.
They must not create Desktop reserved records/checker copies, edit retained captures,
or execute a paid mapper outside admission. Use the current MCP check in the applicable mode;
optional evidence does not authorize capture, replace the trusted supervisor checker, or relax
strict admission. Bash may be unavailable under OAuth, so never stall or
substitute hand-authored hashes, locks, records, or checker copies when those
tools cannot run. Return the authored executable closure to the job loop, which
follows the supervisor's capture action before review, validation, and admission.
That job loop dispatches exactly one built-in read-only reviewer over the
supervisor-provided retained capture and blueprint; the reviewer remains a
conversation child and never a supervisor operation.
Dispatch, sanitization, claim relay, and authorization remain governed by
[reference/adversarial-review.md](reference/adversarial-review.md).
## Invariants — NEVER violate these
After supervisor capture, the retained closure contains the complete file set: `spec.py`, `models.py`, `infra-profile.yaml`, `transform/main.py`, `requirements.txt`, `dp-blueprint.approved.md`, `dp-blueprint.lock.json`, `build-record.json`, `README.md`, the connector companion artifact where the type has one — and, for a credentialed source, `SENSITIVE` and `.gitignore`. This frozen inventory describes legacy literal credentials; a Desktop-local `attributesSecretRef` holds no authored secret value, so its public profile needs neither marker, and neither does an env-injected profile (harness/operator-provided variable) that is all `public: true` with a single bare-name `credential_env`; the native-entry `attributesSecretRef` stays the preferred shape for user builds, never default to `credential_env`. This is the captured result, not the pre-capture authored-tree requirement. For 2+ labeled CSV sources, additionally verify the root-level `companion-files` manifest. For `api-source`, additionally require the closure-local `connectivity_check.py` probe; only its endpoint-map companion is absent because the endpoint map is `endpoint_<model>` attributes on the infra-profile service.
- **Python-only closure**: under workflow-v2, emit only `spec.py`, `models.py`, `infra-profile.yaml`, `connectivity_check.py` for `api-source`, `transform/main.py`, `requirements.txt`, `README.md`, the connector companion artifact where the type has one — and, for a legacy literal credential profile, `SENSITIVE` and `.gitignore` (for `api-source`, the endpoint-map companion is absent because its map is carried by `endpoint_<model>` profile attributes; the connectivity probe is still required). Do not emit, initialize, verify, or require `dp-blueprint.approved.md`, `dp-blueprint.proposal.approved.json`, `dp-blueprint.lock.json`, or `build-record.json` in the authored tree; the supervisor materializes and validates those files during capture. NEVER hand-write `deployment-spec.yaml` / `manifest.yaml` / `models.yaml` — the supervisor compiles those from the Python at pin time. The active `dp-blueprint.md` and its typed proposal are authored beside the closure by the job loop: expectations and promises are authored under Inputs and Outputs, while executable contracts and fixed local delivery remain internal.
- **Custom contracts are an exact executable inventory, never optional decoration** — every typed-v3 Input expectation and Output promise produces exactly one verifier and matching `custom(...)` wiring at its declared attachment and phase, carrying the same name, model, guarantee, rule, and fields; ordinary `.promise(model)` does not satisfy one. Capture/preflight reject missing, extra, placeholder, or unwired contracts. Create no contract from inferred schema facts; for API inputs, fail/ask when the runtime cannot execute the declared phase, while supported output promises remain wired. See [reference/custom-contracts.md](reference/custom-contracts.md).
- **Self-contained closure — no cross-boundary contract pointers** (Step 6a): the approved `dp-blueprint.md` is byte-copied in as `dp-blueprint.approved.md` and bound by `dp-blueprint.lock.json`, so everything a later session needs to continue the work lives INSIDE the closure and self-containment is hash-checkable rather than a discipline anyone has to remember. A promised derived model's contract (rubric, thresholds, output schema, verdict set) is materialized in the closure — in the approved spec, as `contracts/<name>.md`, or as the inert derived model itself — NEVER referenced by a `../`-rooted path to a doc outside the closure, `../dp-blueprint.md` included. Phase C fails a missing snapshot, lock, `build-record.json` or `README.md`, a snapshot whose bytes no longer match the lock, and any closure-escaping contract reference.
- **Scope is part of the contract, not an incidental choice**: if the source is sampled rather than taken whole, the selection rule is stated in `Scope` (and so travels in `dp-blueprint.approved.md`), reproducible over the same source, and MUST NOT drop rows on which a downstream model or step depends.
- **The naming invariant**: each physical model name == `models.py` `semantic_model` arg == `PHYSICAL_MODELS` == `main.<name>`, unquoted lowercase snake_case; required models also appear in `spec.py` as `.promise`, while optional-empty models appear there as `.model` and in `OPTIONAL_EMPTY_MODELS`. A physical table is expected for every required model and for every optional model that yields rows; only an absent optional-empty table is allowed. Base models additionally match the connector's per-model reference (`data/<name>/`, see "THE NAMING INVARIANT" table), with an absent optional base directory allowed only when it is listed as optional. Semantic views are `.model(...)` only and have no physical table. The transform's read-back assert is the runtime tripwire — keep it.
- **Output port named `duckdb`**: `.port("duckdb", storage(...))`, transform param `duckdb` typed `DuckDbOutput` (port name == param name). The local DuckDB driver requires exactly this name.
- **Through the port, always**: dlt destination is `duckdb.path` / `duckdb.schema`. No raw `duckdb.connect` writes, no view/table DDL, no direct file writes into staging. **Derived models do not relax this** — they reach the port as `@dlt.resource` generators in the same `pipeline.run(...)`, not as DDL.
- **Derived models are flat, deterministic, and in-run** (Step 3a): plain scalar dicts (no DataFrame — no pyarrow in the fixed venv; no nested values — they spawn `parent__field` child tables), appended to the SAME `resources` list, landed in ONE `pipeline.run(..., write_disposition="replace")`, named from `duckdb.model_tables`, listed in `PHYSICAL_MODELS`. Read the sources yourself with stdlib `csv`. No `now()`, no unseeded random, sorted inputs. Imports confined to pandas / duckdb / stdlib.
- **Every derived model carries mandatory in-memory asserts** (Step 3b): Tier 1 always — declared-key uniqueness plus a grain-derived row count against independently-read source rows; Tier 2 whenever a measure column is present — a signed measure total reconciled per currency pre-FX in `Decimal`, every exclusion itemized as a named term. Raised with actual-vs-expected before the rows are yielded. It is the in-transform data-quality gate, and it is mandatory whether or not the closure also declares executable contracts — the runtime now enforces those too (custom input expectations before the transform, custom output promises after the DuckDB writes, blocking publication when violated), but a promise cannot see the intermediate state an assert checks. Never restate the transform's arithmetic as an assert, never substitute a weaker invariant for the measure reconciliation, and never loosen one to make a run pass. A model that **scores** adds both: every scored cell carries an explanation row (`band_id` + `evidence_field` + `evidence_quote` + `evidence_kind` + `limitation`, keyed by entity × criterion, reusing the `reference/llm-judgments.md` citation vocabulary; `evidence_kind` is `fact`/`inference` per explanation row and is NOT `nxd_decisions.provenance`, which is authorship per ruling), and every quote is asserted a verbatim substring of the field it cites. **Absence is labelled, never scored** — a field the derivation could not read scores empty with a `limitation` naming the kind: never the scale minimum, never zero, never a gate `FAIL` (an absent gate input is a landed `UNKNOWN`); it drops out of the weighted sum, the composite lands beside the fraction of rubric weight that scored, and a cap keyed on absence is legitimate only when its verdict names the uncertainty (`NEEDS_MORE_INFO`), never when it is a judgement (`REJECT`). Full rules, the absence kinds, and the precedence when a supplied rubric's bottom band *is* the absence case: [reference/derived-models.md](reference/derived-models.md).
- **Multi-source joins add a fail-closed source contract**: copy/adapt [`scripts/source_contract.py`](scripts/source_contract.py) into the self-contained transform. For CSV/file sources, call `read_csv_rows` before matching and use `expected_columns` when the approved header set is exact; for API/database sources, apply the same schema check to the complete captured rows before matching. The recipe rejects missing or blank required fields before a wrong name can silently produce zero matches. When the approved output asks for match coverage, call `coverage_summary` separately for every source side and land its row count, matched count, basis-point rate, and complete unmatched identity list. For an aggregate ratio, expose additive numerator/denominator metrics separately and use `assert_aggregate_ratio` over those columns; never expose a row-level ratio (such as per-campaign CPA) with `Agg.AVG` or any other reduction. The allowed row-grain alternative is a derived ratio column validated with `assert_row_ratios`, without a reducing metric over that column. The default output quantum is one integer unit for cent-scaled CPA; pass the approved `quantum` for fractional rates. These are transform assertions, not review suggestions: raise with actual values before any derived resource is yielded, and copy the recipe's source into the closure rather than importing it from an installed skill tree.
- **No materialization before the policy read-back** (Workflow § Gate): when the request supplies a procedure with a gap that changes a score, verdict, gate outcome, or which rows land, NOTHING is written — no closure directory, no source copy, no generated code, no table, no scoring, no build — until the user has seen the enumerated proposal and replied. Reading the source is allowed; answering a technical delivery question is not approval; "use your judgement" licenses authoring the proposal, not skipping the turn.
- **Compile the approved `dp-blueprint.md`; never re-derive or exceed it.** `Models` and `Transform` define the plan, `Outputs` define the public surface, and `Decisions` becomes one ledger row per approved typed Decision through the mechanical projection in [reference/pre-capture-audit.md](reference/pre-capture-audit.md). A ruling in the closure that appears in no spec section is one the user never approved. The IR lives beside the closure and is never referenced from it by a `../` path (Phase C fails that); the approved revision travels inside as the byte-copied `dp-blueprint.approved.md`, and outcomes — row counts, blockers, review rounds — never go back into the IR.
- **The self-heal loop may change generated code; it may NEVER change the IR.** A compiler does not edit your source to make the build pass. Fix `spec.py` / `models.py` / `transform/main.py` / the landed data as often as the caps allow (remap ≤ ~2 per question, regenerate ≤ ~3 total, counted from `build-record.json` `attempts[]` rather than estimated), but if green is only reachable by changing the plan — narrowing the population to dodge a bad join, dropping a model whose grain will not resolve, relaxing a threshold, weakening a criterion — **stop**: that is a spec edit requiring re-approval, not a heal. Escalate it as `blocker.spec_edit_required`. Every attempt records `spec_hash_before` and `spec_hash_after`, so a heal that moved the hash is caught mechanically instead of trusted. A build-time blocker is an `open_questions` entry discovered LATE: write it back into the live `dp-blueprint.md`, which un-approves the spec and puts it in the same "needs your input" queue as a pre-build gap — never invent a second mechanism for it. Typed heal exits: `healed`, `healed_with_concessions`, `caps_exhausted`, `blocked`, `retry_environmental`; non-convergence is reported, never looped on silently and never abandoned silently.
- **FORBIDDEN versus DISCOURAGED — a heal loop may not relitigate an absolute.** FORBIDDEN, never done even to reach green, escalated as a blocker instead: hand-writing `deployment-spec.yaml` / `manifest.yaml` / `models.yaml` (`blocker.forbidden_handwritten_yaml`); hand-rolling a durable watermark instead of `transform_state` (`blocker.forbidden_manual_watermark`); `write_disposition="replace"` while yielding a delta (`blocker.forbidden_replace_disposition`); loosening an assert into restating its own arithmetic (`blocker.forbidden_assert_restates_arithmetic`); and reaching green only by changing the plan (`blocker.spec_edit_required`). DISCOURAGED is permissible, but the run is then green **with a disclosed concession** — record it in `build-record.json` `concessions[]` with what was done, what it cost, and the alternative rejected. Every recorded concession must be explained in plain language before claiming a materialized result; use [user-facing-language.md](../nxd-run-job-loop/reference/user-facing-language.md) for the wording. **A green run carrying an undisclosed concession is the worst state in this design, because it reads as materialized.** And `materialized` is the word — never `correct`: a green run means the approved plan compiled, ran and published, never that the numbers are right. The term is the pack's, backed by a `dp_diagnostics.py materialized` subcommand. Codes, the full split, the record's schema and the naming rule itself: **nxd-run-job-loop**'s `reference/build-record.md`.
- **No `.semantic_tools(...)`**: the supervisor's semantic child builds the catalog from compiled semantic roles; the spec must not emit an RPC port.
- **Public semantic DSL only**: base models carry `primary_key` / `dimension` / `join`; metrics are `metric_field(metric(...))` on `semantic_view(...)`. Never import private modules or write metadata directly.
- **Validated keys, by kind**: every physical model, required or optional, has one or more `primary_key()` fields (missing is `struct.no_primary_key`; settle before capture, since fixing it afterward forces a reset and a new review round). A **base** model's key is one or more EXISTING source columns whose tuple is non-null and unique across the supplied export — never synthesize one; stop and ask for the source key when that evidence is absent. A **derived** model's key is defined by the derivation's grain, constructed deterministically from source values plus the grain's ordinal, and proven unique by an in-transform assert. A dedupe keeps its source key; only a regrain declares a new composite.
- **Connector via secrets, `infra-profile.yaml` shape**: source config only from `secrets[...]`, with canonical source names in the [source types index](reference/source-types.md), arriving as ONE flat map merged across every service named in `.secrets([...])` — a `csv-source`/`file-source` contributes its single driver-supplied key, a `db-source`/`api-source` one key per connection field, so two instances of a type collide unless every key carries a label prefix (`reference/multi-source.md`) — always delivered via `.secrets([...])` on the transform. The profile is `metadata.name: desktop-local` with at least three services (`duckdb`, `python-compute`, one connector service per source instance). `duckdb`, `python-compute`, `csv-source`, and `file-source` keep `attributes: []` (their companion path file is relative); `db-source`/`api-source` (and their labeled variants) carry explicitly public topology attributes and a native Desktop `attributesSecretRef` for credential fields; legacy literal profiles may still carry one `{"key": ..., "value": ..., "public": <bool>}` attribute per connection field — for `api-source` that includes one `endpoint_<model>` attribute per API-backed model, which is where the endpoint map lives rather than in a companion file — marked `public:` by sensitivity — secrets/identity (password, user, tokens/keys) `false`, non-secret topology/config (host, port, database, schema, base_url, auth_type, region) `true` so it survives an export — see `reference/database-source.md` / `reference/api-source.md`. Never fabricate a credential, never narrate one in chat, never write a raw database password or API token into a committed closure file, and never let two same-type instances share a name. A legacy literal credential profile emits `.gitignore` (naming `infra-profile.yaml`, never `*`) and `SENSITIVE` in the same step that writes the credential, plus `chmod 0600 infra-profile.yaml` where a shell can reach the closure. An env-injected, ref-less all-public profile with one bare-name `credential_env` is also exempt (see `reference/api-source.md`; not the generator default). For a local reference with only public topology, Phase C defers authenticated binding and source access to supervisor admission.
- **Labeled transform-only CSV exception**: a `csv-source-<label>` root is not a per-label secret. Read its relative path file below the mandatory `NXD_TRANSFORM_ROOT` using a fail-closed environment lookup (`os.environ["NXD_TRANSFORM_ROOT"]` or equivalent); never fall back to `.` or `Path.cwd()`. Carry its non-empty `data-<label>/` tree through the root-level `companion-files` manifest; the general `secrets[...]` rule above applies to ordinary single-source CSV/file closures and credentialed connectors.
- **Run-local dlt state** (`pipelines_dir` under the run dir + `DLT_DATA_DIR` set; never `~/.dlt`); **`write_disposition="replace"`**; **`.transform-complete` touch** after the assert. **Incrementality never relaxes the run-local half**: dlt's own state stays ephemeral under the run dir, and the durable watermark lives in the kernel's `transform_state` bag — two separate mechanisms, never composed. `transform_state` round-trips on desktop and is the only sanctioned durable store: never hand-roll one (sidecar file, marker table, `SELECT max(<cursor>)` off the output table, durable `pipelines_dir`). The one sanctioned incremental route is [reference/incremental-transforms.md](reference/incremental-transforms.md); read it before switching any disposition, because every failure mode here is silent. It gates on **every promised model being append-safe** (never an aggregate, regrain, or dedupe), addresses the bag through **`for_model()`**, never flat indexing at any model count, yields every promised model every run, and verifies the write by **row count** — the table-name assert cannot see a missing write under `"append"` — and moves the `.transform-complete` touch after **both** checks (leave it after the naming assert and the readiness gate can report the build ready before the row-count check raises). `"replace"` while yielding only a delta shrinks the table to the delta; `"append"` without a cursor is the duplicate-rows bug.
- **Place, don't redesign**: semantic roles come from nxd-build-semantic-data-product. Preserve a file connector's supplied export exactly by default; omit unneeded personal-data columns only through the declared, verified projection in [nxd-run-job-loop's source-materialization guide](../nxd-run-job-loop/reference/source-materialization.md). Treat a database or API connector as read-only. Cleaning, dedupe, reclassification and regrain happen ONLY in derived models downstream of the approved landed source, never by editing the user's original. A reference or dimension model lands every source row; roll-ups and out-of-scope rows are excluded only in the derived model that needs them, as named reconciliation terms ([derived-models](reference/derived-models.md)). Use an existing validated key for base models or surface the missing-key problem. Promise required base and derived models, register optional physical models and metric views with `.model(...)`, and add no marker model on desktop.
- **Reference data is landed, never hardcoded**: FX rates, merchant→category rulings, account mappings and similar judgements that exist in no source data are user-confirmed and landed as their own model, so they stay queryable and reviewable. **This includes any agent- or LLM-inferred score, verdict, or classification** — landed as data (`status = proposed`, `provenance = agent_authored`); a per-entity judgement literal in transform code is hardcoded even when the downstream arithmetic is computed. Never bake reference data into transform code as a constant dict or `if` ladder. With no user available to confirm, land the mapping anyway as PROPOSED, recorded as a row in the closure's landed `nxd_decisions` model — never a `DECISIONS.md` file — see [reference/derivation-plan.md](reference/derivation-plan.md) and, for agent judgement, [reference/llm-judgments.md](reference/llm-judgments.md). **The transform never imports a provider SDK, and calls a model only through the sanctioned seam**: `import anthropic` (or any listed provider root) in `transform/main.py` is denied outright. Inference in a **packaged** closure runs through `nxd.experimental.field_mapper`'s `make_call`, under a consent grant — that is what keeps the procedure inside the artifact, resolves the credential outside it, and puts the approval in front of the user. Agent-side judging that lands as CSV before the build is the **exploration** lane: right while the rubric is still moving, wrong as a shipping shape, because the prompt and the reading of the evidence stay outside the closure. Self-containment is a property of the logic, not the values — a bundled procedure whose scores move between runs is more self-contained than a frozen output nobody can re-derive. Self-check **Phase E enforces this mechanically** before the transform is imported, and it is a tripwire rather than a sandbox: it denies an enumerated list of model-SDK and transport imports there, and model-SDK imports in `contracts/**/*.py` too, so a green Phase E means "no *listed* SDK", not "provably offline" (see [reference/self-check.md](reference/self-check.md) § What Phase E cannot see). **Phase G** is the separate, sanctioned path, and it is a *consent* check rather than a reach one: a closure that imports the field-mapper harness — `nxd.experimental.field_mapper`, shipped inside the installed `nxd` package, per [reference/field-mapper.md](reference/field-mapper.md) — may map, but only under a grant in `contracts/` binding the hash of each mapper spec kept there. Reach for it whenever a packaged closure's answers depend on inference — including the mapping over rows the transform itself produces that it was first written for; while the product is still being explored, [reference/llm-judgments.md](reference/llm-judgments.md) is the cheaper lane and needs no grant, no consent record, and no model call at build time — but it is a scaffold, and a closure being packaged moves its judging here. The harness computes that id itself, and the three consent codes are `owner: user` because you cannot consent on the user's behalf, extend an expiry, or decide a drifted rubric is still acceptable (see § What Phase G cannot see).
- **Proven pins**: `dlt[duckdb]==1.28.2`, `duckdb==1.5.4`, pandas, the nxd wheel; Python `>=3.12,<3.13`.
**Related skills:** **`nxd-run-job-loop`** owns the conversation and invokes this skill; **`nxd-build-semantic-data-product`** produces the inferred model it places; **`nxd-build-data-product`** is the k8s/cloud path.
