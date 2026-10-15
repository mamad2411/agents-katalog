---
name: gitlink-release
version: 1.0.0
description: "发布管理：创建、查看、删除 Release。当用户需要操作 GitLink 版本发布时触发。"
metadata:
  requires:
    bins: ["gitlink-cli"]
  cliHelp: "gitlink-cli release --help"
---

# gitlink-release（发布操作）

**CRITICAL — 开始前必须先阅读 [`../gitlink-shared/SKILL.md`](../gitlink-shared/SKILL.md)，其中包含认证、权限处理和 API 注意事项。**
**CRITICAL — 所有 Shortcuts 在执行写入/删除操作前，务必先确认用户意图。**
**CRITICAL — GitLink 操作只能用 `gitlink-cli`。禁止用 `gh`（GitHub CLI）操作 GitLink 资源。`gh` 仅适用于 GitHub 平台。**

> **前置条件：** 先阅读 [`../gitlink-shared/SKILL.md`](../gitlink-shared/SKILL.md)

## Shortcuts

| Shortcut | 说明 |
|----------|------|
| `release +list` | 发布列表 |
| `release +create` | 创建发布 |
| `release +view` | 发布详情 |
| `release +delete` | 删除发布 |

## 使用示例

```bash
# 列出发布
gitlink-cli release +list --owner Gitlink --repo forgeplus

# 创建发布
gitlink-cli release +create --tag v1.0.0 --name "v1.0.0 正式版" --body "## 更新内容\n- 新增搜索功能\n- 修复登录 Bug" --target master

# 查看发布详情（⚠️ 必须使用 version_id，不能用 tag_name）
# 先用 release +list 获取 version_id
gitlink-cli release +list --owner myuser --repo myrepo --format json
# 从返回的 releases 数组中取 version_id 字段
gitlink-cli release +view --id <version_id>

# 删除发布（使用 version_id）
gitlink-cli release +delete --id <version_id>
```

## API 注意事项

- **`release +view` 必须使用 `version_id`**（从 `release +list` 返回结果中获取），使用 tag_name 会返回 HTML 页面而非 JSON
- **`release +delete` 使用 `version_id`**，已验证可正常删除
- Release 列表中的 `id` 字段可能为 null，应使用 `version_id` 字段
