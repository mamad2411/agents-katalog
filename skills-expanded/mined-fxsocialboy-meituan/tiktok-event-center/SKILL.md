---
name: tiktok-event-center
description: |
  查询 TikTok Watchdog 事件中心（事件仓库）：按事件 DSL 搜索变更事件，支持时间窗、分页与聚合摘要。
  默认访问 `https://watchdog-i18n.bytedance.net`，使用 `POST /api/v1/events/search`。
---

> **session_id 传递**：若本次任务需要在多次 `gdpa-cli run` 之间串联 workflow 状态、日志或上下文，请复用同一个 `session_id`。如果当前 skill / Agent 已经提供了 `session_id`，**请直接复用，不要新建**。
>
> - **已有时优先复用**：不要重复执行 `create-session`。
> - **没有时再创建**：执行 `gdpa-cli create-session`。
> - **后续调用**：可以显式传 `--session-id <session_id>`，例如 `gdpa-cli run <agent> --session-id <session_id> --input '{...}'`。
> - **适用场景**：Base Workflow、BITS Dev Workflow、post-coding-verify 及其他依赖 Session 工作目录的场景需要持续复用；普通单次查询通常可以不传。

# TikTok 事件中心（Watchdog 事件仓库）

## 鉴权

需要本机 **I18N 或对应区域** 的 ByteCloud JWT（与 `gdpa-cli login` 一致）。请求头携带 `x-jwt-token`，由工具自动注入，勿在对话中粘贴 token。

## Action

### `search`

在事件仓库中检索事件。

| 参数 | 必填 | 说明 |
|------|------|------|
| `action` | 是 | 固定为 `search` |
| `query` | 是 | 查询 DSL，例如 `operators:laihongquan`、`source:faas` |
| `vregion` | 否 | 用于选择 JWT（默认 `Singapore-Central` → I18N JWT） |
| `base_url` | 否 | 默认 `https://watchdog-i18n.bytedance.net`；仅允许 **https** 且主机名为 `watchdog-i18n.bytedance.net`（可带 path，会被忽略），禁止自定义端口/用户信息与未白名单域名 |
| `time_start` / `time_end` | 否 | RFC3339，如 `2026-04-15T16:01:07+08:00`；未传时按 `duration_days` 回推 |
| `duration_days` | 否 | 未指定 `time_start` 时，从 `time_end`（默认当前时间）向前推的天数，默认 `7`，最大 `366` |
| `page_size` | 否 | 列表行数，默认 `30`，最大 `100`；`0` 表示只要聚合/统计、不要 `items` 行 |
| `stats_only` | 否 | `true` 时强制 `page_size=0`，Facet 默认 `["Source"]` |
| `cursor` | 否 | 下一页：填入上一页响应 `data.page_info.end_cursor`（写入请求 `pager.begin_cursor`） |
| `pager` | 否 | 高级用法：对象会与默认 `pager` 合并（可覆盖字段） |
| `aggregate` | 否 | 高级用法：覆盖默认聚合块 |
| `facet_keys` | 否 | 数组，覆盖默认（列表模式默认为空数组） |
| `contexts` | 否 | 默认 `[]` |
| `timeout_ms` | 否 | HTTP 超时，默认 `60000` |

## 响应摘要

成功时 `data` 主要字段：

- `total`：命中总数
- `page_info`：`begin_cursor` / `end_cursor` / `has_next_page` / `has_previous_page`
- `items`：精简后的记录列表（`record.id`、`title`、`action`、`source`、`status`、`started_at`、`ticket_url`、`tags` 等；其中 `tags` 会按 `key:value` 转成 `map[string][]string`；`src` / `attributes` 过长会截断）
- `item_count`：本页条数
- `aggr` / `metrics`：与页面一致的聚合信息（若请求包含 facet）

## 示例

```json
{
  "action": "search",
  "query": "operators:laihongquan",
  "duration_days": 7,
  "page_size": 30
}
```

下一页：

```json
{
  "action": "search",
  "query": "operators:laihongquan",
  "cursor": "<上一页返回的 data.page_info.end_cursor>",
  "page_size": 30
}
```

仅要统计、不拉明细行：

```json
{
  "action": "search",
  "query": "operators:laihongquan",
  "stats_only": true
}
```

## 限制

- 仅封装只读搜索，不写事件。
- 事件 DSL 语法与 Watchdog 事件探索页一致，详见站内帮助文档。
