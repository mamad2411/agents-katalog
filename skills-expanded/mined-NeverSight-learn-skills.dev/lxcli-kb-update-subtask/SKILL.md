---
name: lxcli-kb-update-subtask
description: "Kanboard: 更新子任务"
metadata:
  version: 0.0.13
  openclaw:
    category: "productivity"
    requires:
      bins:
        - lxcli
    cliHelp: "lxcli kb updateSubtask --help"
---

# kb updateSubtask

更新子任务。

## Usage

```bash
lxcli kb updateSubtask --params '{"id":123,"task_id":123,"title":"value","user_id":123,"time_estimated":"value","time_spent":"value","status":123,"position":123,"plan_begin_time":"value","plan_end_time":"value"}'
```

## Parameters

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| id | integer | ✓ | 子任务 ID |
| task_id | integer | ✓ | 父需求/bug ID。接口按该任务检查项目权限。 |
| title | string |  | 子任务标题 |
| user_id | integer |  | 子任务处理人 Kanboard 用户 ID。传 0 表示未分配。 |
| time_estimated | number |  | 预估时间，最多保留两位小数 |
| time_spent | number |  | 已花费时间，最多保留两位小数 |
| status | integer |  | 子任务状态：0 未开始，1 进行中，2 已完成 |
| position | integer |  | 子任务排序位置 |
| plan_begin_time | string |  | 计划开始时间，格式 YYYY-MM-DD |
| plan_end_time | string |  | 计划结束时间，格式 YYYY-MM-DD |

## Examples

```bash
lxcli kb updateSubtask --params '{"id":123,"task_id":123,"title":"value","user_id":123,"time_estimated":"value","time_spent":"value","status":123,"position":123,"plan_begin_time":"value","plan_end_time":"value"}'
```
