---
name: bytees
description: Run Elasticsearch DSL queries on ByteES clusters across Singapore-Central, US-East, US-EastRed, EU-TTP2, US-TTP, US-TTP2. Uses Kibana Console Proxy for non-TTP regions and DataQ for TTP regions. Use whenever the user wants to query ByteES, run an ES search, check ES index documents, inspect ES cluster data, or mentions ByteES / Elasticsearch / Kibana dev tools. Accepts raw ES DSL body as string or JSON object.
---

> **session_id 传递**：若本次任务需要在多次 `gdpa-cli run` 之间串联 workflow 状态、日志或上下文，请复用同一个 `session_id`。如果当前 skill / Agent 已经提供了 `session_id`，**请直接复用，不要新建**。
>
> - **已有时优先复用**：不要重复执行 `create-session`。
> - **没有时再创建**：执行 `gdpa-cli create-session`。
> - **后续调用**：可以显式传 `--session-id <session_id>`，例如 `gdpa-cli run <agent> --session-id <session_id> --input '{...}'`。
> - **适用场景**：Base Workflow、BITS Dev Workflow、post-coding-verify 及其他依赖 Session 工作目录的场景需要持续复用；普通单次查询通常可以不传。

# ByteES Agent

Query ByteES (Elasticsearch) across multiple VRegions.

> **When to Use**: Run Elasticsearch DSL queries against ByteES clusters. Covers both I18N/EU Kibana Console Proxy regions and US-TTP / US-TTP2 DataQ regions.

## Quick Start

```bash
# 查 Singapore-Central 集群的索引（默认 vregion，走 Kibana）
gdpa-cli run bytees --session-id "$SESSION_ID" --input '{
  "cluster_psm": "byte.es.entity_platform",
  "path": "_cat/indices",
  "method": "GET"
}'

# 带 DSL 的 _search
gdpa-cli run bytees --session-id "$SESSION_ID" --input '{
  "cluster_psm": "byte.es.entity_platform",
  "path": "my_index/_search",
  "method": "GET",
  "body": {"query": {"match_all": {}}, "size": 5},
  "vregion": "sg"
}'

# US-EastRed（走 EU Kibana 网关，仅非受限员工可见）
gdpa-cli run bytees --session-id "$SESSION_ID" --input '{
  "cluster_psm": "byte.es.foo",
  "path": "_search",
  "body": {"query": {"term": {"status": "ok"}}},
  "vregion": "us-eastred"
}'

# US-TTP（走 DataQ，index + body 必填）
gdpa-cli run bytees --session-id "$SESSION_ID" --input '{
  "cluster_psm": "byte.es.albert",
  "index": ".kibana_1",
  "body": {"query": {"match_all": {}}, "size": 10},
  "vregion": "us-ttp"
}'
```

## Input Parameters

### Required

| Parameter | Type | Description |
|-----------|------|-------------|
| `cluster_psm` | string | ByteES 集群 PSM，例如 `byte.es.entity_platform`。URL 中的 `/kibana/{cluster_psm}/my/api/console/proxy` 就是该参数。 |

### Optional

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `path` | string | `_search` | ES REST 相对路径（不以 `/` 开头），例如 `_search`、`my_index/_search`、`_cat/indices`。Kibana 后端透传；DataQ 后端仅用于从首段提取 `index`。 |
| `method` | string | `GET` | ES HTTP 方法（`GET` / `POST` / `PUT` / `DELETE` 等）。仅 Kibana 后端使用。 |
| `body` | object / string | `null` | ES DSL。`object`/`map` 会自动 JSON 序列化；`string` 必须是合法 JSON。DataQ 后端必填。 |
| `index` | string | auto | ES 索引名，仅 DataQ 后端（US-TTP/US-TTP2）必填；未显式传时会自动从 `path` 首段解析（如 `.kibana_1/_search` → `.kibana_1`）。 |
| `vregion` | string | `Singapore-Central` | VRegion 名或别名，参考下方路由表。 |

## Backend Routing

根据 `vregion` 自动选择后端：

| Backend | Gateway | VRegions |
|---------|---------|----------|
| **Kibana Console Proxy** | `kibana-bytees-i18n.tiktok-row.net` | `Singapore-Central`, `US-East` |
| **Kibana Console Proxy** | `kibana-bytees.tiktok-eu.net` | `US-EastRed`, `EU-TTP2` |
| **DataQ** | `dataq.tiktok-row.net` | `US-TTP`, `US-TTP2` |

### VRegion 别名

| VRegion | Aliases | Backend | JWT |
|---------|---------|---------|-----|
| `Singapore-Central` (default) | `sg` | Kibana I18N | i18n |
| `US-East` | `us`, `i18n` | Kibana I18N | i18n |
| `US-EastRed` | `us-eastred`, `useastred` | Kibana EU | i18n |
| `EU-TTP2` | `eu-ttp2`, `euttp2` | Kibana EU | i18n |
| `US-TTP` | `ttp`, `us-ttp` | DataQ | ttp-us |
| `US-TTP2` | `ttp2`, `us-ttp2` | DataQ | ttp-us |

## Output Format

### Kibana 后端

返回 ES 原始响应（已解析 JSON），放在 `data` 字段里：

```json
{
  "success": true,
  "backend": "kibana",
  "vregion": "Singapore-Central",
  "cluster_psm": "byte.es.entity_platform",
  "path": "my_index/_search",
  "method": "GET",
  "data": {
    "took": 5,
    "hits": {
      "total": {"value": 123, "relation": "eq"},
      "hits": [
        {"_index": "my_index", "_id": "1", "_source": {"foo": "bar"}}
      ]
    }
  }
}
```

### DataQ 后端

```json
{
  "success": true,
  "backend": "dataq",
  "vregion": "US-TTP",
  "cluster_psm": "byte.es.bar",
  "data": {
    "row_count": 10,
    "columns": ["_id", "_source"],
    "rows": [ {"_id": "...", "_source": "..."} ]
  }
}
```

> DataQ 返回的 `rows` 为 `map[string]string` 或 `[][]string`，字段由 DataQ 侧决定。

## Examples

### Get cluster indices (Kibana)

```bash
gdpa-cli run bytees --session-id "$SESSION_ID" --input '{"cluster_psm": "byte.es.entity_platform", "path": "_cat/indices", "method": "GET"}'
```

### Match-all search with size limit (Kibana)

```bash
gdpa-cli run bytees --session-id "$SESSION_ID" --input '{
  "cluster_psm": "byte.es.entity_platform",
  "path": "my_index/_search",
  "body": {"query": {"match_all": {}}, "size": 5}
}'
```

### Targeted term search on US-EastRed (EU Kibana)

```bash
gdpa-cli run bytees --session-id "$SESSION_ID" --input '{
  "cluster_psm": "byte.es.foo",
  "path": "my_index/_search",
  "body": {"query": {"term": {"env": "prod"}}, "size": 1},
  "vregion": "us-eastred"
}'
```

### DataQ on US-TTP

显式传 `index`：

```bash
gdpa-cli run bytees --session-id "$SESSION_ID" --input '{
  "cluster_psm": "byte.es.albert",
  "index": ".kibana_1",
  "body": {"query": {"match": {"name": "foo"}}, "size": 10},
  "vregion": "us-ttp"
}'
```

或让 CLI 从 `path` 首段自动解析 `index`：

```bash
gdpa-cli run bytees --session-id "$SESSION_ID" --input '{
  "cluster_psm": "byte.es.albert",
  "path": ".kibana_1/_search",
  "body": {"query": {"match_all": {}}, "size": 10},
  "vregion": "us-ttp"
}'
```

## Kibana 认证（重要）

`kibana-bytees-i18n.tiktok-row.net` / `kibana-bytees.tiktok-eu.net` 走 `sso.bytedance.com`
OAuth2 授权码登录，不认 `x-jwt-token`；浏览器里真正的鉴权 cookie 是：

| Cookie | 含义 | TTL |
|--------|------|-----|
| `gdpr` | ES256 JWT，Kibana 最终认证的凭据 | ~24h |
| `permission` | 常量 `"true"`，同时下发 | 与 gdpr 同期 |

sso.bytedance.com 放行 `/oauth2/authorize` 需要**一整包 session cookies**（不仅仅是
`bd_sso_3b6da9`）：`sessionid` / `bd_sso_sid_*` / `__Host_bd_sso_sid_*` / `bd_sso_3b6da9`
等同时命中才会直接授权，缺任何一条都会跳去 IdP 联邦然后卡在二次登录。

CLI 通过两级缓存 + 一次性 bootstrap 拿到它们：

1. 一次 `gdpa-cli bytees bootstrap` 从本机浏览器一次性抽取 **SSO cookie bundle**
   （macOS 下默认扫 Chrome / Edge / Chromium / Brave；~7 天 TTL，跟随 bd_sso_3b6da9 exp）；
2. CLI 把 bundle 灌进 cookie jar 跑一遍 OAuth2 链，把当前域的 `gdpr` / `permission`
   写入 `~/.gdpa_cache/bytees/`；
3. 之后 `gdpa-cli run bytees ...` 命中缓存即用；gdpr 过期前会自动用 bundle 再跑
   一次 OAuth2 链刷新，全过程用户无感；
4. bundle 过期（~7 天）后再次 `gdpa-cli bytees bootstrap` 即可——只要浏览器里
   仍保持登录态，bootstrap 依然零点击。

### 一次性引导（零点击）

```bash
# 默认：自动从本机 Chrome/Edge 抽 cookie bundle，对两个 Kibana 域都做 bootstrap
gdpa-cli bytees bootstrap

# 只引导 Singapore-Central / US-East（tiktok-row 域）
gdpa-cli bytees bootstrap --vregion sg

# 只引导 US-EastRed / EU-TTP2（tiktok-eu 域）
gdpa-cli bytees bootstrap --vregion eu-ttp2

# 限定只扫某个浏览器
gdpa-cli bytees bootstrap --browser chrome
```

#### 前置条件

1. 在 Chrome / Edge / Chromium / Brave 任一浏览器里访问过 Kibana 一次，完成 SSO
   登录（账号 + 密码 + OTP）直到 `https://kibana-bytees-i18n.tiktok-row.net/kibana/...`
   或 `https://kibana-bytees.tiktok-eu.net/kibana/...` 的 Dev Tools 页面成功渲染。
2. 运行 `gdpa-cli bytees bootstrap`。CLI 会：
   - 读 `~/Library/Application Support/<浏览器>/<Profile>/Cookies` SQLite，
     扫 `.bytedance.com` / `sso.bytedance.com` / `.tiktok-row.net` / `.tiktok-eu.net`
     / `.sso.tiktok-intl.com` 下所有 session cookies；
   - 从 macOS Keychain 取 `<浏览器> Safe Storage` 密码派生 AES-128-CBC key；
   - AES-CBC 解密 v10/v11 encrypted_value，按 cookie 类型剥 SHA256(host) 前缀；
   - 灌进 cookie jar 跑 OAuth2 链写入 `~/.gdpa_cache/bytees/`（0600）。
3. **首次运行会弹一次 macOS Keychain 授权框**（内容：`gdpa-cli wants to access
   "Chrome Safe Storage"`），点 **"Always Allow"** 后本 binary 以后静默生效。

#### 失败排查

- `kibana session cookies not found ...`：浏览器里没登录过，或者 Kibana 登录态已
  过期。CLI 会自动替你打开 Kibana 页面，完成登录后重跑 bootstrap 即可。
- `automatic cookie extraction is not supported on this OS`：当前仅支持 macOS；
  Linux / Windows 版本暂未实现自动抽取，请在 macOS 上 bootstrap 后把
  `~/.gdpa_cache/bytees/` 同步过去。
- `oauth2 chain did not reach kibana domain`：浏览器里的 sso.bytedance.com session
  已过期（即便 bd_sso_3b6da9 看起来还在）。请在浏览器里重新访问 Kibana 完成一次
  登录，再跑 bootstrap。

### 缓存管理

```bash
# 查看当前缓存状态（JSON 格式）
gdpa-cli bytees credential get

# 清除缓存
gdpa-cli bytees credential clear

# 打印缓存目录路径
gdpa-cli bytees credential path
```

缓存目录结构：

```
~/.gdpa_cache/bytees/
├── sso.json            # SSO cookie bundle + exp（bd_sso_3b6da9 的 exp 为准）
├── gdpr_i18n.json      # tiktok-row 域 gdpr + permission + exp
└── gdpr_eu.json        # tiktok-eu 域 gdpr + permission + exp
```

## Error Handling

| Error | Cause | Solution |
|-------|-------|----------|
| `cluster_psm parameter is required` | 缺少集群 PSM | 补上 `cluster_psm`（如 `byte.es.entity_platform`） |
| `body is not valid JSON` | `body` 作为字符串但不是合法 JSON | 传 JSON 对象或改成合法 JSON 字符串 |
| `body (ES DSL) is required for DataQ ...` | US-TTP / US-TTP2 未提供 `body` | DataQ 后端必须带 DSL |
| `index is required for DataQ ...` | DataQ 路径下无法解析出 ES 索引 | 显式传 `index`，或把 `path` 写成 `<index>/_search` 格式 |
| `invalid vregion` | VRegion 名错误 | 参照上方路由表 / 别名表 |
| `ByteES Kibana 凭据未初始化` | 未运行 bootstrap | 运行 `gdpa-cli bytees bootstrap --vregion <vregion>` |
| `bd_sso_3b6da9 已过期` | 超过 7 天未 bootstrap | 重新运行 `gdpa-cli bytees bootstrap` |
| `oauth2 chain did not reach kibana domain` | 浏览器里 sso.bytedance.com session 已过期 | 在浏览器里重新登录一次 Kibana 后再跑 bootstrap |
| `kibana gdpr cookie rejected (302 -> /sso/...)` | 服务端拒绝缓存的 gdpr（小概率） | 本地缓存已被清，下次请求会自动 OAuth2 刷新；若仍失败请 `bootstrap` |
| `authentication failed` | JWT 获取失败 | 重新 `gdpa-cli login` / 检查网络 |
| `DataQ error (code=...)` | DataQ 业务错误 | 检查 `cluster_psm`、DSL 是否被 DataQ 支持 |

## Notes

- **只读**：本 skill 只做查询类调用。虽然底层 Kibana Console Proxy 可以接 `POST /_index/_doc` 这类写操作，请只用在读路径上。
- **Body 透传**：Kibana 后端是把 `body` 原样传给 ES REST endpoint，因此你可以把它当作 Kibana Dev Tools 里 Request body 的等价物使用。
- **US-EastRed / EU-TTP2 受限员工不可访问**：这两个区域走 `kibana-bytees.tiktok-eu.net`，ByteCloud 网关只允许非受限员工访问。如果 JWT 失败请先确认账户归属。
- **DataQ 语义**：`data_source=bytees`，`psm=cluster_psm`，`index=<ES index>`，`idc=<VRegion 对应的 IDC>`（由 VRegion 自动查表：US-TTP→useast5, US-TTP2→useast8），`region=<VRegion 原名>`（如 `US-TTP`；不走 RDS 那个 `ova` 别名），`query=ES DSL JSON`。DataQ 服务端据此定位真实 ES 集群并转发 DSL。若发现字段语义变化，请把新 curl 样例落到 `pkg/devflow-api-clients/idl/protobuf/dataq/curl_data/` 后再联系维护者调整。
- **超时**：大查询请配合 `size` / `from` / `timeout` DSL 字段使用，避免网关超时。
