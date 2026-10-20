---
name: abase
description: Query Abase NoSQL data via ByteCloud gateway across multiple regions. Use whenever the user wants to query Abase data, list Abase tables, search Abase namespaces, check key values, or mentions Abase/NoSQL/KV store. Supports Singapore, US, China, BOE, and EU environments. Users can provide just a namespace name or PSM without knowing the cluster.
---

> **session_id 传递**：若本次任务需要在多次 `gdpa-cli run` 之间串联 workflow 状态、日志或上下文，请复用同一个 `session_id`。如果当前 skill / Agent 已经提供了 `session_id`，**请直接复用，不要新建**。
>
> - **已有时优先复用**：不要重复执行 `create-session`。
> - **没有时再创建**：执行 `gdpa-cli create-session`。
> - **后续调用**：可以显式传 `--session-id <session_id>`，例如 `gdpa-cli run <agent> --session-id <session_id> --input '{...}'`。
> - **适用场景**：Base Workflow、BITS Dev Workflow、post-coding-verify 及其他依赖 Session 工作目录的场景需要持续复用；普通单次查询通常可以不传。

# Abase Agent

Query Abase NoSQL data via ByteCloud gateway.

> **When to Use**: Query Abase key-value data, list tables in a namespace, search namespace info, or check Abase data across Singapore, US, China, BOE, and EU environments.

## Quick Start

```bash
# Search namespace by name (auto-discovers cluster)
gdpa-cli run abase --session-id "$SESSION_ID" --input '{
  "action": "search_namespace",
  "search": "entity_storage",
  "vregion": "sg"
}'

# Search namespace by PSM
gdpa-cli run abase --session-id "$SESSION_ID" --input '{
  "action": "search_namespace",
  "search": "bytedance.abase2.entity_storage",
  "vregion": "sg"
}'

# List tables — by namespace (auto-resolve cluster)
gdpa-cli run abase --session-id "$SESSION_ID" --input '{
  "action": "list_tables",
  "namespace": "entity_storage",
  "vregion": "sg"
}'

# List tables — by PSM (auto-resolve cluster + namespace)
gdpa-cli run abase --session-id "$SESSION_ID" --input '{
  "action": "list_tables",
  "psm": "bytedance.abase2.ies_item_attr",
  "vregion": "cn"
}'

# List tables — by PSM + cluster (auto-resolve namespace)
gdpa-cli run abase --session-id "$SESSION_ID" --input '{
  "action": "list_tables",
  "psm": "bytedance.abase2.ies_item_attr",
  "cluster": "common8",
  "vregion": "cn"
}'

# List tables — explicit cluster + namespace (no resolve)
gdpa-cli run abase --session-id "$SESSION_ID" --input '{
  "action": "list_tables",
  "cluster": "global10",
  "namespace": "entity_storage",
  "vregion": "sg"
}'

# Query — by namespace (auto-resolve cluster)
gdpa-cli run abase --session-id "$SESSION_ID" --input '{
  "action": "query",
  "namespace": "entity_storage",
  "table": "sandbox",
  "command": "get",
  "inputs": "test_key",
  "vregion": "sg"
}'

# Query — by PSM (auto-resolve cluster + namespace)
gdpa-cli run abase --session-id "$SESSION_ID" --input '{
  "action": "query",
  "psm": "bytedance.abase2.entity_storage",
  "table": "sandbox",
  "command": "get",
  "inputs": "test_key",
  "vregion": "sg"
}'

# Query — explicit cluster + namespace (no resolve)
gdpa-cli run abase --session-id "$SESSION_ID" --input '{
  "cluster": "common8",
  "namespace": "ies_item_attr",
  "table": "item_attr",
  "command": "get",
  "inputs": "my_key",
  "vregion": "cn"
}'
```

## Input Parameters

### Namespace Identification

The agent always calls SearchNamespaces API to resolve `cluster`, `namespace`, and `psm`. The resolved PSM is automatically used as the `consul` parameter for API calls.

| Mode | Parameters | What the agent resolves |
|------|-----------|------------------------|
| **By namespace** | `namespace` | Resolves `cluster` + `psm` from namespace name |
| **By PSM** | `psm` | Resolves `cluster` + `namespace` from PSM |
| **Both** | `namespace` + `cluster`, or `psm` + `cluster` | Still resolves to obtain `psm` (cluster may be overridden by resolved value) |

### Required for `query` action

| Parameter | Type | Description |
|-----------|------|-------------|
| `table` | string | Table name within the namespace |
| `command` | string | Abase command (`get`, `hget`, `hgetall`, `set`, `del`, etc.) |
| `inputs` | string | Command input (key name) |

### Required for all actions

| Parameter | Type | Description |
|-----------|------|-------------|
| `vregion` | string | Target VRegion (required). See supported list below. Aliases supported (e.g. `sg`, `cn`, `us`) |

### Optional

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `action` | string | `query` | Action type: `query`, `list_tables`, or `search_namespace` |
| `original_mode` | bool | `false` | Whether to use original mode |

## Actions

### `search_namespace` — Search Namespace Info

Find Abase namespace details by name or PSM. Returns cluster, owner, PSM, and other metadata.

```bash
gdpa-cli run abase --session-id "$SESSION_ID" --input '{"action": "search_namespace", "search": "entity_storage", "vregion": "sg"}'
gdpa-cli run abase --session-id "$SESSION_ID" --input '{"action": "search_namespace", "search": "bytedance.abase2.entity_storage", "vregion": "cn"}'
```

### `list_tables` — List Tables in Namespace

```bash
# By namespace only (auto-resolve cluster)
gdpa-cli run abase --session-id "$SESSION_ID" --input '{"action": "list_tables", "namespace": "entity_storage", "vregion": "sg"}'

# By PSM only (auto-resolve cluster + namespace)
gdpa-cli run abase --session-id "$SESSION_ID" --input '{"action": "list_tables", "psm": "bytedance.abase2.ies_item_attr", "vregion": "cn"}'

# By PSM + cluster (auto-resolve namespace, use given cluster)
gdpa-cli run abase --session-id "$SESSION_ID" --input '{"action": "list_tables", "psm": "bytedance.abase2.ies_item_attr", "cluster": "common8", "vregion": "cn"}'

# Explicit cluster + namespace (no auto-resolve)
gdpa-cli run abase --session-id "$SESSION_ID" --input '{"action": "list_tables", "cluster": "common8", "namespace": "ies_item_attr", "vregion": "cn"}'
```

### `query` — Query Key-Value Data

```bash
# By namespace only (auto-resolve cluster)
gdpa-cli run abase --session-id "$SESSION_ID" --input '{"action": "query", "namespace": "entity_storage", "table": "sandbox", "command": "get", "inputs": "my_key", "vregion": "sg"}'

# By PSM only (auto-resolve cluster + namespace)
gdpa-cli run abase --session-id "$SESSION_ID" --input '{"action": "query", "psm": "bytedance.abase2.entity_storage", "table": "sandbox", "command": "get", "inputs": "my_key", "vregion": "sg"}'

# By PSM + cluster (auto-resolve namespace, use given cluster)
gdpa-cli run abase --session-id "$SESSION_ID" --input '{"action": "query", "psm": "bytedance.abase2.ies_item_attr", "cluster": "common8", "table": "item_attr", "command": "get", "inputs": "my_key", "vregion": "cn"}'

# Explicit cluster + namespace (no auto-resolve)
gdpa-cli run abase --session-id "$SESSION_ID" --input '{"cluster": "common8", "namespace": "ies_item_attr", "table": "item_attr", "command": "get", "inputs": "my_key", "vregion": "cn"}'
```

## Supported VRegions

| VRegion | Aliases | Gateway | JWT |
|---------|---------|---------|-----|
| `Singapore-Central` (default) | `sg` | cloud.tiktok-row.net | i18n |
| `US-East` | `us`, `i18n` | cloud.tiktok-row.net | i18n |
| `China-North` | `cn`, `china` | cloud.bytedance.net | CN |
| `China-East` | `chinaeast` | cloud.bytedance.net | CN |
| `China-BOE` | `boe`, `cn-boe` | cloud-boe.bytedance.net | CN |
| `US-BOE` | `boei18n`, `boe-i18n` | cloud-boei18n.bytedance.net | i18n |
| `EU-TTP2` | `eu-ttp2`, `euttp2` | bc-iedt-gw.tiktok-eu.net | i18n |
| `US-EastRed` | `us-eastred`, `useastred` | bc-iedt-gw.tiktok-eu.net | i18n |

## Output Format

### Search Namespace Result

```json
{
  "success": true,
  "action": "search_namespace",
  "vregion": "Singapore-Central",
  "cluster": "global10",
  "namespace": "entity_storage",
  "data": {
    "id": 2517170,
    "name": "entity_storage",
    "cluster_name": "global10",
    "psm": "bytedance.abase2.entity_storage",
    "owner": "...",
    "service_tree_path": "..."
  }
}
```

### Query Result

```json
{
  "success": true,
  "action": "query",
  "vregion": "Singapore-Central",
  "cluster": "global10",
  "namespace": "entity_storage",
  "data": {
    "results": [...],
    "raw": "..."
  }
}
```

### List Tables Result

```json
{
  "success": true,
  "action": "list_tables",
  "vregion": "China-North",
  "cluster": "common8",
  "namespace": "ies_item_attr",
  "data": {
    "tables": [...],
    "table_count": 5
  }
}
```

## Error Handling

| Error | Cause | Solution |
|-------|-------|----------|
| `namespace (or psm/search) parameter is required` | No namespace identifier provided | Add `namespace`, `psm`, or `search` parameter |
| `namespace not found for "xxx"` | SearchNamespaces did not find exact match | Verify namespace name or PSM spelling |
| `table parameter is required` | Missing table name for query | Add `table` parameter |
| `command parameter is required` | Missing Abase command | Add `command` (get, hget, etc.) |
| `invalid vregion` | Unknown VRegion | Check supported VRegion list above |
| `authentication failed` | JWT token issue | Run `gdpa-cli login` |

## Notes

- **Always resolves**: The agent always calls SearchNamespaces API to obtain `cluster`, `namespace`, and `psm`. This ensures the `consul` parameter (PSM) is always available for API calls. Adds ~1-2s latency.
- **PSM auto-detection**: If the `namespace` parameter starts with `abase_`, `bytedance.abase2.`, or `bytedance.abase.`, the agent automatically treats it as a PSM. For example, passing `namespace: "abase_tiktok_penalty_center_sg_alisg"` is equivalent to passing `psm: "abase_tiktok_penalty_center_sg_alisg"`.
- **PSM formats**: `entity_storage`, `abase_entity_storage`, `bytedance.abase2.entity_storage`, and `bytedance.abase.entity_storage` all work as search keys. PSM prefixes are automatically stripped before querying the API.
- **Auto-derived parameters**: `dc` (data center) is derived from `vregion` (e.g. Singapore-Central → sg1, US-East → maliva); `consul` is derived from the resolved PSM. Users do not need to specify either.
- **Default action**: If `action` is not specified, defaults to `query`.
- **CN regions**: China-North/China-East/China-BOE automatically set `x-bcgw-tenant-id: bytedance`.
