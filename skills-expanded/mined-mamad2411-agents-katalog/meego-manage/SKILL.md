---
name: meego-manage
description: Use when user mention meego. Create, query, get details, update Meego work items, and drive workflow — query workflow detail, update node (schedule/owners/fields), confirm/rollback nodes, or state-flow transitions. Supports project info, work item type discovery, field metadata, and guided creation with auto-fetched field configs (required/optional, defaults, options).
---

> **session_id 传递**：若本次任务需要在多次 `gdpa-cli run` 之间串联 workflow 状态、日志或上下文，请复用同一个 `session_id`。如果当前 skill / Agent 已经提供了 `session_id`，**请直接复用，不要新建**。
>
> - **已有时优先复用**：不要重复执行 `create-session`。
> - **没有时再创建**：执行 `gdpa-cli create-session`。
> - **后续调用**：可以显式传 `--session-id <session_id>`，例如 `gdpa-cli run <agent> --session-id <session_id> --input '{...}'`。
> - **适用场景**：Base Workflow、BITS Dev Workflow、post-coding-verify 及其他依赖 Session 工作目录的场景需要持续复用；普通单次查询通常可以不传。

# Meego Manage Agent

Search and manage Meego work items across projects.

> **When to use**: When you need to find existing Meego tasks/stories/issues to associate, search a user's work items, look up project info, create items, update existing work items, or drive workflow nodes / state transitions.

## Actions

| action | Description |
|---|---|
| `query` (default) | Query Meego work items across projects (includes detailed fields like description/priority/assignee/attachments) |
| `project` | 查询项目信息（返回项目列表及 `name/simple_name/administrators`；传入 `project_key` 时返回该项目详情） |
| `create` | 创建工作项（task/story/issue 等）— **详见 `references/create.md`** |
| `get` | 按 `work_item_id` / `work_item_ids` 取详情，支持 `fields` / `expand` — **详见 `references/get.md`** |
| `update` | 更新工作项字段 — **详见 `references/update.md`** |
| `work_item_types` | 获取空间下全部工作项类型（`type_key` / `name` 等，供后续接口的 `work_item_type_key` 使用；对应 Open API `GET /open_api/{project_key}/work_item/all-types`） |
| `fields` | 获取字段元信息（含 `field_key`、`field_type_key`、select 的 `options` 枚举、`compound_fields` 等；对应 Open API `POST /open_api/{project_key}/field/all`） |
| `template` | 管理本地默认创建模板（`./.gdpa/meego.yaml`）— **详见 `references/create.md`** |
| `query_workflow` | 获取工作项工作流详情（节点 / 状态 / connections / transition_id）— **详见 `references/workflow.md`** |
| `update_node` | 更新节点流的某个节点（排期 / 负责人 / 表单字段 / 角色）— **详见 `references/workflow.md`** |
| `operate_node` | 完成或回滚节点流的某个节点 — **详见 `references/workflow.md`** |
| `state_change` | 状态流工作项跨状态流转（依赖 `transition_id`）— **详见 `references/workflow.md`** |

## 路由：按 action 决定加载哪个 reference

模型应根据用户意图先选定 `action`，再加载对应文档：

| 想做的事 | 必读文件 |
|---|---|
| 查询工作项列表 / 项目信息 / 工作项类型 / 字段元数据 | 仅本 SKILL.md（参数都在下方表里） |
| 新建工作项、管理本地创建模板 | + `references/create.md` |
| 取工作项详情 | + `references/get.md` |
| 修改工作项字段 | + `references/update.md` |
| 流程相关：查工作流、改节点、推/回滚节点、状态流转 | + `references/workflow.md` |

> reference 文件在 skill 安装时已一并复制到本目录。请直接 read（`./references/<name>.md`），不要再尝试重新拉取。

## 关键参数规范（按 action）

| action | 是否需要 `project_key` | 获取方式 |
|---|---|---|
| `query` | 否 | 可选传入；不传则跨项目查询 |
| `project` | 否（推荐传） | 不传时列出所有项目；传入时返回该项目详情 |
| `create` | 是 | 优先显式传入；否则自动读取 `./.gdpa/meego.yaml` |
| `get` | 是 | 优先显式传入；否则自动读取 `./.gdpa/meego.yaml` |
| `update` | 是 | 优先显式传入；否则自动读取 `./.gdpa/meego.yaml` |
| `work_item_types` | 是 | 与 `create/get/update` 相同；需空间 `project_key` 或本地 `./.gdpa/meego.yaml` |
| `fields` | 是 | 同上；**可选**传入 `work_item_type_key` 限定某一工作项类型（建议先 `work_item_types` 再 `fields`）；不传则拉取该空间下全量字段定义 |
| `query_workflow` | 是 | 同 `create/get/update`；额外必传 `work_item_id`，可选 `flow_type`（0=节点流，1=状态流）/ `fields` / `expand` |
| `update_node` | 是 | 同上；额外必传 `work_item_id` 和 `node_id`（先 `query_workflow` 拿） |
| `operate_node` | 是 | 同上；额外必传 `work_item_id` / `node_id` / `node_action`（`confirm` 或 `rollback`），`rollback` 时必填 `rollback_reason` |
| `state_change` | 是 | 同上；额外必传 `work_item_id` 和 `transition_id`（用 `query_workflow` 配 `flow_type=1` 拿） |

## 本地持久化约定（多 action 共享）

**配置文件**：`./.gdpa/meego.yaml`（仅当前仓库生效，不提交到代码库）

存储 `project_key` 用于兜底（`create/get/update/workflow*` 不传时自动读取），以及按 `(project_key, work_item_type_key)` 索引的本地创建模板。

**Agent 应主动保存的情况**：
- `action=project` + 传入了 `project_key` 时 → 将 `project_key` 和返回的详情写入 `./.gdpa/meego.yaml`
- `action=query/get/create/update` + 传入了 `project_key` 时 → 同样写入本地配置

**Agent 应读取本地配置的情况**：
- `action=create/get/update/workflow*` 且未传入 `project_key` 时 → 读取 `./.gdpa/meego.yaml` 中的 `project.key`

**返回时附带的可解释信息**：
- 当使用了本地配置的 `project_key` 时，结果中会包含 `meta.project_source = "local_config"`

**完整 schema 与本地模板（`templates: [...]`）字段定义**见 `references/create.md`。

## 鉴权

默认用 `gdpa-cli login cn` 后的身份调用，无需手动传参。如果默认身份不对（如 bot 账号、非 bytedance 邮箱），可在 input 显式覆盖：

- `"email": "<your-email>"` — 走 Meego 反查拿 user_key
- `"user_key": "<your-user-key>"` — 直接用，跳过反查

两者都拿不到时 agent 会立即报错并提示。
