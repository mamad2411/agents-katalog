---
name: bytedoc-query
description: Query ByteDoc (MongoDB) databases via ByteCloud Gateway — execute MongoDB find queries on collections across Singapore-Central, US-East, China-North, and China-BOE regions. Use whenever the user wants to query a ByteDoc/MongoDB database, check collection data, run MongoDB find queries, look up documents in ByteDoc, or mentions ByteDoc/bytedoc/MongoDB queries via ByteCloud. Also trigger when the user needs to inspect data in a ByteDoc database, verify document contents, debug data issues by querying MongoDB collections, or wants to run web_query against a ByteDoc database. Supports both CN (cloud.bytedance.net) and I18N (bc-*-gw.tiktok-row.net) gateways. This is read-only and executes find queries only.
---

> **session_id 传递**：若本次任务需要在多次 `gdpa-cli run` 之间串联 workflow 状态、日志或上下文，请复用同一个 `session_id`。如果当前 skill / Agent 已经提供了 `session_id`，**请直接复用，不要新建**。
>
> - **已有时优先复用**：不要重复执行 `create-session`。
> - **没有时再创建**：执行 `gdpa-cli create-session`。
> - **后续调用**：可以显式传 `--session-id <session_id>`，例如 `gdpa-cli run <agent> --session-id <session_id> --input '{...}'`。
> - **适用场景**：Base Workflow、BITS Dev Workflow、post-coding-verify 及其他依赖 Session 工作目录的场景需要持续复用；普通单次查询通常可以不传。

# ByteDoc Query Agent

Query ByteDoc (MongoDB) databases through the ByteCloud Gateway.

> **When to Use**: Query MongoDB collections in ByteDoc databases, inspect document data, or run find queries across regions.

## Quick Start

```bash
# Query a collection (default: Singapore-Central)
gdpa-cli run bytedoc-query --session-id "$SESSION_ID" --input '{
  "database": "treco_llm_core",
  "collection": "llm_core_task_test",
  "query": "find()"
}'

# Query with filter
gdpa-cli run bytedoc-query --session-id "$SESSION_ID" --input '{
  "database": "treco_llm_core",
  "collection": "llm_core_task_test",
  "query": "find({\"status\": \"active\"})",
  "limit": 10
}'

# Query in US-East region
gdpa-cli run bytedoc-query --session-id "$SESSION_ID" --input '{
  "database": "my_database",
  "collection": "my_collection",
  "query": "find()",
  "vregion": "US-East"
}'
```

## Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `database` | string | Yes | ByteDoc database name (e.g. `treco_llm_core`) |
| `collection` | string | Yes | Collection name (e.g. `llm_core_task_test`) |
| `query` | string | No | MongoDB query string (default: `find()`) |
| `vregion` | string | No | VRegion (default: `Singapore-Central`) |
| `limit` | int | No | Max number of results to return (default: no limit) |
| `psm` | string | No | PSM for resource schema (default: `toutiao.bytedoc_platform.cloud_api`) |

## VRegion Mapping

| VRegion | Aliases | Gateway | x-bcgw-vregion | JWT |
|---------|---------|---------|----------------|-----|
| `Singapore-Central` | `sg`, `singapore` | `bc-sgdt-gw.tiktok-row.net` | SGALI | i18n |
| `US-East` | `us`, `useast`, `i18n` | `bc-useastdt-gw.tiktok-row.net` | MVAALI | i18n |
| `China-North` | `cn`, `china` | `cloud.bytedance.net` | — | cn |
| `China-BOE` | `boe`, `cn-boe` | `cloud-boe.bytedance.net` | — | cn |

## Output Format

### Successful Query

```json
{
  "success": true,
  "database": "treco_llm_core",
  "collection": "llm_core_task_test",
  "query": "find()",
  "vregion": "Singapore-Central",
  "data": [ ... ],
  "count": 42
}
```

### Query Error

```json
{
  "success": false,
  "database": "treco_llm_core",
  "collection": "llm_core_task_test",
  "error": "error message"
}
```

## Examples

### Query All Documents

```bash
gdpa-cli run bytedoc-query --session-id "$SESSION_ID" --input '{"database": "treco_llm_core", "collection": "llm_core_task_test"}'
```

### Query with MongoDB Filter

```bash
gdpa-cli run bytedoc-query --session-id "$SESSION_ID" --input '{"database": "treco_llm_core", "collection": "llm_core_task_test", "query": "find({\"status\": \"active\"})", "limit": 5}'
```

### Query US-East Region

```bash
gdpa-cli run bytedoc-query --session-id "$SESSION_ID" --input '{"database": "my_db", "collection": "my_col", "query": "find()", "vregion": "us"}'
```

### Query China-North Region

```bash
gdpa-cli run bytedoc-query --session-id "$SESSION_ID" --input '{"database": "my_db", "collection": "my_col", "query": "find()", "vregion": "cn"}'
```

### Query China-BOE Region

```bash
gdpa-cli run bytedoc-query --session-id "$SESSION_ID" --input '{"database": "my_db", "collection": "my_col", "query": "find()", "vregion": "boe"}'
```

## Error Handling

| Error | Cause | Solution |
|-------|-------|----------|
| `database parameter is required` | Missing database name | Add `database` parameter |
| `collection parameter is required` | Missing collection name | Add `collection` parameter |
| `vregion "xxx" is not supported` | Unsupported region | Use `sg`, `us`, `cn`, or `boe` |
| `authentication failed` | JWT token error | Check login status with `gdpa-cli login i18n` (SG/US) or `gdpa-cli login` (CN) |
| `code != 0` | API returned error | Check database/collection name and permissions |

## Notes

- **Default VRegion**: Singapore-Central. Use `vregion` to query different regions.
- **Read-Only**: Only find/query operations are supported, no insert/update/delete.
- **Default Query**: If `query` is not provided, defaults to `find()` which returns all documents.
- **Resource Schema**: The `row_og_required_schema` is auto-constructed from database/collection/psm.
- **Data Format**: Response `data` may be a JSON string — the agent parses it for readability.
