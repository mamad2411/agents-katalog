---
name: diag
description: Watchdog Diag Notebook engine for chained assertions on RPC responses, Diag-platform log queries, and RDS database queries. Use ONLY when the user explicitly mentions Diag, Watchdog Diag, Diag Notebook, or specifically needs Diag-unique features like chained notebook assertions, Diag log queries by keyword/logID, or Diag RDS database queries with assertions. 
---

> **session_id 传递**：若本次任务需要在多次 `gdpa-cli run` 之间串联 workflow 状态、日志或上下文，请复用同一个 `session_id`。如果当前 skill / Agent 已经提供了 `session_id`，**请直接复用，不要新建**。
>
> - **已有时优先复用**：不要重复执行 `create-session`。
> - **没有时再创建**：执行 `gdpa-cli create-session`。
> - **后续调用**：可以显式传 `--session-id <session_id>`，例如 `gdpa-cli run <agent> --session-id <session_id> --input '{...}'`。
> - **适用场景**：Base Workflow、BITS Dev Workflow、post-coding-verify 及其他依赖 Session 工作目录的场景需要持续复用；普通单次查询通常可以不传。

> **session_id 可选**：Diag 的单次调用不强制要求 `--session-id`。
>
> **session_id 传递**：当你需要把一组 RPC 调用、日志查询和 RDS 查询串到同一条排障链路里时，建议显式复用同一个 Session。
> 1. 创建 Session（可选）: `gdpa-cli create-session`（返回 session_id）
> 2. 需要串联多条命令时，通过 `--session-id` 参数显式传递：
>    - `gdpa-cli run <agent> --session-id <session_id> --input '{...}'`
>    - `gdpa-cli run devflow list --session-id <session_id> --psm xxx`
> 3. 如果本次只是一次性查询，也可以直接省略 `--session-id`。

# Diag Skill

通过 Watchdog Diag 平台进行 RPC 调用测试、日志查询和 RDS 数据库查询，支持断言验证。

## 三种操作模式

1. **rpc_call**: 通过 Diag 平台发起 RPC 调用并获取结果（支持断言）
2. **log_query**: 通过 Diag 平台查询日志（支持关键字查询和 LogID 查询）
3. **rds_query**: 通过 Diag 平台查询 RDS 数据库（支持参数化查询和断言）

## ⚠️ RPC 调用的 request 构建流程（重要）

执行 `rpc_call` 时，`request` 参数是 RPC 方法的请求体 JSON。**必须严格按照方法的 IDL 定义来构造**，否则调用会失败。

### 构建步骤

1. **获取方法的 IDL 定义**：
   - 如果当前代码仓库中有该服务的 IDL（Thrift/Protobuf）文件，直接读取字段定义。
   - **如果代码中找不到 IDL 定义，必须使用 `/bam-api` skill 查询 PSM 的接口定义**：
     ```
     /bam-api 查询 <psm> 的 <method> 方法的请求参数定义
     ```
   - BAM 会返回方法的完整请求/响应结构体定义，包括字段名、类型、是否必填等信息。

2. **根据 IDL 定义构造 request JSON**：
   - 将 IDL 字段映射为 JSON key/value，注意字段名的大小写（通常 Thrift 字段首字母大写，Protobuf 使用 camelCase 或 PascalCase）。
   - 对于必填字段，确保有值；可选字段按需填入。
   - `Base` 字段通常包含 `LogID`、`Caller`、`Extra`（如 `{"env": "ppe_xxx"}`）等。

3. **与用户确认**：
   - 在发起 RPC 调用之前，**向用户展示即将发送的 request 结构和断言条件**，让用户确认或修改。
   - 用自然语言描述构造逻辑，例如："我将使用以下参数调用 `psm:method`，request 包含 xxx 字段，断言验证 StatusCode=0，是否继续？"

### request 编码方式

`request` 字段中的 JSON 对象会被自动编码为 Diag 平台的 `j` + base64(JSON) 格式，**无需手动编码**。只需传入原始 JSON 对象即可。

## 使用方法

```bash
gdpa-cli run diag --session-id "$SESSION_ID" --input '{"action": "<action>", ...}'
```

## 支持的 Action

| Action | 描述 | 必填参数 | 可选参数 |
|--------|------|----------|----------|
| rpc_call | RPC 调用 | psm, method | request, vregion, cluster, env, branch, timeout, vdc, ip_port, assertions |
| log_query | 日志查询 | psms (或 psm) | vregion, include_keywords, exclude_keywords, start_time, end_time, time_range, limit, logid, case_sensitive, assertions |
| rds_query | RDS 数据库查询 | region, db, sql | args, useProxy, assertions |

## 输入参数

### 通用参数

| 参数 | 类型 | 描述 |
|------|------|------|
| action | string | 操作类型（必填） |

### rpc_call

| 参数 | 类型 | 描述 |
|------|------|------|
| psm | string | 服务 PSM（必填） |
| method | string | RPC 方法名（必填） |
| request | object | 请求体 JSON，按 IDL 定义构造（自动编码为 j+base64 格式） |
| vregion | string | 区域，默认 Singapore-Central |
| cluster | string | 集群，默认 "default" |
| env | string | 环境名，如 "ppe_xxx" |
| branch | string | 分支，默认 "master" |
| timeout | int | 超时时间（毫秒），默认 10000 |
| vdc | string | 虚拟数据中心 |
| ip_port | string | 指定实例 IP:Port |
| assertions | array | 断言列表，每项 {field, operator, value} |

### log_query

| 参数 | 类型 | 描述 |
|------|------|------|
| psms | array | 服务 PSM 列表（必填，或使用 psm 单个 PSM） |
| vregion | string | 区域，默认 Singapore-Central |
| logid | string | LogID（提供时使用 LogID 查询模式） |
| include_keywords | array | 包含关键词（关键字查询模式） |
| exclude_keywords | array | 排除关键词 |
| include_operator | string | 包含操作符，AND/OR，默认 AND |
| exclude_operator | string | 排除操作符，AND/OR，默认 AND |
| case_sensitive | bool | 是否区分大小写，默认 true |
| start_time | int | 开始时间戳（秒） |
| end_time | int | 结束时间戳（秒） |
| time_range | string | 相对时间范围，如 "1h"、"30m" |
| limit | int | 返回条数，默认 100 |
| assertions | array | 断言列表 |

### rds_query

| 参数 | 类型 | 描述 |
|------|------|------|
| region | string | RDS 区域，格式 "VRegion/dc"（必填），如 "Singapore-Central/alisg"。仅写 VRegion 时会使用默认 dc |
| db | string | 数据库名称（必填） |
| sql | string | SQL 查询语句（必填），仅支持 SELECT / EXPLAIN |
| args | array | SQL 参数化查询参数，支持基本类型和数组 |
| useProxy | bool | 是否使用直连模式，默认 false |
| assertions | array | 断言列表 |

#### VRegion-DataCenter 映射（region 参数）

| VRegion | 默认 DC | 其他可用 DC |
|---------|---------|------------|
| China-BOE | boe | - |
| China-North | cn | - |
| Singapore-Central | alisg | sg_sensitive, sg2, sgdt |
| US-EastRed | us_east_gcp | - |
| US-East | maliva | maliva_sensitive, useastdt, awsvagm |
| US-TTP | ova | - |
| US-TTP2 | useast8 | - |
| EU-TTP | ie | iedt |

### 断言 (assertions)

断言使用 JMESPath 语法进行字段路径访问，支持链式断言：

```json
{
  "assertions": [
    {"field": "BaseResp.StatusCode", "operator": "=", "value": 0},
    {"field": "incident.summary.status", "operator": "=", "value": "finished"}
  ]
}
```

**支持的操作符**:
`=`, `==`, `!=`, `>`, `<`, `>=`, `<=`, `like`, `contains`, `~=`(正则), `startsWith`, `endsWith`, `is`, `isNot`

**`is`/`isNot` 特殊用法**:
- `{"field": "path", "operator": "is", "value": "exists"}` — 判断路径是否存在
- `{"field": "obj", "operator": "is", "value": "null"}` — 判断字段是否为 null

## 输出格式

### rpc_call（无断言）
```json
{"success": true, "action": "rpc_call", "psm": "...", "method": "...", "raw_data": {...}, "log_id": "...", "notebook_url": "..."}
```

### rpc_call（有断言）
```json
{"success": true, "action": "rpc_call", "assert_matched": true, "notebook_url": "..."}
```

> `assert_matched` 字段的契约：**只要请求里带了 `assertions`，结果就一定包含 `assert_matched`**（`true`/`false` 均会返回，以便稳定判断是否匹配）。未传 `assertions` 时不返回该字段。`rpc_call` / `log_query` / `rds_query` 三种 action 行为一致。

### log_query
```json
{"success": true, "action": "log_query", "logs": [...], "total": 6, "notebook_url": "..."}
```

## 完整示例工作流

### 场景：测试某 PSM 的 RPC 接口并验证返回值

```
步骤 1: 使用 /bam-api 查询接口定义
    → /bam-api 查询 desrpc.stability.thrift_server 的 GetItem 方法

步骤 2: 根据 IDL 定义构造 request，向用户确认
    → "我将调用 desrpc.stability.thrift_server:GetItem，参数包含 item_id=475590858，
       环境 ppe_desrpc_test，区域 US-East，是否继续？"

步骤 3: 用户确认后发起调用
    → gdpa-cli run diag --session-id "$SESSION_ID" --input '{"action":"rpc_call", ...}'

步骤 4: 查看结果，按需追加断言验证
```

### RPC 调用测试
```bash
gdpa-cli run diag --session-id "$SESSION_ID" --input '{
  "action": "rpc_call",
  "psm": "desrpc.stability.thrift_server",
  "method": "GetItem",
  "request": {"item_id": 475590858, "Base": {"Extra": {"env": "ppe_desrpc_test"}}},
  "vregion": "US-East",
  "env": "ppe_desrpc_test",
  "vdc": "maliva"
}'
```

### RPC 调用 + 断言
```bash
gdpa-cli run diag --session-id "$SESSION_ID" --input '{
  "action": "rpc_call",
  "psm": "desrpc.stability.thrift_server",
  "method": "GetItem",
  "request": {"item_id": 475590858},
  "vregion": "US-East",
  "assertions": [{"field": "BaseResp.StatusCode", "operator": "=", "value": 0}]
}'
```

### 日志关键字查询
```bash
gdpa-cli run diag --session-id "$SESSION_ID" --input '{
  "action": "log_query",
  "psms": ["desrpc.stability.thrift_server"],
  "vregion": "US-East",
  "time_range": "1h",
  "include_keywords": ["error"],
  "limit": 100
}'
```

### 日志 LogID 查询
```bash
gdpa-cli run diag --session-id "$SESSION_ID" --input '{
  "action": "log_query",
  "psms": ["desrpc.test.client"],
  "logid": "021773316919797fdbddc530000046900000000000000366b1ca8",
  "vregion": "sg"
}'
```

### RDS 数据库查询（无断言）
```bash
gdpa-cli run diag --session-id "$SESSION_ID" --input '{
  "action": "rds_query",
  "region": "Singapore-Central/alisg",
  "db": "gdp",
  "sql": "SELECT id, name, psm FROM intent_service LIMIT 1",
  "args": []
}'
```

### RDS 数据库查询 + 断言
```bash
gdpa-cli run diag --session-id "$SESSION_ID" --input '{
  "action": "rds_query",
  "region": "Singapore-Central/alisg",
  "db": "gdp",
  "sql": "SELECT id, name FROM intent_service WHERE id > ? LIMIT 10",
  "args": [0],
  "assertions": [{"field": "id", "operator": ">", "value": 0}]
}'
```

### RDS 参数化查询（使用数组参数）
```bash
gdpa-cli run diag --session-id "$SESSION_ID" --input '{
  "action": "rds_query",
  "region": "US-TTP/ova",
  "db": "social",
  "sql": "SELECT * FROM notice WHERE to_user_id = ? AND related_item_id IN (?) LIMIT 10",
  "args": ["user123", [100, 200, 300]]
}'
```

### RDS 直连模式
```bash
gdpa-cli run diag --session-id "$SESSION_ID" --input '{
  "action": "rds_query",
  "region": "US-East/maliva",
  "db": "watchman",
  "sql": "SELECT * FROM ack LIMIT 1",
  "args": [],
  "useProxy": true
}'
```

## 注意事项

1. BOE 环境不支持 Diag 功能
2. RPC 请求体（request）会自动编码为 `j` + base64(JSON) 格式，无需手动编码
3. 每次执行会自动生成随机的 Notebook ID，无需手动管理
4. 断言中的值会根据类型自动编码（整数加 `i` 前缀，布尔值加 `b` 前缀）
5. 日志查询支持两种模式：关键字查询（默认）和 LogID 查询（提供 logid 时自动切换）
6. 区域域名映射：I18N → watchdog.tiktok-row.net, US-TTP → watchdog.tiktok-us.net, EU-TTP → watchdog.tiktok-eu.org
7. **构造 RPC request 时务必参考 IDL 定义**，可通过 `/bam-api` 获取。发送前应与用户确认参数和断言。
8. RDS 查询仅支持 SELECT 和 EXPLAIN 语句，不支持 DML（INSERT/UPDATE/DELETE）和多语句
9. RDS 查询的 SQL 参数会自动编码为 `j` + base64(JSON) 格式，无需手动编码
10. RDS 直连模式（useProxy=true）需确保 `iesarch.watchdog.diag_engine` 已获得目标 DB 的 read 授权
11. RDS 的 `region` 参数需精确到 DataCenter（格式 "VRegion/dc"），仅写 VRegion 会使用默认 dc 映射
12. 在 TTP 合规区域中，COUNT(*) 等聚合函数对应的字段可明文透出，其他字段仅展示 Schema
