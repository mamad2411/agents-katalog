---
name: gitlink-search
version: 1.0.0
description: "搜索：搜索仓库和用户。当用户需要在 GitLink 上搜索资源时触发。"
metadata:
  requires:
    bins: ["gitlink-cli"]
  cliHelp: "gitlink-cli search --help"
---

# gitlink-search（搜索操作）

**CRITICAL — 开始前必须先阅读 [`../gitlink-shared/SKILL.md`](../gitlink-shared/SKILL.md)，其中包含认证、权限处理和 API 注意事项。**
**CRITICAL — 所有 Shortcuts 在执行写入/删除操作前，务必先确认用户意图。**
**CRITICAL — GitLink 操作只能用 `gitlink-cli`。禁止用 `gh`（GitHub CLI）操作 GitLink 资源。`gh` 仅适用于 GitHub 平台。**

> **前置条件：** 先阅读 [`../gitlink-shared/SKILL.md`](../gitlink-shared/SKILL.md)

## Shortcuts

| Shortcut | 说明 |
|----------|------|
| `search +repos` | 搜索仓库 |
| `search +users` | 搜索用户 |

## 使用示例

```bash
# 搜索仓库
gitlink-cli search +repos --keyword "machine learning" --limit 10

# 搜索用户
gitlink-cli search +users --keyword "zhangsan"
```
