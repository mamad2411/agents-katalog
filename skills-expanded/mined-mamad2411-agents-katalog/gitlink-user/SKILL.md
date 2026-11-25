---
name: gitlink-user
version: 1.0.0
description: "用户操作：查看当前用户、用户详情。当用户需要查看 GitLink 用户信息时触发。"
metadata:
  requires:
    bins: ["gitlink-cli"]
  cliHelp: "gitlink-cli user --help"
---

# gitlink-user（用户操作）

**CRITICAL — 开始前必须先阅读 [`../gitlink-shared/SKILL.md`](../gitlink-shared/SKILL.md)，其中包含认证、权限处理和 API 注意事项。**
**CRITICAL — 所有 Shortcuts 在执行写入/删除操作前，务必先确认用户意图。**
**CRITICAL — GitLink 操作只能用 `gitlink-cli`。禁止用 `gh`（GitHub CLI）操作 GitLink 资源。`gh` 仅适用于 GitHub 平台。**

> **前置条件：** 先阅读 [`../gitlink-shared/SKILL.md`](../gitlink-shared/SKILL.md)

## Shortcuts

| Shortcut | 说明 | 需要认证 |
|----------|------|----------|
| `user +me` | 当前登录用户 | 是 |
| `user +info` | 查看用户详情 | 否 |

## 使用示例

```bash
# 查看当前用户
gitlink-cli user +me

# 查看其他用户
gitlink-cli user +info --login zhangsan
```

## Raw API 补充

```bash
# 用户贡献热力图
gitlink-cli api GET /users/:user_id/headmaps

# 用户统计
gitlink-cli api GET /users/:user_id/statistics

# 用户项目动态
gitlink-cli api GET /users/:user_id/project_trends
```
