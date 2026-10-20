---
name: bits-devops
description: Manage BITS DevOps workflows — create development tasks, query task info, manage stages, handle project operations, and manage merge requests (create MR, query MR info, code review, QA review, tag binding). Use whenever the user mentions BITS DevOps, development workflow, dev tasks, or BITS merge requests.
---

> **session_id 传递**：若本次任务需要在多次 `gdpa-cli run` 之间串联 workflow 状态、日志或上下文，请复用同一个 `session_id`。如果当前 skill / Agent 已经提供了 `session_id`，**请直接复用，不要新建**。
>
> - **已有时优先复用**：不要重复执行 `create-session`。
> - **没有时再创建**：执行 `gdpa-cli create-session`。
> - **后续调用**：可以显式传 `--session-id <session_id>`，例如 `gdpa-cli run <agent> --session-id <session_id> --input '{...}'`。
> - **适用场景**：Base Workflow、BITS Dev Workflow、post-coding-verify 及其他依赖 Session 工作目录的场景需要持续复用；普通单次查询通常可以不传。

# BITS DevOps 研发效能管理

> **何时使用**: 当需要进行 BITS DevOps 研发效能相关操作时调用此 SKILL，如创建/查询/关闭开发任务、查看空间信息等。

## 使用方法

```bash
gdpa-cli run bits-devops [--session-id <session_id>] --input '{"action": "<action_name>", ...}'
```

> `--session-id` 对 bits-devops 的单次调用是可选的；如果它被放进 bits-dev-workflow 这类多阶段流程中，必须在整条链路里复用同一个 Session ID。

## 认证说明

**无需手动传递 `access_token`**。系统会通过当前登录用户的 JWT 自动从 BITS IAM 获取访问令牌。只需确保已通过 `gdpa-cli login` 登录即可。

| 参数 | 类型 | 说明 |
|------|------|------|
| `access_token` | string | 可选，手动指定 BITS API 令牌（一般无需填写） |
| `user_email` | string | 可选，用户邮箱前缀（一般自动获取） |

参数同时支持 snake_case（`dev_task_id`）和 camelCase（`devTaskId`）两种格式。

## 常用流程

| 流程 | 详细文档 |
|------|----------|
| 任务失败排查 | [SKILL_workflows.md](./SKILL_workflows.md) |

## 关于 space_id

很多 action 需要 `space_id` 参数。如果不知道 space_id，**请先调用 `get_recent_spaces`** 获取用户最近访问的空间列表，让用户选择对应空间后再执行后续操作。

## 支持的 Action 列表

### 空间与配置工具

| Action | 说明 | 需要 space_id | 详细文档 |
|--------|------|:---:|----------|
| `get_recent_spaces` | 获取最近访问的空间列表 | 否 | [SKILL_space_tools.md](./SKILL_space_tools.md) |
| `get_workspace_info` | 获取 BITS 空间基本信息 | **是** | [SKILL_space_tools.md](./SKILL_space_tools.md) |
| `get_dev_templates` | 获取空间的开发任务模板列表 | **是** | [SKILL_space_tools.md](./SKILL_space_tools.md) |
| `get_dev_template_detail` | 获取开发任务模板详情 | 否 | [SKILL_space_tools.md](./SKILL_space_tools.md) |
| `check_template_meego` | 检查模板是否要求关联 Meego 需求 | 否 | [SKILL_space_tools.md](./SKILL_space_tools.md) |
| `get_team_flow` | 获取研发流程配置详情 | 否 | [SKILL_space_tools.md](./SKILL_space_tools.md) |
| `search_projects` | 按关键词搜索项目（需指定 project_type） | 否 | [SKILL_space_tools.md](./SKILL_space_tools.md) |

### 开发任务操作

| Action | 说明 | 需要 space_id | 详细文档 |
|--------|------|:---:|----------|
| `create_dev_task` | 创建开发任务（默认 action） | **是** | [SKILL_dev_task.md](./SKILL_dev_task.md) |
| `add_project_to_dev_task` | 向已有任务新增项目 | 否 | [SKILL_dev_task.md](./SKILL_dev_task.md) |
| `remove_project_from_dev_task` | 从任务删除项目 | 否 | [SKILL_dev_task.md](./SKILL_dev_task.md) |
| `close_dev_task` | 关闭开发任务 | 否 | [SKILL_dev_task.md](./SKILL_dev_task.md) |
| `pass_dev_task_stage` | 通过开发任务阶段 | 否 | [SKILL_dev_task.md](./SKILL_dev_task.md) |
| `run_pipeline` | 运行开发任务流水线 | **是** | [SKILL_dev_task.md](./SKILL_dev_task.md) |

### TCC 配置变更

| Action | 说明 | 需要 space_id | 详细文档 |
|--------|------|:---:|----------|
| `import_tcc_configs` | 导入 TCC 配置到开发任务 | 否 | [SKILL_tcc_config.md](./SKILL_tcc_config.md) |
| `list_tcc_configs` | 查询可导入的 TCC 配置列表 | 否 | [SKILL_tcc_config.md](./SKILL_tcc_config.md) |
| `list_tcc_tags` | 查询 TCC 配置标签 | 否 | [SKILL_tcc_config.md](./SKILL_tcc_config.md) |
| `get_tcc_regions` | 查询 TCC 区域列表 | 否 | [SKILL_tcc_config.md](./SKILL_tcc_config.md) |
| `list_tcc_change_items` | 查询已导入的 TCC 变更项 | 否 | [SKILL_tcc_config.md](./SKILL_tcc_config.md) |
| `get_tcc_change_detail` | 查询变更项配置详情 | 否 | [SKILL_tcc_config.md](./SKILL_tcc_config.md) |
| `get_tcc_change_diff` | 查询配置变更 Diff（基线 vs 草稿） | 否 | [SKILL_tcc_config.md](./SKILL_tcc_config.md) |
| `discard_tcc_change` | 放弃配置变更 | 否 | [SKILL_tcc_config.md](./SKILL_tcc_config.md) |
| `list_tcc_deploy_targets` | 查询可选变更目标（平铺列表 + 互斥标记） | 否 | [SKILL_tcc_config.md](./SKILL_tcc_config.md) |
| `set_tcc_deploy_target` | 设置变更目标（BOE/PPE/Prod） | 否 | [SKILL_tcc_config.md](./SKILL_tcc_config.md) |
| `get_tcc_config_content` | 读取配置内容（草稿/在线版本） | 否 | [SKILL_tcc_config.md](./SKILL_tcc_config.md) |
| `edit_tcc_config` | 编辑配置内容/描述/备注/标签 | 否 | [SKILL_tcc_config.md](./SKILL_tcc_config.md) |
| `add_tcc_config` | 新增配置项（创建全新配置，非导入） | 否 | [SKILL_tcc_config.md](./SKILL_tcc_config.md) |

### 开发任务查询

| Action | 说明 | 需要 space_id | 详细文档 |
|--------|------|:---:|----------|
| `get_opened_dev_task_list` | 获取空间内已开启的开发任务列表 | **是** | [SKILL_dev_task.md](./SKILL_dev_task.md) |
| `get_dev_task_basic_info` | 获取开发任务基本信息 | 否 | [SKILL_dev_task.md](./SKILL_dev_task.md) |
| `get_dev_task_changes` | 获取代码变更列表 | 否 | [SKILL_dev_task.md](./SKILL_dev_task.md) |
| `get_dev_task_project_info` | 获取项目部署配置 | 否 | [SKILL_dev_task.md](./SKILL_dev_task.md) |
| `get_dev_task_lane_info` | 获取泳道环境配置 | 否 | [SKILL_dev_task.md](./SKILL_dev_task.md) |
| `get_dev_task_code_review_info` | 获取代码审查信息 | 否 | [SKILL_dev_task.md](./SKILL_dev_task.md) |
| `get_dev_task_stages` | 获取工作流阶段信息 | 否 | [SKILL_dev_task.md](./SKILL_dev_task.md) |
| `get_dev_task_vars` | 获取变量设置 | 否 | [SKILL_dev_task.md](./SKILL_dev_task.md) |
| `get_dev_task_pipelines` | 获取流水线信息 | 否 | [SKILL_dev_task.md](./SKILL_dev_task.md) |
| `get_pipeline_run` | 获取流水线运行详情（含各 Job 步骤） | 否 | [SKILL_dev_task.md](./SKILL_dev_task.md) |

### MR 操作

| Action | 说明 | 详细文档 |
|--------|------|----------|
| `get_group_projects` | 获取 Group 下项目列表（project_gitlab_id） | [SKILL_mr.md](./SKILL_mr.md) |
| `get_develop_configs` | 获取 Group 开发配置（custom_fields 定义） | [SKILL_mr.md](./SKILL_mr.md) |
| `create_mr` | 创建合并请求 | [SKILL_mr.md](./SKILL_mr.md) |
| `get_mr_basic` | 获取 MR 基本信息 | [SKILL_mr.md](./SKILL_mr.md) |
| `get_mr_branch_detail` | 获取 MR 分支详情 | [SKILL_mr.md](./SKILL_mr.md) |
| `get_mr_repo_state` | 获取 MR 仓库状态/冲突信息 | [SKILL_mr.md](./SKILL_mr.md) |
| `get_mr_graph` | 获取 MR 流水线阶段 | [SKILL_mr.md](./SKILL_mr.md) |
| `get_mr_permission` | 获取 MR 权限 | [SKILL_mr.md](./SKILL_mr.md) |
| `get_mr_host_id` | 获取 MR 宿主项目信息 | [SKILL_mr.md](./SKILL_mr.md) |
| `get_mr_types` | 获取可用 MR 类型 | [SKILL_mr.md](./SKILL_mr.md) |
| `get_tags_list` | 获取标签列表 | [SKILL_mr.md](./SKILL_mr.md) |
| `bind_mr_tags` | 批量绑定标签到 MR | [SKILL_mr.md](./SKILL_mr.md) |
| `get_code_review_detail` | 获取代码审查详情 | [SKILL_mr.md](./SKILL_mr.md) |
| `get_qa_review_status` | 获取 QA 审查状态 | [SKILL_mr.md](./SKILL_mr.md) |
| `start_qa_review` | 启动 QA 审查 | [SKILL_mr.md](./SKILL_mr.md) |
| `get_qa_review_rules` | 获取匹配的 QA 审查规则 | [SKILL_mr.md](./SKILL_mr.md) |
| `get_user_tasks` | 搜索用户 Feature 任务 | [SKILL_mr.md](./SKILL_mr.md) |
| `bind_mr_feature` | 关联 MR 与 Feature 任务（支持多次调用） | [SKILL_mr.md](./SKILL_mr.md) |
| `get_mr_checkpoint` | 获取准入检测信息 | [SKILL_mr.md](./SKILL_mr.md) |
| `get_mr_timeline` | 获取 MR Timeline | [SKILL_mr.md](./SKILL_mr.md) |
| `get_mr_block_error` | 获取 MR 阻塞错误 | [SKILL_mr.md](./SKILL_mr.md) |
| `retry_workflow` | 重试工作流 | [SKILL_mr.md](./SKILL_mr.md) |
| `close_mr` | 关闭 MR | [SKILL_mr.md](./SKILL_mr.md) |
| `sync_target_branch` | 同步目标分支（develop/RC） | [SKILL_mr.md](./SKILL_mr.md) |
