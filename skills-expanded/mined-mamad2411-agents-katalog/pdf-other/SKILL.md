---
name: pdf-other
version: 1.0.0
description: "pdf-cli 其他模块：版本历史、系统公告、使用帮助。当用户需要查看版本更新、系统公告或使用指南时使用。"
metadata:
  requires:
    bins: ["pdf-cli"]
  cliHelp: "pdf-cli other --help"
---

# other

**CRITICAL — 开始前 MUST 先用 Read 工具读取 [`../pdf-shared/SKILL.md`](../pdf-shared/SKILL.md)，其中包含认证、配置、错误处理**

## 命令概览

| 命令 | 说明 | 需要登录 |
|------|------|----------|
| [`version`](references/pdf-other-version.md) | 查看版本历史 | 否 |
| [`notice`](references/pdf-other-notice.md) | 查看系统公告 | 否 |
| [`help-guide`](references/pdf-other-help.md) | 查看使用指南 | 否 |

## 快速开始

```bash
# 查看版本历史
pdf-cli other version

# 查看系统公告
pdf-cli other notice

# 查看使用指南
pdf-cli other help-guide
```
