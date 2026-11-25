---
name: nxd-build-semantic-data-product
description: Builds a governed text-to-SQL / metrics / semantic-layer data product on Nextdata OS, exposing curated metrics and dimensions over MCP so an AI agent can answer natural-language questions without writing raw SQL. Use when the task is to create or extend a data product that lets agents query business metrics by name (e.g. order_count, revenue) sliced by dimensions (e.g. region, product_category), when you need NL-to-SQL governance over a Snowflake data product, or when exposing a semantic layer as an MCP server tool set. Also covers INFERRING the semantic model when no schema doc exists — profiling a materialized source table (local DuckDB sample) and deriving grains, metrics, dimensions, joins, and PII flags from the profile plus the user's natural-language questions. The author writes only per-field semantic annotations on the models; the one-line .semantic_tools() spec flag auto-generates the three governed MCP tools from the installed nxd.data_product wheel.
allowed-tools:
  - Bash
  - Read
  - Write
  - Edit
  - MultiEdit
  - Glob
  - Grep
  - AskUserQuestion
metadata:
  author: nextdata
  version: 0.76.0
---

# nxd-build-semantic-data-product skill

## Overview

A semantic-layer data product exposes **named metrics and dimensions** over MCP.
An AI agent calls `run_semantic_query` with concept names; the data product
compiles a correct, governed SQL query and returns rows — no raw SQL escapes the
DP boundary.

**You author only the per-field semantic annotations on the models.** A single
`.semantic_tools(service=...)` flag on the spec auto-generates the three governed
MCP tools at pod boot. The kernel compiles the annotations into typed payloads; the
compiler, dialect, and tool factory ship in the `nxd.data_product` wheel as
`nxd.experimental.semantic` — imported, not vendored. The three tools:

| Tool | Purpose |
|------|---------|
| `list_models` | Enumerate the semantic models (entities) with grain + metric/dimension counts, plus author `agent_instructions` and `verified_queries` (see `reference/registry-authoring.md`), `data_product` per model (empty on a data product's own endpoint unless the model declares it), and — on a data product's own MCP — `is_view` on every model, `over` on views and `to_data_product` on a join that reaches another data product's model |
| `describe_model` | Human-oriented detail for one model: metrics (+ compatible dimensions), dimensions (+ PII flags), joins, model `agent_instructions` |
| `run_semantic_query` | Compile a concept selection to governed SQL, run it, return rows |

See `reference/overview.md` for the design and how annotations flow to the tools.

> **This skill teaches the `.semantic_tools()` pattern.**

> **Two flows use the inference here — pick one first.**
> - **Platform flow (this skill):** a governed semantic DP on Nextdata OS —
>   Snowflake/warehouse output, split-pod k8s `.semantic_tools()`, a deploy step.
>   The workflow/credential/deploy/consume sections below assume this flow.
> - **Local end-to-end flow:** the AI generates AND runs the DP locally on a
>   desktop supervisor — a **different shape** owned by
>   **nxd-generate-data-product**. Follow the data-only boundary in
>   [reference/local-inference-handoff.md](reference/local-inference-handoff.md),
>   then stop and return its complete inference handoff to the owning job loop.
>   **Do NOT
>   follow the Snowflake/credential/deploy/consume steps below in the local flow.**

---

## Workflow

> **The data product is FOUR files, not one:** `models.py` + `spec.py` +
> `transform.py` + `requirements.txt`. A validated `models.py` is a milestone, NOT
> the finish line — passing the acceptance test still leaves an unshippable DP if
> the other three are missing. Carry the work through every step to all four files
> (Step 7 checks completeness) before reporting done.

### Step 1 — Derive the semantic vocabulary from the schema

Interview the user or read the table DDL to establish, per source table:

1. **Model** — the physical table: a unique name + one or more **primary-key**
   columns (the entity key, e.g. `order_id`) + a **description** (one line:
   what one row is). It reaches the agent in both `list_models` and `describe_model`.
2. **Dimensions** — columns an agent can group or filter by. Each: a concept
   `name`, the physical `column`, a logical `type` (`string` / `date` / `number`),
   a `description`, and `pii: true` if governed. Dimension names are unique across all models in the spec, joined or not.
3. **Metrics** — named aggregated measures. Each: a concept `name`, the physical
   `column` it aggregates, the `agg` function (`count`, `count_distinct`, `sum`,
   `avg`, `min`, `max`), a `description`, and `boolean: true` for a flag that counts
   truthy rows.
4. **Joins** — documented N:1 relationships, declared on the MANY-side model's join
   key: `to_model` (the ONE side), `to_column`, `cardinality: many_to_one`.
   Cross-model dimension reach is **auto-derived** from N:1 joins by the compiler.

### Step 1-alt — Infer from a profiled source + the user's questions

When there is **no schema doc** — only a materialized sample of the source and the
user's natural-language questions — derive the Step-1 vocabulary yourself. In
the platform flow, Steps 2–4 (models.py / transform.py / spec.py) are unchanged.
In the local end-to-end flow, follow the linked handoff and stop before codegen.

**1. Profile the materialized tables → `schema.json`.** A sample load (e.g. dlt)
lands each source table as `main.<name>` in a local DuckDB file. Read
[reference/scripts-bootstrap.md](reference/scripts-bootstrap.md) first, then introspect ALL of them with this skill's profiler
(DuckDB mode — needs `duckdb`, e.g. `uv run --with duckdb`) and **save the combined document as `schema.json`**:

```bash
PROFILE_SKILL_DIR="<nxd-build-semantic-data-product>"
python "$PROFILE_SKILL_DIR/scripts/profile_tabular.py" sample.duckdb <table1> <table2> ... > schema.json
```

With two or more tables the profiler emits ONE combined document —
`{"path": ..., "format": "duckdb", "tables": {<table>: <profile>, ...}}` — where
each table's profile carries, per column: `declared_type`, `nullable`, `null_pct`,
`distinct_count`, `cardinality` (distinct/total, exact full-table), `sample_values`,
plus freshness hints. `schema.json` is the **handoff artifact**: keep it in the
workspace, infer by READING it (re-query the DuckDB file only for targeted
follow-ups like the join-containment probe below), and leave it as the evidence
for how the model was derived. **Ground the model in this profile — annotate only
columns that exist in it; never invent or rename columns.**

**2. Classify each column from its profile signals:**

| Profile signal | Likely role |
|---|---|
| `cardinality` == 1.0 AND `null_pct` == 0 (exact full-table), id-ish name (`*_id`, `*_key`, uuid samples) | **grain** candidate (the model's entity key) |
| id-ish name, cardinality < 1.0, values match another table's grain | **join** key candidate (MANY side → `to_model`, `many_to_one`) — validate before declaring (see below) |
| numeric (`DOUBLE`/`DECIMAL`/amount-ish name), not an id, **additive** (see below) | **metric** candidate |
| `BOOLEAN` / true-false samples | boolean-flag **metric** (`"boolean": true` — MUST pair with `"agg": "sum"`) and/or dimension |
| low-cardinality string (`segment`, `status`, `channel`, country codes) | **dimension** (`type: "string"`) |
| `DATE`/`TIMESTAMP` (freshness hints) | **dimension** (`type: "date"`) |
| samples look like emails, names, phones, addresses | dimension with **`"pii": true`** — flag from the DATA, even if no question asks for it (NULLs in some rows don't unmark it) |

**Primary-key selection.** Trust exact full-table cardinality; samples can fake
uniqueness. Prefer a unique column that matches the entity or FK target; if
needed, use a composite `{"kind": "primary_key"}` role and validate its
non-null unique tuple with `COUNT(*)` versus `COUNT(DISTINCT (a, b))`.

**Local-desktop handoff.** Every physical base needs one or more validated
primary-key columns across the complete export, not a shard or lucky sample.
Without evidence, request the source key; never invent one or generate a
closure. Emit canonical `primary_key()` / `{"kind": "primary_key"}`, never
the deprecated `grain` alias.

**What crosses the boundary.** Per model: its `description`, and per column its
`data_type`, its roles, and for each dimension/metric role a `name`, a
`description`, and `pii` where it applies. Roles alone are an incomplete
handoff — the generator places what it is given and infers nothing, so a
concept that arrives without a description reaches `describe_models` as a bare
name and stays that way.

**Join validation.** Never use name similarity or a few overlapping samples.
Every non-null FK must resolve on the ONE side, and its target column must be
that model's full-table unique primary key; otherwise `many_to_one` is a lie.

Declare the blob on the MANY-side FK with explicit `to_model` and `to_column`. If
the samples don't overlap, that is evidence AGAINST the join — probe or ask.

**Additive vs non-additive numerics.** A numeric column is a `sum` metric only if
it is **additive across rows** (amounts, quantities, per-row durations). Scores,
points, percentages and rates (`loyalty_points`, `discount_pct`) are NOT sum
metrics; aggregate one only when a question justifies it (`avg`/`min`/`max`),
else expose it as a `number` dimension whose description says why it is not
summed; never leave one unannotated. A **snapshot** written once per period
(`stock_on_hand` per `snapshot_date`) adds across warehouses, never across
dates: where supported, declare `non_additive_over=["snapshot_date"]` (a query
summing across dates then gets SQ-308); never a plain `sum` without it (`reference/registry-authoring.md`). A **distinct count landed per bucket** (accounts active per week, per week and feature) is not additive either: summing it across weeks or features counts one account once per bucket. Prefer a `count_distinct` metric on the event-level model, with the bucket (`week_start`) landed as a dimension column in the first build, so every grouping is a true distinct count; a kept pre-aggregated count takes `non_additive_over` on each bucket dimension where supported, else is a `number` dimension, never a plain `sum`.

**DuckDB declared type → `AttributeSpec` data type** (for the `models.py` attributes). Timestamp columns import `DurationUnit` from `nxd.spec.data_types` and require an explicit unit; the example below uses millisecond precision.

| DuckDB `declared_type` | `nxd.spec.data_types` |
|---|---|
| `VARCHAR` / `TEXT` | `string()` |
| `TINYINT`/`SMALLINT`/`INTEGER`/`BIGINT`/`HUGEINT` | `int64()` |
| `DOUBLE` / `FLOAT` / `REAL` | `float64()` |
| `DECIMAL(p,s)` / `NUMERIC` | `decimal(p, s)` (or `float64()` if precision is not load-bearing) |
| `BOOLEAN` | `boolean()` |
| `DATE` | `date32()` |
| `TIMESTAMP` / `TIMESTAMPTZ` | `timestamp(unit=DurationUnit.Milliseconds)` |

**3. Let the QUESTIONS drive what you declare** — the profile says what a
column *could* be; the questions say what it *must* be:

- "total/revenue/spend ..." → a `sum` metric on the money column.
- "how many X ..." over a flag ("churned", "first-time") → a metric on the
  boolean column with **`"agg": "sum"` AND `"boolean": true`** — the dialect
  defines the boolean CASE-sum ONLY for `sum` (`SUM(CASE WHEN ... THEN 1 ELSE
  0 END)`); `"boolean": true` with any other agg is invalid. Never a plain
  numeric SUM of a flag.
- "average ..." → `avg`. "how many distinct/top N by count" → `count` /
  `count_distinct` on the grain/key. A column serving two aggs gets a
  `{"roles": [...]}` wrapper. "by/per <attribute>" → that column is a dimension.
- A question slicing one table's metric by another table's attribute (e.g. orders
  by customer country) → declare the validated N:1 **join** on the MANY-side FK;
  the compiler auto-derives the cross-model dimension reach.
- "per order / per customer ..." confirms the **grain** of each model (one row per
  entity — cross-check against exact full-table cardinality 1.0).

**Every column gets a role, and every dimension and metric role a
description** — the questions decide which role, not whether to annotate.
`primary_key()` and `join()` take no `description`; do not infer one for them,
and never fall back to the enclosing `field()`, which the agent never sees. The
one exception to the role rule is a column a declared metric already
aggregates: its meaning travels on the metric. The marker model is exempt
from the ROLE rule only — it still takes a `.description(...)`. A column with no role produces no metric,
dimension or join and is invisible to `describe_model`; leaving one bare is a
decision to make it unqueryable. A spare dimension costs a line in the catalog;
a missing one costs an unanswerable question and a rebuild. Flag from the DATA,
the same way `pii` is flagged — even when no question asks for it.

**Metrics are the exception, and stay question-driven.** Do not declare metrics
no question motivates — that is how non-additive numerics end up as nonsense
`sum`s. A numeric that earns no metric is still annotated: expose it as a
`number` dimension with a description saying what it is and why it is not
summed (`loyalty_points`, `account_balance`, `discount_pct`). Unannotated is
not the fallback; a dimension is.

**3b. Surface ambiguity — don't silently resolve it.** The role grammar has
**no filtered metrics, no derived ratios, and no default filters**: a metric is
exactly `<agg>(<column>)`. When a question's business definition is ambiguous
against the profiled data, do NOT hard-code one interpretation silently:

- *Status-qualified totals* — "total revenue" over a table whose `status` samples
  include `refunded` / `cancelled`: the metric can only be the unconditional
  `sum`. Say so in the metric `description` (e.g. "Gross order amount across ALL
  statuses, including refunded and cancelled") AND declare the status column as a
  dimension so consumers filter at query time.
- *Derived ratios* ("revenue per customer", "churn rate") — not expressible as one
  metric; expose the component metrics and state that the ratio is computed by the
  caller from two queries.
- In an interactive session, ask (AskUserQuestion) instead of guessing; in a
  non-interactive run, record the ambiguity and your chosen interpretation in the
  metric descriptions and your final report.

**4. Naming invariant.** Each `semantic_model(name)` argument is the **bare
unquoted lowercase physical table name** — `semantic_model("customers")` for the
table profiled as `main.customers` (never `"main.customers"`, never a prettified
rename). Attribute names must match the profiled column names **byte-exactly**
(post-dlt snake_case preserved — `customer_id`, not `CUSTOMER_ID`). The transform
seeds those same tables (unquoted), so compiler, seed, and profile resolve to one
object.

### Step 2 — Author `models.py` with the public semantic DSL

Use the public `nxd.spec` field builders only. The platform compiles those public
roles for every **promised** model at build time; never mutate private attribute
metadata or add a second semantic representation.

`primary_key()` is canonical (never the deprecated `grain` alias), and pairs with a `dimension(...)` on the same field — a bare key never reaches `describe_models`, so nothing can group by it. Use
`join(to="<model>", to_column="<col>")`, not `to_model=`, and give every
dimension its stable business name and PII flag when applicable.

Keep every module **flat at the DP root** — `models.py`, `transform.py`, `spec.py` are siblings. No `transform/` subdir package.

```python
# models.py
from nxd.spec import Agg, dimension, field, join, metric, metric_field, primary_key
from nxd.spec import semantic_model, semantic_view
from nxd.spec.data_types import float64, int64, string

# Abridged. This file must ALSO define `products` (the join target below — a join
# is invalid unless its `to=` model exists) and `provision_marker` (Step 4's marker).
orders = (
    semantic_model("orders")
    .description("One row per order.")
    .schema(
        {
            "ORDER_ID": field(int64(), primary_key(), dimension(name="order_id"), description="Order key."),  # bare key = not groupable
            "REGION": field(
                string(),
                dimension(name="region"),
                # The description goes on the field; the dimension inherits it,
                # so describe_model and the catalog UI show the same sentence.
                description="Sales region the order was booked in.",
            ),
            "PRODUCT_ID": field(int64(), join(to="products", to_column="PRODUCT_ID")),
            # Bare is correct here: the total_revenue metric below aggregates
            # this column, so its meaning travels on the metric.
            "REVENUE_USD": field(float64()),
        }
    )
)

order_metrics = semantic_view("order_metrics", orders).schema(
    {
        "total_revenue": metric_field(
            float64(),
            metric(
                Agg.SUM,
                of=orders.field("REVENUE_USD"),
                name="total_revenue",
            ),
            description="Gross order revenue in USD across all order statuses.",
        ),
    }
)

```

**Role grammar** — public `field()` DSL:

| Role | Public DSL |
|------|------|
| primary key | `field(<type>(), primary_key(), dimension(name=...), description=...)` — roles compose, and a bare `primary_key()` is not groupable |
| dimension | `field(<type>(), dimension(name=..., pii=<bool>), description=...)` |
| metric | define on a `semantic_view(...)` with `metric_field(metric(...), description=...)`; do not add it to a physical base field |
| join | `field(<type>(), join(to=..., to_column=...))` — no description parameter |
| model | `semantic_model(...).description("One row per ...")` |

Emit `primary_key()`; `grain` is deprecated.

**Write the `description` once, on the field** — `field(..., description=...)` /
`metric_field(..., description=...)`. A dimension or metric declaring none of its
own inherits it, so `describe_model` and the catalog UI show the same sentence.
`dimension(description=...)` / `metric(description=...)` still win but are
deprecated and emit a `FutureWarning`.

See `reference/registry-authoring.md` for the full role vocabulary,
auto-derivation rules, and a worked example.

### Step 3 — Author `transform.py` to seed the base tables (base-table default)

By default, `run_semantic_query` compiles against base tables from the kernel
payloads; this path needs no semantic-view DDL or provisioning hook.

```python
# transform.py
from nxd.data_product.context import Snowflake


def transform(snowflake: Snowflake) -> None:
    import pandas as pd
    from snowflake import connector
    from snowflake.connector.pandas_tools import write_pandas

    if snowflake is None or not snowflake.schema:
        return
    fqn = (f"{snowflake.database}.{snowflake.schema}."
           if snowflake.database else f"{snowflake.schema}.")
    rows = pd.DataFrame([
        {"ORDER_ID": 101, "REGION": "EMEA", "PRODUCT_ID": 1, "REVENUE_USD": 100.0},
        {"ORDER_ID": 102, "REGION": "AMER", "PRODUCT_ID": 2, "REVENUE_USD": 250.0},
    ])
    conn = connector.connect(
        user=snowflake.user, account=snowflake.account, warehouse=snowflake.warehouse,
        role=snowflake.role, database=snowflake.database, schema=snowflake.schema,
        ocsp_fail_open=True, **snowflake.connector_params(),
    )
    try:
        # Create UNQUOTED so Snowflake folds to upper-case — the compiler
        # references the base table unquoted too, so both resolve to one object.
        conn.cursor().execute(
            f"CREATE OR REPLACE TABLE {fqn}orders "
            "(ORDER_ID NUMBER, REGION VARCHAR, PRODUCT_ID NUMBER, REVENUE_USD FLOAT)"
        )
        write_pandas(conn, rows, "ORDERS",
                     database=snowflake.database, schema=snowflake.schema)
        # Marker row (the promised marker model).
        managed = snowflake.full_table_name("semantic_smoke_marker")
        conn.cursor().execute(f"TRUNCATE TABLE IF EXISTS {managed}")
        write_pandas(conn, pd.DataFrame([{"MARKER_ID": 1, "VIEW_NAME": "n/a"}]),
                     managed.split(".")[-1].strip('"'),
                     database=snowflake.database, schema=snowflake.schema)
    finally:
        conn.close()
```

The transform's param name (`snowflake`) MUST match the storage output port name;
it is injected as a typed `Snowflake` handle. **Never type it `Any`** — an untyped
param gets a raw `Context` with no driver methods.

### Step 4 — Wire `spec.py`: transform + storage port + `.semantic_tools()`

`.semantic_tools(service=...)` auto-wires the three MCP tools + an mcp-api port.
**Promise every annotated model** on the storage port so its attributes reach the
kernel-generated manifest (and thus the `.nxd/semantic/<model>.json` payloads); add
the marker model so produce-verification passes.

```python
# spec.py
from nxd.spec import code, data_product, data_product_output, storage
from transform import transform
from models import orders, order_metrics, provision_marker   # provision_marker = the marker model

INFRA_PROFILE = "<infra-profile-name>"

_storage = (
    data_product_output()
    .promise(provision_marker)
    .promise(orders)
    .model(order_metrics)
    .port("snowflake", storage(f"/infra-profile/{INFRA_PROFILE}#/services/<snowflake>"))
)

spec = (
    data_product(name="my-semantic-dp", domain="...", version="1.0.0-dev",
                 infra_profile=INFRA_PROFILE)
    # Seeds the base table(s) + the marker row for default base-table routing.
    .transform(
        code(transform).compute(f"/infra-profile/{INFRA_PROFILE}#/services/<compute>")
    )
    .output(_storage)
    # ONE line — auto-wires the three tools + the mcp-api port (defaults
    # port_name="mcp-api", mcp_path="/mcp").
    .semantic_tools(service="<mcp-service-name>")
)
```

`semantic_tools(service, *, port_name="mcp-api", mcp_path="/mcp", backend="snowflake",
view_name=None, view_names=None)` — `service` names the infra-profile service.

Key facts:
- **RPC output:** `.semantic_tools()` creates one when absent and composes its
  three tools onto an existing RPC output; `service`, `port_name`, and `mcp_path`
  are ignored in that compose case.
- **Promise every annotated model**, or its attributes never reach the manifest and
  its `.nxd/semantic/<model>.json` payload is never written.
- **For this transform-backed pattern, `.transform(...)` is required** — it seeds the base tables the tools query AND
  bundles the sibling `models.py` (the `**/*.py` glob runs on the compute path).
- **Base-table default needs no semantic-view DDL.** For native routing, provision
  separately with `.provision(sql(...).compute(...))` and set `view_name` or
  `view_names`; do not put `plain_view_ddl()` in the transform.
- **Use plain `storage(...)` for this transform-backed path.** For the separate
  no-transform `.config(...).as_view(...)` facade, follow the reference.

---

### Step 5 — Emit `requirements.txt` (REQUIRED deliverable)

**Write a `requirements.txt`** (alongside `spec.py` / `models.py` / `transform.py`).
The flow-neutral entries are always `nxd.data_product[spec]`, `pandas`, and
`pyyaml>=6.0.2`. Then add the **storage runtime for your output backend**
(backend-dependent — list the one your DP actually uses):

- **Local DuckDB flow** (profiled-from-a-local-sample): add `duckdb` — the transform
  and semantic tools run against DuckDB. Do NOT add a Snowflake connector.
- **Snowflake/warehouse flow** (platform): add `snowflake-connector-python[pandas]`
  and `nxd.drivers[rpc]` for the split-pod topology.

Without this file the compute pod can't install its runtime. `pyyaml` powers the
`.semantic_tools()` manifest fallback (`_manifest_compile` compiles the blobs from
`models.yaml` when the MCP pod runs no kernel). See
`reference/runtime-and-dependencies.md`.

---

### Step 6 — Glossary links and cross-DP lineage (optional)

`semantic_model(...).link(Predicate.GlossaryTerm, "<term-uri>")` attaches
governed glossary terms (model-level and, with an attribute name as the first
arg, per-attribute). `attribute(int64(), "SUBJECT_ID").referencing(data_product=...,
model=..., attribute=[...])` on a schema attribute declares a cross-DP foreign
key the discover UI renders as a SEMANTIC RELATIONSHIP.

Declare the runtime dependency with `.input(...).source(...)` in `spec.py`
(before `.transform()`); the `.referencing(...)` makes the FK render as a semantic
relationship. Cross-DP joins resolve at QUERY time via the live mesh — the
downstream transform seeds only its own base tables. See
`reference/runtime-and-dependencies.md` for the full lineage form.

---

### Step 7 — Verify the DP is complete before reporting done

The acceptance test validates `models.py` only — passing it does NOT mean the DP
is finished. Before reporting done, confirm all four files exist in the workspace:
`models.py` (validated), `spec.py` (Step 4), `transform.py` (Step 3),
`requirements.txt` (Step 5). If any is missing, the DP is incomplete — author it.

---

## Invariants — NEVER violate these

- **Never re-implement the compiler or MCP tools.** They live in
  `nxd.experimental.semantic` (shipped with the `nxd.data_product` wheel) and are
  auto-wired by `.semantic_tools()`. Import; never copy.
- **Use `.semantic_tools(service=...)`.** It creates an RPC output or composes
  the tools onto an existing one, whose port configuration it keeps.
- **Promise every annotated model.** Un-promised model → no manifest attributes →
  no `.nxd/semantic/<model>.json` payload → that model is invisible to the tools.
- **Use the public field DSL only.** Author keys, dimensions, and joins with
  `field(..., role(...))`; author metrics on semantic views. Never mutate private
  model metadata.
- **Native semantic-view DDL is optional;** the base-table route is default.
- **In this transform-backed pattern, declare `.transform(...)`** — it seeds the base tables AND bundles
  `models.py`.
- **Chasm-trap**: a resolvable, collapsible path permits cross-home metrics,
  pre-aggregated at their home grains; disconnected paths or unsafe roll-ups
  raise `CompileError`.
- **Agg enum is closed**: count, count_distinct, sum, avg, min, max.
- **Cross-model arithmetic is a `derived_metric`** on a `semantic_composition`, never agent-side math; weekly/coarser feeds declare `time_grain=`. See `reference/registry-authoring.md`.
- **Read-only, 200-row cap**: the query path is aggregated and capped. No raw-SQL
  passthrough.
- **All modules flat at the DP root**: never a `transform/` subdir; import flat.
- **Matched wheel version set**: `core` + `drivers` + `data_product` all the same
  version, recent enough to carry `.semantic_tools()`. A stale `core` fails at
  runtime (`missing field secret_password`). See `reference/runtime-and-dependencies.md`.

## Reference docs

| File | Content |
|------|---------|
| `reference/overview.md` | Design + how public semantic roles flow to the 3 tools |
| `reference/registry-authoring.md` | Full role grammar + auto-derivation + derived metrics + native time grains + snapshot, private and presentation fields + worked example |
| `reference/compiler-and-routing.md` | Compile paths + chasm-trap + Snowflake dialect |
| `reference/runtime-and-dependencies.md` | Requirements, wheel version, payload delivery + fallback, lineage |
| `reference/scripts/templates/semantic_dp.py.tmpl` | Complete models.py + transform.py + spec.py example |
| `reference/scripts/scaffold_semantic_dp.py` | Scaffold automation (writes models/transform stubs + requirements, prints spec wiring) |

This skill is the **producer** side; to **query** a deployed DP, use the **nxd-query-data-product** skill.
