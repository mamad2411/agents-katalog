---
name: lxcli-kb-move-task-position
description: "Kanboard: 移动需求状态列"
metadata:
  version: 0.0.13
  openclaw:
    category: "productivity"
    requires:
      bins:
        - lxcli
    cliHelp: "lxcli kb moveTaskPosition --help"
---

# kb moveTaskPosition

移动需求状态列。

## Usage

```bash
lxcli kb moveTaskPosition --params '{"project_id":123,"task_id":123,"column_id":123,"position":123,"swimlane_id":123}'
```

## Parameters

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| project_id | integer | ✓ | 项目 ID。必须是任务所属项目。 |
| task_id | integer | ✓ | 需求/bug ID |
| column_id | integer |  | 目标状态列 ID。未传时保留当前状态列 |
| position | integer |  | 目标列内排序位置，必须 >= 1。未传时保留当前排序值 |
| swimlane_id | integer |  | 目标泳道 ID。未传或传 0 保留当前泳道 |

## Examples

```bash
lxcli kb moveTaskPosition --params '{"project_id":123,"task_id":123,"column_id":123,"position":123,"swimlane_id":123}'
```
