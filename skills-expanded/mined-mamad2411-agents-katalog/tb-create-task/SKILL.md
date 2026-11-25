---
name: tb-create-task
description: 在 TeamBition 项目中创建新任务
allowed-tools: Bash(node *), Read, Edit
---

# 创建 TeamBition 任务

**缓存优先**：模板和工作流状态从 `.teambition.cache.md` 读取。如果缓存不存在，提示先执行 `/tb-sync`。
**重要**：必须严格按步骤执行，**不得跳过任何步骤**。

## 步骤 1（必须）：选择项目

读取 `.teambition.md` 中的常用项目。用 `AskUserQuestion`（单选）让用户选择。

## 步骤 2（必须）：选择任务类型

**不得跳过。** 读取 `.teambition.cache.md` 中该项目的"### 模板"表格。
只展示 **Taskflow ID 不为 `-`** 的模板。
用 `AskUserQuestion`（单选）让用户选择。label: 模板名称，description: Template ID。

## 步骤 3（必须）：选择工作流状态

**不得跳过。** 读取 `.teambition.cache.md` 中该项目的"### 工作流状态"表格。
只展示**工作流 ID 等于步骤 2 选中模板的 Taskflow ID** 的状态。
用 `AskUserQuestion`（单选）让用户选择。label: 状态名称，description: 状态 ID。

## 步骤 4（必须）：填写任务信息

在对话中问用户（自由文本）：
> 请提供以下信息：
> 1. **任务标题**（必填，支持多个，每行一个或分号分隔）
> 2. **任务备注**（选填，所有任务共用）
> 3. **截止日期**（选填，如 2026-04-30 或 "下周五"，所有任务共用）

## 步骤 5（必须）：选择优先级

用 `AskUserQuestion`（单选），option: 无(0) / 低(1) / 中(2) / 高(3)。

## 步骤 6：批量创建任务

对每个标题执行：
```bash
node ${CLAUDE_SKILL_DIR}/scripts/tb-api.mjs create-task --projectId <ID> --content "<标题>" --note "<备注>" --priority <N> --dueDate <ISO> --templateId <步骤2的ID>
```

## 步骤 7：设置工作流状态

如果步骤 3 选的不是第一个 start 状态，对每个新任务执行：
```bash
node ${CLAUDE_SKILL_DIR}/scripts/tb-api.mjs update-task-status --taskId <ID> --projectId <ID> --statusId <步骤3的ID>
```

## 步骤 8：更新最近任务

用 Edit 追加到 `.teambition.md` 最近任务表格。

## 步骤 9：展示结果

以表格展示所有创建结果。
