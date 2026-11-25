---
name: board-pack-scaffolding
kind: workflow
surfaces: [tool]
description: >
  Experimental internal workflow for evaluating multi-dashboard scaffolding:
  propose a folder structure, review with the user, then apply through the
  Python agent API. Use only when explicitly evaluating pack-level scaffolding
  for a data source or project. Do NOT use for a single-dashboard request
  (use {{ s_skill_name_build }}). Do NOT use for normal CLI guidance, chart edits, or
  bug fixes in one board file.
metadata:
  author: fivetran
---

# Dashboard Pack Scaffolding

Scaffold a coherent folder-and-dashboard structure for a data source or project.
The flow is always: **explore schema → propose → human review → apply → validate**.
Never apply without the user seeing and approving the proposal first.

> This is a **tool-only experimental skill** (`surfaces: [tool]`). It is not a
> public CLI workflow and should not be presented as product documentation.

## When NOT to fire

- A single-dashboard request ("add a revenue chart") → use `{{ s_skill_name_build }}`
- A chart edit or layout fix on an existing board
- A bug fix in one board file
- A request for public CLI help or installation guidance
- A sparse `charts/` dir alone — sparsity is a signal, not a trigger; confirm
  pack-level intent explicitly before proceeding

## The Workflow

### Step 1 — Explore the schema

Before proposing anything, read the real schema with metadata SQL against the
configured source (source names are in `dbt_charts.yml`):

```bash
dct query <source> "SELECT table_schema, table_name FROM INFORMATION_SCHEMA.TABLES ORDER BY 1, 2"
```

Use it to understand what connectors and domains are present, and drill into
column names with `INFORMATION_SCHEMA.COLUMNS` filtered to the tables you care
about. Running it first lets you sanity-check the proposal and catch
misconfigured sources before the propose step.

To see which data pages are already authored, grep the boards for `aliases:`
entries with `/data/...` URLs (`grep -rn "/data/" charts/`).

### Step 2 — Propose

Generate a pack proposal through the agent API:

```python
from pathlib import Path

from dbt_charts.agent_api.pack import propose_pack

proposal, proposal_path = propose_pack(Path("."))
print(proposal_path)
```

The planner reads schema metadata, groups tables into folders and dashboards, and
writes a proposal artifact to `target/dbt-charts/proposals/`. Nothing under `charts/`
is touched yet.

Optional: specify an organization mode if the user has a preference.

```python
proposal, proposal_path = propose_pack(Path("."), mode="connector-first")
```

Use `mode="domain-first"` when the user explicitly wants business-domain folders.

### Step 3 — Show and review the proposal

Read the proposal file and present it clearly to the user. Explain:

- Which folders will be created under `charts/`
- What the `index.yml` landing dashboard covers per folder
- Which dashboards will be scaffolded

**Crucially, review the data bindings.** Each `ProposedDashboard` may carry a
`canonical_data_url` field. When set, the generated board will claim that data
URL via an `aliases:` entry, so that `/data/<source>/<schema>/<table>/` redirects
to the authored page instead of the generic system view. Verify these bindings are
correct before applying:

- The URL must match the actual source/schema/table the dashboard covers.
- Two dashboards in the same proposal cannot share the same `canonical_data_url`
  — the apply step raises if they do.
- A `canonical_data_url` of `None` means no alias will be emitted; the generic
  system view continues to serve that data URL.

If the proposed bindings look wrong, edit the proposal YAML to correct or clear
the `canonical_data_url` values before applying.

Ask the user to confirm or request changes before proceeding. If they request
changes, edit the proposal YAML directly and summarize what changed.

### Step 4 — Apply

Once the user approves, load and apply the reviewed proposal through the agent
API:

```python
from pathlib import Path

from dbt_charts.agent_api.pack import apply_proposal
from dbt_charts.cli.filesystem_project import FilesystemProject
from dbt_charts.core.pack.proposal_store import load_proposal

proposal = load_proposal(Path("target/dbt-charts/proposals/fivetran-zendesk/proposal.yml"))
result = apply_proposal(proposal, FilesystemProject(Path(".")))
print(result.model_dump())
```

The apply path creates the `charts/` folder tree: one subfolder per proposed
folder, with an `index.yml` landing and dashboard stubs. It validates
every generated file and skips existing ones unless `overwrite=True` is passed.

Generated boards with a `canonical_data_url` automatically include:

```yaml
aliases:
  - /data/<source>/<schema>/<table>/
```

This makes the data URL redirect to the authored board. The `index.yml` landing
links to canonical `/data/...` paths for dashboards with data URLs, so
drill-through links are stable even before the detail pages are built out.

### Step 5 — Validate and confirm data links

After scaffolding, validate the generated files:

```bash
dct validate charts/
```

Fix any errors, then confirm data links resolve correctly: each dashboard
that claims a data URL must carry an `aliases:` entry with the expected
`/data/...` URL (`dct validate` lints alias source names; `grep -rn "/data/"
charts/` shows the claimed URLs).

Then open `dct serve` so the user can see the landing pages and start filling
in queries.

```bash
dct serve
```

Visit a landing page (e.g. `http://localhost:8001/zendesk/`) and click one of
the data links. It should redirect to the authored board. If it serves the
generic system view instead, the alias is not set — check the board file.

## The `index.yml` Convention

Every pack folder landing is **always** `index.yml`, never `overview.yml`:

```
charts/
  zendesk/
    index.yml          ← folder landing (DO NOT name this overview.yml)
    ticket-overview.yml
    user-overview.yml
  salesforce/
    index.yml          ← folder landing
    opportunity-overview.yml
    account-overview.yml
```

The server routes `charts/zendesk/` → `charts/zendesk/index.yml` automatically.
If you ever encounter `overview.yml` as a folder landing in existing code or
docs examples, that is stale — rename it to `index.yml`.

## Data URL format

Canonical data URLs follow the pattern:

```
/data/<source>/<schema>/<table>/
```

Examples:
- `/data/fivetran_zendesk/zendesk/tickets/`
- `/data/fivetran_salesforce/salesforce/opportunity/`
- `/data/db/analytics/orders/`

These URLs always resolve: the generic data system view serves them when no
authored board claims them. An authored board claims one by putting the URL in its
`aliases:` list. The alias is on the board — there is no central data registry
file to maintain.

**Row-level links** use the `/detail/` sub-path with the primary key as a query
param:

```
/data/<source>/<schema>/<table>/detail/?id=12345
```

Row links are only safe when a URL-safe numeric primary key exists. The planner
does not auto-generate row links because it cannot inspect column types at
proposal time; you add them manually once you know which column is the key.
Do not invent row links from row offsets or arbitrary visible columns — use
only a column whose name is `id` or ends in `_id` and whose type is integer
or exact decimal (scale 0).

## Quality checklist

Before handing back to the user:

- [ ] Schema explored with INFORMATION_SCHEMA queries before proposing
- [ ] Data bindings reviewed — each `canonical_data_url` matches the
      dashboard's actual source/schema/table
- [ ] No duplicate `canonical_data_url` values across proposed dashboards
- [ ] Proposal reviewed and approved by user before applying
- [ ] Every folder landing is `index.yml`, not `overview.yml`
- [ ] `dct validate charts/` passes with no errors
- [ ] Claimed data URLs have matching `aliases:` entries in the board files
- [ ] `dct serve` confirms landing pages route correctly and data links redirect
