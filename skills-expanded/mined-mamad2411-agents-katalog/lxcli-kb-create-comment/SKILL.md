---
name: lxcli-kb-create-comment
description: "Kanboard: 对需求增加评论"
metadata:
  version: 0.0.13
  openclaw:
    category: "productivity"
    requires:
      bins:
        - lxcli
    cliHelp: "lxcli kb createComment --help"
---

# kb createComment

对需求增加评论。

## Usage

```bash
lxcli kb createComment --task_id <ID> --user_id <ID> --content <VALUE>
lxcli kb createComment --params '{"task_id":123,"user_id":123,"content":"value","reference":"value"}'
```

快捷参数使用见上方；`--params` 用于完整参数场景。若同时传入，CLI 优先使用 `--params`。

## Parameters

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| task_id | integer | ✓ | 需求/bug ID |
| user_id | integer | ✓ | 评论作者 Kanboard 用户 ID |
| content | string | ✓ | 评论内容（支持 Markdown） |
| reference | string |  | 外部引用，如 Meet 消息 ID |

## Examples

```bash
lxcli kb createComment --task_id <ID> --user_id <ID> --content <VALUE>
```
