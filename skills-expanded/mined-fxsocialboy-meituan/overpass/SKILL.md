---
name: overpass
description: Retrieve service IDL information, list interface methods with AI-generated comments, trigger Overpass code generation for client stubs, and manage project-level repos (query, force refresh, branch update). Use whenever the user mentions Overpass, wants to generate client code for calling another service, needs to see a service's method list, wants to know a service's IDL path/repo info, needs to trigger code generation, or wants to manage Overpass project-level repos. This is for reading IDL metadata and generating client code — for editing IDL files use edit-idl.
---

> **session_id 传递**：若本次任务需要在多次 `gdpa-cli run` 之间串联 workflow 状态、日志或上下文，请复用同一个 `session_id`。如果当前 skill / Agent 已经提供了 `session_id`，**请直接复用，不要新建**。
>
> - **已有时优先复用**：不要重复执行 `create-session`。
> - **没有时再创建**：执行 `gdpa-cli create-session`。
> - **后续调用**：可以显式传 `--session-id <session_id>`，例如 `gdpa-cli run <agent> --session-id <session_id> --input '{...}'`。
> - **适用场景**：Base Workflow、BITS Dev Workflow、post-coding-verify 及其他依赖 Session 工作目录的场景需要持续复用；普通单次查询通常可以不传。

# Overpass 工具

> **何时使用**: 当需要获取服务 IDL 信息、查看接口方法列表、生成 overpass 代码、或管理项目维度仓库时调用此 SKILL。

## 使用方法

```bash
gdpa-cli run overpass --session-id "$SESSION_ID" --input '{"action": "<action>", ...}'
```

## 支持的 Action

### PSM 维度

| Action | 描述 | 必填参数 | 可选参数 |
|--------|------|----------|----------|
| `get_psm_idl_info` | 获取服务 IDL 路径和仓库信息（GitType: 0=gitlab, 1=gerrit） | psm | |
| `get_psm_repo_info` | 获取服务 overpass repo 路径、method 路径、主结构体路径及操作指令 | psm | biz, branch, framework_type |
| `get_psm_method_list` | 获取服务的 IDL 方法列表（含 AI 生成注释） | psm | branch |
| `generate_psm_repo` | 触发代码生成并轮询等待完成后返回结果 | psm | biz, branch, framework_type, kitex_version |
| `get_settings` | 获取 Overpass 平台设置（KitexVersions 等） | | |

### 项目维度

> 项目维度 action 统一支持 `repo_name` 或 `project_id` **二选一**，传任意一个即可自动互查补全另一个。

| Action | 描述 | 必填参数 | 可选参数 |
|--------|------|----------|----------|
| `query_project_repo` | 查询项目维度仓库列表（repo_name 模糊搜索或 project_id 精确查询） | repo_name 或 project_id（二选一） | page, page_size |
| `force_refresh_project_repo` | 强制刷新项目维度仓库（触发重新生成并轮询等待完成） | repo_name 或 project_id（二选一） | |
| `update_project_branch` | 创建或更新项目维度的分支生成配置（默认订阅人为当前用户） | branch + (repo_name 或 project_id 二选一) | subscribe_users |

## 输入参数

| 参数 | 类型 | 描述 |
|------|------|------|
| action | string | 必填，要执行的操作 |
| psm | string | PSM 维度 action 必填，PSM（项目服务名） |
| biz | string | 可选，业务线（支持 overpass、tikcast、webcastv2、oecv2）。未指定时自动从 PSM 已有配置获取，查不到则默认 overpass |
| branch | string | 可选，分支名称。PSM 维度默认 master；项目维度 update_project_branch 时必填 |
| framework_type | int | 可选，框架类型（0=KiteX, 1=Hertz, 2=Lust, 3=Euler, 4=Jet, 5=JS）。未指定时自动从 PSM 已有配置获取，查不到则默认 0(KiteX) |
| kitex_version | string | 可选，指定 kitex 版本。可选值：v1.20.3、v1.19.4、v1.18.4、v1.15.3、v1.11.6。未指定时自动从 PSM 已有配置获取，查不到则降级到平台默认版本 |
| repo_name | string | 项目维度操作时可选，仓库名（支持模糊搜索）。与 project_id 二选一 |
| project_id | int | 项目维度操作时可选，项目 ID。与 repo_name 二选一，可通过 query_project_repo 获取 |
| page | int | 可选，分页页码，默认 1 |
| page_size | int | 可选，每页数量，默认 10 |
| subscribe_users | []string | 可选，订阅用户列表。不指定时默认使用当前登录用户 |

## 输出格式

```json
{
  "success": true,
  "action": "get_psm_idl_info",
  "data": { ... }
}
```

## 示例

```bash
# === PSM 维度 ===

# 获取服务 IDL 基础信息
gdpa-cli run overpass --session-id "$SESSION_ID" --input '{"action": "get_psm_idl_info", "psm": "tiktok.user.service"}'

# 获取服务 overpass 代码生成信息
gdpa-cli run overpass --session-id "$SESSION_ID" --input '{"action": "get_psm_repo_info", "psm": "tiktok.user.service"}'

# 指定业务线和分支
gdpa-cli run overpass --session-id "$SESSION_ID" --input '{"action": "get_psm_repo_info", "psm": "tiktok.user.service", "biz": "tikcast", "branch": "develop"}'

# 获取服务的 IDL 方法列表（包含 IDL 方法名、GO 方法名、AI 分析的方法注释）
gdpa-cli run overpass --session-id "$SESSION_ID" --input '{"action": "get_psm_method_list", "psm": "tiktok.user.service"}'

# 生成 PSM 对应的 overpass 代码（master 分支）
gdpa-cli run overpass --session-id "$SESSION_ID" --input '{"action": "generate_psm_repo", "psm": "tiktok.user.service"}'

# 生成指定分支的 overpass 代码
gdpa-cli run overpass --session-id "$SESSION_ID" --input '{"action": "generate_psm_repo", "psm": "tiktok.user.service", "branch": "feature-xxx"}'

# 指定 kitex 版本生成（适用于 IDL 过大的 PSM）
gdpa-cli run overpass --session-id "$SESSION_ID" --input '{"action": "generate_psm_repo", "psm": "ttec.cart.product", "kitex_version": "v1.18.4"}'

# 获取平台设置
gdpa-cli run overpass --session-id "$SESSION_ID" --input '{"action": "get_settings"}'

# === 项目维度（repo_name 或 project_id 二选一，自动互查补全） ===

# 通过 repo_name 模糊搜索
gdpa-cli run overpass --session-id "$SESSION_ID" --input '{"action": "query_project_repo", "repo_name": "toutiao_comment_"}'

# 通过 project_id 精确查询
gdpa-cli run overpass --session-id "$SESSION_ID" --input '{"action": "query_project_repo", "project_id": 492}'

# 强制刷新 —— 用 repo_name
gdpa-cli run overpass --session-id "$SESSION_ID" --input '{"action": "force_refresh_project_repo", "repo_name": "ttam_monorepo"}'

# 强制刷新 —— 用 project_id
gdpa-cli run overpass --session-id "$SESSION_ID" --input '{"action": "force_refresh_project_repo", "project_id": 492}'

# 创建/更新项目分支 —— 用 repo_name
gdpa-cli run overpass --session-id "$SESSION_ID" --input '{"action": "update_project_branch", "repo_name": "ttam_monorepo", "branch": "feat-test"}'

# 创建/更新项目分支 —— 用 project_id（默认订阅当前用户）
gdpa-cli run overpass --session-id "$SESSION_ID" --input '{"action": "update_project_branch", "project_id": 492, "branch": "feat-test"}'

# 指定订阅用户
gdpa-cli run overpass --session-id "$SESSION_ID" --input '{"action": "update_project_branch", "project_id": 492, "branch": "feat-test", "subscribe_users": ["alice", "bob"]}'
```

## 注意事项

- `generate_psm_repo` 触发生成后轮询等待完成即返回，最长等待 5 分钟
- `generate_psm_repo` 的 `kitex_version`、`framework_type`、`biz` 三个参数均按三级降级获取：用户指定 > PSM 已有平台配置 > 默认值。对于 IDL 过大的 PSM，Overpass 平台通常已配置优化的 kitex 版本（如 v1.18.4），会自动使用
- 项目维度所有 action 支持 `repo_name` 或 `project_id` **二选一**，传任意一个即可，系统会自动查询补全另一个
- `force_refresh_project_repo` 触发刷新后会轮询 `query_project_repo` 等待状态从 Creating 变为 Done，最长等待 5 分钟
- `update_project_branch` 不指定 `subscribe_users` 时自动使用当前登录用户作为订阅人
- 项目维度仓库状态：Creating（生成中）、Done（已完成）
- 项目维度文档参考：https://bytedance.larkoffice.com/wiki/M3LxwvKiKieoVLkkkn0cW3Y3n7c