---
name: gitlink-issue
version: 2.0.0
description: "Issue 管理：创建、查看、更新、关闭/批量关闭 Issue，添加评论。当用户需要操作 GitLink Issue 时触发。"
metadata:
  requires:
    bins: ["gitlink-cli"]
  cliHelp: "gitlink-cli issue --help"
---

# gitlink-issue（Issue 操作）

**CRITICAL — 开始前必须先阅读 [`../gitlink-shared/SKILL.md`](../gitlink-shared/SKILL.md)，其中包含认证、权限处理和 API 注意事项。**
**CRITICAL — 所有 Shortcuts 在执行写入/删除操作前，务必先确认用户意图。**
**CRITICAL — GitLink 操作只能用 `gitlink-cli`。禁止用 `gh`（GitHub CLI）操作 GitLink 资源。`gh` 仅适用于 GitHub 平台。**

> **前置条件：** 先阅读 [`../gitlink-shared/SKILL.md`](../gitlink-shared/SKILL.md) 了解认证和全局参数。

## Shortcuts

| Shortcut | 说明 | 需要认证 |
|----------|------|----------|
| `issue +list` | Issue 列表 | 否（公开项目） |
| `issue +create` | 创建 Issue | 是 |
| `issue +view` | Issue 详情 | 否（公开项目） |
| `issue +update` | 更新 Issue | 是 |
| `issue +close` | 关闭 Issue | 是 |
| `issue +batch-close` | 批量关闭 Issue，支持 `--dry-run` 预览 | 是（dry-run 不写入） |
| `issue +comment` | 添加评论 | 是 |

## 使用示例

```bash
# 列出 Issue
gitlink-cli issue +list --owner Gitlink --repo forgeplus --state open

# 创建 Issue
gitlink-cli issue +create --owner myuser --repo myrepo --title "Bug: 登录失败" --body "复现步骤：..."

# 查看 Issue 详情（使用网页可见的 Issue 编号）
gitlink-cli issue +view --owner Gitlink --repo forgeplus --number 4

# 更新 Issue
gitlink-cli issue +update --number 4 --title "新标题" --body "更新描述"

# 关闭 Issue
gitlink-cli issue +close --number 4

# 预览批量关闭 Issue，不修改数据
gitlink-cli issue +batch-close --owner myuser --repo myrepo --numbers 123,124 --dry-run

# 从 CSV 文件批量关闭 Issue
gitlink-cli issue +batch-close --owner myuser --repo myrepo --from issues.csv

# 添加评论
gitlink-cli issue +comment --number 4 --body "已修复，请验证"
```

## Raw API 补充

```bash
# 获取 Issue 评论列表（使用 v1 API，按 issue number 查询）
gitlink-cli api GET /v1/:owner/:repo/issues/:number/journals

# 批量更新 Issue（仍使用旧版 API，需传数据库 ID）
gitlink-cli api POST /:owner/:repo/issues/series_update --body '{"ids":[1,2,3],"status_id":"closed"}'
```

## GitLink Issue 字段映射

| gitlink-cli 参数 | GitLink API 字段 | 说明 |
|------------------|-----------------|------|
| `--number` / `-n` | `project_issues_index` | Issue 编号（网页 URL 中的序号） |
| `--title` | `subject` | Issue 标题 |
| `--body` | `description` | Issue 描述 |
| `--assignee` | `assigned_to_id` | 指派人 ID |
| `--milestone` | `fixed_version_id` | 里程碑 ID |
| `--state` | `status_id` | 状态（open=1，closed=5，也可直接传数字 ID） |

## API 注意事项

- **Issue 编号（`--number`）是网页 URL 中看到的序号**（如 `issues/4` 中的 `4`），不是数据库内部 ID
- **批量关闭使用 `--numbers`，同样传网页 URL 中的 Issue 编号**，不是数据库内部 ID
- Issue 操作使用 v1 API（`/api/v1/`），支持按 Issue 编号查询和操作
- **创建 Issue 时 CLI 会自动设置 `status_id: 1`（新增）和 `priority_id: 2`（正常）**
- **更新/关闭 Issue 时必须保留当前 `subject` 和 `description`**，即使只修改状态（CLI 会先读取当前 Issue 并自动带回）
- v1 API 写操作必须使用 `access_token`（非 `token`）认证，CLI 已自动处理

## Issue 状态映射（status_id）

| status_id | 名称 | 说明 |
|-----------|------|------|
| 1 | 新增 | 新建 Issue 的默认状态 |
| 2 | 正在解决 | 处理中 |
| 3 | 已解决 | 已修复 |
| 5 | 关闭 | 关闭（`+close` 命令使用此值） |
