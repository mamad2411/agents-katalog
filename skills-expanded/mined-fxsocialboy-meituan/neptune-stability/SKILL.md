---
name: neptune-stability
description: Query Neptune stability governance rules — service authentication (Authen) status and timeout configuration (Timeout) including read/write/connection/RPC timeouts. Use whenever the user asks about RPC timeout settings, service timeout configuration, how long an RPC call is allowed, connection timeout values, or wants to troubleshoot timeout-related issues between services. This skill focuses on stability rules (auth + timeout) — for ACL/authorization use neptune-acl.
---

> **session_id 传递**：若本次任务需要在多次 `gdpa-cli run` 之间串联 workflow 状态、日志或上下文，请复用同一个 `session_id`。如果当前 skill / Agent 已经提供了 `session_id`，**请直接复用，不要新建**。
>
> - **已有时优先复用**：不要重复执行 `create-session`。
> - **没有时再创建**：执行 `gdpa-cli create-session`。
> - **后续调用**：可以显式传 `--session-id <session_id>`，例如 `gdpa-cli run <agent> --session-id <session_id> --input '{...}'`。
> - **适用场景**：Base Workflow、BITS Dev Workflow、post-coding-verify 及其他依赖 Session 工作目录的场景需要持续复用；普通单次查询通常可以不传。

# Neptune Stability 稳定性规则查询

查询 Neptune 平台的稳定性规则，包括服务鉴定（Authen）状态和超时配置（Timeout）。

## When to Use

- 查看服务鉴定（Authen）是否开启
- 查询 RPC 超时配置（读/写/连接/RPC 超时）
- 查询特定 caller → callee 调用链路的超时配置
- 排查服务间调用超时问题
- 确认稳定性治理规则是否已配置

## Command Format

```bash
gdpa-cli run neptune-stability --session-id "$SESSION_ID" --input '<json_params>'
```

## Input Schema

```json
{
  "type": "object",
  "required": ["callee"],
  "properties": {
    "callee": {
      "type": "string",
      "description": "被调服务名（PSM 格式），如 'tiktok.my_service'"
    },
    "callee_cluster": {
      "type": "string",
      "default": "default",
      "description": "被调集群"
    },
    "caller": {
      "type": "string",
      "description": "主调服务名（PSM 格式），用于查询特定调用链路的超时配置"
    },
    "caller_cluster": {
      "type": "string",
      "description": "主调集群，配合 caller 使用"
    },
    "category": {
      "type": "string",
      "enum": ["Authen", "Timeout"],
      "default": "Authen",
      "description": "规则类型：Authen（服务鉴定）或 Timeout（超时配置）"
    },
    "method": {
      "type": "string",
      "default": "*",
      "description": "方法名，'*' 表示所有方法"
    },
    "vregion": {
      "type": "string",
      "enum": ["Singapore-Central", "US-East", "China-North", "China-East", "US-TTP", "US-TTP2", "EU-TTP2", "US-EastRed", "China-Pay", "China-Pay2", "China-HKPay", "China-North6", "US-Compliance", "MY-Compliance", "US-EE", "China-BOE", "China-BOE2", "US-BOE", "Asia-SaaS", "Asia-CIS", "Singapore-Compliance"],
      "default": "Singapore-Central",
      "description": "VRegion，需与服务部署区域匹配。别名：'sg'→Singapore-Central, 'us'→US-East, 'cn'→China-North, 'boe'→China-BOE, 'boei18n'→US-BOE"
    }
  }
}
```

## Output Schema

### Authen 类型响应

```json
{
  "success": true,
  "data": {
    "callee": "tiktok.my_service",
    "category": "Authen",
    "vregion": "Singapore-Central",
    "configured": true,
    "status": "on",
    "message": "Service authentication is ON for 'tiktok.my_service'"
  }
}
```

### Timeout 类型响应

```json
{
  "success": true,
  "data": {
    "callee": "tiktok.my_service",
    "category": "Timeout",
    "vregion": "Singapore-Central",
    "configured": true,
    "read_timeout_ms": 1000,
    "write_timeout_ms": 1000,
    "conn_timeout_ms": 500,
    "rpc_timeout_ms": 2000,
    "message": "Timeout config for 'tiktok.my_service': rpc=2000ms, read=1000ms, write=1000ms, conn=500ms"
  }
}
```

## Examples

### 查询服务鉴定状态

```bash
gdpa-cli run neptune-stability --session-id "$SESSION_ID" --input '{
  "callee": "tiktok.my_service",
  "category": "Authen",
  "vregion": "us"
}'
```

### 查询超时配置

```bash
gdpa-cli run neptune-stability --session-id "$SESSION_ID" --input '{
  "callee": "tiktok.my_service",
  "category": "Timeout",
  "vregion": "sg"
}'
```

### 查询指定 caller 调用链路的超时

```bash
gdpa-cli run neptune-stability --session-id "$SESSION_ID" --input '{
  "caller": "desrpc.test.client",
  "caller_cluster": "maliva-va",
  "callee": "desrpc.stability.thrift_server",
  "callee_cluster": "default",
  "category": "Timeout",
  "method": "GetItem",
  "vregion": "sg"
}'
```

### 查询指定方法的超时

```bash
gdpa-cli run neptune-stability --session-id "$SESSION_ID" --input '{
  "callee": "tiktok.my_service",
  "category": "Timeout",
  "method": "GetUser",
  "vregion": "cn"
}'
```

## Category 说明

| Category | 用途 | 返回字段 |
|----------|------|---------|
| `Authen` | 服务鉴定 | `status`（on/off） |
| `Timeout` | 超时配置 | `rpc_timeout_ms`, `read_timeout_ms`, `write_timeout_ms`, `conn_timeout_ms` |

## Error Handling

| Error | Cause | Solution |
|-------|-------|----------|
| `callee parameter is required` | 缺少 callee | 添加 callee 参数 |
| `category must be 'Authen' or 'Timeout'` | category 值无效 | 使用 Authen 或 Timeout |
| `authentication failed` | JWT 获取失败 | 运行 `gdpa-cli login` |
| `configured: false` | 未配置规则 | 确认服务名和 VRegion 正确 |

## Notes

- 稳定性规则按 VRegion 维度存储，需指定正确 VRegion
- 默认查询 Authen 类型，如需查询超时配置请指定 `category: "Timeout"`
- `method: "*"` 表示服务级别的规则，指定具体方法名可查询方法级别规则
- 支持通过 `caller` + `caller_cluster` 查询特定调用链路的超时配置；不传则查询 callee 服务级别规则
