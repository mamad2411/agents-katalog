---
name: tb-update-task-status
description: 更新任务的工作流状态
allowed-tools: Bash(node *), Read, Edit
---

# 更新任务状态

**缓存优先**：工作流状态从 `.teambition.cache.md` 读取。如果缓存不存在，提示先执行 `/tb-sync`。

## 步骤

1. 读取 `.teambition.md` 常用项目，用 `AskUserQuestion`（单选）选择项目
2. 执行 `node ${CLAUDE_SKILL_DIR}/scripts/tb-api.mjs get-project-tasks --projectId <ID>` 获取任务列表（实时）
3. 用 `AskUserQuestion`（单选）选择任务
4. 读取 `.teambition.cache.md` 中该项目的"### 工作流状态"表格，用 `AskUserQuestion`（单选）选择目标状态
5. 执行：
```bash
node ${CLAUDE_SKILL_DIR}/scripts/tb-api.mjs update-task-status --taskId <ID> --projectId <ID> --statusId <ID>
```
6. 更新 `.teambition.md` 最近任务记录
