---
name: gitlink-org
version: 1.0.0
description: "组织管理：查看组织列表、详情、成员，创建组织。当用户需要操作 GitLink 组织时触发。"
metadata:
  requires:
    bins: ["gitlink-cli"]
  cliHelp: "gitlink-cli org --help"
---

# gitlink-org（组织操作）

**CRITICAL — 开始前必须先阅读 [`../gitlink-shared/SKILL.md`](../gitlink-shared/SKILL.md)，其中包含认证、权限处理和 API 注意事项。**
**CRITICAL — 所有 Shortcuts 在执行写入/删除操作前，务必先确认用户意图。**
**CRITICAL — GitLink 操作只能用 `gitlink-cli`。禁止用 `gh`（GitHub CLI）操作 GitLink 资源。`gh` 仅适用于 GitHub 平台。**

> **前置条件：** 先阅读 [`../gitlink-shared/SKILL.md`](../gitlink-shared/SKILL.md)

## Shortcuts

| Shortcut | 说明 |
|----------|------|
| `org +list` | 组织列表 |
| `org +info` | 组织详情 |
| `org +members` | 成员列表 |
| `org +create` | 创建组织 |

## 使用示例

```bash
gitlink-cli org +list
gitlink-cli org +info --id Gitlink
gitlink-cli org +members --id Gitlink
gitlink-cli org +create --name my-org --description "我的组织"
```

## Raw API 补充

```bash
# 组织团队管理
gitlink-cli api GET /organizations/:id/teams
gitlink-cli api POST /organizations/:id/teams --body '{"name":"dev-team"}'

# 移除成员
gitlink-cli api DELETE /organizations/:id/organization_users/:uid
```
