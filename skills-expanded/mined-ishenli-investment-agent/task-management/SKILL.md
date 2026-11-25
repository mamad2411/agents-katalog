---
name: task-management
description: >
  创建、查询、跟进用户的投资任务：跟踪投资建议、价格触发条件、定期监控、到期提醒。
  当用户说"帮我盯着 XX"、"到 XX 价格提醒我"、"记个任务"、"我的待办/任务"、"跟进一下上次说的"，
  或对话中产生了明确的待办结论（如"进一步研究这只股票"）时，**务必使用此技能**。
version: "1.0.0"
category: tasks
author: investment-agent
---

# 投资任务管理

## 创建任务：createTaskTool

| 参数 | 说明 |
|------|------|
| `title` | 必填，一句话任务标题 |
| `description` | 任务的详细说明 / 监控条件 |
| `type` | `one_time` 一次性 / `price_trigger` 价格触发 / `monitoring` 持续监控 / `date_driven` 日期驱动，默认 `one_time` |
| `priority` | `low` / `medium` / `high` / `urgent`，默认 `medium` |
| `linked_symbols` | 关联资产代码列表，如 `["AAPL", "NVDA"]` |
| `due_date` | 截止日期（YYYY-MM-DD） |
| `source_type` | `agent_chat`（默认）/ `analysis_report` / `manual` |

典型场景映射：

- "跌破 150 提醒我" → type=`price_trigger`，description 写明触发条件与数值，linked_symbols 填代码。
- "每周看看美联储动向" → type=`monitoring` 或 `date_driven`。
- 本次分析给出的待办（如"下个财报季再评估"）→ 主动建议创建任务而非口头承诺，经用户确认后创建。

## 查询：listTasksTool

支持 `status`（pending / in_progress / completed / cancelled / expired）、`priority`、`search` 关键词、`limit` / `offset`。

- 用户问"我的任务/待办"→ 默认列 pending + in_progress，按优先级排序呈现。
- `expired` 状态的任务一并提示，让用户决定是否重建或取消。

## 更新：updateTaskTool

- 必填 `task_id`（从 listTasks 结果中取，**禁止编造 ID**）。
- 可更新 `status`（completed / cancelled / in_progress / pending）、`title`、`description`、`priority`、`linked_symbols`。
- 用户说"完成了/取消那个任务"→ 完成用 `completed`，明确放弃用 `cancelled`，不确定问一句。
