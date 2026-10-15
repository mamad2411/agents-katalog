---
name: lxcli-kb-get-all-comments
description: "Kanboard: 获取评论列表"
metadata:
  version: 0.0.13
  openclaw:
    category: "productivity"
    requires:
      bins:
        - lxcli
    cliHelp: "lxcli kb getAllComments --help"
---

# kb getAllComments

获取评论列表。

## Usage

```bash
lxcli kb getAllComments --task_id <ID>
lxcli kb getAllComments --params '{"task_id":123}'
```

快捷参数使用见上方；`--params` 用于完整参数场景。若同时传入，CLI 优先使用 `--params`。

## Parameters

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| task_id | integer | ✓ | 需求/bug ID |

## Examples

```bash
lxcli kb getAllComments --task_id <ID>
```
