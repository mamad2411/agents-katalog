---
name: bytecloud-doc
description: Search ByteCloud Document Center (cloud.bytedance.net / cloud-boe.bytedance.net) knowledge base and retrieve full document content by doc_id — not via paas-gw. Use whenever the user wants ByteCloud docs, TCE/TCC/Neptune/BITS documentation, how-to guides on ByteCloud, knowledge base search, or full doc body by doc_id. Also trigger for cloud.bytedance.net documentation URLs, 「字节云文档」「文档中心」, or "how to do X on ByteCloud" questions even if the user does not name this agent.
---

> **session_id 传递**：若本次任务需要在多次 `gdpa-cli run` 之间串联 workflow 状态、日志或上下文，请复用同一个 `session_id`。如果当前 skill / Agent 已经提供了 `session_id`，**请直接复用，不要新建**。
>
> - **已有时优先复用**：不要重复执行 `create-session`。
> - **没有时再创建**：执行 `gdpa-cli create-session`。
> - **后续调用**：可以显式传 `--session-id <session_id>`，例如 `gdpa-cli run <agent> --session-id <session_id> --input '{...}'`。
> - **适用场景**：Base Workflow、BITS Dev Workflow、post-coding-verify 及其他依赖 Session 工作目录的场景需要持续复用；普通单次查询通常可以不传。

> **session_id 可选**：普通单次文档检索可以直接运行 `gdpa-cli run bytecloud-doc --session-id "$SESSION_ID" --input '{...}'`。
>
> 1. 如需把多次文档检索串到同一条排障/调研链路里，可先执行 `gdpa-cli create-session` → 得到 `session_id`
> 2. 后续命令显式复用：`gdpa-cli run bytecloud-doc --session-id <session_id> --input '{...}'`

# ByteCloud 文档中心（ByteCloud Doc）

通过 **ByteCloud Web 域名**调用文档开放接口（路径前缀 `/api/v1/cloud_developer/api/open/v1/...`），与 TCE Open Gateway 使用的站点一致：

| 环境 | 默认 `base_url` |
|------|------------------|
| CN 生产 | `https://cloud.bytedance.net` |
| CN BOE | `https://cloud-boe.bytedance.net` |

**不要**默认使用 `paas-gw*.byted.org`；仅在自行对接旧网关并需要 `domain` 头时，再在 API Client 层使用 `WithDomain()`（Agent 侧已按 Web 路径调用，一般不需要）。

---

## 输入（JSON，`--input`）

顶层字段均为字符串，除非注明为数组。

| 字段 | 必填 | 说明 |
|------|------|------|
| `action` | 是 | `knowledge_search` 或 `get_document` |
| `query` | 搜库时必填 | 自然语言检索语句 |
| `doc_id` | 读正文时必填 | 文档 ID（可从 `knowledge_search` 结果的 `doc_id` 或文档 URL 路径末段取得） |
| `jwt` | 否 | 个人身份 JWT（`x-jwt-token`），覆盖内部自动获取 |
| `token` | 否 | 服务账号 Bearer token，覆盖内部自动获取 |
| `site` | 否 | 站点简写，见下表；与 `target_addr` 二选一（`target_addr` 优先） |
| `target_addr` | 否 | 完整根 URL（含 scheme），覆盖 `site` 与默认环境 |
| `product_ids` | 否 | 字符串数组，只搜指定产品（如 `tce`、`bits`） |
| `ignore_product_ids` | 否 | 字符串数组，排除产品 |

### `site` 取值

| `site` | 解析为 `base_url` |
|--------|---------------------|
| 省略、`auto`、`default` | 按运行环境：`BOE` → cloud-boe，否则 → cloud 生产 |
| `cn`、`china`、`china-north`、`prod`、`production` | `https://cloud.bytedance.net` |
| `boe`、`china-boe`、`dev` | `https://cloud-boe.bytedance.net` |

未知 `site` 会在校验阶段报错；请改用上表关键字或直接使用 `target_addr`。

---

## 输出（stdout 侧结构化结果）

Agent 将结果写入会话的 `Results["bytecloud-doc"]` 与 `_final_result`，为 JSON 对象。

### 成功（`success: true`）

公共字段：

| 字段 | 类型 | 说明 |
|------|------|------|
| `success` | bool | `true` |
| `action` | string | `knowledge_search` 或 `get_document` |
| `base_url` | string | 本次请求实际使用的根地址（与上表一致） |

**`knowledge_search` 额外字段：**

| 字段 | 类型 | 说明 |
|------|------|------|
| `query` | string | 检索语句 |
| `total` | number | 命中总数（服务端返回） |
| `items` | array | 每条含 `title`、`url`、`content`、`score`、`doc_id`、`product_id` |

**`get_document` 额外字段：**

| 字段 | 类型 | 说明 |
|------|------|------|
| `doc_id` | string | 请求的文档 ID |
| `document` | object | 含 `title`、`content`、`content_html`、`doc_url`、`product_id`、`language`、`doc_created_at`、`doc_updated_at`、`publisher`、`creator`、`pv`、`lark_url`、`breadcrumbs`（数组，可选） |

### 失败（`success: false`）

| 字段 | 说明 |
|------|------|
| `success` | `false` |
| `action` | 请求的 `action`（若已通过校验） |
| `error` | 人类可读错误信息（参数缺失、未知 `site`、HTTP/API 错误等） |

---

## Actions 与示例

### `knowledge_search`

```bash
gdpa-cli run bytecloud-doc --session-id <sid> --input '{
  "action": "knowledge_search",
  "query": "tce如何扩容",
  "site": "cn"
}'
```

可选：`product_ids`、`ignore_product_ids`（JSON 字符串数组）。

### `get_document`

```bash
gdpa-cli run bytecloud-doc --session-id <sid> --input '{
  "action": "get_document",
  "doc_id": "abc123",
  "site": "boe"
}'
```

---

## 鉴权说明

Agent 默认通过 `jwtutil.GetCNJwt()` 内部自动获取 CN JWT，无需手动传入鉴权参数。

如需覆盖，可通过 `jwt` 或 `token` 字段传入自定义凭证：
1. 同时传 `jwt` 与 `token` 时优先走 `jwt`。
2. 若内部自动获取失败，请先执行 `gdpa-cli login cn`。

---

## 典型工作流

1. `knowledge_search` 获取片段与 `doc_id`、`score`。
2. 需要全文时用 `get_document` + 上一步的 `doc_id`。
3. 展示时优先 Markdown `content`；需渲染可用 `content_html`。

---

## 与 API Client 开发者的说明

- 默认 `pkg/devflow-api-clients/impl/bytecloud_doc` 使用 **cloud.bytedance.net** 系域名；IDL 中 RPC 路径已含 `cloud_developer` 前缀。
- 若仍对接 **paas-gw**，可额外传入 `bytecloud_doc.WithDomain()`，与默认 Web 路径二选一，勿混用重复路由。
