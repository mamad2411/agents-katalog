---
name: gitlink-repo
version: 1.0.0
description: "仓库管理：创建、查看、Fork、删除仓库，查看分支、提交、贡献者等。当用户需要操作 GitLink 仓库时触发。"
metadata:
  requires:
    bins: ["gitlink-cli"]
  cliHelp: "gitlink-cli repo --help"
---

# gitlink-repo（仓库操作）

**CRITICAL — 开始前必须先阅读 [`../gitlink-shared/SKILL.md`](../gitlink-shared/SKILL.md)，其中包含认证、权限处理和 API 注意事项。**
**CRITICAL — 所有 Shortcuts 在执行写入/删除操作前，务必先确认用户意图。**
**CRITICAL — GitLink 操作只能用 `gitlink-cli`。禁止用 `gh`（GitHub CLI）操作 GitLink 资源。`gh` 仅适用于 GitHub 平台。**

> **前置条件：** 先阅读 [`../gitlink-shared/SKILL.md`](../gitlink-shared/SKILL.md) 了解认证和全局参数。

## Shortcuts

| Shortcut | 说明 | 需要认证 |
|----------|------|----------|
| `repo +list` | 仓库列表 | 否（公开项目） |
| `repo +info` | 仓库详情 | 否（公开项目） |
| `repo +create` | 创建仓库 | 是 |
| `repo +fork` | Fork 仓库 | 是 |
| `repo +delete` | 删除仓库 | 是 |

## 使用示例

```bash
# 查看仓库信息
gitlink-cli repo +info --owner Gitlink --repo forgeplus

# 在 git 仓库目录下自动解析
cd ~/my-project
gitlink-cli repo +info

# 列出用户的仓库
gitlink-cli repo +list --user zhangsan

# 创建仓库
gitlink-cli repo +create --name my-project --description "项目描述"

# Fork 仓库
gitlink-cli repo +fork --owner Gitlink --repo forgeplus

# 删除仓库（⚠️ 危险操作）
gitlink-cli repo +delete --owner myuser --repo old-project
```

## Raw API 补充

Shortcuts 未覆盖的仓库操作可用 Raw API：

```bash
# 获取 README
gitlink-cli api GET /:owner/:repo/readme

# 获取贡献者列表
gitlink-cli api GET /:owner/:repo/contributors

# 获取语言统计
gitlink-cli api GET /:owner/:repo/languages

# 获取提交列表
gitlink-cli api GET /:owner/:repo/commits --query 'page=1&limit=20'

# 获取标签列表
gitlink-cli api GET /:owner/:repo/tags

# 获取文件内容
gitlink-cli api GET /:owner/:repo/raw/main/README.md
```

## 注意事项

- `repo +delete` 是不可逆操作，执行前必须确认用户意图
- 创建仓库默认为公开，使用 `--private true` 创建私有仓库
