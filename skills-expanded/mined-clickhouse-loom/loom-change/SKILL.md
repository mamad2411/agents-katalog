---
name: loom-change
description: Lists what else a Loom change must touch in the same PR (generated files, snapshots, erasure classification, docs, manifests) for a new or changed op, field, table, column, migration, setting, flag, worker, provider, CLI command, plugin hook or dashboard page. Use before editing for any of those.
metadata:
  internal: true
---

# Making a Loom change

Find the row for the change, read its guide before the first edit, and finish its "also" column in the same pull request. The rules under `.claude/rules/` add the area-specific traps.

| Change | Guide | Also in the same PR |
| --- | --- | --- |
| Wire op (new, renamed, removed field) | [adding-an-operation](../../../docs/development/adding-an-operation.md) | `python -m scripts.codegen.sdk_py_gen`, `.sdk_py_client_gen`, `.sdk_ts_gen`, `.docs_reference`, `.op_reach_census`; unit test + integration test for a read or write path; MCP listing budget if it is listed by default; its dashboard control, or a `NOT_IN_DASHBOARD` reason in `server/operations/dashboard.py` |
| Table or column | [adding-a-table](../../../docs/development/adding-a-table.md) | migration + `make schema-dump`; RMT row builders; `loom.memory_versions` + its view for a `loom.memory` column; erasure step + census row, or a `NO_MEMORY_CONTENT` / `STEP_ONLY_TABLES` entry with its reason; a new table's row in `docs/architecture/storage-layout.md`, its Today cell when the engine, sort key, partition key or TTL changes, its Erasure cell when its census classification changes, its row removed when the table is dropped (with the dump pending, the row test fails until it lands) |
| Migration | [migrations](../../../docs/development/migrations.md) | next free number on current `origin/main`; additive only; `make schema-dump` on a private ClickHouse (with none at hand, leave `schemas/schema.sql` unchanged and report the dump as pending; never hand-edit it); written values N-1 tolerates ([rolling upgrades](../../../docs/architecture/rolling-upgrades.md)), `make test-mixed-version` |
| Setting | [extending-loom](../../../docs/development/extending-loom.md#add-a-setting) | field in its area's section of `server/settings/catalog.py` (models in `Models`) with a comment on what it controls and its values; `python -m scripts.codegen.settings_reference`, `.settings_schema` and `.settings_example`; read as `settings.<field>`; a rename or removal follows the [settings rule](../../rules/settings.md) |
| Retire a flag | — | delete the setting, its branch and any request field carrying it; the PR body's changelog entry names it |
| Worker | [adding-a-worker](../../../docs/development/adding-a-worker.md) | registry row; `LOOM_UPDATE_WORKER_SNAPSHOT=1` for an intended snapshot change |
| Provider | [extending-loom](../../../docs/development/extending-loom.md#add-a-provider) | `make bench-quick` evidence before changing a default (ask first — see `loom-bench`) |
| Code-index language | [adding-language-support](../../../docs/development/adding-language-support.md) | stay outside the extractor stamp; backfill plan in the PR |
| CLI command or flag | [code-generation](../../../docs/development/code-generation.md) | `LOOM_UPDATE_CLI_SNAPSHOT=1` snapshot; `python -m scripts.codegen.docs_reference`; a command the chart's hook Jobs run (`deploy/helm/loom/templates/hooks.yaml`) changes there too |
| Plugin file (hook, `lib/`, `bin/`, skill, `assets/`, `.mcp.json`, Codex `plugin-defaults.json`, a manifest's listing fields) | [integrations](../../../integrations/claude-code-plugin/README.md) | hook scripts, `lib/`, `bin/`, skills and `assets/`: edit `integrations/claude-code-plugin/`, then `python -m scripts.codegen.agent_plugin_sync`; a manifest, `hooks.json`, `.mcp.json` or `plugin-defaults.json`: edit each plugin's own copy (`plugins` rule); for a behaviour change, bump both plugin manifests to a version no other open PR uses |
| Dashboard | [dashboard-design](../../../docs/development/dashboard-design.md), [local-development](../../../docs/development/local-development.md#the-dashboard) | `npm --prefix frontend run test`, `npm --prefix frontend run build`, bundle budget, `make lint` (Biome's accessibility rules) |
| Helm chart | [kubernetes](../../../docs/operations/kubernetes.md) | `helm lint --strict` and `kubeconform` on both overlays; a renamed setting as in the Setting row |
| Docs | [documentation-style](../../../docs/development/documentation-style.md) | regenerate generated pages; never hand-edit them |

## Before the first edit

- A new table, op group, auth-model change, external dependency or identity-tuple change is a material change: the PR body carries the design (what, why, the alternatives and their cost, the migration story), and the matching `docs/architecture/` page describes the system as it now is ([material changes](../../../CONTRIBUTING.md#material-changes)).
- Read the rule for each area the change touches (`AGENTS.md`, "Rules by area"), and search for the helper you are about to write.
- Moving a module: shipped files resolve through `server.core.paths`, never `Path(__file__).parents[N]`.

Then run `loom-pre-push`.
