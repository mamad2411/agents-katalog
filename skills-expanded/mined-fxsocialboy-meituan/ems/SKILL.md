---
name: ems
description: Query and operate the EMS Platform (a.k.a. Entity Platform; EMS = Entity-Mapping-Storage; ent.tiktok-row.net) — list/get storages and entities, inspect sync channels (edges, lag, throughput), query entity online DDL, list/get EMS schema-change workflows, update storage owners, validate CREATE/ALTER DDL, publish schema changes, approve the Owner gate, and advance bound BPM resource-deployment tickets. Use when the user mentions EMS, Entity-Mapping-Storage, Entity Platform, ent.tiktok-row.net, storage_iac, storage spec/topology, DB Spec, RDS table create/alter, DDL validation, Owner gate, sync edge/channel, or provides an ent.tiktok-row.net URL, a storage URI (`tiktok/mysql/xxx`), an entity URI, or an EMS workflow ID. Do NOT use for BITS, DevFlow, Meego, or standalone BPM tickets. EMS is i18n-line ONLY — no BOE / BOE-I18N; refuse BOE requests. EMS also does NOT support publishing schema changes to the `BOE-I18N` vregion — drop it from validate/create inputs and refuse if asked.
---

> **session_id 传递**：若本次任务需要在多次 `gdpa-cli run` 之间串联 workflow 状态、日志或上下文，请复用同一个 `session_id`。如果当前 skill / Agent 已经提供了 `session_id`，**请直接复用，不要新建**。
>
> - **已有时优先复用**：不要重复执行 `create-session`。
> - **没有时再创建**：执行 `gdpa-cli create-session`。
> - **后续调用**：可以显式传 `--session-id <session_id>`，例如 `gdpa-cli run <agent> --session-id <session_id> --input '{...}'`。
> - **适用场景**：Base Workflow、BITS Dev Workflow、post-coding-verify 及其他依赖 Session 工作目录的场景需要持续复用；普通单次查询通常可以不传。

# EMS Skill

Query the **EMS Platform** (a.k.a. **Entity Platform**) at `ent.tiktok-row.net` — storages, entities, sync channels, and schema-change workflows.

> **Naming**: EMS = **Entity-Mapping-Storage**. The platform is also referred to as the **Entity Platform** in product docs and team conversations. "Entity Management Service" is **NOT** the correct expansion — do not use it. All three names (`EMS` / `Entity-Mapping-Storage` / `Entity Platform`) refer to the same console at `ent.tiktok-row.net`.

> **When to Use**: Look up a storage's spec / topology / tables, inspect a storage's sync channels, check an entity's schema or online DDL across vregions, browse schema-change workflows, drive an RDS table create/alter through validate → publish → owner approve → BPM, or resolve an ent.tiktok-row.net URL.

## ⚠️ Region coverage — i18n line ONLY

EMS is deployed exclusively on the i18n production line (`https://ent.tiktok-row.net`). There is **no BOE, no BOE-I18N, no CN-line** counterpart of this platform.

Concretely:
- The skill always uses an I18N JWT (resolved from `region.GetJWT("Singapore-Central")`).
- Storages/entities can themselves be deployed to BOE / BOE-I18N vregions, but **the EMS metadata catalog that describes them lives on i18n only** — you still query it through `ent.tiktok-row.net`.
- If the user asks "查 BOE 的 EMS / EMS 的 BOE 环境 / 在 BOE-I18N 上看 storage_iac"，refuse and point them at the i18n console (`ent.tiktok-row.net`) instead of guessing or substituting another endpoint.
- The `target_addr` parameter is for **i18n staging hosts**, not for BOE — do not pass a BOE address there.

### ⚠️ Schema-change publishing on `BOE-I18N` is NOT supported (write side)

Even though EMS can _read_ the metadata of a BOE / BOE-I18N storage, the **publish path** (`validate_ddl_change` → `create_schema_change` → `approve_workflow_owner_gate` → `advance_workflow_bpm_ticket`) cannot drive a CREATE / ALTER through to a `BOE-I18N` vregion today — the resource-deployment step has no working BPM ticket on that region. Concretely:

- Do **NOT** include `BOE-I18N` in `tables[i].vregions` or the top-level `vregions` for `validate_ddl_change` / `create_schema_change`. Drop it from the list (or split that region out into a separate, manual change) before publishing.
- When a user asks "在 BOE-I18N 上发布 / 建表 / 改表 storage / table"，refuse the publish and surface this limitation; do not silently retry on a different region.
- Read-only inspection of a BOE-I18N-bearing storage / entity (`get_storage`, `get_entity`, `list_entities`, `get_entity_online_ddl`, sync-channel actions) is unaffected — those just query the i18n catalog.

## Actions

All actions use the caller's Singapore-Central JWT (obtained automatically). EMS only has an i18n deployment, so there is no BOE / BOE-I18N / CN target to switch to — `target_addr` is reserved for i18n staging / proxy hosts, NOT for BOE.

| action | role | reference |
|---|---|---|
| `list_storages` | List V2+V3 storages (default mode=2 = my storages) | `references/storages.md` |
| `get_storage` | Get storage detail (spec / topology / meta) by URI | `references/storages.md` |
| `update_storage_owners` | (write) Modify a storage's owners list (add/remove) | `references/storages.md` |
| `get_storage_sync_channel` | List sync edges of a storage (mermaid + ascii topology) | `references/sync_channels.md` |
| `get_storage_sync_channel_detail` | Detail for ONE edge (sub-task / lag / throughput / link) | `references/sync_channels.md` |
| `list_entities` | List entities (auto: storage_uri ⇒ all-under-storage; else my-entities) | `references/entities.md` |
| `get_entity` | Get entity detail (schema / columns) by entity URI | `references/entities.md` |
| `get_entity_online_ddl` | Query an RDS table's online DDL across vregions | `references/entities.md` |
| `list_workflows` | List schema-change workflows (my / by storage / by entity) | `references/workflows.md` |
| `get_workflow` | Get workflow detail + bound BITS pipeline + BPM tickets | `references/workflows.md` |
| `validate_ddl_change` | Validate a batch of CREATE/ALTER DDL + infer entity_mapping | `references/schema_change.md` |
| `create_schema_change` | (write) Publish a workflow on top of validated DDL (one workflow per batch) | `references/schema_change.md` |
| `approve_workflow_owner_gate` | (write) Approve the workflow's Owner-approval gate | `references/schema_change.md` |
| `advance_workflow_bpm_ticket` | (write) List or drive BPM tickets bound to the resource-deployment step | `references/schema_change.md` |
| `close_workflow` | (write) Terminate the workflow (cascades to BPM tickets) | `references/schema_change.md` |

**Read-only**: `list_storages`, `get_storage`, `get_storage_sync_channel`, `get_storage_sync_channel_detail`, `list_entities`, `get_entity`, `get_entity_online_ddl`, `list_workflows`, `get_workflow`, `validate_ddl_change`.

**Write actions** (all are two-phase: preview by default, pass `confirm=true` to apply):

- `update_storage_owners` — modify a storage's `owners` list. Auto-completes; no separate approval step.
- `create_schema_change` — publish a CREATE/ALTER TABLE DDL workflow.
- `approve_workflow_owner_gate` — approve the Owner-approval gate of a schema-change workflow as the current JWT user.
- `advance_workflow_bpm_ticket` — drive a BPM ticket bound to a workflow's resource-deployment step (Approve / Reject / postpone).
- `close_workflow` — terminate the entire EMS schema-change workflow (cascades to all bound BPM tickets). Use this — not BPM `op_key=stop` — when you want to actually cancel a workflow.

## 路由：按用户意图决定加载哪个 reference

模型应根据用户意图先选定 `action`，再加载对应文档：

| 想做的事 | 必读文件 |
|---|---|
| 查 storage / 改 storage owner | `references/storages.md` |
| 看一条 storage 的同步链路 / 某条 edge 的延迟、吞吐、子任务 | `references/sync_channels.md` |
| 查 entity（表）/ entity 列表 / RDS 表的在线 DDL | `references/entities.md` |
| 浏览 / 查询 schema-change workflow（含 pipeline + BPM 状态） | `references/workflows.md` |
| RDS 建表 / 改表 全流程：validate → publish → owner approve → BPM → close | `references/schema_change.md` |

> reference 文件在 skill 安装时已一并复制到本目录。请直接 read（`./references/<name>.md`），不要再尝试重新拉取。

## Quick Start

```bash
# List MY storages (mode defaults to 2 = owner; skill reads JWT username automatically, no owner param needed)
gdpa-cli run ems --session-id "$SESSION_ID" --input '{"action":"list_storages"}'

# Get storage detail — URI contains slashes; pass it un-escaped
gdpa-cli run ems --session-id "$SESSION_ID" --input '{
  "action": "get_storage",
  "uri": "tiktok/mysql/new_one_rds"
}'

# List tables / entities under an RDS storage
gdpa-cli run ems --session-id "$SESSION_ID" --input '{
  "action": "list_entities",
  "storage_uri": "tiktok/mysql/new_one_rds"
}'

# Storage sync channel topology — by URI (fast path) or by PSM (skill resolves once)
gdpa-cli run ems --session-id "$SESSION_ID" --input '{
  "action": "get_storage_sync_channel",
  "storage_uri": "tiktok/mysql/new_one_rds"
}'

# Workflow detail by id
gdpa-cli run ems --session-id "$SESSION_ID" --input '{
  "action": "get_workflow",
  "id": "119090688003"
}'

# RDS table change — full lifecycle (validate ⇒ publish ⇒ owner approve ⇒ drive BPM ⇒ close)
gdpa-cli run ems --session-id "$SESSION_ID" --input '{
  "action": "validate_ddl_change",
  "rds_uri": "tiktok/mysql/new_one_rds",
  "tables": [
    {
      "table_name": "foo",
      "ddl_sql": "CREATE TABLE foo (id BIGINT(20) UNSIGNED NOT NULL COMMENT '\''ID'\'', PRIMARY KEY (id)) ENGINE=INNODB CHARSET=utf8mb4"
    }
  ]
}'

gdpa-cli run ems --session-id "$SESSION_ID" --input '{
  "action": "create_schema_change",
  "rds_uri": "tiktok/mysql/new_one_rds",
  "tables": [
    {
      "table_name": "foo",
      "ddl_sql": "CREATE TABLE foo (id BIGINT(20) UNSIGNED NOT NULL, PRIMARY KEY (id)) ENGINE=INNODB CHARSET=utf8mb4"
    }
  ],
  "confirm": true
}'

# After create_schema_change returns workflow_id, drive the workflow:
gdpa-cli run ems --session-id "$SESSION_ID" --input '{"action":"approve_workflow_owner_gate","workflow_id":"<id>","confirm":true}'
gdpa-cli run ems --session-id "$SESSION_ID" --input '{"action":"advance_workflow_bpm_ticket","workflow_id":"<id>"}'

# Terminate the entire workflow (cancels all bound BPM tickets):
gdpa-cli run ems --session-id "$SESSION_ID" --input '{"action":"close_workflow","workflow_id":"<id>","confirm":true}'
```

完整参数与每个 action 的 preview / confirm 输出格式见对应 `references/<name>.md`。

## Parameters shared by all actions

| Param | Type | Required | Notes |
|-------|------|----------|-------|
| `action` | string | Yes | Action name (see the table above) |
| `target_addr` | string | No | Override the default `https://ent.tiktok-row.net` host (i18n staging only — never a BOE address) |

> ⚠️ 不同 workflow-相关 action 用了不同的参数名：`get_workflow` 收 `id`，而 `approve_workflow_owner_gate` / `advance_workflow_bpm_ticket` / `close_workflow` 收 `workflow_id`。这是按 "拿资源" vs "操作 workflow" 区分的；具体见 `references/workflows.md` 与 `references/schema_change.md`。

## URL Mapping Cheat-Sheet

| UI Page | Action to Use |
|--------|--------|
| `https://ent.tiktok-row.net/storage?mode=1` | `list_storages` |
| `https://ent.tiktok-row.net/storage_iac/detail?uri=...` | `get_storage` |
| `https://ent.tiktok-row.net/storage_iac/detail?activeTab=table&uri=...` | `list_entities` with `storage_uri=<uri>` |
| `https://ent.tiktok-row.net/storage_iac/detail?activeTab=dbSpec&uri=...` | `get_storage` (spec embedded in V3 storage detail) |
| `https://ent.tiktok-row.net/storage_iac/detail?syncNodeId=<src>->...&uri=<storage_uri>` | `get_storage_sync_channel_detail` (one edge) |
| `https://ent.tiktok-row.net/entity` | `list_entities` |
| `https://ent.tiktok-row.net/storage_schema/detail?uri=...` | `get_entity` |
| `https://ent.tiktok-row.net/workflow` | `list_workflows` |
| `https://ent.tiktok-row.net/storage_iac/detail?activeTab=workflow&uri=<storage_uri>` | `list_workflows` with `storage_uri=<uri>` |
| `https://ent.tiktok-row.net/entity/detail?uri=<entity_uri>` (Workflow tab) | `list_workflows` with `entity_uri=<uri>` |
| `https://ent.tiktok-row.net/workflow/detail/<id>` | `get_workflow` |
| `https://ent.tiktok-row.net/storage_schema/detail/edit_v3?uri=<entity_uri>` (DDL editor) | `validate_ddl_change` ⇒ `create_schema_change` |
| `https://ent.tiktok-row.net/workflow/detail/<id>` (Owner-approval gate) | `approve_workflow_owner_gate` |
| `https://ent.tiktok-row.net/workflow/detail/<id>` (Close Workflow button) | `close_workflow` |
| `https://bpm-i18n.tiktok-row.net/record/<ticket_id>` (BPM ticket bound to a workflow) | `advance_workflow_bpm_ticket` |

## Output Shape

Every call returns:

```json
{
  "success": true,
  "action": "<action>",
  "data": {
    "<echoed request params>": "...",
    "data": { "...": "real EMS payload" }
  }
}
```

On failure, `success` is `false`, `data` is `null`, and a human-readable `error` field is present.

### ⚠️ Important: EMS response envelope

All EMS APIs (including the `/sdp/v1/dts/*` proxied endpoints) return the HTTP body as a uniform envelope:

```json
{ "code": 0, "message": "", "data": { "...": "actual payload" } }
```

The skill forwards that entire `data` field to you **as-is (raw JSON)**. So to read the real returned object, always drill into `result.data.data` — not `result.data`. The outer `data` only echoes the request parameters for traceability, the real EMS payload is the inner `data`.

Typical fields inside the inner `data`:
- List APIs (`list_storages`, `list_entities`, `list_workflows`): `list` (array) + `page_info` (page_num / page_size / total). Some older endpoints use `items` / `total` at top-level of the inner data.
- Detail APIs (`get_storage`, `get_entity`, `get_workflow`): the resource object directly.
- `get_entity_online_ddl`: `ddl_list` keyed by vregion.
- `get_storage_sync_channel`: `edge_list` (array) + `intention_diff` + `config`.
- `get_storage_sync_channel_detail`: per-edge SDP detail — typically `lag` / `throughput` / `link` / `sub_tasks` (one entry per VDC inside src/dst VRegion). Forward-compat passthrough; do not rely on the exact shape.
