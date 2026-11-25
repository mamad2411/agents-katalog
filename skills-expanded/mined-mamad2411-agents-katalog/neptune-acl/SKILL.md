---
name: neptune-acl
description: Query Neptune service access control and authorization rules — check if service authentication (Authen) is enabled, if strict authorization (AccCtrl/ACL) is turned on, or if a specific caller PSM is authorized to access a callee. Use whenever the user asks about service authentication status, ACL configuration, access control between services, whether a service has auth enabled, or if one service is authorized to call another. This skill focuses on auth/ACL — for timeout config use neptune-stability.
---

> **session_id 传递**：若本次任务需要在多次 `gdpa-cli run` 之间串联 workflow 状态、日志或上下文，请复用同一个 `session_id`。如果当前 skill / Agent 已经提供了 `session_id`，**请直接复用，不要新建**。
>
> - **已有时优先复用**：不要重复执行 `create-session`。
> - **没有时再创建**：执行 `gdpa-cli create-session`。
> - **后续调用**：可以显式传 `--session-id <session_id>`，例如 `gdpa-cli run <agent> --session-id <session_id> --input '{...}'`。
> - **适用场景**：Base Workflow、BITS Dev Workflow、post-coding-verify 及其他依赖 Session 工作目录的场景需要持续复用；普通单次查询通常可以不传。

# Neptune ACL 服务治理查询

查询 Neptune 平台的服务治理规则，支持 3 种场景：服务鉴定、严格授权开启检查、具体授权检查。

## 三种场景

| action | 场景 | Category | 说明 |
|--------|------|----------|------|
| `check_authen` | 服务鉴定是否开启 | Authen | 检查被调服务的服务鉴定状态 |
| `check_acl_enabled` | 严格授权是否开启 | AccCtrl | 检查被调是否全局开启了严格授权（caller 固定为 any） |
| `check_acl_authorized` | 查看是否有授权 | AccCtrl | 检查指定 caller 是否被授权访问被调 |

## Command Format

```bash
gdpa-cli run neptune-acl --session-id "$SESSION_ID" --input '<json_params>'
```

## Input Schema

```json
{
  "type": "object",
  "required": ["action", "callee"],
  "properties": {
    "action": {
      "type": "string",
      "enum": ["check_authen", "check_acl_enabled", "check_acl_authorized"],
      "description": "查询场景"
    },
    "callee": {
      "type": "string",
      "description": "被调服务名（PSM 格式），如 'tiktok.my_service'"
    },
    "callee_cluster": {
      "type": "string",
      "default": "default",
      "description": "被调集群"
    },
    "method": {
      "type": "string",
      "default": "*",
      "description": "方法名，'*' 表示所有方法（支持通配）"
    },
    "caller": {
      "type": "string",
      "description": "主调服务名（仅 check_acl_authorized 时必填）"
    },
    "caller_cluster": {
      "type": "string",
      "default": "default",
      "description": "主调集群（仅 check_acl_authorized 时使用，支持 '*' 通配）"
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

---

## 场景 1：查看服务鉴定是否开启 (check_authen)

检查被调服务是否开启了服务鉴定（Authen）。

```bash
gdpa-cli run neptune-acl --session-id "$SESSION_ID" --input '{
  "action": "check_authen",
  "callee": "tiktok.my_service",
  "callee_cluster": "default",
  "method": "*",
  "vregion": "us"
}'
```

**响应示例：**

```json
{
  "success": true,
  "data": {
    "action": "check_authen",
    "callee": "tiktok.my_service",
    "configured": true,
    "authen_enabled": true,
    "status": "on",
    "message": "服务鉴定已开启 for 'tiktok.my_service'"
  }
}
```

---

## 场景 2：查看严格授权是否开启 (check_acl_enabled)

检查被调服务是否全局开启了严格授权。caller 和 caller_cluster 自动设为 `any`。

```bash
gdpa-cli run neptune-acl --session-id "$SESSION_ID" --input '{
  "action": "check_acl_enabled",
  "callee": "tiktok.my_service",
  "callee_cluster": "default",
  "method": "*",
  "vregion": "us"
}'
```

**响应示例：**

```json
{
  "success": true,
  "data": {
    "action": "check_acl_enabled",
    "callee": "tiktok.my_service",
    "configured": true,
    "acl_enabled": true,
    "deny": true,
    "message": "严格授权已开启 for 'tiktok.my_service'（未授权的调用方将被拒绝）"
  }
}
```

---

## 场景 3：查看指定 PSM 是否有授权 (check_acl_authorized)

在严格授权开启的前提下，检查指定 caller 是否被授权访问 callee。

```bash
gdpa-cli run neptune-acl --session-id "$SESSION_ID" --input '{
  "action": "check_acl_authorized",
  "callee": "tiktok.my_service",
  "callee_cluster": "default",
  "caller": "tiktok.caller_service",
  "caller_cluster": "default",
  "method": "*",
  "vregion": "us"
}'
```

**响应示例（已授权）：**

```json
{
  "success": true,
  "data": {
    "action": "check_acl_authorized",
    "callee": "tiktok.my_service",
    "caller": "tiktok.caller_service",
    "configured": true,
    "authorized": true,
    "status": "ALLOWED",
    "message": "caller 'tiktok.caller_service' 已被授权访问 callee 'tiktok.my_service'"
  }
}
```

**响应示例（被拒绝）：**

```json
{
  "success": true,
  "data": {
    "action": "check_acl_authorized",
    "configured": true,
    "authorized": false,
    "status": "DENIED",
    "message": "caller 'tiktok.caller_service' 被拒绝访问 callee 'tiktok.my_service'"
  }
}
```

---

## 各场景参数对照

| 参数 | check_authen | check_acl_enabled | check_acl_authorized |
|------|-------------|-------------------|---------------------|
| `action` | 必填 | 必填 | 必填 |
| `callee` | 必填 | 必填 | 必填 |
| `callee_cluster` | 可选 (default) | 可选 (default) | 可选 (default) |
| `method` | 可选 (*) | 可选 (*) | 可选 (*) |
| `caller` | 不需要 | 不需要（自动=any） | **必填** |
| `caller_cluster` | 不需要 | 不需要（自动=any） | 可选 (default, 支持 *) |
| `vregion` | 可选 (Singapore-Central) | 可选 (Singapore-Central) | 可选 (Singapore-Central) |

## Error Handling

| Error | Cause | Solution |
|-------|-------|----------|
| `action parameter is required` | 缺少 action | 指定 action 参数 |
| `callee parameter is required` | 缺少 callee | 添加 callee 参数 |
| `caller parameter is required for action 'check_acl_authorized'` | 场景 3 缺少 caller | 添加 caller 参数 |
| `authentication failed` | JWT 获取失败 | 运行 `gdpa-cli login` |
| `StatusCode=-1` | 未找到匹配规则 | 确认服务名和 VRegion 正确 |

## Notes

- 所有规则按 VRegion 维度存储，需指定正确的 VRegion
- `method` 支持 `*` 通配表示所有方法，也可指定具体方法名如 `GetUser`
- 场景 3 的 `caller_cluster` 支持 `*` 通配
