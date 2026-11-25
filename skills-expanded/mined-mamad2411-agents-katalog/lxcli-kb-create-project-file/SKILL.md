---
name: lxcli-kb-create-project-file
description: "Kanboard: 上传附件到项目"
metadata:
  version: 0.0.13
  openclaw:
    category: "productivity"
    requires:
      bins:
        - lxcli
    cliHelp: "lxcli kb createProjectFile --help"
---

# kb createProjectFile

上传附件到项目。

## Usage

```bash
lxcli kb createProjectFile --file <VALUE> --project_id <ID>
lxcli kb createProjectFile --params '{"project_id":123,"filename":"value","blob":"value"}'
```

快捷参数使用见上方；`--params` 用于完整参数场景。若同时传入，CLI 优先使用 `--params`。

## Parameters

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| project_id | integer | ✓ | 项目 ID |
| filename | string | ✓ | 文件名 |
| blob | string | ✓ | 文件内容 Base64 编码 |

## Examples

```bash
lxcli kb createProjectFile --file <VALUE> --project_id <ID>
```
