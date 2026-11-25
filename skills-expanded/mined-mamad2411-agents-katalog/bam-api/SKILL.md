---
name: bam-api
description: Query BAM API interface definitions, endpoint lists, version information, or create new versions by PSM, method name, path, or endpoint ID. Use this whenever the user wants to look up API definitions, check interface documentation, find endpoint details, list a service's APIs, browse API versions, or create a new BAM version. Also trigger when the user needs to understand what APIs a service exposes, find a specific method signature, or publish a new version — this is for reading API metadata and version management, not for sending actual requests (use bam-query for that).
---

> **session_id 传递**：若本次任务需要在多次 `gdpa-cli run` 之间串联 workflow 状态、日志或上下文，请复用同一个 `session_id`。如果当前 skill / Agent 已经提供了 `session_id`，**请直接复用，不要新建**。
>
> - **已有时优先复用**：不要重复执行 `create-session`。
> - **没有时再创建**：执行 `gdpa-cli create-session`。
> - **后续调用**：可以显式传 `--session-id <session_id>`，例如 `gdpa-cli run <agent> --session-id <session_id> --input '{...}'`。
> - **适用场景**：Base Workflow、BITS Dev Workflow、post-coding-verify 及其他依赖 Session 工作目录的场景需要持续复用；普通单次查询通常可以不传。

# BAM API 查询与版本管理

> **何时使用**: 当需要查询 BAM 上的 API 接口信息、获取版本列表、或创建新版本时调用此 SKILL。

## 使用方法

```bash
gdpa-cli run bam-api --session-id "$SESSION_ID" --input '{"action": "<action>", ...}'
```

## 支持的 Action

| Action | 描述 | 必填参数 | 可选参数 |
|--------|------|----------|----------|
| `get_api_definition_info` | 通过方法名称获取接口定义 | psm, method | version, branch, region |
| `get_api_definition_info_through_path` | 通过路径获取接口定义 | psm, path | version, branch, region |
| `get_api_definition_info_without_psm` | 不需要 PSM，通过关键字获取接口定义 | keyword | offset, count, ep_type, version, branch, region |
| `get_api_definition_info_with_endpoint_id` | 通过 endpointId 获取接口定义（推荐） | endpointId | version, branch, region |
| `get_api_service_list` | 获取 PSM 的接口列表 | psm | version, branch, region |
| `get_api_service_versions` | 获取 PSM 的版本列表 | psm | branch, region |
| `create_service_version` | 创建 PSM 的新版本（⚠️ 写操作，调用前必须确认） | psm, branch | version, note, cluster, no_check, region |

## 输入参数

| 参数 | 类型 | 描述 |
|------|------|------|
| action | string | 必填，要执行的操作 |
| psm | string | PSM（项目服务名），部分 action 需要 |
| method | string | 方法名称 |
| path | string | 接口路径 |
| endpointId | string | 接口 ID |
| version | string | 可选，版本号（如 1.0.21）；create_service_version 不填则自动取最新版本+1 |
| branch | string | 可选，分支名称 |
| keyword | string | 关键字（方法名或路径） |
| offset | string | 可选，页码，默认 0 |
| count | string | 可选，每页数量，默认 10 |
| ep_type | string | 可选，接口类型（http 或 rpc） |
| region | string | 可选，查询区域：`cn`（默认）或 `i18n` |
| note | string | 可选，版本备注 |
| cluster | string | 可选，集群，默认 default |
| no_check | string | 可选，是否跳过检查（"true" 或 "false"） |

## 输出格式

```json
{
  "success": true,
  "action": "get_api_service_list",
  "data": { ... }
}
```

## 示例

```bash
# 获取 PSM 的接口列表
gdpa-cli run bam-api --session-id "$SESSION_ID" --input '{"action": "get_api_service_list", "psm": "tiktok.user.service"}'

# 通过方法名称获取接口定义
gdpa-cli run bam-api --session-id "$SESSION_ID" --input '{"action": "get_api_definition_info", "psm": "tiktok.user.service", "method": "GetUserInfo"}'

# 通过方法名称获取接口定义（指定版本和分支）
gdpa-cli run bam-api --session-id "$SESSION_ID" --input '{"action": "get_api_definition_info", "psm": "tiktok.user.service", "method": "GetUserInfo", "version": "v1", "branch": "master"}'

# 通过路径获取接口定义
gdpa-cli run bam-api --session-id "$SESSION_ID" --input '{"action": "get_api_definition_info_through_path", "psm": "tiktok.user.service", "path": "/api/v1/user/info"}'

# 不需要 PSM，通过关键字获取接口定义
gdpa-cli run bam-api --session-id "$SESSION_ID" --input '{"action": "get_api_definition_info_without_psm", "keyword": "GetUserInfo"}'

# 分页查询，指定接口类型
gdpa-cli run bam-api --session-id "$SESSION_ID" --input '{"action": "get_api_definition_info_without_psm", "keyword": "user", "offset": "0", "count": "20", "ep_type": "http"}'

# 通过 endpointId 获取接口定义（推荐，如果已知 endpointId 优先使用）
gdpa-cli run bam-api --session-id "$SESSION_ID" --input '{"action": "get_api_definition_info_with_endpoint_id", "endpointId": "12345"}'

# 指定版本
gdpa-cli run bam-api --session-id "$SESSION_ID" --input '{"action": "get_api_definition_info_with_endpoint_id", "endpointId": "12345", "version": "1.0.21"}'

# 获取 PSM 的版本列表
gdpa-cli run bam-api --session-id "$SESSION_ID" --input '{"action": "get_api_service_versions", "psm": "tiktok.user.service"}'

# 查询 I18N 区域的接口列表
gdpa-cli run bam-api --session-id "$SESSION_ID" --input '{"action": "get_api_service_list", "psm": "tiktok.user.service", "region": "i18n"}'

# 查询 I18N 区域的接口定义
gdpa-cli run bam-api --session-id "$SESSION_ID" --input '{"action": "get_api_definition_info", "psm": "tiktok.user.service", "method": "GetUserInfo", "region": "i18n"}'

# 创建新版本（自动取最新版本+1，自动从 git 获取 commit 信息）
gdpa-cli run bam-api --session-id "$SESSION_ID" --input '{"action": "create_service_version", "psm": "tiktok.user.service", "branch": "master"}'

# 创建新版本（指定版本号）
gdpa-cli run bam-api --session-id "$SESSION_ID" --input '{"action": "create_service_version", "psm": "tiktok.user.service", "branch": "master", "version": "1.0.62"}'

# 创建新版本（指定版本号和备注）
gdpa-cli run bam-api --session-id "$SESSION_ID" --input '{"action": "create_service_version", "psm": "tiktok.user.service", "branch": "feature/my-branch", "version": "1.0.5", "note": "new release"}'
```

## 注意事项

- `region` 默认为 `cn`（国内），查询国际化服务时需指定 `region` 为 `i18n`
- `create_service_version` 会自动完成三步：① 获取当前最新版本号并+1；② 从 git 获取目标分支最新 commit；③ 创建新版本。业务只需提供 `psm` + `branch` 即可
- **IMPORTANT: YOU MUST** 在调用 `create_service_version` 前向用户确认 psm、branch、即将创建的版本号，用户确认后再执行；执行完毕后将创建结果（版本号、状态）清晰展示给用户
- `create_service_version` 需要登录用户身份，请确保已通过 `gdpa-cli login` 登录
