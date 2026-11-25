---
name: lxcli-kb-search-subtasks
description: "Kanboard: 搜索子任务列表"
metadata:
  version: 0.0.13
  openclaw:
    category: "productivity"
    requires:
      bins:
        - lxcli
    cliHelp: "lxcli kb searchSubtasks --help"
---

# kb searchSubtasks

搜索子任务列表。

## Usage

```bash
lxcli kb searchSubtasks --project_id <ID> --iteration_id <ID> --user_id <ID> --page <ID>
lxcli kb searchSubtasks --params '{"project_id":123,"iteration_id":123,"user_id":123,"page":123}'
```

快捷参数使用见上方；`--params` 用于完整参数场景。若同时传入，CLI 优先使用 `--params`。

## Parameters

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| project_id | integer |  | 项目 ID。传入后仅返回该项目下的子任务，并按项目检查查看权限；不传时仅在当前用户有权限查看的启用项目中查找。 |
| iteration_id | integer |  | 迭代 ID。传入后仅返回所属需求在该迭代下的子任务；不传表示不限制迭代。 |
| user_id | integer |  | 处理人 ID。传入后仅返回该处理人的子任务；不传或传 0 表示不限制处理人。 |
| page | integer |  | 页码，从 1 开始，默认 1。每页固定最多 30 条，按页翻取。 |

## Examples

```bash
lxcli kb searchSubtasks --project_id <ID> --iteration_id <ID> --user_id <ID> --page <ID>
```
