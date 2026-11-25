---
name: tos
description: Query TOS (Object Storage) via ByteCloud gateway — list favorite/viewable buckets, list objects in a bucket, and get download URLs. Use whenever the user wants to browse TOS buckets, list objects in a bucket, get download links for TOS objects, or mentions TOS/object storage/Bucket. Supports China-North, China-BOE, Singapore-Central, US-East and other ByteCloud regions.
---

> **session_id 传递**：若本次任务需要在多次 `gdpa-cli run` 之间串联 workflow 状态、日志或上下文，请复用同一个 `session_id`。如果当前 skill / Agent 已经提供了 `session_id`，**请直接复用，不要新建**。
>
> - **已有时优先复用**：不要重复执行 `create-session`。
> - **没有时再创建**：执行 `gdpa-cli create-session`。
> - **后续调用**：可以显式传 `--session-id <session_id>`，例如 `gdpa-cli run <agent> --session-id <session_id> --input '{...}'`。
> - **适用场景**：Base Workflow、BITS Dev Workflow、post-coding-verify 及其他依赖 Session 工作目录的场景需要持续复用；普通单次查询通常可以不传。

> **session_id 可选**：普通单次 TOS 查询可以直接运行 `gdpa-cli run tos --session-id "$SESSION_ID" --input '{...}'`。
>
> - **需要串联一组查询或排障链路时**：先执行 `gdpa-cli create-session` 获取 session_id，再在后续命令中显式传入 `--session-id`。
> - **复用**：若当前会话中已经创建过 session_id，直接复用即可，无需重复创建。

# TOS Agent

Query TOS (Object Storage) via ByteCloud gateway — list buckets, list objects, and get download URLs.

> **When to Use**: Browse TOS buckets, list objects in a bucket, get download links for TOS objects.

## Quick Start

```bash
# List favorite buckets (default: China-North)
gdpa-cli run tos --session-id "$SESSION_ID" --input '{
  "action": "list_favorite_buckets"
}'

# List all viewable buckets in Singapore
gdpa-cli run tos --session-id "$SESSION_ID" --input '{
  "action": "list_viewable_buckets",
  "vregion": "sg"
}'

# List objects in a bucket (China-BOE)
gdpa-cli run tos --session-id "$SESSION_ID" --input '{
  "action": "list_objects",
  "bucket_id": "70300593",
  "vregion": "boe"
}'

# Get download URL for an object (US-East)
gdpa-cli run tos --session-id "$SESSION_ID" --input '{
  "action": "get_download_url",
  "bucket_name": "binary-tool",
  "object_key": "data.tgz",
  "vregion": "us"
}'
```

## Input Parameters

### Required

| Parameter | Type | Description |
|-----------|------|-------------|
| `action` | string | Action type: `list_favorite_buckets`, `list_viewable_buckets`, `list_objects`, `get_download_url` |

### Action-Specific Required Parameters

| Action | Required Parameters | Description |
|--------|---------------------|-------------|
| `list_favorite_buckets` | (none) | List user's favorited buckets |
| `list_viewable_buckets` | (none) | List all buckets user can view |
| `list_objects` | `bucket_id` | List objects in a bucket (bucket_id is numeric) |
| `get_download_url` | `object_key` + (`bucket_name` or `bucket_id`) | Get download URL for an object |

### Optional

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `vregion` | string | `China-North` | VRegion: `China-North`, `China-BOE`, `Singapore-Central`, `US-East`, etc. Aliases: `cn`, `boe`, `sg`, `us` |
| `page_num` | int | `0` | Page number for bucket list (0-indexed) |
| `page_size` | int | `20` | Page size for bucket list |
| `prefix` | string | `""` | Object key prefix filter for `list_objects` |
| `limit` | int | `20` | Max objects per page for `list_objects` |
| `lastkey` | string | `""` | Pagination cursor for `list_objects` (use last object's key from previous page) |

## Actions

### 1. list_favorite_buckets

获取用户收藏的 TOS Bucket 列表。

```bash
gdpa-cli run tos --session-id "$SESSION_ID" --input '{
  "action": "list_favorite_buckets",
  "page_num": 0,
  "page_size": 20
}'
```

**Output**:
```json
{
  "success": true,
  "action": "list_favorite_buckets",
  "vregion": "China-North",
  "data": {
    "records": [
      {
        "id": 10157,
        "bucket_name": "profile",
        "creator": "zhangsan",
        "storage_type": "standard",
        "create_time": 1703588533,
        "region": "China-North/CN-3DC/Default/OwnBuild",
        "public": "internal",
        "status": true,
        "favor": true
      }
    ],
    "total_item_num": 2,
    "total_page_num": 1,
    "cur_page_num": 0,
    "has_next": false,
    "has_prev": false,
    "item_per_page": 20
  }
}
```

### 2. list_viewable_buckets

获取用户可查看的所有 TOS Bucket 列表（包含非收藏的）。

```bash
gdpa-cli run tos --session-id "$SESSION_ID" --input '{
  "action": "list_viewable_buckets",
  "vregion": "China-North"
}'
```

响应格式与 `list_favorite_buckets` 相同。

### 3. list_objects

获取指定 Bucket 中的对象列表。

```bash
# Basic listing
gdpa-cli run tos --session-id "$SESSION_ID" --input '{
  "action": "list_objects",
  "bucket_id": "20006480"
}'

# With prefix filter
gdpa-cli run tos --session-id "$SESSION_ID" --input '{
  "action": "list_objects",
  "bucket_id": "20006480",
  "prefix": "logs/"
}'

# Pagination: use lastkey from previous response
gdpa-cli run tos --session-id "$SESSION_ID" --input '{
  "action": "list_objects",
  "bucket_id": "20006480",
  "limit": 10,
  "lastkey": "some-object-key"
}'
```

**Output**:
```json
{
  "success": true,
  "action": "list_objects",
  "vregion": "China-North",
  "data": {
    "has_more": false,
    "objects": [
      {
        "key": "data.tgz",
        "size": 5442,
        "name": "data.tgz",
        "directory": false,
        "timestamp": 1650268744
      },
      {
        "key": "des-rpc-tool",
        "size": 16699188,
        "name": "des-rpc-tool",
        "directory": false,
        "timestamp": 1633687305
      }
    ]
  }
}
```

**Pagination**: When `has_more` is `true`, pass the last object's `key` as `lastkey` in the next request.

### 4. get_download_url

获取对象的下载链接。通过 `GetBackendConfig` API 获取下载 URL 前缀后拼接构造。

- `download_url`（外网直接下载）：需要 `bucket_name`，通过 `object_download_url` 前缀拼接
- `og_download_url`（内网 API 下载）：需要 `bucket_id`，通过 `backend_domain` + API 端点构造

```bash
# 获取外网下载链接（需要 bucket_name）
gdpa-cli run tos --session-id "$SESSION_ID" --input '{
  "action": "get_download_url",
  "bucket_name": "binary-tool",
  "object_key": "data.tgz"
}'

# 获取内网下载链接（需要 bucket_id）
gdpa-cli run tos --session-id "$SESSION_ID" --input '{
  "action": "get_download_url",
  "bucket_id": "20006480",
  "object_key": "data.tgz"
}'

# 同时获取两种下载链接
gdpa-cli run tos --session-id "$SESSION_ID" --input '{
  "action": "get_download_url",
  "bucket_name": "binary-tool",
  "bucket_id": "20006480",
  "object_key": "data.tgz"
}'
```

**Output**:
```json
{
  "success": true,
  "action": "get_download_url",
  "vregion": "China-North",
  "data": {
    "bucket_name": "binary-tool",
    "object_key": "data.tgz",
    "download_url": "https://tosv.byted.org/obj/binary-tool/data.tgz",
    "og_download_url": "https://new-tos.byted.org/api/v1/bucket/20006480/object/op/download?key=data.tgz"
  }
}
```

- `download_url`: 外网临时域名下载链接（`object_download_url` 前缀 + `/{bucket_name}/{object_key}`），需要 `bucket_name` 参数
- `og_download_url`: 内网 API 下载链接（`backend_domain` + `/api/v1/bucket/{bucket_id}/object/op/download?key={object_key}`），需要 `bucket_id` 参数，需要登录态

## VRegion Mapping

| VRegion | Aliases | JWT Type | Description |
|---------|---------|----------|-------------|
| `China-North` (default) | `cn`, `china` | CN | 中国北方 |
| `China-BOE` | `boe`, `cn-boe` | CN | 中国 BOE 环境 |
| `US-BOE` | `boei18n`, `boe-i18n`, `us-boe` | CN | 国际化 BOE 环境 |
| `Singapore-Central` | `sg`, `singapore` | i18n | 新加坡 |
| `US-East` | `us`, `i18n` | i18n | 美东 |

## Typical Workflow

1. **发现 Bucket**：先调用 `list_favorite_buckets` 或 `list_viewable_buckets` 获取 bucket 列表，记录 `id` 和 `bucket_name`
2. **浏览对象**：使用 `list_objects` + `bucket_id` 查看对象列表
3. **获取下载链接**：使用 `get_download_url` + `bucket_name` + `object_key` 获取下载 URL

## Error Handling

| Error | Cause | Solution |
|-------|-------|----------|
| `action parameter is required` | Missing action | Add `action` parameter |
| `bucket_id parameter is required` | Missing bucket_id for list_objects | Add `bucket_id` parameter |
| `bucket_name parameter is required` | Missing bucket_name for get_download_url | Add `bucket_name` parameter |
| `object_key parameter is required` | Missing object_key for get_download_url | Add `object_key` parameter |
| `authentication failed` | JWT token issue | Check network and login status (`gdpa-cli login`) |
| `TOS error (status=xxx)` | TOS backend error | Check parameters, permissions, or bucket_id |

## Notes

- **bucket_id vs bucket_name**: `list_objects` uses numeric `bucket_id` (from bucket list response); `get_download_url` uses `bucket_name` for `download_url` and `bucket_id` for `og_download_url`
- **Download URL construction**: `download_url` = `{object_download_url}/{bucket_name}/{object_key}`; `og_download_url` = `{backend_domain}/api/v1/bucket/{bucket_id}/object/op/download?key={object_key}`
- **Object key encoding**: For object keys containing special characters in `og_download_url`, they are automatically URL-encoded as query parameter values
- **Pagination**: Use `lastkey` cursor-based pagination for `list_objects`; use `page_num`/`page_size` for bucket lists
