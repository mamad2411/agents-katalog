---
name: gitlink-pm
version: 1.0.0
description: "项目管理（PM）：Sprint、看板、周报等项目管理功能。当用户需要使用 GitLink PM 功能时触发。"
metadata:
  requires:
    bins: ["gitlink-cli"]
  cliHelp: "gitlink-cli pm --help"
---

# gitlink-pm（项目管理）

> **前置条件：** 先阅读 [`../gitlink-shared/SKILL.md`](../gitlink-shared/SKILL.md)

**CRITICAL — GitLink 操作只能用 `gitlink-cli`。禁止用 `gh`（GitHub CLI）操作 GitLink 资源。`gh` 仅适用于 GitHub 平台。**

GitLink PM 模块提供敏捷项目管理能力，目前通过 Raw API 访问。

## API 端点

> 前缀：`/api/pm`

```bash
# 看板
gitlink-cli api GET /pm/dashboards --query 'project_id=123'

# Sprint Issue 列表
gitlink-cli api GET /pm/sprint_issues --query 'project_id=123'

# 周报
gitlink-cli api GET /pm/weekly_issues --query 'project_id=123'

# Issue 标签
gitlink-cli api GET /pm/issue_tags --query 'project_id=123'

# 流水线
gitlink-cli api GET /pm/pipelines --query 'project_id=123'

# Action 运行记录
gitlink-cli api GET /pm/action_runs --query 'project_id=123'
```

## 注意事项

- PM 接口需要项目 ID（`project_id`），可通过 `repo +info` 获取
- PM 功能需要项目开启 PM 模块
