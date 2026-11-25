---
name: complex-task-planner
version: 2.0.0
description: "复杂多步骤任务规划与分步执行。任务需要计划、todo、跨多个工具/网站/文件、需要继续/暂停/失败恢复时使用。必须使用内置 TodoWrite 工具维护完整任务清单和进度。"
allowed-tools: Bash(*)
---

# 复杂任务规划与执行

## 何时启用

满足任意 2 条即视为复杂任务，必须先使用本 skill：

1. 用户目标需要 3 个及以上独立步骤才能完成
2. 涉及多个网站、工具、Skill、文件操作或 Bash/webcli
3. 需要先调研现状再决定下一步
4. 存在分支、不确定性、失败恢复或需要重试
5. 用户明确说“分步”“计划”“todo”“多步完成”“继续”“暂停后继续”
6. 当前对话已经存在未完成 Todo List

简单单步任务不要启用本 skill。

## 核心规则

- 计划和进度的唯一来源是内置 `TodoWrite` 工具。
- 创建计划时，必须调用 `TodoWrite`，写入完整 todo 列表。
- 每次开始、继续、完成、阻塞、修改、新增或删除 todo 时，必须再次调用 `TodoWrite`。
- `TodoWrite.todos` 是完整最新列表，不是增量 diff。
- 已完成 todo 不得修改、删除或回退状态。
- 未完成 todo 可以修改、删除、新增、重排或调整状态。
- 当前计划未完成、失败或中止时，不要重开新计划；继续原 TodoWrite 列表并只调整未完成项。
- 全部 todo 完成后，当前计划结束；后续新目标才创建新的 TodoWrite 列表。
- 同一时间最多 1 个 todo 为 `in_progress`。

## TodoWrite 格式

调用 `TodoWrite` 时，每个 todo 应包含：

- `content`: 对用户可读的步骤标题
- `status`: `pending`、`in_progress` 或 `completed`
- `activeForm`: 正在执行该步骤时的动词短语
- `blocked_reason` 或 `failure_reason`: 可选；当当前 `in_progress` 项受阻、失败、超时、连续重试失败或需要用户介入时填写原因。若 `status` 为 `in_progress` 且原因非空，前端会显示为失败；否则你也可以把该项改回 `pending`、调整后续计划或删除未完成项。

示例：

```json
{
  "todos": [
    {
      "content": "第1步：检查当前登录状态",
      "status": "in_progress",
      "activeForm": "检查当前登录状态"
    },
    {
      "content": "第2步：读取目标页面数据",
      "status": "pending",
      "activeForm": "读取目标页面数据"
    },
    {
      "content": "第3步：整理结果并回复用户",
      "status": "pending",
      "activeForm": "整理结果并回复用户"
    }
  ]
}
```

## 执行流程

1. 判断任务复杂度。
2. 如果需要计划，先调用 `TodoWrite` 创建完整列表。
3. 执行当前 `in_progress` todo。
4. 当前 todo 完成后，调用 `TodoWrite`：将它设为 `completed`，并将下一项设为 `in_progress`。
5. 遇到阻塞、失败、超时或连续重试失败时，说明原因，并调用 `TodoWrite`：由你决定该项继续 `in_progress` 并写入 `blocked_reason`/`failure_reason` 以显示失败，或改回 `pending`，或调整/删除未完成计划；不要修改已完成项。
6. 所有 todo 都是 `completed` 后，正常收尾。

## 回复要求

- 可以用自然语言向用户解释进度，但进度事实必须同步写入 `TodoWrite`。
- 不要只说“第 N 步完成/开始”而不调用 `TodoWrite`。
- 不要把计划写成普通 Markdown 表格来代替 `TodoWrite`。
